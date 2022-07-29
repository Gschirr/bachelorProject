# https://praw.readthedocs.io/en/v3.6.2/pages/exceptions.html
# https://praw.readthedocs.io/en/latest/index.html
import pandas as pd
import praw
import loginCredentialsConfig
from praw.exceptions import RedditAPIException
from psaw import PushshiftAPI


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

# import prefetched authors from csv file
dataFrameImportAuthors = pd.read_csv("dataFrameAuthors.csv")

# final dict where all authors with their corresponding posts to r/Android are saved
authorPlusPosts = {
    "author": [],
    "author_id": [],
    "post": [],
    "subreddit": [],
    "subredditToPost": []
}


# remove first column "Unnamed: 0" and delete duplicates
dataFrameImportAuthors = dataFrameImportAuthors.iloc[:, 1:]
dataFrameImportAuthors = dataFrameImportAuthors.drop_duplicates(subset="author")

# list where praw api instance fetches all author objects from reddit
authorObjects = []


# iterate through dataframe with author names and fetch corresponding Redditor-object from reddit
for index, row in dataFrameImportAuthors.iterrows():
    temp = row["author"]
    fetchedAuthor = reddit.redditor(temp)
    print(fetchedAuthor.name)

    if fetchedAuthor == None:
        continue

    else:
        authorObjects.append(fetchedAuthor)


for author in authorObjects:
    try:
        if hasattr(author, "is_suspended") or not hasattr(author, "comment_karma"):
            continue
        for comment in author.comments.new(limit=None):
            if comment.subreddit == "Android":
                authorPlusPosts["author_id"].append(author)
                authorPlusPosts["subredditToPost"].append(comment.body)

                print(author.name)
                print(comment.subreddit_name_prefixed)


    except RedditAPIException as exception:
        for subexception in exception.items:
            print(subexception.error_type)

    except BaseException as error:
        print('An exception occurred: {}'.format(error))


dataFrameAuthorsWithPosts = pd.DataFrame(authorPlusPosts)
dataFrameAuthorsWithPosts.to_csv("authorsPlusPosts.csv", encoding="utf-8")