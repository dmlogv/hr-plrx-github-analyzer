"""
Repository analyzer
"""

__all__ = []
__version__ = '0.0.1'


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

