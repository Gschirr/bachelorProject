import pandas as pd
from praw.exceptions import RedditAPIException
from prawcore.exceptions import Forbidden
import praw
# from psaw import PushshiftAPI
# to use PSAW
import loginCredentialsConfig
from itertools import islice


# api = PushshiftAPI()
# to use PRAW

logCred = loginCredentialsConfig.Credentials
# create praw instance
reddit = praw.Reddit(
    client_id       = logCred.clientID,    #if fetched Author == walkingdistances this or the next one throws error
    client_secret   = logCred.secretToken,
    username        = logCred.username,
    password        = logCred.password,
    user_agent      = logCred.userAgent
)

# import prefetched authors from csv file
dataFramePosts = pd.read_csv("authorsPlusPosts.csv")
dataFramePosts = dataFramePosts.iloc[:, 1:]
dataFramePosts = dataFramePosts.drop(columns=["author_id"])

#
dataFramePosts.to_csv("dataFramePosts.csv", encoding="utf-8", index=False)

# dataFramePostsPOLISHED = pd.read_csv("dataFramePosts.csv")
#
# # print("Breakpoint")
#
#
# #
# #  take author name into variable and save line to new array
# authorArray = []
# currentAuthor = dataFramePostsPOLISHED.loc[0].get("author")
# authorArray.append(dataFramePostsPOLISHED.loc[0])
# for index, row in islice(dataFramePostsPOLISHED.iterrows(), 1, None):
#     if row.T.get("author") == currentAuthor:
#         # check if next line author is same, if so take line into same array
#         authorArray.append(row)
#
#     else:
#         # if not, save array and start from step 1
#         fileName = "authorDir\\" + currentAuthor + ".csv"
#         authorDf = pd.DataFrame(authorArray)
#         authorDf.to_csv(fileName, encoding="utf-8", index=False)
#
#         currentAuthor = row.T.get("author")
#         authorArray.clear()
#         authorArray.append(row)





# print("Breakpoint")