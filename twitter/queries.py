from google.cloud import bigquery
import config
client = bigquery.Client()

# Replace the TABLE ID in the FROM clause to match your table ID

# Perform Query- 1.
# Produce a count of all tweets consumed
QUERY = ('SELECT COUNT(*) AS total_tweets FROM `twitter-stream-330604.tweets_dataset.tweets`')
query_job = client.query(QUERY)  
rows = query_job.result()

for row in rows:
    print(f'Total Tweets = {row["total_tweets"]}')

# Perform Query- 2.
# Produce a count of unique tweets
QUERY = ('SELECT COUNT(*) AS unique_tweets FROM `twitter-stream-330604.tweets_dataset.tweets` where text NOT LIKE "RT @%"')
query_job = client.query(QUERY)
rows = query_job.result()

for row in rows:
    print(f'Unique Tweets = {row["unique_tweets"]}')