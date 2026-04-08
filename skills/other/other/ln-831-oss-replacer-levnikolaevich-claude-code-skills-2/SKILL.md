---
name: ln-831-oss-replacer
description: "Replaces custom modules with OSS packages using atomic keep/discard testing. Use when migrating custom code to established libraries."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, mcp__Ref, mcp__context7, mcp__hex-line__outline, mcp__hex-line__bulk_replace, mcp__hex-graph__find_references
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-831-oss-replacer

**Type:** L3 Worker
**Category:** 8XX Optimization

Executes OSS replacement plans from `ln-645-open-source-replacer`. For each custom module with a viable OSS alternative: install package, rewrite imports, run verification, then keep or discard atomically.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Migration plan from audit output or a target module |
| **Output** | Replaced modules plus a machine-readable modernization summary |
| **Companion** | `ln-645-open-source-replacer` identifies candidates, `ln-831` executes them |

---

## Workflow

**Phases:** Pre-flight -> Load Plan -> Prioritize -> Replace Loop -> Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Migration plan or target module | Yes | Block replacement |
| Test infrastructure | Yes | Block replacement |
| Package manager available | Yes | Block replacement |
| Workspace baseline safe | Yes | In managed runs coordinator already prepared it; in standalone runs protect rollback locally |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for test detection.

### Runtime Coordination

Managed runs receive deterministic `runId` and exact `summaryArtifactPath` from `ln-830`.
Standalone runs remain supported; if runtime arguments are omitted, generate a standalone run-scoped artifact before returning.

---

## Phase 1: Load Migration Plan

From audit report, extract:

| Field | Description |
|-------|-------------|
| `custom_module` | Path to the custom implementation |
| `loc` | Lines of code in the custom module |
| `oss_package` | Recommended OSS replacement |
| `confidence` | HIGH, MEDIUM, or LOW |
| `api_mapping` | Custom function to OSS equivalent |

If no audit report exists, analyze the target module and search Context7 or Ref for viable OSS alternatives.

**MANDATORY READ:** Load `shared/references/research_tool_fallback.md`

---

## Phase 2: Prioritize Replacements

| Priority | Criteria |
|----------|----------|
| 1 | HIGH confidence and >200 LOC |
| 2 | HIGH confidence and 100-200 LOC |
| 3 | MEDIUM confidence and >200 LOC |
| 4 | MEDIUM confidence and 100-200 LOC |
| Skip | LOW confidence |

---

## Phase 3: Replace Loop (Keep/Discard)

Per-module cycle:

```text
FOR each replacement candidate:
  1. INSTALL: add the OSS package
  2. REWRITE: update imports and call sites using api_mapping
  3. VERIFY: run tests
     IF tests fail -> DISCARD and revert all changes for this candidate
  4. KEEP: only after verification passes
  5. DELETE: remove old custom module after keep
  6. LOG: record result for the final report
```

Stop conditions:

| Condition | Action |
|-----------|--------|
| All candidates processed | Stop and report |
| 3 consecutive discards | Warn and stop for manual review |
| Test infrastructure itself breaks | Stop and revert to last known good state |
| No candidates above confidence threshold | Stop and report no viable replacements |

Atomic revert on discard:

| Step | Revert Action |
|------|---------------|
| Package installed | Uninstall it |
| Files modified | Restore module files |
| Lock file changed | Restore lock file |

Safety rules:

| Rule | Description |
|------|-------------|
| One module at a time | Never replace multiple modules simultaneously |
| No API signature drift | Public interfaces must stay compatible |
| Tests required | Skip modules with no coverage when risk is unclear |
| Confidence gate | Skip LOW-confidence replacements |

---

## Phase 4: Report Results

| Field | Description |
|-------|-------------|
| `source` | Audit report path or target module |
| `candidates_total` | Total replacement candidates |
| `replacements_applied` | Successfully replaced modules |
| `replacements_discarded` | Failed replacements with reasons |
| `replacements_skipped` | Skipped due to low confidence or missing tests |
| `loc_removed` | Total lines of custom code removed |
| `packages_added` | New OSS packages installed |
| `details[]` | Per replacement summary |
| `artifact_path` | Durable worker report path, if written |

---

## Configuration

```yaml
Options:
  audit_report: "docs/project/codebase_audit.md"
  target_module: ""
  min_confidence: "MEDIUM"
  run_tests: true
  require_test_coverage: true
  delete_old_module: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Package not found | OSS package name changed | Search current docs for the new package name |
| API mismatch | Mapping differs from real library API | Query docs and retry only if fix is clear |
| Circular dependency | New package conflicts with current architecture | Skip and report manual follow-up |
| No test coverage | Too risky for automated replacement | Skip and report |

---

## References

- `../ln-645-open-source-replacer/SKILL.md`
- `shared/references/ci_tool_detection.md`
- `shared/references/research_tool_fallback.md`

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit a `modernization-worker` summary envelope.

Managed mode:
- `ln-830` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/modernization-worker/ln-831--{identifier}.json`

## Definition of Done

- [ ] Migration plan loaded or target module analyzed
- [ ] Candidates prioritized by confidence and code-reduction value
- [ ] Each replacement executed atomically with keep/discard verification
- [ ] Discarded replacements fully reverted
- [ ] Kept replacements remove old custom code only after verification passes
- [ ] Report captures applied, discarded, skipped replacements, and LOC removed
- [ ] `modernization-worker` summary artifact written to the managed or standalone path

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
