import json
from pathlib import Path

import orjson
import redis

from input_validation import validate_repository_name, parse_watch_count


def import_repositories():
    """Import GitHub repository data without overwriting existing records."""

    connection = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    connection.ping()
    print("Connected to Redis successfully!")

    file_path = Path(__file__).resolve().parent.parent / "Sample_Repos.json"

    if not file_path.exists():
        print("Error: Sample_Repos.json was not found.")
        return

    count = 0
    imported = 0
    existing = 0
    skipped = 0

    with open(file_path, "r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                # Decode one JSON Lines record at a time.
                repo = orjson.loads(line)

                # Validate repository data before database access.
                repo_name = validate_repository_name(
                    repo.get("repo_name")
                )

                parse_watch_count(repo.get("watch_count"))

            except (
                orjson.JSONDecodeError,
                TypeError,
                ValueError,
                AttributeError,
            ) as error:
                skipped += 1
                print(
                    f"Skipping invalid record on line "
                    f"{line_number}: {error}"
                )
                continue

            repo["repo_name"] = repo_name

            key = "github:repo:" + repo_name

            # Insert only if the repository does not already exist.
            if connection.set(key, json.dumps(repo), nx=True):
                imported += 1
            else:
                existing += 1

            count += 1

            # Limit the import to 1,000 valid records.
            if count >= 1000:
                break

    print("\nREDIS IMPORT RESULTS")
    print("-" * 40)
    print(f"Valid records processed: {count:,}")
    print(f"New repositories imported: {imported:,}")
    print(f"Existing repositories: {existing:,}")
    print(f"Invalid records skipped: {skipped:,}")


if __name__ == "__main__":
    import_repositories()
