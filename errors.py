def missing(df):
  missing_vals = df.isna()

  columns_with_missing_vals = missing_vals.sum()
  
  columns_with_missing_vals = columns_with_missing_vals [columns_with_missing_vals > 0]

  return columns_with_missing_vals, columns_with_missing_vals.sum() 

def duplicate(df):
  duplicate_mask = df.duplicated()

  duplicate_rows = df [duplicate_mask == True]

  duplicate_count = duplicate_mask.sum()
  return duplicate_rows, duplicate_count