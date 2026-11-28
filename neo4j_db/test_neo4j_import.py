
"""Unit tests for Neo4j dataset validation and batch importing."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from neo4j_db.neo4j_import import (
    load_repositories,
    import_batch,
    MAX_WATCH_COUNT,
)


class TestNeo4jImport(unittest.TestCase):
    """Verify importer validation and database write behavior."""

    def setUp(self):
        """Create an isolated temporary dataset for each test."""
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.data_file = (
            Path(self.temp_dir.name) / "test_repositories.json"
        )

        patcher = patch(
            "neo4j_db.neo4j_import.DATA_FILE",
            self.data_file,
        )

        patcher.start()
        self.addCleanup(patcher.stop)

    def write_records(self, records):
        """Write test records in JSON Lines format."""
        with self.data_file.open("w", encoding="utf-8") as file:
            for record in records:
                file.write(json.dumps(record) + "\n")

    def test_valid_repository(self):
        """Verify valid records are loaded and owners extracted."""
        self.write_records([
            {"repo_name": "google/test", "watch_count": 100}
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(invalid, 0)
        self.assertEqual(repositories, [
            {
                "owner_name": "google",
                "repo_name": "google/test",
                "watch_count": 100,
            }
        ])

    def test_numeric_string_watch_count(self):
        """Verify numeric strings are converted to integers."""
        self.write_records([
            {"repo_name": "owner/repo", "watch_count": "250"}
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(invalid, 0)
        self.assertEqual(repositories[0]["watch_count"], 250)
        self.assertIsInstance(
            repositories[0]["watch_count"], int
        )

    def test_invalid_repository_names(self):
        """Reject malformed and unsafe repository names."""
        self.write_records([
            {"repo_name": "invalidrepo", "watch_count": 100},
            {"repo_name": "owner/$ne", "watch_count": 100},
            {"repo_name": "", "watch_count": 100},
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 3)

    def test_negative_watch_count(self):
        """Reject negative watch counts."""
        self.write_records([
            {"repo_name": "owner/repo", "watch_count": -100}
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 1)

    def test_decimal_watch_count(self):
        """Reject decimal watch counts."""
        self.write_records([
            {"repo_name": "owner/repo", "watch_count": 10.5},
            {"repo_name": "owner/repo", "watch_count": "10.5"},
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 2)

    def test_boolean_watch_count(self):
        """Reject boolean values instead of converting them."""
        self.write_records([
            {"repo_name": "owner/repo", "watch_count": True},
            {"repo_name": "owner/repo", "watch_count": False},
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 2)

    def test_missing_required_properties(self):
        """Reject records missing required properties."""
        self.write_records([
            {"repo_name": "owner/repo"},
            {"watch_count": 100},
            {},
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 3)

    def test_malformed_json(self):
        """Skip malformed JSON and continue processing."""
        self.data_file.write_text(
            'invalid json\n'
            '{"repo_name":"owner/repo","watch_count":100}\n',
            encoding="utf-8",
        )

        repositories, invalid = load_repositories()

        self.assertEqual(len(repositories), 1)
        self.assertEqual(invalid, 1)

    def test_non_object_json(self):
        """Reject JSON values that are not repository objects."""
        self.write_records([None, [], 100, "repository"])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 4)

    def test_integer_overflow(self):
        """Reject watch counts exceeding Neo4j's integer limit."""
        self.write_records([
            {
                "repo_name": "owner/repo",
                "watch_count": str(MAX_WATCH_COUNT + 1),
            }
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 1)

    def test_maximum_integer(self):
        """Accept the maximum supported Neo4j integer."""
        self.write_records([
            {
                "repo_name": "owner/repo",
                "watch_count": str(MAX_WATCH_COUNT),
            }
        ])

        repositories, invalid = load_repositories()

        self.assertEqual(invalid, 0)
        self.assertEqual(
            repositories[0]["watch_count"],
            MAX_WATCH_COUNT,
        )

    def test_blank_lines(self):
        """Skip blank lines without counting them as invalid."""
        self.data_file.write_text(
            '\n'
            '   \n'
            '{"repo_name":"owner/repo","watch_count":100}\n'
            '\n',
            encoding="utf-8",
        )

        repositories, invalid = load_repositories()

        self.assertEqual(len(repositories), 1)
        self.assertEqual(invalid, 0)

    def test_import_record_limit(self):
        """Stop processing after the valid record limit."""
        self.write_records([
            {"repo_name": "invalid", "watch_count": 100},
            {"repo_name": "owner/repo1", "watch_count": 100},
            {"repo_name": "owner/repo2", "watch_count": 200},
            {"repo_name": "owner/repo3", "watch_count": 300},
        ])

        with patch("neo4j_db.neo4j_import.MAX_RECORDS", 2):
            repositories, invalid = load_repositories()

        self.assertEqual(len(repositories), 2)
        self.assertEqual(invalid, 1)

    def test_empty_dataset(self):
        """Handle an empty dataset without errors."""
        self.write_records([])

        repositories, invalid = load_repositories()

        self.assertEqual(repositories, [])
        self.assertEqual(invalid, 0)

    def test_parameterized_batch_import(self):
        """Verify parameterized writes and non-overwrite logic."""
        transaction = Mock()

        repositories = [
            {
                "owner_name": "owner",
                "repo_name": "owner/repo",
                "watch_count": 100,
            }
        ]

        expected_counters = Mock(
            nodes_created=2,
            relationships_created=1,
        )

        transaction.run.return_value.consume.return_value.counters = (
            expected_counters
        )

        counters = import_batch(transaction, repositories)

        args, kwargs = transaction.run.call_args
        query = args[0]

        self.assertIn("UNWIND $repositories", query)
        self.assertIn("MERGE (o:Owner", query)
        self.assertIn("MERGE (r:Repository", query)
        self.assertIn("ON CREATE SET", query)
        self.assertIn("MERGE (o)-[:OWNS]->(r)", query)

        self.assertEqual(kwargs["repositories"], repositories)
        self.assertEqual(counters.nodes_created, 2)
        self.assertEqual(counters.relationships_created, 1)

        transaction.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
