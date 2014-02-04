#!/usr/bin/env/python
#
# Pulls information from a redis queue created from redditcomments_redis.py to store into MongoDB
#
# Written by: Joe Engel
# Additional Contributers: Mark Lessel

import redis
import pymongo
import json
import time

m = pymongo.MongoClient(host='localhost').redistest 
db = redis.Redis('localhost')
		
while True:
	comment = db.lpop("comments")
	if not comment:
		print "Queue empty... retrying in 1 second"
		time.sleep(1)
		continue
	comment = json.loads(comment)
	m.comments.save(comment)
	print "Inserted commentID %s" % comment['_id']