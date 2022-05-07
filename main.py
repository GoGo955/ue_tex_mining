from warnings import simplefilter
import pandas as pd

from utils import (
    load_data,
    decode_data,
    clean_name_cols,
    extract_simple_matches,
    find_best_match,
    cartesian_product_simplified
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
    print(f"Exact match df row count: {exact_match_df.shape[0]}")
    print(f"Substrung match df row count: {substr_match_df.shape[0]}")
    print(f"Unmatched df row count: {unmatched_df.shape[0]}")


if __name__ == "__main__":
    # suppress pandas future warning (related to regex method from pandas)
    simplefilter(action='ignore', category=FutureWarning)
    # raw
    raw_df = load_data("compare_matches.xlsx", 500)

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
    exact_match_df, substr_match_df, unmatched_df = extract_simple_matches(clean_df)
    check_shape()

    # phase 2 - similarities. split unmatched to two sample dfs, create a cartesian product
    # and apply the lev dist func.

    # split data
    left = unmatched_df['name_1_clean']
    right = unmatched_df['name_2_clean']

    # do crossjoin, apply the lev algo, add rank col for lev scores
    cart_df = cartesian_product_simplified(left, right)
    cart_df['lev'] = cart_df.apply(
        lambda row: find_best_match(row['name_1_clean'], row['name_2_clean']),
        axis=1
    )
    cart_df['min_lev'] = cart_df.groupby('name_1_clean')['lev'].rank(method='min')

    # select rows with best rank per each pair
    results_df = cart_df[cart_df['min_lev'] == 1]
    print(results_df.head(30))

    # issue to solve - this approach leaves the duplicates. Also the output shape minimally differs
    # from the original unmatched_df
    print(f"Unmatched df row count: {unmatched_df.shape[0]}")
    print(f"Matched df row count: {results_df.drop_duplicates().shape[0]}")

    bad_matches_df = (
        pd
        .concat(
            [
                unmatched_df[['name_1_clean', 'name_2_clean']],
                results_df[['name_1_clean', 'name_2_clean']]
            ]
        )
        .drop_duplicates(keep=False)
    )
    print(bad_matches_df)
