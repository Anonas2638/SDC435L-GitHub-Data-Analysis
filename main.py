
import redis

from import_repositories import import_repositories
from redis_crud import crud_menu
from repository_popularity import (
    get_repositories_from_redis,
    show_popular_repositories
)
from owner_analysis import owner_analysis


def main():
    """Main entry point for the GitHub Data Analysis application."""

    connection = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    # Verify the Redis connection before starting the application.
    try:
        connection.ping()
        print("Connected to Redis successfully!")
    except redis.RedisError as error:
        print(f"Connection failed: {error}")
        return

    while True:
        print("\n" + "=" * 45)
        print("         GITHUB DATA ANALYSIS")
        print("       SDC435L - Redis Integration")
        print("=" * 45)

        print("1. Import repository data")
        print("2. Manage repositories (CRUD)")
        print("3. Repository popularity analysis")
        print("4. Repository owner analysis")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                import_repositories()

            elif choice == "2":
                crud_menu()

            elif choice == "3":
                repositories = get_repositories_from_redis()

                if repositories:
                    show_popular_repositories(repositories)
                else:
                    print("No repository records found.")

            elif choice == "4":
                owner_analysis()

            elif choice == "5":
                print("Thank you for using GitHub Data Analysis!")
                break

            else:
                print("Invalid selection. Please try again.")

        except redis.RedisError as error:
            print(f"Redis error: {error}")


if __name__ == "__main__":
    main()
