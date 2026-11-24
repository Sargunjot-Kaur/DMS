# finds the number of missing cells in each affected column and the total.
def missing(df):
  missing_vals = df.isna()
  columns_with_missing_vals = missing_vals.sum()
  columns_with_missing_vals = columns_with_missing_vals [columns_with_missing_vals > 0]
  return columns_with_missing_vals, columns_with_missing_vals.sum() 

# finds the extra copies of identical rows and their count.
def duplicate(df):
  duplicate_mask = df.duplicated()
  duplicate_rows = df [duplicate_mask == True]
  duplicate_count = duplicate_mask.sum()
  return duplicate_rows, duplicate_count

# finds all rows with repeated IDs in the chosen column and their count.
def duplicated_IDs(df, column_name):
  duplicated_mask_columns = df[column_name].duplicated(keep = False)
  duplicate_vals = df [duplicated_mask_columns == True]
  duplicate_vals_count = duplicated_mask_columns.sum()
  return duplicate_vals, duplicate_vals_count

# finds rows with a negative monthly rent.
def negative_rent(df):
  rent_text = df["monthly_rent_eur"].astype("string").str.strip()
  rent_text = rent_text.str.removesuffix(" EUR").str.replace(",", "", regex=False)
  rent = pd.to_numeric(rent_text, errors="coerce")
  negative_mask = rent < 0
  return df[negative_mask], negative_mask.sum()


# finds rows with a floor area of zero or less.
def nonpositive_area(df):
  area = pd.to_numeric(df["area_sqm"], errors="coerce")
  area_mask = area <= 0
  return df[area_mask], area_mask.sum()


# finds rows where the lease ends before it starts.
def reversed_lease_dates(df):
  start_dates = pd.to_datetime(
    df["lease_start"], format="mixed", dayfirst=True, errors="coerce"
  )