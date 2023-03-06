# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 00:27:29 2023

@author: Sebastian
"""

import praw
import pandas as pd
import datetime as time
from colorama import Fore, Style

#Obtained from praw.ini file in working directory
reddit = praw.Reddit("uls-healthyeating", check_for_async=False)

food_multireddit = reddit.multireddit(name="food", redditor = "nomeii")

top_dict = {"subreddit" : [],
            "title" : [],
            "is_self" : [],
            "url" : [],
            "upvote_ratio" : [],
            "num_comments" : [],
            "permalink" : []
            }


N_TITLES = 1000

for index,subreddit in enumerate(food_multireddit.subreddits):
    subreddit_name = subreddit.display_name
    
    #Weird codes are to get text in red
    print("\n[", time.datetime.now(), "]", f"{Fore.RED}****{subreddit_name}****{Style.RESET_ALL}")
    print(f"Subreddit number: {index}")
    
    subreddit_data = subreddit.top(limit=N_TITLES, time_filter="year")
    
    for post in subreddit_data:
        
        top_dict["subreddit"].append(post.subreddit)
        top_dict["title"].append(post.title)
        top_dict["is_self"].append(post.is_self)
        top_dict["url"].append(post.url)
        top_dict["upvote_ratio"].append(post.upvote_ratio)
        top_dict["num_comments"].append(post.num_comments)
        top_dict["permalink"].append(post.permalink)
    
top_df = pd.DataFrame(top_dict)

top_df.to_csv("reddit_data.csv", index = False)
