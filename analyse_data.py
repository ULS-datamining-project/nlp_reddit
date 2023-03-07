# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 22:22:55 2023

@author: Sebastian
"""

import pandas as pd
# import huggingface libraries
#import transformers  as tr


raw_data = pd.read_csv("data/reddit_data.csv")
subreddit_health = pd.read_csv("data/subreddit_health.csv")

#Merge assessment of subreddit health with subreddit data
reddit_data = raw_data.merge(subreddit_health, on = "subreddit")


