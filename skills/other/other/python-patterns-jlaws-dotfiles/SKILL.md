---
name: python-patterns
description: Use when creating Python projects, choosing concurrency models, optimizing performance, or managing dependencies with uv.
---

# Python Patterns

Tooling opinions, concurrency decisions, async guardrails, profiling workflow, and packaging.

## Style Guide

Source: Google Python Style Guide. Only rules linters/formatters cannot enforce.

### Naming
- `_internal` prefix for module-internal names
- Avoid single-char names except counters (`i`, `j`), exceptions (`e`), file handles (`f`)
- Names describe purpose, not type: `user_list` not `l`, `count` not `n`
- Boolean variables/functions: `is_`, `has_`, `can_`, `should_` prefix
- Avoid generic names: `data`, `info`, `temp`, `val` — be specific
- Module names: short, lowercase, no dashes — `utilities` not `my-utils`

### Docstrings
- Google-style with `Args:`/`Returns:`/`Raises:` sections
- Every public module, function, class, and method

### Practices
- No mutable default args; use `None` + assign inside
- No `assert` for validation — use `raise ValueError`
- Logging: `%` formatting not f-strings (`logger.info('Val: %s', val)`)
- Comprehensions: simple only, no multiple `for` clauses
- Lambda: one-liners only, prefer named functions
- `with` for all file/resource handling
- Max function length ~40 lines
- No `staticmethod`; limit `classmethod` to named constructors
- Properties: only trivial computations

## Tooling Defaults

| Concern | Use | Why |
|---------|-----|-----|
| Package manager | `uv` | 10-100x faster than pip/poetry, handles venvs + Python versions |
| Linter + formatter | `ruff` | Replaces black, isort, flake8 in one tool |
| Type checker | `mypy` (strict) | Catch bugs at dev time |
| Testing | `pytest` + `pytest-asyncio` | De facto standard |
| Build backend | `hatchling` (libraries), `setuptools` (apps) | Hatch is modern, setuptools is universal |

### ruff config opinions
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

## uv Workflows

```bash
# New project
uv init my-project && cd my-project
uv python pin 3.12

# Deps (updates pyproject.toml + uv.lock in one step)
uv add fastapi uvicorn
uv add --dev pytest ruff

# Run without activating venv
uv run pytest
uv run python app.py

# CI/deploy: fail if lockfile stale
uv sync --frozen

# Upgrade
uv lock --upgrade-package requests
uv lock --upgrade  # all deps
```

### uv Key Opinions
- **Always commit `uv.lock`** -- reproducible builds
- **Use `uv run`** instead of activating venvs -- simpler, works in scripts/CI
- **`--frozen` in CI** -- fail if lockfile is stale rather than silently resolving
- **Pin Python version** with `.python-version` file
- **Export for compat**: `uv export --format requirements-txt > requirements.txt`

### uv Gotchas
- `uv add` modifies `pyproject.toml` AND `uv.lock` in one step (unlike poetry two-step)
- `uv sync` creates `.venv` if it doesn't exist
- Cache is global (`~/.cache/uv`) -- shared across projects, rarely needs clearing
- `uv pip install` is pip-compat interface; `uv add` is project-level -- don't mix them

### uv Docker (multi-stage)
```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "app.py"]
```

### uv CI Pattern
```yaml
- uses: astral-sh/setup-uv@v2
  with: { enable-cache: true }
- run: uv python install 3.12
- run: uv sync --all-extras --dev
- run: uv run pytest
```

### uv Workspace (monorepo)
```toml
[tool.uv.workspace]
members = ["packages/*"]
```

## Project Scaffolding

- **Always use `src/` layout** -- prevents importing uninstalled code, cleaner test isolation
- **Single source of truth**: `pyproject.toml` for everything (no setup.py, setup.cfg)
- **Version**: `setuptools-scm` for git-tag-based, or `__version__` in `__init__.py`
- **Dependency ranges**: `"requests>=2.28,<3"` -- avoid exact pins except in lockfiles
- **Type stubs**: include `py.typed` marker for PEP 561

### Project Type Selection

| Type | When | Key deps |
|------|------|----------|
| **FastAPI** | REST APIs, microservices, async | fastapi, uvicorn, pydantic-settings, sqlalchemy, alembic |
| **Django** | Full-stack web, admin, ORM-heavy | django, django-environ, psycopg, gunicorn |
| **Library** | Reusable packages | hatchling (build backend) |
| **CLI** | Command-line tools | typer, rich |

## Concurrency Decision Framework

| Workload | Use | Why |
|----------|-----|-----|
| I/O-bound (HTTP, DB, files) | `asyncio` | Single-threaded, no GIL contention, lowest overhead |
| I/O-bound + sync libraries | `threading` + `ThreadPoolExecutor` | When you can't go async all the way |
| CPU-bound | `multiprocessing` | Bypasses GIL, true parallelism |
| CPU-bound + shared state | `multiprocessing` + `Manager` | Avoid; redesign to message-passing if possible |
| Mixed I/O + CPU | `asyncio` + `run_in_executor` | Async for I/O, thread/process pool for CPU |

## Async Gotchas

### Blocking the loop kills performance
```python
# WRONG - blocks event loop, all coroutines stall
async def bad():
    time.sleep(1)

# RIGHT - offload blocking work
async def good():
    await asyncio.get_event_loop().run_in_executor(None, time.sleep, 1)
```

### gather vs TaskGroup
- `asyncio.gather(*tasks, return_exceptions=True)` -- fan-out, collect all results
- `asyncio.TaskGroup()` (3.11+) -- structured concurrency, cancels siblings on first exception
- **Prefer `TaskGroup`** for correctness; use `gather` when you need partial results

### Semaphore for rate limiting
```python
sem = asyncio.Semaphore(10)
async def rate_limited_fetch(url: str) -> bytes:
    async with sem:
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                return await r.read()
```

### Cancellation must be handled
```python
async def cancelable_task():
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # cleanup here
        raise  # re-raise to propagate
```

### Connection pool sizing
```python
connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
async with aiohttp.ClientSession(connector=connector) as session:
    ...
```

## Profiling Strategy

| Need | Tool | Command |
|------|------|---------|
| Where is time spent? | `cProfile` | `python -m cProfile -o out.prof script.py` |
| Line-by-line timing | `line_profiler` | `kernprof -l -v script.py` |
| Memory usage | `memory_profiler` | `python -m memory_profiler script.py` |
| Production sampling | `py-spy` | `py-spy record -o flame.svg --pid PID` |
| Memory leaks | `tracemalloc` | Built-in, snapshot comparison |
| Benchmarking | `pytest-benchmark` | `pytest --benchmark-compare` |

### Profiling workflow
1. **Measure first** -- never optimize without a profile
2. `cProfile` to find hot functions (sort by `cumtime`)
3. `line_profiler` on the hot function to find hot lines
4. Fix algorithmic issues before micro-optimizations
5. Re-profile to verify improvement

### tracemalloc for leak detection
```python
tracemalloc.start()
snap1 = tracemalloc.take_snapshot()
# ... run suspect code ...
snap2 = tracemalloc.take_snapshot()
for stat in snap2.compare_to(snap1, 'lineno')[:10]:
    print(stat)
```

## Performance Patterns

### Caching decisions

| Scenario | Use |
|----------|-----|
| Pure function, small args | `@functools.lru_cache(maxsize=256)` |
| Pure function, unhashable args | `@functools.cache` (3.9+) or serialize key |
| TTL-based | `cachetools.TTLCache` or Redis |
| Async | `aiocache` or manual dict + asyncio.Lock |
| Cross-process | Redis or memcached |

**Gotcha**: `@lru_cache` requires hashable args -- use `tuple` not `dict`.

### __slots__ for many instances
```python
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
# ~40% less memory per instance vs regular class
```

### Batch I/O operations
```python
# SLOW: commit per insert
for item in items:
    cursor.execute("INSERT ...", item)
    conn.commit()

# FAST: single commit
cursor.executemany("INSERT ...", items)
conn.commit()
```

## Packaging

- **Build backend**: `hatchling` for libraries, `setuptools` for apps that don't publish
- **Entry points**: `[project.scripts]` for CLIs, `[project.entry-points]` for plugins

### Publishing workflow
```bash
uv pip install build twine
python -m build
twine check dist/*
twine upload --repository testpypi dist/*  # test first
twine upload dist/*
```
