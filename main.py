from utils import (
    load_data,
    decode_data,
    clean_name_cols
)


if __name__ == "__main__":
    raw_df = load_data("compare_matches.xlsx")
    preprocessed_df = decode_data(raw_df)

    # decide if cleaned names should contain spaces or not
    cols_to_clean = ['name_1', 'name_2']
    preprocessed_df = clean_name_cols(preprocessed_df, cols_to_clean)
    print(preprocessed_df.head())
