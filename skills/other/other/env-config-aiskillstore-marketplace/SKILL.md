---
name: env-config
description: |
  Use when setting up environment configuration, loading .env files, or managing
  application settings across environments.
  Triggers for: .env setup, loading environment variables, Pydantic BaseSettings,
  configuration validation, or secret management.
  NOT for: code-specific logic, feature flags, or runtime feature toggles.
---

# Environment Configuration Skill

Expert environment configuration management for Python/FastAPI projects with secure secrets handling and multi-environment support.

## Quick Reference

| Pattern | Usage |
|---------|-------|
| Load .env | `load_dotenv()` at application start |
| Access var | `settings.DB_URL`, `settings.JWT_SECRET` |
| Required var | `Field(..., description="Database URL")` |
| Optional var | `DB_HOST: str = "localhost"` |
| Secret type | `SecretStr` for sensitive values |

## Project Structure

```
project/
├── .env                  # Local development (NOT committed)
├── .env.example          # Template with all required vars (committed)
├── .env.staging          # Staging environment
├── .env.production       # Production environment (managed by infra)
└── config/
    ├── __init__.py
    └── settings.py       # Pydantic BaseSettings
```

## settings.py - Base Configuration

```python
# config/settings.py
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "ERP System"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/v1"

    # Database
    DB_URL: str = Field(
        ...,
        description="PostgreSQL connection URL",
        examples=["postgresql://user:pass@localhost:5432/dbname"],
    )
    DB_POOL_SIZE: int = Field(default=5, ge=1, le=100)

    # JWT Authentication
    JWT_SECRET_KEY: SecretStr = Field(
        ...,
        description="Secret key for JWT signing",
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = Field(default=15, ge=1)

    # Redis (Optional)
    REDIS_URL: str | None = None

    # Logging
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR)$")

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    @property
    def is_production(self) -> bool:
        return not self.DEBUG


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance for application lifecycle."""
    return Settings()
```


## .env.example - Template File

```bash
# .env.example - Copy to .env and fill in values
# DO NOT commit actual secrets!

# Application
APP_NAME="ERP System"
DEBUG=false
API_V1_PREFIX="/v1"

# Database (required)
DB_URL="postgresql://user:password@localhost:5432/erp_db"

# JWT Authentication (required - generate with: openssl rand -hex 32)
JWT_SECRET_KEY="your-secret-key-here-generate-with-openssl-rand-hex-32"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=15

# Redis (optional)
# REDIS_URL="redis://localhost:6379/0"

# Logging
LOG_LEVEL="INFO"

# CORS
CORS_ORIGINS="http://localhost:3000"
```

## .env - Local Development

```bash
# .env - Local development only
# NEVER commit this file to version control

APP_NAME="ERP System"
DEBUG=true
API_V1_PREFIX="/v1"

# Local PostgreSQL
DB_URL="postgresql://postgres:postgres@localhost:5432/erp_dev"

# Generate with: openssl rand -hex 32
JWT_SECRET_KEY="local-dev-secret-key-change-in-production"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=15

# Local Redis (if using)
REDIS_URL="redis://localhost:6379/0"

LOG_LEVEL="DEBUG"

CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

## Usage in Application

### FastAPI Application

```python
# main.py
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()  # Load .env file

from config.settings import get_settings


@asynccontextmanager
async def lifespan(app):
    settings = get_settings()
    print(f"Starting {settings.APP_NAME} in {'DEBUG' if settings.DEBUG else 'PROD'} mode")
    yield
    print("Shutting down...")


app = FastAPI(
    title=get_settings().APP_NAME,
    lifespan=lifespan,
)


# Include routers
from app.routers import fees, students
app.include_router(fees.router, prefix=get_settings().API_V1_PREFIX)
app.include_router(students.router, prefix=get_settings().API_V1_PREFIX)
```

### Database Connection

```python
# database.py
from sqlmodel import create_engine, Session
from config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.DB_URL.get_secret_value() if hasattr(settings.DB_URL, 'get_secret_value') else settings.DB_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=10,
)


def get_session():
    with Session(engine) as session:
        yield session
```

### JWT Configuration

```python
# auth/jwt.py
from datetime import timedelta
from config.settings import get_settings

settings = get_settings()

JWT_SECRET = settings.JWT_SECRET_KEY.get_secret_value()
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_EXPIRATION_MINUTES


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # ... token creation logic
    pass
```

## Multi-Environment Support

### Environment-Specific Configs

```python
# config/settings.py

class Settings(BaseSettings):
    # ... shared settings

    @classmethod
    def from_env(cls, env: str = "development") -> "Settings":
        """Load settings for specific environment."""
        env_file = {
            "development": ".env",
            "staging": ".env.staging",
            "production": ".env.production",
        }.get(env, ".env")

        return cls(_env_file=env_file)
```

### Production Override

```bash
# Production should use environment variables, not .env files
# Set these in your deployment platform (Docker, K8s, Cloud Run, etc.)

export DB_URL="postgresql://prod_user:prod_pass@prod-db.example.com:5432/erp_prod"
export JWT_SECRET_KEY="production-secret-key-from-secrets-manager"
export DEBUG=false
export LOG_LEVEL="WARNING"
```

## Secret Management

### Generate Secrets

```bash
# Generate secure random secret
openssl rand -hex 32  # For JWT_SECRET_KEY

# Generate database password
openssl rand -base64 32
```

### Secret Rotation Script

```python
# scripts/rotate_secret.py
"""Rotate a secret in all environments."""
import os
import re

def rotate_secret(env_file: str, key: str, new_value: str):
    """Replace secret value in .env file."""
    with open(env_file, "r") as f:
        content = f.read()

    # Pattern to match KEY=value
    pattern = f"^{key}=.*$"
    replacement = f"{key}={new_value}"

    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    with open(env_file, "w") as f:
        f.write(new_content)

    print(f"Rotated {key} in {env_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: rotate_secret.py <env_file> <key> <new_value>")
        sys.exit(1)

    rotate_secret(sys.argv[1], sys.argv[2], sys.argv[3])
```

## Quality Checklist

- [ ] **Validation on load**: All required fields have `Field(..., ...)` validation
- [ ] **No leaks in logs**: Use `SecretStr` for sensitive values, never print settings
- [ ] **.env.example committed**: Template shows all required variables
- [ ] **.env.gitignored**: Local development file excluded from version control
- [ ] **Secrets generated**: JWT secrets use `openssl rand -hex 32`
- [ ] **Environment isolation**: Different configs for dev/staging/production
- [ ] **Type safety**: All settings have proper type annotations

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `@jwt-auth` | JWT_SECRET_KEY from settings |
| `@sqlmodel-crud` | DB_URL from settings |
| `@fastapi-app` | All app settings from settings |
| `@db-migration` | Database URL for migrations |
| `@api-route-design` | API prefix, CORS origins |

## Security Best Practices

### DO

- Use `SecretStr` for passwords, API keys, tokens
- Rotate secrets regularly
- Use different secrets per environment
- Store production secrets in secrets manager
- Validate all required settings at startup

### DON'T

- Never commit `.env` files to version control
- Never hardcode secrets in source code
- Never log settings or environment variables
- Never use default/placeholder secrets in production
- Never expose configuration details in error messages

## Startup Validation

```python
# config/validate.py
"""Validate required configuration at startup."""
from pydantic import ValidationError
from config.settings import Settings


def validate_settings() -> bool:
    """Ensure all required settings are configured."""
    try:
        settings = Settings()
        return True
    except ValidationError as e:
        print("Configuration validation failed:")
        for error in e.errors():
            print(f"  - {error['loc'][0]}: {error['msg']}")
        return False


if __name__ == "__main__":
    if not validate_settings():
        exit(1)
```
