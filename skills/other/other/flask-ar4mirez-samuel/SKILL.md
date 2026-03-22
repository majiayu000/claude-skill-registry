---
name: flask
description: |
  Flask framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Flask projects, or when the user mentions Flask.
  Provides blueprint patterns, extensions, Jinja2 templates, and REST API guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: python
  extensions: ".py"
---

# Flask Framework Guide

> Applies to: Flask 3.0+, REST APIs, Microservices, Web Applications
> Language Guide: @.claude/skills/python-guide/SKILL.md

## Overview

Flask is a lightweight WSGI web framework providing the basics for building web applications while allowing flexibility in choosing components.

**Use Flask when:**
- Building microservices or small-to-medium APIs
- You want flexibility to choose your own ORM, auth, etc.
- Rapid prototyping is needed
- You prefer explicit over implicit behavior

**Consider alternatives when:**
- You need async support (use FastAPI or Quart)
- You want batteries-included (use Django)
- High performance async is critical (use FastAPI)

## Guardrails

### Flask-Specific Guidelines

- Use the application factory pattern (never use global app instances)
- Use blueprints for modular routing
- Use Flask extensions appropriately (init in extensions.py)
- Configure via environment variables with class-based config
- Use Marshmallow for validation/serialization
- Implement proper error handlers for all error types
- Use Flask-Migrate for database migrations
- Use Flask-JWT-Extended for authentication

### Security Guidelines

- Never store plain passwords (use werkzeug.security)
- Use environment variables for all secrets
- Implement proper authentication and authorization
- Validate all user input with Marshmallow schemas
- Use HTTPS in production
- Set secure cookie options (HTTPONLY, SECURE, SAMESITE)
- Sanitize all database queries via SQLAlchemy ORM
- Configure CORS restrictively in production

### Testing Guidelines

- Use pytest with Flask test client
- Use fixtures for test data and app context
- Test both success and error cases for every endpoint
- Mock external services (never call real APIs in tests)
- Use a separate test database
- Coverage target: >80% for business logic

## Project Structure

```
myproject/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration classes
│   ├── extensions.py         # Flask extensions (single init point)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py           # Base model class with mixins
│   │   └── user.py
│   ├── api/
│   │   ├── __init__.py       # API blueprint registration
│   │   ├── users.py          # User endpoints
│   │   └── auth.py           # Auth endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py   # Business logic (no Flask imports)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py           # Marshmallow schemas
│   └── utils/
│       ├── __init__.py
│       ├── errors.py         # Custom exceptions and handlers
│       └── decorators.py     # Auth and role decorators
├── migrations/               # Alembic migrations (via Flask-Migrate)
├── tests/
│   ├── conftest.py           # Fixtures: app, client, db_session
│   ├── test_api/
│   │   └── test_users.py
│   └── test_services/
│       └── test_user_service.py
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── run.py                    # Entry point
```

Key conventions:
- `app/__init__.py` contains `create_app()` factory only
- `app/extensions.py` centralizes all extension instances
- `app/services/` holds business logic, no Flask imports
- `app/schemas/` holds Marshmallow validation/serialization
- `app/utils/errors.py` defines custom exceptions and handlers

## Application Factory

Always use the factory pattern. Never use a global `app = Flask(__name__)`.

```python
"""Flask application factory."""
from flask import Flask

from app.config import config
from app.extensions import db, migrate, ma, jwt, cors


def create_app(config_name: str = "development") -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_commands(app)

    return app


def register_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")


def register_error_handlers(app: Flask) -> None:
    """Register error handlers."""
    from app.utils.errors import (
        handle_app_error,
        handle_validation_error,
        handle_not_found,
        handle_internal_error,
    )
    from marshmallow import ValidationError

    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(500, handle_internal_error)


def register_commands(app: Flask) -> None:
    """Register CLI commands."""
    from app.commands import seed_db
    app.cli.add_command(seed_db)
```

## Blueprints

Organize routes into blueprints. Register them in the factory.

```python
"""API blueprint registration."""
from flask import Blueprint

api_bp = Blueprint("api", __name__)

# Import routes to register them
from app.api import users, auth  # noqa: F401, E402
```

Blueprint endpoints follow REST conventions:

| Method | Route | Handler | Description |
|--------|-------|---------|-------------|
| GET | `/resources` | `get_resources()` | List with pagination |
| GET | `/resources/<id>` | `get_resource(id)` | Get single resource |
| POST | `/resources` | `create_resource()` | Create resource |
| PATCH | `/resources/<id>` | `update_resource(id)` | Partial update |
| DELETE | `/resources/<id>` | `delete_resource(id)` | Delete resource |

## Configuration

Use class-based configuration with environment variable overrides.

```python
"""Application configuration."""
import os
from datetime import timedelta
from typing import Type


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/myapp_dev"
    )
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/myapp_test"
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


config: dict[str, Type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
```

## Extensions

Centralize all Flask extension instances in a single file.

```python
"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()
```

Common extensions and their purposes:

| Extension | Purpose |
|-----------|---------|
| Flask-SQLAlchemy | ORM and database integration |
| Flask-Migrate | Alembic database migrations |
| Flask-Marshmallow | Serialization and validation |
| Flask-JWT-Extended | JWT authentication |
| Flask-CORS | Cross-origin resource sharing |
| Flask-Limiter | Rate limiting |
| Flask-Caching | Response and data caching |
| Flask-Mail | Email sending |

## Error Handling

Define a custom exception hierarchy and register handlers.

```python
"""Custom exceptions and error handlers."""
from flask import jsonify


class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status_code=409)


def handle_validation_error(error):
    return jsonify({"error": "Validation error", "details": error.messages}), 400


def handle_app_error(error: AppError):
    return jsonify({"error": error.message}), error.status_code


def handle_not_found(error):
    return jsonify({"error": "Not found"}), 404


def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

## Jinja2 Templates

When building server-rendered pages (not just APIs):

- Templates live in `app/templates/` with a `base.html` layout
- Use template inheritance: `{% extends "base.html" %}`
- Use `{% block content %}` for page-specific content
- Escape user content automatically (Jinja2 autoescape is on by default)
- Use `url_for()` for all URLs in templates
- Keep logic out of templates; use filters and context processors

```html
{# app/templates/base.html #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My App{% endblock %}</title>
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}
    {% block content %}{% endblock %}
</body>
</html>
```

## CLI Commands

Register custom CLI commands via Click.

```python
"""Custom CLI commands."""
import click
from flask.cli import with_appcontext
from app.extensions import db


@click.command("seed-db")
@with_appcontext
def seed_db():
    """Seed database with initial data."""
    # Create initial records
    db.session.commit()
    click.echo("Database seeded.")
```

## Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed database
flask seed-db

# Run development server
flask run

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"

# Run tests
pytest
pytest -v --cov=app --cov-report=html

# Lint and format
black .
isort .
ruff check .
mypy app/
```

## Dependencies

### requirements.txt
```
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.0
Flask-Migrate>=4.0.0
Flask-Marshmallow>=0.15.0
Flask-JWT-Extended>=4.6.0
Flask-CORS>=4.0.0
marshmallow-sqlalchemy>=0.29.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
gunicorn>=21.0.0
```

### requirements-dev.txt
```
-r requirements.txt
pytest>=7.4.0
pytest-flask>=1.2.0
pytest-cov>=4.1.0
black>=23.0.0
isort>=5.12.0
mypy>=1.5.0
ruff>=0.1.0
```

## Advanced Topics

For detailed code examples and advanced patterns, see:

- [references/patterns.md](references/patterns.md) -- Models, schemas, services, API endpoints, authentication, decorators, testing, and deployment patterns

## External References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
