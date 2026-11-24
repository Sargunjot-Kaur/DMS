import argparse
import json
import pandas as pd
from pathlib import Path
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
    if "unit_id" not in data.columns:
        raise ValueError("Required column is missing: unit_id")
    return data


def main():
    parser = argparse.ArgumentParser(description="Check a property CSV.")
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV")
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

    # Creates a valid json file will the report informartion
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
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()