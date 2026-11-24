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

## Run the tests

The six pytest tests cover missing cells, exact duplicates, repeated IDs, negative rent, nonpositive floor area, and lease date order.

```bash
python -m pytest -q test_errors.py
```

To run the same tests inside the Linux container, use:

```bash
docker run --rm --entrypoint python dms-quality -m pytest -q test_errors.py
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
| `requirements.txt` | Lists the Python dependencies for the pipeline and tests |
| `Dockerfile` | Defines the Linux environment for running the pipeline |
| `raw_data/property_data_raw.csv` | Contains the sample property data |
| `data_notes.txt` | Records issues observed in the source dataset |

## Future improvements

- Validate tenant email addresses and flag values that cannot be parsed.
- Standardise capitalisation in building and city names.
- Export flagged rows for review before migration.

## Author

Sargunjot Kaur
