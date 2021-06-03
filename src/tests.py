
import requests
import json

URL_PREFIX = 'http://0.0.0.0:8888/api/'



def _display_response(_response):
    #json_object = json.loads(response.text)
    #json_formatted_str = json.dumps(json_object, indent=2)
    json_formatted_str = json.dumps(_response.json(), indent=2)
    print(json_formatted_str)


def read_all():
    url = URL_PREFIX + 'shortlinks'
    response = requests.get(url)
    print(response)
    _display_response(response)
    #print(response.json())


def create(_destination):
    url = URL_PREFIX + 'shortlinks'
    response = requests.post(url, data={'destination':_destination})
    print(response)



if __name__ == "__main__":
    print('Running tests...')
    read_all()
    create('https://www.bbc.com/')

