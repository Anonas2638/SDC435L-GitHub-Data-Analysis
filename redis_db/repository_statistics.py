
from statistics import mean, median
from redis_db.repository_popularity import get_repositories_from_redis


def repository_statistics():
    """Display statistical analysis of repository watch counts."""

    # Retrieve existing repository records from Redis.
    repositories = get_repositories_from_redis()

    if not repositories:
        print("No repository records found.")
        return

    watch_counts = []

    # Convert watch counts to integers and skip invalid values.
    for repository in repositories:
        try:
            count = int(repository["watch_count"])

            if count >= 0:
                watch_counts.append(count)

        except (KeyError, ValueError, TypeError):
            continue

    if not watch_counts:
        print("No valid watch counts found.")
        return

    # Calculate and display descriptive statistics.
    print("\nRepository Watch Count Statistics")
    print("-" * 50)

    print(f"Total repositories: {len(repositories):,}")
    print(f"Repositories analyzed: {len(watch_counts):,}")
    print(f"Total watches: {sum(watch_counts):,}")
    print(f"Average watches: {mean(watch_counts):,.2f}")
    print(f"Median watches: {median(watch_counts):,.2f}")
    print(f"Minimum watches: {min(watch_counts):,}")
    print(f"Maximum watches: {max(watch_counts):,}")


if __name__ == "__main__":
    repository_statistics()
