# File for testing wiki.py, ignore

import requests
from config import BASE_URL

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

for doc in sample_documents:
    response = requests.post("{}documents/{}".format(BASE_URL, doc['title']), doc['json'])
    print(response.json())

response = requests.post('{}documents/Flask'.format(BASE_URL), {'content': 'This is the latest latest Flask wiki'})
print(response.json())

#response = requests.get('{}documents/Flask/1800pm'.format(BASE_URL), {'content': 'This is the latest Flask wiki'})
