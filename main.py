import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from utils import tokenizer, sum_over


if __name__ == "__main__":
    # ingest
    true_df = pd.read_csv("data/True.csv", nrows=5)
    true_raw = " ".join(true_df['title'].to_list())

    count_vectorizer = CountVectorizer(tokenizer=tokenizer)
    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenizer)

    true_count_transform = count_vectorizer.fit_transform(true_df['title']).toarray()
    true_tfidf_transform = tfidf_vectorizer.fit_transform(true_df['title']).toarray()

    top10_tokens = sum_over(
        transform=true_count_transform,
        feature_names=count_vectorizer.get_feature_names_out(),
        axis=0
    )

    most_important_tokens = sum_over(
        transform=true_tfidf_transform,
        feature_names=tfidf_vectorizer.get_feature_names_out(),
        axis=0
    )
    most_imp_docs = sum_over(
        transform=true_count_transform,
        feature_names=count_vectorizer.get_feature_names_out(),
        axis=1
    )

    print(top10_tokens)
    print(most_important_tokens)
    print(most_imp_docs)
