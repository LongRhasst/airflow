#job1
import requests

def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        if response.status_code == 404:
            return {'status': 'not found'}
        elif response.status_code == 500:
            return {'status': 'internal server error'}
        else:
            return {'status': 'unknown error'}
