from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow')

from scripts.request_api import request_api
from scripts.clean_data import clean_data
from scripts.structured_data import structured_data
from scripts.save import save

default_args = {
    'owner' : 'airflow',
    'start_date' : datetime(2025, 6, 10),
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5),
}

with DAG(
    dag_id='my_dag',
    default_args=default_args,
    description='DAG run 4 job cleaning data',
    schedule_interval='0 8 * * *',  # Cron format: At 8:00 AM every day
    catchup=False,
    tags=['data_pipeline', 'cleaning']
) as dag:
    
    t1 = PythonOperator(
        task_id='request_data',
        python_callable=request_api,
        op_kwargs={'url': 'https://restcountries.com/v3.1/independent?status=true'},
    )
    
    t2 = PythonOperator(
        task_id='clean_data',
        python_callable=structured_data,
        op_kwargs={'path': '/opt/airflow/foundation/structured_data.csv'},
    )
    
    t3 = PythonOperator(
        task_id='process_data',
        python_callable=clean_data,
        op_kwargs={'path': '/opt/airflow/foundation/structured_data.csv'},
    )
    
    t4 = PythonOperator(
        task_id='save_data',
        python_callable=save,
    )
    
    t1 >> t2 >> t3 >> t4