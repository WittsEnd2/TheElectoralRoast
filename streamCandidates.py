from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import unicodedata
import emoji

ckey = '9QNHTvlJIUm6nW0xZfCQrbv1c'
csecret = 'H8poLEFkwNM0PoBxSvzHsF0c3l3PJEUI8DPvEJnWuKQOCw5BRJ'
atoken = '199110460-MbCtBAwLlxDd54qiV73uebJglTPTfAYZ6Z8zDCYo'
asecret = 'MNLqjreqgEwihGYgqkvexJ0JZlgNbAltfyfuwDHaOyPMX'
trump = open("trump.txt", "a")
clinton = open("clinton.txt", "a")
bernie = open("bernie.txt", "a")
rubio = open("rubio.txt", "a")
cruz = open("cruz.txt", "a")
class listener(StreamListener):
	def on_data(self, data):
		
		data = str(emoji.demojize(data))
		
		decoded = json.loads(str(data))
		if 'place' in decoded and decoded['place'] is not None:
			loc = decoded['place']['bounding_box']['coordinates'][0][0]
			
			tweet = str(emoji.demojize(decoded['text']).encode("unicode_escape"))
			tweet = tweet[1:]
			tweet = tweet.strip("\n")
			tweet = tweet.strip("\.")

			tweet = tweet.replace("\n",". ")
			tweet = tweet.replace("\\'","'")
			tweet = tweet.replace("\\","")
			tweet = tweet.replace("\\\.",".")
			tweet = tweet.replace("\"", "'")
			tweet = tweet.replace("\\n",". ")
			print (tweet)
			tweetLower = tweet.lower()
			if("trump" in tweetLower):
				trump.write('{"tweet": "' + tweet +'", "coordinates": ' + str(loc) + '}\n')
				trump.flush()
			if("sanders" in tweetLower or "bernie" in tweet.lower()):
				bernie.write('{"tweet": "' + tweet +'", "coordinates": ' + str(loc) + '}\n')
				bernie.flush()
			if("clinton" in tweetLower):
				clinton.write('{"tweet": "' + tweet +'", "coordinates": ' + str(loc) + '}\n')
				clinton.flush()
			if("rubio" in tweetLower):
				rubio.write('{"tweet": "' + tweet +'", "coordinates": ' + str(loc) + '}\n')
				rubio.flush()
			if("cruz" in tweetLower):
				cruz.write('{"tweet": "' + tweet +'", "coordinates": ' + str(loc) + '}\n')
				cruz.flush()
		return True
	def on_error(self, status):
		print (status)
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(languages=["en"], track={"Trump", "Sanders", "Bernie", "Clinton", "Rubio", "Cruz"})
