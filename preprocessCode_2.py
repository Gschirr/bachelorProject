import pandas as pd
import re
import nltk
from nltk import WordNetLemmatizer
from sklearn.feature_extraction import text

ADDITIONAL_STOP_WORDS = ['like', 'make', 'know', 'think', 'just', 'don\'t', 'want', 've', 'isn', 'able',
                         'http', 'say', 'lot', 'try', 'sorry', 'removed', 'doesn\'t', 'didn\'t', 'i\'ve',
                         'i\'ll', 'it\'ll', 'it\'s', 'i\'m', 'can\'t', 'won\'t', 'haven\'t', 'you\'re',
                         'wouldn\'t', 'i\'d', 'that\'s', 'there\'s', 'wasn\'t', 'isn\'t', 'what\'s',
                         'theyre', 'they\'re', 'use']

wordnet_lemmatizer = WordNetLemmatizer()
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

# Adding additional Words to the stopword list that seem to add noise to the results
stop = list(text.ENGLISH_STOP_WORDS) + ADDITIONAL_STOP_WORDS


# Lemmatization Helper
def lemmatize_text(text):
    temp = [lemmatizer.lemmatize(w, pos='v') for w in w_tokenizer.tokenize(text)]
    temp = ' '.join(temp)

    return temp

# Only keep long Comments Helper
def remove_ShortSentences(text):
    if (len(text) < 200):
        return None
    else:
        return text

# https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0
corpus = pd.read_csv("authorsPlusPosts.csv")

# rename column 'subredditToPost' to 'comment'
corpus.rename(columns={'subredditToPost':'comment'}, inplace=True)

# remove author_id column
corpus.drop(columns=['Unnamed: 0', 'author_id'],  inplace=True)

# Remove punctuation
corpus['comment_noPunctuation'] = corpus['comment'].map(lambda x: re.sub('[,\.!?]', '', str(x)))

# lowercase everything
corpus['comment_lowercase'] = corpus['comment_noPunctuation'].map(lambda x: x.lower())

# Remove URLs
corpus['comment_noLinks'] = corpus['comment_lowercase'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

# Remove Emojis
filterOutNonAscii = lambda x: ord(x) < 256
corpus['comment_noEmoji'] = corpus['comment_noLinks'].apply(lambda x: ''.join(filter(filterOutNonAscii, x)))

# Remove subreddit names
corpus['comment_noSubreddits'] = corpus['comment_noEmoji'].map(lambda x: re.sub('/?r/\w+/?', '', str(x)))

# Remove newline (\n) (replace with 1 whitespace)
corpus['comment_noNewline'] = corpus['comment_noSubreddits'].str.replace(r'\n', ' ')

# Remove double multiple whitespaces
corpus['comment_singleWhitespace'] = corpus['comment_noNewline'].str.replace(' +', ' ')

# Lemmatization
corpus['text_lemmatized'] = corpus['comment_singleWhitespace'].apply(lemmatize_text)

# Remove common english stopwords
corpus['comment_noStopwords'] = corpus['text_lemmatized'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

# Remove every row that has fewer than 75 characters
corpus['comment_noShortSentences'] = corpus['comment_noStopwords'].apply(remove_ShortSentences)

# Remove every non-Alphanumerical character that is left
corpus['comment_alphanumerical'] = corpus['comment_noShortSentences'].str.replace('[^a-zA-Z0-9 ]', '')

# Remove comments that are empty after cleanup
corpus = corpus[['comment_alphanumerical']]



print("Size before: " + str(len(corpus.index)))
corpus.dropna(subset=['comment_alphanumerical'], inplace=True)
print("Size after: " + str(len(corpus.index)))

corpus.to_csv("authorsPlusPosts_CLEANED.csv", encoding="utf-8")