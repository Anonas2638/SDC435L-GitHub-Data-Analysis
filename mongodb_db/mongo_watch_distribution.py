
# Name: Sherika Fayson
# Course: SDC435L - Week 2 Group Project
# Feature: Repository Watch Count Distribution

from pymongo.errors import PyMongoError

from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)


def show_watch_distribution(collection):
    """Group repositories by their watch count ranges."""

    pipeline = [
        {
            "$bucket": {
                "groupBy": "$watch_count",
                "boundaries": [0, 1000, 2500, 5000, 10000],
                "default": "10000+",
                "output": {
                    "count": {"$sum": 1}
                }
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    if not results:
        print("No repository documents found.")
        return

    # Define readable labels for each watch count range.
    ranges = {
        0: "0 - 999",
        1000: "1,000 - 2,499",
        2500: "2,500 - 4,999",
        5000: "5,000 - 9,999",
        "10000+": "10,000+"
    }

    distribution = {
        result["_id"]: result["count"]
        for result in results
    }

    total = sum(distribution.values())

    print("\nREPOSITORY WATCH COUNT DISTRIBUTION")
    print("-" * 65)
    print(f"Total repositories analyzed: {total:,}\n")

    print(f"{'Watch Count Range':<20}{'Repositories':>15}{'Percentage':>15}")
    print("-" * 65)

    for bucket, label in ranges.items():
        count = distribution.get(bucket, 0)
        percentage = (count / total) * 100

        print(
            f"{label:<20}"
            f"{count:>15,}"
            f"{percentage:>14.2f}%"
        )

    # Display a simple text-based distribution chart.
    print("\nWATCH COUNT DISTRIBUTION CHART")
    print("-" * 65)

    for bucket, label in ranges.items():
        count = distribution.get(bucket, 0)
        percentage = (count / total) * 100
        bar = "#" * max(1, round(percentage / 2)) if count > 0 else ""

        print(f"{label:<18} | {bar} ({count:,})")

    print("\nAnalysis completed successfully!")


def main():
    """Run watch count distribution analysis independently."""

    try:
        with get_connection() as client:
            collection = get_collection(client)
            show_watch_distribution(collection)

    except PyMongoError as error:
        print(f"MongoDB error: {error}")


if __name__ == "__main__":
    main()
