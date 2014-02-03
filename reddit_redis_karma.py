#!/usr/bin/env/python

# Store a given users top 10 subreddits by karma 

import redis
import praw

# Open up a redis and reddit connection
db = redis.Redis(host='162.242.149.158')
conn = praw.Reddit('Reddit/redis parsing by /u/joeskyyy')

# Limit how many subreddits to return
limit = 10

# User you wish to see
user_name = "joeskyyy"

# Retrieve the user obv and their submitted subreddits sorted by top scores
user = conn.get_redditor(user_name)
submitted = user.get_submitted(sort='top', limit=limit)


# For each subreddit the user has submitted to (limited by limit) store the subreddit name and karma
for sub in submitted:
	subreddit = sub.subreddit.display_name
	db.rpush(user_name, '%s : %s' % (subreddit, sub.score))

# Print the stored values
print db.lrange(user_name, 0, -1)