---
name: parallel-fix-django
description: Fix Django-specific blockers identified in parallelization readiness assessment
argument-hint: "[--dimension <name>] [--dry-run]"
---

# parallel-fix-django

**Category**: Parallel Development (Django)

## Usage

```bash
/parallel-fix-django [--dimension <name>] [--dry-run]
```

## Arguments

- `--dimension`: Optional - Focus on specific dimension (app-boundaries, shared-state, contracts, tests, docs, deps)
- `--dry-run`: Optional - Show what would be fixed without making changes

## Purpose

Fix blockers identified by `/parallel-ready-django` to prepare the Django codebase for parallel multi-agent development. References the `remediation-checklist.md` from the skill.

## Prerequisites

- Run `/parallel-ready-django` first
- `.claude/readiness-report.md` must exist with identified blockers

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Read Readiness Report

```bash
cat .claude/readiness-report.md
```

Parse the "Blockers" and "Risks" sections to identify what needs fixing.

### 2. Fix by Dimension

#### App Boundaries Fixes

**Problem: God App (>15 models)**
```
1. Identify models that can be grouped by domain
2. Create new Django app: python manage.py startapp [domain] apps/[domain]
3. Move models incrementally with migrations
4. Update all imports
5. Verify tests pass
```

**Problem: Circular Imports**
```python
# Before - circular import
from apps.orders.models import Order  # in users/models.py
from apps.users.models import User    # in orders/models.py

# After - use string reference
class Order(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
```

**Problem: Cross-App Imports >30%**
```
1. Identify shared types/utilities
2. Create apps/shared/ app for common code
3. Move shared code to shared app
4. Update imports to use shared
```

#### Shared State Fixes

**Problem: Cross-App Signals**
```python
# Before - implicit signal
@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)

# After - explicit service call
class UserService:
    def __init__(self, stats_service: StatsService):
        self.stats_service = stats_service

    def create_user(self, email: str, name: str) -> User:
        user = User.objects.create(email=email, name=name)
        self.stats_service.initialize_for_user(user.id)
        return user
```

**Problem: Global Mutable State**
```python
# Before - global variable
_cache = {}

# After - use Django cache
from django.core.cache import cache

def get_cached_value(key: str):
    return cache.get(key)
```

#### API Contracts Fixes

**Problem: Serializers with `__all__`**
```python
# Before
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# After - explicit fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]
        read_only_fields = ["id", "created_at"]
```

**Problem: No Mypy Configuration**

Add to `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["mypy_django_plugin.main", "mypy_drf_plugin.main"]

[[tool.mypy.overrides]]
module = "*.migrations.*"
ignore_errors = true

[tool.django-stubs]
django_settings_module = "config.settings.local"
```

Install dependencies:
```bash
pip install django-stubs djangorestframework-stubs mypy
```

**Problem: No OpenAPI**

Add drf-spectacular:
```bash
pip install drf-spectacular
```

Update settings:
```python
INSTALLED_APPS = [..., "drf_spectacular"]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Project API",
    "VERSION": "1.0.0",
}
```

Add URL:
```python
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
```

#### Test Infrastructure Fixes

**Problem: No Pytest Setup**
```bash
pip install pytest pytest-django factory-boy
```

Create `conftest.py`:
```python
import pytest

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
```

Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = "-v --tb=short"
```

**Problem: No Factories**

Create `apps/[app]/tests/factories.py`:
```python
import factory
from apps.users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
```

#### Documentation Fixes

**Problem: No CLAUDE.md**

Create `CLAUDE.md` with Django conventions. Reference `infrastructure-setup.md` from skill for full template.

**Problem: No Linting**

Add to `pyproject.toml`:
```toml
[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "W", "F", "I", "B", "C4", "UP"]

[tool.ruff.isort]
known-first-party = ["apps", "config"]
```

Run initial format:
```bash
pip install ruff
ruff format .
ruff check . --fix
```

#### Dependencies Fixes

**Problem: Too Many Migrations**
```bash
# Squash migrations
python manage.py squashmigrations [app] 0001 [last_migration]
```

**Problem: Unpinned Dependencies**
```bash
# Pin all dependencies
pip freeze > requirements.txt
# Or use poetry
poetry lock
```

### 3. Re-run Assessment

After fixes, suggest re-running assessment:
```
/parallel-ready-django
```

### 4. Report Results

Output:
```
🔧 Django Parallelization Fixes Applied

Fixed Issues:
✅ Converted 5 serializers from __all__ to explicit fields
✅ Added mypy configuration to pyproject.toml
✅ Created CLAUDE.md with Django conventions
✅ Added ruff linting configuration

Remaining Issues:
⚠️ 2 cross-app signals need manual review (apps/orders/signals.py)
⚠️ God app 'core' has 18 models - consider splitting

Next steps:
1. Review remaining issues manually
2. Run /parallel-ready-django to verify score improved
3. Target score ≥80 before running /parallel-decompose
```

## Example

```bash
# Fix all blockers
/parallel-fix-django

# Fix only serializer issues
/parallel-fix-django --dimension contracts

# Preview changes without applying
/parallel-fix-django --dry-run

# After fixing, re-assess
/parallel-ready-django
```

## Related Commands

- `/parallel-ready-django` - Run assessment first
- `/parallel-setup` - Ensure infrastructure exists
- `/parallel-decompose` - Create tasks after score ≥80
