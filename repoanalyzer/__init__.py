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

    def __init__(self, repo):
        self.repo = repo
        self.results = []

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}" for {self.repo}>'

    def analyze(self, *args, **kwargs):
        """
        Analyze repository

        Args:
            *args, **kwargs: analysis options

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
        pulls = [p.state for p in self.repo.pulls
                 if (p.created_at >= self.start_date
                     and (p.closed_at is None
                          or p.closed_at < self.end_date))]
        opened = sum(1 for state in pulls if state == 'open')
        closed = sum(1 for state in pulls if state == 'closed')

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
        pulls = [1 for p in self.repo.pulls
                 if (p.created_at >= self.start_date
                     and (p.closed_at is None
                          or p.closed_at < self.end_date)

                     and ((p.closed_at or self.end_date)
                          - p.created_at).days > self.days)]

        self.results = [[len(pulls)]]

        return self
