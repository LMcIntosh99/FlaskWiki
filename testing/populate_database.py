import requests

BASE_URL = 'http://127.0.0.1:5000/'
sample_documents = [
    {
        'title': 'WikiTest',
        'json': {
            'content': 'This is the WikiTest wiki'
        }
    },
    {
        'title': 'Python',
        'json': {
            'content': 'This is the Python wiki'
        }
    },
    {
        'title': 'Flask',
        'json': {
            'content': 'This is the Flask wiki'
        }
    }
]


def populate():
    print('Populating database...')
    for doc in sample_documents:
        requests.post("{}documents/{}".format(BASE_URL, doc['title']), doc['json'])
    print("Finished")
