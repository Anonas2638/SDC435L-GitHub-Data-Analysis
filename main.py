# Name: Sherika Fayson
# Course: SDC435L
# Project: GitHub Data Analysis
# Purpose: Central application entry point.

from redis_db.redis_menu import redis_menu
from mongodb_db.mongo_menu import mongo_menu
from cassandra_db.cassandra_menu import cassandra_menu


def main():
    """Provide navigation between database integrations."""

    while True:
        print("\n" + "=" * 50)
        print("         GITHUB DATA ANALYSIS")
        print("        SDC435L - Group Project")
        print("=" * 50)

        print("1. Redis")
        print("2. MongoDB")
        print("3. Cassandra")
        print("4. Neo4j (Coming Soon)")
        print("5. SQLite (Coming Soon)")
        print("6. Exit")

        choice = input("\nSelect a database: ").strip()

        if choice == "1":
            redis_menu()

        elif choice == "2":
            mongo_menu()

        elif choice == "3":
            cassandra_menu()

        elif choice == "4":
            print("\nNeo4j integration is coming in Week 4.")

        elif choice == "5":
            print("\nSQLite integration is coming in Week 5.")

        elif choice == "6":
            print("\nThank you for using GitHub Data Analysis!")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
