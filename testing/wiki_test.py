import unittest
import requests
from populate_database import populate
from config import BASE_URL


class RestTest(unittest.TestCase):

    def test_documents_get(self):
        response = requests.get("{}documents".format(BASE_URL))
        self.assertEqual(['Flask', 'WikiTest', 'Python'], response.json())

    def test_document_title_get(self):
        response = requests.get("{}documents/WikiTest".format(BASE_URL))
        self.assertEqual('WikiTest', response.json()[0]['title'])
        self.assertEqual('This is the WikiTest wiki', response.json()[0]['content'])


if __name__ == '__main__':
    populate()
    unittest.main()
