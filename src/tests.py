
import requests


URL_PREFIX = 'http://0.0.0.0:8888/api/'


def read_all():
    url = URL_PREFIX + 'shortlinks'
    response = requests.get(url)
    print(response)
    print(response.json())


if __name__ == "__main__":
    print('Running tests...')
    read_all()

