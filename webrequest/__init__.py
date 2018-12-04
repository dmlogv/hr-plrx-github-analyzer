"""
Web Request Demo package

Provides REST Get method.
"""

__all__ = ['get', 'get_json']
__version__ = '0.0.1'


import urllib.request
import json


def use_auth(user, password):
    pass


class Headers:
    """
    HTTP Headers
    """
    @staticmethod
    def _parse_links(links):
        """
        HTTP Link Header

        Args:
            links (str): Raw HTTP Link Header

        Returns:
            dict(rel, url)
        """
        if not links:
            return None

        # Sorry for it all
        # Replace '<', '>', ' '
        cleaned = links.translate(str.maketrans(dict.fromkeys('<> ')))
        # Split separate links by rel
        by_rel = [link.split(';') for link in cleaned.split(',')]
        # Split rel from URL
        by_fields = {rel.replace('rel="', '').replace('"', ''): url for url, rel in by_rel}
        return by_fields

    def __init__(self, headers):
        self._headers = headers
        self.links = self._parse_links(self._headers.get('Link'))


class Response:
    """
    HTTP Response object
    """
    def __init__(self, url):
        self.url = None
        self.response = None
        self.headers = None

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
        """
        Load via HTTP Get method

        Args:
            url (str): resource URL
        """
        if not url:
            raise AttributeError('Empty URL')

        self.url = url
        self.response = urllib.request.urlopen(self.url)
        self.headers = Headers(self.response.info())

    def json(self):
        """
        Parse JSON response

        Returns:
            dict or list
        """
        return json.loads(str(self))


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
