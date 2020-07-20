# Load libraries
import sys
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import tree
# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# using dataset.tsv to generate train.tsv and test.tsv
def generate_dataset(filename):
    train_data = pd.read_csv(filename, sep='\t', header=None, nrows=4000)
    train_data.to_csv('train.tsv', sep='\t', header=None, index=False)
    test_data = pd.read_csv(filename, sep='\t', header=None, skiprows=4000)
    test_data.to_csv('test.tsv', sep='\t', header=None, index=False)


# load data from 'train.tsv' and 'test.tsv'
def load_data():
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    train_data = pd.read_csv(train_file, sep='\t', header=None)
    test_data = pd.read_csv(test_file, sep='\t', header=None)
    return train_data, test_data


def print_result(test_index, predicted_labels):
    for i in range(0, len(predicted_labels)):
        print(test_index[i], predicted_labels[i])
    return


def print_report():
    # print(valid_test_y, predicted_y)
    # print(DT_model.predict_proba(test_X_bag_of_words))
    print(classification_report(test_y, predicted_y))
    return


if __name__ == '__main__':
    # obtain data
    # generate_dataset('dataset.tsv')

    # load data
    train_data, test_data = load_data()

    train_X = np.array(train_data[1])
    train_y = np.array(train_data[2])

    test_index = np.array(test_data[0])
    test_X = np.array(test_data[1])
    test_y = np.array(test_data[2])

    # analyse with VADER
    predicted_y = []
    analyser = SentimentIntensityAnalyzer()
    for text in test_X:
        score = analyser.polarity_scores(text)
        if score['compound'] >= 0.05:
            predicted_y.append('positive')
        elif score['compound'] <= -0.05:
            predicted_y.append('negative')
        else:
            predicted_y.append('neutral')

    # print_result(test_index, predicted_y)
    print_report()
