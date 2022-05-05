import pandas as pd

from utils import (
    load_data,
    decode_data,
    clean_name_cols
)


def check_shape():
    # temp shape check
    print(f"Raw df row count: {raw_df.shape[0]}")
    print(f"Clean df row count: {clean_df.shape[0]}")
    print(f"Duplicate df row count: {duplicates_df.shape[0]}")
    print(
        "Summary row count after first (simple) phase of matching:",
        f"{substr_match_df.shape[0] + exact_match_df.shape[0] + unmatched_df.shape[0]}"
    )


if __name__ == "__main__":
    # raw
    raw_df = load_data("compare_matches.xlsx")

    # preprocessed
    preprocessed_df = decode_data(raw_df)
    cols_to_clean = ['name_1', 'name_2']
    preprocessed_df = clean_name_cols(preprocessed_df, cols_to_clean)

    # clean
    clean_df = preprocessed_df.drop_duplicates()
    duplicates_df = (
        preprocessed_df[preprocessed_df.duplicated(subset=cols_to_clean, keep=False)]
        .drop_duplicates()
    )

    # phase 1 - simple matching
    exact_match_df = clean_df[clean_df['name_1_clean'] == clean_df['name_2_clean']]

    substr_match_df = pd.concat([clean_df, exact_match_df]).drop_duplicates(keep=False)
    substr_match_df['is_substr'] = [
        row[0] in row[1] or row[1] in row[0]
        for row
        in zip(substr_match_df['name_1_clean'], substr_match_df['name_2_clean'])
    ]
    # figure out if this is correct - if not, remove E712 from setup cfg
    substr_match_df = substr_match_df[substr_match_df['is_substr'] == True]

    unmatched_df = (
        pd
        .concat([clean_df, exact_match_df, substr_match_df.drop('is_substr', axis=1)])
        .drop_duplicates(keep=False)
    )

    check_shape()

    # phase 2 - similarities

    # preprocessed_df.to_excel('data\preprocessed_matches.xlsx')
