import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils import clean_text, porter_stem, remove_eng_stopwords, porter_stem, bow


if __name__ == "__main__":
    # ingest
    true_df = pd.read_csv("data/True.csv")
    true_raw = " ".join(true_df['title'].to_list())

    # preprocess
    true_preprocessed = clean_text(true_raw)
    true_preprocessed_lst = true_preprocessed.split(" ")
    true_preprocessed_lst = porter_stem(remove_eng_stopwords(true_preprocessed_lst))

    # clean
    bag_of_words = bow(true_preprocessed_lst)

    wc = WordCloud()
    wc.generate_from_frequencies(bag_of_words)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
