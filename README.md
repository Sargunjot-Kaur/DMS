# Data Management System (DMS)

DMS is a Python command-line tool for checking property data before a migration. It reads a CSV, checks its required columns, and prints a JSON report that summarises the issues found.

## What DMS checks

| Check | What the report counts |
| --- | --- |
| Missing values | Missing cells across the CSV, with a breakdown by affected column |
| Exact duplicates | Extra copies of rows that match across all columns |
| Repeated unit IDs | All rows sharing a nonblank `unit_id`, with a count for each repeated ID |
| Negative rent | Rows where monthly rent is below zero |
| Invalid floor area | Rows where floor area is zero or less |
| Reversed lease dates | Rows where the lease end date is earlier than the start date |

A CSV must contain `unit_id`, `monthly_rent_eur`, `area_sqm`, `lease_start`, and `lease_end`. Rent values can use comma thousands separators and an `EUR` suffix, such as `1,450 EUR`. Lease dates can use ISO dates or day-first formats such as `04/02/2026` and `04 Feb 2026`. The range and date-order checks use values that parse successfully.

## Run locally

Use Python 3.12 to match the Docker environment.

```bash
git clone https://github.com/Sargunjot-Kaur/DMS.git
cd DMS
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py raw_data/property_data_raw.csv
```

Pass a different CSV path to check another dataset. To save the sample report to a file, run:

```bash
python main.py raw_data/property_data_raw.csv > quality_report.json
```

## Run with Docker

Start Docker, then run the following commands from the project directory. The image includes the sample CSV and uses it by default.

```bash
docker build -t dms-quality .
docker run --rm dms-quality
```

To verify the container is running Linux, use:

```bash
docker run --rm --entrypoint uname dms-quality -s
```

The Docker verification workflow builds the image from a fresh pull-request checkout, checks the sample report, and runs the tests in the container.

## Run on Linux over SSH

Connect to a Linux machine where you have an account:

```bash
ssh user@linux-host
uname -s
```

On the remote host, clone the repository and follow the local or Docker instructions above. Run the checks there and save the JSON report on that host.

## Run the tests

Six tests cover the data checks. Two more cover the JSON output and the optional S3 upload.

```bash
python -m pytest -q
```

To run the same tests inside the Linux container, use:

```bash
docker run --rm --entrypoint python dms-quality -m pytest -q
```

## Save a report to Amazon S3

Use an existing private S3 bucket and a configured AWS profile with permission to write the object. Replace `dms` and `your-private-bucket` with your profile and bucket.

```bash
AWS_PROFILE=dms python main.py raw_data/property_data_raw.csv \
  --s3-output s3://your-private-bucket/reports/quality-report.json \
  > quality_report.json
```

The command prints the report as JSON and uploads the same report with content type `application/json`. If the upload fails, the command reports the error on standard error and exits with status 1. To download the object for verification, use the AWS CLI with permission to read it:

```bash
aws --profile dms s3 cp \
  s3://your-private-bucket/reports/quality-report.json downloaded_report.json
python -m json.tool downloaded_report.json
```

## Sample report

The included CSV produces the following results:

| JSON field | Sample result |
| --- | --- |
| `rows_checked` | 60 |
| `missing_cells` | 7 |
| `missing_by_column` | 2 in `lease_end` and 1 each in five other columns |
| `extra_duplicate_rows` | 5 |
| `rows_with_repeated_unit_ids` | 12 |
| `repeated_unit_ids` | 6 IDs, each appearing twice |
| `negative_rent_rows` | 1 |
| `nonpositive_area_rows` | 1 |
| `reversed_lease_date_rows` | 1 |

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Reads the CSV path, validates the input, and prints the JSON report |
| `errors.py` | Contains the six data-quality checks |
| `test_errors.py` | Tests the behaviour of each check with a small example dataset |
| `test_main.py` | Tests JSON output and S3 upload behaviour |
| `requirements.txt` | Lists the Python dependencies for the pipeline and tests |
| `Dockerfile` | Defines the Linux environment for running the pipeline |
| `raw_data/property_data_raw.csv` | Contains the sample property data |

## Future improvements

- Validate tenant email addresses and flag values that cannot be parsed.
- Standardise capitalisation in building and city names.
- Export flagged rows for review before migration.

## Author

Sargunjot Kaur
