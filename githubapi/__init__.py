"""
GitHub Demo API
"""

__all__ = ['Resource', 'Container', 'Repo']
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
        self._raw = {}

        self.path = path

    def __getattr__(self, item):
        """
        Get value from GitHub API response
        """
        try:
            return self._raw[item]
        except KeyError:
            raise AttributeError(f'GitHub API does not store `{item}` attribute')

    def load(self):
        self._raw = self._api.get_json(self.path)


class Container(Resource):
    def __getitem__(self, item):
        return self._raw[item]

    def __iter__(self):
        return iter(self._raw)


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


class Contributors(Container):
    """
    Repository Contributor API
    """
    pass


class Pulls(Container):
    """
    Repository Pull-request API
    """
    pass


class Issues(Container):
    """
    Repository Issue API
    """
    pass
