# Data Science Job Posting Pipeline
A Python-based pipeline for ingesting, cleaning, transforming, and validating a dataset of data science job postings on Glassdoor.

### Overview

This project demonstrates a complete data processing pipeline which includes:

* Data Ingestion: Loading the dataset (and optionally downloading it from Kaggle).
* Data Cleaning: Normalizing column names, handling missing or placeholder values, and preparing the data for analysis.
* Data Transformation: Extracting and restructuring key information such as salary ranges, revenue ranges, and location details.
* Data Validation: Ensuring data integrity by validating each row of the processed DataFrame.

The dataset used is the "Data Science Job Posting on Glassdoor" dataset. You can download it from Kaggle or use your own CSV file placed in the data folder.

### Project Structure
``` plaintext
.
├── data                           # Directory for dataset files
├── data_ingestion.py              # Functions for downloading and loading the dataset
├── data_cleaning.py               # Functions for cleaning the dataset
├── data_transform.py              # Functions for transforming the dataset
├── data_validation.py             # Functions for validating the dataset
└── main.py                        # Main pipeline script
```
### Installation

1. Clone the Repository:
``` bash
git clone https://github.com/badutka/glassdoor-ds-jobs.git
```

2. Install Dependencies:
If you have a requirements.txt file:

``` bash
pip install -r requirements.txt
```
3. Otherwise, install the required packages manually:
``` bash
pip install pandas
...
```

### Usage

1. Prepare the Dataset:

* If you haven't already, download the "Data Science Job Posting on Glassdoor" dataset from Kaggle.
* Place the downloaded CSV file (e.g., Uncleaned_DS_Jobs.csv) in the data folder.
* Alternatively, if you have configured the Kaggle API, you can uncomment the following line in main.py to download and unzip the dataset automatically:

``` python
data_ingestion.download_and_unzip_kaggle_dataset(DATASET_ORIGIN, DATASET_NAME, DOWNLOAD_PATH)
```
2. Run the Pipeline: \
Execute the main script:

``` bash
python main.py
```

The script will:

* Load and ingest the dataset.
* Clean and transform the data.
* Validate each row and print a preview of the processed DataFrame along with any validation errors.

### Modules Overview

* data_ingestion: \
Handles the loading (and optional downloading) of the dataset.


* data_cleaning: \
Contains functions to normalize column names, drop unnecessary columns, and replace placeholder values with proper null values.


* data_transform: \
Provides functionality to extract key features from the dataset such as:
  * Salary ranges (e.g., extracting minimum and maximum salary).
  * Revenue ranges (e.g., extracting minimum and maximum revenue).
  * Location information (city and state from both job location and headquarters).
  * The number of competitors.


* data_validation: \
  Implements row-level validation to ensure data integrity and quality before further analysis.