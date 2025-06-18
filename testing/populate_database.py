import requests
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_URL

sample_documents = [
    {
        'title': 'McIntosh',
        'json': {
            'content': 'This is the McIntosh wiki'
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
