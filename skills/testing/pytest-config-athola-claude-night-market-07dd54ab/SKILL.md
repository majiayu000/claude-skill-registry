---
name: pytest-config
description: |

Triggers: fixtures, config, configuration, pytest, testing
  Standardized pytest configuration for plugin development with shared test patterns.

  Triggers: pytest configuration, conftest, fixtures, test setup
  Use when: setting up pytest for plugin development or creating fixtures
category: infrastructure
tags: [pytest, testing, configuration, fixtures]
dependencies: [leyline:testing-quality-standards]
estimated_tokens: 200
provides:
  infrastructure: [pytest-config, conftest-patterns, coverage-config]
modules:
  - modules/conftest-patterns.md
  - modules/git-testing-fixtures.md
  - modules/mock-fixtures.md
  - modules/ci-integration.md
version: 1.3.5
---
## Table of Contents

- [Quick Start](#quick-start)
- [Detailed Patterns](#detailed-patterns)
- [Integration with Other Skills](#integration-with-other-skills)
- [Exit Criteria](#exit-criteria)
- [Troubleshooting](#troubleshooting)

# Pytest Configuration Patterns

Standardized pytest configuration and patterns for consistent testing infrastructure across Claude Night Market plugins.

## Quick Start

### Basic pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
    "--strict-markers",
]
markers = [
    "unit: marks tests as unit tests",
    "integration: marks tests as integration tests",
    "slow: marks tests as slow running",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/migrations/*", "*/__pycache__/*"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "def __str__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
precision = 2
show_missing = true
```
**Verification:** Run `pytest -v` to verify tests pass.

## Detailed Patterns

For detailed implementation patterns, see:

- **[Conftest Patterns](modules/conftest-patterns.md)** - Conftest.py templates, fixtures, test markers, and directory structure
- **[Git Testing Fixtures](modules/git-testing-fixtures.md)** - GitRepository helper class for testing git workflows
- **[Mock Fixtures](modules/mock-fixtures.md)** - Mock tool fixtures for Bash, TodoWrite, and other Claude Code tools
- **[CI Integration](modules/ci-integration.md)** - GitHub Actions workflows and test commands for automated testing
- **Module Index**: See `modules/README.md` for module organization overview

## Integration with Other Skills

This skill provides foundational patterns referenced by:
- `parseltongue:python-testing` - Uses pytest configuration and fixtures
- `pensive:test-review` - Uses test quality standards
- `sanctum:test-*` - Uses conftest patterns and Git fixtures

Reference in your skill's frontmatter:
```yaml
dependencies: [leyline:pytest-config, leyline:testing-quality-standards]
```
**Verification:** Run `pytest -v` to verify tests pass.

## Exit Criteria

- pytest configuration standardized across plugins
- conftest.py provides reusable fixtures
- test markers defined and documented
- coverage configuration enforces quality thresholds
- CI/CD integration configured for automated testing
## Troubleshooting

### Common Issues

**Tests not discovered**
Ensure test files match pattern `test_*.py` or `*_test.py`. Run `pytest --collect-only` to verify.

**Import errors**
Check that the module being tested is in `PYTHONPATH` or install with `pip install -e .`

**Async tests failing**
Install pytest-asyncio and decorate test functions with `@pytest.mark.asyncio`
