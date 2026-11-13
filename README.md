# SDC435L – GitHub Data Analysis Group Project

## Project Overview

This project is part of the SDC435L NoSQL Databases Lab course at ECPI University. The goal is to develop a Python application that analyzes GitHub Archive data using five different database technologies over five weeks: Redis, MongoDB, Cassandra, Neo4j, and SQLite.

Each week, the application will be expanded to demonstrate database integration, data management, and analysis features.

## Week 1 – Redis Integration

The first week focuses on connecting Python to Redis, importing GitHub Archive data, and analyzing repository popularity.

### Features Implemented

**1. Redis Database Connection**
- Established a connection between Python and Redis.
- Verified the connection using the Redis PING command.

**2. GitHub Archive Data Import**
- Created `import_repositories.py` to read repository information from `Sample_Repos.json`.
- Stores repository records in Redis using keys beginning with `github:repo:`.
- Successfully imported and tested data from the provided GitHub Archive dataset.
- Configured the import script to limit future imports to 10,000 records.

**3. Repository Popularity Analysis**
- Created `repository_popularity.py`.
- Retrieves stored repository information from Redis.
- Sorts repositories by their `watch_count` values.
- Displays the top 10 most popular repositories.
- Successfully tested the analysis using 277,771 repository records stored in Redis.

## Technologies and Dependencies

- Python 3
- Redis database server
- redis Python library
- Ubuntu Linux / ECPI VCASTLE
- GitHub for version control
- GitHub Archive dataset

## Project Files

- `import_repositories.py` – Imports GitHub Archive repository data into Redis.
- `repository_popularity.py` – Retrieves and ranks repositories by popularity.
- `Sample_Repos.json` – Source dataset provided through ECPI Canvas (download separately).

## Setup Instructions

1. Download the GitHub Archive dataset from the SDC435L course in Canvas.
2. Install Python 3, Redis, and the Redis Python library.
3. Start the Redis server.
4. Place `Sample_Repos.json` in the same directory as the Python files.
5. Import repository data:

   `python3 import_repositories.py`

6. Run the repository popularity analysis:

   `python3 repository_popularity.py`

## Week 1 Development Status

**Completed:**
- GitHub repository created.
- Instructor invited to the repository.
- Python and Redis connection tested.
- GitHub Archive repository data imported.
- Repository popularity analysis implemented and tested.

**Remaining Group Requirements:**
- Implement user-controlled Create, Read, Update, and Delete operations.
- Complete two additional data-analysis features.
- Integrate all features into a single application.
- Complete group testing and final Week 1 submission.

## Future Development

In the following weeks, the application will be expanded to support MongoDB, Cassandra, Neo4j, and SQLite.

The goal is to create one Python application that demonstrates different database models and their capabilities for analyzing GitHub Archive data.

## Course Information

**Course:** SDC435L – NoSQL Databases Lab

**Project:** GitHub Data Analysis

**Institution:** ECPI University
