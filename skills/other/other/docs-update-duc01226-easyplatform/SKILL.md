---
name: docs-update
version: 2.0.0
description: '[Documentation] Holistic documentation orchestrator — detects impacted docs from git changes and updates project docs + business feature docs'
activation: user-invoked
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

> **Critical Purpose:** Ensure ALL documentation stays in sync with code changes — project docs, business feature docs, and AI companions.

## Quick Summary

**Goal:** Detect which documentation categories are impacted by recent code changes and update them accordingly.

**Workflow:**

1. **Phase 0: Triage** — `git diff` to categorize what changed and which doc types are impacted
2. **Phase 1: Project Docs** — Update project-level docs (README, codebase-summary, etc.) if impacted
3. **Phase 2: Business Feature Docs** — Detect affected modules, update existing feature docs in `docs/business-features/`
4. **Phase 3: Summary Report** — What was checked, updated, and skipped

**Key Rules:**

- NEVER create new business feature docs from scratch — only update existing ones
- Fast exit when no documentation is impacted (e.g., only `.claude/` config changes)
- Always report what was checked, even if nothing needed updating

---

## Phase 0: Triage — Detect Impacted Documentation

### Step 0.1: Collect Changed Files

1. Run `git diff --name-only HEAD` (captures both staged and unstaged changes)
2. If no uncommitted changes, run `git diff --name-only HEAD~1` (last commit)
3. If still empty, run `git diff --name-only origin/develop...HEAD` (branch changes)

### Step 0.2: Categorize Changes

Classify each changed file into documentation impact categories:

| Changed File Pattern | Impact Category | Action |
| --- | --- | --- |
| `src/Services/**` | **feature-docs** + project-docs | Phase 1 + Phase 2 |
| `{frontend-apps-dir}/**`, `{frontend-libs-dir}/{domain-lib}/**` | **feature-docs** + project-docs | Phase 1 + Phase 2 |
| `{legacy-frontend-dir}/**Client/**` | **feature-docs** + project-docs | Phase 1 + Phase 2 |
| `src/Platform/**` | project-docs | Phase 1 only |
| `docs/**` | project-docs | Phase 1 only |
| `.claude/**`, config files only | **none** | Fast exit |
| `{frontend-libs-dir}/{platform-core-lib}/**`, `{frontend-libs-dir}/{common-lib}/**` | project-docs | Phase 1 only |

### Step 0.3: Fast Exit Check

If ALL changed files fall into the **none** category (e.g., only `.claude/`, `.github/`, root config files):
- Report: `"No documentation impacted by current changes (config/tooling only)."`
- **Exit early** — skip Phase 1 and Phase 2.

---

## Phase 1: Project Documentation Update

**When to run:** Changed files include `src/Platform/**`, `docs/**`, or architectural changes.

**When to skip:** Only service-layer or frontend feature files changed (no architectural impact). Skip and proceed to Phase 2.

### Step 1.1: Spawn Scouts (standalone invocation only)

When invoked standalone (not as a workflow step), spawn scouts for broad codebase context:

1. Spawn 2-4 `scout-external` (preferred) or `scout` (fallback) via Task tool
2. Target directories that actually exist — adapt to project structure
3. Merge scout results into context summary

**When invoked as a workflow step:** Skip scouting — use git diff context from Phase 0 directly.

### Step 1.2: Update Project Docs

Pass context to `docs-manager` agent to update impacted project docs:

- `docs/codebase-summary.md`: Update if service structure or dependencies changed
- `docs/system-architecture.md`: Update if cross-service patterns changed
- `README.md`: Update if project scope or setup changed (keep under 300 lines)

Only update docs that are **directly impacted** by the changes. Do not regenerate all docs.

---

## Phase 2: Business Feature Documentation Update

> **This phase replaces the need to invoke `/feature-docs` separately for update scenarios.**
> docs-update handles the full update lifecycle: detection → analysis → update → verification.
> Only invoke `/feature-docs` directly when **creating new feature docs from scratch**.

**When to run:** Changed files match `src/Services/**`, `{frontend-apps-dir}/**`, `{frontend-libs-dir}/{domain-lib}/**`, or `{legacy-frontend-dir}/**Client/**`.

**When to skip:** No service-layer or frontend feature files changed. Report: `"No business feature docs impacted."`

### Step 2.1: Auto-Detect Affected Modules

<!-- Source: feature-docs Step 1.0 -->

Extract unique module names from changed file paths:

| Changed File Path Pattern | Detected Module |
| --- | --- |
| `src/Services/{Module}/**` | {Module} |
| `{frontend-apps-dir}/{app-name}/**` | {Module} (map app to module) |
| `{frontend-libs-dir}/{domain-lib}/src/{feature}/**` | {Module} (map feature to module) |
| `{legacy-frontend-dir}/{Module}Client/**` | {Module} |

Build project-specific mapping by examining:
```bash
ls -d src/Services/*/
ls -d docs/business-features/*/
```

### Step 2.2: Check Existing Docs

For each detected module:

1. Check if `docs/business-features/{Module}/` exists
2. Check if `docs/business-features/{Module}/detailed-features/` has feature docs
3. **If docs exist** → proceed to Step 2.3 (update mode)
4. **If no docs exist** → report: `"Module {Module} has no feature docs. Consider running /feature-docs to create them."` and skip

### Step 2.3: Diff Analysis

<!-- Source: feature-docs Step 1.5.1 -->

1. Categorize changes by type: backend entity, command, query, frontend component, i18n, etc.
2. Map each change to impacted documentation sections using the table below

### Step 2.4: Section Impact Mapping

<!-- Source: feature-docs Step 1.5.2 -->

| Change Type | Impacted Doc Sections |
| --- | --- |
| New entity property | 3 (Business Requirements), 9 (Domain Model), 10 (API Reference) |
| New API endpoint | 10 (API Reference), 12 (Backend Controllers), 14 (Security) |
| New frontend component | 11 (Frontend Components) |
| New filter/query | 3 (Business Requirements), 10 (API Reference) |
| New i18n keys | 11 (Frontend Components) |
| Any new functionality | **17 (Test Specs), 18 (Test Data), 19 (Edge Cases), 20 (Regression Impact)** — MANDATORY |
| Any change | 1 (Executive Summary), 26 (Version History) — ALWAYS UPDATE |

### Step 2.5: Update Impacted Sections

For each module with existing docs:

1. Read the existing feature doc (`README.{FeatureName}.md`)
2. Update ONLY the sections identified in Step 2.4
3. **Mandatory test coverage** — when documenting new functionality, MUST update:
   - Section 17 (Test Specifications): Add TC-{MOD}-XXX test cases with GIVEN/WHEN/THEN
   - Section 18 (Test Data): Add seed data for new test cases
   - Section 19 (Edge Cases): Add boundary conditions and error states
   - Section 20 (Regression Impact): Add regression risk rows
4. Update Section 26 (Version History) with new version entry
5. Add CHANGELOG entry under `[Unreleased]` following Keep a Changelog format

### Step 2.6: AI Companion Sync

If `README.{FeatureName}.ai.md` exists alongside the updated feature doc:
- Update the AI companion to reflect changes (keep 300-500 lines)
- Update `Last synced` timestamp

### Step 2.7: Verification (Mandatory)

<!-- Source: feature-docs Phase 3.5 -->

After updating feature docs, run a verification pass on all changed sections:

1. **Evidence audit** — Every test case (TC-{MOD}-XXX) MUST have `file:line` evidence. Read the claimed file at the claimed line and verify the code supports the assertion. Fix immediately if wrong.
2. **Domain model check** — Verify entity properties, types, and enum values against actual source code. Remove anything not found in source.
3. **Cross-reference audit** — Test Summary counts match actual TC count. No template placeholders remain (`{FilePath}`, `{LineRange}`). All internal links resolve.

**If verification finds hallucinated or stale content → fix before completing Phase 2.**

### Step 2.8: TC Coverage Cross-Reference

After updating feature docs, cross-reference integration test TC codes against doc TC codes:

1. Use the Grep tool to find all `[Trait("TestSpec", ...)]` in the affected service's integration test project:
   ```
   Grep pattern="Trait\(\"TestSpec\"" path="src/Services/{ServiceDir}/{Service}.IntegrationTests" glob="*.cs"
   ```
2. Use the Grep tool to find all `TC-{MOD}-XXX` in the affected feature doc Section 17 / test-specs doc:
   ```
   Grep pattern="TC-[A-Z]{2,}-[0-9]+" path="docs/business-features/{Module}/detailed-features" glob="*.md"
   ```
3. Compare the TC codes found:
   - TC in docs but no Trait in code → flag as `Status: Untested` in the doc
   - Trait in code but no TC in docs → add TC entry to the feature doc Section 17
4. Report discrepancies in the Phase 3 Summary Report

### Decision: When docs-update Handles It vs. When to Recommend /feature-docs

| Scenario | Action |
| --- | --- |
| Existing docs + code changes | **docs-update handles it** (Steps 2.1–2.7 above) |
| No existing docs for module | Report: recommend `/feature-docs` for creation |
| Major new feature (new entity, new service, >10 new endpoints) | **docs-update handles update**, but report: "Consider full `/feature-docs` review for completeness" |
| User explicitly asks for full 26-section doc | Defer to `/feature-docs` |

---

## Phase 3: Summary Report

Always output a summary of what happened:

```
### Documentation Update Summary

**Triage:** {N} files changed → {categories detected}

**Project Docs:**
- {Updated/Skipped}: {reason}

**Business Feature Docs:**
- Module {X}: {Updated sections A, B, C / No existing docs / Not impacted}
- Module {Y}: {Updated sections D, E / Skipped: no feature docs}

**Recommendations:**
- {Any new docs that should be created}
- {Any stale docs flagged but not auto-fixed}
```

---

## Additional Requests

<additional_requests>
$ARGUMENTS
</additional_requests>

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
