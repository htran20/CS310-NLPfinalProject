import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
from sklearn import naive_bayes
from sklearn.externals import joblib
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words


# create English stop words list
en_stop = get_stop_words('en')
remov_list = ["@", "#"]

# list for tokenized documents in loop
texts = []
tokenizer = RegexpTokenizer('(?u)\\b\\w\\w\\w+\\b')


def preprocessing(string):
    """
    Method for preprocessing data
    :param string: raw string
    :return: list of preprocessed word
    """
    raw = string.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    stopped_tokens = [i for i in stopped_tokens if not i[0] in remov_list]

    return stopped_tokens


def main():
    messages =[]
    scores =[]

    with open("cmt_file.txt") as f:
        list_cmt = f.read().split("\n")
        for cmt in list_cmt[:-1]:
            messages.append(cmt)

    count = 0
    with open("score_file.txt") as f:
        list_scores = f.read().split("\n")
        for score in list_scores[:-1]:
            if int(score) > 3:
                count += 1
                scores.append(1)
            else:
                scores.append(0)

    # #Addressing over-sampling by duplicate one copy of each negative review
    # negscores = []
    # negsents = []
    #
    # for cnt, i in enumerate(messages):
    #     if scores[cnt] == 0:
    #         negsents.append(i)
    #         negscores.append(0)
    #
    # messages += negsents
    # scores += negscores
    # #-------------------------------------------------

    # loop through document list
    for i in messages:
        # concatenate token as a string and add into texts
        pre_process_list = preprocessing(i)
        processed_text = " ".join(pre_process_list)
        texts.append(processed_text)

    # Use TF-IDF to transform pre-processed text to feature vector
    tf = TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True)
    X = tf.fit_transform(texts)
    print("number of reviews: ", X.shape[0])
    print("number of positive reviews: ", count)
    print("number of negative reviews: ", X.shape[0] - count)

    scores = np.array(scores)
    # Split data into two parts: 80% for training and 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, scores, test_size=0.2, shuffle=True)

    # Classifier to apply:
    classif = naive_bayes.MultinomialNB()
    # classif = LinearSVC()

    # Train the classifier
    classif.fit(X_train, y_train)

    # Predict using trained classfier
    y_pre = classif.predict(X_test)
    print(classification_report(y_test, y_pre))
    print(classification_report(y_train, classif.predict(X_train)))

    # Test with simple comments
    text = ["It is lovely and I love of it", "I don't like the food", "It is so terrible"]

    new_text = []
    for i in text:
        new_text.append([" ".join(preprocessing(i))])

    for cnt, i in enumerate(new_text):
        test = tf.transform(i)
        print(classif.predict(test))


if __name__ == '__main__':
    main()
