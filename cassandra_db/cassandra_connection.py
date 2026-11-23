
"""Reusable Cassandra connection for the GitHub Data Analysis project."""

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT

CASSANDRA_HOST = "127.0.0.1"
CASSANDRA_PORT = 9042
KEYSPACE = "github_archive"


def get_cassandra_connection():
    """Connect to Cassandra and return the cluster and session."""

    profile = ExecutionProfile(
        consistency_level=ConsistencyLevel.ONE
    )

    cluster = Cluster(
        [CASSANDRA_HOST],
        port=CASSANDRA_PORT,
        connect_timeout=10,
        execution_profiles={
            EXEC_PROFILE_DEFAULT: profile
        },
    )

    try:
        session = cluster.connect(KEYSPACE)
        return cluster, session

    except Exception:
        cluster.shutdown()
        raise


def test_connection():
    """Verify Cassandra connectivity and the repositories table."""
    cluster = None

    try:
        cluster, session = get_cassandra_connection()

        result = session.execute(
            "SELECT table_name FROM system_schema.tables "
            "WHERE keyspace_name = %s AND table_name = %s",
            (KEYSPACE, "repositories"),
        )

        if result.one() is None:
            print("Connection successful, but repositories table is missing.")
            return

        print("Connected to Cassandra successfully!")
        print(f"Keyspace: {KEYSPACE}")
        print("Table: repositories")
        print(f"Host: {CASSANDRA_HOST}:{CASSANDRA_PORT}")

    except Exception as error:
        print(f"Cassandra connection failed: {error}")

    finally:
        if cluster is not None:
            cluster.shutdown()


if __name__ == "__main__":
    test_connection()
