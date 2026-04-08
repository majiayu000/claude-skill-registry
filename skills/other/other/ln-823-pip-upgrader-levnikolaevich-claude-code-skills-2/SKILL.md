---
name: ln-823-pip-upgrader
description: "Upgrades Python pip/poetry/pipenv dependencies with breaking change handling. Use when updating Python dependencies."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-823-pip-upgrader

**Type:** L3 Worker
**Category:** 8XX Optimization

Upgrades Python dependencies with automatic breaking change detection.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project path plus package manager type |
| **Output** | Updated dependency manifests and a machine-readable dependency upgrade summary |
| **Supports** | pip, poetry, pipenv |

---

## Workflow

**Phases:** Pre-flight -> Detect Manager -> Security Audit -> Check Outdated -> Apply Upgrades -> Verify Installation -> Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| `requirements.txt`, `pyproject.toml`, or `Pipfile` | Yes | Block upgrade |
| Python package manager available | Yes | Block upgrade |
| Virtual environment active | No | Warn user if managed environment is unclear |
| Workspace baseline safe | Yes | In managed runs coordinator already prepared it; in standalone runs protect rollback locally |

### Runtime Coordination

Managed runs receive deterministic `runId` and exact `summaryArtifactPath` from `ln-820`.
Standalone runs remain supported; if runtime arguments are omitted, generate a standalone run-scoped artifact before returning.

---

## Phase 1: Detect Manager

| Manager | Indicator Files |
|---------|-----------------|
| pip | `requirements.txt` |
| poetry | `pyproject.toml` + `poetry.lock` |
| pipenv | `Pipfile` + `Pipfile.lock` |

---

## Phase 2: Security Audit

| Manager | Command |
|---------|---------|
| pip | `pip-audit --json` |
| poetry | `poetry audit` |
| pipenv | `pipenv check` |

Actions:

| Severity | Action |
|----------|--------|
| Critical | Block and report |
| High | Warn and continue |
| Moderate/Low | Log only |

---

## Phase 3: Check Outdated

| Manager | Command |
|---------|---------|
| pip | `pip list --outdated --format=json` |
| poetry | `poetry show --outdated` |
| pipenv | `pipenv update --outdated` |

---

## Phase 4: Apply Upgrades

| Manager | Command |
|---------|---------|
| pip | `pip install --upgrade <package>` |
| pip (freeze) | `pip freeze > requirements.txt` |
| poetry | `poetry update` |
| pipenv | `pipenv update` |

---

## MCP Tools for Migration Search

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | `mcp__context7__query-docs` | First choice for library docs |
| 2 | `mcp__Ref__ref_search_documentation` | Official docs and PyPI |
| 3 | WebSearch | Latest info and community fixes |

Use MCP tools whenever a package upgrade crosses a major version or introduces import errors.

---

## Phase 5: Verify Installation

| Check | Command |
|-------|---------|
| Import smoke test | `python -c "import <package>"` |
| Tests | `pytest` or `python -m pytest` |

Common breaking examples:

**MANDATORY READ:** Load [breaking_changes_patterns.md](../ln-820-dependency-optimization-coordinator/references/breaking_changes_patterns.md) for shared patterns.

| Package | Breaking Version | Key Changes |
|---------|------------------|-------------|
| pydantic | 1 -> 2 | Compatibility layer required |
| sqlalchemy | 1 -> 2 | Query API changes |
| fastapi | 0.99 -> 0.100+ | Pydantic v2 alignment |

---

## Phase 6: Report Results

| Field | Description |
|-------|-------------|
| `project` | Project path |
| `packageManager` | pip, poetry, or pipenv |
| `duration` | Total time |
| `upgrades[]` | Applied upgrades |
| `verification` | Import/test verdict |
| `warnings[]` | Non-blocking issues |
| `artifact_path` | Durable worker report path, if written |

---

## Configuration

```yaml
Options:
  upgradeType: major          # major | minor | patch
  auditLevel: high
  minimumReleaseAge: 14
  pythonVersion: "3.12"
  useVirtualenv: true
  runTests: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| ImportError | Breaking API change | Search current migration docs |
| Dependency conflict | Version mismatch | Regenerate lock file or rollback offending package |

---

## References

- [breaking_changes_patterns.md](../ln-820-dependency-optimization-coordinator/references/breaking_changes_patterns.md)
- [python_venv_handling.md](references/python_venv_handling.md)

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit a `dependency-worker` summary envelope.

Managed mode:
- `ln-820` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/dependency-worker/ln-823--{identifier}.json`

## Definition of Done

- [ ] Package manager detected from project indicators
- [ ] Security audit completed for the selected Python manager
- [ ] Outdated packages identified
- [ ] Breaking changes checked via patterns plus current docs
- [ ] Upgrades applied with manifest and lock updates persisted
- [ ] Import smoke test and required tests succeed
- [ ] `dependency-worker` summary artifact written to the managed or standalone path

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
