"""CRUD operations for GitHub repositories stored in Cassandra."""

from input_validation import validate_repository_name, validate_watch_count

def validate_cassandra_watch_count(watch_count):
    """Validate a watch count against Cassandra's integer limits."""
    count = validate_watch_count(watch_count)

    if count > 2147483647:
        raise ValueError(
            "Watch count cannot exceed 2147483647."
        )

    return count

def create_repository(session, repo_name, watch_count):
    """Create a repository only if it does not already exist."""
    repo_name = validate_repository_name(repo_name)
    watch_count = validate_cassandra_watch_count(watch_count)
    statement = session.prepare(
        """
        INSERT INTO repositories (repo_name, watch_count)
        VALUES (?, ?)
        IF NOT EXISTS
        """
    )
    result = session.execute(statement, (repo_name, watch_count))
    return result.one().applied


def read_repository(session, repo_name):
    """Retrieve a repository using its primary key."""
    repo_name = validate_repository_name(repo_name)
    statement = session.prepare(
        """
        SELECT repo_name, watch_count
        FROM repositories
        WHERE repo_name = ?
        """
    )
    return session.execute(statement, (repo_name,)).one()


def update_repository(session, repo_name, watch_count):
    """Update an existing repository's watch count."""
    repo_name = validate_repository_name(repo_name)
    watch_count = validate_cassandra_watch_count(watch_count)
    statement = session.prepare(
        """
        UPDATE repositories
        SET watch_count = ?
        WHERE repo_name = ?
        IF EXISTS
        """
    )
    result = session.execute(statement, (watch_count, repo_name))
    return result.one().applied


def delete_repository(session, repo_name):
    """Delete a repository only if it exists."""
    repo_name = validate_repository_name(repo_name)
    statement = session.prepare(
        """
        DELETE FROM repositories
        WHERE repo_name = ?
        IF EXISTS
        """
    )
    result = session.execute(statement, (repo_name,))
    return result.one().applied
