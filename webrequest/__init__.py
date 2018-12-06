"""
Web Request Demo package

Provides REST Get method.
"""

__all__ = ['get', 'get_json']
__version__ = '0.0.1'


import base64
import urllib.request
import json


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
        self.links = self._parse_links(self._headers.get('Link')) or {}


class Response:
    """
    HTTP Response object
    """
    def __init__(self, url, credentials=()):
        self.url = None
        self.response = None
        self.headers = None

        self._credentials = credentials

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

    @property
    def credentials(self):
        """
        Format credential to HTTP Header format

        Returns:
            str
        """
        if not self._credentials:
            return None
        credentials = '{}:{}'.format(*self._credentials)
        encoded = base64.b64encode(credentials.encode('ascii'))
        return 'Basic {}'.format(encoded.decode('ascii'))

    def get(self, url):
        """
        Load via HTTP Get method

        Args:
            url (str): resource URL
        """
        if not url:
            raise AttributeError('Empty URL')

        self.url = url
        if self.credentials:
            request = urllib.request.Request(url)
            request.add_header('Authorization', self.credentials)
            self.response = urllib.request.urlopen(request)
        else:
            self.response = urllib.request.urlopen(self.url)
        self.headers = Headers(self.response.info())

    def json(self):
        """
        Parse JSON response

        Returns:
            dict or list
        """
        return json.loads(str(self))


def get(url, credentials=()):
    """
    Returns HTTP GET response

    Args:
        url (str): source URL
        credentials (tuple): login, password

    Returns:
        str
    """
    return Response(url, credentials=credentials)


def get_json(url, credentials=()):
    """
    Returns HTTP GET response as JSON-dict

    Args:
        url (str): source URL
        credentials (tuple): login, password

    Returns:
        dict
    """
    return Response(url, credentials=credentials).json()
