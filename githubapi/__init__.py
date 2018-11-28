"""
GitHub Demo API
"""

__all__ = ['Repo']
__version__ = '0.0.1'


import posixpath
import urllib.parse


# Root GitHub URL (https://developer.github.com/v3/#current-version)
ROOT = 'https://api.github.com'


class Repo:
    """
    Repository API
    """
    def __init__(self, requestapi, owner, repository, api_root=ROOT):
        self._api = requestapi

        self._root = api_root
        self.owner = owner
        self.repository = repository
        self.path = urllib.parse.urljoin(self._root,
                                         posixpath.join(owner, repository))
        self.raw = None

    def load(self):
        self.raw = self._api.get_json(self.path)


class Contributor:
    """
    Repository Contributor API
    """
    pass


class Pull:
    """
    Repository Pull-request API
    """
    pass


class Issue:
    """
    Repository Issue API
    """
    pass