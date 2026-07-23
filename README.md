# Data Management System (DMS)

DMS is a simple Python project for checking data quality before data is imported into another system.

It reads a property dataset from a CSV file and finds common problems that could cause errors during data migration, such as missing information and duplicate records.

## What the Project Checks

The current version checks for:

- Missing values in any column
- Completely duplicated rows
- Repeated IDs in a selected column
- The number of detected problems

For the included property dataset, the project is also intended to help identify:

- Inconsistent capitalisation in building names and cities
- Incorrect numeric values
- Invalid tenant email addresses
- Incorrect lease dates
- Duplicate building or unit IDs

## Why This Is Useful

Before data is transferred from spreadsheets or old systems into a new platform, it should be checked carefully.

This project helps make that process easier by finding data-quality problems early. The results can then be reviewed and corrected before the final import.

## Technologies Used

- Python
- Pandas
- CSV data

## Project Structure

```text
DMS/
├── main.py
├── errors.py
├── data_notes.txt
└── raw_data/
    └── property_data_raw.csv
```

- `main.py` loads the CSV file and runs the checks.
- `errors.py` contains reusable functions for detecting data problems.
- `data_notes.txt` records known issues found in the dataset.
- `raw_data/property_data_raw.csv` contains the original property data.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Sargunjot-Kaur/DMS.git
cd DMS
```

### 2. Install Pandas

```bash
pip install pandas
```

### 3. Add the CSV file

Place the source dataset at:

```text
raw_data/property_data_raw.csv
```

### 4. Run the program

```bash
python main.py
```

## Output

When the program runs, it displays:

- The first five rows of the dataset
- The total number of rows and columns
- All column names
- Missing values by column
- Duplicate rows
- Repeated values in the `unit_id` column

This output shows which records need attention before the data is moved into the target system.

## Main Functions

### `missing(df)`

Finds columns containing empty values and returns the number of missing values.

### `duplicate(df)`

Finds rows that are exact duplicates and returns the duplicate count.

### `duplicated_IDs(df, column_name)`

Finds every row that uses a repeated ID in the selected column.

## Future Improvements

- Automatically correct inconsistent capitalisation
- Validate email-address formats
- Convert numeric columns to the correct data type
- Validate lease start and end dates
- Remove or flag invalid records
- Export a clean CSV file ready for import
- Generate a data-quality summary report

## Author

Sargunjot Kaur

