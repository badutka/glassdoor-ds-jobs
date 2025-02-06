import data_ingestion
import os

# Define constants for dataset details and paths
DATASET_ORIGIN = 'rashikrahmanpritom'
DATASET_NAME = 'data-science-job-posting-on-glassdoor'
DOWNLOAD_PATH = 'data'

# Call the function to download and unzip the dataset
# data_ingestion.download_and_unzip_kaggle_dataset(DATASET_ORIGIN, DATASET_NAME, DOWNLOAD_PATH)

csv_file_path = os.path.join(DOWNLOAD_PATH, 'Uncleaned_DS_Jobs.csv')
df = data_ingestion.load_csv(csv_file_path)