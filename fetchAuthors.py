import os

import pandas as pd
import time
from prawcore.exceptions import Forbidden
import praw
from psaw import PushshiftAPI
# to use PSAW
import loginCredentialsConfig

api = PushshiftAPI()
# to use PRAW

logCred = loginCredentialsConfig.Credentials
# create praw instance
reddit = praw.Reddit(
    client_id       = logCred.clientID,
    client_secret   = logCred.secretToken,
    username        = logCred.username,
    password        = logCred.password,
    user_agent      = logCred.userAgent
)

# gets all comments from one submission
subreddit = reddit.subreddit("android")

# collect submission authors name, id and submission id
dataSetAuthors = {
    "author_Id": [],
    "author": []
}

commentsList = []
# outer loop fetches all the submissions
start_time = time.time()
for submission in subreddit.hot(limit=1000):
    if submission.pinned == True or submission.stickied == True:
        continue

    dataSetAuthors["author_Id"].append(submission.name)
    dataSetAuthors["author"].append(submission.author)

    submission.comments.replace_more(limit=10)
    # inner loop fetches corresponding comments to submission
    for comment in submission.comments.list():
        if comment == None or comment.author == None:
            continue

        dataSetAuthors["author_Id"].append(comment.name)
        dataSetAuthors["author"].append(comment.author)

        print(20*"/")
        print("Comment Author: {}, comment: \n{}".format(comment.author, comment.body))
        print()

dataFrameAuthors = pd.DataFrame(dataSetAuthors)
dataFrameAuthors.drop_duplicates()

dataFrameAuthors.to_csv("dataFrameAuthors.csv", encoding="utf-8")
