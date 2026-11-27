
import orjson
import redis

def show_popular_repositories(repositories):
    """Display the top 10 repositories by watch count."""

    ranked = sorted(
        repositories,
        key=lambda repo: int(repo.get("watch_count", 0)),
        reverse=True
    )

    print("\nTop 10 Most Popular GitHub Repositories")
    print("-" * 60)

    for rank, repo in enumerate(ranked[:10], start=1):
        name = repo.get("repo_name", "Unknown")
        watches = int(repo.get("watch_count", 0))
        print(f"{rank}. {name} - {watches:,} watches")

def get_repositories_from_redis():
    """Retrieve repository records stored in Redis."""

    connection = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    connection.ping()
    print("Connected to Redis successfully!")

    repositories = []

    for key in connection.scan_iter(match="github:repo:*"):
        data = connection.get(key)
        if data:
            repositories.append(orjson.loads(data))

    return repositories

if __name__ == "__main__":
    repositories = get_repositories_from_redis()

    print(f"Loaded {len(repositories):,} repositories from Redis.")

    if repositories:
        show_popular_repositories(repositories)
    else:
        print("No repository records found in Redis yet.")
