"""
Repository analyzer
"""

__all__ = []
__version__ = '0.0.1'

import datetime
import operator


class Report:
    """
    Repository analysis and reporting
    """
    name = 'Main report'
    headers = ()

    @staticmethod
    def filter_by_state(container, state):
        """
        Filter container by item state

        Item have to contains state field.

        Args:
            container (Container, e. g. githubapi.Container): iterable container
            state (str): value

        Returns:

        """
        return [item for item in container if item.state == state]

    def __init__(self, repo):
        self.repo = repo
        self.results = []

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}" for {self.repo}>'

    def analyze(self):
        """
        Analyze repository

        Returns:
            Report
        """
        return self

    def table(self):
        """
        Get results in tabular format

        Returns:
            str
        """
        return (
            f'{self.name}\n' +
            '-' * len(self.name) + '\n' +
            '\t'.join(map(str, self.headers)) + '\n' +
            '\n'.join(['\t'.join(map(str, row)) for row in self.results]) + '\n\n'
            )

    def json(self):
        """
        Get result in JSON-able format

        Returns:
            dict
        """
        return {
            'name': self.name,
            'headers': list(self.headers),
            'results': [
                dict(zip(self.headers, row))
                for row in self.results
                ]
            }


class DateLimitedReport(Report):
    """
    Repository analysis limited by resource dates
    """
    @staticmethod
    def filter_by_date_bounds(container, start_date, end_date):
        """
        Filter container by data bounds.

        Container have to contains created_at, closed_at fields

        Args:
            container (Container, e. g. githubapi.Container): iterable container
            start_date (datetime.datetime): min date bound
            end_date (datetime.datetime): max date bound

        Returns:
            list
        """
        return [item for item in container
                if (item.created_at >= start_date
                    and (item.closed_at is None
                         or item.closed_at < end_date))]

    @staticmethod
    def filter_old(container, end_date, threshold):
        """
        Filter container by difference between created_at and closed_at

        Args:
            container: Container, e. g. githubapi.Container
            end_date (datetime.datetime): max date bound
            threshold (datetime.datetime): max difference

        Returns:

        """
        return [item for item in container
                if ((item.closed_at or end_date)
                    - item.created_at).days > threshold]

    def __init__(self, repo, start_date, end_date):
        super().__init__(repo)

        self.start_date = start_date or datetime.datetime(1900, 1, 1)
        self.end_date = end_date or datetime.datetime.now()


class ActiveContributors(Report):
    """
    Top of repository contributors

    Returns logins and number of their commits in reversed order.
    """
    name = 'Active contributors'
    headers = ('Login', 'Commit number')

    def __init__(self, repo, top=30):
        """

        Args:
            repo: repository
            top: number of contributors to output
        """
        super().__init__(repo)

        self.top = top

    def analyze(self):
        contributors = [(c.login, c.contributions)
                        for c in self.repo.contributors]
        contributors.sort(key=operator.itemgetter(1), reverse=True)

        self.results = contributors[:self.top]

        return self


class OpenedClosedPulls(DateLimitedReport):
    """
    Number of opened ad closed pull-requests
    """
    name = 'Opened and closed pulls'
    headers = ('Opened', 'Closed')

    def analyze(self):
        pulls = self.filter_by_date_bounds(
            self.repo.pulls, self.start_date, self.end_date)
        opened = len(self.filter_by_state(pulls, 'open'))
        closed = len(self.filter_by_state(pulls, 'closed'))

        self.results = [(opened, closed)]

        return self


class OldPulls(DateLimitedReport):
    """
    Number of old pull-requests (non-closed in N days)
    """
    name = 'Old pull-requests'
    headers = ('Old pulls number',)

    def __init__(self, repo, start_date, end_date, days=30):
        """
        Args:
            days (int): days to old
        """
        super().__init__(repo, start_date, end_date)

        self.days = days

    def analyze(self):
        pulls = self.filter_by_date_bounds(
            self.repo.pulls, self.start_date, self.end_date)
        pulls = self.filter_old(pulls, self.end_date, self.days)

        self.results = [[len(pulls)]]

        return self


class OpenedClosedIssues(DateLimitedReport):
    """
    Number of opened and closed issues
    """
    name = "Opened and closed issues"
    headers = ('Opened', 'Closed')

    def analyze(self):
        issues = self.filter_by_date_bounds(self.repo.issues, self.start_date, self.end_date)
        opened = len(self.filter_by_state(issues, 'opened'))
        closed = len(self.filter_by_state(issues, 'closed'))

        self.results = [(opened, closed)]

        return self
