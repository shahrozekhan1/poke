# Pokémon ETL Pipeline

A comprehensive ETL pipeline that fetches Pokémon data from the PokéAPI, processes it, stores it in SQLite, and serves it via a RESTful API with a web interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Complete ETL Pipeline** - Extract → Transform → Load with full logging and error handling
- **Modern Web UI** - Clean interface for browsing and filtering Pokémon data
- **Advanced Filters** - Filter by type, HP, attack, and evolution status
- **FastAPI Backend** - RESTful API with automatic documentation and rate limiting
- **Normalized Database** - Properly structured SQLite database with referential integrity
- **Idempotent Operations** - Run the pipeline multiple times safely without data duplication

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
pokemon-etl-pipeline/
├── app.py                      # FastAPI application & endpoints
├── main.py                     # ETL pipeline orchestration
├── constants.py                # Configuration constants
├── index.html                  # Frontend UI
├── data_processing/
│   ├── extract.py             # API data extraction
│   ├── transform.py           # Data transformation logic
│   └── load.py                # Database operations
├── db/
│   └── pokemon_database.db    # SQLite database (generated)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Prerequisites

- Python 3.10+ (recommended 3.11 or 3.12)
- `pip` (Python package manager)
- Internet connection (for PokéAPI access)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pokemon-etl-pipeline.git
cd pokemon-etl-pipeline
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Database Directory

```bash
mkdir -p db
```

## Usage

### Running the ETL Pipeline

```bash
python3 main.py
```

This will:
- Fetch data for the first 12 Pokémon from PokéAPI
- Transform and normalize the data
- Load it into SQLite database
- Display a progress bar during execution

### Running the Web Application

```bash
uvicorn app:app --reload
```

Access the application at:
- **Web Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

## Database Schema

### Core Tables

- **pokemon** - Main Pokémon information (id, name, is_evolved)
- **types** - Pokémon types lookup table
- **abilities** - Pokémon abilities lookup table
- **stats** - Pokémon stats lookup table

### Junction Tables

- **pokemon_types** - Links Pokémon to their types
- **pokemon_abilities** - Links Pokémon to their abilities
- **pokemon_stats** - Links Pokémon to their stat values

### Evolution Tables

- **evolution_chains** - Stores evolution chain information
- **evolution_links** - Links Pokémon in evolution chains

## API Endpoints

### ETL Operations

```
POST /etl/run-pipeline
```
Triggers the ETL pipeline to fetch and process Pokémon data.

### Pokémon Data

```
GET /pokemon
```
Returns a list of all Pokémon names in the database.

```
GET /pokemon/{pokemon_id}
```
Returns detailed information for a specific Pokémon.

```
GET /pokemon/filter?type_name=water&hp_min=50&hp_max=100
```
Returns filtered Pokémon based on query parameters:
- `type_name` - Filter by type (e.g., fire, water, grass)
- `hp_min` / `hp_max` - Filter by HP range
- `attack_min` / `attack_max` - Filter by attack range
- `is_evolved` - Filter by evolution status (true/false)

## Configuration

Edit `constants.py` to customize the pipeline:

```python
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
API_DELAY = 0.5                              # Delay between API calls (seconds)
DATABASE_FILE = "db/pokemon_database.db"     # SQLite database path
POKEMON_TO_FETCH = 12                        # Number of Pokémon to fetch
```

## Architecture

The pipeline follows a standard ETL architecture:

```
EXTRACT → TRANSFORM → LOAD
```

1. **Extract** - Fetch data from PokéAPI
2. **Transform** - Normalize and structure the data
3. **Load** - Store in SQLite database with proper relationships

### Key Components

- **data_processing/extract.py** - Handles API requests with rate limiting
- **data_processing/transform.py** - Normalizes nested JSON structures
- **data_processing/load.py** - Manages database operations and transactions
- **app.py** - FastAPI server with endpoints and CORS configuration
- **main.py** - Pipeline orchestration and progress tracking

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for Pokémon fans and data engineers**

*Powered by [PokéAPI](https://pokeapi.co/) • [FastAPI](https://fastapi.tiangolo.com/) • [SQLite](https://www.sqlite.org/)*
