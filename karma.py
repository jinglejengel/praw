#!/usr/bin/env/python

import praw

user_agent = ("Low API Testing from /u/joeskyyy")

# Limit how many subreddits to return
limit = 10

# User you wish to see
user_name = "joeskyyy"

r = praw.Reddit(user_agent=user_agent)
user = r.get_redditor(user_name)
gen = user.get_submitted(limit=limit)
karma_by_subreddit = {}
for thing in gen:
	subreddit = thing.subreddit.display_name
	karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)
print karma_by_subreddit
