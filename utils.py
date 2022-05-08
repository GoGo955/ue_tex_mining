import pandas as pd
import itertools as it
from Levenshtein import distance as lev
import math
import numpy as np


def load_data(filename: str, rows: int) -> pd.DataFrame:
    """
    Reads the 'n' rows of xlsx file from data folder for a given filename
    Returns raw DataFrame.
    """
    return pd.read_excel(
        f"data\{filename}",
        header=0,
        nrows=rows
    )


def decode_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes the text to utf-8, removes accents etc.
    Returns cleaned df.
    """
    cols = df.select_dtypes(include=[object]).columns
    return (
        df[cols]
        .apply(
            lambda x:
            x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        )
    )


def clean_name_cols(df: pd.DataFrame, cols: list([str])) -> pd.DataFrame:
    """
    Removes interpunctions, multispaces and format to lowercase given str columns.
    Returns cleaned df.
    """
    for colname in cols:
        df[f'{colname}_clean'] = df[colname].str.lower()
        df[f'{colname}_clean'] = df[f'{colname}_clean'].str.replace("[^A-Za-z\s\d]+", "")
        df[f'{colname}_clean'] = df[f'{colname}_clean'].str.replace("\s{2,}", " ")
        df[f'{colname}_clean_1'] = df[f'{colname}_clean'].str.replace("\s+", "")
    return df


def extract_simple_matches(clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms input cleaned DF as three separate DataFrames. First one contains exact matches,
    second contains matches based on substrings (col1 is substr of col2 or vice versa) and the
    third one contains the rest - all unmatched rows (in this simple manner).
    Returns: (exact_match_df, substr_match_df, unmatched_df)
    """
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
    return exact_match_df, substr_match_df, unmatched_df


def convert_tuple_to_string(some_tuple, join_type=' '):
    '''Convert tuple to string'''
    string_from_tuple = [join_type.join(item) for item in some_tuple]
    return string_from_tuple


def find_inner_permututations(team_name_):
    '''Find permutations of different possible length'''
    team_name = team_name_.split(" ")
    team_name_permutations = [
        x for len in range(1, len(team_name) + 1) for x in it.combinations(team_name, len)
    ]
    perm_list_string = convert_tuple_to_string(team_name_permutations)
    return perm_list_string


def find_best_match(col_a, col_b, threshold=5):

    team_a = find_inner_permututations(col_a)
    team_b = find_inner_permututations(col_b)

    # get cartesian product
    permutations = []

    for combination in it.product(team_a, team_b):
        permutations.append(combination)

    # Combination dict: key - tuple with team_name permutations, value - score based on levenshtein,
    #                   match total length and intersection including char exact ordering
    actual_score_dict = {perm_tuple: math.inf for perm_tuple in permutations}

    # length of the shorter team name to avoid null id matching during intersection
    mini = min(len(ele) for ele in [col_a, col_b])

    # intersection involves matching chars on full team names and NOT their permutations
    intersection = len(list(set(col_a[:mini]).intersection(col_b[:mini]))) + 1

    for perm_tuple in actual_score_dict:
        lev_score = lev(perm_tuple[0], perm_tuple[1]) + 1
        match_len = len(perm_tuple[0] + perm_tuple[1]) + 1

        if match_len > threshold:
            actual_score_dict[perm_tuple] = (lev_score) * (1 / (match_len * intersection))

    # get the best score
    min_score = min(actual_score_dict, key=actual_score_dict.get)

    return actual_score_dict[min_score]


def cartesian_product_simplified(left, right):
    la, lb = len(left), len(right)
    ia2, ib2 = np.broadcast_arrays(*np.ogrid[:la, :lb])

    return pd.DataFrame(
        np.column_stack([left.values[ia2.ravel()], right.values[ib2.ravel()]]),
        columns=['name_1_clean', 'name_2_clean']
    )
