# job2
import pandas as pd
import os
from airflow.utils.log.logging_mixin import LoggingMixin

def structured_data(input_path, **context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='job1_get_data')
    log = LoggingMixin().log
    # log.info(f"Pulled data from XCom: {data}")
    
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    
    df = pd.DataFrame(data)
    # log.info(f"DataFrame created with shape: {df.shape}")  # Debugging line to check DataFrame shape
    print(df.head())  # Debugging line to check the DataFrame structure
    try:
        df.to_csv(input_path, index=False)
        return f"Data written to {input_path}"
    except Exception as e:
        return f"Error: {str(e)}"
    
