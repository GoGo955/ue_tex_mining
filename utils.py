import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
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
