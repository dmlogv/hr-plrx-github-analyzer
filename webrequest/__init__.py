"""
Web Request Demo package

Provides REST Get method.
"""

__all__ = ['get', 'get_json']
__version__ = '0.0.1'


import urllib.request
import json


def get(url):
    """
    Returns HTTP GET response

    Args:
        url (str): source URL

    Returns:
        str
    """
    response = urllib.request.urlopen(url)
    return response and response.read().decode()


def get_json(url):
    """
    Returns HTTP GET response as JSON-dict

    Args:
        url (str): source URL

    Returns:
        dict
    """
    return json.loads(get(url))
