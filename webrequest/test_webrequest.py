import json.decoder
import unittest
import urllib.error

from . import *


class GetTest(unittest.TestCase):
    def test_valid(self):
        actual = get('https://api.github.com')

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


class GetJsonTest(unittest.TestCase):
    def test_valid(self):
        actual = get_json('https://api.github.com')

        self.assertIsInstance(actual, dict)
        self.assertIn('current_user_url', actual)
        self.assertEqual(actual.get('current_user_url'), 'https://api.github.com/user')

    def test_malformed(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            get_json('http://google.com')
