import pandas as pd
import re
import numpy as np
from typing import Union

# Define a type alias for revenue values that could be float or pandas' NA
RevenueType = Union[float, pd.NA]


def extract_revenue_range(s: Union[str, pd.NA]) -> (RevenueType, RevenueType):
    """Extract the minimum and maximum revenue values from a revenue string.

    This function takes a revenue string in various formats such as:
      - "$X to $Y million/billion (USD)"
      - "$X million/billion to $Y million/billion (USD)"
      - "$X+ million/billion (USD)"
      - "Less than $X million/billion (USD)"
    and extracts the numeric lower and upper revenue bounds, converting them to USD numbers.
    If only one bound is available, the other is set to NaN. If the string is not in a recognized
    format or is missing, both values will be NaN.

    Args:
        s (str or NA): A revenue string representing a range of revenue values or a partial value.

    Returns:
        pandas.Series: A Series with two elements:
            - The first element is the lower bound revenue as a float (in USD), or NaN if unavailable.
            - The second element is the upper bound revenue as a float (in USD), or NaN if unavailable.
    """
    if pd.isna(s):
        return pd.Series([np.nan, np.nan])

    # Pattern 1: "$X million/billion to $Y million/billion"
    # e.g., "$500 million to $1 billion (USD)"
    match = re.search(
        r'\$([\d]+)\s*(million|billion)\s*to\s*\$([\d]+)\s*(million|billion)',
        s, re.IGNORECASE
    )
    if match:
        low, low_unit, high, high_unit = match.groups()
        low_factor = 1e6 if low_unit.lower() == 'million' else 1e9
        high_factor = 1e6 if high_unit.lower() == 'million' else 1e9
        return pd.Series([float(low) * low_factor, float(high) * high_factor])

    # Pattern 2: "$X to $Y (unit)"
    # e.g., "$1 to $2 billion (USD)" where the unit is only provided once.
    match = re.search(
        r'\$([\d]+)\s*to\s*\$([\d]+)\s*(million|billion)',
        s, re.IGNORECASE
    )
    if match:
        low, high, unit = match.groups()
        factor = 1e6 if unit.lower() == 'million' else 1e9
        return pd.Series([float(low) * factor, float(high) * factor])

    # Pattern 3: "$X+ (unit)" (only lower bound available)
    # e.g., "$10+ billion (USD)"
    match = re.search(
        r'\$([\d]+)\+\s*(million|billion)',
        s, re.IGNORECASE
    )
    if match:
        low, unit = match.groups()
        factor = 1e6 if unit.lower() == 'million' else 1e9
        return pd.Series([float(low) * factor, np.nan])

    # Pattern 4: "Less than $X (unit)" (only upper bound available)
    # e.g., "Less than $1 million (USD)"
    match = re.search(
        r'Less than\s*\$([\d]+)\s*(million|billion)',
        s, re.IGNORECASE
    )
    if match:
        high, unit = match.groups()
        factor = 1e6 if unit.lower() == 'million' else 1e9
        return pd.Series([0.0, float(high) * factor])

    # If no pattern matches, return NaN for both bounds
    return pd.Series([np.nan, np.nan])


def extract_salary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Extract minimum and maximum salary values from the 'salary_estimate' column.

    The salary estimate is expected to be in the format "$<number>K-$<number>K"
    (case-insensitive). The extracted values are converted to integers (dollars).

    Args:
        df (pd.DataFrame): DataFrame containing the 'salary_estimate' column.

    Returns:
        pd.DataFrame: DataFrame with new 'salary_min' and 'salary_max' columns added,
                      and the original 'salary_estimate' column dropped.
    """
    salary_cols = df['salary_estimate'].str.extract(r'\$(\d+)[Kk]-\$(\d+)[Kk]')
    df['salary_min'] = salary_cols[0].astype(int) * 1000
    df['salary_max'] = salary_cols[1].astype(int) * 1000
    df = df.drop(columns=['salary_estimate'])
    return df


def extract_location_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Extract city and state from the 'location' column.

    The location column is expected to be in the format "City, State".

    Args:
        df (pd.DataFrame): DataFrame containing the 'location' column.

    Returns:
        pd.DataFrame: DataFrame with new 'location_city' and 'location_state' columns,
                      and the original 'location' column dropped.
    """
    df['location_city'] = df['location'].str.split(',').str[0]
    df['location_state'] = df['location'].str.split(',').str[1].str.strip()
    df = df.drop(columns=['location'])
    return df


def extract_headquarters_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Extract city and state from the 'headquarters' column.

    The headquarters column is expected to be in the format "City, State".

    Args:
        df (pd.DataFrame): DataFrame containing the 'headquarters' column.

    Returns:
        pd.DataFrame: DataFrame with new 'headquarters_city' and 'headquarters_state' columns,
                      and the original 'headquarters' column dropped.
    """
    df['headquarters_city'] = df['headquarters'].str.split(',').str[0]
    df['headquarters_state'] = df['headquarters'].str.split(',').str[1].str.strip()
    df = df.drop(columns=['headquarters'])
    return df


def extract_num_competitors(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the number of competitors from the 'competitors' column.

    The competitors column is expected to be a comma-separated string.

    Args:
        df (pd.DataFrame): DataFrame containing the 'competitors' column.

    Returns:
        pd.DataFrame: DataFrame with a new 'num_competitors' column,
                      and the original 'competitors' column dropped.
    """
    df['num_competitors'] = df['competitors'].str.split(',').str.len()
    df = df.drop(columns=['competitors'])
    return df
