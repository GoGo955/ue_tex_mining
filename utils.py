import pandas as pd


def load_data(filename: str) -> pd.DataFrame:
    """
    Reads the xlsx file from data folder for a given filename
    Returns raw DataFrame.
    """
    return pd.read_excel(
        f"data\{filename}",
        header=0,
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
    pass
