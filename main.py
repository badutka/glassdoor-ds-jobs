import os
import pandas as pd

import data_ingestion
import data_cleaning
import data_transform

# Constants for dataset details and paths
DATASET_ORIGIN = 'rashikrahmanpritom'
DATASET_NAME = 'data-science-job-posting-on-glassdoor'
DOWNLOAD_PATH = 'data'


def main():
    """Main function to execute the data ingestion, cleaning, and transformation pipeline."""
    # ==========================
    # Data Ingestion Steps
    # ==========================
    # Uncomment the following line to download and unzip the dataset if needed
    # data_ingestion.download_and_unzip_kaggle_dataset(DATASET_ORIGIN, DATASET_NAME, DOWNLOAD_PATH)

    csv_file_path = os.path.join(DOWNLOAD_PATH, 'Uncleaned_DS_Jobs.csv')
    df = data_ingestion.load_csv(csv_file_path)

    # ==========================
    # Data Cleaning Steps
    # ==========================
    df = data_cleaning.normalize_column_names(df)

    # Drop unnecessary columns if they exist
    df = df.drop(columns=['index', 'job_description'], errors='ignore')

    # Extract company name before newline character
    df['company_name'] = df['company_name'].str.split('\n').str[0]

    # Extract estimated salary range (e.g., "$40K-$80K")
    df['salary_estimate'] = df['salary_estimate'].str.extract(r'(\$\d+K-\$\d+K)')

    # Replace placeholder values with NaN for specified columns
    df = data_cleaning.replace_vals_in_cols(
        df,
        ['rating', 'headquarters', 'size', 'founded', 'type_of_ownership', 'industry', 'sector', 'revenue', 'competitors'],
        ['-1', -1, -1.0, 'Unknown / Non-Applicable'],
        pd.NA
    )

    # ==========================
    # Data Transformation Steps
    # ==========================
    # Extract revenue ranges into min_revenue and max_revenue columns
    df[['min_revenue', 'max_revenue']] = df['revenue'].apply(data_transform.extract_revenue_range)
    df = df.drop(columns=['revenue'])

    # Extract salary columns from salary_estimate
    df = data_transform.extract_salary_columns(df)

    # Extract location columns (city and state) from location field
    df = data_transform.extract_location_columns(df)

    # Extract headquarters columns (city and state) from headquarters field
    df = data_transform.extract_headquarters_columns(df)

    # Calculate the number of competitors
    df = data_transform.extract_num_competitors(df)

    # Output a preview of the transformed DataFrame
    print(df.head())


if __name__ == '__main__':
    main()
