import pandas as pd
import numpy as np
import pytest
import tempfile
import os
import shutil

from src.data_ingestion import download_and_unzip_kaggle_dataset, load_csv
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


@pytest.fixture
def mock_read_csv(mocker):
    """Fixture to mock pandas.read_csv."""
    return mocker.patch('pandas.read_csv')


# Define the test function
def test_download_and_unzip_kaggle_dataset():
    # Test parameters
    DATASET_ORIGIN = 'rashikrahmanpritom'
    DATASET_NAME = 'data-science-job-posting-on-glassdoor'
    DOWNLOAD_PATH = 'data_test'

    # Step 1: Ensure the DOWNLOAD_PATH does not exist before starting the test
    if os.path.exists(DOWNLOAD_PATH):  # pragma: no cover
        shutil.rmtree(DOWNLOAD_PATH)  # Remove the directory if it exists

    # Step 2: Run the function to download and unzip the dataset
    download_and_unzip_kaggle_dataset(DATASET_ORIGIN, DATASET_NAME, DOWNLOAD_PATH)  # todo: mock the api?

    # Step 3: Check if the directory and the dataset zip file exist
    assert os.path.exists(DOWNLOAD_PATH), f"Directory {DOWNLOAD_PATH} was not created."
    assert os.path.exists(f'{DOWNLOAD_PATH}/{DATASET_NAME}.zip'), f"Dataset zip file was not downloaded."

    # Step 4: Check if the dataset was unzipped (check if the expected file(s) are extracted)
    # Replace 'your_expected_file.csv' with a real file name in the dataset (e.g., 'data.csv')
    assert any(fname.endswith('.csv') for fname in os.listdir(DOWNLOAD_PATH)), "No CSV file found in the unzipped directory."

    # Step 5: Clean up - Delete the downloaded and unzipped files
    shutil.rmtree(DOWNLOAD_PATH)
    print(f"Test completed. '{DOWNLOAD_PATH}' has been deleted.")


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


def test_load_csv_success(mock_read_csv):
    """
    Test the load_csv function to ensure it correctly calls pandas.read_csv
    and returns the expected DataFrame.
    """
    # Mocking the pandas.read_csv to return a fake DataFrame when called
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_read_csv.return_value = mock_df

    file_path = 'test.csv'

    # Call the function
    result = load_csv(file_path)

    # Assertions to verify that the function behaves correctly
    mock_read_csv.assert_called_once_with(file_path)  # Ensure read_csv was called with the correct path
    assert isinstance(result, pd.DataFrame)  # Ensure the result is a pandas DataFrame
    assert result.shape == (2, 2)  # Check if the DataFrame shape is as expected


def test_load_csv_error(mock_read_csv):
    """
    Test the load_csv function to ensure it handles errors correctly
    when pandas.read_csv raises an exception.
    """
    # Mocking pandas.read_csv to raise an error (e.g., FileNotFoundError)
    mock_read_csv.side_effect = FileNotFoundError("File not found")

    file_path = 'non_existent_file.csv'

    # Call the function and handle the expected error
    with pytest.raises(FileNotFoundError, match="File not found"):
        load_csv(file_path)

    # Ensure read_csv was called with the correct path
    mock_read_csv.assert_called_once_with(file_path)


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
    assert extract_revenue_range(pd.NA).equals(pd.Series([np.nan, np.nan]))
    assert extract_revenue_range("$5 to $10 million (USD)").equals(pd.Series([5_000_000.0, 10_000_000.0]))
    assert extract_revenue_range("$500 million to $1 billion (USD)").equals(pd.Series([500_000_000.0, 1_000_000_000.0]))
    assert extract_revenue_range("$10+ billion (USD)").equals(pd.Series([10_000_000_000.0, np.nan]))
    assert extract_revenue_range("Less than $1 million (USD)").equals(pd.Series([0.0, 1_000_000]))
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


def test_validate_row_success():
    """Test row validation."""
    sample_df = pd.DataFrame({
        "job_title": ["Software Engineer", "Data Scientist"],
        "salary_min": [40000, 50000],
        "salary_max": [80000, 90000],
        "location_city": ["San Francisco", "New York"],
        "location_state": ["CA", np.nan],
        "company_name": ["TestCorp", "TechCorp"],
        "rating": [4.5, 4.2],
        "size": ["Medium", "Large"],
        "founded": [1999, 2005],
        "type_of_ownership": ["Private", "Public"],
        "industry": ["Tech", "Finance"],
        "sector": ["Software", "Finance"],
        "min_revenue": [5000000, 10000000],
        "max_revenue": [10000000, 20000000],
        "headquarters_city": ["Los Angeles", "Chicago"],
        "headquarters_state": ["CA", "IL"],
        "num_competitors": [2, 3],
    })

    for _, row in sample_df.iterrows():
        job_offer, error = validate_row(row)

        assert job_offer is not None
        assert error in (None, "")


def test_validate_row_error():
    """Test row validation."""
    sample_df = pd.DataFrame({
        "job_title": ["Software Engineer", "Data Scientist"],
        "salary_min": [40000, 50000],
    })

    for _, row in sample_df.iterrows():
        job_offer, error = validate_row(row)

        assert job_offer is None
        assert error is not None and error != ""
