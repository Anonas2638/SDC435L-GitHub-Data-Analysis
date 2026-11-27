"""Unit tests for Cassandra watch count distribution analysis."""

import unittest
from unittest.mock import Mock
from types import SimpleNamespace
from io import StringIO
from contextlib import redirect_stdout

from cassandra_db.cassandra_analysis import (
    watch_count_distribution_analysis,
)


class TestWatchCountDistribution(unittest.TestCase):

    def run_analysis(self, counts):
        """Simulate Cassandra records and capture analysis output."""

        session = Mock()

        session.execute.return_value = [
            SimpleNamespace(watch_count=count)
            for count in counts
        ]

        output = StringIO()

        with redirect_stdout(output):
            watch_count_distribution_analysis(session)

        return output.getvalue()

    def test_distribution_boundaries(self):
        """Verify that boundary values enter the correct buckets."""

        counts = [
            0, 1, 100, 101, 1000,
            1001, 10000, 10001
        ]

        output = self.run_analysis(counts)

        self.assertIn("0 watchers: 1 (12.5%)", output)
        self.assertIn("1-100 watchers: 2 (25.0%)", output)
        self.assertIn("101-1000 watchers: 2 (25.0%)", output)
        self.assertIn("1001-10000 watchers: 2 (25.0%)", output)
        self.assertIn("10001+ watchers: 1 (12.5%)", output)
        self.assertIn("Total repositories analyzed: 8", output)

    def test_empty_dataset(self):
        """Verify that an empty dataset is handled safely."""

        output = self.run_analysis([])

        self.assertIn("No watch count data found.", output)

    def test_null_watch_counts(self):
        """Verify that missing watch counts are excluded."""

        output = self.run_analysis([None, 100, 1000])

        self.assertIn("Total repositories analyzed: 2", output)

    def test_all_null_watch_counts(self):
        """Verify that a dataset containing only nulls is handled."""

        output = self.run_analysis([None, None])

        self.assertIn("No watch count data found.", output)


if __name__ == "__main__":
    unittest.main()
