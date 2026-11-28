
"""Import GitHub repository data into the Neo4j graph database."""

import os
from pathlib import Path

import orjson

from input_validation import (
    validate_repository_name,
    parse_watch_count,
)
from neo4j_db.neo4j_connection import get_neo4j_driver
from neo4j_db.neo4j_schema import create_constraints


DATA_FILE = Path(__file__).resolve().parent.parent / "Sample_Repos.json"
MAX_RECORDS = 1000
BATCH_SIZE = 100
MAX_WATCH_COUNT = 9223372036854775807


def load_repositories():
    """Read and validate repository records from the JSON Lines dataset."""
    repositories = []
    invalid_records = 0

    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        for line in file:
            if len(repositories) >= MAX_RECORDS:
                break

            if not line.strip():
                continue

            try:
                record = orjson.loads(line)

                repo_name = validate_repository_name(
                    record.get("repo_name")
                )

                watch_count = parse_watch_count(
                    record.get("watch_count")
                )

                # Neo4j stores integers as signed 64-bit values.
                if watch_count > MAX_WATCH_COUNT:
                    raise ValueError("Watch count exceeds Neo4j integer limit.")

                # Extract the owner from the full repository name.
                owner_name = repo_name.split("/", 1)[0]

                repositories.append({
                    "owner_name": owner_name,
                    "repo_name": repo_name,
                    "watch_count": watch_count,
                })

            except (ValueError, TypeError, AttributeError):
                invalid_records += 1

    return repositories, invalid_records


def import_batch(transaction, repositories):
    """Import a batch without overwriting existing repository values."""
    query = """
    UNWIND $repositories AS item

    MERGE (o:Owner {name: item.owner_name})

    MERGE (r:Repository {repo_name: item.repo_name})
    ON CREATE SET r.watch_count = item.watch_count

    MERGE (o)-[:OWNS]->(r)
    """

    result = transaction.run(
        query,
        repositories=repositories
    )

    return result.consume().counters


def import_repositories():
    """Initialize the schema and import validated repository records."""
    repositories, invalid_records = load_repositories()

    create_constraints()

    database = os.getenv("NEO4J_DATABASE", "neo4j")

    nodes_created = 0
    relationships_created = 0

    with get_neo4j_driver() as driver:
        with driver.session(database=database) as session:

            # Batch writes reduce the number of database transactions.
            for start in range(0, len(repositories), BATCH_SIZE):
                batch = repositories[start:start + BATCH_SIZE]

                counters = session.execute_write(
                    import_batch,
                    batch
                )

                nodes_created += counters.nodes_created
                relationships_created += counters.relationships_created

    print("\nNeo4j import completed successfully.")
    print(f"Valid records processed: {len(repositories)}")
    print(f"Invalid records skipped: {invalid_records}")
    print(f"New nodes created: {nodes_created}")
    print(f"New relationships created: {relationships_created}")


if __name__ == "__main__":
    import_repositories()
