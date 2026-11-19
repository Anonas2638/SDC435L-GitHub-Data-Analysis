# SDC435L – GitHub Data Analysis Group Project

## Project Overview

This project is part of the SDC435L NoSQL Databases Lab course at ECPI
University. The goal is to develop a Python application that analyzes GitHub
Archive data using five database technologies over five weeks: Redis, MongoDB,
Cassandra, Neo4j, and SQLite.

Each week, the application will be expanded to demonstrate database
integration, data management, and analysis features.

## Week 1 – Redis Integration

The first week focuses on connecting Python to Redis, importing GitHub Archive
data, performing CRUD operations, and analyzing repository information.

### Features Implemented

#### 1. Redis Database Connection

- Established a connection between Python and Redis.
- Verified the connection using the Redis PING command.

#### 2. GitHub Archive Data Import

- Created `redis_db/import_repositories.py` to read repository information
  from `Sample_Repos.json`.
- Stores repository records as JSON strings using keys beginning with `github:repo:`.
- Successfully imported and tested data from the provided GitHub Archive dataset.
- Limits imports to 1,000 records per execution in the current implementation.

#### 3. Repository Popularity Analysis

- Created `redis_db/repository_popularity.py`.
- Retrieves stored repository information from Redis.
- Sorts repositories by their `watch_count` values.
- Displays the top 10 most popular repositories.
- Previously tested using 277,771 repository records stored in Redis.

#### 4. Repository Management (CRUD)

- Created `redis_db/redis_crud.py`.
- Implements Create, Read, Update, and Delete operations.
- Uses Redis SET with the NX option to prevent duplicate records.
- Uses Redis SET with the XX option to update existing records.
- Allows users to manage repositories through an interactive menu.
- Includes input validation, error handling, and deletion confirmation.
- Maintains consistency with the existing JSON data structure.

#### 5. Repository Owner Analysis

- Created `redis_db/owner_analysis.py`.
- Retrieves repository records using Redis SCAN.
- Extracts repository owners from the `repo_name` field.
- Uses Python's Counter class to aggregate repository counts.
- Displays the top 10 owners by the number of repositories in the imported dataset.

#### 6. Integrated Application

- Created `main.py` as the application's entry point.
- Integrates dataset importing, CRUD operations, repository popularity
  analysis, repository owner analysis, and watch count statistics.
- Provides an interactive command-line interface for accessing application features.
- Handles invalid menu selections and Redis connection errors.

#### 7. Repository Watch Count Statistics

- Created `redis_db/repository_statistics.py`.
- Reuses existing Redis repository retrieval functionality.
- Converts watch counts to integers and skips invalid values.
- Calculates total, average, median, minimum, and maximum watch counts.
- Tested with 1,000 records and integrated into the main menu.

## Technologies and Dependencies

- Python 3 (tested with Python 3.13.15)
- Redis database server
- Redis Python library (8.1.0)
- Ubuntu Linux / ECPI VCASTLE
- macOS
- GitHub for version control
- GitHub Archive dataset

## Project Files

| File | Description |
| --- | --- |
| `main.py` | Main application and navigation menu |
| `redis_db/__init__.py` | Identifies the Redis Python package |
| `redis_db/import_repositories.py` | Imports GitHub Archive data into Redis |
| `redis_db/repository_popularity.py` | Ranks repositories by watch count |
| `redis_db/redis_crud.py` | Implements repository CRUD operations |
| `redis_db/owner_analysis.py` | Ranks repository owners by repository count |
| `redis_db/repository_statistics.py` | Calculates watch count statistics |
| `requirements.txt` | Python package dependencies |
| `Sample_Repos.json` | Source dataset provided through Canvas |
| `.gitignore` | Excludes local datasets and environment files |
| `README.md` | Project documentation |

### Directory Structure

```text
SDC435L-GitHub-Data-Analysis/
├── redis_db/
│   ├── __init__.py
│   ├── import_repositories.py
│   ├── redis_crud.py
│   ├── repository_popularity.py
│   ├── owner_analysis.py
│   └── repository_statistics.py
├── main.py
├── mongo_repository_analysis.py
├── requirements.txt
├── Sample_Repos.json (local dataset)
├── README.md
└── .gitignore
```

The Redis modules are organized into a Python package. The existing Week 2
MongoDB module remains in the project root.

## Redis Data Model

Repository records are stored using the following key format:

```text
github:repo:owner/repository
```

Example JSON value:

```json
{
    "repo_name": "FreeCodeCamp/FreeCodeCamp",
    "watch_count": "90457"
}
```

Repository names serve as unique identifiers. Watch counts are stored as
strings to maintain consistency with the original dataset.

## Setup Instructions

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

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and Start Redis

Ensure Redis is installed and running locally on port 6379.

For Ubuntu:

```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

For macOS using Homebrew:

```bash
brew install redis
brew services start redis
```

Verify the Redis connection:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

### 5. Prepare the Dataset

- Download the GitHub Archive dataset from the SDC435L course in Canvas.
- Extract the downloaded ZIP file.
- Place `Sample_Repos.json` in the project root beside `main.py`, not inside
  `redis_db/`.

The dataset is excluded from GitHub and must be downloaded separately.

### 6. Run the Application

```bash
python main.py
```

## Application Menu

```text
=============================================
         GITHUB DATA ANALYSIS
       SDC435L - Redis Integration
=============================================
1. Import repository data
2. Manage repositories (CRUD)
3. Repository popularity analysis
4. Repository owner analysis
5. Repository watch count statistics
6. Exit
```

Select option 1 to import repository records if the database has not already
been populated.

## Repository Management Menu

```text
1. Create repository
2. Read repository
3. Update repository
4. Delete repository
5. Return to main menu
```

## Running Individual Modules

Run the following commands from the project root using Python's `-m` flag to
execute the packaged modules independently.

Import repository data:

```bash
python -m redis_db.import_repositories
```

Run repository popularity analysis:

```bash
python -m redis_db.repository_popularity
```

Run repository management:

```bash
python -m redis_db.redis_crud
```

Run repository owner analysis:

```bash
python -m redis_db.owner_analysis
```

Run repository watch count statistics:

```bash
python -m redis_db.repository_statistics
```

## Testing

The application was tested using a local Redis server. CRUD operations were
verified before package restructuring. Dataset import, all three analyses,
invalid menu handling, and application exit were verified again afterward.

| Test | Result |
| --- | --- |
| Python-to-Redis connection | Passed |
| Dataset import of 1,000 records | Passed |
| Create repository | Passed |
| Read repository | Passed |
| Update repository | Passed |
| Delete repository | Passed |
| Verify repository deletion | Passed |
| Repository popularity analysis | Passed |
| Repository owner analysis | Passed |
| Repository watch count statistics | Passed |
| Statistical analysis menu integration | Passed |
| Repeated analysis execution | Passed |
| Main menu navigation | Passed |
| CRUD submenu navigation | Passed |
| Invalid menu selection | Passed |
| Application exit | Passed |
| Redis package imports and independent module execution | Passed |
| Dataset import after package relocation | Passed |
| All three analyses after package relocation | Passed |

### Sample Owner Analysis Results

The following results were obtained from the imported sample:

| Rank | Owner | Repository Count |
| --- | --- | --- |
| 1 | google | 22 |
| 2 | facebook | 19 |
| 3 | Ramotion | 8 |
| 4 | gaearon | 7 |
| 5 | reactjs | 7 |

Results may vary depending on the number of repository records imported.

### Sample Watch Count Statistics

| Metric | Result |
| --- | ---: |
| Total repositories | 1,000 |
| Repositories analyzed | 1,000 |
| Total watches | 2,383,125 |
| Average watches | 2,383.12 |
| Median watches | 1,693.00 |
| Minimum watches | 1,083 |
| Maximum watches | 90,457 |

Results reflect the imported sample.

## Team Contributions

### Anosha Naseri

- GitHub repository creation and configuration.
- Python and Redis database integration.
- GitHub Archive dataset import.
- Repository popularity analysis.
- Initial README documentation.
- Initial Week 1 progress report.

### Sherika Fayson

- Redis CRUD operations.
- Interactive repository management menu.
- Repository owner analysis.
- Repository watch count statistical analysis.
- Third analysis feature integration and testing.
- Main application integration.
- Python dependency management.
- CRUD and application integration testing.
- Redis package restructuring and post-refactoring verification.
- README documentation updates.

## Week 1 Development Status

### Completed

- [x] GitHub repository created.
- [x] Instructor invited to the repository.
- [x] Python and Redis connection tested.
- [x] GitHub Archive repository data imported.
- [x] Repository popularity analysis implemented and tested.
- [x] CRUD operations implemented and tested.
- [x] Interactive repository management menu implemented.
- [x] Repository owner analysis implemented and tested.
- [x] Existing features integrated into a single application.
- [x] Individual and integration testing completed.
- [x] Dependencies and documentation updated.
- [x] Third required data analysis feature implemented and tested.
- [x] Third analysis feature integrated into the main application.
- [x] Local functionality and integration testing completed.
- [x] Redis modules reorganized into a Python package.
- [x] Dataset path and package imports updated and verified.

### Remaining Group Requirements

- [ ] Final group verification and merge of the completed Week 1 changes.
- [ ] Consolidate the Week 1 progress report.
- [ ] Prepare the final application ZIP file.
- [ ] Complete the final Week 1 group submission.

## Future Development

| Week | Database | Database Model |
| --- | --- | --- |
| 1 | Redis | Key-value |
| 2 | MongoDB | Document |
| 3 | Cassandra | Wide-column |
| 4 | Neo4j | Graph |
| 5 | SQLite | Relational |

The goal is to create one Python application that demonstrates different
database models and their capabilities for analyzing GitHub Archive data.

## Course Information

**Course:** SDC435L – NoSQL Databases Lab

**Project:** GitHub Data Analysis

**Institution:** ECPI University

## Week 2 – MongoDB Repository Analysis

### New Feature

- `mongo_repository_analysis.py` imports GitHub Archive repository records
  into MongoDB and displays the top 10 repositories ranked by watch count.
- Successfully tested with 400,000 repository records.
- Converts `watch_count` values from strings to integers for accurate sorting.

### Dependencies

- Python 3
- MongoDB Community Server
- PyMongo (`pip install pymongo`)

### Technology Requirements

- Windows 11 or compatible operating system
- Local MongoDB server running on port 27017
- GitHubArchive-Dataset, including `Sample_Repos.json`

### How to Run

1. Install Python 3, MongoDB, and PyMongo.
2. Extract the GitHub Archive dataset.
3. Update the `file_path` variable in `mongo_repository_analysis.py` to match
   the location of `Sample_Repos.json`.
4. Start MongoDB.
5. Run `python mongo_repository_analysis.py`.

### Current Status

The repository watch count analysis has been tested successfully. Group
integration and additional CRUD and analysis features are pending.
