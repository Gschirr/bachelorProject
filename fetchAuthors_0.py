import os

import pandas as pd
import time
import praw
from psaw import PushshiftAPI
from datetime import datetime
from datetime import date


# to use PSAW
import loginCredentialsConfig

api = PushshiftAPI()
# to use PRAW


# Initialization of the PRAW Reddit API Wrapper with Credentials from the Created Reddit Account
# Credentials are hidden within a config file to 1. avoid hardcoding them, 2. for Privacy reasons
logCred = loginCredentialsConfig.Credentials
# create praw instance
reddit = praw.Reddit(
    client_id       = logCred.clientID,
    client_secret   = logCred.secretToken,
    username        = logCred.username,
    password        = logCred.password,
    user_agent      = logCred.userAgent
)

# set subreddit in PRAW's reddit object, in this case it is the r/Android community
subreddit = reddit.subreddit("android")

# create python dict, with fields for the authors ID (internal Reddit id) as well as the authors name which is shown on
# on the plattform with his posts
dataSetAuthors = {
    "author_Id": [],
    "author": []
}



commentsList = []
# outer loop fetches all the submissions (alle Haupt-Posts)
start_time = time.time()
# Fetch from "Hot" Sorting because this has more userengagement
for submission in subreddit.hot(limit=1000):
    # Ignore pinned or stickied Posts, da diese eher Mod oder Infoposts sind
    if submission.pinned == True or submission.stickied == True:
        continue

    # add all the authors from those submissions to the dataframe
    dataSetAuthors["author_Id"].append(submission.name)
    dataSetAuthors["author"].append(submission.author)

    submission.comments.replace_more(limit=10)
    # inner loop fetches corresponding comments to submission
    for comment in submission.comments.list():
        # check if comment or author have been deleted to avoid code to run into exception
        if comment == None or comment.author == None:
            continue

        # add all the authors from the comments within the above mentioned submissions to the dataframe
        dataSetAuthors["author_Id"].append(comment.name)
        dataSetAuthors["author"].append(comment.author)

        print(20*"/")
        print("Comment Author: {}, comment: \n{}".format(comment.author, comment.body))
        print()

dataFrameAuthors = pd.DataFrame(dataSetAuthors)
dataFrameAuthors.drop_duplicates()

# fetched 04_06
dataFrameAuthors.to_csv("dataFrameAuthors.csv", encoding="utf-8")

now = datetime.now()
today = date.today()

current_time = now.strftime("%H:%M:%S")
print("Fetch ended at Current Time =", current_time)

print("On the: ", today)
