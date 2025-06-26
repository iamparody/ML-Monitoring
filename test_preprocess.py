
from preprocess import preprocess_data

df = preprocess_data("data/green_tripdata_2024-03.parquet")
print(df.head())
print(f"Data shape: {df.shape}")
