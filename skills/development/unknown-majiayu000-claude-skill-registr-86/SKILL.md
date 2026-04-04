---
name: pytest-runner
description: Execute Python tests with pytest, supporting fixtures, markers, coverage, and parallel execution. Use for Python test automation.
tools: Read, Write, Bash
---

# Pytest Runner Skill

## Purpose

Single responsibility: Execute and manage pytest test suites with proper configuration, coverage reporting, and failure analysis. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Python virtual environment is active or available
- [ ] pytest is installed (`pip show pytest`)
- [ ] Test directory exists with test files
- [ ] pytest.ini or pyproject.toml configured (optional)

**DO NOT run tests without verifying environment.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Multiple test directories detected - which to run?
- Coverage threshold unclear
- Parallel execution appropriate?
- Specific markers or keywords needed?

**NEVER modify test configurations without user approval.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Test files, pytest config, fixtures | Application code details |
| PERIPHERAL | Coverage reports, test markers | CI/CD pipelines |
| DISTRACTOR | Other language tests | Deployment configs |

## Workflow Steps

### Step 1: Environment Check (Grounding)

```bash
# Verify virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
  # Activate if exists
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
  elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
  else
    echo "WARNING: No virtual environment active"
  fi
fi

# Verify pytest installed
python -m pytest --version || pip install pytest
```

### Step 2: Discover Tests

```bash
# List all test files
find . -name "test_*.py" -o -name "*_test.py" | head -20

# Show pytest collection
python -m pytest --collect-only -q
```

### Step 3: Execute Tests

**Basic execution:**
```bash
python -m pytest tests/ -v
```

**With coverage:**
```bash
python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

**Parallel execution:**
```bash
python -m pytest tests/ -v -n auto  # requires pytest-xdist
```

**With markers:**
```bash
python -m pytest tests/ -v -m "unit"
python -m pytest tests/ -v -m "not slow"
```

### Step 4: Analyze Results

```bash
# Parse test results
python -m pytest tests/ -v --tb=short 2>&1 | tee test_results.txt

# Extract failures
grep -E "^FAILED|^ERROR" test_results.txt

# Coverage summary
python -m pytest --cov=src --cov-report=term | grep -E "^TOTAL|^Name"
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Capture test output
2. **DIAGNOSE** - Check error type:
   - `ImportError` → Check dependencies, PYTHONPATH
   - `FixtureError` → Check conftest.py
   - `CollectionError` → Check test file syntax
   - `Timeout` → Reduce test scope or add markers
3. **ADAPT** - Adjust test selection or configuration
4. **RETRY** - With narrower scope (max 3 attempts)
5. **ESCALATE** - Report failures with context

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/pytest-runner/`

```
checkpoints/pytest-runner/
├── test_collection.json     # Discovered tests
├── test_results.json        # Last run results
├── coverage_report.json     # Coverage data
└── failure_analysis.md      # Failure diagnostics
```

## Common Pytest Options

| Option | Purpose |
|--------|---------|
| `-v` | Verbose output |
| `-x` | Stop on first failure |
| `-s` | Show print statements |
| `--lf` | Run last failed tests |
| `--ff` | Run failed tests first |
| `-k "pattern"` | Filter by name pattern |
| `-m "marker"` | Filter by marker |
| `--tb=short` | Shorter tracebacks |

## Configuration Templates

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_functions = test_*
addopts = -v --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
```

**pyproject.toml:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --tb=short"
```

## References

- pytest documentation: https://docs.pytest.org/
- REF-001: Production-Grade Agentic Workflows (BP-4 single responsibility)
- REF-002: LLM Failure Modes (Archetype 1 grounding)
