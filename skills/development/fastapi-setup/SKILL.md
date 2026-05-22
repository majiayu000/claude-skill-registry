---
name: fastapi-setup
description: Initialize FastAPI backend projects with UV package manager, configure project structure, install dependencies, and set up basic FastAPI application. Use when setting up a new FastAPI backend or initializing the backend directory for Phase 2.
allowed-tools: Bash, Write, Read, Glob
---

# FastAPI Project Setup

Quick reference for initializing FastAPI backend projects with modern tooling (UV, SQLModel, pytest).

## Quick Start

### 1. Initialize Backend with UV

```bash
cd backend

# Initialize Python project with UV
uv init --name backend --python 3.13

# Create project structure
mkdir -p src/models src/routers src/services src/middleware src/schemas src/utils tests alembic

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/routers/__init__.py
touch src/services/__init__.py
touch src/middleware/__init__.py
touch src/schemas/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

### 2. Install Dependencies

```bash
# Core dependencies
uv add fastapi[all]
uv add sqlmodel
uv add psycopg2-binary
uv add python-jose[cryptography]
uv add passlib[bcrypt]
uv add python-dotenv
uv add alembic

# Development dependencies
uv add --dev pytest
uv add --dev pytest-cov
uv add --dev httpx
uv add --dev pytest-asyncio
```

### 3. Create Basic FastAPI App

Create `src/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Todo API",
    description="RESTful API for Todo Web Application - Phase 2",
    version="1.0.0"
)

# CORS configuration
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Todo API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 4. Create Configuration

Create `src/config.py`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

### 5. Create Environment Variables Template

Create `.env.example`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here-min-32-characters

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

Create actual `.env` file:
```bash
cp .env.example .env
# Edit .env with actual values
```

### 6. Set Up Database Connection

Create `src/database.py`:

```python
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool
from src.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    poolclass=NullPool,  # Let Neon handle pooling
    connect_args={
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
)

def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI dependency for database sessions"""
    with Session(engine) as session:
        yield session
```

### 7. Initialize Alembic for Migrations

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini - comment out the sqlalchemy.url line
# It will be set from environment variable

# Edit alembic/env.py
```

Update `alembic/env.py`:

```python
from logging.config import fileConfig
from sqlmodel import SQLModel
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all models so Alembic can detect them
from src.models.task import Task  # Import as you create models

# Alembic Config object
config = context.config

# Set DATABASE_URL from environment
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = SQLModel.metadata

# ... rest of env.py (keep default functions)
```

### 8. Create Basic Test Setup

Create `tests/conftest.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.main import app
from src.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

Create `tests/test_main.py`:

```python
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### 9. Create pyproject.toml

Create or update `pyproject.toml`:

```toml
[project]
name = "backend"
version = "1.0.0"
description = "Todo API Backend - Phase 2"
requires-python = ">=3.13"
dependencies = [
    "fastapi[all]>=0.115.0",
    "sqlmodel>=0.0.24",
    "psycopg2-binary>=2.9.9",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-dotenv>=1.0.0",
    "alembic>=1.13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",
    "pytest-asyncio>=0.23.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=term-missing"
```

### 10. Test the Setup

```bash
# Run the FastAPI server
cd backend
uv run uvicorn src.main:app --reload --port 8000

# In another terminal, run tests
uv run pytest

# Check code coverage
uv run pytest --cov=src --cov-report=html
```

## Verification Checklist

After setup, verify:
- [ ] `uv run uvicorn src.main:app --reload` starts successfully
- [ ] http://localhost:8000 returns JSON response
- [ ] http://localhost:8000/docs shows Swagger UI
- [ ] http://localhost:8000/health returns healthy status
- [ ] `uv run pytest` runs and passes
- [ ] `.env` file exists and has DATABASE_URL
- [ ] All __init__.py files created
- [ ] Alembic initialized successfully

## Next Steps

After basic setup:
1. Create database models in `src/models/`
2. Create API routers in `src/routers/`
3. Set up JWT authentication middleware
4. Create first Alembic migration
5. Write comprehensive tests

## Troubleshooting

**UV not found**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Import errors**:
- Ensure all __init__.py files exist
- Check PYTHONPATH includes src directory
- Use `uv run python` instead of just `python`

**Database connection errors**:
- Verify DATABASE_URL in .env
- Check Neon database is running
- Test connection with psql

## References

- FastAPI: https://fastapi.tiangolo.com/
- UV: https://docs.astral.sh/uv/
- SQLModel: https://sqlmodel.tiangolo.com/
- Alembic: https://alembic.sqlalchemy.org/
