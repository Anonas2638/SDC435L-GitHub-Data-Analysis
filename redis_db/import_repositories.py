import json
from pathlib import Path
import redis

def import_repositories():
    """Import GitHub repository data into Redis."""

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

    with open(file_path, "r", encoding="utf-8-sig") as file:
        for line in file:
            if not line.strip():
                continue

            repo = json.loads(line)
            repo_name = repo.get("repo_name")

            if not repo_name:
                continue

            key = "github:repo:" + repo_name
            connection.set(key, json.dumps(repo))
            count += 1

            if count >= 1000:
                break

    print(f"\nFinished importing {count:,} records!")

if __name__ == "__main__":
    import_repositories()
