import json.decoder
import unittest
import urllib.error

from . import *
from . import Headers


class HeadersLinkTest(unittest.TestCase):
    def test_empty(self):
        self.assertIsNone(Headers._parse_links(None))
        self.assertIsNone(Headers._parse_links({}))

    def test_parsing(self):
        data = ('<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=15>; rel="next", '
                '<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=34>; rel="last", '
                '<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=1>; rel="first", '
                '<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=13>; rel="prev"')

        expected = {'next': 'https://api.github.com/search/code?q=addClass+user%3Amozilla&page=15',
                    'last': 'https://api.github.com/search/code?q=addClass+user%3Amozilla&page=34',
                    'first': 'https://api.github.com/search/code?q=addClass+user%3Amozilla&page=1',
                    'prev': 'https://api.github.com/search/code?q=addClass+user%3Amozilla&page=13'}

        self.assertEqual(expected, Headers._parse_links(data))

    def test_parsing_one(self):
        data = '<https://api.github.com/search/code?q=addClass+user%3Amozilla&page=15>; rel="next"'
        expected = {'next': 'https://api.github.com/search/code?q=addClass+user%3Amozilla&page=15'}

        self.assertEqual(expected, Headers._parse_links(data))


class GetTest(unittest.TestCase):
    def test_valid(self):
        actual = str(get('https://api.github.com'))

        self.assertIsInstance(actual, str)
        self.assertIn('github', actual)

    def test_get_invalid_url(self):
        with self.assertRaises(AttributeError):
            get(None)
        with self.assertRaises(urllib.error.URLError):
            get('htp:/hi')

    def test_nonexisting_url(self):
        with self.assertRaises(urllib.error.URLError):
            get('http://localhost/nope')


class RequestHeadersTest(unittest.TestCase):
    def setUp(self):
        self.response = get('https://api.github.com/repos/fastlane/fastlane/issues?per_page=100')

    def test_has_links(self):
        self.assertIn('Link', dict(self.response.headers._headers))
        self.assertIsNotNone(self.response.headers.links)


class GetJsonTest(unittest.TestCase):
    def test_valid(self):
        actual = get_json('https://api.github.com')

        self.assertIsInstance(actual, dict)
        self.assertIn('current_user_url', actual)
        self.assertEqual(actual.get('current_user_url'), 'https://api.github.com/user')

    def test_malformed(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            get_json('http://google.com')
