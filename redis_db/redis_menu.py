
# Name: Sherika Fayson
# Course: SDC435L
# Purpose: Integrate all Redis application features.

import redis

from redis_db.import_repositories import import_repositories
from redis_db.redis_crud import crud_menu
from redis_db.repository_popularity import (
    get_repositories_from_redis,
    show_popular_repositories
)
from redis_db.owner_analysis import owner_analysis
from redis_db.repository_statistics import repository_statistics


def redis_menu():
    """Provide access to all Redis application features."""

    connection = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    # Verify the Redis connection.
    try:
        connection.ping()
        print("\nConnected to Redis successfully!")
    except redis.RedisError as error:
        print(f"Connection failed: {error}")
        return

    while True:
        print("\n" + "=" * 50)
        print("         GITHUB DATA ANALYSIS")
        print("       SDC435L - Redis Integration")
        print("=" * 50)

        print("1. Import repository data")
        print("2. Manage repositories (CRUD)")
        print("3. Repository popularity analysis")
        print("4. Repository owner analysis")
        print("5. Repository watch count statistics")
        print("6. Return to main menu")

        choice = input("\nSelect an option: ").strip()

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
                repository_statistics()

            elif choice == "6":
                return

            else:
                print("Invalid selection. Please try again.")

        except redis.RedisError as error:
            print(f"Redis error: {error}")


if __name__ == "__main__":
    redis_menu()
