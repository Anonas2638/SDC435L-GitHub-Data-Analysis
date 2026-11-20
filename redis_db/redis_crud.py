
import json
import redis

# Establish a connection to the Redis database.
connection = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

PREFIX = "github:repo:"


def create_repository(repo_name, watch_count):
    """Create a new repository without overwriting existing data."""
    repo_name = repo_name.strip()

    if not repo_name or watch_count < 0:
        return False

    key = PREFIX + repo_name

    repository = {
        "repo_name": repo_name,
        "watch_count": str(watch_count)
    }

    return bool(
        connection.set(key, json.dumps(repository), nx=True)
    )


def read_repository(repo_name):
    """Retrieve a repository from Redis."""
    key = PREFIX + repo_name
    data = connection.get(key)

    if data is None:
        return None

    return json.loads(data)


def update_repository(repo_name, watch_count):
    """Update the watch count of an existing repository."""
    repository = read_repository(repo_name)

    if repository is None or watch_count < 0:
        return False

    repository["watch_count"] = str(watch_count)

    key = PREFIX + repo_name

    return bool(
        connection.set(key, json.dumps(repository), xx=True)
    )


def delete_repository(repo_name):
    """Delete a repository from Redis."""
    key = PREFIX + repo_name

    return connection.delete(key) > 0


def crud_menu():
    """Allow users to manage repository records."""

    while True:
        print("\n--- Repository Management ---")
        print("1. Create repository")
        print("2. Read repository")
        print("3. Update repository")
        print("4. Delete repository")
        print("5. Return to main menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Repository name (owner/repo): ").strip()
                count = int(input("Watch count: "))

                if create_repository(name, count):
                    print("Repository created successfully.")
                else:
                    print("Invalid input or repository already exists.")

            elif choice == "2":
                name = input("Repository name: ").strip()
                repository = read_repository(name)

                if repository is not None:
                    print(json.dumps(repository, indent=4))
                else:
                    print("Repository not found.")

            elif choice == "3":
                name = input("Repository name: ").strip()
                count = int(input("New watch count: "))

                if update_repository(name, count):
                    print("Repository updated successfully.")
                else:
                    print("Repository not found or invalid watch count.")

            elif choice == "4":
                name = input("Repository name: ").strip()
                confirm = input("Confirm deletion (y/n): ").lower()

                if confirm == "y":
                    if delete_repository(name):
                        print("Repository deleted successfully.")
                    else:
                        print("Repository not found.")
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                break

            else:
                print("Invalid selection. Please try again.")

        except ValueError:
            print("Watch count must be a valid integer.")

        except redis.RedisError as error:
            print(f"Redis error: {error}")


if __name__ == "__main__":
    try:
        connection.ping()
        crud_menu()
    except redis.RedisError as error:
        print(f"Connection failed: {error}")
