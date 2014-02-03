#!/usr/bin/env/python

# Store a given users top 10 subreddits by karma 

import redis
import praw
import json

# Open up a redis and reddit connection
db = redis.Redis(host='localhost')
conn = praw.Reddit('Reddit/redis parsing by /u/joeskyyy')

# Limit how many subreddits to return
limit = 10

# User you wish to see
user_name = "joeskyyy"

# Retrieve the user obv and their submitted subreddits sorted by top scores
user = conn.get_redditor(user_name)
submitted = user.get_submitted(sort='top', limit=limit)

#db.rpush("karma", json.loads(submitted))

# For each subreddit the user has submitted to (limited by limit) store the subreddit name and karma
userlist = []

for sub in submitted:
	karma = {}
	karma['subreddit'] = sub.subreddit.display_name
	karma['karma'] = sub.score
	userlist.append(karma)

db.rpush("karma", json.dumps(userlist))

# Print the stored values
print db.lrange("karma", 0, -1)