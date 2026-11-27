
from collections import Counter

import orjson
import redis

# Connect to the Redis database.
connection = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def owner_analysis(limit=10):
    """Display owners with the most repositories."""

    owner_counts = Counter()

    # Scan repository keys without blocking Redis with KEYS.
    for key in connection.scan_iter(match="github:repo:*"):
        data = connection.get(key)

        if data is None:
            continue

        repository = orjson.loads(data)
        repo_name = repository.get("repo_name", "")

        # Extract the owner from the repository name.
        if "/" in repo_name:
            owner = repo_name.split("/", 1)[0]
            owner_counts[owner] += 1

    if not owner_counts:
        print("No repository data found.")
        return

    print(f"\n--- Top {limit} Repository Owners ---")
    print(f"{'Rank':<6}{'Owner':<30}{'Repositories':>12}")
    print("-" * 48)

    for rank, (owner, count) in enumerate(
        owner_counts.most_common(limit), start=1
    ):
        print(f"{rank:<6}{owner:<30}{count:>12}")


if __name__ == "__main__":
    try:
        connection.ping()
        owner_analysis()
    except redis.RedisError as error:
        print(f"Connection failed: {error}")
