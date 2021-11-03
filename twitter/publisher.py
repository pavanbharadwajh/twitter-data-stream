import config
from tweepy_listener import listener

def publish():
    twitter_stream = listener(config.TWITTER_CONSUMER_KEY,
                        config.TWITTER_CONSUMER_SECRET,
                        config.TWITTER_ACCESS_TOKEN,
                        config.TWITTER_ACCESS_TOKEN_SECRET)
    # Extract data related to particular track
    twitter_stream.filter(track=["Justin Beiber", "JustinBeiber", "#JustinBieber, #justinbeiber","justinbeiber"],
                         languages=['en'],
                         stall_warnings=True)
    
if __name__ == '__main__':
    publish()
