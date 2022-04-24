import pandas as pd

from utils import vectorize, fit_classifiers


if __name__ == "__main__":
    # ingest
    true_df = pd.read_csv("data/True.csv", nrows=100)
    true_df['type'] = 'true'

    fake_df = pd.read_csv("data/Fake.csv", nrows=100)
    fake_df['type'] = 'fake'

    full_df = pd.concat([fake_df, true_df])

    # vectorize
    data = vectorize(full_df)

    # fit and evaluate classifiers
    fit_classifiers(data)
