import json
import requests
from datetime import datetime, timedelta
import pandas as pd

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

GCP_PROJECT = "dataengineering1-433721"
BUCKET_NAME = "dataengineering1-433721_crypto_data_raw"
GCS_PATH = "crypto_raw_test/file"

url = "https://api.coingecko.com/api/v3/coins/markets"
api_params = {  # Renamed from `params` to `api_params`
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 250,
    'page': 1,
    'sparkline': False
}

def data_fetch_api(url, api_params):  # Renamed from `params` to `api_params`
    response = requests.get(url, params=api_params)  # Renamed here too
    data = response.json()
    
    with open("crypto_data.json", "w") as f:
        json.dump(data,f)


default_args = {
    "owner": "abhi",
    "depends_on_past": False
}

dag = DAG(
    dag_id="orchaestration",
    default_args=default_args,
    description="Fetch data using crypto API",
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2024, 11, 17),
    catchup=False
)

fetch_data_task = PythonOperator(
    task_id="fetch_data_using_api",
    python_callable=data_fetch_api,  # Pass function reference
    op_args=[url, api_params],  # Pass the renamed `api_params`
    dag=dag
)

upload_to_gcs_task = LocalFilesystemToGCSOperator(
    task_id = "upload_data_to_gcs_from_local",
    src = "crypto_data.json",
    dst = GCS_PATH + "_{{ ts_nodash }}.json",
    bucket = BUCKET_NAME,
    gcp_conn_id = "gcptest",
    dag = dag

)



fetch_data_task >> upload_to_gcs_task
