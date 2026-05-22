---
name: quality-gates
description: Understanding and passing workflow quality gates (validate, dry, pytest, ruff, typecheck)
---

# Quality Gates Skill

Use this skill to understand what each quality gate checks and how to ensure your workflow passes all gates.

## Default Gates

### 1. validate - Structural Validation

**What it checks**:
- run.py exists and is valid Python
- PEP 723 metadata is present (`# /// script`)
- Required dependencies are declared (pydantic, rich)
- BaseWorkflow is subclassed
- run() method is implemented
- Imported tools exist in tools/ directory

**Common failures**:
```
✗ Missing PEP 723 metadata block
✗ run.py must subclass BaseWorkflow
✗ Workflow class must implement run() method
✗ Tool not found: yahoo_finance (imported from tools.yahoo_finance)
```

**How to fix**:
- Add PEP 723 block at top of run.py
- Ensure class inherits from `BaseWorkflow[ParamsType]`
- Implement `def run(self) -> int:` method
- Create missing tools in tools/ directory

### 2. dry - Dry Run

**What it checks**:
- Workflow executes with mock data (no real API calls)
- dry_run.py exists and provides mocks
- No crashes or unhandled exceptions
- Returns exit code 0

**Common failures**:
```
✗ dry_run.py not found
✗ KeyError: 'api_key' (accessing env var in dry run)
✗ ConnectionError: API not available (real network call in dry run)
```

**How to fix**:
- Create dry_run.py with mock functions
- Replace all external calls with mocks
- Use DryRunContext to log mock behavior
- Test locally: `raw run workflow --dry`

## Optional Gates

### 3. pytest - Unit Tests

**What it checks**:
- All tests in test.py pass
- No test failures or errors

**Enable in .raw/config.yaml**:
```yaml
builder:
  gates:
    optional:
      pytest:
        command: "pytest test.py -v"
        timeout_seconds: 60
```

**Common failures**:
```
✗ AssertionError: Expected 0 but got 1
✗ ModuleNotFoundError: No module named 'workflow_name'
```

**How to fix**:
- Write tests that match actual behavior
- Import workflow class correctly
- Run pytest locally to debug

### 4. ruff - Linting & Formatting

**What it checks**:
- Code follows Python style guide
- No unused imports
- Consistent formatting

**Enable in .raw/config.yaml**:
```yaml
builder:
  gates:
    optional:
      ruff:
        command: "ruff check . && ruff format . --check"
        timeout_seconds: 30
```

**Common failures**:
```
✗ F401 'sys' imported but unused
✗ E501 Line too long (92 > 88 characters)
```

**How to fix**:
- Remove unused imports
- Run `ruff format .` to auto-format
- Run `ruff check --fix .` for auto-fixes

### 5. typecheck - Type Validation

**What it checks**:
- Type hints are correct
- No type mismatches

**Enable in .raw/config.yaml**:
```yaml
builder:
  gates:
    optional:
      typecheck:
        command: "mypy run.py"
        timeout_seconds: 60
```

## Gate Failure Strategy

When gates fail:

1. **Read the error message carefully**
   - Gate output is saved to `.raw/builds/<build_id>/logs/<gate>.log`
   - Contains full error details

2. **Fix one gate at a time**
   - Start with `validate` (structural issues)
   - Then `dry` (runtime issues)
   - Finally optional gates (quality issues)

3. **Test locally before rebuilding**
   ```bash
   raw validate workflow-id  # Check validation
   raw run workflow-id --dry # Check dry run
   pytest test.py            # Check tests
   ```

4. **Common patterns**:
   - validate fails → Fix run.py structure
   - dry fails → Add/fix mocks in dry_run.py
   - pytest fails → Fix tests or implementation
   - ruff fails → Run auto-formatters
   - typecheck fails → Add/fix type hints

## Example: Fixing Validation Failure

```
✗ Validation failed
Errors:
  • Missing PEP 723 metadata block (# /// script)
  • Tool not found: yahoo_finance (imported from tools.yahoo_finance)
```

**Steps to fix**:
1. Add PEP 723 block to run.py:
   ```python
   #!/usr/bin/env python3
   # /// script
   # requires-python = ">=3.10"
   # dependencies = ["pydantic>=2.0", "rich>=13.0", "yfinance>=0.2"]
   # ///
   ```

2. Create tools/yahoo_finance/:
   ```bash
   mkdir -p tools/yahoo_finance
   touch tools/yahoo_finance/__init__.py
   # Create tools/yahoo_finance/tool.py
   ```

3. Validate again:
   ```bash
   raw validate workflow-id
   ```
