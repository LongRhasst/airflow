from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow')


from scripts.call_data_api import get_data
from scripts.structured import structured_data
from scripts.transform_data import process_transform
from scripts.save import get_df

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='my_dag',
    default_args=default_args,
    description='Run 4 jobs every day at 8:00 a.m',
    schedule_interval='0 8 * * *',  
    catchup=False,
    tags=['data_pipeline']
) as dag:

    t1 = PythonOperator(
        task_id='job1_get_data',
        python_callable=get_data,
        op_kwargs={'url': 'https://restcountries.com/v3.1/all'}
    )

    t2 = PythonOperator(
        task_id='job2_structured_data',
        python_callable=structured_data,
        op_kwargs={'input_path': '/opt/airflow/foundation/restcountries.csv'}
    )

    t3 = PythonOperator(
        task_id='job3_rename_columns',
        python_callable=process_transform,
        op_kwargs={'csv_path': '/opt/airflow/foundation/restcountries.csv'}
    )

    t4 = PythonOperator(
        task_id='job4_save_df',
        python_callable=get_df
    )

    t1 >> t2 >> t3 >> t4
