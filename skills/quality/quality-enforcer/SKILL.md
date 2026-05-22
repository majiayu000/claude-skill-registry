---
name: quality-enforcer
version: 5.0.0
description: |
  Enforces quality gates: 80% test coverage, passing tests, successful builds,
  semantic versioning. Runs before PR creation.

  Use when: Running tests, checking coverage, validating quality, versioning

  Triggers: run tests, check coverage, quality gates, version bump
---

# Quality Enforcer

## Purpose

Ensures code quality standards are met before integration. Enforces:
- Test coverage ≥ 80%
- All tests passing
- Successful builds
- Linting clean (ruff)
- Type checking clean (mypy)
- Container health (if applicable)

## Scripts

### check_coverage.py

Runs pytest with coverage and verifies 80% threshold.

```bash
python .claude/skills/quality-enforcer/scripts/check_coverage.py [threshold]
```

**Arguments:**
- `threshold` (optional): Coverage percentage required (default: 80)

**Exit codes:**
- 0: Coverage meets threshold
- 1: Coverage below threshold or error

### run_quality_gates.py

Runs all quality gates and reports comprehensive results.

```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Checks:**
1. Test coverage (≥80%)
2. All tests passing
3. Build successful
4. Linting clean
5. Type checking clean

**Exit codes:**
- 0: All gates passed
- 1: One or more gates failed

## Quality Gates

### Gate 1: Test Coverage

Minimum 80% code coverage required.

```bash
uv run pytest --cov=src --cov-report=term --cov-fail-under=80
```

### Gate 2: All Tests Passing

All unit and integration tests must pass.

```bash
uv run pytest -v
```

### Gate 3: Successful Build

Package must build without errors.

```bash
uv build
```

### Gate 4: Linting

Code must pass ruff linting.

```bash
uv run ruff check src/ tests/
```

### Gate 5: Type Checking

Code must pass mypy type checking.

```bash
uv run mypy src/
```

## Integration with Workflow

The workflow-orchestrator calls this skill before PR creation:

```python
# In workflow orchestrator
if current_phase == 3:  # Quality Assurance
    load_skill('quality-enforcer')

    result = subprocess.run([
        'python',
        '.claude/skills/quality-enforcer/scripts/run_quality_gates.py'
    ])

    if result.returncode != 0:
        print("⚠️  Quality gates failed - fix issues before creating PR")
        return False

    print("✓ All quality gates passed")
```

## Semantic Versioning

Uses git-workflow-manager's semantic_version.py to calculate version bumps.

```python
# Calculate new version
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/semantic_version.py',
    'develop',  # base branch
    'v1.0.0'    # current version
], capture_output=True, text=True)

new_version = result.stdout.strip()
```

## Updating TODO with Version

```python
# Update TODO file with new semantic version
import yaml
from pathlib import Path

def update_version_in_todo(todo_file, new_version):
    """Update semantic_version in TODO file YAML frontmatter."""

    content = Path(todo_file).read_text()
    parts = content.split('---', 2)
    frontmatter = yaml.safe_load(parts[1])
    body = parts[2]

    frontmatter['quality_gates']['semantic_version'] = new_version

    new_content = f"---\n{yaml.dump(frontmatter)}---{body}"
    Path(todo_file).write_text(new_content)
```

## Best Practices

- Run quality gates frequently during development
- Fix issues immediately - don't accumulate technical debt
- Aim for >80% coverage, not just exactly 80%
- Write tests alongside implementation
- Use type hints consistently
- Keep linting rules reasonable but enforce them
