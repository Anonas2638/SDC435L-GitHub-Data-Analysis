
"""Initialize the graph database schema and uniqueness constraints."""

import os

from neo4j_db.neo4j_connection import get_neo4j_driver


def create_constraints():
    """Create unique identifiers for owner and repository nodes."""
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    constraints = [
        """
        CREATE CONSTRAINT owner_name_unique IF NOT EXISTS
        FOR (o:Owner)
        REQUIRE o.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT repository_name_unique IF NOT EXISTS
        FOR (r:Repository)
        REQUIRE r.repo_name IS UNIQUE
        """
    ]

    with get_neo4j_driver() as driver:
        with driver.session(database=database) as session:

            # IF NOT EXISTS allows safe execution on repeated runs.
            for query in constraints:
                session.run(query).consume()

            print("Neo4j schema initialized successfully.")

            # Display the constraints for verification.
            result = session.run(
                "SHOW CONSTRAINTS YIELD name, type "
                "RETURN name, type ORDER BY name"
            )

            for record in result:
                print(f"{record['name']}: {record['type']}")


if __name__ == "__main__":
    create_constraints()
