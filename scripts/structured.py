# job2
import pandas as pd
import os

def structured_data(input_path, **context):
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='job1_get_data')
    
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    
    df = pd.DataFrame(data)
    try:
        df.to_csv(input_path, index=False)
        return f"Data written to {input_path}"
    except Exception as e:
        return f"Error: {str(e)}"