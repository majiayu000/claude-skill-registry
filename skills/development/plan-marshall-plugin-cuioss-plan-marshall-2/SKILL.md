---
name: plan-marshall-plugin
description: Python domain extension with pyprojectx build operations and workflow integration
user-invocable: false
allowed-tools: Read, Bash
---

# Plan Marshall Plugin - Python Domain

Domain extension providing Python development capabilities to plan-marshall workflows, including pyprojectx build execution with output parsing.

## Purpose

- Domain identity and workflow extensions
- Build execution via pyprojectx (`./pw` wrapper)
- Module detection for Python projects
- Profile-based skill organization

## Extension API

Configuration in `extension.py` implements the Extension API contract:

| Function | Purpose |
|----------|---------|
| `get_skill_domains()` | Domain metadata with profiles |
| `provides_triage()` | Returns `None` (future: ext-triage-python) |
| `discover_modules(project_root)` | Discover Python modules via pyproject.toml |

---

## Scripts Overview

| Script | Type | Purpose |
|--------|------|---------|
| `extension.py` | Extension | ExtensionBase implementation |
| `python_build.py` | CLI + Library | pyprojectx operations, `execute_direct()` |

---

## Mutual Exclusivity

This extension is **mutually exclusive** with `pm-plugin-development:plan-marshall-plugin` for module discovery:

| Project Type | Handled By |
|-------------|------------|
| plan-marshall marketplace | `pm-plugin-development` |
| Other Python projects | `pm-dev-python` (this extension) |

Detection uses `marketplace/.claude-plugin/marketplace.json`:
- If `name` field equals `"plan-marshall"` → skip (pm-plugin-development handles it)
- Otherwise → this extension provides module discovery

This avoids duplicate modules when both extensions are active.

---

## Runtime Discovery

The extension discovers available commands by parsing `pyproject.toml`:

```
1. Skip if this is the plan-marshall marketplace (detected via marketplace.json)
2. Check pyproject.toml exists
3. Parse [tool.pyprojectx.aliases] section (using tomllib)
4. Map aliases to canonical commands
5. Check ./pw wrapper exists
6. Return module with discovered commands
```

**Detected aliases mapped to canonical commands:**
- `compile` → mypy on production sources
- `test-compile` → mypy on test sources
- `module-tests` → pytest
- `quality-gate` → ruff check
- `verify` → Full verification
- `coverage` → pytest with coverage
- `clean` → Remove artifacts

---

## Wrapper Detection

Commands are executed via the pyprojectx wrapper:

```
./pw > pwx (system pyprojectx)
```

The `detect_wrapper(project_dir)` function checks for the `pw` script in the project root before falling back to system pyprojectx.

---

## Timeout Learning

Command durations are recorded for adaptive timeouts:

```python
# Before execution
timeout = timeout_get("python:verify", default=300, project_dir=".")
# Returns: learned * 1.25 or default

# After execution
timeout_set("python:verify", duration=45, project_dir=".")
# Updates .plan/run-configuration.json
```

---

## Build Operations

### python_build run (Primary API)

Unified command that executes build and returns parsed output on failure.

```bash
python3 .plan/execute-script.py pm-dev-python:plan-marshall-plugin:python_build run \
    --commandArgs "<canonical-command>" \
    [--format <toon|json>] \
    [--mode <mode>] \
    [--timeout <seconds>]
```

**Parameters**:
- `--commandArgs` - Canonical command to execute (required)
- `--format` - Output format: toon (default) or json
- `--mode` - Output mode: actionable (default), structured, errors
- `--timeout` - Timeout in seconds (default from run-config)

**Output Format (TOON)**:

Success:
```
status	success
exit_code	0
duration_seconds	12
log_file	.plan/temp/build-output/default/python-2026-01-14-143022.log
command	./pw verify
```

Build Failed:
```
status	error
exit_code	1
duration_seconds	8
log_file	.plan/temp/build-output/default/python-2026-01-14-143022.log
command	./pw module-tests
error	build_failed

errors[2]{file,line,message,category}:
test/test_foo.py	42	AssertionError: expected True	test_failure
src/bar.py	15	error: Incompatible types	type_error

tests:
  passed: 40
  failed: 2
  skipped: 0
```

---

## Output Modes

- **actionable** (default) - Errors + warnings NOT in acceptable_warnings
- **structured** - All errors + all warnings with `[accepted]` markers
- **errors** - Only errors, compact format

## Error Categories

| Category | Description |
|----------|-------------|
| `type_error` | mypy type errors |
| `lint_error` | ruff violations |
| `test_failure` | pytest test failures |
| `import_error` | Module import errors |

## Error Codes

| Code | Meaning | Recovery |
|------|---------|----------|
| `build_failed` | Non-zero exit code | Errors included in response |
| `timeout` | Exceeded timeout | Increase timeout, check log_file |
| `execution_failed` | Process couldn't start | Check ./pw exists |
| `log_file_creation_failed` | Can't create log | Check permissions |

---

## Integration

This extension is discovered by:
- `extension-api` - Build system detection and command generation
- `skill-domains` - Domain configuration
- `marshall-steward` - Project setup wizard

## References

- `plan-marshall:extension-api` - Extension API contract
- `plan-marshall:extension-api/standards/build-execution-flow.md` - Complete execution lifecycle
