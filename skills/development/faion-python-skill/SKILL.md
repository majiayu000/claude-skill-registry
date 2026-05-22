---
name: faion-python-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*, pip:*, poetry:*, pytest:*, mypy:*, black:*, isort:*, flake8:*)
---

# Python Ecosystem Skill

**Technical skill for Python development: Django, FastAPI, pytest, Poetry, async, typing, and code quality tools.**

---

## Purpose

Provides patterns and best practices for Python ecosystem development. Used by faion-code-agent for:
- Python project setup and dependency management
- Django web application development
- FastAPI REST API development
- Testing with pytest
- Type hints and static analysis
- Code formatting and linting

---

## 3-Layer Architecture

```
Layer 1: Domain Skills (orchestrators)
    |
Layer 2: Agents (executors)
    |   - faion-code-agent (uses this skill)
    |   - faion-test-agent (uses this skill)
    |
Layer 3: Technical Skills (this)
    - faion-python-skill
```

---

## Triggers

Use this skill when:
- Setting up a new Python project
- Writing Django models, views, serializers, admin
- Creating FastAPI routes and dependencies
- Writing pytest tests, fixtures, mocking
- Managing dependencies with Poetry or pip
- Adding type hints and running mypy
- Configuring Black, isort, flake8

---

# Methodology M-PY-001: Project Setup with Poetry

## Problem

Python projects need consistent dependency management, virtual environments, and reproducible builds.

## Framework

### Step 1: Initialize Project

```bash
# New project
poetry new my-project
cd my-project

# Or existing project
cd existing-project
poetry init
```

### Step 2: Configure pyproject.toml

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = ["Author Name <author@example.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"
djangorestframework = "^3.14"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-django = "^4.8"
pytest-cov = "^4.1"
mypy = "^1.8"
black = "^24.0"
isort = "^5.13"
flake8 = "^7.0"
django-stubs = "^4.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Step 3: Manage Dependencies

```bash
# Add dependency
poetry add django fastapi

# Add dev dependency
poetry add --group dev pytest mypy

# Update dependencies
poetry update

# Lock dependencies
poetry lock

# Install from lock file
poetry install

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

### Step 4: Virtual Environment

```bash
# Create and activate
poetry shell

# Or run command in venv
poetry run python manage.py migrate
poetry run pytest

# Show venv path
poetry env info --path
```

## Templates

**Minimal pyproject.toml:**
```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = ""
authors = []

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Agent

Executed by: faion-code-agent, faion-devops-agent

---

# Methodology M-PY-002: Django Patterns

## Problem

Django projects need consistent architecture: models, views, serializers, services, and admin configuration.

## Framework

### Project Structure

```
project/
|-- config/                    # Django settings
|   |-- __init__.py
|   |-- settings/
|   |   |-- __init__.py
|   |   |-- base.py           # Common settings
|   |   |-- development.py    # Dev overrides
|   |   |-- production.py     # Prod overrides
|   |-- urls.py
|   |-- wsgi.py
|   |-- asgi.py
|
|-- apps/
|   |-- users/
|   |   |-- __init__.py
|   |   |-- models.py
|   |   |-- views.py
|   |   |-- serializers.py
|   |   |-- services.py       # Business logic
|   |   |-- admin.py
|   |   |-- urls.py
|   |   |-- tests/
|   |   |   |-- __init__.py
|   |   |   |-- test_models.py
|   |   |   |-- test_views.py
|   |   |   |-- test_services.py
|   |   |-- migrations/
|
|-- manage.py
|-- pyproject.toml
```

### Models Pattern

```python
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.TextChoices):
    """User type choices."""
    REGULAR = 'regular', 'Regular User'
    PREMIUM = 'premium', 'Premium User'
    ADMIN = 'admin', 'Administrator'


class User(BaseModel):
    """User model."""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.REGULAR,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email
```

### Services Pattern (Business Logic)

```python
# services.py
from django.db import transaction
from .models import User, UserType


def create_user(
    email: str,
    name: str,
    *,
    user_type: str = UserType.REGULAR,
) -> User:
    """Create a new user."""
    user = User.objects.create(
        email=email,
        name=name,
        user_type=user_type,
    )
    return user


def upgrade_to_premium(
    user: User,
    *,
    upgraded_by: User | None = None,
) -> User:
    """Upgrade user to premium."""
    user.user_type = UserType.PREMIUM
    user.save(update_fields=['user_type', 'updated_at'])
    return user


@transaction.atomic
def transfer_ownership(
    from_user: User,
    to_user: User,
    item_id: int,
) -> None:
    """Transfer item ownership between users."""
    from apps.items import models as item_models

    item = item_models.Item.objects.select_for_update().get(id=item_id)
    item.owner = to_user
    item.save(update_fields=['owner', 'updated_at'])
```

### Views Pattern (Thin Views)

```python
# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import services
from .serializers import CreateUserRequest, UserResponse


class UserCreateView(APIView):
    """Create user endpoint."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.create_user(
            email=serializer.validated_data['email'],
            name=serializer.validated_data['name'],
        )

        return Response(
            UserResponse(user).data,
            status=status.HTTP_201_CREATED,
        )
```

### Serializers Pattern

```python
# serializers.py
from rest_framework import serializers
from .models import User


class CreateUserRequest(serializers.Serializer):
    """Request serializer for user creation."""
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)


class UserResponse(serializers.ModelSerializer):
    """Response serializer for user data."""
    class Meta:
        model = User
        fields = ['uid', 'email', 'name', 'user_type', 'created_at']
        read_only_fields = fields
```

### Admin Pattern

```python
# admin.py
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'user_type', 'is_active', 'created_at']
    list_filter = ['user_type', 'is_active', 'created_at']
    search_fields = ['email', 'name']
    readonly_fields = ['uid', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = [
        (None, {'fields': ['email', 'name']}),
        ('Status', {'fields': ['user_type', 'is_active']}),
        ('Metadata', {'fields': ['uid', 'created_at', 'updated_at']}),
    ]
```

## Templates

**Cross-app imports:**
```python
# Always use aliases for cross-app imports
from apps.orders import models as order_models
from apps.users import services as user_services
```

## Agent

Executed by: faion-code-agent

---

# Methodology M-PY-003: FastAPI Patterns

## Problem

FastAPI projects need consistent route organization, dependency injection, Pydantic models, and async handling.

## Framework

### Project Structure

```
project/
|-- app/
|   |-- __init__.py
|   |-- main.py               # FastAPI app
|   |-- config.py             # Settings
|   |-- dependencies.py       # DI dependencies
|   |
|   |-- routers/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- items.py
|   |
|   |-- schemas/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- items.py
|   |
|   |-- models/
|   |   |-- __init__.py
|   |   |-- users.py
|   |
|   |-- services/
|   |   |-- __init__.py
|   |   |-- users.py
|   |
|   |-- db/
|       |-- __init__.py
|       |-- database.py
|       |-- session.py
|
|-- tests/
|-- pyproject.toml
```

### Main Application

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import users, items
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    await init_db()
    yield


app = FastAPI(
    title="My API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Routes with Dependencies

```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.schemas.users import UserCreate, UserResponse
from app.services import users as user_service
from app.models.users import User

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user."""
    user = await user_service.create_user(db, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get user by ID."""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
```

### Pydantic Schemas

```python
# schemas/users.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """User creation request."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update request."""
    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None


class UserResponse(UserBase):
    """User response."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Dependencies

```python
# dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.models.users import User
from app.services import auth as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_db():
    """Database session dependency."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current authenticated user."""
    user = await auth_service.get_user_from_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user


# Type alias for cleaner signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
```

### Background Tasks

```python
# routers/notifications.py
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


def send_email(email: str, message: str) -> None:
    """Send email in background."""
    # Email sending logic
    pass


@router.post("/notify")
async def send_notification(
    email: str,
    message: str,
    background_tasks: BackgroundTasks,
):
    """Send notification email."""
    background_tasks.add_task(send_email, email, message)
    return {"status": "notification queued"}
```

## Templates

**Async service function:**
```python
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

## Agent

Executed by: faion-code-agent

---

# Methodology M-PY-004: pytest Patterns

## Problem

Python projects need consistent testing with fixtures, mocking, parametrization, and coverage.

## Framework

### Test Structure

```
tests/
|-- __init__.py
|-- conftest.py               # Shared fixtures
|-- test_models.py
|-- test_services.py
|-- test_views.py
|-- integration/
|   |-- __init__.py
|   |-- test_api.py
|-- fixtures/
    |-- users.py
    |-- items.py
```

### conftest.py (Shared Fixtures)

```python
# conftest.py
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_db():
    """Mock database session."""
    return MagicMock()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
    }


# Django-specific
@pytest.fixture
def api_client():
    """DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client
```

### Fixtures with Factory Pattern

```python
# fixtures/users.py
import pytest
from apps.users.models import User


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create(
        email="user@example.com",
        name="Test User",
    )


@pytest.fixture
def user_factory(db):
    """Factory for creating users."""
    def create_user(
        email: str = "user@example.com",
        name: str = "Test User",
        **kwargs,
    ) -> User:
        return User.objects.create(
            email=email,
            name=name,
            **kwargs,
        )
    return create_user


@pytest.fixture
def users(user_factory):
    """Create multiple test users."""
    return [
        user_factory(email=f"user{i}@example.com")
        for i in range(3)
    ]
```

### Mocking

```python
# test_services.py
from unittest.mock import patch, MagicMock
import pytest

from apps.users import services


class TestCreateUser:
    def test_create_user_success(self, sample_user_data):
        """Test successful user creation."""
        with patch.object(services, 'send_welcome_email') as mock_email:
            user = services.create_user(**sample_user_data)

            assert user.email == sample_user_data['email']
            mock_email.assert_called_once_with(user)

    def test_create_user_duplicate_email(self, user, sample_user_data):
        """Test duplicate email raises error."""
        sample_user_data['email'] = user.email

        with pytest.raises(ValueError, match="Email already exists"):
            services.create_user(**sample_user_data)


class TestExternalAPI:
    @patch('apps.users.services.external_api.get_user_info')
    def test_sync_user_from_external(self, mock_get_info):
        """Test syncing user from external API."""
        mock_get_info.return_value = {
            "id": "ext-123",
            "name": "External User",
        }

        result = services.sync_from_external("ext-123")

        assert result.external_id == "ext-123"
        mock_get_info.assert_called_once_with("ext-123")
```

### Parametrize

```python
# test_validators.py
import pytest
from apps.users.validators import validate_email, validate_password


class TestEmailValidation:
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user.name@example.co.uk", True),
        ("invalid", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
    ])
    def test_validate_email(self, email, expected):
        """Test email validation with various inputs."""
        assert validate_email(email) == expected


class TestPasswordValidation:
    @pytest.mark.parametrize("password,error_msg", [
        ("short", "Password must be at least 8 characters"),
        ("nodigits", "Password must contain a digit"),
        ("12345678", "Password must contain a letter"),
    ])
    def test_invalid_passwords(self, password, error_msg):
        """Test password validation error messages."""
        with pytest.raises(ValueError, match=error_msg):
            validate_password(password)
```

### Django Integration Tests

```python
# test_views.py
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUserAPI:
    def test_create_user(self, api_client):
        """Test user creation endpoint."""
        response = api_client.post("/api/v1/users/", {
            "email": "new@example.com",
            "name": "New User",
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "new@example.com"

    def test_get_user_requires_auth(self, api_client):
        """Test that user endpoint requires authentication."""
        response = api_client.get("/api/v1/users/me/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, authenticated_client, user):
        """Test getting current user info."""
        response = authenticated_client.get("/api/v1/users/me/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/test_services.py

# Run specific test class
pytest tests/test_services.py::TestCreateUser

# Run specific test
pytest tests/test_services.py::TestCreateUser::test_create_user_success

# Run with verbose output
pytest -v

# Run failed tests only
pytest --lf

# Run and stop on first failure
pytest -x
```

## Templates

**pytest.ini or pyproject.toml:**
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

## Agent

Executed by: faion-test-agent, faion-code-agent

---

# Methodology M-PY-005: Type Hints and mypy

## Problem

Python code needs type safety for better IDE support, documentation, and catching bugs early.

## Framework

### Basic Type Hints

```python
from typing import Any

# Variables
name: str = "John"
age: int = 30
is_active: bool = True
scores: list[int] = [1, 2, 3]
data: dict[str, Any] = {"key": "value"}

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[str]) -> None:
    for item in items:
        print(item)
```

### Optional and Union Types

```python
from typing import Optional

# Optional (value or None)
def get_user(user_id: int) -> Optional[User]:
    """Return user or None if not found."""
    return User.objects.filter(id=user_id).first()

# Modern syntax (Python 3.10+)
def get_user(user_id: int) -> User | None:
    """Return user or None if not found."""
    return User.objects.filter(id=user_id).first()

# Union of types
def process(value: int | str) -> str:
    return str(value)
```

### Generic Types

```python
from typing import TypeVar, Generic
from collections.abc import Sequence, Mapping

T = TypeVar('T')

class Repository(Generic[T]):
    """Generic repository pattern."""

    def get(self, id: int) -> T | None:
        raise NotImplementedError

    def list(self) -> list[T]:
        raise NotImplementedError

    def create(self, item: T) -> T:
        raise NotImplementedError


# Using the generic
class UserRepository(Repository[User]):
    def get(self, id: int) -> User | None:
        return User.objects.filter(id=id).first()


# Type aliases
UserId = int
UserDict = dict[str, Any]
Callback = Callable[[int, str], bool]
```

### Callable Types

```python
from collections.abc import Callable

# Function that takes a callback
def apply_operation(
    values: list[int],
    operation: Callable[[int], int],
) -> list[int]:
    return [operation(v) for v in values]

# Async callable
from collections.abc import Awaitable

AsyncHandler = Callable[[Request], Awaitable[Response]]
```

### TypedDict for Structured Dicts

```python
from typing import TypedDict, NotRequired

class UserData(TypedDict):
    id: int
    email: str
    name: str
    is_active: NotRequired[bool]  # Optional field

def process_user(data: UserData) -> None:
    print(data["email"])  # Type-safe access
```

### Protocol for Duck Typing

```python
from typing import Protocol

class Sendable(Protocol):
    """Protocol for objects that can be sent."""
    def send(self, message: str) -> bool:
        ...

class EmailClient:
    def send(self, message: str) -> bool:
        # Send email
        return True

class SMSClient:
    def send(self, message: str) -> bool:
        # Send SMS
        return True

def notify(client: Sendable, message: str) -> bool:
    """Works with any Sendable."""
    return client.send(message)
```

### mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

# Per-module configuration
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

### Running mypy

```bash
# Check all code
mypy src/

# Check specific file
mypy src/services/users.py

# Check with specific options
mypy --strict src/

# Generate HTML report
mypy --html-report mypy-report src/
```

## Templates

**Type-safe function signature:**
```python
def process_user(
    user_id: int,
    action: str,
    *,
    force: bool = False,
    metadata: dict[str, Any] | None = None,
) -> tuple[User, bool]:
    ...
```

## Agent

Executed by: faion-code-agent

---

# Methodology M-PY-006: Code Formatting (Black, isort, flake8)

## Problem

Python code needs consistent formatting, import organization, and linting across the team.

## Framework

### Black Configuration

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
    | migrations
)/
'''
```

### isort Configuration

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip = [".venv", "migrations"]
known_first_party = ["apps", "config"]
known_third_party = ["django", "rest_framework", "fastapi"]
sections = [
    "FUTURE",
    "STDLIB",
    "THIRDPARTY",
    "FIRSTPARTY",
    "LOCALFOLDER",
]
```

### flake8 Configuration

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, E501, W503
exclude =
    .git,
    .venv,
    __pycache__,
    migrations,
    .mypy_cache,
per-file-ignores =
    __init__.py:F401
    tests/*:S101
```

### Running Tools

```bash
# Format with Black
black src/
black --check src/  # Check only

# Sort imports with isort
isort src/
isort --check-only src/  # Check only

# Lint with flake8
flake8 src/

# Run all (typical order)
isort src/ && black src/ && flake8 src/
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs
          - types-requests
```

### Install and Use Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

### Makefile Integration

```makefile
.PHONY: format lint fix

format:
	isort src/ tests/
	black src/ tests/

lint:
	flake8 src/ tests/
	mypy src/

fix: format lint
```

## Templates

**Complete pyproject.toml tools section:**
```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.11"
strict = true
```

## Agent

Executed by: faion-code-agent, faion-devops-agent

---

# Methodology M-PY-007: Virtual Environments

## Problem

Python projects need isolated environments for dependencies, avoiding conflicts between projects.

## Framework

### venv (Built-in)

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Deactivate
deactivate

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt
```

### Poetry (Recommended)

```bash
# Create new project with venv
poetry new my-project
cd my-project

# Or initialize in existing project
poetry init

# Install dependencies (creates venv automatically)
poetry install

# Activate venv
poetry shell

# Run command in venv
poetry run python script.py
poetry run pytest

# Show venv info
poetry env info
poetry env info --path

# Remove venv
poetry env remove python

# Use specific Python version
poetry env use python3.11
```

### pyenv for Python Versions

```bash
# Install pyenv (Linux)
curl https://pyenv.run | bash

# List available Python versions
pyenv install --list

# Install specific version
pyenv install 3.11.7

# Set local version for project
cd my-project
pyenv local 3.11.7

# Set global version
pyenv global 3.11.7

# Show current version
pyenv version
```

### pyenv + Poetry Integration

```bash
# Install Python version
pyenv install 3.11.7

# Set for project
cd my-project
pyenv local 3.11.7

# Initialize Poetry with this version
poetry env use $(pyenv which python)
poetry install
```

### Best Practices

```bash
# Directory structure with venv
project/
|-- .venv/              # Virtual environment (gitignored)
|-- .python-version     # pyenv local version
|-- pyproject.toml      # Poetry config
|-- poetry.lock         # Locked dependencies
|-- requirements.txt    # Optional export

# .gitignore
.venv/
*.pyc
__pycache__/
.mypy_cache/
.pytest_cache/
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only dependency files first (cache layer)
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY . .

CMD ["python", "main.py"]
```

## Templates

**requirements.txt from Poetry:**
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output requirements-dev.txt --with dev --without-hashes
```

## Agent

Executed by: faion-devops-agent, faion-code-agent

---

# Methodology M-PY-008: Async Python (asyncio)

## Problem

Python applications need efficient concurrent execution for I/O-bound operations like API calls, database queries, and file operations.

## Framework

### Basic Async/Await

```python
import asyncio


async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main():
    result = await fetch_data("https://api.example.com/data")
    print(result)


# Run the async function
asyncio.run(main())
```

### Concurrent Execution

```python
import asyncio


async def fetch_user(user_id: int) -> dict:
    """Simulate fetching user data."""
    await asyncio.sleep(0.5)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}


async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)


async def main():
    # Sequential: 5 seconds
    # Concurrent: ~0.5 seconds
    users = await fetch_all_users([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Fetched {len(users)} users")
```

### TaskGroup (Python 3.11+)

```python
import asyncio


async def process_item(item: str) -> str:
    await asyncio.sleep(0.1)
    return f"Processed: {item}"


async def main():
    results = []

    async with asyncio.TaskGroup() as tg:
        for item in ["a", "b", "c"]:
            task = tg.create_task(process_item(item))
            # Tasks run concurrently

    # All tasks completed when exiting context
```

### Async Context Managers

```python
import asyncio
from contextlib import asynccontextmanager


class AsyncDatabaseConnection:
    async def connect(self) -> None:
        print("Connecting to database...")
        await asyncio.sleep(0.1)

    async def disconnect(self) -> None:
        print("Disconnecting from database...")
        await asyncio.sleep(0.1)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


# Using async context manager
async def main():
    async with AsyncDatabaseConnection() as db:
        # Use db connection
        pass


# Function-based context manager
@asynccontextmanager
async def get_connection():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()
```

### Async Generators

```python
import asyncio


async def async_range(start: int, stop: int):
    """Async generator example."""
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i


async def main():
    async for num in async_range(0, 5):
        print(num)
```

### Semaphores for Rate Limiting

```python
import asyncio


async def fetch_with_limit(
    urls: list[str],
    max_concurrent: int = 5,
) -> list[dict]:
    """Fetch URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Timeouts

```python
import asyncio


async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "Done"


async def main():
    try:
        # Timeout after 2 seconds
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out")


# Context manager timeout (Python 3.11+)
async def main_with_scope():
    async with asyncio.timeout(2.0):
        result = await slow_operation()
```

### Async in Django

```python
# views.py
from django.http import JsonResponse
import asyncio


async def async_view(request):
    """Async Django view."""
    data = await fetch_external_data()
    return JsonResponse(data)


# Call sync code from async
from asgiref.sync import sync_to_async

@sync_to_async
def get_user_sync(user_id: int):
    return User.objects.get(id=user_id)


async def async_view_with_db(request):
    user = await get_user_sync(request.user.id)
    return JsonResponse({"name": user.name})
```

### Async in FastAPI

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()


@app.get("/items")
async def get_items():
    """Async endpoint."""
    items = await fetch_items_from_db()
    return {"items": items}


@app.get("/aggregate")
async def get_aggregate():
    """Concurrent data fetching."""
    users, products, orders = await asyncio.gather(
        fetch_users(),
        fetch_products(),
        fetch_orders(),
    )
    return {
        "users": users,
        "products": products,
        "orders": orders,
    }
```

## Templates

**Async main pattern:**
```python
async def main():
    # Your async code
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

## Agent

Executed by: faion-code-agent

---

# Quick Reference

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| Poetry | Dependency management | `poetry add`, `poetry install` |
| pytest | Testing | `pytest`, `pytest --cov` |
| mypy | Type checking | `mypy src/` |
| Black | Code formatting | `black src/` |
| isort | Import sorting | `isort src/` |
| flake8 | Linting | `flake8 src/` |

## Patterns Summary

| Pattern | Use When |
|---------|----------|
| Services | Business logic, DB writes |
| Thin Views | HTTP handling only |
| Factory Fixtures | Flexible test data |
| TypedDict | Structured dictionaries |
| Protocol | Duck typing with type safety |
| asyncio.gather | Concurrent I/O operations |
| Semaphore | Rate limiting |

## Methodology Index

| ID | Name | Purpose |
|----|------|---------|
| M-PY-001 | Project Setup with Poetry | Dependency management |
| M-PY-002 | Django Patterns | Models, views, serializers, admin |
| M-PY-003 | FastAPI Patterns | Routes, dependencies, Pydantic |
| M-PY-004 | pytest Patterns | Fixtures, mocking, parametrize |
| M-PY-005 | Type Hints and mypy | Type safety and static analysis |
| M-PY-006 | Code Formatting | Black, isort, flake8 |
| M-PY-007 | Virtual Environments | venv, Poetry, pyenv |
| M-PY-008 | Async Python | asyncio, concurrent execution |

---

## Sources

- [Python Documentation](https://docs.python.org/3/)
- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)

---

*Python Ecosystem Skill v1.0*
*Layer 3 Technical Skill*
*8 Methodologies | Used by faion-code-agent, faion-test-agent*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-PY-001 | Project Setup Poetry | [methodologies/M-PY-001_project_setup_poetry.md](methodologies/M-PY-001_project_setup_poetry.md) |
| M-PY-002 | Django Patterns | [methodologies/M-PY-002_django_patterns.md](methodologies/M-PY-002_django_patterns.md) |
| M-PY-003 | Fastapi Patterns | [methodologies/M-PY-003_fastapi_patterns.md](methodologies/M-PY-003_fastapi_patterns.md) |
| M-PY-004 | Pytest Testing | [methodologies/M-PY-004_pytest_testing.md](methodologies/M-PY-004_pytest_testing.md) |
| M-PY-005 | Asyncio Patterns | [methodologies/M-PY-005_asyncio_patterns.md](methodologies/M-PY-005_asyncio_patterns.md) |
| M-PY-006 | Type Hints | [methodologies/M-PY-006_type_hints.md](methodologies/M-PY-006_type_hints.md) |
| M-PY-007 | Packaging | [methodologies/M-PY-007_packaging.md](methodologies/M-PY-007_packaging.md) |
| M-PY-008 | Code Quality | [methodologies/M-PY-008_code_quality.md](methodologies/M-PY-008_code_quality.md) |
