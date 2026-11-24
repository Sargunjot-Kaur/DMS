import pandas as pd
from errors import missing, duplicate, duplicated_IDs, negative_rent, nonpositive_area, reversed_lease_dates

# Test to count that the missing valueys are counted per column in total
def test_missing():
  df = pd.DataFrame({
    "unit_id": ["U001", "U002", "U003"],
    "rent": [500, None, None],
    "area": [None, 60, 70]
  })

  columns_with_missing_vals, missing_count = missing(df)

  assert columns_with_missing_vals.to_dict() == {"rent": 2, "area": 1}
  assert missing_count == 3

# Test to check that only extra copies of identical rows are counted as duplicates.
def test_duplicate():
  df = pd.DataFrame({
    "unit_id": ["U001", "U001", "U001"],
    "rent": [500, 500, 650]
  })

  duplicate_rows, duplicate_count = duplicate(df)

  assert duplicate_rows.index.tolist() == [1]
  assert duplicate_count == 1

# Test to check that every row with a repeated unit ID is counted, even when other columns differ.
def test_duplicated_IDs():
  df = pd.DataFrame({
    "unit_id": ["U001", "U001", "U002"],
    "rent": [500, 650, 700]
  })

  duplicate_vals, duplicate_vals_count = duplicated_IDs(df, "unit_id")

  assert duplicate_vals.index.tolist() == [0, 1]
  assert duplicate_vals_count == 2