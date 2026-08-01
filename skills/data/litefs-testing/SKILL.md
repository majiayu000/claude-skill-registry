---
name: litefs-testing
description: 'Testing patterns for litefs-py and litefs-django. Use when writing tests,
  setting up fixtures, understanding test organization, or configuring pytest marks.
  Triggers: test, pytest, unit test, integrat'
---

---
name: litefs-testing
description: Testing patterns for litefs-py and litefs-django. Use when writing tests, setting up fixtures, understanding test organization, or configuring pytest marks. Triggers: test, pytest, unit test, integration test, property-based testing, hypothesis, fixtures, in-memory adapters.
---

# LiteFS Testing Strategy

Project-specific testing patterns for litefs-py and litefs-django.

## When to Use

- Writing tests for LiteFS-related code
- Setting up test fixtures
- Understanding test organization

## Test Organization

```bash
# By category
pytest -m unit           # Fast, no LiteFS process
pytest -m integration    # With Docker + FUSE
pytest -m property       # Property-based tests
```

## Test Directory Structure

```
tests/
├── unit/                    # No I/O, no subprocess
│   ├── domain/              # Pure domain logic (settings, config)
│   ├── usecases/            # Use case tests with in-memory adapters
│   └── conftest.py          # In-memory adapter fixtures
├── integration/             # Requires Docker + FUSE
│   ├── test_backend.py
│   └── test_replication.py
└── conftest.py              # Shared fixtures
```

## CI Strategy

- **Unit tests**: Run on all PRs (fast, no Docker)
- **Integration tests**: Run on main branch only (requires Docker + FUSE)
- **Local testing**: Docker Compose setup mirrors integration CI

## Test Isolation Rules

**Unit tests (`tests/unit/`) must NOT:**

- Spawn subprocesses or call LiteFS binary
- Access filesystem beyond temp directories
- Require FUSE or Docker

**Unit tests SHOULD use:**

- In-memory adapter fixtures:
  - `in_memory_process_runner` → `InMemoryProcessRunner`
  - `in_memory_config_writer` → `InMemoryConfigWriter`
  - `fake_primary_detector` → `FakePrimaryDetector`

## In-Memory Adapter Pattern

```python
# tests/unit/conftest.py
@pytest.fixture
def in_memory_process_runner():
    return InMemoryProcessRunner()

# tests/unit/usecases/test_process_manager.py
def test_start_litefs(in_memory_process_runner):
    manager = ProcessManager(runner=in_memory_process_runner)
    manager.start()
    assert in_memory_process_runner.started is True
```

## Property-Based Testing (Hypothesis)

Use for config generation and settings validation:

```bash
uv run pytest -m property -v
```

**When to use:**

| Pattern         | Property to Test          | Example                |
| --------------- | ------------------------- | ---------------------- |
| **Round-trip**  | `parse(generate(x)) == x` | Config YAML generation |
| **Invariants**  | Bounds always hold        | Path validation        |
| **Idempotence** | `f(f(x)) == f(x)`         | Settings normalization |

```python
from hypothesis import given, strategies as st

@pytest.mark.property
@given(mount_path=st.text(min_size=1).filter(lambda x: x.startswith("/")))
def test_config_includes_mount_path(mount_path):
    settings = LiteFSSettings(mount_path=mount_path)
    config = ConfigGenerator().generate(settings)
    assert mount_path in config
```








