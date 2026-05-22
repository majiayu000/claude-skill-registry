---
name: pytest-fixtures
description: Pytest fixture design, conftest.py hierarchy, and DRY test code patterns. Identifies duplicate fixtures, plans fixture scope, and designs conftest.py structure. Use when creating test directories, refactoring test fixtures, or reviewing test code for duplication.
---

# Pytest Fixtures

Fixture management and conftest.py design for Python test suites.

## When to Use

- Creating new test directories
- Refactoring test fixtures
- Reviewing tests for DRY violations
- Planning fixture hierarchy

## MCP Workflow

```python
# 1. Find existing conftest files
serena.search_for_pattern("conftest\\.py", paths_include_glob="**/tests/**")

# 2. Identify fixture definitions
serena.search_for_pattern("@pytest\\.fixture", paths_include_glob="**/tests/**")

# 3. Find duplicate fixture names
jetbrains.search_in_files_by_text("def sample_", fileMask="test_*.py")

# 4. Check existing helpers
serena.get_symbols_overview(relative_path="tests/")
```

## Fixture Hierarchy

```
tests/
├── conftest.py           # Shared across ALL tests
│   └── Fixtures: session-scoped, DB connections, API clients
├── cli/
│   ├── conftest.py       # CLI-specific fixtures
│   │   └── Fixtures: CLI runner, mock console, sample paths
│   └── test_*.py
└── core/
    ├── conftest.py       # Core-specific fixtures
    │   └── Fixtures: domain models, sample data
    └── {module}/
        ├── conftest.py   # Module-specific (rarely needed)
        └── test_*.py
```

## Scope Selection Guide

| Scope | Recreated | Use When |
|-------|-----------|----------|
| `function` | Each test | Default; mutable state |
| `class` | Each class | Class-based tests, shared setup |
| `module` | Each file | Expensive setup, immutable data |
| `session` | Once | DB connections, API clients |

**Rule**: Start with `function`, widen scope only for performance.

## Fixture Design Patterns

### 1. Factory Fixture (Preferred for Flexibility)

```python
@pytest.fixture
def make_user():
    """Factory that creates users with custom attributes."""
    def _make_user(name: str = "test", role: str = "user") -> User:
        return User(name=name, role=role)
    return _make_user

# Usage in test
def test_admin_access(make_user):
    admin = make_user(role="admin")
    assert admin.can_access_admin_panel()
```

### 2. Parameterized Fixture

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    """Runs test with each database type."""
    return create_connection(request.param)
```

### 3. Cleanup Fixture (yield pattern)

```python
@pytest.fixture
def temp_file(tmp_path):
    """Provides temp file and cleans up after test."""
    path = tmp_path / "test.txt"
    path.write_text("content")
    yield path
    # Cleanup happens after test
```

## Duplicate Detection Checklist

Run before creating fixtures:

```bash
# Find fixtures with same name
grep -r "@pytest.fixture" tests/ | grep "def " | cut -d: -f2 | sort | uniq -d

# Find common helper patterns
grep -rh "def get_output\|def create_\|def make_\|def sample_" tests/
```

## conftest.py Planning

### Before Creating New Test Directory

1. **Check parent conftest** - What fixtures already exist?
2. **Identify shared fixtures** - What 2+ tests need?
3. **Plan fixture scope** - Function/module/session?
4. **Document dependencies** - What does each fixture need?

### conftest.py Template

```python
"""
Fixtures for {directory} tests.

Shared fixtures:
- {fixture_name}: {description}

Dependencies:
- Uses: {parent_fixture} from parent conftest
"""
import pytest

@pytest.fixture
def fixture_name():
    """One-line description."""
    return value
```

## DRY Violation Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Same fixture in 2+ files | Maintenance burden | Move to shared conftest |
| `get_output()` in multiple files | Helper duplication | Create `helpers.py` |
| Copy-paste setup code | Test fragility | Factory fixture |
| Inline data creation | Readability | Data fixtures |

## Helper Function Consolidation

```
tests/
├── conftest.py       # Fixtures only
├── helpers.py        # Shared utility functions
│   ├── get_output()
│   ├── assert_table_contains()
│   └── create_mock_response()
└── fixtures/         # Complex fixture data
    ├── sample_metrics.json
    └── sample_datasets.yaml
```

## Output Format

```markdown
## Fixture Analysis: {directory}

### Existing Fixtures
| Location | Fixture | Scope | Used By |
|----------|---------|-------|---------|
| tests/conftest.py | db_session | session | 15 tests |
| tests/cli/conftest.py | cli_runner | function | 8 tests |

### Issues Found
1. **Duplicate**: `sample_project_path` in test_a.py and test_b.py
   - Action: Move to tests/cli/conftest.py

2. **Missing conftest**: tests/core/workflow/ has no conftest
   - Action: Create with shared fixtures

### Recommendations
- [ ] Create tests/cli/conftest.py with: cli_runner, mock_console
- [ ] Move get_output() to tests/helpers.py
- [ ] Change db_session scope from function to module
```

## Quality Checklist

- [ ] No duplicate fixture definitions across files
- [ ] Fixtures use narrowest appropriate scope
- [ ] conftest.py exists for directories with 3+ test files
- [ ] Helper functions in helpers.py, not test files
- [ ] Fixtures have docstrings explaining purpose
- [ ] Factory pattern used for flexible data creation
