
"""Unit tests for Neo4j repository owner relationship analysis."""

import unittest
from unittest.mock import Mock, patch
from io import StringIO

from neo4j_db.owner_analysis import (
    get_ownership_overview,
    get_top_owners,
    get_owner_distribution,
    display_owner_distribution,
    display_top_owners,
)


class TestOwnerAnalysis(unittest.TestCase):
    """Verify ownership queries and output formatting."""

    def setUp(self):
        """Create a mock database session for each test."""
        self.session = Mock()

    def test_ownership_overview(self):
        """Verify ownership overview results are returned."""
        expected = {
            "total_owners": 828,
            "total_repositories": 1000,
            "total_relationships": 1000,
        }

        self.session.run.return_value.single.return_value.data.return_value = expected

        result = get_ownership_overview(self.session)

        self.assertEqual(result, expected)
        self.session.run.assert_called_once()

    def test_top_owners(self):
        """Verify ranked owner records are returned."""
        expected = [
            {
                "owner": "google",
                "repository_count": 22,
                "total_watch_count": 56092,
                "average_watch_count": 2549.64,
            },
            {
                "owner": "facebook",
                "repository_count": 19,
                "total_watch_count": 56208,
                "average_watch_count": 2958.32,
            },
        ]

        self.session.run.return_value.data.return_value = expected

        result = get_top_owners(self.session)

        self.assertEqual(result, expected)
        self.assertEqual(result[0]["owner"], "google")

    def test_parameterized_limit(self):
        """Verify the requested limit is passed to Cypher."""
        self.session.run.return_value.data.return_value = []

        get_top_owners(self.session, limit=5)

        args, kwargs = self.session.run.call_args

        self.assertIn("LIMIT $limit", args[0])
        self.assertEqual(kwargs["limit"], 5)

    def test_owner_distribution(self):
        """Verify ownership distribution results."""
        expected = {
            "total_owners": 828,
            "single_repo_owners": 745,
            "multiple_repo_owners": 83,
            "avg_repos_per_owner": 1.21,
            "max_repos_per_owner": 22,
        }

        self.session.run.return_value.single.return_value.data.return_value = expected

        result = get_owner_distribution(self.session)

        self.assertEqual(result, expected)
        self.assertEqual(
            result["single_repo_owners"]
            + result["multiple_repo_owners"],
            result["total_owners"],
        )

    def test_distribution_percentages(self):
        """Verify ownership percentages are formatted correctly."""
        distribution = {
            "total_owners": 828,
            "single_repo_owners": 745,
            "multiple_repo_owners": 83,
            "avg_repos_per_owner": 1.21,
            "max_repos_per_owner": 22,
        }

        with patch("sys.stdout", new_callable=StringIO) as output:
            display_owner_distribution(distribution)

        self.assertIn("89.98%", output.getvalue())
        self.assertIn("10.02%", output.getvalue())

    def test_empty_distribution(self):
        """Verify empty data does not cause division by zero."""
        distribution = {
            "total_owners": 0,
            "single_repo_owners": 0,
            "multiple_repo_owners": 0,
            "avg_repos_per_owner": None,
            "max_repos_per_owner": None,
        }

        with patch("sys.stdout", new_callable=StringIO) as output:
            display_owner_distribution(distribution)

        self.assertIn("0.00%", output.getvalue())
        self.assertIn(
            "Average repositories per owner: 0.00",
            output.getvalue(),
        )

    def test_top_owners_formatting(self):
        """Verify owner names and watch counts are displayed."""
        owners = [
            {
                "owner": "google",
                "repository_count": 22,
                "total_watch_count": 56092,
                "average_watch_count": 2549.64,
            }
        ]

        with patch("sys.stdout", new_callable=StringIO) as output:
            display_top_owners(owners)

        result = output.getvalue()

        self.assertIn("google", result)
        self.assertIn("56,092", result)
        self.assertIn("2,549.64", result)


if __name__ == "__main__":
    unittest.main()
