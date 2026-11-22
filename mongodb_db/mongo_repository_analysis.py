
# Name: Anosha Naseri
# Date: 11/19/2026
# Course: SDC435L - Week 2 Group Project
# Feature: Top 10 Repositories by Watch Count
# Refactored by: Sherika Fayson
# Purpose: Integrate analysis into the modular MongoDB application.

from pymongo.errors import PyMongoError

from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)


def show_popular_repositories(collection):
    """Display the top 10 repositories ranked by watch count."""

    print("\nTOP 10 REPOSITORIES BY WATCH COUNT")
    print("-" * 55)

    # Retrieve the 10 most-watched repositories.
    top_repositories = collection.find(
        {},
        {"_id": 0, "repo_name": 1, "watch_count": 1}
    ).sort("watch_count", -1).limit(10)

    found = False

    for rank, repo in enumerate(top_repositories, start=1):
        found = True
        print(
            f"{rank}. {repo['repo_name']} - "
            f"{repo['watch_count']:,} watchers"
        )

    if not found:
        print("No repository documents found.")
        print("Please import the dataset first.")
    else:
        print("\nAnalysis completed successfully!")


def main():
    """Run the repository popularity analysis independently."""

    try:
        with get_connection() as client:
            collection = get_collection(client)
            show_popular_repositories(collection)

    except PyMongoError as error:
        print(f"MongoDB error: {error}")


if __name__ == "__main__":
    main()
