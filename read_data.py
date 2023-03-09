# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 00:27:29 2023

@author: Sebastian
"""

import praw
import pandas as pd
import datetime as time
from colorama import Fore, Style
from pathlib import Path

# Make data directory for newly written data if it doesn't already exist
DATA_DIRECTORY = "data/"
Path(DATA_DIRECTORY).mkdir(parents=True, exist_ok=True)

POST_TIME_PERIOD = "year"

# Number of posts per subreddit to pull
N_TITLES = 1000

#Obtained from praw.ini file in working directory
reddit = praw.Reddit("uls-healthyeating", check_for_async=False)

# Chose this multireddit as it has many food subreddits
food_multireddit = reddit.multireddit(name="food", redditor = "nomeii")

top_dict = {"subreddit" : [],
            "title" : [],
            "is_self" : [],
            "selftext" : [],
            "author" : [],
            "url" : [],
            "score" : [],
            "upvote_ratio" : [],
            "n_gilded" : [],
            "num_comments" : [],
            "permalink" : [],
            "created_utc" : []
            }

# Cycle over each of the subreddits, grab posts and append it to the
# global dictionary

for index,subreddit in enumerate(food_multireddit.subreddits):
    subreddit_name = subreddit.display_name
    
    #Subreddits to appear in red
    print("\n[", time.datetime.now(), "]", f"{Fore.RED}****{subreddit_name}****{Style.RESET_ALL}")
    print(f"Subreddit number: {index}")
    
    subreddit_data = subreddit.top(limit=N_TITLES, time_filter=POST_TIME_PERIOD)
    
    for post in subreddit_data:
        
        top_dict["subreddit"].append(subreddit_name)
        top_dict["title"].append(post.title)
        top_dict["is_self"].append(post.is_self)
        top_dict["selftext"].append(post.selftext)
        top_dict["author"].append(None if post.author is None else post.author.name)
        top_dict["url"].append(post.url)
        top_dict["score"].append(post.score)
        top_dict["upvote_ratio"].append(post.upvote_ratio)
        top_dict["n_gilded"].append(post.gilded)
        top_dict["num_comments"].append(post.num_comments)
        top_dict["permalink"].append(post.permalink)
        top_dict["created_utc"].append(post.created_utc)
    
# Combine dictionary into one large dataframe    
top_df = pd.DataFrame(top_dict)

top_df.to_csv(DATA_DIRECTORY + "raw_reddit_data.csv", index = False)
