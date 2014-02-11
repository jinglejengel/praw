#!/usr/bin/env python
#
# Store reddit comments into a redis DB using praw and redis-py
#
# Written by Joe Engel
# Additional Contributers: Mark Lessel

import redis
from redis.sentinel import Sentinel
import praw
import json
import time

# Open a redis DB connection
db = Sentinel([('localhost', 26379), ('localhost',26380)], socket_timeout=0.1)
master = db.master_for('mymaster', socket_timeout=0.1)

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
                succeeded = False
                while not succeeded:
                        try:
                                succeeded = master.rpush("comments", json.dumps(post))
                        except:
                                print "Error! Failover detected, trying to locate new master"
                                master = db.master_for('mymaster', socket_timeout=0.1)
                                time.sleep(1)
                                continue
                print "Inserted commentID: %s" % comment.id