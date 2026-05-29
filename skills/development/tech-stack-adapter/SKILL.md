---
name: tech-stack-adapter
version: 5.0.0
description: |
  Detects Python project configuration and provides commands for
  testing, building, coverage, and containerization.

  Use when: Starting workflow, detecting project stack, need TEST_CMD

  Triggers: detect stack, what commands, initial setup

  Outputs: TEST_CMD, BUILD_CMD, COVERAGE_CMD, COVERAGE_CHECK, MIGRATE_CMD
---

# Tech Stack Adapter

## Purpose

One-time detection of Python/uv project configuration. Returns standardized
commands for use throughout workflow.

## Detection Script

Run `scripts/detect_stack.py` to analyze the project and generate command configuration.

## Usage in Workflow

```bash
# Run once at workflow start
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py > /tmp/stack_config.json

# Access in other skills
export TEST_CMD=$(jq -r '.test_cmd' /tmp/stack_config.json)
export BUILD_CMD=$(jq -r '.build_cmd' /tmp/stack_config.json)
export COVERAGE_CHECK=$(jq -r '.coverage_check' /tmp/stack_config.json)
```

## Output Format

```json
{
  "stack": "python",
  "package_manager": "uv",
  "project_name": "project-name",
  "repo_root": "/path/to/repo",
  "install_cmd": "uv sync",
  "test_cmd": "uv run pytest",
  "build_cmd": "uv build",
  "coverage_cmd": "uv run pytest --cov=src --cov-report=term",
  "coverage_check": "uv run pytest --cov=src --cov-report=term --cov-fail-under=80",
  "database": "sqlite",
  "orm": "sqlalchemy",
  "migrate_cmd": "uv run alembic upgrade head",
  "container": "podman",
  "has_containerfile": false,
  "has_compose": false,
  "test_framework": "pytest",
  "has_pytest_cov": true
}
```

## Detected Configuration

The script detects:

- **Package manager**: uv or pip
- **Test framework**: pytest, unittest, or none
- **Coverage tool**: pytest-cov presence
- **Database**: SQLite, PostgreSQL (via SQLAlchemy), or none
- **ORM**: SQLAlchemy, none
- **Migrations**: Alembic presence
- **Container**: Containerfile and podman-compose.yml existence

## Integration with Other Skills

All other skills should call this detector first to get project-specific commands:

```python
import json
import subprocess

# Run detector
result = subprocess.run(
    ['python', '.claude/skills/tech-stack-adapter/scripts/detect_stack.py'],
    capture_output=True,
    text=True
)

config = json.loads(result.stdout)

# Use detected commands
subprocess.run(config['test_cmd'].split())
subprocess.run(config['coverage_check'].split())
```
