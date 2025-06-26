import requests
from tqdm import tqdm 
import os

file = 'green_tripdata_2024-03.parquet'
url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{file}'
save_path = f'data/{file}'

os.makedirs('data', exist_ok=True)

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

with open(save_path, 'wb') as f:
    for chunk in tqdm(response.iter_content(chunk_size=1024), 
                      total=total_size // 1024, 
                      unit='KB', desc=f'Downloading {file}'):
        if chunk:
            f.write(chunk)
