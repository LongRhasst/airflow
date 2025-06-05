#job4
from sqlalchemy import create_engine
import pandas as pd
import os

DB_USER = os.getenv('MYSQL_USER', 'airflow')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'airflow')
DB_HOST = os.getenv('MYSQL_HOST', 'mysql')
DB_PORT = os.getenv('MYSQL_PORT', '3306')
DB_NAME = os.getenv('MYSQL_DATABASE', 'airflow')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def save_to_mysql(df, table_name):
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Successfully saved DataFrame to table '{table_name}'.")
    except Exception as e:
        print(f"Error saving DataFrame to table '{table_name}': {e}")
        raise

def get_df():
    countries_csv_path = '/opt/airflow/trusted/countries.csv'
    country_currency_csv_path = '/opt/airflow/trusted/country_currency.csv'

    try:
        print(f"Reading {countries_csv_path}...")
        df_countries = pd.read_csv(countries_csv_path)
        save_to_mysql(df_countries, 'countries')
    except FileNotFoundError:
        print(f"Error: {countries_csv_path} not found.")
    except Exception as e:
        print(f"An error occurred while processing countries.csv: {e}")

    try:
        print(f"Reading {country_currency_csv_path}...")
        df_country_currency = pd.read_csv(country_currency_csv_path)
        save_to_mysql(df_country_currency, 'country_currency')
    except FileNotFoundError:
        print(f"Error: {country_currency_csv_path} not found.")
    except Exception as e:
        print(f"An error occurred while processing country_currency.csv: {e}")

if __name__ == '__main__':
    print(f"Attempting to connect to DB with URL: {DATABASE_URL} (for script execution context)")
    if not os.path.exists('/opt/airflow/trusted'):
        os.makedirs('/opt/airflow/trusted', exist_ok=True)
    
    get_df()