
# Name: Sherika Fayson
# Course: SDC435L
# Week 2: MongoDB Integration
# Purpose: Import GitHub Archive repository data into MongoDB.

from pathlib import Path

import orjson

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import PyMongoError

from input_validation import validate_repository_name, parse_watch_count
from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)
from mongodb_db.mongo_crud import validate_mongo_watch_count

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
                # Decode each JSON Lines record independently to keep memory use low.
                record = orjson.loads(line)

                repo_name = validate_repository_name(record.get("repo_name"))
                watch_count = validate_mongo_watch_count(parse_watch_count(record.get("watch_count")))

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

            except (
                orjson.JSONDecodeError,
                KeyError,
                ValueError,
                TypeError,
                AttributeError,
            ):
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
