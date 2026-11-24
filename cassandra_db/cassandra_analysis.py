
# Author: Anosha Naseri
# Course: SDC435L
# Week 3: Cassandra Data Analysis
# Purpose: Analyze GitHub repository data using Cassandra.

from cassandra_db.cassandra_connection import get_cassandra_connection
from statistics import mean

def top_repositories(session):
    """Display the top 10 repositories by watch count."""

    rows = session.execute(
        "SELECT repo_name, watch_count FROM repositories"
    )

    repositories = [
        row for row in rows if row.watch_count is not None
    ]

    ranked = sorted(
        repositories,
        key=lambda row: row.watch_count,
        reverse=True
    )[:10]

    print("\n===== Top 10 Repositories by Watch Count =====")

    for index, repo in enumerate(ranked, start=1):
        print(f"{index}. {repo.repo_name}: {repo.watch_count:,} watchers")

    print(f"\nTotal repositories analyzed: {len(repositories)}")

def repository_name_analysis(session):
    """Analyze repository name lengths."""

    rows = session.execute(
        "SELECT repo_name FROM repositories"
    )

    names = [row.repo_name for row in rows if row.repo_name]

    if not names:
        print("No repositories found.")
        return

    longest = max(names, key=len)
    shortest = min(names, key=len)
    average = mean(len(name) for name in names)

    print("\n===== Repository Name Analysis =====")
    print(f"Longest name: {longest}")
    print(f"Length: {len(longest)} characters")

    print(f"\nShortest name: {shortest}")
    print(f"Length: {len(shortest)} characters")

    print(f"\nAverage name length: {average:.2f} characters")
    print(f"Total repositories analyzed: {len(names)}")

def main():
    """Connect to Cassandra and test both analysis features."""

    cluster = None

    try:
        cluster, session = get_cassandra_connection()

        print("Connected to Cassandra successfully!")

        top_repositories(session)
        repository_name_analysis(session)

    except Exception as error:
        print(f"Analysis failed: {error}")

    finally:
        if cluster is not None:
            cluster.shutdown()

if __name__ == "__main__":
    main()
