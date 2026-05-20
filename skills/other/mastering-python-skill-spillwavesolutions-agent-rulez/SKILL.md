---
name: mastering-python-skill
description: Modern Python coaching covering language foundations through advanced production patterns. Use when asked to "write Python code", "explain Python concepts", "set up a Python project", "configure Poetry or PDM", "write pytest tests", "create a FastAPI endpoint", "run uvicorn server", "configure alembic migrations", "set up logging", "process data with pandas", or "debug Python errors". Triggers on "Python best practices", "type hints", "async Python", "packaging", "virtual environments", "Pydantic validation", "dependency injection", "SQLAlchemy models".
allowed-tools:
  - Read
  - Write
  - Bash
  - Edit
metadata:
  version: 2.1.0
  domains:
    - python
    - testing
    - packaging
    - web-development
    - async
    - security
---

# Mastering Python Skill

Production-ready Python patterns with runnable code examples.

## Contents

- [Workflow](#workflow)
- [Reference Files](#reference-files)
- [Sample CLI Tools](#sample-cli-tools)
- [When NOT to Use](#when-not-to-use)
- [Full Table of Contents](TOC.md)

---

## Workflow

### Phase 1: Setup

1. Verify Python version
   ```bash
   python --version  # Require 3.10+, prefer 3.12+
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv .venv && source .venv/bin/activate
   ```

3. Install dependencies
   ```bash
   poetry install  # or: pip install -r requirements.txt
   ```

### Phase 2: Develop

4. Reference appropriate patterns:
   - Types → [type-systems.md](references/foundations/type-systems.md)
   - Async → [async-programming.md](references/patterns/async-programming.md)
   - APIs → [fastapi-patterns.md](references/web-apis/fastapi-patterns.md)
   - DB → [database-access.md](references/web-apis/database-access.md)

5. Follow project structure from [project-structure.md](references/foundations/project-structure.md)

### Phase 3: Validate

6. Run quality checks
   ```bash
   ruff check . && ruff format --check .
   mypy src/
   ```

7. Run tests with coverage
   ```bash
   pytest -v --cov=src --cov-report=term-missing
   ```

### Phase 4: Deploy

8. Build and verify package
   ```bash
   python -m build && twine check dist/*
   ```

9. Deploy per [docker-deployment.md](references/packaging/docker-deployment.md) or [ci-cd-pipelines.md](references/production/ci-cd-pipelines.md)

**Pre-Completion Checklist:**
```
- [ ] All tests pass
- [ ] mypy reports no errors
- [ ] ruff check clean
- [ ] Coverage ≥80%
- [ ] No security warnings in dependencies
```

---

## Reference Files

| Category | Files | Key Topics |
|----------|-------|------------|
| **Foundations** | [syntax-essentials](references/foundations/syntax-essentials.md), [type-systems](references/foundations/type-systems.md), [project-structure](references/foundations/project-structure.md), [code-quality](references/foundations/code-quality.md) | Variables, type hints, generics, src layout, ruff, mypy |
| **Patterns** | [async-programming](references/patterns/async-programming.md), [error-handling](references/patterns/error-handling.md), [decorators](references/patterns/decorators.md), [context-managers](references/patterns/context-managers.md), [generators](references/patterns/generators.md) | async/await, exceptions, Result type, with statements, yield |
| **Testing** | [pytest-essentials](references/testing/pytest-essentials.md), [mocking-strategies](references/testing/mocking-strategies.md), [property-testing](references/testing/property-testing.md) | Fixtures, parametrize, unittest.mock, Hypothesis |
| **Web APIs** | [fastapi-patterns](references/web-apis/fastapi-patterns.md), [pydantic-validation](references/web-apis/pydantic-validation.md), [database-access](references/web-apis/database-access.md) | Dependencies, middleware, validators, SQLAlchemy async |
| **Packaging** | [poetry-workflow](references/packaging/poetry-workflow.md), [pyproject-config](references/packaging/pyproject-config.md), [docker-deployment](references/packaging/docker-deployment.md) | Lock files, PEP 621, multi-stage builds |
| **Production** | [ci-cd-pipelines](references/production/ci-cd-pipelines.md), [monitoring](references/production/monitoring.md), [security](references/production/security.md) | GitHub Actions, OpenTelemetry, OWASP, JWT |

See [TOC.md](TOC.md) for detailed topic lookup.

---

## Sample CLI Tools

Runnable examples demonstrating production patterns:

| Tool | Demonstrates | Reference |
|------|-------------|-----------|
| [async_fetcher.py](sample-cli/async_fetcher.py) | Async HTTP, rate limiting, error handling | [async-programming.md](references/patterns/async-programming.md) |
| [config_loader.py](sample-cli/config_loader.py) | Pydantic settings, .env files, validation | [pydantic-validation.md](references/web-apis/pydantic-validation.md) |
| [db_cli.py](sample-cli/db_cli.py) | SQLAlchemy async CRUD, repository pattern | [database-access.md](references/web-apis/database-access.md) |
| [code_validator.py](sample-cli/code_validator.py) | Run→check→fix with ruff and mypy | [code-quality.md](references/foundations/code-quality.md) |

```bash
# Test examples
python sample-cli/async_fetcher.py https://httpbin.org/get
python sample-cli/config_loader.py --show-env
python sample-cli/db_cli.py init --sample-data && python sample-cli/db_cli.py list
python sample-cli/code_validator.py src/
```

---

## When NOT to Use

- **Non-Python languages**: Use language-specific skills
- **ML/AI model internals**: Use PyTorch/TensorFlow skills
- **Cloud infrastructure**: Use AWS/GCP skills for infra (this covers code)
- **Legacy Python 2**: Focus is Python 3.10+
