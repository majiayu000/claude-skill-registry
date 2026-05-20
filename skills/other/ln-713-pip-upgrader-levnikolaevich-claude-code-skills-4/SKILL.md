---
name: ln-713-pip-upgrader
description: Upgrades Python pip/poetry/pipenv dependencies with breaking change handling
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-713-pip-upgrader

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-710-dependency-upgrader

Upgrades Python dependencies with automatic breaking change detection.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project path, package manager type |
| **Output** | Updated requirements.txt/pyproject.toml |
| **Supports** | pip, poetry, pipenv |

---

## Workflow

See [diagram.html](diagram.html) for visual workflow.

**Phases:** Pre-flight → Detect Manager → Security Audit → Check Outdated → Apply Upgrades → Verify Installation → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| requirements.txt OR pyproject.toml OR Pipfile | Yes | Block upgrade |
| Virtual environment active | No | Warn user (risk of system pollution) |

> Workers assume coordinator (ln-710) already verified git state and created backup.

---

## Phase 1: Detect Manager

| Manager | Indicator Files |
|---------|-----------------|
| pip | requirements.txt |
| poetry | pyproject.toml + poetry.lock |
| pipenv | Pipfile + Pipfile.lock |

---

## Phase 2: Security Audit

### Commands

| Manager | Command |
|---------|---------|
| pip | `pip-audit --json` |
| poetry | `poetry audit` (via plugin) |
| pipenv | `pipenv check` |

### Actions

| Severity | Action |
|----------|--------|
| Critical | Block upgrade, report |
| High | Warn, continue |
| Moderate/Low | Log only |

---

## Phase 3: Check Outdated

### Commands

| Manager | Command |
|---------|---------|
| pip | `pip list --outdated --format=json` |
| poetry | `poetry show --outdated` |
| pipenv | `pipenv update --outdated` |

---

## Phase 4: Apply Upgrades

### Commands

| Manager | Command |
|---------|---------|
| pip | `pip install --upgrade <package>` |
| pip (freeze) | `pip freeze > requirements.txt` |
| poetry | `poetry update` |
| pipenv | `pipenv update` |

---

## MCP Tools for Migration Search

### Priority Order (Fallback Strategy)

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | mcp__context7__query-docs | First choice for library docs |
| 2 | mcp__Ref__ref_search_documentation | Official docs and PyPI |
| 3 | WebSearch | Latest info, community solutions |

### Context7 Usage

| Step | Tool | Parameters |
|------|------|------------|
| 1. Find library | mcp__context7__resolve-library-id | libraryName: "pydantic" |
| 2. Query docs | mcp__context7__query-docs | query: "pydantic v1 to v2 migration breaking changes" |

### MCP Ref Usage

| Action | Tool | Query Example |
|--------|------|---------------|
| Search | mcp__Ref__ref_search_documentation | "python pydantic 2 migration guide" |
| Read | mcp__Ref__ref_read_url | URL from search results |

### WebSearch Fallback

Use when Context7/Ref return no results:
- `"<package> python <version> breaking changes migration"`
- `"<ImportError message> <package> fix"`

---

## Phase 5: Verify Installation

### Commands

| Check | Command |
|-------|---------|
| Import test | `python -c "import <package>"` |
| Tests | `pytest` or `python -m pytest` |

---

## Phase 6: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| project | Project path |
| packageManager | pip, poetry, or pipenv |
| duration | Total time |
| upgrades[] | Applied upgrades |
| verification | PASSED or FAILED |

---

## Common Breaking Changes

**MANDATORY READ:** Load [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md) for full patterns.

| Package | Breaking Version | Key Changes |
|---------|------------------|-------------|
| pydantic | 1 → 2 | V1 compatibility layer needed |
| sqlalchemy | 1 → 2 | Query syntax changes |
| fastapi | 0.99 → 0.100+ | Pydantic v2 required |

---

## Configuration

```yaml
Options:
  # Upgrade scope
  upgradeType: major          # major | minor | patch

  # Security
  auditLevel: high
  minimumReleaseAge: 14

  # Python specific
  pythonVersion: "3.12"
  useVirtualenv: true

  # Verification
  runTests: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| ImportError | Breaking API change | Search Context7/Ref for migration |
| Dependency conflict | Version mismatch | Try pip-compile or poetry lock |

---

## References

- [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md)
- [python_venv_handling.md](references/python_venv_handling.md)

---

## Definition of Done

- Package manager detected (pip/poetry/pipenv) from indicator files
- Security audit completed (pip-audit/poetry audit/pipenv check)
- Outdated packages identified and listed
- Upgrades applied with requirements.txt/pyproject.toml updated
- Breaking changes handled via MCP migration guides
- Import tests and pytest pass after upgrades
- Report returned with upgrades applied and verification status

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
