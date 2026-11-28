
"""Reusable database connection for the Neo4j graph database."""

import os

from neo4j import GraphDatabase


def get_neo4j_driver():
    """Create and verify a Neo4j driver using environment settings."""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")

    # Require credentials rather than hardcoding a database password.
    if not password:
        raise ValueError("NEO4J_PASSWORD environment variable is required.")

    driver = GraphDatabase.driver(
        uri,
        auth=(username, password)
    )

    # Verify connectivity and release resources if connection fails.
    try:
        driver.verify_connectivity()
    except Exception:
        driver.close()
        raise

    return driver


def test_connection():
    """Execute a simple Cypher query to verify database access."""
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    with get_neo4j_driver() as driver:
        with driver.session(database=database) as session:
            result = session.run("RETURN 1 AS connection_test")
            record = result.single()

            print("Neo4j connection successful!")
            print(f"Connection test: {record['connection_test']}")


if __name__ == "__main__":
    test_connection()
