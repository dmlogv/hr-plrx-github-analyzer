import unittest

from . import *


class ParseUrlTest(unittest.TestCase):
    def test_parse_url(self):
        self.assertEqual(('dm-logv', 'aero-stat'),
                         parse_url('https://github.com/dm-logv/aero-stat/'))
        self.assertEqual(('dm-logv', 'aero-stat'),
                         parse_url('https://github.com/dm-logv/aero-stat/issues'))
        self.assertEqual(('dm-logv', 'aero-stat'),
                         parse_url('//github.com/dm-logv/aero-stat/issues'))
        self.assertEqual(('owner', 'repo'), parse_url('//gh.c/owner/repo/'))

        with self.assertRaises(ValueError):
            parse_url('gh.c/owner/repo/')

        with self.assertRaises(ValueError):
            parse_url('//gh.c/owner/')


class Api:
    """
    WebApi mock class
    """
    @staticmethod
    def get(url, **kwargs):
        """
        Returns Response-like object

        Args:
            url (str): mock URL

        Returns:
            Response
        """
        class Response:
            def __init__(self, url):
                self.url = url
                self.headers = None

            def json(self):
                return {'url': self.url}

        return Response(url)

    @staticmethod
    def get_json(url, **kwargs):
        """
        Returns JSON-like dict

        Args:
            url (str): mock URL

        Returns:
            dict
        """
        return Api.get(url, **kwargs).json


class LoadedResourceTest(unittest.TestCase):
    def setUp(self):
        self.resource = Resource(Api, 'http://contoso.com')
        self.resource.load()

    def test_getattr(self):
        self.assertEqual('http://contoso.com', self.resource.url)

    def test_get_not_existing_attr(self):
        with self.assertRaises(AttributeError):
            self.resource.jabba_the_hutt


class ParsedResourceTest(unittest.TestCase):
    def setUp(self):
        self.resource = Resource()

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.resource.load()

    def test_empty_path(self):
        with self.assertRaises(ValueError):
            self.resource.load(api=Api)
        with self.assertRaises(ValueError):
            self.resource.load(api=Api, path='')

    def test_empty_api(self):
        with self.assertRaises(ValueError):
            self.resource.load(path='b')
        with self.assertRaises(ValueError):
            self.resource.load(path='b', api=None)



class ContainerTest(unittest.TestCase):
    def setUp(self):
        self.container = Container(None, None)
        self.container._raw = [{'name': 'Mike'},
                               {'name': 'Nick'},
                               {'name': 'Oak'}]

    def test_index(self):
        self.assertEqual({'name': 'Nick'}, self.container[1])
        with self.assertRaises(IndexError):
            self.container[10]

    def test_iter(self):
        for i, item in enumerate(self.container):
            self.assertEqual(self.container[i], item)


class RepoTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo('dm-logv', 'aero-stat', 'http://gh.com', Api)

    def test_init(self):
        self.assertEqual('dm-logv', self.repo.owner)
        self.assertEqual('aero-stat', self.repo.repository)
        self.assertEqual('http://gh.com', self.repo._root)

    def test_path(self):
        self.assertEqual('http://gh.com/repos/dm-logv/aero-stat', self.repo.path)

    def test_load(self):
        self.repo.load()
        self.assertEqual({'url': self.repo.path}, self.repo._raw)
