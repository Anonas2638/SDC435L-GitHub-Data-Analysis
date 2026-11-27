"""Import GitHub Archive repository data into Cassandra."""

from pathlib import Path

import orjson

from cassandra_db.cassandra_connection import get_cassandra_connection
from input_validation import validate_repository_name, parse_watch_count
from cassandra_db.cassandra_crud import validate_cassandra_watch_count


DATA_FILE = Path(__file__).resolve().parent.parent / "Sample_Repos.json"
MAX_RECORDS = 1000


def load_repositories():
    """Read and validate repository records from the JSON dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    repositories = []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                # Read JSON Lines incrementally instead of decoding the full file.
                record = orjson.loads(line)
                repo_name = validate_repository_name(record.get("repo_name"))
                watch_count = validate_cassandra_watch_count(
                    parse_watch_count(record.get("watch_count"))
                )
                repositories.append((repo_name, watch_count))

                if len(repositories) >= MAX_RECORDS:
                    break

            except (ValueError, TypeError, AttributeError):
                print(f"Skipping invalid record on line {line_number}")

    return repositories


def import_repositories():
    """Import repository records without overwriting existing rows."""
    cluster = None

    try:
        repositories = load_repositories()

        cluster, session = get_cassandra_connection()

        statement = session.prepare(
            """
            INSERT INTO repositories (repo_name, watch_count)
            VALUES (?, ?)
            IF NOT EXISTS
            """
        )

        imported = 0
        existing = 0

        for repo_name, watch_count in repositories:
            result = session.execute(statement, (repo_name, watch_count))
            row = result.one()

            if row and row.applied:
                imported += 1
            else:
                existing += 1

        print("\nCassandra Import Summary")
        print("------------------------")
        print(f"Valid records processed: {len(repositories)}")
        print(f"New repositories: {imported}")
        print(f"Already existing: {existing}")

    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Import error: {error}")

    except Exception as error:
        print(f"Cassandra operation failed: {error}")

    finally:
        if cluster is not None:
            cluster.shutdown()


if __name__ == "__main__":
    import_repositories()
