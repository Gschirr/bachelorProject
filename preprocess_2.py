import pandas as pd
from time import time
import re
import nltk
from sklearn.feature_extraction import text

ADDITIONAL_STOP_WORDS = ['like', 'make', 'know', 'think', 'just', 'don\'t', 'want', 've', 'isn', 'able',
                         'http', 'say', 'lot', 'try', 'sorry', 'removed', 'doesn\'t', 'didn\'t', 'i\'ve',
                         'i\'ll', 'it\'ll', 'it\'s', 'i\'m', 'can\'t', 'won\'t', 'haven\'t', 'you\'re',
                         'wouldn\'t', 'i\'d', 'that\'s', 'there\'s', 'wasn\'t', 'isn\'t', 'what\'s',
                         'theyre', 'they\'re', 'use']

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

# adding additional Words to the stopword list that seem to add noise to the results
stop = list(text.ENGLISH_STOP_WORDS) + ADDITIONAL_STOP_WORDS


# lemmatization Helper
def lemmatize_text(text):
    text = [lemmatizer.lemmatize(w, pos='v') for w in w_tokenizer.tokenize(text)]
    text = ' '.join(text)
    return text

# long comments helper
def remove_ShortSentences(text):
    if (len(text) < 200):
        return None
    else:
        return text

# https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0
corpus = pd.read_csv("authorsPlusPosts.csv")

# rename column 'subredditToPost' to 'comment'
corpus.rename(columns={'subredditToPost' : 'comment'}, inplace=True)

# remove author_id column
corpus.drop(columns=['Unnamed: 0', 'author_id'],  inplace=True)

# drop all other columns except 'comment'
corpus = corpus[['comment']]

t0 = time()

# remove punctuation
corpus['comment'] = corpus['comment'].map(lambda x: re.sub('[,\.!?]', '', str(x)))

# lowercase everything
corpus['comment'] = corpus['comment'].map(lambda x: x.lower())

# remove URLs
corpus['comment'] = corpus['comment'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

# remove Emojis
filterOutNonAscii = lambda x: ord(x) < 256
corpus['comment'] = corpus['comment'].apply(lambda x: ''.join(filter(filterOutNonAscii, x)))

# remove subreddit names
corpus['comment'] = corpus['comment'].map(lambda x: re.sub('/?r/\w+/?', '', str(x)))

# remove newline (\n) (replace with 1 whitespace)
corpus['comment'] = corpus['comment'].str.replace(r'\n', ' ')

# remove double multiple whitespaces
corpus['comment'] = corpus['comment'].str.replace(' +', ' ')

# lemmatization
corpus['comment'] = corpus['comment'].apply(lemmatize_text)

# remove common english stopwords
corpus['comment'] = corpus['comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

# remove every row that has fewer than 200 characters
corpus['comment'] = corpus['comment'].apply(remove_ShortSentences)

# remove every non-Alphanumerical character that is left
corpus['comment'] = corpus['comment'].str.replace('[^a-zA-Z0-9 ]', '')


print("Corpus size before cleanup: " + str(len(corpus.index)))
# remove comments that are empty after cleanup
corpus.dropna(subset=['comment'], inplace=True)

print("Corpus size after cleanup: " + str(len(corpus.index)))

# export cleaned corpus to csv
corpus.to_csv("authorsPlusPosts_CLEANED.csv", encoding="utf-8")