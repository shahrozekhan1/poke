# Pokémon ETL Pipeline
A comprehensive ETL pipeline that fetches Pokémon data from the PokéAPI, processes it, stores it in SQLite, and serves it via a RESTful API with a web interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📘 Project Description
The **Pokémon ETL Pipeline** is a full-stack data engineering project that demonstrates how to build an end-to-end **Extract, Transform, Load (ETL)** system integrated with a **web API** and **interactive frontend**.

It automatically retrieves Pokémon data from the public **[PokéAPI](https://pokeapi.co/)**, cleans and structures it into a **normalized SQLite database**, and exposes it through a **FastAPI RESTful API** and **web interface**.

The project highlights key engineering concepts such as:
- API data extraction and rate-limiting  
- Data normalization and relational schema design  
- ETL orchestration with logging and error handling  
- RESTful API design with automatic documentation  
- Containerization using **Docker** for reproducible deployments  
- Unit testing and modular architecture  

This project is ideal for developers, data engineers, or learners who want to explore **real-world ETL pipelines**, **database design**, and **API integration** using **Python**, **FastAPI**, and **Docker**.

---

> 📝 **Note:**  
> The project includes **comprehensive logging** across all ETL steps and the FastAPI backend.  
> Logs capture detailed information about extraction, transformation, loading, and API events to assist in debugging and monitoring.

---

## Features
- **Complete ETL Pipeline** — Extract → Transform → Load with full logging and error handling  
- **FastAPI Backend** — RESTful API with automatic docs and modular routing  
- **Modern Web Interface** — Clean, browser-based UI for viewing and filtering Pokémon data  
- **Advanced Filters** — Filter by type, HP, attack, and evolution status  
- **SQLite Storage** — Lightweight, normalized relational database  
- **Dockerized Deployment** — Easily containerized and portable  
- **Tested Codebase** — Unit tests covering all core modules  

---

## 🧩 Project Structure
```

POKE/
├── app.py
├── main.py
├── constants.py
├── index.html
│
├── crud/
├── data_processing/
│   ├── extract.py
│   ├── load.py
│   └── transform.py
│
├── db/
│   └── pokemon_database.db
│
├── models/
│   ├── files.py
│   └── history.py
│
├── routers/
├── schemas/
│   └── etl.py
│
├── tests/
│   ├── **init**.py
│   ├── test_extract.py
│   ├── test_load.py
│   ├── test_main.py
│   └── test_transform.py
│
├── uploads/
│
├── dockerfile
├── .gitignore
├── .dockerignore
├── requirements.txt
├── requirements_test.txt
├── Readme.md
└── testing/
└── testing.ipynb

````

---

## ⚙️ Prerequisites
- Python **3.10+**
- `pip` (Python package manager)
- Internet connection (for PokéAPI access)
- Optional: **Docker** (for containerized deployment)

---

## 🚀 Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pokemon-etl-pipeline.git
cd pokemon-etl-pipeline/POKE
````

### 2. Create and Activate Virtual Environment

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

---

## 🧱 Docker Containerization

This project is fully containerized for easy deployment using **Docker**.

### 🐳 Build Docker Image

```bash
docker build -t backend-app:latest .
```

### 🚀 Run Docker Container

```bash
docker run \
  --name backend-app \
  -p 8000:8000 \
  -v "$(pwd)":/app \
  backend-app:latest
```

### 🌐 Access the App

* Web Interface → [http://localhost:8000](http://localhost:8000)
* API Docs → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing

```bash
python3 -m unittest discover -v
```

If you maintain separate test dependencies:

```bash
pip install -r requirements_test.txt
python3 -m unittest discover -v
```

---

## ⚙️ Configuration

Edit `constants.py` to modify pipeline settings:

```python
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
API_DELAY = 0.5
DATABASE_FILE = "db/pokemon_database.db"
POKEMON_TO_FETCH = 12
```

---

## 🧩 Design Choices (ETL, Data Mapping, Database Schema & Framework Choice )

### 1. **ETL Workflow**

The pipeline follows a clean separation of concerns:

* **Extract (`extract.py`)** — Retrieves Pokémon data via the PokéAPI with rate-limiting to prevent throttling. Each Pokémon’s details and evolution chain are fetched independently for modularity.
* **Transform (`transform.py`)** — Converts nested JSON from PokéAPI into structured data that fits a relational model. Complex lists (types, abilities, stats) are flattened while preserving relationships.
* **Load (`load.py`)** — Performs idempotent inserts/updates into the SQLite database, ensuring repeated runs do not cause data duplication.

### 2. **Data Transformation**

* The raw PokéAPI response contains deeply nested structures (types, abilities, stats, evolution chains).
* To support efficient querying and filtering, the transformation step:

  * Normalizes nested lists into lookup tables (e.g., `types`, `abilities`, `stats`).
  * Links them through junction tables (`pokemon_types`, `pokemon_abilities`, `pokemon_stats`).
  * Ensures consistent naming and key mappings for downstream analytics.
* This design allows powerful queries like:

```sql
SELECT 
    p.name AS pokemon_name,
    GROUP_CONCAT(pt.type_name, ', ') AS types,
    MAX(CASE WHEN ps.stat_name = 'hp' THEN ps.base_stat END) AS hp,
    MAX(CASE WHEN ps.stat_name = 'attack' THEN ps.base_stat END) AS attack
FROM 
    pokemon p
JOIN 
    pokemon_types pt ON p.id = pt.pokemon_id
JOIN 
    pokemon_stats ps ON p.id = ps.pokemon_id
JOIN 
    stats s ON ps.stat_name = s.name
GROUP BY 
    p.name
HAVING 
    hp > 50 AND attack > 60;
```

### 3. **Database Schema Design**

* **Normalization Level:** 3NF — Each entity (Pokémon, type, ability, stat, evolution) is stored in its own table, avoiding redundancy.
* **Relationship Mapping:**

  * **One-to-Many:** Evolution chains → Pokémon
  * **Many-to-Many:** Pokémon ↔ Types / Abilities / Stats
* **Advantages:**

  * Improved data consistency and query performance
  * Easier updates without redundancy
  * Clean joins for data exploration or future analytics

### 4. **Idempotency & Error Handling**

* Each ETL stage is **idempotent** — re-running it will not duplicate or corrupt data.
* Logging captures all critical events and exceptions for debugging.
* Transaction management ensures partial failures do not leave the database in an inconsistent state.

### 5. **Why SQLite**

* Lightweight, serverless, and perfect for local and demo-scale ETL pipelines.
* Can easily be swapped with PostgreSQL or MySQL by adjusting connection settings in `load.py`.

### 6. **Framework Choice — FastAPI**

**FastAPI** was chosen as the backend framework for several important reasons:

#### 🧠 Why FastAPI

* **Modern and high-performance:** Built on top of **ASGI** and **Starlette**, FastAPI supports asynchronous execution, making it ideal for ETL and API-heavy workloads.
* **Automatic Documentation:** Generates **OpenAPI (Swagger)** and **ReDoc** documentation automatically — accessible at `/docs` and `/redoc`.
* **Validation & Serialization:** Built-in **Pydantic models** ensure type-safe request/response validation, reducing runtime errors.
* **Ease of Integration:** Works seamlessly with **SQLite**, **SQLAlchemy**, and other libraries; easy to containerize with **Docker**.
* **Developer Productivity:** Extremely concise syntax and auto-generated docs make development and debugging faster.

#### 🚀 Benefits in This Project

* Used to expose RESTful endpoints like `/pokemon`, `/pokemon/filter`, and `/etl/run-pipeline`
* Allows filtering Pokémon data directly via query parameters (type, hp, attack, evolution status)
* Returns clean JSON responses and descriptive error messages
* Enables future scalability (e.g., migrating to PostgreSQL or deploying on Kubernetes)

---

## 🏗️ Architecture

```
EXTRACT → TRANSFORM → LOAD
```

1. **Extract** — Retrieve Pokémon data from PokéAPI
2. **Transform** — Normalize and clean the data
3. **Load** — Store structured data in SQLite

Core modules:

* `data_processing/extract.py` — Handles API requests with rate limits
* `data_processing/transform.py` — Normalizes nested JSON structures
* `data_processing/load.py` — Manages database transactions
* `app.py` — FastAPI application
* `main.py` — Orchestrates ETL pipeline execution

---

## 🧠 Assumptions

During the design and development of this ETL pipeline, a few key assumptions were made to balance **complexity**, **performance**, and **clarity** of the database schema.

1. **Simplified Relational Model**
   The database schema was initially designed with fewer tables to keep the structure lightweight and easily understandable.
   The assumption was that only the **most relevant** Pokémon data (name, stats, types, abilities, evolution info) would be required for analytics and API usage.

2. **Incremental Refinement**
   As the ETL logic evolved and more nested JSON structures were discovered in the PokéAPI, the schema was amended to introduce **normalized relationships** — such as `pokemon_types`, `pokemon_abilities`, and `pokemon_stats`.
   This was a deliberate trade-off: keeping the schema simple at first, then expanding it only when necessary for data integrity and scalability.

3. **PokéAPI Data Consistency**
   It was assumed that the PokéAPI data is **complete and consistent**, meaning no Pokémon entries would be missing required fields (types, stats, abilities).
   The ETL logic still includes validation and logging in case the API returns incomplete or malformed records.

4. **Limited Dataset Scope**
   The ETL currently fetches a **subset of Pokémon** (e.g., first 12) for demonstration purposes.
   This assumption makes testing and iteration faster while retaining functional completeness.
   The pipeline can easily scale to process all Pokémon if needed.

5. **Local Environment Execution**
   The project assumes a **local or Dockerized setup** where SQLite and FastAPI are deployed on the same container.
   This simplifies configuration and removes the need for separate database hosting or networking layers.

---

## 🧩 Testing Strategy

Testing was implemented using Python’s built-in `unittest` framework to ensure each layer of the project is reliable and behaves as expected.

### ✅ Unit Tests

* **`test_extract.py`** — Validates PokéAPI response structure and rate limiting
* **`test_transform.py`** — Checks that data normalization and mapping produce valid relational records
* **`test_load.py`** — Ensures database inserts, updates, and transactions behave correctly
* **`test_main.py`** — Confirms that the full ETL pipeline runs end-to-end without data loss

### 🧪 Running Tests

```bash
python3 -m unittest discover -v
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature/new-feature`)
5. Submit a Pull Request

---

## 🤖 Potential Improvements & Future Enhancements

### 1. **AI-Powered Data Analysis**

Integrating **AI and Machine Learning** models could unlock new capabilities such as:

* **Pokémon Stat Prediction**
* **Type Effectiveness Modeling**
* **Evolution Chain Prediction**
* **AI-Powered Recommendations**

### 2. **AI-Assisted Data Cleaning & Enrichment**

* Use **LLMs** or rule-based AI pipelines to automatically validate and enrich API data.

### 3. **Predictive Analytics Dashboard**

* Integrate an **AI insights dashboard** where users can visualize stats and run AI-based predictions.

### 4. **Data Pipeline Improvements**

* Add **Prefect** or **Airflow** for ETL orchestration
* Implement **async ETL execution**
* Introduce **data versioning**
* Include **AI-powered anomaly detection**

### 5. **Scalability & Infrastructure**

* Use **Docker Compose** or **Kubernetes**
* Move to **PostgreSQL** or **AWS RDS**
* Implement **Redis caching**
* Implement **GraphQL** API layer

### 6. **Developer Experience & Automation**

* GitHub Actions CI/CD
* AI code review tools
* AI-assisted documentation generation

### 7. **User-Facing Enhancements**

* Interactive Web UI (React + FastAPI)
* Search & Recommendation Engine
* Gamification Layer

### 8. **AI-Powered Monitoring & Maintenance**

* Anomaly detection in logs
* AI-based ETL run reports
* Natural language query support in API

---
**Made with ❤️ for Pokémon fans and data engineers**
*Powered by [PokéAPI](https://pokeapi.co/) • [FastAPI](https://fastapi.tiangolo.com/) • [SQLite](https://www.sqlite.org/) • [Docker](https://www.docker.com/)*
