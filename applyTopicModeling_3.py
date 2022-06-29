from time import sleep
import random

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# parameter constants that seem to deliver meaningful results (If not None, build a vocabulary that only consider the top
# max_features ordered by term frequency across the corpus.) so, more == better
FEATURE_LIST = [300, 600, 1200, 5000, 20000]
COMPONENTS_LIST = [5, 10, 15, 20, 25]

n_samples = None
n_features = None
n_components = None
n_top_words = 12

# import cleaned corpus, extract 'comment' column and shuffle list
df = pd.read_csv('authorsPlusPosts_CLEANED.csv')
dataList = df['comment'].values.tolist()
random.shuffle(dataList)

# Set samples Parameter to use all elements from corpus
n_samples = len(df['comment'])

def plot_top_words(model, feature_names, n_top_words, title, modelName):
    # fig, axes = plt.subplots(5, 5, figsize=(30, 15), sharex=True)
    fig, axes = plt.subplots(5, 5, figsize=(45, 25), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx +1}", fontdict={"fontsize": 30})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)

    # Save plots to directory
    # fileName = modelName + "_numberOfFeature_" + str(n_features) + "_numberOfComponents_" + str(n_components) + "_numberOfTopWords_" + str(n_top_words)
    fileName = modelName + "_numberOfFeature_" + str("No_treshold") + "_numberOfComponents_" + str(n_components) + "_numberOfTopWords_" + str(n_top_words)

    if modelName == "lda":
        plt.savefig(r"Plots\lda\\" + fileName)
    elif modelName == "nmf":
        plt.savefig(r"Plots\nmf\\" + fileName)
    else:
        plt.savefig(r"Plots\\" + fileName)
    sleep(5)
    plt.close()


# outer loop that iterates over different number of features
for feature in FEATURE_LIST:
    # set loop iteration feature variable
    n_features = feature

    # inner loop that iterates over different number of components (topics)
    for component in COMPONENTS_LIST:
        # set loop iteration component variable
        n_components = component

        # take given number of samples from whole corpus (in this case all of them)
        data_samples = dataList[:n_samples]

        # NMF vectorize, fit and plot
        # Use tf-idf features for NMF.
        tfidf_vectorizer = TfidfVectorizer(
            max_df=0.95, min_df=2, max_features=n_features
        )
        # tfidf = tfidf_vectorizer.fit_transform(df[DATA_COLUMN_CONSTANT].apply(lambda x: str(x)))
        tfidf = tfidf_vectorizer.fit_transform(data_samples)
        # tfidf = tfidf_vectorizer.fit_transform(data_samples.apply(lambda x: str(x)))
        nmf = NMF(
            n_components=n_components,
            random_state=1,
            beta_loss="kullback-leibler",
            solver="mu",
            max_iter=1000,
            alpha=0.1,
            l1_ratio=0.5,
        ).fit(tfidf)
        tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
        plot_top_words(nmf, tfidf_feature_names, n_top_words, "Topics in NMF model", "nmf")

        # LDA vectorize, fit and plot
        # Use tf (raw term count) features for LDA.
        tf_vectorizer = CountVectorizer(
            max_df=0.95, min_df=2, max_features=n_features
        )
        # tf = tf_vectorizer.fit_transform(df[DATA_COLUMN_CONSTANT].apply(lambda x: str(x)))
        tf = tf_vectorizer.fit_transform(data_samples)
        lda = LatentDirichletAllocation(
            n_components=n_components,
            max_iter=5,
            learning_method="batch",
            learning_offset=50.0,
            random_state=0,
        )
        lda.fit(tf)
        tf_feature_names = tf_vectorizer.get_feature_names_out()
        plot_top_words(lda, tf_feature_names, n_top_words, "Topics in LDA model", "lda")
        # https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py