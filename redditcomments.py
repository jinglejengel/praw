#!/usr/bin/env python
#
# Simple Comment Parser which uses praw (Python API for Reddit) and pymongo (Python driver for MongoDB) to store certain comment attributes into
# a MongoDB Database.
#
# Written by Joe Engel


import pymongo
import praw
import time

#Open MongoDB Connection to DB "reddit"
db = pymongo.MongoClient().reddit

#Create the reddit object, and pull comment stream from http://reddit.com/r/all/comments
r = praw.Reddit('Comment Parsing by /u/joeskyyy')
while True:
        all_comments = r.get_comments('all')

        #Loop through the list of comments returned and store their id, content, author, subreddit, and permalink if the comment has not already been stored
        for comment in all_comments:
                if not db.comments.find_one({'_id':comment.id}):
                        db.comments.insert({'_id':comment.id, 'comment':comment.body, 'author': str(comment.author), 'subreddit': str(comment.subreddit), 'permalink': comment.permalink})
                        print "Inserted commentID: %s" % comment.id
