# Databricks notebook source
import os
import requests
from datetime import datetime, timedelta

bronze_volume = '/Volumes/workspace/bronze/bronzevolume'
bronze_dir = os.path.join(bronze_volume, 'nyc_taxi_raw')
os.makedirs(bronze_dir, exist_ok=True)

# COMMAND ----------

import time
import random

def get_random_user_agent():
    return {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            f'Chrome/{random.randint(110,118)}.0.{random.randint(1000,5999)}.{random.randint(0,199)} '
            'Safari/537.36'
        )
    }

def download_file(url, dest_path):
    try:
        response = requests.get(url, stream=True, headers=get_random_user_agent())
        if response.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f'Downloaded: {dest_path}')
        else:
            print(f'HTTP {response.status_code}: {url}')
            time.sleep(2)
    except Exception as e:
        print(f'Error downloading {url}: {e}')

# COMMAND ----------

current_date = datetime.now()
latest_available = current_date - timedelta(days=60)
start_year = 2020
end_year = latest_available.year
base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
dtype = dbutils.widgets.get("type")

print(f'Bronze download: {start_year} to {end_year}, up to month {latest_available.month}')

for year in range(start_year, end_year + 1):
        max_month = latest_available.month if year == end_year else 12
        for month in range(1, max_month + 1):
            filename = f'{dtype}_tripdata_{year}-{month:02d}.parquet'
            url = f'{base_url}/{filename}'
            dest_folder = os.path.join(bronze_dir, dtype, str(year))
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, filename)
            if not os.path.exists(dest_path):
                download_file(url, dest_path)
            else:
                print(f'Already exists: {dest_path}')

print('Bronze layer download complete. All raw files are in:', bronze_dir)
