# Load libraries
import sys
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import tree
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


"""
ABOUT CONTENT PRE-PROCESSING:
1. remove url: substitute url to ' '
2. remove junk characters: substitute junk_characters to ''(empty)
3. set word to be at least two letters
"""


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


def remove_stop_words(line):
    all_stop_words = set(stopwords.words('english'))  # get all stopwords
    line_words = line.split(' ')
    temp_words = []
    for word in line_words:
        if word not in all_stop_words:
            temp_words.append(word)
        else:
            continue
    result_line = ' '.join(temp_words)
    return result_line


def apply_stem_words(line):
    poster_stemer = PorterStemmer()
    line_words = line.split(' ')
    temp_words = []
    for word in line_words:
        temp_words.append(poster_stemer.stem(word))
    result_line = ' '.join(temp_words)
    return result_line


# preporcessing all content
def contents_pre_processing_without_stopwords_stem(contents):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[!*(),]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    junk_char_pattern = re.compile(r'[^a-zA-Z0-9@#$_%\s]')
    final_contents = []
    for line in contents:
        line_rm_url = re.sub(url_pattern, ' ', line)  # remove urls
        line_rm_junk = re.sub(junk_char_pattern, '', line_rm_url)
        final_contents.append(line_rm_junk)
    final_contents = np.array(final_contents)
    return final_contents


def contents_pre_processing_with_stopwords_stem(contents):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[!*(),]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    junk_char_pattern = re.compile(r'[^a-zA-Z0-9@#$_%\s]')
    final_contents = []
    for line in contents:
        line_rm_url = re.sub(url_pattern, ' ', line)  # remove urls
        line_rm_junk = re.sub(junk_char_pattern, '', line_rm_url)
        line_rm_stopwords = remove_stop_words(line_rm_junk)
        line_stem_words = apply_stem_words(line_rm_stopwords)
        final_contents.append(line_stem_words)
    final_contents = np.array(final_contents)
    return final_contents


# create count vectorizer and fit it with training data
def create_count_vectorizer(train_X, test_X):
    # set word to be at least two letters using 'token_pattern'
    # max_features indicates the top n frequency words in bag_of_words

    count = CountVectorizer(token_pattern='[a-zA-Z0-9@#$_%]{2,}', max_features=1000, lowercase=False)
    # count = CountVectorizer(token_pattern='[a-zA-Z0-9@#$_%]{2,}', max_features=1000, lowercase=False)
    train_X_bag_of_words = count.fit_transform(train_X)

    # transform the test data into bag of words creaed with fit_transform
    test_X_bag_of_words = count.transform(test_X)
    return train_X_bag_of_words, test_X_bag_of_words


def print_result(test_index, predicted_labels):
    for i in range(0, len(predicted_labels)):
        print(str(test_index[i]), predicted_labels[i])
    return


def print_report():
    # print(valid_test_y, predicted_y)
    # print(DT_model.predict_proba(test_X_bag_of_words))
    print(classification_report(valid_test_y, predicted_y, zero_division=0))
    return


if __name__ == '__main__':
    # obtain data
    # generate_dataset('dataset.tsv')

    # load data
    train_data, test_data = load_data()

    unvalid_train_X = np.array(train_data[1])
    valid_train_y = np.array(train_data[2])

    valid_test_index = np.array(test_data[0])
    unvalid_test_X = np.array(test_data[1])
    valid_test_y = np.array(test_data[2])

    # preprocessing data (without stopwords and stem)--> get valid trainX and testX
    valid_train_X = contents_pre_processing_without_stopwords_stem(unvalid_train_X)
    valid_test_X = contents_pre_processing_without_stopwords_stem(unvalid_test_X)

    # valid_train_X = contents_pre_processing_with_stopwords_stem(unvalid_train_X)
    # valid_test_X = contents_pre_processing_with_stopwords_stem(unvalid_test_X)

    # create bag_of_words using count vectorizer
    train_X_bag_of_words, test_X_bag_of_words = create_count_vectorizer(valid_train_X, valid_test_X)

    # create model for Decision Tree
    # if random_state id not set. the feaures are randomised, therefore tree may be different each time
    # print("----Decision Tree Model:")
    clf = tree.DecisionTreeClassifier(min_samples_leaf=int(0.01 * len(valid_train_X)), criterion='entropy', random_state=0)
    DT_model = clf.fit(train_X_bag_of_words, valid_train_y)

    # predict and print results
    predicted_y = DT_model.predict(test_X_bag_of_words)
    print_result(valid_test_index, predicted_y)
    # print_report()
