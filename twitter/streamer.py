import json
from datetime import datetime
import config
import logging

from google.cloud import bigquery

from keywords import MUSIC_SET
logger = logging.getLogger()


def collect_tweets(raw_data):
    data = json.loads(raw_data.decode())
    # if not data['retweeted'] and 'RT @' not in data['text']:
    if keyword_search(data):
        tweet = transform_data(data)
        write_tweets_to_bq(config.DATASET_ID, config.TABLE_ID, tweet)

def keyword_search(data):
    text = [x.lower() for x in data['text'].split()]
    hashtags = [i['text'].lower() for i in data['entities']['hashtags']]
    tweet_set = set().union(*[text, hashtags])
    if  tweet_set & MUSIC_SET:
        return True
    return False

def transform_data(data):
    transformed_data = dict()
    transformed_data['id'] = data['id']
    transformed_data['created_at'] = __to_datetime(data['created_at'])
    transformed_data['tweet_location'] = data['geo']
    transformed_data['text'] = data['text']
    transformed_data['retweet_count'] = data['retweet_count']
    transformed_data['favorite_count'] = data['favorite_count']
    transformed_data['user_name'] = data['user']['name']
    transformed_data['user_location'] = data['user']['location']
    transformed_data['user_followers_count'] = data['user']['followers_count']
    return transformed_data

def __to_datetime(timestamp):
    return datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")

def write_tweets_to_bq(dataset_id, table_id, tweets):
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    errors = client.insert_rows_json(table, [tweets])
    if not errors:
        logging.info('Loaded {} row(s) into {}:{}'.format(len([tweets]), dataset_id, table_id))
        print('Loaded {} row(s) into {}:{}'.format(len([tweets]), dataset_id, table_id))
    else:
        for error in errors:
            logging.error(error)