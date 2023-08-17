import os
import requests
from google.cloud import storage
import gzip
import json
import google.auth
from google.oauth2 import service_account
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta


bucket_name = 'marileite3bucket'

credentials_dict = {
    "type": "service_account",
    "project_id": "able-reef-396111",
    "private_key_id": "44a410649db48f62f4c2e7c2e92dae283beb8c2b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDRKyHM9H6ptlP/\nQuKUOXB7w1PodfiHOAMbL1FKa9Jm+xml0qQSzQQRgUuSWeLHAT2QV23RhduUfUey\nnqVR8M4xjVznBHt6abmXOpLmG+e0UlSENu//HC/WB3tag3x8YLYLU6YOvqPgFoOm\n/+x8ZAZNZRzTlAoCCbyrFM4BIdwrb+UHlCr8LpSe9RscI03i3YNpszC3lMFvp98/\nLreYqr9Pa1xMAzHaNIxBEFA4n1e0UmNZh6IWmqvJSmkEEH0xQ02zP36diRJ+fJSa\nFPwZla3tsf2jv+g+YgV7j/p/T4rtINc1aEcbAFGwJ9x6UYycN6h0hhJRXhBefYWY\n3f6RVYn9AgMBAAECggEAB8HprMGDl2qRm8W2BAkg/MIThlX7u+jDUA/gRq+QMS1j\nt99DolveqFc11OLHCETpl4UaklBR2A8REz+S141kBE6fG6/ySWm1jkrdQFytalC5\nsuFGY4fULAQBL+vw+GbuJtDjzNJcCbdOtilHMsd95q3BlNo9yHIRKyd9dWl1Ui9b\nbVfX1axA4hi6JcVBhCUKIpVF9zRGkOnNPebeSUQzwioesI3+jIzG6iypB14CpC/j\nKe/m533RXbmeR6j+/OfOWTxeurbV5tOQ3On52r370rxIknq07DVz50v+m/8xY/8P\nGx0O6xtyb8b0ejsytbY48/EJBZ6QRJMzNXm0YpUxgQKBgQDy32r3mdD44R0YhLec\n9ObdLODurKx5IphESfK5RrZfF8PBZpeF/MoEwe4U9lxWSj1R5qWId8nPMK/ITsKv\np+CbKn4+Q+oAuoRIIPpQbxzTZd3ignkU/Etvp2BWwB4RaLt+5quT8rrFpfe6TenP\n39xk7W4zOVXCHBws9+Ab3a88gQKBgQDceVrwZWtoo87osNBlIfhpEPRcRVHKA7vh\n32Bu99MJu9LNsCahBUYAwa6gDS7PA2xIpgUlXdMmY5Mj8saM9O9OIRMyj65dRl+1\nGzcva+Qp5VYxd1meUK4VLwxJbFdcBiA5R7T7QIctWNU86kBwmrrhjwLqbSJpZp/B\nlXWDh0F/fQKBgQCbl3fOkbLnjkf2iiebHOW9sd+T5/lCTWBg90LRYTS6bN4Sy2et\nBcpiC987fKyg90SbcHiBmcQmwNkMKTDeGV1x6mIf/6AswVC3aLET0GsWHv9r+gwZ\n3ptxNzgnu0JIAuGDJcGrsWfn8TBoITv12UM3QUhE9qkzBpEiWdYv4/A8gQKBgBX7\nK2voUKsgGdLtPfm3R1MCU7qXVq4zbRn58V1e6/V+emfzdgZ7xhzxMn3WkqIlDzi3\nBLBTCGg9aUAeRllrWiiJ96YE2TeHeqdNzVS3Bwp+SPeplI/KL3EBPdJcMOGF4tST\nJ6IdLt0AjFIEcORJKPSwE3RX6SRlDOx6ADta0tbpAoGAfDQybSSw2QZakgAqjOFQ\nAPHlrNYqQjBgJqka121rwEfbs8F0p8kJ3PAlK7kMMgzayIA8h/sMB0o6cSuG9ZFI\nDenYxVs90pb2e2blqhFaN5jYNJ+G/HLGjVN6WBn59K7LaJ7QD02YCUbHmMJkSB/k\n9F2nEfGrbBFosi65ly9d0OE=\n-----END PRIVATE KEY-----\n",
    "client_email": "myserviceaccount@able-reef-396111.iam.gserviceaccount.com",
    "client_id": "104440612820737559485",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myserviceaccount%40able-reef-396111.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

credentials = service_account.Credentials.from_service_account_info(credentials_dict)

client = storage.Client(credentials=credentials)

def upload_to_storage():

    url = 'https://ifood-data-architect-test-source.s3-sa-east-1.amazonaws.com/consumer.csv.gz'
    response = requests.get(url)
    if response.status_code == 200:
        compressed_content = response.content
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        exit(1)

    decompressed_content = gzip.decompress(compressed_content)

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('consumer.csv')
    blob.upload_from_string(decompressed_content)

    print("File uploaded to Google Cloud Storage.")

def print_content():
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('consumer.csv')
    downloaded_content = blob.download_as_text()
    print("File Content:")
    print(downloaded_content)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 17),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_mari',
    default_args=default_args,
    schedule_interval= '@daily', 
    catchup=False,
)

upload_task = KubernetesPodOperator(
    task_id='upload_to_storage',
    name='upload-storage-pod',
    namespace='airflow',
    image='mareleite3/airflow', 
    cmds=["python", "-c"],
    arguments=[upload_to_storage], 
    get_logs=True,
    dag=dag,
)

print_task = KubernetesPodOperator(
    task_id='print_content',
    name='print-content-pod',
    namespace='airflow',
    image='mareleite3/airflow',
    cmds=["python", "-c"],
    arguments=[print_content], 
    get_logs=True,
    dag=dag,
)

upload_task >> print_task
