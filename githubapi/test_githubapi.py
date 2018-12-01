import unittest

from . import *


class Api:
    """
    WebApi mock class
    """
    @staticmethod
    def get_json(url):
        """
        Returns JSON-like dict

        Args:
            url (str): mock URL

        Returns:
            dict
        """
        return {'url': url}


class ResourceTest(unittest.TestCase):
    def setUp(self):
        self.resource = Resource(Api, 'http://contoso.com')
        self.resource.load()

    def test_getattr(self):
        self.assertEqual('http://contoso.com', self.resource.url)

    def test_get_not_existing_attr(self):
        with self.assertRaises(AttributeError):
            self.resource.jabba_the_hutt


class RepoTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo(Api, 'dm-logv', 'aero-stat', 'http://gh.com')

    def test_init(self):
        self.assertEqual('dm-logv', self.repo.owner)
        self.assertEqual('aero-stat', self.repo.repository)
        self.assertEqual('http://gh.com', self.repo._root)

    def test_path(self):
        self.assertEqual('http://gh.com/dm-logv/aero-stat', self.repo.path)

    def test_load(self):
        self.repo.load()
        self.assertEqual({'url': self.repo.path}, self.repo._raw)
