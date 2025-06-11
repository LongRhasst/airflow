import requests
import json

def request_api(url):
    try:
        response = requests.get(url)
        data = response.json()
        # print(type(data))  # Print the type of the data
        if response.status_code == 200:
            path = '/opt/airflow/raw/raw.json'
            data = json.dumps(data, indent=4)
            with open(path, 'w') as file:
                file.write(data)
    except requests.exceptions.ConnectionError as conn:
        print(f"Request failed: {conn} - Status code: {response.status_code if 'response' in locals() else 'N/A'}")
    except  requests.exceptions.Timeout as timeout:
        print(f"Request timed out: {timeout}")
