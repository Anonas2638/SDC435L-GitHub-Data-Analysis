# SDC435L – GitHub Data Analysis Group Project

## Project Overview

This ECPI University SDC435L group project develops a modular
Python command-line application to explore GitHub Archive
repository data using five database technologies over five weeks:

- Redis (key-value)
- MongoDB (document)
- Cassandra (wide-column)
- Neo4j (graph)
- SQLite (relational)

The application provides a centralized entry point through
`main.py`, with separate modules for database connectivity,
dataset imports, CRUD operations, and repository data analysis.

Weeks 1, 2, and 3 are implemented. Neo4j and SQLite remain
scheduled for future development.

## Development Status

| Week | Database | Status |
| ------ | ---------- | -------- |
| 1 | Redis | Complete and submitted |
| 2 | MongoDB | Complete and submitted |
| 3 | Cassandra | Implemented and tested |
| 4 | Neo4j | Planned |
| 5 | SQLite | Planned |

---

## Week 1: Redis Integration

Redis stores repository records as JSON strings using keys
formatted as `github:repo:owner/repository`.

### Redis Implemented Features

- Local Redis connection and connectivity verification.
- JSON Lines dataset import of up to 1,000 valid records.
- Interactive Create, Read, Update, and Delete operations.
- Duplicate repository prevention.
- Repository popularity analysis.
- Top 10 repository owners.
- Repository watch count statistics.
- Repository name length analysis module.
- Integration with the central application menu.

### Data Import

The `redis_db/import_repositories.py` module reads
`Sample_Repos.json` from the project root.

The importer validates repository names and watch counts,
skips invalid records, and uses conditional insertion
(`nx=True`) to prevent existing records from being overwritten.

Import results report:

- Valid records processed.
- Newly imported repositories.
- Existing repositories.
- Invalid records skipped.

### Redis Analysis Modules

| Module | Purpose |
| -------- | --------- |
| `repository_popularity.py` | Top 10 repositories by watch count |
| `owner_analysis.py` | Top 10 repository owners |
| `repository_statistics.py` | Watch count descriptive statistics |
| `repo_name_length_analysis.py` | Repository name length analysis |

The original Redis popularity analysis was also tested
against 277,771 records in the initial development environment.

The integrated application uses a reproducible
1,000-record sample.

---

## Week 2: MongoDB Integration

MongoDB stores repository records as BSON documents in the
`GitHubArchive` database and `Repositories` collection.

Default connection:

`mongodb://localhost:27017/`

### Connection and Import

- Reusable database connection and collection functions.
- Connectivity verification and error handling.
- Repository name and watch count validation.
- Integer conversion for watch counts.
- Non-destructive imports using `$setOnInsert` and upsert.
- Unique ascending index on `repo_name`.
- Descending index on `watch_count`.

### CRUD Operations

The `mongodb_db/mongo_crud.py` module provides interactive
repository management using:

- `insert_one()`
- `find_one()`
- `update_one()`
- `delete_one()`

The application validates repository identifiers and watch
counts, rejects duplicates, requests confirmation before
deletion, and handles missing repositories.

### MongoDB Analysis Modules

| Module | Purpose |
| -------- | --------- |
| `mongo_repository_analysis.py` | Top 10 repositories by watch count |
| `mongo_name_analysis.py` | Five longest and shortest repository names |
| `mongo_watch_distribution.py` | Watch count distribution and percentages |

The original MongoDB popularity analysis was tested with
400,000 records before being refactored to use the shared
database connection and existing collection data.

The integrated implementation was tested using 1,000 documents.

---

## Week 3: Cassandra Integration

Cassandra stores repository records using a wide-column
database model and Cassandra Query Language (CQL).

### Database Configuration

| Setting | Value |
| --------- | ------- |
| Host | 127.0.0.1 |
| Port | 9042 |
| Keyspace | github_archive |
| Table | repositories |
| Primary key | repo_name |
| Repository name type | TEXT |
| Watch count type | INT |
| Replication factor | 1 |
| Consistency level | ONE |

The replication and consistency settings are intended for
the local, single-node development environment rather than
a production deployment.

### Cassandra Implemented Features

- Reusable Cassandra connection and session management.
- Keyspace and table configuration.
- JSON Lines dataset import.
- Prepared CQL statements.
- Conditional insertion using `IF NOT EXISTS`.
- Interactive Create, Read, Update, and Delete operations.
- Repository name and watch count validation.
- Cassandra integer range validation.
- Three repository analysis features.
- Central application menu integration.
- Automated watch count distribution tests.

### Analysis Features

The `cassandra_db/cassandra_analysis.py` module provides:

1. Top 10 repositories ranked by watch count.
2. Longest and shortest repository names, including
   average repository name length.
3. Watch count distribution across defined ranges.

The watch count distribution implementation was corrected
to ensure each repository is assigned to the appropriate
watch count range.

### Development Environments

Cassandra development was performed using two environments:

| Component | Local macOS | ECPI VCASTLE |
| ----------- | ------------- | -------------- |
| Operating system | macOS | Ubuntu Linux |
| Python | 3.13 | 3.8.10 |
| Cassandra | 5.0.9 | 4.0.5 |
| Deployment | Docker | Local installation |
| Python driver | 3.29.3 | 3.29.3 |

Dependency compatibility should be verified when installing
the updated application in either environment.

---

## Project Structure

```text
SDC435L-GitHub-Data-Analysis/
├── main.py
├── input_validation.py
├── test_input_validation.py
├── redis_db/
│   ├── __init__.py
│   ├── import_repositories.py
│   ├── owner_analysis.py
│   ├── redis_crud.py
│   ├── redis_menu.py
│   ├── repo_name_length_analysis.py
│   ├── repository_popularity.py
│   └── repository_statistics.py
├── mongodb_db/
│   ├── __init__.py
│   ├── mongo_connection.py
│   ├── mongo_crud.py
│   ├── mongo_import.py
│   ├── mongo_menu.py
│   ├── mongo_name_analysis.py
│   ├── mongo_repository_analysis.py
│   └── mongo_watch_distribution.py
├── cassandra_db/
│   ├── __init__.py
│   ├── cassandra_analysis.py
│   ├── cassandra_connection.py
│   ├── cassandra_crud.py
│   ├── cassandra_import.py
│   ├── cassandra_menu.py
│   ├── test_cassandra_analysis.py
│   └── test_cassandra_crud.py
├── requirements.txt
├── README.md
├── .gitignore
└── Sample_Repos.json
```

The dataset is provided through the course and is not
tracked in Git.

---

## Requirements

- Python 3
- Git
- Redis server
- MongoDB Community Server
- Apache Cassandra
- Docker Desktop for containerized Cassandra deployment
  on macOS
- GitHub Archive `Sample_Repos.json` dataset

### Python Dependencies

Dependencies are managed through `requirements.txt`.

```text
redis==6.1.1
pymongo==4.10.1
cassandra-driver==3.29.3
orjson>=3.10.7,<4
```

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Anonas2638/SDC435L-GitHub-Data-Analysis.git

cd SDC435L-GitHub-Data-Analysis
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Start Redis

On macOS using Homebrew:

```bash
brew install redis
brew services start redis
```

Verify the connection:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

### 4. Start MongoDB

On macOS using Homebrew:

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Verify the connection:

```bash
mongosh --eval 'db.adminCommand({ ping: 1 })'
```

MongoDB should return `ok: 1`.

### 5. Start Cassandra

For local development using Docker Desktop:

```bash
docker run -d \
  --name cassandra-week3 \
  -p 127.0.0.1:9042:9042 \
  -e MAX_HEAP_SIZE=1G \
  -e HEAP_NEWSIZE=200M \
  -v cassandra-week3-data:/var/lib/cassandra \
  cassandra:5.0
```

If the container already exists, start it instead:

```bash
docker start cassandra-week3
```

Allow Cassandra sufficient time to initialize.

Verify the node status:

```bash
docker exec cassandra-week3 nodetool status
```

Connect to Cassandra:

```bash
docker exec -it cassandra-week3 cqlsh
```

Create the development keyspace and table if they do not
already exist:

```sql
CREATE KEYSPACE IF NOT EXISTS github_archive
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE github_archive;

CREATE TABLE IF NOT EXISTS repositories (
    repo_name TEXT PRIMARY KEY,
    watch_count INT
);
```

Exit CQLSH:

```sql
EXIT;
```

For ECPI VCASTLE environments with Cassandra already
installed, verify the running service using:

```bash
nodetool status
```

Then connect using:

```bash
cqlsh
```

Use the same keyspace and table configuration.

### 6. Add the Dataset

Download and extract `Sample_Repos.json` from the SDC435L
Canvas course.

Place the dataset in the project root beside `main.py`.

---

## Running the Application

From the project root with the virtual environment activated:

```bash
python main.py
```

### Main Menu

```text
==================================================
         GITHUB DATA ANALYSIS
        SDC435L - Group Project
==================================================
1. Redis
2. MongoDB
3. Cassandra
4. Neo4j (Coming Soon)
5. SQLite (Coming Soon)
6. Exit
```

Select the database you want to use.

Each implemented database provides access to repository
imports, CRUD operations, analysis features, and navigation
back to the main menu.

Import repository data before running analyses if the
selected database is empty.

### Running Individual Modules

#### Redis

```bash
python -m redis_db.import_repositories
python -m redis_db.redis_crud
python -m redis_db.repository_popularity
python -m redis_db.owner_analysis
python -m redis_db.repository_statistics
```

#### MongoDB

```bash
python -m mongodb_db.mongo_import
python -m mongodb_db.mongo_crud
python -m mongodb_db.mongo_repository_analysis
python -m mongodb_db.mongo_name_analysis
python -m mongodb_db.mongo_watch_distribution
```

#### Cassandra

```bash
python -m cassandra_db.cassandra_import
python -m cassandra_db.test_cassandra_crud
```

Cassandra analysis features are accessible through option 3
of the main application menu.

---

## Database Model Comparison

| Attribute | Redis | MongoDB | Cassandra |
| ----------- | ------- | --------- | ----------- |
| Database model | Key-value | Document | Wide-column |
| Record representation | JSON string | BSON document | CQL row |
| Repository identifier | Redis key | Unique repo_name field | Primary key |
| Watch count type | String | Integer | 32-bit integer |
| Query approach | Redis commands | MongoDB queries | CQL |
| Analysis approach | Python iteration | Aggregation queries | CQL + Python |
| Duplicate prevention | SET NX | Unique index/upsert | INSERT IF NOT EXISTS |

### Example Dataset Record

```json
{
    "repo_name": "FreeCodeCamp/FreeCodeCamp",
    "watch_count": "90457"
}
```

Redis preserves the JSON string representation.

MongoDB converts the watch count to an integer and
generates an `_id` field.

Cassandra stores the repository name as a TEXT primary key
and the watch count as an INT column.

---

## Code Quality and Performance Improvements

Following instructor feedback, the application was refactored
to improve input validation, JSON decoding performance,
maintainability, and data integrity.

### Shared Input Validation

The `input_validation.py` module centralizes reusable
validation logic across Redis, MongoDB, and Cassandra.

The module:

- Validates repository names using the `owner/repository`
  format.
- Removes leading and trailing whitespace.
- Rejects unsupported characters and malformed names.
- Accepts only nonnegative integer watch counts.
- Rejects Boolean values, decimals, and invalid text.
- Converts valid numeric strings into integers.

Database-specific validation also enforces storage limits.

| Database | Maximum watch count enforced |
| ---------- | ------------------------------ |
| Redis | No database-specific integer limit |
| MongoDB | 9,223,372,036,854,775,807 |
| Cassandra | 2,147,483,647 |

The repository name validation rules are application-specific
and are not intended to implement every GitHub naming rule.

### Maintainability

- Shared validation functions reduce duplicated logic.
- Comments explain important implementation decisions.
- Docstrings describe function responsibilities.
- Validation is performed before database operations.
- Existing modular database architecture is preserved.

### Data Integrity

- Redis uses conditional insertion with `nx=True`.
- MongoDB uses `$setOnInsert` with upsert.
- Cassandra uses `INSERT IF NOT EXISTS`.
- Invalid dataset records are skipped during imports.
- Existing Redis JSON storage compatibility is maintained.
- Repeated imports preserve existing repository records.

---

## JSON Performance Benchmark

The application uses `orjson` for JSON decoding during
dataset imports and selected Redis retrieval and analysis
operations.

A local benchmark was performed on macOS using all 400,000
records from `Sample_Repos.json`.

Each JSON library was tested five times using the same
records. File loading was excluded from the timed operations,
and the median execution time was recorded.

### Benchmark Results

| Metric | Standard json | orjson |
| -------- | --------------- | -------- |
| Records decoded | 400,000 | 400,000 |
| Benchmark runs | 5 | 5 |
| Median decoding time | 0.3310 seconds | 0.0654 seconds |

Measured improvements:

- JSON decoding speedup: **5.06x**
- JSON decoding time reduction: **80.25%**

All 400,000 records were successfully decoded by both
libraries during the benchmark.

These measurements represent JSON decoding performance
only, not total database import execution time or overall
application performance.

Results may vary across hardware, operating systems,
Python versions, and dependency versions.

---

## Testing and Verification

### Automated Testing

Automated tests cover:

- Repository name normalization.
- Malformed and unsupported repository names.
- Invalid watch count values.
- Numeric string conversion.
- MongoDB integer boundaries.
- Cassandra integer boundaries.
- Validation before database access.
- Existing Redis JSON compatibility.
- Redis conditional import behavior.
- Cassandra watch count distribution.

Run the automated test suite from the project root:

```bash
python -m unittest test_input_validation cassandra_db.test_cassandra_analysis -v
```

Latest local result:

```text
Ran 17 tests in 0.006s

OK
```

**17 of 17 automated tests passed.**

### Cassandra Live CRUD Testing

With Cassandra running and the keyspace and table configured:

```bash
python -m cassandra_db.test_cassandra_crud
```

The live test verifies:

1. Create a temporary repository.
2. Read and verify its watch count.
3. Update and verify its watch count.
4. Delete and verify its removal.

All four Cassandra CRUD operations passed.

### Import Regression Testing

Repeated imports were tested using the existing
1,000-record sample in each database.

| Database | Records processed | New | Existing |
| ---------- | ------------------- | ----- | ---------- |
| Redis | 1,000 | 0 | 1,000 |
| MongoDB | 1,000 | 0 | 1,000 |
| Cassandra | 1,000 | 0 | 1,000 |

Redis and MongoDB also reported zero invalid records
during their repeated import tests.

### Manual Regression Testing

| Test | Redis | MongoDB | Cassandra |
| ------ | ------- | --------- | ----------- |
| Database connection | Passed | Passed | Passed |
| Dataset import | Passed | Passed | Passed |
| Repeated import | Passed | Passed | Passed |
| Create repository | Passed | Passed | Passed |
| Read repository | Passed | Passed | Passed |
| Update repository | Passed | Passed | Passed |
| Delete repository | Passed | Passed | Passed |

Additional Redis verification included:

- Duplicate creation rejection.
- Invalid repository name rejection.
- Negative and decimal watch count rejection.
- Invalid update input rejection.
- Graceful error handling.
- Existing JSON storage compatibility.
- Matching SHA-256 checksums for a sampled repository
  before and after repeated import.
- Repository popularity and owner analysis regression tests.

A mocked importer test also verifies that conditional
insertion is requested and existing records are counted
correctly.

MongoDB invalid-input handling was manually retested.

The Cassandra watch count distribution is covered by
automated unit tests.

Not every previously implemented analysis feature was
rerun during the shared validation refactoring.

---

## Sample Analysis Results

The following results are based on the reproducible
1,000-record dataset sample.

### Top 10 Repositories by Watch Count

| Rank | Repository | Watch count |
| ------ | ------------ | ------------- |
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

These popularity results were observed across the
Redis, MongoDB, and Cassandra implementations.

### Redis Owner Analysis

| Rank | Owner | Repository count |
| ------ | ------- | ------------------ |
| 1 | google | 22 |
| 2 | facebook | 19 |
| 3 | Ramotion | 8 |
| 4 | gaearon | 7 |
| 5 | reactjs | 7 |
| 6 | angular | 6 |
| 7 | Microsoft | 6 |
| 8 | sindresorhus | 5 |
| 9 | github | 5 |
| 10 | airbnb | 4 |

### Redis Watch Count Statistics

| Metric | Value |
| -------- | ------- |
| Total repositories | 1,000 |
| Total watches | 2,383,125 |
| Average watches | 2,383.12 |
| Median watches | 1,693 |
| Minimum watches | 1,083 |
| Maximum watches | 90,457 |

### MongoDB Repository Name Analysis

#### Five Longest Repository Names

| Repository | Characters |
| ------------ | ------------ |
| MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL- | 60 |
| numbbbbb/the-swift-programming-language-in-chinese | 50 |
| SamyPesse/How-to-Make-a-Computer-Operating-System | 49 |
| ReactjsProgram/react-fundamentals-curriculum | 44 |
| h5bp/Front-end-Developer-Interview-Questions | 44 |

#### Five Shortest Repository Names

| Repository | Characters |
| ------------ | ------------ |
| tj/co | 5 |
| v8/v8 | 5 |
| wg/wrk | 6 |
| git/git | 7 |
| npm/npm | 7 |

### MongoDB Watch Count Distribution

| Watch count range | Repositories | Percentage |
| ------------------- | -------------- | ------------ |
| 0–999 | 0 | 0.00% |
| 1,000–2,499 | 711 | 71.10% |
| 2,500–4,999 | 224 | 22.40% |
| 5,000–9,999 | 57 | 5.70% |
| 10,000+ | 8 | 0.80% |
| Total | 1,000 | 100.00% |

### Cassandra Repository Name Analysis

| Metric | Result |
| -------- | -------- |
| Longest repository name length | 60 characters |
| Shortest repository name returned | v8/v8 |
| Shortest name length | 5 |
| Average repository name length | 19.90 |

Longest repository name:
`MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-`

Multiple repositories may share the same name length.

### Cassandra Watch Count Distribution

| Watch count range | Repositories | Percentage |
| ------------------- | -------------- | ------------ |
| 0 | 0 | 0.00% |
| 1–100 | 0 | 0.00% |
| 101–1,000 | 0 | 0.00% |
| 1,001–10,000 | 992 | 99.20% |
| 10,001+ | 8 | 0.80% |
| Total | 1,000 | 100.00% |

MongoDB and Cassandra use different distribution ranges.
Their individual bucket counts are therefore not directly
comparable.

Sample analysis results depend on the imported dataset.

---

## Team Contributions

### Anosha Naseri

#### Week 1 — Anosha Naseri

- Created and configured the group GitHub repository.
- Invited collaborators and the instructor.
- Implemented the initial Redis connection and importer.
- Developed repository popularity analysis.
- Prepared README and progress report documentation.

#### Week 2 — Anosha Naseri

- Developed the original MongoDB repository popularity
  analysis.
- Tested the standalone implementation with 400,000 records.
- Updated the group README and progress report.

#### Week 3 — Anosha Naseri

- Configured Cassandra in the VCASTLE environment.
- Developed Cassandra repository popularity analysis.
- Developed repository name length analysis.
- Contributed to application integration and testing.
- Updated project documentation.

### Sherika Fayson

#### Week 1 — Sherika Fayson

- Implemented Redis CRUD and interactive management.
- Developed repository owner analysis.
- Developed watch count statistics.
- Integrated and restructured the Redis application.
- Performed testing and documentation updates.
- Created pull requests #1 and #2.

#### Week 2 — Sherika Fayson

- Configured the local MongoDB environment.
- Implemented reusable database connection functions.
- Developed document schema, indexes, and non-destructive
  dataset imports.
- Implemented CRUD operations and input validation.
- Refactored repository popularity analysis for integration.
- Developed repository name and watch count distribution
  analyses.
- Integrated Redis and MongoDB into the central menu.
- Performed application testing and documentation.

#### Week 3 — Sherika Fayson

- Configured Cassandra locally using Docker.
- Implemented Cassandra database connectivity.
- Configured the keyspace and table.
- Developed the JSON dataset importer.
- Implemented prepared CQL CRUD operations.
- Developed the interactive repository management menu.
- Performed Cassandra import and CRUD testing.
- Corrected Cassandra watch count distribution logic.
- Added automated distribution tests.
- Verified corrected distribution results.

#### Cross-Database Code Quality Improvements

- Implemented shared input validation.
- Added database-specific integer range validation.
- Integrated `orjson` for optimized JSON decoding.
- Improved Redis import data integrity.
- Added comments and documentation.
- Expanded automated test coverage.
- Performed cross-database regression testing.
- Conducted a 400,000-record JSON decoding benchmark.

### Omari Johnson

#### Week 2 — Omari Johnson

Assigned repository name length and watch count distribution
analyses. Contributions were not confirmed in the original
Week 2 documentation. Both features were implemented and
tested by Sherika Fayson.

#### Week 3 — Omari Johnson

- Contributed the initial Cassandra watch count distribution
  implementation.

---

## Future Development

### Week 4: Neo4j

Planned implementation of a graph database integration
following the existing modular architecture.

### Week 5: SQLite

Planned implementation of a relational database integration
and final application consolidation.

### Continued Improvements

- Reuse shared validation across future database modules.
- Expand automated test coverage.
- Verify dependency compatibility across development
  environments.
- Maintain consistent documentation and database interfaces.
- Perform final integration and regression testing.

---

## Course Information

- **Course:** SDC435L – NoSQL Databases Lab
- **Institution:** ECPI University
- **Instructor:** Schevon Joseph
- **Project:** GitHub Data Analysis
- **Repository:** <https://github.com/Anonas2638/SDC435L-GitHub-Data-Analysis>
