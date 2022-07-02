from time import time
from time import sleep
import random

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py


# parameter constants that seem to deliver meaningful results
FEATURE_LIST = [300, 600, 1200, 3000]
COMPONENTS_LIST = [5, 10, 15, 20, 25]
DATA_COLUMN_CONSTANT = 'comment'

n_samples = None
n_features = None
n_components = None
n_top_words = 12

def plot_top_words(model, feature_names, n_top_words, title, modelName):
    fig, axes = plt.subplots(5, 5, figsize=(30, 15), sharex=True)
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
    fileName = modelName + "_numberOfFeature_" + str(n_features) + "_numberOfComponents_" + str(n_components) + "_numberOfTopWords_" + str(n_top_words)

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
    n_features = feature
    # inner loop that iterates over different number of components (topics)
    for component in COMPONENTS_LIST:
        print("Loading dataset...")
        t0 = time()

        df = pd.read_csv('../authorsPlusPosts_CLEANED.csv')
        dataList = df[DATA_COLUMN_CONSTANT].values.tolist()
        random.shuffle(dataList)

        data_samples = dataList[:n_samples]
        # Set samples Parameter to use all elements from corpus
        n_samples = len(data_samples)
        print("done in %0.3fs." % (time() - t0))

        n_components = component
        # Use tf-idf features for NMF.
        print("Extracting tf-idf features for NMF...")
        tfidf_vectorizer = TfidfVectorizer(
            max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
        )
        t0 = time()

        tfidf = tfidf_vectorizer.fit_transform(df[DATA_COLUMN_CONSTANT].apply(lambda x: str(x)))
        print("done in %0.3fs." % (time() - t0))

        # Use tf (raw term count) features for LDA.
        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(
            max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
        )
        t0 = time()

        tf = tf_vectorizer.fit_transform(df[DATA_COLUMN_CONSTANT].apply(lambda x: str(x)))
        print("done in %0.3fs." % (time() - t0))
        print()


        #Fit the NMF model
        print(
            "\n" * 2,
            # "Fitting the NMF model (generalized Kullback-Leibler "
            # "divergence) with tf-idf features, n_samples=%d and n_features=%d..."
            "Fitting the NMF model with tf-idf features, n_samples=%d and n_features=%d..."
            % (n_samples, n_features),
        )
        t0 = time()
        nmf = NMF(
            n_components=n_components,
            random_state=1,
            # beta_loss="kullback-leibler",
            beta_loss="frobenius",
            solver="mu",
            max_iter=1000,
            alpha=0.1,
            l1_ratio=0.5,
        ).fit(tfidf)
        print("done in %0.3fs." % (time() - t0))

        tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
        plot_top_words(nmf, tfidf_feature_names, n_top_words, "Topics in NMF model", "nmf")
        # plot_top_words(
        #     nmf,
        #     tfidf_feature_names,
        #     n_top_words,
        #     "Topics in NMF model (generalized Kullback-Leibler divergence)",
        #     "nmf"
        # )

        print(
            "\n" * 2,
            "Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
            % (n_samples, n_features),
        )
        lda = LatentDirichletAllocation(
            n_components=n_components,
            max_iter=5,
            learning_method="batch",
            learning_offset=50.0,
            random_state=0,
        )
        t0 = time()
        lda.fit(tf)
        print("done in %0.3fs." % (time() - t0))

        tf_feature_names = tf_vectorizer.get_feature_names_out()
        plot_top_words(lda, tf_feature_names, n_top_words, "Topics in LDA model", "lda")