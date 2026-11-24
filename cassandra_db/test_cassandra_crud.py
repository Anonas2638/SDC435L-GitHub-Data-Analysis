
"""Test Cassandra CRUD operations."""

from cassandra_db.cassandra_connection import get_cassandra_connection
from cassandra_db.cassandra_crud import (
    create_repository,
    read_repository,
    update_repository,
    delete_repository,
)


def test_crud():
    cluster = None
    repo_name = "test/crud-demo"

    try:
        cluster, session = get_cassandra_connection()

        # Clean up any leftover record from an earlier test.
        delete_repository(session, repo_name)

        # CREATE
        print("\n1. CREATE")
        created = create_repository(session, repo_name, 100)
        assert created, "Create failed"
        print(f"Repository created: {repo_name}")

        # READ
        print("\n2. READ")
        repository = read_repository(session, repo_name)
        assert repository is not None
        assert repository.watch_count == 100
        print(f"Repository: {repository.repo_name}")
        print(f"Watch count: {repository.watch_count}")

        # UPDATE
        print("\n3. UPDATE")
        updated = update_repository(session, repo_name, 250)
        assert updated, "Update failed"

        repository = read_repository(session, repo_name)
        assert repository.watch_count == 250
        print(f"Updated watch count: {repository.watch_count}")

        # DELETE
        print("\n4. DELETE")
        deleted = delete_repository(session, repo_name)
        assert deleted, "Delete failed"

        repository = read_repository(session, repo_name)
        assert repository is None
        print(f"Repository deleted: {repo_name}")

        print("\nAll four Cassandra CRUD tests passed!")

    except Exception as error:
        print(f"\nCRUD test failed: {error}")
        raise

    finally:
        if cluster is not None:
            cluster.shutdown()


if __name__ == "__main__":
    test_crud()
