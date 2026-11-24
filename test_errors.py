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

# Tests to check that negative rent is flagged and zero rent is allowed.
def test_negative_rent():
  df = pd.DataFrame({"monthly_rent_eur": [500, "-1,450 EUR", 0, None]})
  rows, count = negative_rent(df)

  assert rows.index.tolist() == [1]
  assert count == 1


# Tests to check that zero and negative floor areas are flagged.
def test_nonpositive_area():
  df = pd.DataFrame({"area_sqm": [55, 0, -10, "eighty", None]})
  rows, count = nonpositive_area(df)

  assert rows.index.tolist() == [1, 2]
  assert count == 2


# to check Tests that reversed dates are flagged across different date formats.
def test_reversed_lease_dates():
  df = pd.DataFrame({
    "lease_start": ["04/02/2026", "2026-02-04", "05 Feb 2026", "31/02/2026"],
    "lease_end": ["03.02.2026", "2026-02-04", "2026-03-05", "2026-01-01"]
  })
  rows, count = reversed_lease_dates(df)

  assert rows.index.tolist() == [0]
  assert count == 1