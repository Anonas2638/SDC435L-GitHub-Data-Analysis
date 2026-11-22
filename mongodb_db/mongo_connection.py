
# Name: Sherika Fayson
# Course: SDC435L
# Week 2: MongoDB Integration
# Purpose: Establish a reusable MongoDB database connection.

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "GitHubArchive"
COLLECTION_NAME = "Repositories"


def get_connection():
    """Establish and verify a connection to MongoDB."""
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    try:
        client.admin.command("ping")
        return client
    except PyMongoError:
        client.close()
        raise


def get_collection(client):
    """Return the GitHub repository collection."""
    database = client[DATABASE_NAME]
    return database[COLLECTION_NAME]


def main():
    """Test the MongoDB connection independently."""
    try:
        with get_connection() as client:
            collection = get_collection(client)

            print("Successfully connected to MongoDB!")
            print(f"Database: {DATABASE_NAME}")
            print(f"Collection: {COLLECTION_NAME}")
            print(f"Total documents: {collection.count_documents({})}")

    except PyMongoError as error:
        print(f"MongoDB connection failed: {error}")


if __name__ == "__main__":
    main()
