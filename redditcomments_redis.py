#!/usr/bin/env python
#
# Store reddit comments into a redis DB using praw and redis-py
#
# Written by Joe Engel
# Additional Contributers: Mark Lessel

import redis
import praw
import json



# Open a redis DB connection
db = redis.Redis(host='localhost')

# Create the reddit object, and pull comment stream from http://reddit.com/r/all/comments
r = praw.Reddit('Comment Parsing by /u/joeskyyy')
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
		db.rpush("comments", json.dumps(post))
		print "Inserted commentID: %s" % comment.id
