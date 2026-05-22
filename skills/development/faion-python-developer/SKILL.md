---
name: faion-python-developer
description: "Python development: Django, FastAPI, async patterns, testing, type hints."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Python Developer Skill

Python development specializing in Django, FastAPI, async programming, and modern Python patterns.

## Purpose

Handles all Python backend development including Django full-stack apps, FastAPI async APIs, pytest testing, and Python best practices.

---

## Context Discovery

### Auto-Investigation

Gather Python project context before asking questions:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `manage.py` | `Glob("**/manage.py")` | Django project |
| `pyproject.toml` | `Read("pyproject.toml")` | Dependencies, Python version, tools |
| `requirements.txt` | `Read("requirements.txt")` | Dependencies (legacy setup) |
| `settings/*.py` | `Glob("**/settings/*.py")` | Django settings structure |
| `services/*.py` | `Glob("**/services/*.py")` | Service layer exists → follow pattern |
| `conftest.py` | `Glob("**/conftest.py")` | pytest fixtures exist → check style |
| `factories.py` | `Glob("**/factories.py")` | Factory Boy used for tests |
| `tasks.py` or `celery.py` | `Glob("**/tasks.py")` | Celery async tasks used |
| `.pre-commit-config.yaml` | `Glob("**/.pre-commit-config.yaml")` | Pre-commit hooks, linting tools |
| `mypy.ini` or `pyproject.toml [tool.mypy]` | Check for mypy config | Type checking enforced |

**Read existing code to understand patterns:**
```
- Read a model file to see BaseModel pattern
- Read a service file to see service layer style
- Read a test file to see testing conventions
- Read serializers to see DRF patterns
```

### Discovery Questions

Use `AskUserQuestion` for Python-specific decisions not clear from investigation.

#### Q1: Framework Choice (only if not detected)

```yaml
question: "Which Python framework are you using?"
header: "Framework"
multiSelect: false
options:
  - label: "Django"
    description: "Full-featured web framework with ORM"
  - label: "FastAPI"
    description: "Modern async API framework"
  - label: "Flask"
    description: "Lightweight microframework"
  - label: "No framework (scripts/CLI)"
    description: "Pure Python application"
```

**Routing:**
- "Django" → django-* methodologies
- "FastAPI" → python-fastapi, python-async
- "Flask" → python-web-frameworks
- "No framework" → python-basics, python-code-quality

#### Q2: Code Placement (for new code in Django)

```yaml
question: "What type of code are you writing?"
header: "Code Type"
multiSelect: false
options:
  - label: "Database operations (create/update/delete)"
    description: "Code that modifies data"
  - label: "Business logic (calculations, transformations)"
    description: "Pure functions, no side effects"
  - label: "API endpoint"
    description: "HTTP request handling"
  - label: "Background task"
    description: "Async/scheduled processing"
  - label: "Not sure"
    description: "I'll help you decide based on what it does"
```

**Routing (Django decision tree):**
- "Database operations" → `services/` directory
- "Business logic" → `utils/` directory (pure functions)
- "API endpoint" → `views/` or `viewsets/`
- "Background task" → `tasks/` with Celery
- "Not sure" → Ask what the code does, apply decision tree

#### Q3: Async Requirements

```yaml
question: "Does this need async/concurrent execution?"
header: "Async"
multiSelect: false
options:
  - label: "Yes, I/O bound (API calls, file ops)"
    description: "Multiple external calls that can run in parallel"
  - label: "Yes, background processing"
    description: "Long-running tasks that shouldn't block"
  - label: "No, synchronous is fine"
    description: "Simple request-response flow"
  - label: "Not sure"
    description: "I'll analyze and recommend"
```

**Routing:**
- "I/O bound" → python-async, asyncio patterns
- "Background processing" → django-celery or FastAPI BackgroundTasks
- "Synchronous" → Standard patterns
- "Not sure" → Analyze task characteristics

#### Q4: Type Safety Level

```yaml
question: "What level of type safety do you want?"
header: "Types"
multiSelect: false
options:
  - label: "Strict (full type hints, mypy strict)"
    description: "Maximum type safety, catch errors early"
  - label: "Gradual (key interfaces typed)"
    description: "Type public APIs, internal can be looser"
  - label: "Minimal (match existing code)"
    description: "Follow project's current style"
```

**Routing:**
- "Strict" → python-type-hints strict mode, Protocol, TypedDict
- "Gradual" → Type annotations on public functions
- "Minimal" → Match existing codebase style

#### Q5: Testing Approach (for new features)

```yaml
question: "How should we approach testing?"
header: "Testing"
multiSelect: false
options:
  - label: "TDD (tests first)"
    description: "Write tests before implementation"
  - label: "Tests after implementation"
    description: "Write tests once code works"
  - label: "Match existing test coverage"
    description: "Follow project's testing patterns"
  - label: "No tests needed"
    description: "Spike/prototype, tests later"
```

**Routing:**
- "TDD" → tdd-workflow, write test first
- "Tests after" → django-pytest or python-testing-pytest
- "Match existing" → Read conftest.py, follow patterns
- "No tests" → Skip testing methodologies

---

## When to Use

- Django projects (models, services, API, testing)
- FastAPI async APIs
- Python async patterns and concurrency
- Python type hints and strict typing
- Python testing with pytest
- Python code quality and tooling

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **Django Core** |
| Django standards | Django coding standards, project structure | django-coding-standards.md |
| Django models | Model design, base model patterns | django-base-model.md |
| Django models reference | Model fields, managers, migrations | django-models.md |
| Django services | Service layer architecture | django-services.md |
| Django API | DRF patterns, serializers, viewsets | django-api.md |
| Django testing | Django test patterns, factories | django-testing.md |
| Django pytest | pytest-django, fixtures, parametrize | django-pytest.md |
| Django celery | Async tasks, queues, beat | django-celery.md |
| Django quality | Code quality, linting, formatting | django-quality.md |
| Django imports | Import organization, circular imports | django-imports.md |
| Django decision tree | Framework selection, when to use Django | django-decision-tree.md |
| Django decomposition | Breaking down Django monoliths | decomposition-django.md |
| **FastAPI** |
| FastAPI basics | Routes, dependencies, validation | python-fastapi.md |
| Web frameworks | Django vs FastAPI vs Flask comparison | python-web-frameworks.md |
| **Async Python** |
| Async basics | asyncio, await, event loop | python-async.md |
| Async patterns | Concurrent patterns, asyncio best practices | python-async-patterns.md |
| **Type Safety** |
| Type hints | Gradual typing, annotations | python-type-hints.md |
| Python typing | TypedDict, Protocol, Generic | python-typing.md |
| **Testing** |
| pytest basics | Fixtures, parametrize, markers | python-testing-pytest.md |
| **Python Core** |
| Python basics | Language fundamentals, patterns | python-basics.md |
| Python overview | Quick reference | python.md |
| Python modern 2026 | Python 3.12/3.13 features | python-modern-2026.md |
| Python code quality | ruff, mypy, black, isort | python-code-quality.md |
| Poetry setup | Dependency management, pyproject.toml | python-poetry-setup.md |

## Tools

- **Frameworks:** Django 5.x, FastAPI 0.1x, Flask
- **Testing:** pytest, pytest-django, pytest-asyncio, factory-boy
- **Type checking:** mypy, pyright
- **Linting:** ruff, flake8, pylint
- **Formatting:** black, isort
- **Package management:** poetry, pip-tools, uv

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-backend-developer | Database patterns (PostgreSQL, Redis) |
| faion-api-developer | REST/GraphQL API design |
| faion-testing-developer | Advanced testing patterns |
| faion-devtools-developer | Architecture patterns, code quality |

## Integration

Invoked by parent skill `faion-software-developer` when working with Python code.

---

*faion-python-developer v1.0 | 24 methodologies*
