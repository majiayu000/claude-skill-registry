---
name: verify-and-health
description: Runs all 9 verification gates and health checks, interprets failures with actionable fix guidance, and re-verifies after fixes. Use at session start, before commits, or whenever you need to check project integrity. Lightweight daily-use workflow.
protocol_id: PROTO-ORG-4
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-verify, organon-health]
loads:
  - CLAUDE.md
  - book-llms/three-layer-architecture.md
---

# Verify and Health Workflow

> Implements PROTO-ORG-4 from `organon/protocols/PROTOCOLS.md`. Daily-use verification and health check for project integrity.

---

## When to Use This Skill

Use this skill when:
- **Starting a work session** — baseline integrity check
- **Before committing changes** — ensure nothing is broken
- **After significant edits** — verify no regressions
- **Diagnosing issues** — understand what's wrong and how to fix it

**Purpose:** Run all automated verification gates, interpret results, and guide fixes with specific actions.

---

## Context Loading

1. Load project constraints:
   - Read `CLAUDE.md` (project invariants and development workflow)
2. Load verification reference:
   - Read `book-llms/three-layer-architecture.md` (Verification Gates section only)

**Note:** This is intentionally lightweight. Only load additional context if a specific failure requires it.

---

## Steps

### Step 1: Run All Verification Gates

```bash
cd packages/tools && npx organon verify
```

This runs all 9 gates:
- **frontmatter** (blocking) — YAML frontmatter present, valid, and truthful
- **triplets** (blocking) — Protocol↔workflow bindings are bidirectional
- **references** (blocking) — `inherits_from`, `loads:`, `protocol_file` resolve
- **placeholder-detection** (advisory) — Template placeholders like `[Describe...]` remain
- **freshness** (advisory) — Files reviewed within configured threshold
- **invariant-coverage** (blocking) — Every non-judgment invariant has ≥1 test
- **workflow-quality** (blocking) — Workflows have protocol_id, tools, loads, error recovery
- **tier4-tests** (advisory) — Test files use `@organon-invariant` annotations
- **version-alignment** (advisory) — Config methodology_version matches CLI version

### Step 2: Run Health Check

```bash
cd packages/tools && npx organon health
```

Reports overall project health score with breakdown by category.

### Step 3: Interpret Failures

Map each failure to a fix action:

| Gate | Diagnostic Code | Fix Action |
|------|-----------------|------------|
| frontmatter | Missing required field | Add field per `book-llms/frontmatter-system.md` schema |
| frontmatter | Count mismatch | Update `invariants_count`, `principles_count`, or `heuristics_count` to match actual content |
| frontmatter | Token estimate off | Recalculate using ~12 tokens/line heuristic |
| references | Broken file path | Update path to correct location or create missing file |
| references | Broken related_files entry | Fix path or remove stale reference |
| triplets | Orphaned workflow | Add `protocol_id` and `protocol_file` to workflow frontmatter |
| triplets | Phantom automation | Create the workflow that the protocol references, or change protocol to `manual` tier |
| triplets | Protocol↔workflow ID mismatch | Align `protocol_id` in workflow with `id` in protocol |
| coverage | Invariant without test | Create tier-4 test mapping invariant ID to test |
| workflow-quality | `WORKFLOW_MISSING_PROTOCOL_ID` | Add `protocol_id: PROTO-SCOPE-N` to workflow frontmatter |
| workflow-quality | `WORKFLOW_MISSING_PROTOCOL_FILE` | Add `protocol_file: path/to/PROTOCOLS.md` to workflow frontmatter |
| workflow-quality | `WORKFLOW_MISSING_TOOLS` | Add `tools: [tool-list]` to workflow frontmatter |
| workflow-quality | `WORKFLOW_MISSING_LOADS` | Add `loads:` array with organon files to load |
| workflow-quality | `WORKFLOW_BROKEN_LOADS_REF` | Fix path in `loads` array to point to existing file |
| workflow-quality | `WORKFLOW_NO_ERROR_RECOVERY` | Add `## Error Recovery` section with failure/recovery table |
| references | `REFERENCE_BROKEN_INHERIT` | Fix `inherits_from` to reference existing organon `name` fields |
| references | `REFERENCE_BROKEN_LOADS` | Fix path in workflow `loads:` array to point to existing file |
| references | `REFERENCE_BROKEN_PROTOCOL_FILE` | Fix `protocol_file` path in workflow frontmatter |
| placeholder-detection | `PLACEHOLDER_DETECTED` | Replace template placeholders (`[Describe...]`) with real content |
| tier4-tests | `TIER4_MISSING_ANNOTATION` | Add `@organon-invariant INV-ID` annotation to test files |
| version-alignment | `VERSION_METHODOLOGY_DRIFT` | Update `methodology_version` in `organon.config.json` to match CLI version |

### Step 4: Guide Fixes

For each failure:
1. Identify the specific file and field
2. Show the exact value to add or change
3. Reference the specification that defines the correct format

### Step 5: Re-verify

After all fixes are applied:

```bash
cd packages/tools && npx organon verify && npx organon health
```

All gates should pass. Health score should be equal to or higher than before.

---

## Verification

- [ ] All 9 gates pass (`organon verify` exits 0)
- [ ] Health score reported (`organon health` completes)
- [ ] No regressions from previous health score
- [ ] All fix actions were specific and actionable

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| `organon verify` command not found | Build organon-tools: `cd packages/tools && npm install && npm run build` |
| Gate failure not in diagnostic table | Read the gate's error message for file:line details. Check `book-llms/workflow-authoring.md` for diagnostic codes. |
| Fix introduces new failure | Re-run full verification. Cascading failures are common when fixing references — fix in dependency order (frontmatter → references → triplets). |
| Health score decreased after fixes | Investigate what changed. A lower score usually means a file was removed or frontmatter was invalidated. |
| Too many failures to fix in one session | Prioritize: frontmatter gate first (other gates depend on it), then references, then triplets, then workflow-quality. |
