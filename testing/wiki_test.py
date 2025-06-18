import unittest
import requests
from populate_database import populate
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_URL


class RestTest(unittest.TestCase):

    def test_documents_get(self):
        response = requests.get("{}documents".format(BASE_URL))
        self.assertEqual(['Flask', 'McIntosh', 'Python'], response.json())

    def test_document_title_get(self):
        response = requests.get("{}documents/McIntosh".format(BASE_URL))
        self.assertEqual('McIntosh', response.json()[0]['title'])
        self.assertEqual('This is the McIntosh wiki', response.json()[0]['content'])


if __name__ == '__main__':
    populate()
    unittest.main()
