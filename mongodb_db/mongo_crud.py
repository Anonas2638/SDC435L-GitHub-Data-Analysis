
# Name: Sherika Fayson
# Course: SDC435L
# Week 2: MongoDB Integration
# Purpose: Manage repository documents using CRUD operations.

from pymongo.errors import PyMongoError, DuplicateKeyError

from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)


# CREATE
def create_repository(collection, repo_name, watch_count):
    """Insert a new repository document."""

    repo_name = repo_name.strip()

    if not repo_name or watch_count < 0:
        raise ValueError("Invalid repository name or watch count.")

    document = {
        "repo_name": repo_name,
        "watch_count": watch_count
    }

    try:
        collection.insert_one(document)
        return True

    except DuplicateKeyError:
        return False


# READ
def read_repository(collection, repo_name):
    """Retrieve a repository by its name."""

    return collection.find_one(
        {"repo_name": repo_name.strip()}
    )


# UPDATE
def update_repository(collection, repo_name, watch_count):
    """Update the watch count of an existing repository."""

    if watch_count < 0:
        raise ValueError("Watch count cannot be negative.")

    result = collection.update_one(
        {"repo_name": repo_name.strip()},
        {"$set": {"watch_count": watch_count}}
    )

    return result.matched_count > 0


# DELETE
def delete_repository(collection, repo_name):
    """Delete an existing repository document."""

    result = collection.delete_one(
        {"repo_name": repo_name.strip()}
    )

    return result.deleted_count > 0


# USER INPUT
def get_repository_name():
    """Prompt the user for a valid repository name."""

    repo_name = input("Enter repository name: ").strip()

    if not repo_name:
        raise ValueError("Repository name cannot be empty.")

    return repo_name


def get_watch_count():
    """Prompt the user for a nonnegative watch count."""

    watch_count = int(input("Enter watch count: "))

    if watch_count < 0:
        raise ValueError("Watch count cannot be negative.")

    return watch_count


# INTERACTIVE CRUD MENU
def crud_menu(collection):
    """Allow users to manage MongoDB repository documents."""

    while True:
        print("\nMONGODB REPOSITORY MANAGEMENT")
        print("-" * 40)
        print("1. Create repository")
        print("2. Read repository")
        print("3. Update repository")
        print("4. Delete repository")
        print("5. Return to main menu")

        choice = input("\nSelect an option: ").strip()

        try:

            # Create
            if choice == "1":
                repo_name = get_repository_name()
                watch_count = get_watch_count()

                if create_repository(
                    collection, repo_name, watch_count
                ):
                    print("Repository created successfully.")
                else:
                    print("Repository already exists.")

            # Read
            elif choice == "2":
                repo_name = get_repository_name()

                repository = read_repository(
                    collection, repo_name
                )

                if repository:
                    print("\nREPOSITORY DETAILS")
                    print("-" * 40)
                    print(f"ID: {repository['_id']}")
                    print(f"Name: {repository['repo_name']}")
                    print(f"Watch count: {repository['watch_count']:,}")
                else:
                    print("Repository not found.")

            # Update
            elif choice == "3":
                repo_name = get_repository_name()
                watch_count = get_watch_count()

                if update_repository(
                    collection, repo_name, watch_count
                ):
                    print("Repository updated successfully.")
                else:
                    print("Repository not found.")

            # Delete
            elif choice == "4":
                repo_name = get_repository_name()

                confirm = input(
                    f"Delete {repo_name}? (y/n): "
                ).strip().lower()

                if confirm == "y":

                    if delete_repository(
                        collection, repo_name
                    ):
                        print("Repository deleted successfully.")
                    else:
                        print("Repository not found.")

                else:
                    print("Deletion cancelled.")

            # Return
            elif choice == "5":
                return

            else:
                print("Invalid selection. Please try again.")

        except ValueError as error:
            print(f"Invalid input: {error}")

        except PyMongoError as error:
            print(f"Database error: {error}")


def main():
    """Run the MongoDB CRUD menu independently."""

    try:
        with get_connection() as client:
            collection = get_collection(client)
            crud_menu(collection)

    except PyMongoError as error:
        print(f"MongoDB error: {error}")


if __name__ == "__main__":
    main()
