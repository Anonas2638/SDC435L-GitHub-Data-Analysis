"""Tests for validation shared by the database CRUD features."""

import unittest
from unittest.mock import Mock, patch

from cassandra_db.cassandra_crud import read_repository as read_cassandra_repository
from input_validation import (
    validate_repository_name,
    validate_watch_count,
    parse_watch_count,
)
from cassandra_db.cassandra_crud import validate_cassandra_watch_count
from mongodb_db.mongo_crud import read_repository as read_mongo_repository
from mongodb_db.mongo_crud import validate_mongo_watch_count
from redis_db.redis_crud import create_repository as create_redis_repository
from redis_db.redis_crud import read_repository as read_redis_repository
from io import StringIO
from redis_db.import_repositories import import_repositories


class TestInputValidation(unittest.TestCase):
    def test_repository_name_is_trimmed(self):
        self.assertEqual(
            validate_repository_name("  owner/repository  "),
            "owner/repository",
        )
        self.assertEqual(
            validate_repository_name("owner/_repository"),
            "owner/_repository",
        )

    def test_repository_name_rejects_unsafe_or_malformed_values(self):
        invalid_names = (
            "",
            "   ",
            "owner",
            "owner/",
            "/repository",
            "owner/repo/extra",
            "owner/$ne",
            "owner/repo name",
            None,
            123,
            True,
            "a" * 101 + "/repository",
            "owner/" + "a" * 101,
        )

        for repo_name in invalid_names:
            with self.subTest(repo_name=repo_name):
                with self.assertRaises(ValueError):
                    validate_repository_name(repo_name)

    def test_watch_count_rejects_invalid_values(self):
        for watch_count in (-1, True, False,"10", 10.5, None):
            with self.subTest(watch_count=watch_count):
                with self.assertRaises(ValueError):
                    validate_watch_count(watch_count)

    def test_watch_count_accepts_zero_and_positive_integers(self):
        self.assertEqual(validate_watch_count(0), 0)
        self.assertEqual(validate_watch_count(42), 42)

    def test_crud_functions_reject_unsafe_names_before_database_access(self):
        """Verify invalid repository names never reach the database."""

        mongo_collection = Mock()
        cassandra_session = Mock()

        with self.assertRaises(ValueError):
            read_mongo_repository(mongo_collection, "owner/$ne")

        with self.assertRaises(ValueError):
            read_cassandra_repository(cassandra_session, "owner")

        with patch("redis_db.redis_crud.connection") as redis_connection:
            with self.assertRaises(ValueError):
                create_redis_repository("owner/$ne", 10)

            redis_connection.set.assert_not_called()
            redis_connection.get.assert_not_called()

        mongo_collection.find_one.assert_not_called()
        cassandra_session.prepare.assert_not_called()
        cassandra_session.execute.assert_not_called()

    def test_redis_reader_decodes_existing_json_records(self):
        stored_record = '{"repo_name":"owner/repository","watch_count":"10"}'

        with patch(
            "redis_db.redis_crud.connection.get",
            return_value=stored_record,
        ):
            repository = read_redis_repository("owner/repository")

        self.assertEqual(repository["repo_name"], "owner/repository")
        self.assertEqual(repository["watch_count"], "10")

    def test_parse_watch_count_accepts_valid_values(self):
        valid_values = (
            ("100", 100),
            (" 100 ", 100),
            ("0", 0),
            (100, 100),
            (0, 0),
        )

        for value, expected in valid_values:
            with self.subTest(value=value):
                self.assertEqual(parse_watch_count(value), expected)

    def test_parse_watch_count_rejects_invalid_values(self):
        invalid_values = (
            True,
            False,
            10.9,
            -0.5,
            -1,
            "-100",
            "10.5",
            "abc",
            "",
            None,
        )

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_watch_count(value)

    def test_cassandra_watch_count_accepts_boundaries(self):
        self.assertEqual(validate_cassandra_watch_count(0), 0)
        self.assertEqual(
            validate_cassandra_watch_count(2147483647),
            2147483647,
        )

    def test_cassandra_watch_count_rejects_out_of_range_values(self):
        for value in (-1, 2147483648):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_cassandra_watch_count(value)

    def test_mongo_watch_count_accepts_boundaries(self):
        self.assertEqual(validate_mongo_watch_count(0), 0)
        self.assertEqual(
            validate_mongo_watch_count(9223372036854775807),
            9223372036854775807,
        )

    def test_mongo_watch_count_rejects_out_of_range_values(self):
        for value in (-1, 9223372036854775808):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_mongo_watch_count(value)


    def test_redis_import_preserves_existing_repository(self):
        """Verify the importer does not overwrite existing records."""

        sample_data = (
            '{"repo_name": "owner/repository", "watch_count": "100"}\n'
        )

        with patch(
            "redis_db.import_repositories.redis.Redis"
        ) as mock_redis, patch(
            "redis_db.import_repositories.Path.exists",
            return_value=True
        ), patch(
            "redis_db.import_repositories.open",
            return_value=StringIO(sample_data),
            create=True
        ), patch("builtins.print") as mock_print:

            connection = mock_redis.return_value

            # Simulate Redis rejecting an insert for an existing key.
            connection.set.return_value = None

            import_repositories()

            connection.set.assert_called_once_with(
                "github:repo:owner/repository",
                '{"repo_name": "owner/repository", "watch_count": "100"}',
                nx=True
            )

            mock_print.assert_any_call(
                "New repositories imported: 0"
            )

            mock_print.assert_any_call(
                "Existing repositories: 1"
            )

if __name__ == "__main__":
    unittest.main()
