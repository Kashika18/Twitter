import tweepy
import pandas as pd
import csv
import os

consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']
access_key=os.environ['access_key']
access_secret=os.environ['access_secret']

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#getting all tweets of a user
def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #initializing a list to hold all the tweepy Tweets
	alltweets = []  
    
    #making initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #saving most recent tweets
	alltweets.extend(new_tweets)
    
    
    
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0 and len(new_tweets)<1000:
        
		#saving the id of the oldest tweet less one
		oldest = alltweets[-1].id -1
		
		print(f"getting tweets before {oldest}")
        
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
		alltweets.extend(new_tweets)
        
		print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    #write the csv  
	with open(f'new_{screen_name}_tweets.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	users_locs = [[tweet.user.created_at,tweet.text] for tweet in alltweets]
	
	tweet_text = pd.DataFrame(data=users_locs,columns=['Created_at', "Text"])
	
	print(tweet_text.head())

	pass

		
if __name__ == '__main__':
	#pass in the username of the account you want to download
	user_name = input("Enter the user name")
	get_all_tweets(user_name)