# International-Configuration-Management-API

## Overview
This project is a FastAPI-based application for managing configuration requirements for onboarding organizations from various countries. It supports CRUD operations (Create, Read, Update, Delete) to handle different onboarding requirements for each country.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/International-Configuration-Management-API.git
    cd International-Configuration-Management-API
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file with your database connection details:
    ```env
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/config_db
    ```

5. Apply database migrations:
    ```bash
    alembic upgrade head
    ```

6. Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload
    ```

### Testing

To run the tests, use pytest:
```bash
pytest
