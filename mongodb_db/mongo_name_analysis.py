
# Name: Sherika Fayson
# Course: SDC435L - Week 2 Group Project
# Feature: Longest and Shortest Repository Names

from pymongo.errors import PyMongoError

from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)


def show_repository_names(collection):
    """Analyze repositories based on name length."""

    pipeline = [
        {
            "$project": {
                "_id": 0,
                "repo_name": 1,
                "name_length": {
                    "$strLenCP": "$repo_name"
                }
            }
        },
        {
            "$facet": {
                "longest": [
                    {"$sort": {"name_length": -1, "repo_name": 1}},
                    {"$limit": 5}
                ],
                "shortest": [
                    {"$sort": {"name_length": 1, "repo_name": 1}},
                    {"$limit": 5}
                ]
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    if not results or not results[0]["longest"]:
        print("No repository documents found.")
        return

    print("\nTOP 5 LONGEST REPOSITORY NAMES")
    print("-" * 60)

    for rank, repo in enumerate(results[0]["longest"], start=1):
        print(
            f"{rank}. {repo['repo_name']} "
            f"({repo['name_length']} characters)"
        )

    print("\nTOP 5 SHORTEST REPOSITORY NAMES")
    print("-" * 60)

    for rank, repo in enumerate(results[0]["shortest"], start=1):
        print(
            f"{rank}. {repo['repo_name']} "
            f"({repo['name_length']} characters)"
        )

    print("\nAnalysis completed successfully!")


def main():
    """Run repository name analysis independently."""

    try:
        with get_connection() as client:
            collection = get_collection(client)
            show_repository_names(collection)

    except PyMongoError as error:
        print(f"MongoDB error: {error}")


if __name__ == "__main__":
    main()
