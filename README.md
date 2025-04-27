# Golden Raspberry Awards API

This project provides a RESTful API for accessing and analyzing data from the Golden Raspberry Awards (also known as the Razzies), which honor the worst in film each year.

## Features
- **List all movies** in the database
- **Retrieve movie details** by ID
- **Analyze producer win intervals**: Find the minimum and maximum intervals between wins for producers

## Tech Stack
- **Python**
- **FastAPI** for building the REST API
- **SQLite** (in-memory) for data storage
- **CSV** file import for initial data## Specifications

The `specs/` directory contains additional resources for understanding and integrating with the Golden Raspberry Awards API:

- **Especificação Backend.pdf**:  
  This document provides a detailed backend specification, including requirements, data models, and API contract details.

- **example.json**:  
  An example JSON file illustrating the expected data format for requests or responses.

## Project Structure
```
data/                 # Contains the movie data to load into the database
src/                  # Main application
services/             # Business logic and analysis functions
database/             # Database connection and data loading logic
requirements/         # Python dependency libraries
tests/                # Integration tests
logs/                 # Log files
```

## Setup & Usage
1. **Install dependencies**:
   ```bash
   pip install -r requirements/base.txt
   ```

2. **Run the API**:
   ```bash
   uvicorn src.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000/`.

3. **Endpoints**:
   - `GET /movies` — List all movies
   - `GET /movies/{movie_id}` — Get details for a specific movie
   - `GET /movie/winners` — Get producers with min/max win intervals

4. **Testing**:
   Run integration tests with:
   ```bash
   pytest tests/
   ```

## Alternate Setup & Usage (with Make)

You can use the provided `Makefile` to simplify common tasks:

1. **Install dependencies**:
   ```bash
   make install
   ```

2. **Run the API**:
   ```bash
   make run
   ```
   The API will be available at `http://127.0.0.1:8000/`.

3. **Run tests**:
   ```bash
   make test
   ```

4. **To see available commands**:
   ```bash
   make help
   ```

## Data Source
- The movie data is loaded from a `csv` file in the `data` folder on startup.

## Logging
- Logs are written to `logs/golden_raspberry_app.log`.

## API Documentation

- **Swagger UI:**  
  Interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) when the server is running.

- **ReDoc:**  
  Alternative documentation is available at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Both interfaces allow you to explore and test API endpoints directly from your browser.
