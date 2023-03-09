# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:22:57 2023

@author: Sebastian
"""

from transformers import pipeline
import pandas as pd

classifier = pipeline("sentiment-analysis", "distilbert-base-uncased-finetuned-sst-2-english")

raw_data = pd.read_csv("data/raw_reddit_data.csv")
subreddit_health = pd.read_csv("data/subreddit_health.csv")

#Merge assessment of subreddit health with subreddit data
reddit_data = raw_data.merge(subreddit_health, on = "subreddit")

# Run sentiment analysis on each    

#reddit_head = reddit_data.copy().loc[0:5,]
#reddit_head.loc[:,('label', 'score')] = reddit_head.title.apply(classifier).explode().apply(pd.Series)
import datetime as time

print(time.datetime.now())
reddit_data.loc[:,('label', 'score')] = reddit_data.title.apply(classifier).explode().apply(pd.Series)
print(time.datetime.now())
reddit_data.rename(columns = {"label" : "sentiment_label", "score" : "sentiment_score"})

reddit_data.to_csv("data/reddit_data_sentiment.csv", index = False)