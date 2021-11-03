import logging
from google.cloud import pubsub_v1

import config
from streamer import collect_tweets

logger = logging.getLogger()

# Create subscriber to get data from GCP PUB/SUB
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(config.PROJECT_ID, 'pub-sub-to-bq')
topic = subscriber.topic_path(config.PROJECT_ID, config.TOPIC_ID)

def callback(message):
    logger.info('Received message: {}'.format(message))
    collect_tweets(message.data)
    message.ack()

def receive_tweets():
    # print('hello')
    try:
        subscriber.get_subscription(request={"subscription": subscription_path})
    except Exception as e:
        # Not Found
        if e.code == 404:
            subscriber.create_subscription(
            name=subscription_path, topic=topic)
    
    future = subscriber.subscribe(subscription_path, callback= callback)
    try:
        future.result()
    except Exception as ex:
    # Close the subscriber if not using a context manager.
        subscriber.close()
        raise
    finally:
        future.cancel()

if __name__ == '__main__':
    receive_tweets()
    