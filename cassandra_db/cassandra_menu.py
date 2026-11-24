
"""Interactive Cassandra repository management menu."""

from cassandra_db.cassandra_connection import get_cassandra_connection
from cassandra_db.cassandra_crud import (
    create_repository,
    read_repository,
    update_repository,
    delete_repository,
)


def get_watch_count():
    """Prompt for a valid, nonnegative Cassandra integer."""
    while True:
        try:
            count = int(input("Enter watch count: ").strip())
            if 0 <= count <= 2147483647:
                return count
            print("Enter a number between 0 and 2147483647.")
        except ValueError:
            print("Please enter a valid whole number.")


def get_repo_name():
    """Prompt for a nonempty repository name."""
    while True:
        name = input("Enter repository name: ").strip()
        if name:
            return name
        print("Repository name cannot be empty.")


def cassandra_menu():
    """Run the interactive CRUD menu."""
    cluster = None

    try:
        cluster, session = get_cassandra_connection()
        print("\nConnected to Cassandra successfully!")

        while True:
            print("\n===== Cassandra Repository Menu =====")
            print("1. Create repository")
            print("2. Read repository")
            print("3. Update repository watch count")
            print("4. Delete repository")
            print("5. Exit")

            choice = input("Choose an option (1-5): ").strip()

            try:
                if choice == "1":
                    name = get_repo_name()
                    count = get_watch_count()

                    if create_repository(session, name, count):
                        print("Repository created successfully.")
                    else:
                        print("Repository already exists.")

                elif choice == "2":
                    name = get_repo_name()
                    repository = read_repository(session, name)

                    if repository:
                        print(f"Repository: {repository.repo_name}")
                        print(f"Watch count: {repository.watch_count}")
                    else:
                        print("Repository not found.")

                elif choice == "3":
                    name = get_repo_name()
                    count = get_watch_count()

                    if update_repository(session, name, count):
                        print("Repository updated successfully.")
                    else:
                        print("Repository not found.")

                elif choice == "4":
                    name = get_repo_name()

                    confirm = input(
                        f"Delete '{name}'? (yes/no): "
                    ).strip().lower()

                    if confirm == "yes":
                        if delete_repository(session, name):
                            print("Repository deleted successfully.")
                        else:
                            print("Repository not found.")
                    else:
                        print("Deletion cancelled.")

                elif choice == "5":
                    print("Exiting Cassandra menu.")
                    break

                else:
                    print("Invalid option. Choose 1-5.")

            except Exception as error:
                print(f"Database operation failed: {error}")

    except Exception as error:
        print(f"Unable to connect to Cassandra: {error}")

    finally:
        if cluster is not None:
            cluster.shutdown()


if __name__ == "__main__":
    cassandra_menu()
