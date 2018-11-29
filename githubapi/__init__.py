"""
GitHub Demo API
"""

__all__ = ['Repo']
__version__ = '0.0.1'


import posixpath
import urllib.parse


# Root GitHub URL (https://developer.github.com/v3/#current-version)
ROOT = 'https://api.github.com'


class Resource:
    """
    Web resource base class
    """
    def __init__(self, requestapi, path):
        """
        Initialize web resource

        Args:
            requestapi: REST API methods class
            path: resource URL
        """
        self._api = requestapi
        # Parsed resource response
        self._raw = None

        self.path = path

    def load(self):
        self._raw = self._api.get_json(self.path)


class Repo(Resource):
    """
    Repository API
    """
    def __init__(self, requestapi, owner, repository, api_root=ROOT):
        self._root = api_root
        self.owner = owner
        self.repository = repository
        path = urllib.parse.urljoin(self._root,
                                    posixpath.join(owner, repository))

        super().__init__(requestapi, path)


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
