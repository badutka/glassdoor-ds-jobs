import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Set up the Kaggle API key file path if needed
# Optional if the Kaggle API key is placed in the default location (~/.kaggle/kaggle.json or C:\Users\<YourUsername>\.kaggle\kaggle.json)
# os.environ['KAGGLE_CONFIG_DIR'] = '/path/to/.kaggle'  # Optional step

# Define constants for dataset details and paths
DATASET_ORIGIN = 'rashikrahmanpritom'
DATASET_NAME = 'data-science-job-posting-on-glassdoor'
DOWNLOAD_PATH = 'data'


def download_and_unzip_kaggle_dataset(dataset_origin, dataset_name, download_path):
    """
    Downloads a Kaggle dataset and unzips it into the specified folder.

    Args:
    - dataset_origin (str): Kaggle username or organization.
    - dataset_name (str): The name of the dataset.
    - download_path (str): The directory where the dataset will be saved.
    """
    # Initialize the Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Construct the dataset origin and zip file path
    download_origin = f'{dataset_origin}/{dataset_name}'
    zip_file_path = f'{download_path}/{dataset_name}.zip'

    # Download the dataset
    api.dataset_download_files(download_origin, path=download_path, unzip=False)

    # Unzip the downloaded file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(download_path)

    print(f"Dataset '{dataset_name}' downloaded and extracted to '{download_path}'.")


# Call the function to download and unzip the dataset
download_and_unzip_kaggle_dataset(DATASET_ORIGIN, DATASET_NAME, DOWNLOAD_PATH)
