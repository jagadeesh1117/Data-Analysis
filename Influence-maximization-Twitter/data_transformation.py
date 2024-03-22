# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 23:58:24 2021

@author: Jagadeesh
"""
class TweetGrabber():
    
    def __init__(self,myApi,sApi,at,sAt):
        import tweepy
        self.tweepy = tweepy
        auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
        auth.set_access_token("access_key", "access_secret")
        self.api = tweepy.API(auth)
        
        
    def strip_non_ascii(self,string):
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)
        
    def keyword_search(self,keyword,csv_prefix):
        import csv        
        API_results = self.api.search(q=keyword,rpp=1000,show_user=True,tweet_mode='extended')

        with open(f'{csv_prefix}.csv', 'w',encoding='utf-8', newline='') as csvfile:
            fieldnames = ['tweet_id', 'tweet_text', 'date', 'user_id', 'follower_count',
                          'retweet_count','user_mentions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in API_results:
                text = self.strip_non_ascii(tweet.full_text)
                date = tweet.created_at.strftime('%m/%d/%Y')        
                writer.writerow({
                                'tweet_id': tweet.id_str,
                                'tweet_text': text,
                                'date': date,
                                'user_id': tweet.user.id_str,
                                'follower_count': tweet.user.followers_count,
                                'retweet_count': tweet.retweet_count,
                                'user_mentions':tweet.entities['user_mentions']
                                })        
        
    def user_search(self,user,csv_prefix):
        import csv
        API_results = self.tweepy.Cursor(self.api.user_timeline,id=user,tweet_mode='extended').items()
        with open(f'{csv_prefix}.csv', 'w',encoding='utf-8', newline='') as csvfile:
            
            fieldnames = ['tweet_id', 'tweet_text', 'date', 'user_id', 'user_mentions', 'retweet_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in API_results:
                text = self.strip_non_ascii(tweet.full_text)
                date = tweet.created_at.strftime('%m/%d/%Y')        
                writer.writerow({
                                'tweet_id': tweet.id_str,
                                'tweet_text': text,
                                'date': date,
                                'user_id': tweet.user.id_str,
                                'user_mentions':tweet.entities['user_mentions'],
                                'retweet_count': tweet.retweet_count
                                })     
    

t = TweetGrabber(
    myApi = 'value',
    sApi = 'value',
    at = 'value',
    sAt = 'value')
t.user_search(user='Tesla',csv_prefix='tesla_tweets')
t.user_search(user='elonmusk',csv_prefix='elon_tweets')

import data_write
data_write.second_code()
