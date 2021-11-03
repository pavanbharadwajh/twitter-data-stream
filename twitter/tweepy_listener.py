from tweepy.streaming import Stream
from google.cloud import pubsub_v1
import sys
import logging
import config

logger = logging.getLogger()


# Create publisher to publish data to GCP PUB/SUB
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(config.PROJECT_ID, config.TOPIC_ID)

# TwitterStream Api Listener
class listener(Stream):
    def on_data(self, raw_data):
        # logger.info("publishing tweet")
        print("publishing tweet")
        publisher.publish(topic_path, data= raw_data)
        return True

    def on_error(self, status):
        logger.error(status)
