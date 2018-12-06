"""
GitHub Demo API
"""

__all__ = ['parse_url', 'add_url_params', 'Resource', 'Container', 'Repo']
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


def add_url_params(url, params):
    """
    Add parameters to URL

    Args:
        url (str): base URL
        params (dict):

    Returns:
        str: URL
    """
    parts = list(urllib.parse.urlparse(url))
    existing_params = urllib.parse.parse_qs(parts[4])
    existing_params.update(params)
    parts[4] = urllib.parse.urlencode(existing_params)

    return urllib.parse.urlunparse(parts)


class Resource:
    """
    Web resource base class
    """
    def __init__(self, api=None, path=None, **kwargs):
        """
        Initialize web resource

        Args:
            api: REST API methods class
            path: resource URL
            **kwargs: API arguments
        """
        self._api = api
        self._api_kwargs = kwargs
        self.path = path

        self._response = None
        # Parsed resource response
        self._raw = {}

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

    def load(self, api=None, path=None, **kwargs):
        """
        Load web resource

        Args:
            api: REST API methods class
            path: resource URL
            **kwargs: API arguments

        Returns:
            Resource
        """
        self._api = api or self._api
        self.path = path or self.path
        self._api_kwargs = kwargs or self._api_kwargs

        if not self._api:
            raise ValueError('api argument did not present')
        if not self.path:
            raise ValueError('path argument did not present')

        self._response = self._api.get(self.path, **self._api_kwargs)
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

    def load(self, api=None, path=None, **kwargs):
        """
        Load container with pagination support

        Returns:
            Container
        """
        super().load(api, path, **kwargs)

        current = self._response
        while True:
            next_url = current.headers.links.get('next')
            if not next_url:
                break
            current = self._api.get(next_url, **self._api_kwargs)
            self._raw.extend(current.json())

        return self


class Repo(Resource):
    """
    Repository API
    """
    resource_url = 'repos'
    params = {'per_page': 100}

    def __init__(self, owner, repository, api_root=ROOT, api=None, **kwargs):
        self._root = api_root
        self.owner = owner
        self.repository = repository

        self.contributors = None
        self.pulls = None
        self.issues = None

        path = urllib.parse.urljoin(self._root, posixpath.join(
            self.resource_url, owner, repository))

        super().__init__(api, path, **kwargs)

    def load_containers(self):
        """
        Load resource containers

        Returns:
            Repo
        """
        # Bypass empty API arguments
        empty_substitute = {'/number': ''}

        self.contributors = Contributors().load(
            self._api,
            add_url_params(self.contributors_url.format(None), self.params),
            **self._api_kwargs)
        self.pulls = Pulls().load(
            self._api,
            add_url_params(self.pulls_url.format(**empty_substitute), self.params),
            **self._api_kwargs)
        self.issues = Issues().load(
            self._api,
            add_url_params(self.issues_url.format(**empty_substitute), self.params),
            **self._api_kwargs)

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
