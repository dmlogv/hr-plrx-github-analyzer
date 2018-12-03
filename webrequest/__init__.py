"""
Web Request Demo package

Provides REST Get method.
"""

__all__ = ['get', 'get_json']
__version__ = '0.0.1'


import urllib.request
import json


class Response:
    """
    HTTP Response object
    """
    def __init__(self, url):
        self.url = None
        self.response = None
        self.headers = {}

        self.get(url)

    def __repr__(self):
        return f'<{self.__class__.__name__} url="{self.url}">'

    def __str__(self):
        """
        Response string representation

        Returns:
            str
        """
        return self.response.read().decode()

    def get(self, url):
        if not url:
            raise AttributeError('Empty URL')

        self.url = url
        self.response = urllib.request.urlopen(self.url)
        self.headers = dict(self.response.info())

    def json(self):
        """
        Parse JSON response

        Returns:
            dict or list
        """
        return json.load(self.response)


def get(url):
    """
    Returns HTTP GET response

    Args:
        url (str): source URL

    Returns:
        str
    """
    return Response(url)


def get_json(url):
    """
    Returns HTTP GET response as JSON-dict

    Args:
        url (str): source URL

    Returns:
        dict
    """
    return Response(url).json()
