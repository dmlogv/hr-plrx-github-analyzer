"""
GitHub Demo API
"""

__all__ = ['parse_url', 'Resource', 'Container', 'Repo']
__version__ = '0.0.1'


import posixpath
import urllib.parse


# Root GitHub URL (https://developer.github.com/v3/#current-version)
ROOT = 'https://api.github.com'


def parse_url(url):
    """
    Extract owner and repo from GitHub URL

    Args:
        url (str): valid link

    Returns:
        (owner, repo)
    """
    parsed_url = urllib.parse.urlsplit(url)
    if not parsed_url.netloc:
        raise ValueError(f'Url {url} is not valid')
    path = parsed_url.path.strip('/')
    try:
        owner, repo, *_ = path.split('/')
    except ValueError:
        raise ValueError(f'Url {url} does not contain path to repo')

    return owner, repo


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
        self._response = None
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

    def __repr__(self):
        return f'<{self.__class__.__name__} path="{self.path}">'

    def load(self):
        self._response = self._api.get(self.path)
        self._raw = self._response.json()

        return self


class Container(Resource):
    """
    Web resources container
    """
    def __getitem__(self, item):
        return self._raw[item]

    def __iter__(self):
        return iter(self._raw)

    def __repr__(self):
        return (f'<{self.__class__.__name__} '
                f'path="{self.path}" '
                f'items={len(self._raw)}>')

    def load(self):
        self._response = self._api.get()
        self._raw = self._response.json()

        return self


class Repo(Resource):
    """
    Repository API
    """
    resource_url = 'repos'

    def __init__(self, requestapi, owner, repository, api_root=ROOT):
        self._api = requestapi
        self._root = api_root
        self.owner = owner
        self.repository = repository

        self.contributors = None
        self.pulls = None
        self.issues = None

        path = urllib.parse.urljoin(self._root, posixpath.join(
            self.resource_url, owner, repository))

        super().__init__(self._api, path)

    def load_containers(self):
        # Bypass empty API arguments
        empty_substitute = {'/number': ''}

        self.contributors = Contributors(self._api, self.contributors_url.format(None)).load()
        self.pulls = Pulls(self._api, self.pulls_url.format(**empty_substitute)).load()
        self.issues = Issues(self._api, self.issues_url.format(**empty_substitute)).load()

        return self


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
