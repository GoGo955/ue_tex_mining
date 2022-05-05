from utils import (
    load_data,
    decode_data
)


if __name__ == "__main__":
    raw_df = load_data("compare_matches.xlsx")
    preprocessed_df = decode_data(raw_df)

    cols_to_clean = ['name_1', 'name_1']
