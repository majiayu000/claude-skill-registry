---
name: ln-831-oss-replacer
description: "Replaces custom modules with OSS packages using atomic keep/discard testing. Use when migrating custom code to established libraries."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# ln-831-oss-replacer

**Type:** L3 Worker
**Category:** 8XX Optimization
**Parent:** ln-830-code-modernization-coordinator

Executes OSS replacement plans from ln-645-open-source-replacer auditor. For each custom module with an OSS alternative: install package, rewrite imports, run tests, keep or discard atomically.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Migration plan from `docs/project/codebase_audit.md` (ln-645 section) OR target module |
| **Output** | Replaced modules, migration report |
| **Companion** | ln-645-open-source-replacer (finds candidates) → ln-831 (executes replacement) |

---

## Workflow

**Phases:** Pre-flight → Load Plan → Prioritize → Replace Loop → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Migration plan OR target module | Yes | Block replacement |
| Test infrastructure | Yes | Block (need tests for verification) |
| Package manager available | Yes | Block (need to install OSS packages) |
| Git clean state | Yes | Block (need clean baseline for revert) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` — use Test Frameworks section for test detection.

### Worktree & Branch Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use ln-831 row.

---

## Phase 1: Load Migration Plan

### From Audit Report

Read `docs/project/codebase_audit.md`, extract ln-645 findings:

| Field | Description |
|-------|-------------|
| custom_module | Path to custom implementation |
| loc | Lines of code in custom module |
| oss_package | Recommended OSS replacement |
| confidence | How well OSS covers functionality (HIGH/MEDIUM/LOW) |
| api_mapping | Custom function → OSS equivalent |

### From Target Module

If no audit report: analyze target module, search Context7/Ref for OSS alternatives.

**MANDATORY READ:** Load `shared/references/research_tool_fallback.md` for MCP tool chain.

---

## Phase 2: Prioritize Replacements

| Priority | Criteria |
|----------|----------|
| 1 (highest) | HIGH confidence + >200 LOC (max code reduction) |
| 2 | HIGH confidence + 100-200 LOC |
| 3 | MEDIUM confidence + >200 LOC |
| 4 | MEDIUM confidence + 100-200 LOC |
| Skip | LOW confidence (too risky for automated replacement) |

---

## Phase 3: Replace Loop (Keep/Discard)

### Per-Module Cycle

```
FOR each replacement candidate (R1..RN):
  1. INSTALL: Add OSS package
     npm install {package} / dotnet add package / pip install
  2. REWRITE: Update imports + call sites using api_mapping
  3. VERIFY: Run tests
     IF tests FAIL → DISCARD (revert ALL: uninstall package, restore files) → next
  4. TESTS PASS → KEEP
  5. DELETE: Remove old custom module (only after keep)
  6. LOG: Record replacement for report
```

### Stop Conditions (Replace Loop)

| Condition | Action |
|-----------|--------|
| All candidates processed | STOP — proceed to Report |
| 3 consecutive DISCARDs | WARN — "3 replacements failed in a row. Continue?" |
| Test infrastructure breaks (suite itself fails) | STOP — revert all, report last known good state |
| No candidates above confidence threshold | STOP — report "no viable replacements found" |

### Atomic Revert on Discard

| Step | Revert Action |
|------|---------------|
| Package installed | Uninstall: `npm uninstall` / `dotnet remove package` / `pip uninstall` |
| Files modified | `git checkout -- {modified_files}` |
| Lock file changed | `git checkout -- {lock_file}` |

### Safety Rules

| Rule | Description |
|------|-------------|
| One module at a time | Never replace multiple modules simultaneously |
| No API signature changes | Public API of replaced module must stay compatible |
| Tests required | Skip module if no tests cover it (too risky) |
| Confidence gate | Skip LOW confidence replacements |

---

## Phase 4: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| source | Audit report path or target module |
| candidates_total | Total replacement candidates |
| replacements_applied | Successfully replaced modules |
| replacements_discarded | Failed replacements with reasons |
| replacements_skipped | LOW confidence / no test coverage |
| loc_removed | Total lines of custom code removed |
| packages_added | New OSS packages installed |
| details[] | Per-replacement: module, package, LOC removed |

---

## Configuration

```yaml
Options:
  # Source
  audit_report: "docs/project/codebase_audit.md"
  target_module: ""

  # Confidence
  min_confidence: "MEDIUM"      # MEDIUM | HIGH

  # Verification
  run_tests: true

  # Safety
  require_test_coverage: true   # Skip modules with no tests
  delete_old_module: true       # Delete custom module after successful replacement
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Package not found | OSS package name changed | Search Context7/Ref for current name |
| API mismatch | OSS API differs from mapping | Query docs for correct API, attempt fix |
| Circular dependency | New package conflicts | Skip replacement, log as manual |
| No test coverage | Custom module untested | Skip (too risky for automated replacement) |

---

## References

- `../ln-645-open-source-replacer/SKILL.md` (companion: finds candidates)
- `shared/references/ci_tool_detection.md` (test detection)
- `shared/references/research_tool_fallback.md` (MCP tool chain)

---

## Definition of Done

- [ ] Migration plan loaded from audit report or target module analyzed
- [ ] Candidates prioritized by confidence + LOC
- [ ] Each replacement applied atomically: install → rewrite → test → keep/discard
- [ ] Discarded replacements fully reverted (package + files + lock)
- [ ] Kept replacements: old custom module deleted
- [ ] Report returned with candidates total, applied, discarded, LOC removed

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
