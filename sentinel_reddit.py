#!/usr/bin/env python
#
# Store reddit comments into a redis DB (backended with sentinel failover) using praw and redis-py
#
# Written by Joe Engel
# Additional Contributers: Mark Lessel - https://github.com/magglass1

import redis
from redis.sentinel import Sentinel
import praw
import json
import time

# Open a redis DB connection
db = Sentinel([('x.x.x.x', 26379), ('x.x.x.x', 26379), ('x.x.x.x', 26379)], socket_timeout=0.1)
master = db.master_for('mymaster', socket_timeout=0.1)

# Create the reddit object, and pull comment stream from http://reddit.com/r/all/comments
r = praw.Reddit('Comment Parsing by /u/joeskyyy')

# Failover function to re-assign a master ina failover scenario
def failover():
        print "Error! Failover detected, trying to locate new master"
        master = db.master_for('mymaster', socket_timeout=0.1)
        time.sleep(1)
        return master

while True:
		all_comments = r.get_comments('all')

        # Loop through the list of comments returned and store their id, content, author, subreddit, and permalink
		for comment in all_comments:
			post = {}
			post['_id'] = comment.id
			post['comment'] = comment.body
			post['author'] = str(comment.author)
			post['subreddit'] = str(comment.subreddit)
			post['permalink'] = comment.permalink
			# Catch an exception for failure before doing an insert
			succeeded = False
			while not succeeded:
				try:
					succeeded = master.rpush("comments", json.dumps(post))
				except (redis.exceptions.ResponseError, redis.exceptions.ConnectionError):
					master = failover()
					continue
			print "Inserted commentID: %s" % comment.id
