import pandas as pd
from typing import Any


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert DataFrame column names to lowercase and replace spaces with underscores.
    This function might break YAGNI rule but it's defined in case more complex rules are needed for normalization.

    Args:
        df (pd.DataFrame): The DataFrame with original column names.

    Returns:
        pd.DataFrame: The DataFrame with normalized column names.
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=True)
    return df


def replace_vals_in_cols(df: pd.DataFrame, cols: list[str], old_val: Any, new_val: Any) -> pd.DataFrame:
    """
    Replace occurrences of `old_val` with `new_val` in specified columns of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        cols (List[str]): A list of column names in which to perform the replacement.
        old_val (Any): The value to be replaced.
        new_val (Any): The value to replace `old_val` with.

    Returns:
        pd.DataFrame: The DataFrame with the specified values replaced.
    """
    for col in cols:
        df[col] = df[col].replace(old_val, new_val)
    return df
