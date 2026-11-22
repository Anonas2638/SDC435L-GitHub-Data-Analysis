
# Name: Sherika Fayson
# Course: SDC435L
# Week 2: MongoDB Integration
# Purpose: Import GitHub Archive repository data into MongoDB.

import json
from pathlib import Path
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import PyMongoError

from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)

DATASET_PATH = (
    Path(__file__).resolve().parent.parent / "Sample_Repos.json"
)

IMPORT_LIMIT = 1000


def import_repositories(collection, limit=IMPORT_LIMIT):
    """Import repository documents without overwriting existing records."""

    if not DATASET_PATH.is_file():
        print(f"Dataset not found: {DATASET_PATH}")
        return

    # Create indexes to prevent duplicates and improve queries.
    collection.create_index("repo_name", unique=True)
    collection.create_index([("watch_count", DESCENDING)])

    imported = 0
    existing = 0
    skipped = 0
    processed = 0

    with open(DATASET_PATH, "r", encoding="utf-8-sig") as file:

        for line in file:
            if processed >= limit:
                break

            line = line.strip()

            if not line:
                continue

            processed += 1

            try:
                record = json.loads(line)

                repo_name = record["repo_name"].strip()
                watch_count = int(record["watch_count"])

                if not repo_name or watch_count < 0:
                    skipped += 1
                    continue

                record["repo_name"] = repo_name
                record["watch_count"] = watch_count

                # Insert only if the repository does not already exist.
                result = collection.update_one(
                    {"repo_name": repo_name},
                    {"$setOnInsert": record},
                    upsert=True
                )

                if result.upserted_id is not None:
                    imported += 1
                else:
                    existing += 1

            except (json.JSONDecodeError, KeyError, ValueError,
                    TypeError, AttributeError):
                skipped += 1

    print("\nMONGODB IMPORT RESULTS")
    print("-" * 40)
    print(f"Records processed: {processed:,}")
    print(f"New documents imported: {imported:,}")
    print(f"Existing documents: {existing:,}")
    print(f"Invalid records skipped: {skipped:,}")
    print(f"Total documents: {collection.count_documents({}):,}")


def main():
    """Run the importer independently."""

    try:
        with get_connection() as client:
            collection = get_collection(client)
            import_repositories(collection)

    except (PyMongoError, OSError) as error:
        print(f"Import failed: {error}")


if __name__ == "__main__":
    main()
