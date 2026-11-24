import argparse
import json
from pathlib import Path

import pandas as pd

from errors import (
    duplicate,
    duplicated_IDs,
    missing,
    negative_rent,
    nonpositive_area,
    reversed_lease_dates,
)


def load_csv(path):
    data = pd.read_csv(path, dtype={"unit_id": "string"})
    required_columns = [
        "unit_id", "monthly_rent_eur", "area_sqm", "lease_start", "lease_end"
    ]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Required column is missing: {column}")

    return data


def s3_destination(value):
    bucket, separator, key = value.removeprefix("s3://").partition("/")
    if not value.startswith("s3://") or not bucket or not separator or not key:
        raise argparse.ArgumentTypeError("Use an S3 destination like s3://bucket/path/report.json.")
    return bucket, key


def main():
    parser = argparse.ArgumentParser(description="Check a property CSV.")
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV")
    parser.add_argument(
        "--s3-output", type=s3_destination,
        help="Upload the JSON report to s3://bucket/key",
    )
    args = parser.parse_args()

    try:
        data = load_csv(args.input_csv)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    missing_by_column, missing_count = missing(data)
    _, duplicate_count = duplicate(data)

    # Checks the necessary errors in the CSV file 
    rows_with_ids = data.dropna(subset=["unit_id"])
    repeated_rows, repeated_id_count = duplicated_IDs(rows_with_ids, "unit_id")
    id_counts = repeated_rows["unit_id"].value_counts()

    _, negative_rent_count = negative_rent(data)
    _, nonpositive_area_count = nonpositive_area(data)
    _, reversed_lease_count = reversed_lease_dates(data)

    report = {
        "rows_checked": len(data),
        "missing_cells": int(missing_count),
        "missing_by_column": {
            column: int(count) for column, count in missing_by_column.items()
        },
        "extra_duplicate_rows": int(duplicate_count),
        "rows_with_repeated_unit_ids": int(repeated_id_count),
        "repeated_unit_ids": {
            str(unit_id): int(count) for unit_id, count in id_counts.items()
        },
        "negative_rent_rows": int(negative_rent_count),
        "nonpositive_area_rows": int(nonpositive_area_count),
        "reversed_lease_date_rows": int(reversed_lease_count),
    }

    report_json = json.dumps(report, indent=2)
    print(report_json)

    if args.s3_output is not None:
        try:
            import boto3
            from botocore.exceptions import BotoCoreError, ClientError
        except ImportError:
            parser.exit(1, "Install requirements.txt to enable S3 uploads.\n")

        bucket, key = args.s3_output
        try:
            boto3.client("s3").put_object(
                Bucket=bucket,
                Key=key,
                Body=report_json.encode("utf-8"),
                ContentType="application/json",
            )
        except (BotoCoreError, ClientError) as error:
            parser.exit(1, f"Could not upload the JSON report to S3: {error}\n")


if __name__ == "__main__":
    main()
