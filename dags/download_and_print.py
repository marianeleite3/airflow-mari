from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'mariane_moreira',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'download_and_print_dag',
    default_args=default_args,
    schedule_interval=None,  # Set the schedule interval according to your needs
    catchup=False,  # Prevent backfilling for past runs
    tags=['example'],
)

download_and_save_script = """
import requests

url = 'https://ifood-data-architect-test-source.s3-sa-east-1.amazonaws.com/consumer.csv.gz'
response = requests.get(url)
with open('/path/to/storage/consumer.csv.gz', 'wb') as f:
    f.write(response.content)
"""

download_task = KubernetesPodOperator(
    task_id='download_task',
    name='download-task',
    namespace='default',  # Specify the namespace
    image='python:3',  # Use a Python image
    cmds=["python", "-c"],
    arguments=[download_and_save_script],
    dag=dag,
)

print_script = """
with open('/path/to/storage/consumer.csv.gz', 'rb') as f:
    content = f.read()
    print(content)
"""

print_task = KubernetesPodOperator(
    task_id='print_task',
    name='print-task',
    namespace='default',  # Specify the namespace
    image='python:3',  # Use a Python image
    cmds=["python", "-c"],
    arguments=[print_script],
    dag=dag,
)

download_task >> print_task
