import data_ingestion
import os
import pandas as pd
from typing import Any

# Define constants for dataset details and paths
DATASET_ORIGIN = 'rashikrahmanpritom'
DATASET_NAME = 'data-science-job-posting-on-glassdoor'
DOWNLOAD_PATH = 'data'

# Call the function to download and unzip the dataset
# data_ingestion.download_and_unzip_kaggle_dataset(DATASET_ORIGIN, DATASET_NAME, DOWNLOAD_PATH)

csv_file_path = os.path.join(DOWNLOAD_PATH, 'Uncleaned_DS_Jobs.csv')
df = data_ingestion.load_csv(csv_file_path)


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


# ==========================
# Apply Data Cleaning Steps
# ==========================
df = normalize_column_names(df)

# Drop unnecessary columns
df = df.drop(columns=['index', 'job_description'], errors='ignore')

# Extract company name before newline character
df['company_name'] = df['company_name'].str.split('\n').str[0]

# Extract estimated salary range
df['salary_estimate'] = df['salary_estimate'].str.extract(r'(\$\d+K-\$\d+K)')

# Replace placeholder values with NaN
df = replace_vals_in_cols(df,
                          ['rating', 'headquarters', 'size', 'founded', 'type_of_ownership', 'industry', 'sector', 'revenue', 'competitors'],
                          ['-1', -1, -1.0], pd.NA)
