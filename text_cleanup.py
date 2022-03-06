import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


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
    # remove html
    text = re.sub("<.*?>", " ", text)
    # extract emojis
    emojis = re.findall("[;:><()-]{2,3}", text)
    #  cast lower, remove digits
    text = re.sub("\d", "", text.lower())
    # # remove interpunction
    text = re.sub("[^A-Za-z\s]+", "", text)
    # remove multi spaces
    text = re.sub("\s{2,}", " ", text)
    # add emojis to list of words
    clean_text = text.strip().split(" ") + emojis
    # clean_text.extend(emojis)
    return clean_text


def remove_eng_stopwords(words_list: str) -> list:
    """"""
    return [word for word in words_list if word not in stopwords.words()]
