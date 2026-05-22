# Skill: Neon DB Setup

**Purpose**: Automate Neon PostgreSQL database connection setup for FastAPI + SQLModel projects.

## Trigger Conditions

Invoke this skill when:
- Setting up a new FastAPI backend with database
- User mentions "Neon", "PostgreSQL", or "database connection"
- Phase II implementation requires DB setup

## Capabilities

### 1. Generate Database Configuration

Creates `backend/app/database.py`:

```python
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# Async engine for Neon PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,  # Handles Neon cold starts
    pool_size=5,
    max_overflow=10,
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### 2. Generate Config Settings

Creates/updates `backend/app/config.py`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    CORS_ORIGINS: str = "http://localhost:3000"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
```

### 3. Generate .env.example

```env
# Neon PostgreSQL Connection
# Format: postgresql+asyncpg://user:password@host/database?sslmode=require
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# Better Auth Secret (min 32 chars, must match frontend)
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters

# CORS (comma-separated for multiple origins)
CORS_ORIGINS=http://localhost:3000

# Debug mode
DEBUG=true
```

### 4. Neon-Specific Optimizations

- SSL mode: `require` (mandatory)
- Connection pooling with `pool_pre_ping=True` for cold start handling
- Proper async session management
- Connection timeout configuration

## Usage

```
/neon-db-setup
```

Or automatically triggered when creating backend structure.

## Dependencies

Add to `requirements.txt`:
```
sqlmodel>=0.0.16
asyncpg>=0.29.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
```

## Error Handling

If connection fails, check:
1. Connection string format (must use `postgresql+asyncpg://`)
2. SSL mode is `require`
3. IP allowlist in Neon dashboard
4. Credentials are correct
