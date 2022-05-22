import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils import (
    remove_eng_stopwords,
    clean_text,
    porter_stem,
    vectorize,
    fit_classifiers,
    bow
)


if __name__ == "__main__":
    data = pd.read_csv('data/alexa_reviews.csv', sep=";", encoding='cp1252')

    values_mapping = {1: "Low", 2: "Neutral", 3: "Neutral", 4: "Neutral", 5: "High"}

    data = data[['rating', 'verified_reviews']]
    data = data.replace({"rating": values_mapping})

    data_raw = " ".join(data['verified_reviews'].to_list())
    data_processed = clean_text(data_raw)
    data_processed_lst = data_processed.split(" ")
    data_processed_lst = porter_stem(remove_eng_stopwords(data_processed_lst))

    bag_of_words = bow(data_processed_lst)
    wc = WordCloud()
    wc.generate_from_frequencies(bag_of_words)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    data = vectorize(data)
    fit_classifiers(data)
