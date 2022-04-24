from matplotlib.pyplot import table
from numpy import full
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

from utils import tokenizer


if __name__ == "__main__":
    # ingest
    true_df = pd.read_csv("data/True.csv", nrows=50)
    true_df['type'] = 'true'
    # true_raw = " ".join(true_df['title'].to_list())

    fake_df = pd.read_csv("data/Fake.csv", nrows=50)
    fake_df['type'] = 'fake'
    # fake_raw = " ".join(true_df['title'].to_list())

    full_df = pd.concat([fake_df, true_df])

    print(full_df.describe())
    # full_raw = " ".join(full_df['title'].to_list())

    datasets = train_test_split(
        full_df['title'],
        full_df['type'],
        test_size=0.33,
        random_state=1
    )
    
    dataset_names = ['X_train', 'X_test', 'y_train', 'y_test']
    for df, df_name in zip(datasets, dataset_names):



    # count_vectorizer = CountVectorizer(tokenizer=tokenizer)
    # # tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenizer)

    # true_count_transform = count_vectorizer.fit_transform(true_df['title']).toarray()
    # fake_count_transform = count_vectorizer.fit_transform(fake_df['title']).toarray()
    # # true_tfidf_transform = tfidf_vectorizer.fit_transform(true_df['title']).toarray()
