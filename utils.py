import re
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
