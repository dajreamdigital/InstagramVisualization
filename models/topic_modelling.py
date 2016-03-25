from __future__ import print_function
import utils
import numpy as np
import pandas as pd
import os
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

n_samples = 2000
n_features = 10000
n_topics = 50
n_top_words = 20

def topic_LDA(data):

    data_samples = data

	# Use tf (raw term count) features for LDA.
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
    t0 = time()
    tf = tf_vectorizer.fit_transform(data_samples)
    print("done in %0.3fs." % (time() - t0))

    # Fit the LDA model
    print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..." % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=2, learning_method='online', learning_offset=50., random_state=0)

    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))

    dist = lda.transform(tf)

    return pd.DataFrame(data=dist[0:,0:])


def topic_NMF(data):

    data_samples = data

    # Use tf-idf features for NMF.
    print("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')

    t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(data_samples)
    print("done in %0.3fs." % (time() - t0))

    # Fit the NMF model
    print("Fitting the NMF model with tf-idf features,"
        "n_samples=%d and n_features=%d..."
        % (n_samples, n_features))

    t0 = time()
    nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)
    print("done in %0.3fs." % (time() - t0))

    print("\nTopics in NMF model:")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    dist = nmf.transform(tfidf)

    return pd.DataFrame(data=dist[0:,0:])

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
