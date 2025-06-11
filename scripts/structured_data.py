import pandas as pd
import os

def structured_data(path):
    try:
        df = pd.read_json('/opt/airflow/raw/raw.json')
    except ValueError as e:
        print(f"Error reading JSON file: {e}")
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(df)
    
    try:
        df.to_csv(path, index=False)
        print(f"Data successfully written to {path}")
    except Exception as e:
        print(f"An error occurred while writing to {path}: {e}")
        
# structured_data('foundation/structured_data.csv')