import streamlit as st
import pandas as pd
#import numpy as np
import streamlit.components.v1 as components
import requests
#pip install tweepy
import tweepy

def theTweet(tweet_url):
    """return json[html] for each tweet"""
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]
    return res

def app():

    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAOpRZwEAAAAA7FNAJekf0XHje2UC7t2uvZier5I%3DDBUMPAglhoB4TZoJPYQrWqFXR90kiBa6gdxIZCX0Vnb3u60BRs')

    #query tweets on bikes/berlin/theft
    query = 'berlin (fahrrad OR bike OR bicycle OR rad OR fahrraddiebstahl OR biketheft)' #(fahrraddiebstahl OR biketheft OR diebstahl OR theft)

    # get 10 tweets
    tweets = client.search_recent_tweets(query=query,
                                        tweet_fields=['id', 'created_at'],
                                        max_results=10)
    # 10 tweets to df
    twitter_df = pd.DataFrame(tweets[0])

    # create url per each tweet in df
    twitter_df["url"] = twitter_df["id"].apply(lambda x: f"https://twitter.com/twitter/statuses/{x}")

    #add title
    st.title("Latest tweets about bikes in Berlin")

    ####----FIRST TWEET----####
    tweet_url_1 = twitter_df.head(3)["url"][0]
    res_1 = theTweet(tweet_url_1)
    components.html(res_1,height= 500)
    ####----SECOND TWEET----####
    tweet_url_2 = twitter_df.head(3)["url"][1]
    res_2 = theTweet(tweet_url_2)
    components.html(res_2,height= 500)
    ####----THIRD TWEET----####
    tweet_url_3 = twitter_df.head(3)["url"][2]
    res_3 = theTweet(tweet_url_3)
    components.html(res_3,height= 500)
