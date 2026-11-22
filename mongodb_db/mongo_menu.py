
# Name: Sherika Fayson
# Course: SDC435L
# Week 2: MongoDB Integration
# Purpose: Integrate all MongoDB application features.

from pymongo.errors import PyMongoError

from mongodb_db.mongo_connection import (
    get_connection,
    get_collection
)
from mongodb_db.mongo_import import import_repositories
from mongodb_db.mongo_crud import crud_menu
from mongodb_db.mongo_repository_analysis import (
    show_popular_repositories
)
from mongodb_db.mongo_name_analysis import (
    show_repository_names
)
from mongodb_db.mongo_watch_distribution import (
    show_watch_distribution
)


def mongo_menu():
    """Provide access to all MongoDB application features."""

    try:
        with get_connection() as client:
            collection = get_collection(client)

            print("\nSuccessfully connected to MongoDB!")

            while True:
                print("\n" + "=" * 50)
                print("         GITHUB DATA ANALYSIS")
                print("      SDC435L - MongoDB Integration")
                print("=" * 50)

                print("1. Import repository data")
                print("2. Manage repositories (CRUD)")
                print("3. Repository popularity analysis")
                print("4. Longest and shortest repository names")
                print("5. Repository watch count distribution")
                print("6. Return to main menu")

                choice = input("\nSelect an option: ").strip()

                try:
                    if choice == "1":
                        import_repositories(collection)

                    elif choice == "2":
                        crud_menu(collection)

                    elif choice == "3":
                        show_popular_repositories(collection)

                    elif choice == "4":
                        show_repository_names(collection)

                    elif choice == "5":
                        show_watch_distribution(collection)

                    elif choice == "6":
                        return

                    else:
                        print("Invalid selection. Please try again.")

                except (PyMongoError, OSError) as error:
                    print(f"Operation failed: {error}")

    except PyMongoError as error:
        print(f"MongoDB connection failed: {error}")


if __name__ == "__main__":
    mongo_menu()
