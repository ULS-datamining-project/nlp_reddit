# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 00:27:29 2023

@author: Sebastian
"""

import praw


#Obtained from praw.ini file in working directory
reddit = praw.Reddit("uls-healthyeating", check_for_async=False)
print(reddit.read_only)

for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)
    
#It's ALIVE!