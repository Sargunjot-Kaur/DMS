import argparse
from pathlib import Path

import pandas as pd

from errors import duplicate, duplicated_IDs, missing

# checks if the csv file has a unit_id; else returns - missing column
def load_csv(path):
    data = pd.read_csv(path, dtype={"unit_id": "string"})
    if "unit_id" not in data.columns:
        raise ValueError("Required column is missing: unit_id")
    return data

# take input csv from the terminal --> checks unit_id --> prints errors in file
def main():
    parser = argparse.ArgumentParser(description="Check a property CSV.")
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV")
    args = parser.parse_args()

    try:
        data = load_csv(args.input_csv)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    _, missing_count = missing(data)
    _, duplicate_count = duplicate(data)
    _, repeated_id_row_count = duplicated_IDs(data, "unit_id")

    print(f"Rows checked: {len(data)}")
    print(f"Missing cells: {missing_count}")
    print(f"Extra copies of identical rows: {duplicate_count}")
    print(f"Rows sharing a repeated unit ID: {repeated_id_row_count}")


if __name__ == "__main__":
    main()