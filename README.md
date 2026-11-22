# SDC435L – GitHub Data Analysis Group Project

## Project Overview

This ECPI University SDC435L group project develops a modular Python command-line application to explore GitHub Archive repository data using five database technologies over five weeks: Redis (key-value), MongoDB (document), Cassandra (wide-column), Neo4j (graph), and SQLite (relational).

**Week 1 (Redis)** and **Week 2 (MongoDB)** functionality are implemented and tested. The application offers one entry point, `python main.py`, with separate menus for each database. Cassandra, Neo4j, and SQLite appear as future-week placeholders and are **not implemented yet**.

## Week 1: Redis Integration

Redis stores repository records as JSON strings under keys formatted `github:repo:owner/repository`.

Implemented features:

1. **Connection:** Connects to a local Redis server and verifies connectivity with `PING`.
2. **Dataset import:** `redis_db/import_repositories.py` reads line-delimited records from `Sample_Repos.json` and imports up to 1,000 repository records per run.
3. **CRUD:** `redis_db/redis_crud.py` provides interactive Create, Read, Update, and Delete operations, with duplicate prevention, validation, and deletion confirmation.
4. **Popularity analysis:** `redis_db/repository_popularity.py` displays the ten repositories with the highest watch counts.
5. **Owner analysis:** `redis_db/owner_analysis.py` counts repositories by owner and displays the ten most frequent owners.
6. **Watch count statistics:** `redis_db/repository_statistics.py` calculates the total, mean, median, minimum, and maximum watch counts.
7. **Menu:** `redis_db/redis_menu.py` integrates importing, CRUD, and the three analyses into the Redis submenu.

The initial Redis popularity analysis was also tested against 277,771 records in the original development environment. The integrated application was tested using a reproducible 1,000-record sample.

## Week 2: MongoDB Integration

MongoDB stores repository records as BSON documents in database `GitHubArchive`, collection `Repositories`, using `mongodb://localhost:27017/`.

### Connection and import

- `mongodb_db/mongo_connection.py` provides reusable PyMongo connection and collection functions, with a connectivity check, timeout, and error handling.
- `mongodb_db/mongo_import.py` reads `Sample_Repos.json` from the project root, validates repository names and nonnegative watch counts, and converts watch counts to integers.
- The importer uses `update_one(..., {"$setOnInsert": ...}, upsert=True)` to preserve existing documents and prevent repeated imports from creating duplicates.
- It creates a unique ascending index on `repo_name` and a descending index on `watch_count`.
- It reports newly imported, already existing, and invalid records. A repeated 1,000-record import produced 0 new records, 1,000 existing records, and 0 invalid records.

### CRUD operations

`mongodb_db/mongo_crud.py` provides an interactive menu using `insert_one()`, `find_one()`, `update_one()`, and `delete_one()`. It validates input, rejects duplicate names and negative watch counts, requests confirmation before deletion, and handles missing repositories and invalid selections.

### Three MongoDB analysis features

1. **Top ten repositories by watch count:** `mongodb_db/mongo_repository_analysis.py`. Originally developed by Anosha Naseri and tested with 400,000 records. Refactored by Sherika Fayson to use the shared connection, sort and limit existing collection data, and avoid destructive deletion or reimporting. Retested successfully with 1,000 documents.
2. **Longest and shortest repository names:** `mongodb_db/mongo_name_analysis.py`. Uses MongoDB aggregation with `$strLenCP` and `$facet` to display the five longest and five shortest full repository names. Implemented and tested successfully.
3. **Watch count distribution:** `mongodb_db/mongo_watch_distribution.py`. Uses `$bucket` aggregation to count repositories across watch count ranges and display percentages and text bars. Implemented and tested successfully.

`mongodb_db/mongo_menu.py` integrates importing, CRUD, and all three MongoDB analyses.

## Project Structure

```text
SDC435L-GitHub-Data-Analysis/
├── main.py
├── redis_db/
│   ├── __init__.py
│   ├── import_repositories.py
│   ├── redis_crud.py
│   ├── redis_menu.py
│   ├── repository_popularity.py
│   ├── owner_analysis.py
│   └── repository_statistics.py
├── mongodb_db/
│   ├── __init__.py
│   ├── mongo_connection.py
│   ├── mongo_import.py
│   ├── mongo_crud.py
│   ├── mongo_menu.py
│   ├── mongo_repository_analysis.py
│   ├── mongo_name_analysis.py
│   └── mongo_watch_distribution.py
├── requirements.txt
├── README.md
├── .gitignore
└── Sample_Repos.json    # Download from Canvas; not tracked by Git
```

## Requirements

- Python 3 (tested locally with Python 3.13)
- Redis server, typically on `localhost:6379`
- MongoDB Community Server, typically on `localhost:27017`
- GitHub Archive `Sample_Repos.json` dataset provided through the course
- Python packages from `requirements.txt`: `redis==8.1.0` and `pymongo==4.20.1`
- Git and GitHub for collaboration

The application was developed and tested on macOS; some original feature development was performed in ECPI VCASTLE environments.

## Setup and Run

### 1. Clone the project and install dependencies

```bash
git clone https://github.com/Anonas2638/SDC435L-GitHub-Data-Analysis.git
cd SDC435L-GitHub-Data-Analysis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the virtual environment with `.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.

**Note:** Until the Week 2 pull request is merged, the completed MongoDB implementation is available on the `feature/mongodb-crud` branch rather than `main`.

### 2. Start the database servers

Install and start Redis and MongoDB Community Server for your operating system. On macOS with Homebrew, for example:

```bash
brew install redis
brew services start redis
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

For other platforms, follow the respective official Redis and MongoDB installation instructions. Verify the running services:

```bash
redis-cli ping
mongosh --eval 'db.adminCommand({ ping: 1 })'
```

Redis should return `PONG`, and MongoDB should report `ok: 1`.

### 3. Add the dataset

Download and extract the GitHub Archive dataset from the SDC435L Canvas course. Place `Sample_Repos.json` beside `main.py` in the project root. The dataset is not tracked in GitHub and must be obtained separately.

### 4. Launch the application

```bash
python main.py
```

The main menu is:

```text
GITHUB DATA ANALYSIS
SDC435L - Group Project
1. Redis
2. MongoDB
3. Cassandra (Coming Soon)
4. Neo4j (Coming Soon)
5. SQLite (Coming Soon)
6. Exit
```

Choose `1` for Redis or `2` for MongoDB. Each database submenu provides:

```text
1. Import repository data
2. Manage repositories (CRUD)
3. Repository popularity analysis
4. Repository owner analysis       [Redis]
   Longest and shortest names      [MongoDB]
5. Repository watch count statistics [Redis]
   Repository watch count distribution [MongoDB]
6. Return to main menu
```

Select option `1` in a database submenu before running analyses if its database is empty. The CRUD submenu allows users to create, read, update, and delete records and then return to the database menu.

### Run individual modules

Run these commands from the project root:

```bash
# Redis
python -m redis_db.import_repositories
python -m redis_db.redis_crud
python -m redis_db.repository_popularity
python -m redis_db.owner_analysis
python -m redis_db.repository_statistics

# MongoDB
python -m mongodb_db.mongo_import
python -m mongodb_db.mongo_crud
python -m mongodb_db.mongo_repository_analysis
python -m mongodb_db.mongo_name_analysis
python -m mongodb_db.mongo_watch_distribution
```

## Database Models

| Attribute | Redis | MongoDB |
| --- | --- | --- |
| Database type | Key-value | Document |
| Record representation | JSON string | BSON document |
| Repository identifier | `github:repo:<repo_name>` key | Unique `repo_name` field plus `_id` |
| `watch_count` representation | String from dataset | Integer |
| Analysis approach | Python iteration and statistics | MongoDB queries and aggregation |

Example dataset record:

```json
{"repo_name": "FreeCodeCamp/FreeCodeCamp", "watch_count": "90457"}
```

MongoDB stores the same repository with `watch_count: 90457` as an integer and an automatically generated `_id`. Indexes: `_id_`, unique `repo_name_1`, and descending `watch_count_-1`.

## Testing and Verification

### Week 1: Redis

Connection, import of 1,000 records, CRUD operations, duplicate handling, deletion verification, three analyses, menu navigation, invalid selections, and exit were tested successfully. CRUD was tested before the Redis package restructuring; dataset import and all three analyses were retested after restructuring and again through the integrated menu.

### Week 2: MongoDB

| Test | Result |
| --- | --- |
| Local MongoDB connection and ping | Passed |
| Initial import: 1,000 new documents | Passed |
| Repeat import: 0 new, 1,000 existing | Passed |
| Document schema and integer watch counts | Passed |
| Unique repository and descending watch count indexes | Passed |
| Create, read, update, delete, and verify deletion | Passed |
| Duplicate creation rejection | Passed |
| Invalid menu selection and CRUD exit | Passed |
| Popularity analysis, with existing documents preserved | Passed |
| Longest and shortest repository name analysis | Passed |
| Watch count distribution analysis | Passed |
| Redis and MongoDB navigation through `main.py` | Passed |
| Redis analyses after central menu integration | Passed |
| Future database placeholders and application exit | Passed |

These results describe the tests actually performed, not automated test-suite coverage. The final 1,000-document count was verified after the MongoDB CRUD and analysis tests.

## Sample Analysis Results

### Redis owner analysis (1,000 records)

| Rank | Owner | Repository count |
| ---: | --- | ---: |
| 1 | google | 22 |
| 2 | facebook | 19 |
| 3 | Ramotion | 8 |
| 4 | gaearon | 7 |
| 5 | reactjs | 7 |

### Redis watch count statistics (1,000 records)

| Metric | Value |
| --- | ---: |
| Total repositories | 1,000 |
| Total watches | 2,383,125 |
| Average watches | 2,383.12 |
| Median watches | 1,693 |
| Minimum watches | 1,083 |
| Maximum watches | 90,457 |

### MongoDB top ten repositories (1,000 documents)

| Rank | Repository | Watch count |
| ---: | --- | ---: |
| 1 | FreeCodeCamp/FreeCodeCamp | 90,457 |
| 2 | firehol/netdata | 13,208 |
| 3 | joshbuchea/HEAD | 13,125 |
| 4 | braydie/HowToBeAProgrammer | 12,019 |
| 5 | sindresorhus/awesome | 11,063 |
| 6 | tensorflow/tensorflow | 10,728 |
| 7 | facebook/react | 10,458 |
| 8 | ParsePlatform/parse-server | 10,339 |
| 9 | loverajoel/jstips | 9,585 |
| 10 | facebook/react-native | 9,437 |

### MongoDB repository name lengths (1,000 documents)

**Five longest:**

| Repository | Characters |
| --- | ---: |
| MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL- | 60 |
| numbbbbb/the-swift-programming-language-in-chinese | 50 |
| SamyPesse/How-to-Make-a-Computer-Operating-System | 49 |
| ReactjsProgram/react-fundamentals-curriculum | 44 |
| h5bp/Front-end-Developer-Interview-Questions | 44 |

**Five shortest:**

| Repository | Characters |
| --- | ---: |
| tj/co | 5 |
| v8/v8 | 5 |
| wg/wrk | 6 |
| git/git | 7 |
| npm/npm | 7 |

### MongoDB watch count distribution (1,000 documents)

| Watch count range | Repositories | Percentage |
| --- | ---: | ---: |
| 0–999 | 0 | 0.00% |
| 1,000–2,499 | 711 | 71.10% |
| 2,500–4,999 | 224 | 22.40% |
| 5,000–9,999 | 57 | 5.70% |
| 10,000+ | 8 | 0.80% |

Sample results depend on the imported dataset.

## Team Contributions

### Anosha Naseri

**Week 1:** Created and configured the group GitHub repository, invited collaborators and instructor, implemented the initial Redis connection and importer, developed repository popularity analysis, and prepared initial README and progress report documentation.

**Week 2:** Developed the original MongoDB repository popularity analysis, tested its initial standalone version with 400,000 records, uploaded the initial feature, and updated the group's README and progress report.

### Sherika Fayson

**Week 1:** Implemented Redis CRUD and interactive management, owner analysis, watch count statistics, integration, package restructuring, testing, documentation updates, and pull requests #1 and #2 (both merged).

**Week 2:** Set up local MongoDB, implemented reusable connection, schema and indexes, non-destructive importer, CRUD and validation, refactored Anosha's popularity analysis for shared integration, developed repository name length and watch count distribution analyses, implemented MongoDB menu, extracted the Redis submenu, integrated both into the main application, and tested all six analysis features and database navigation.

### Omari Johnson

Assigned the Week 2 repository name length and watch count distribution analyses. Contributions have not been confirmed. To meet the requirements, Sherika implemented and tested both features.

## Development Status

| Milestone | Status |
| --- | --- |
| Week 1 Redis implementation, testing, and PR merges | Complete |
| Week 1 final submission | Submitted |
| Week 2 MongoDB connection, import, CRUD, and three analyses | Complete and tested |
| Week 2 central application integration | Complete and tested |
| Week 2 README and documentation review | Complete and committed |
| Week 2 feature branch push | Complete |
| Week 2 pull request #3 | Merged into `main` |
| Week 2 final application ZIP | Completed |
| Week 2 progress report | Updated |
| Week 2 final submission | Completed |
| Week 3 Cassandra | Not started |
| Week 4 Neo4j | Not started |
| Week 5 SQLite | Not started |

## Future Development

Week 3 will add Cassandra integration while preserving the modular Python architecture. The later weeks will add Neo4j and SQLite. Each new database implementation will require connectivity, data import, CRUD functionality, three analysis features, integration testing, and documentation updates.

## Course Information

- **Course:** SDC435L – NoSQL Databases Lab
- **Institution:** ECPI University
- **Repository:** https://github.com/Anonas2638/SDC435L-GitHub-Data-Analysis
