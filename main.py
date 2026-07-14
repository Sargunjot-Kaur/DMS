import pandas as pd

source_data = "raw_data/property_data_raw.csv"

data = pd.read_csv(source_data)
#print(data.head)
print(data.head(5))
print(data.shape)
print(data.columns)



