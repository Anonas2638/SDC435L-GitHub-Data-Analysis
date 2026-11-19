
# Name: Anosha Naseri
# Date: 11/19/2026
# Course: SDC435L - Week 2 Group Project
# Feature: Top 10 Repositories by Watch Count

import json
from pymongo import MongoClient

# Location of the GitHub Archive dataset
file_path = r"C:\Users\Student\Downloads\GitHubArchive-Dataset\GitHubArchive-Dataset\Sample_Repos.json"

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/",
                     serverSelectionTimeoutMS=5000)

db = client["GitHubArchive"]
collection = db["Repositories"]

# Read JSON records and import them into MongoDB
records = []

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line:
            record = json.loads(line)

            # Convert watch_count from text to a number
            record["watch_count"] = int(record["watch_count"])
            records.append(record)

# Replace previously imported records to avoid duplicates
collection.delete_many({})

if records:
    collection.insert_many(records)

print("Successfully imported", len(records), "repositories into MongoDB!")

# Retrieve the 10 most-watched repositories
print("\nTOP 10 REPOSITORIES BY WATCH COUNT")
print("-" * 55)

top_repositories = collection.find(
    {},
    {"_id": 0, "repo_name": 1, "watch_count": 1}
).sort("watch_count", -1).limit(10)

for rank, repo in enumerate(top_repositories, start=1):
    print(f"{rank}. {repo['repo_name']} - {repo['watch_count']} watchers")

client.close()
print("\nAnalysis completed successfully!")
