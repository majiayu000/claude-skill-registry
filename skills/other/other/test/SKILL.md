---
name: test
description: Runs automated tests to validate plugin integrity across 14 categories. Use before creating PRs, after making changes to skills or templates, or to verify plugin health.
argument-hint: [all | config | skills | templates | workflow | suno | research | mastering | sheet-music | release | consistency | terminology | behavior | quality | quick]
model: claude-haiku-4-5-20251001
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

## Your Task

**Input**: $ARGUMENTS

Run automated tests to validate plugin integrity. Execute each test methodically and report results clearly.

**Default**: Run all tests if no argument provided.

---

# Plugin Test Suite

You are the plugin's automated test runner. Execute each test, track pass/fail, and report actionable results.

## Quick Automated Tests (`/test quick`)

For fast automated validation, run the pytest suite:

```bash
python3 -m pytest tests/ -v
```

This covers:
- **plugin tests** (`tests/plugin/`) - Frontmatter, templates, references, links, terminology, consistency, config, state, genres, integration
- **unit tests** (`tests/unit/`) - State parsers/indexer, shared utilities, mastering functions

Run specific categories:
```bash
python3 -m pytest tests/plugin/test_skills.py -v       # Skills only
python3 -m pytest tests/plugin/ -v                      # All plugin tests
python3 -m pytest tests/unit/ -v                        # All unit tests
python3 -m pytest tests/ -m "not slow" -v               # Skip slow tests
```

Pytest catches common issues fast. For deep behavioral tests, use the full test suite below.

## Output Format

```
════════════════════════════════════════
CATEGORY: Test Category Name
════════════════════════════════════════

[PASS] Test name
[FAIL] Test name
       → Problem: what's wrong
       → File: path/to/file:line
       → Fix: specific fix instruction

────────────────────────────────────────
Category: X passed, Y failed
────────────────────────────────────────
```

At the end:
```
════════════════════════════════════════
FINAL RESULTS
════════════════════════════════════════
config:       X passed, Y failed
skills:       X passed, Y failed
templates:    X passed, Y failed
...
────────────────────────────────────────
TOTAL:        X passed, Y failed, Z skipped
════════════════════════════════════════
```

---


# TEST CATEGORIES

All test definitions are in [test-definitions.md](test-definitions.md).

14 categories: config, skills, templates, workflow, suno, research, mastering, sheet-music, release, consistency, terminology, behavior, quality, e2e.

Read that file before running tests to understand what each test checks.

---

# RUNNING TESTS

## Commands

| Command | Description |
|---------|-------------|
| `/test` or `/test all` | Run all tests |
| `/test quick` | Run Python test runner (fast automated checks) |
| `/test config` | Configuration system tests |
| `/test skills` | Skill definitions and docs |
| `/test templates` | Template file tests |
| `/test workflow` | Album workflow documentation |
| `/test suno` | Suno integration tests |
| `/test research` | Research workflow tests |
| `/test mastering` | Mastering workflow tests |
| `/test sheet-music` | Sheet music generation tests |
| `/test release` | Release workflow tests |
| `/test consistency` | Cross-reference checks |
| `/test terminology` | Consistent language tests |
| `/test behavior` | Scenario-based tests |
| `/test quality` | Code quality checks |
| `/test e2e` | End-to-end integration test |

## Quick Tests via Pytest

For rapid validation during development, use pytest directly:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test modules
python3 -m pytest tests/plugin/test_skills.py tests/plugin/test_templates.py -v

# Verbose with short tracebacks
python3 -m pytest tests/ -v --tb=short

# Quiet mode (for CI/logs)
python3 -m pytest tests/ -q --tb=line
```

Test modules in `tests/plugin/`:
- `test_skills.py` - Frontmatter, required fields, model validation
- `test_templates.py` - Template existence and structure
- `test_references.py` - Reference doc existence
- `test_links.py` - Internal markdown links
- `test_terminology.py` - Deprecated terms check
- `test_consistency.py` - Version sync, skill counts
- `test_config.py` - Config file validation
- `test_state.py` - State cache tool validation
- `test_genres.py` - Genre directory cross-reference
- `test_integration.py` - Cross-skill prerequisite chains

## Adding New Tests

When bugs are found:
1. Identify which category the test belongs to
2. Add a test that would have caught the bug
3. Run `/test [category]` to verify test fails
4. Fix the bug
5. Run `/test [category]` to verify test passes
6. Commit both the fix and the new test

**Rule:** Every bug fix should add a regression test.

---

# EXECUTION TIPS

- Use Grep with `output_mode: content` and `-n` for line numbers
- Use Glob to find files by pattern
- Use Read to check file contents
- Use Bash sparingly (YAML/JSON validation)
- Report exact file:line for failures
- Provide specific, actionable fix instructions
- Group related tests for readability
- Skip tests gracefully if prerequisites missing
