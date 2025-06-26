
import pandas as pd

def preprocess_data(path):
    print(f"📂 Reading file: {path}")
    df = pd.read_parquet(path)

    
    df["duration_min"] = (df.lpep_dropoff_datetime - df.lpep_pickup_datetime).dt.total_seconds() / 60

 
    df = df[(df.duration_min >= 0) & (df.duration_min <= 60)]
    df = df[(df.passenger_count > 0) & (df.passenger_count <= 8)]

    print(f"✅ Preprocessed data: {df.shape[0]} rows")
    return df
