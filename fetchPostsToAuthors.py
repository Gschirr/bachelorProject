import pandas as pd
from praw.exceptions import RedditAPIException
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
    client_id       = logCred.clientID,    #if fetched Author == walkingdistances this or the next one throws error
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

    # i sometimes get a 404 Error in the following lines some Redditor object seems to be the problem but i cant find out why
    # https://praw.readthedocs.io/en/v3.6.2/pages/exceptions.html
    # and here a link to the most recent docs from PRAW = https://praw.readthedocs.io/en/latest/index.html
    if fetchedAuthor == None:
        continue

    else:
        authorObjects.append(fetchedAuthor)

    # Suspended/banned accounts will only return the name and is_suspended attributes.

# authorIds = dataFrameImportAuthors.get("author_Id")




# for author in dataFrameImportAuthors["author_Id"]:
for author in authorObjects:
    try:
        if hasattr(author, "is_suspended") or not hasattr(author, "comment_karma"):
            continue
        for comment in author.comments.new(limit=None):
            if comment.subreddit == "Android":
                authorPlusPosts["author"].append(author.name)
                authorPlusPosts["author_id"].append(author)
                authorPlusPosts["post"].append(comment)
                authorPlusPosts["subreddit"].append(comment.subreddit_name_prefixed)
                authorPlusPosts["subredditToPost"].append(comment.body)

                print(author.name)
                print(comment.subreddit_name_prefixed)


    except RedditAPIException as exception:
        for subexception in exception.items:
            print(subexception.error_type)

    except BaseException as error:
        dataFrameAuthorsWithPosts = pd.DataFrame(authorPlusPosts)
        dataFrameAuthorsWithPosts.to_csv("authorsPlusPostsException.csv", encoding="utf-8")
        print('An exception occurred: {}'.format(error))


dataFrameAuthorsWithPosts = pd.DataFrame(authorPlusPosts)
dataFrameAuthorsWithPosts.to_csv("authorsPlusPosts.csv", encoding="utf-8")