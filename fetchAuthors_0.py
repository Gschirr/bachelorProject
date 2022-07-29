import pandas as pd
import praw
import loginCredentialsConfig


# initialization of the PRAW Reddit API Wrapper with Credentials from the Created Reddit Account
# credentials are hidden within a config file to 1. avoid hardcoding them, 2. for privacy reasons
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

# outer loop fetches all the submissions
# Fetch from "Hot" Sorting because this has more user-engagement
for submission in subreddit.hot(limit=1000):
    # Ignore pinned or stickied Posts, because those are almost exclusively used for moderation purposes
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

dataFrameAuthors.to_csv("dataFrameAuthors.csv", encoding="utf-8")