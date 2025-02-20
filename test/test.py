import pandas as pd
import numpy as np
import pytest
import tempfile
import os

# Import your functions
from src.data_ingestion import load_csv
from src.data_cleaning import normalize_column_names, replace_vals_in_cols
from src.data_transform import (
    extract_revenue_range,
    extract_salary_columns,
    extract_location_columns,
    extract_headquarters_columns,
    extract_num_competitors,
)
from src.data_validation import validate_row


@pytest.fixture
def sample_df():
    """Fixture that provides a DataFrame with diverse test cases."""
    return pd.DataFrame({
        "salary_estimate": ["$40K-$80K", "$50K-$90K"],
        "location": ["San Francisco, CA", "New York, NY"],
        "headquarters": ["Los Angeles, CA", "Chicago, IL"],
        "competitors": ["Competitor A, Competitor B", "Competitor C"],
        "rating": [-1, 4.5],
        "size": [-1, "Medium"],
        "company_name": ["TestCorp", None],
    })


def test_load_csv():
    """Test that load_csv correctly reads a CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
        temp_file.write("col1,col2\n1,2\n3,4")
        file_path = temp_file.name

    df = load_csv(file_path)
    os.remove(file_path)  # Cleanup

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1", "col2"]
    assert df.shape == (2, 2)


def test_normalize_column_names(sample_df):
    """Test column names are standardized."""
    df = sample_df.copy()
    df.columns = ["Salary Estimate", "Location Info", "HQ", "Competing Firms", "Company Rating", "Company Size", "Name"]
    normalized_df = normalize_column_names(df)
    expected_columns = {"salary_estimate", "location_info", "hq", "competing_firms", "company_rating", "company_size", "name"}
    assert set(normalized_df.columns) == expected_columns


def test_replace_vals_in_cols(sample_df):
    """Test replacing -1 and 'Unknown / Non-Applicable' with NaN."""
    df = sample_df.copy()
    replaced_df = replace_vals_in_cols(df, ["rating", "size"], [-1], pd.NA)

    assert pd.isna(replaced_df.loc[0, "rating"])
    assert pd.isna(replaced_df.loc[0, "size"])
    assert replaced_df.loc[1, "size"] == "Medium"


def test_extract_revenue_range():
    """Test min/max revenue extraction."""
    assert extract_revenue_range("$5 to $10 million (USD)").equals(pd.Series([5000000.0, 10000000.0]))
    assert extract_revenue_range("N/A").equals(pd.Series([np.nan, np.nan]))


def test_extract_salary_columns(sample_df):
    """Test salary extraction."""
    df = extract_salary_columns(sample_df.copy())
    print(df)
    assert df["salary_min"].tolist() == [40000, 50000]
    assert df["salary_max"].tolist() == [80000, 90000]


def test_extract_location_columns(sample_df):
    """Test city and state extraction."""
    df = extract_location_columns(sample_df.copy())
    assert df["location_city"].tolist() == ["San Francisco", "New York"]
    assert df["location_state"].tolist() == ["CA", "NY"]


def test_extract_headquarters_columns(sample_df):
    """Test headquarters city and state extraction."""
    df = extract_headquarters_columns(sample_df.copy())
    assert df["headquarters_city"].tolist() == ["Los Angeles", "Chicago"]
    assert df["headquarters_state"].tolist() == ["CA", "IL"]


def test_extract_num_competitors(sample_df):
    """Test competitor count extraction."""
    df = extract_num_competitors(sample_df.copy())
    assert df["num_competitors"].tolist() == [2, 1]


def test_validate_row(sample_df):
    """Test row validation."""
    valid_row = sample_df.iloc[0]  # First row is valid
    person, error = validate_row(valid_row)
    assert person is not None
    assert error in (None, "")

    invalid_row = sample_df.iloc[1].copy()
    invalid_row["company_name"] = None  # Make it invalid
    person, error = validate_row(invalid_row)
    assert person is None
    assert isinstance(error, str) and len(error) > 0