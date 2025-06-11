import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# MySQL connection from environment variables
DATABASE_URL = os.getenv('MYSQL_URL', 'mysql+mysqlconnector://user:123465@mysql:3306/user')
print(f"Using database URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
def save_to_mysql(df, table_name):
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Data successfully written to {table_name} table in MySQL database.")
    except Exception as e:
        print(f"An error occurred while saving data to MySQL: {e}")
        
def save():
    countries_csv_path = '/opt/airflow/trusted/cleaned_data.csv'
    country_currency_csv_path = '/opt/airflow/foundation/structured_data.csv'
    currency_csv_path = '/opt/airflow/trusted/currencies.csv'
    
    #save coutries data to database
    try:
        print(f'Reading coutries data from {countries_csv_path}')
        df = pd.read_csv(countries_csv_path)
        save_to_mysql(df, 'countries')
    except FileNotFoundError:
        print(f"File not found: {countries_csv_path}")
    except pd.errors.EmptyDataError:
        print(f"No data found in the file: {countries_csv_path}")
    except Exception as e:
        print(f"An error occurred while processing {countries_csv_path}: {e}")
        
    #save country currency data to database
    try:
        print(f'Reading country currency data from {country_currency_csv_path}')
        df = pd.read_csv(country_currency_csv_path)
        save_to_mysql(df, 'country_currency')
    except FileNotFoundError:
        print(f"File not found: {country_currency_csv_path}")
    except pd.errors.EmptyDataError:
        print(f"No data found in the file: {country_currency_csv_path}")
    except Exception as e:
        print(f"An error occurred while processing {country_currency_csv_path}: {e}")
        
    #save currency data to database
    try:
        print(f'Reading currency data from {currency_csv_path}')
        df = pd.read_csv(currency_csv_path)
        save_to_mysql(df, 'currencies')
    except FileNotFoundError:
        print(f"File not found: {currency_csv_path}")
    except pd.errors.EmptyDataError:
        print(f"No data found in the file: {currency_csv_path}")
    except Exception as e:
        print(f"An error occurred while processing {currency_csv_path}: {e}")