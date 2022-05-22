import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.svm import LinearSVC
from sklearn import metrics
# nltk.download('stopwords')


def clean_text(text: str) -> str:
    """
    The basic text cleanup should do the following:
    1. remove html tags;
    2. extract emoticons from text;
    3. convert all letters to lowercase and remove numbers;
    4. remove punctuation marks;
    5. remove excessive spaces (e.g. before or after a block of text);
    6. Includes previously drawn emoticons in the text;
    """
    # extract emojis
    emojis = re.findall("\;[><()-]{1,2}|\:[><()-]{1,2}", text)
    text = re.sub("\;[><()-]{1,2}|\:[><()-]{1,2}", "", text)
    # remove html
    # text = re.sub("<.*?>", " ", text)
    #  cast lower, remove digits
    text = re.sub("\d", "", text.lower())
    # # remove interpunction
    text = re.sub("[^A-Za-z\s]+", "", text)
    # remove multi spaces
    text = re.sub("\s{2,}", " ", text)
    # add emojis to list of words
    clean_text = " ".join([text.strip(), " ".join(emojis)])
    return clean_text


def remove_eng_stopwords(words_list: list) -> list:
    """"""
    return [word for word in words_list if word not in stopwords.words()]


def porter_stem(words_list: list) -> list:
    """"""
    stemmer = PorterStemmer()
    return [stemmer.stem(plural) for plural in words_list]


def bow(words: list) -> dict:
    """"""
    uniques = list(set(words))
    return {unique: words.count(unique) for unique in uniques}


def tokenizer(true_raw):
    """"doc"""
    true_preprocessed = clean_text(true_raw)
    true_preprocessed_lst = true_preprocessed.split(" ")
    true_preprocessed_lst = remove_eng_stopwords(porter_stem(true_preprocessed_lst))
    return [word for word in true_preprocessed_lst if len(word) > 3]


def sum_over(transform, feature_names, axis):
    count = transform.sum(axis=axis)
    l1 = {}
    for i in range(1, 11):
        idx = np.argmax(count)
        if axis == 0:
            l1[i] = (feature_names[idx], count[idx])
        else:
            l1[i] = (count[idx], idx)
        count[idx] = 0

    return l1


def plot_results(data: dict):
    fig, ax = plt.subplots()

    labels = [i[0] for i in data.values()][::-1]
    values = [i[1] for i in data.values()][::-1]

    ax.barh(labels, values)

    for idx, val in enumerate(values):
        plt.text(val, idx, str(val))

    ax.set_xlabel('Ilosc wystapien')
    ax.set_title('Tokeny wystepujace tylko w tytulach prawdziwych tweetow')

    plt.show()


def table_resutls(data: dict):
    table = PrettyTable()
    table.field_names = ['Term', 'Count']

    for i in data.values():
        table.add_row(i)

    table.title = 'Tokeny wystepujace tylko w tytulach prawdziwych tweetow'
    print(table)


def vectorize(df):
    # TODO parametrize vectorizer
    vectorizer = CountVectorizer(tokenizer=tokenizer)

    title_transformed = vectorizer.fit_transform(df['verified_reviews'])

    splitted_data = train_test_split(
        title_transformed,
        df['rating'],
        test_size=0.33,
        random_state=1
    )
    return splitted_data


def fit_classifiers(splitted_data):
    X_train, X_test, y_train, y_test = splitted_data

    clfs = [
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        LinearSVC(),
        AdaBoostClassifier(),
        BaggingClassifier()
    ]

    for clf in clfs:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = metrics.confusion_matrix(y_test, y_pred, labels=clf.classes_)
        print(clf)
        print(metrics.classification_report(y_test, y_pred, labels=clf.classes_))
        disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
        disp.plot()
        plt.show()
