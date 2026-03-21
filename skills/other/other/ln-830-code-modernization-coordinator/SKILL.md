---
name: ln-830-code-modernization-coordinator
description: "Modernizes codebase via OSS replacement and bundle optimization. Use when acting on audit findings to reduce custom code."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# ln-830-code-modernization-coordinator

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization

Coordinates code modernization by delegating to L3 workers: ln-831 (OSS replacer) and ln-832 (bundle optimizer). Executes migration plans from 6XX audit findings.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Audit report (ln-645 migration plan) OR target module |
| **Output** | Modernized codebase with verification proof |
| **Workers** | ln-831 (OSS replacer), ln-832 (bundle optimizer) |

---

## Workflow

**Phases:** Pre-flight → Analyze Input → Delegate → Collect → Verify → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Audit report OR target module | Yes | Block modernization |
| Git clean state | Yes | Block (need clean baseline for revert) |
| Test infrastructure | Yes | Block (workers need tests for keep/discard) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for test/build detection.

---

## Phase 1: Analyze Input

### Worker Selection

| Condition | ln-831 | ln-832 |
|-----------|--------|--------|
| ln-645 findings present (OSS candidates) | Yes | No |
| JS/TS project with package.json | No | Yes |
| Both conditions | Yes | Yes |
| Target module specified | Yes | No |

### Stack Detection

| Indicator | Stack | ln-832 Eligible |
|-----------|-------|----------------|
| package.json + JS/TS files | JS/TS | Yes |
| *.csproj | .NET | No |
| requirements.txt / pyproject.toml | Python | No |
| go.mod | Go | No |

---

## Phase 2: Delegate to Workers

> **CRITICAL:** All delegations use Agent tool with `subagent_type: "general-purpose"` and `isolation: "worktree"` — each worker creates its own branch per `shared/references/git_worktree_fallback.md`.

### Delegation Protocol

```
FOR each selected worker:
  Agent(description: "Modernize via ln-83X",
       prompt: "Execute modernization worker.

Step 1: Invoke worker:
  Skill(skill: \"ln-83X-{worker}\")

CONTEXT:
{delegationContext}",
       subagent_type: "general-purpose",
       isolation: "worktree")
```

### Delegation Context

| Field | Type | Description |
|-------|------|-------------|
| projectPath | string | Absolute path to project |
| auditReport | string | Path to codebase_audit.md (if applicable) |
| targetModule | string | Target module path (if applicable) |
| options.runTests | bool | Run tests after modernization |

### Execution Order

| Order | Worker | Reason |
|-------|--------|--------|
| 1 | ln-831 (OSS replacer) | May add/remove packages, affecting bundle |
| 2 | ln-832 (bundle optimizer) | Runs AFTER package changes are settled |

**Rules:**
- Workers run sequentially — ln-831 package changes affect ln-832 baseline.
- **Dependent workers share branch:** ln-832 launches in ln-831's branch so it sees OSS replacement changes.

---

## Phase 3: Collect Results

Each worker produces an isolated branch. Coordinator aggregates branch reports.

### Worker Branches

| Worker | Branch Pattern | Contents |
|--------|---------------|----------|
| ln-831 | `modernize/ln-831-{module}-{ts}` | OSS replacements |
| ln-832 | `modernize/ln-832-bundle-{ts}` | Bundle optimizations |

### Result Schema

| Field | Type | Description |
|-------|------|-------------|
| worker | string | ln-831 or ln-832 |
| status | enum | success, partial, failed |
| branch | string | Worker's result branch name |
| changes_applied | int | Number of kept changes |
| changes_discarded | int | Number of discarded attempts |
| details | object | Worker-specific report |

---

## Phase 4: Aggregate Reports

Each worker verified independently in its branch (tests, build run by worker itself). Coordinator does NOT rerun verification or revert worker changes.

### On Failure

1. Branch with failing tests logged as "failed" in report
2. User reviews failed branch independently

---

## Phase 5: Report Summary

### Report Schema

| Field | Description |
|-------|-------------|
| input_source | Audit report or target module |
| workers_activated | Which workers ran |
| modules_replaced | OSS replacements applied (ln-831) |
| loc_removed | Custom code lines removed (ln-831) |
| bundle_reduction | Bundle size reduction in bytes/% (ln-832) |
| build_verified | PASSED or FAILED |
| per_worker[] | Individual worker reports |

---

## Configuration

```yaml
Options:
  # Input
  audit_report: "docs/project/codebase_audit.md"
  target_module: ""

  # Workers
  enable_oss_replacer: true
  enable_bundle_optimizer: true

  # Verification
  run_tests: true
  run_build: true

  # Safety
  revert_on_build_failure: true
```

---

## Error Handling

### Recoverable Errors

| Error | Recovery |
|-------|----------|
| ln-831 failure | Continue with ln-832 |
| ln-832 failure | Report partial success (ln-831 results valid) |
| Build failure | Revert last worker, re-verify |

### Fatal Errors

| Error | Action |
|-------|--------|
| No workers activated | Report "no modernization targets found" |
| All workers failed | Report failures, suggest manual review |
| Dirty git state | Block with "commit or stash changes first" |

---

## References

- `../ln-831-oss-replacer/SKILL.md`
- `../ln-832-bundle-optimizer/SKILL.md`
- `../ln-645-open-source-replacer/SKILL.md` (audit companion)
- `shared/references/ci_tool_detection.md`

---

## Definition of Done

- [ ] Input analyzed (audit report or target module)
- [ ] Appropriate workers selected based on input and stack
- [ ] Workers delegated with worktree isolation (`isolation: "worktree"`, ln-831 before ln-832)
- [ ] Each worker produces isolated branch, pushed to remote
- [ ] Coordinator report aggregates per-worker results (branch, changes, status)

---

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `optimization-coordinator`. Run after all phases complete. Output to chat using the `optimization-coordinator` format.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
