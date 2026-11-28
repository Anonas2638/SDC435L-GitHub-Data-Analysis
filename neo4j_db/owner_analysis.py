
"""Analyze repository ownership relationships in Neo4j."""

import os

from neo4j.exceptions import Neo4jError, DriverError
from neo4j_db.neo4j_connection import get_neo4j_driver


def get_ownership_overview(session):
    """Return counts of connected owners, repositories, and relationships."""
    query = """
    MATCH (o:Owner)-[rel:OWNS]->(r:Repository)
    RETURN count(DISTINCT o) AS total_owners,
           count(DISTINCT r) AS total_repositories,
           count(rel) AS total_relationships
    """

    return session.run(query).single().data()


def get_top_owners(session, limit=10):
    """Rank repository owners and calculate engagement statistics."""
    query = """
    MATCH (o:Owner)-[:OWNS]->(r:Repository)
    RETURN o.name AS owner,
           count(r) AS repository_count,
           sum(r.watch_count) AS total_watch_count,
           round(avg(r.watch_count), 2) AS average_watch_count
    ORDER BY repository_count DESC, owner ASC
    LIMIT $limit
    """

    return session.run(query, limit=limit).data()


def get_owner_distribution(session):
    """Calculate single and multiple repository ownership statistics."""
    query = """
    MATCH (o:Owner)-[:OWNS]->(r:Repository)
    WITH o, count(DISTINCT r) AS repository_count
    RETURN
        count(o) AS total_owners,
        sum(CASE WHEN repository_count = 1
            THEN 1 ELSE 0 END) AS single_repo_owners,
        sum(CASE WHEN repository_count > 1
            THEN 1 ELSE 0 END) AS multiple_repo_owners,
        round(avg(repository_count), 2) AS avg_repos_per_owner,
        max(repository_count) AS max_repos_per_owner
    """

    return session.run(query).single().data()


def display_ownership_overview(overview):
    """Display general ownership statistics."""
    print("\nOWNERSHIP OVERVIEW")
    print("-" * 65)

    print(f"Total owners: {overview['total_owners']:,}")
    print(f"Total repositories: {overview['total_repositories']:,}")
    print(f"Total relationships: {overview['total_relationships']:,}")


def display_top_owners(owners):
    """Display ranked owners in a formatted table."""
    print("\nTOP 10 REPOSITORY OWNERS")
    print("-" * 80)

    print(
        f"{'Rank':<6}"
        f"{'Owner':<24}"
        f"{'Repos':>8}"
        f"{'Total Watches':>18}"
        f"{'Avg. Watches':>18}"
    )

    print("-" * 80)

    for rank, owner in enumerate(owners, start=1):
        print(
            f"{rank:<6}"
            f"{owner['owner']:<24}"
            f"{owner['repository_count']:>8,}"
            f"{owner['total_watch_count']:>18,}"
            f"{owner['average_watch_count']:>18,.2f}"
        )


def display_owner_distribution(distribution):
    """Display ownership distribution and percentages."""
    total = distribution["total_owners"]
    single = distribution["single_repo_owners"]
    multiple = distribution["multiple_repo_owners"]

    # Prevent division by zero when the graph is empty.
    single_pct = single / total * 100 if total else 0
    multiple_pct = multiple / total * 100 if total else 0

    average = distribution["avg_repos_per_owner"] or 0
    maximum = distribution["max_repos_per_owner"] or 0

    print("\nOWNER DISTRIBUTION")
    print("-" * 65)

    print(f"Total owners: {total:,}")
    print(f"Single repository owners: {single:,} ({single_pct:.2f}%)")
    print(f"Multiple repository owners: {multiple:,} ({multiple_pct:.2f}%)")
    print(f"Average repositories per owner: {average:.2f}")
    print(f"Maximum repositories per owner: {maximum:,}")


def analyze_repository_owners():
    """Execute and display the repository owner relationship analysis."""
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    try:
        with get_neo4j_driver() as driver:
            with driver.session(database=database) as session:
                overview = get_ownership_overview(session)
                owners = get_top_owners(session)
                distribution = get_owner_distribution(session)

        print("\n" + "=" * 80)
        print("REPOSITORY OWNER RELATIONSHIP ANALYSIS")
        print("=" * 80)

        if overview["total_repositories"] == 0:
            print("No connected repository records found.")
            return

        display_ownership_overview(overview)
        display_top_owners(owners)
        display_owner_distribution(distribution)

        print("\n" + "=" * 80)

    except (Neo4jError, DriverError, ValueError) as error:
        print(f"Neo4j analysis failed: {error}")


if __name__ == "__main__":
    analyze_repository_owners()
