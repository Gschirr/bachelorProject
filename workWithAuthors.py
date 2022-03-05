import pandas as pd




firstAuthor = pd.read_csv("authorDir\\IamPsyduck.csv")

authorDict = {}
allMessages = ""

for index, row in firstAuthor.iterrows():
    comment = row.T.get("subredditToPost")
    allMessages += comment+" "

print("Breakpoint")



