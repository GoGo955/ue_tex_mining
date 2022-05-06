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


def execute():
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
    # suppress pandas future warning
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
    left = unmatched_df['name_1_clean']   # use .head(1000) on full df
    right = unmatched_df['name_2_clean']
    # use code below for full df
    # right = pd.concat([
    #     unmatched_df['name_2_clean'].head(500),
    #     unmatched_df['name_2_clean'].sample(500)]
    # )
    cart_df = cartesian_product_simplified(left, right)
    cart_df['lev'] = cart_df.apply(
        lambda row: find_best_match(row['name_1_clean'], row['name_2_clean']),
        axis=1
    )
    cart_df['min_lev'] = cart_df.groupby('name_1_clean')['lev'].rank(method='min')

    results_df = cart_df[cart_df['min_lev'].isin(range(4))].sort_values(['name_1_clean', 'min_lev'])
    print(results_df.head(20))
    # # cart_df.to_excel('data\cart_prod_sample.xlsx', engine='openpyxl')
    # # clean_df.to_excel('data\clean_matches.xlsx', engine='openpyxl')


if __name__ == "__main__":
    execute()
    # df = load_data('cart_prod_sample.xlsx').drop('Unnamed: 0', axis=1)
    # print(df.head(10))
