---
name: example-framework-skill
description: Example of a properly self-contained skill following all best practices
category: framework
toolchain: python
tags: [self-contained, example, template, best-practice]
version: 1.0.0
author: claude-mpm-skills
updated: 2025-11-30
---

# Example Framework Skill

A complete example demonstrating proper self-containment patterns for Claude Code skills.

**When to Use**: Building applications with Example Framework - includes setup, patterns, testing, and deployment.

---

## Overview

This skill demonstrates the **correct approach** to self-contained skill development:

✅ **Self-Contained**: All essential content inlined - works standalone
✅ **No Dependencies**: No relative paths to other skills
✅ **Complete Examples**: Working code, not fragments
✅ **Graceful Degradation**: Notes optional enhancements without requiring them
✅ **Flat Deployment Ready**: Works in any directory structure

---

## Quick Start

### Installation

```bash
# Install framework
pip install example-framework

# Create new project
example-framework init my-project
cd my-project

# Install dependencies
pip install -r requirements.txt

# Run development server
example-framework dev
```

### Minimal Example (Self-Contained)

```python
"""
Minimal Example Framework application.
Self-contained - no external skill dependencies.
"""
from example_framework import App, route

app = App()

@route("/")
def home():
    """Homepage route."""
    return {"message": "Hello, World!"}

@route("/users/{user_id}")
def get_user(user_id: int):
    """Get user by ID."""
    return {
        "id": user_id,
        "username": f"user_{user_id}"
    }

if __name__ == "__main__":
    # Development server
    app.run(host="0.0.0.0", port=8000, debug=True)
```

**Run it:**
```bash
python app.py
# Visit: http://localhost:8000
```

---

## Core Patterns

### 1. Application Setup (Self-Contained)

**Complete setup pattern** - no external dependencies:

```python
from example_framework import App, Config
from example_framework.middleware import CORSMiddleware, LoggingMiddleware

# Configuration
config = Config(
    DEBUG=True,
    SECRET_KEY="your-secret-key-here",
    DATABASE_URL="sqlite:///./app.db"
)

# Application instance
app = App(config=config)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(LoggingMiddleware)

# Health check endpoint
@app.route("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

### 2. Database Integration (Self-Contained)

**Essential database pattern** - inlined for self-containment:

```python
from example_framework import Database
from contextlib import contextmanager

# Database configuration
db = Database("sqlite:///./app.db")

@contextmanager
def get_db_session():
    """
    Database session context manager.

    Usage:
        with get_db_session() as session:
            users = session.query(User).all()
    """
    session = db.create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Model example
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# CRUD operations
@app.route("/users", methods=["POST"])
def create_user(data):
    """Create new user."""
    with get_db_session() as session:
        user = User(
            username=data["username"],
            email=data["email"]
        )
        session.add(user)
        return user.to_dict(), 201

@app.route("/users/{user_id}")
def get_user(user_id: int):
    """Get user by ID."""
    with get_db_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict()
```

### 3. Testing Pattern (Self-Contained)

**Essential testing patterns** - inlined from testing best practices:

```python
"""
Test suite for Example Framework application.
Self-contained testing patterns - no external skill dependencies.
"""
import pytest
from example_framework.testing import TestClient

# Test client fixture
@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

# Database fixture
@pytest.fixture
def db_session():
    """Create test database session."""
    db.create_all()
    session = db.create_session()
    yield session
    session.close()
    db.drop_all()

# Test examples
def test_home_route(client):
    """Test homepage returns correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_user(client, db_session):
    """Test user creation."""
    response = client.post("/users", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_user(client, db_session):
    """Test get user by ID."""
    # Create user
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    # Get user
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_user_not_found(client):
    """Test 404 for nonexistent user."""
    response = client.get("/users/999")
    assert response.status_code == 404
```

**Run tests:**
```bash
pytest tests/
```

---

## Error Handling

### Standard Error Handler Pattern (Self-Contained)

```python
from example_framework import HTTPException

@app.error_handler(404)
def not_found_handler(error):
    """Handle 404 errors."""
    return {
        "error": "Not Found",
        "message": str(error)
    }, 404

@app.error_handler(500)
def server_error_handler(error):
    """Handle 500 errors."""
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }, 500

@app.error_handler(HTTPException)
def http_exception_handler(error):
    """Handle HTTP exceptions."""
    return {
        "error": error.name,
        "message": error.description
    }, error.status_code

# Custom validation error
class ValidationError(Exception):
    """Validation error."""
    pass

@app.error_handler(ValidationError)
def validation_error_handler(error):
    """Handle validation errors."""
    return {
        "error": "Validation Error",
        "message": str(error)
    }, 400
```

---

## Best Practices

### 1. Configuration Management

```python
# environment-based configuration
import os
from example_framework import Config

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "sqlite:///./dev.db"

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")

# Load config based on environment
env = os.getenv("ENV", "development")
config = DevelopmentConfig() if env == "development" else ProductionConfig()

app = App(config=config)
```

### 2. Dependency Injection

```python
# Dependency injection pattern
from example_framework import Depends

def get_current_user(token: str = Depends("Authorization")):
    """Get current user from token."""
    # Token validation logic
    user_id = validate_token(token)
    return User.query.get(user_id)

@app.route("/profile")
def get_profile(user: User = Depends(get_current_user)):
    """Get current user profile."""
    return user.to_dict()
```

### 3. Request Validation

```python
from example_framework import validate_request

# Request schema
user_schema = {
    "username": {"type": "string", "minLength": 3, "maxLength": 80},
    "email": {"type": "string", "format": "email"},
    "age": {"type": "integer", "minimum": 0}
}

@app.route("/users", methods=["POST"])
@validate_request(user_schema)
def create_user(data):
    """Create user with validated data."""
    # Data is already validated
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201
```

---

## Deployment

### Production Deployment (Self-Contained)

```python
"""
Production deployment configuration.
Self-contained - all necessary patterns included.
"""

# 1. Use production server (e.g., gunicorn)
# requirements.txt:
# gunicorn>=20.1.0

# 2. Production configuration
import os

class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

app = App(config=ProductionConfig())

# 3. Run with gunicorn
# gunicorn -w 4 -b 0.0.0.0:8000 app:app

# 4. Environment variables (.env)
# SECRET_KEY=your-production-secret-key
# DATABASE_URL=postgresql://user:pass@localhost/dbname
# ALLOWED_HOSTS=example.com,www.example.com
```

---

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **pytest-patterns**: Advanced testing patterns and fixtures
  - *Use case*: Comprehensive test suites with parametrization
  - *Integration*: Enhance basic testing patterns shown above
  - *Status*: Optional - basic testing patterns included in this skill

- **database-orm-patterns**: Advanced ORM patterns and optimization
  - *Use case*: Complex queries, relationships, performance tuning
  - *Integration*: Builds on basic database pattern shown above
  - *Status*: Optional - basic CRUD patterns included in this skill

- **api-security**: Authentication, authorization, security best practices
  - *Use case*: Production-ready security implementation
  - *Integration*: Adds security layer to routes
  - *Status*: Recommended for production - basic examples shown above

- **deployment-patterns**: Docker, CI/CD, monitoring, scaling
  - *Use case*: Production deployment and operations
  - *Integration*: Deployment strategies and tooling
  - *Status*: Optional - basic deployment shown above

**Note**: All complementary skills are independently deployable. This skill is fully functional without them.

---

## Common Pitfalls

### ❌ Don't: Relative Imports
```python
# DON'T DO THIS
from ..other_skill.patterns import setup
```

### ✅ Do: Self-Contained Patterns
```python
# Include pattern directly
def setup():
    """Setup pattern (self-contained)."""
    # Implementation here
    pass
```

### ❌ Don't: External Skill Dependencies
```python
# DON'T DO THIS
# This requires pytest-patterns skill
from skills.pytest_patterns import fixture_factory
```

### ✅ Do: Inline Essential Patterns
```python
# Include essential pattern
def fixture_factory(name, default=None):
    """Fixture factory pattern (inlined)."""
    @pytest.fixture
    def _fixture():
        return default
    _fixture.__name__ = name
    return _fixture
```

---

## Progressive Disclosure

For more advanced topics, see the `references/` directory:

- **[references/advanced-patterns.md](references/advanced-patterns.md)**: Advanced framework patterns
- **[references/performance.md](references/performance.md)**: Performance optimization
- **[references/api-reference.md](references/api-reference.md)**: Complete API documentation

**Note**: Main SKILL.md is self-sufficient. References provide optional deep dives.

---

## Resources

**Official Documentation**:
- Example Framework Docs: https://example-framework.readthedocs.io
- API Reference: https://example-framework.readthedocs.io/api
- Community: https://github.com/example-framework/community

**Related Technologies**:
- Python: https://docs.python.org
- SQLite: https://www.sqlite.org
- Pytest: https://docs.pytest.org

---

## Summary

This skill demonstrates **self-contained skill development**:

✅ **Complete**: All essential patterns included inline
✅ **Independent**: Works without other skills
✅ **Tested**: Verified in isolation
✅ **Deployable**: Works in flat directory structure
✅ **Graceful**: Notes optional enhancements without requiring them

**Use this as a template** for creating new skills.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-30
**Self-Containment**: ✅ Fully Compliant
