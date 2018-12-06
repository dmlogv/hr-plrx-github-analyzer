"""
GitHub Demo API
"""

__all__ = ['parse_url', 'add_url_params', 'Resource', 'Container', 'Repo']
__version__ = '0.0.1'


import datetime
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
    dtm_format = '%Y-%m-%dT%H:%M:%SZ'

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
        self.parse(self._response.json())

        return self

    def parse(self, data):
        """
        Assign JSON data to Resource data with type conversion

        Args:
            data (dict): resource data

        Returns:
            Resource
        """
        self._raw = data

        for k, v in self._raw.items():
            if k.endswith('_at'):
                self._raw[k] = v and datetime.datetime.strptime(v, self.dtm_format)

        return self


class Container(Resource):
    """
    Web resources container
    """
    item_type = Resource

    def __init__(self, api=None, path=None, **kwargs):
        super().__init__(api=None, path=None, **kwargs)

        self.items = []

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items)

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

    def parse(self, data, resource=None):
        """
        Assign JSON data to Container data

        Args:
            data (list): resource data
            resource (type): conversion type

        Returns:
            Resource
        """
        resource = resource or self.item_type

        self._raw = data
        self.items = [resource().parse(item) for item in self._raw]

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

    def load_container(self, container, url):
        """
        Load resource container

        Args:
            container(type): Container class
            url (str): container URL

        Returns:
            Container
        """
        return container().load(self._api, add_url_params(url, self.params), **self._api_kwargs)

    def load_containers(self):
        """
        Load resource containers

        Returns:
            Repo
        """
        # Bypass empty API arguments
        empty_substitute = {'/number': ''}

        self.contributors = self.load_container(Contributors, self.contributors_url.format(None))
        self.pulls = self.load_container(Pulls, self.pulls_url.format(**empty_substitute))
        self.issues = self.load_container(Issues, self.issues_url.format(**empty_substitute))

        return self


class Contributor(Resource):
    """
    Repository Contributor API
    """
    pass


class Pull(Resource):
    """
    Repository Pull-request API
    """
    pass


class Issue(Resource):
    """
    Repository Issue API
    """
    pass


class Contributors(Container):
    """
    Repository Contributor API
    """
    item_type = Contributor


class Pulls(Container):
    """
    Repository Pull-request API
    """
    item_type = Pull


class Issues(Container):
    """
    Repository Issue API
    """
    item_type = Issue
