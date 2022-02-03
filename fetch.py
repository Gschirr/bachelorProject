import os

import pandas as pd
import datetime as dt
import time
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
dataSetSubmission = {
    "author": [],
    "author_Id": [],
    "submission_Id": []
    # "comment": []
}

commentsList = []
# outer loop fetches all the submissions
start_time = time.time()
for submission in subreddit.hot(limit=100):
    if submission.pinned == True or submission.stickied == True:
        continue
    # print(40*"Xx")
    # print("Submission Author: {}, Submission comment {}".format(submission.author, submission.selftext))
    # print()
    dataSetSubmission["author"].append(submission.author)
    dataSetSubmission["author_Id"].append(submission.author.id)
    dataSetSubmission["submission_Id"].append(submission.id)
    # dataSetSubmission["comment"].append(submission.selftext)


    submission.comments.replace_more(limit=10)
    # inner loop fetches corresponding comments to submission
    for comment in submission.comments.list():
        if comment == None or comment.author == None or comment.author.id == None:
            continue
        dataSetUserInSubmission = {}
        dataSetUserInSubmission["parent_submission"] = submission
        dataSetUserInSubmission["parent_submission_Id"] = submission.id
        dataSetUserInSubmission["author"] = comment.author
        # dataSetUserInSubmission["author_Id"] = comment.author.id
        dataSetUserInSubmission["comment"] = comment.body
        # dataSetUserInSubmission["comment_Id"] = comment.id

        print(20*"/")
        print("Comment Author: {}, comment: \n{}".format(comment.author, comment.body))
        print()
        commentsList.append(dataSetUserInSubmission)
        # dataFrameComment = pd.DataFrame(dataSetUserInSubmission, index=[comment.author.id])
        # print(dataFrameComment)

# create dataframe for every User with his corresponding posts to android is goal
dataFrameComment = pd.DataFrame(commentsList)
dataFrameSubmission = pd.DataFrame(dataSetSubmission)

print(dataFrameSubmission)
action = f"\t\t[Info] Elapsed time: {time.time() - start_time: .2f}s"
print(action)
# submissions = reddit.submission(id="sfgq5i")

# submission.comments.replace_more(limit=None)
# for comment in submission.comments.list():
#     print("Author: {}, comment: \n{}".format(comment.author, comment.body))

# df.to_csv("topPostsAndroid.csv", header=False, encoding="utf-8", index=False)
