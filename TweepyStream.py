import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

C_KEY = 'beirfmOXV0Ba2rp0fUurEfdJn'
C_SECRET = 'TAN4geV9cuFUfUGnKMVPqQO9byVUi7DVVkFcl4fqIIcqTuoqvM'
A_TOKEN_KEY = '1191389901675216897-NsZA5n1EdpvETLleS7sA2qSyGNOnPJ'
A_TOKEN_SECRET = '1l6LuU3B9yIFb9NIutUo0lUg9mIF63WGkL6Cs4vQHvO5Z'


# Create a StreamListener class
class MyListener(StreamListener):

    def __init__(self, time_limit=30):
        self.start_time = time.time()
        self.limit = time_limit
        self.outFile = open('BtcStreamTweets.json', 'w')
        super(MyListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            self.outFile.write(data.strip())
            self.outFile.write('\n')
            return True
        else:
            self.outFile.close()
            return False

    def on_error(self, status):
        if status == 420 or status == 502 or status == 429:
            print(status)
            self.outFile.close()
            return False
        elif status == 503 or status == 500 or status == 304:
            time.sleep(480)


auth = OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN_KEY, A_TOKEN_SECRET)
myStream = Stream(auth, MyListener(time_limit=86400))
myStream.filter(track=["Bitcoin","BTC"])
