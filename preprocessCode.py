import random

import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition
import matplotlib.pyplot as plt
import numpy as py
import re
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split



df = pd.read_csv('dataFramePosts.csv')


authorPosts_df = df[['author', 'subredditToPost']].rename(columns={'subreditToPost':'post'})

random.shuffle(authorPosts_df)

print(authorPosts_df)


n_features = 1000
n_components = 5
n_top_words = 20

tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english', ngram_range=(1, 2))
tf = tf_vectorizer.fit_transform(authorPosts_df)

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
max_features=n_features, stop_words='english', ngram_range=(1, 2))
tfidf = tfidf_vectorizer.fit_transform(authorPosts_df)

lda = LatentDirichletAllocation(n_components=n_components, random_state=1).fit(tf)

def get_model_topics(model, vectorizer, topics, n_top_words=n_top_words):
    word_dict = {}
    feature_names = vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        word_dict[topics[topic_idx]] = top_features

    return pd.DataFrame(word_dict)

def get_inference(model, vectorizer, topics, text, threshold):
    v_text = vectorizer.transform([text])
    score = model.transform(v_text)

    labels = set()
    for i in range(len(score[0])):
        if score[0][i] > threshold:
            labels.add(topics[i])

    if not labels:
        return 'None', -1, set()

    return topics[np.argmax(score)], score, labels