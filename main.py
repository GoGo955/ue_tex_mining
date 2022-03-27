import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from utils import tokenizer


if __name__ == "__main__":
    # ingest
    true_df = pd.read_csv("data/True.csv", nrows=1000)
    true_raw = " ".join(true_df['title'].to_list())

    vectorizer = CountVectorizer(tokenizer=tokenizer)
    true_transform = vectorizer.fit_transform(true_df['title']).toarray()

    print(true_transform)
