import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('/opt/airflow')
from process.transform_data import processAll, processCurrencies

def clean_data(path):
    os.makedirs('/opt/airflow/trusted', exist_ok=True)
    
    raw_df = pd.read_csv(path)
    
    df_processed = raw_df[['name', 'ccn3', 'cca3', 'independent', 'status', 'currencies' ,'capital', 'altSpellings', 'region', 'languages',
                    'area', 'maps', 'timezones', 'continents', 'flags', 'translations', 'startOfWeek', 'capitalInfo', ]].copy()
    
    
    df_processed = processAll(df_processed)
    print(type(df_processed))

    # print(f"Processed DataFrame columns: {df_processed}")
    df_processed.to_csv('/opt/airflow/trusted/cleaned_data.csv', index=False, encoding='utf-8')
    print(f"Data successfully written to /opt/airflow/trusted/cleaned_data.csv")
    
# clean_data('foundation/structured_data.csv')

