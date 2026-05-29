---
name: agent-ops-constitution
description: "Create/update .agent/constitution.md. Use when commands/boundaries/constraints must be confirmed before baseline or code changes. Draft v0 from repo evidence, then interview user."
category: core
invokes: [agent-ops-context-map, agent-ops-state, agent-ops-interview, agent-ops-tasks]
invoked_by: []
state_files:
  read: [focus.md, issues/*.md, map.md]
  write: [constitution.md, focus.md, issues/*.md]
---

# Constitution workflow (mandatory before baseline)

## Goal
Make `.agent/constitution.md` baseline-ready by confirming:
- allowed/restricted/forbidden work areas
- single-line build/lint/test/format commands
- environment assumptions
- project-specific constraints
- issue-first workflow expectations

## Pre-requisite: Context Map

**Before starting constitution interview, ensure a context map exists:**

1) Check if `.agent/map.md` exists
2) If NO map exists:
   ```
   📍 No context map found. Creating one first to inform constitution questions...
   ```
   → Invoke `agent-ops-context-map` to generate `.agent/map.md`
3) If map exists but is stale (>30 days old or significant changes detected):
   ```
   📍 Context map may be outdated. Refresh? [Y]es / [N]o
   ```
4) Use the map to:
   - Pre-populate candidate work areas
   - Identify build/test tooling
   - Understand project structure for interview questions

## Procedure
1) **Ensure context map exists** (see above)
2) **Run tool detection** — invoke `agent-ops-tools` or `aoc tools scan --save`
   - Creates `.agent/tools.json` with available development tools
   - Identifies missing recommended tools based on detected project type
   - Populates "Available tools" section in constitution
3) Inspect repo evidence (README, CI workflows, package/build files). Do not guess.
4) Draft v0 constitution:
   - every inferred item must cite its evidence ("CANDIDATE from <path>")
   - anything without evidence is `TODO` + `UNCONFIRMED`
   - use detected tools to suggest build/lint/test commands
5) Interview the user:
   - one question per TODO/UNCONFIRMED item
   - ask both "what should it be?" and "why?"
6) Update constitution until:
   - build + test commands are **CONFIRMED**
   - work boundaries are **CONFIRMED**
7) Use `agent-ops-state` to update `.agent/focus.md`.
8) Invoke `agent-ops-tasks` for any setup work discovered.

## Issue Discovery During Constitution

**After constitution setup, invoke `agent-ops-tasks` discovery:**

1) **Collect setup items discovered:**
   - Missing configuration → `CHORE` issue
   - Broken scripts → `BUG` issue
   - Missing documentation → `DOCS` issue
   - Security concerns noted → `SEC` issue
   - Environment issues → `CHORE` issue

2) **Present to user:**
   ```
   📋 Constitution setup found {N} items to address:
   
   High:
   - [BUG] Build script references missing file
   - [CHORE] CI workflow needs updating
   
   Medium:
   - [DOCS] README is outdated
   
   Create issues for these? [A]ll / [S]elect / [N]one
   ```

3) **Workflow continues:**
   - Issues created before baseline capture
   - Baseline can now proceed with known issues documented

## Template
Start from [constitution template](./templates/constitution.template.md).

## Low Confidence Completeness Check (MANDATORY)

**For LOW confidence work, constitution must be verified as complete before proceeding.**

### Required Sections Checklist

When confidence is LOW, verify constitution has ALL of these sections **CONFIRMED** (not TODO/UNCONFIRMED):

| Section | Required | Purpose |
|---------|----------|---------|
| **Project scope** | ✅ | What this project does |
| **Work areas: allowed** | ✅ | Where changes are permitted |
| **Work areas: restricted** | ✅ | Where caution is required |
| **Work areas: forbidden** | ✅ | Where changes are never allowed |
| **Build command** | ✅ | Single-line build command |
| **Test command** | ✅ | Single-line test command |
| **Lint command** | ✅ | Single-line lint command |
| **Format command** | ⚪ Optional | Single-line format command |
| **Coverage command** | ✅ for LOW | How to measure coverage |
| **Environment assumptions** | ✅ | OS, runtime versions, dependencies |
| **Tool detection** | ✅ | `.agent/tools.json` exists |
| **Constraints** | ✅ | Project-specific limitations |
| **Default confidence** | ✅ | LOW/NORMAL/HIGH |

### Completeness Verification

Before LOW confidence work begins:

```
🎯 LOW CONFIDENCE CONSTITUTION CHECK

Checking constitution completeness for low confidence work...

| Section | Status |
|---------|--------|
| Project scope | ✅ CONFIRMED |
| Allowed areas | ✅ CONFIRMED |
| Restricted areas | ✅ CONFIRMED |
| Forbidden areas | ⚠️ TODO |
| Build command | ✅ CONFIRMED |
| Test command | ✅ CONFIRMED |
| Lint command | ✅ CONFIRMED |
| Coverage command | ❌ MISSING |
| Environment | ✅ CONFIRMED |
| Tool detection | ✅ .agent/tools.json exists |
| Constraints | ⚠️ UNCONFIRMED |

Result: INCOMPLETE — 3 items need confirmation

⚠️ Cannot proceed with low confidence work until constitution is complete.

Starting interview to fill gaps...
```

### Staleness Check

For LOW confidence, also check constitution age:

| Age | Action |
|-----|--------|
| < 7 days | Proceed |
| 7-30 days | Prompt: "Constitution is {N} days old. Review before proceeding?" |
| > 30 days | Require: "Constitution is stale. Re-interview before low confidence work." |

### Gap-Filling Interview

If constitution is incomplete for LOW confidence:

1. List missing/unconfirmed sections
2. Invoke `agent-ops-interview` for each gap
3. Update constitution with confirmed values
4. Re-verify completeness
5. Only proceed when all required sections are CONFIRMED

```
📋 Constitution gaps for low confidence work:

1. Forbidden work areas (currently: TODO)
2. Coverage command (currently: MISSING)
3. Constraints (currently: UNCONFIRMED)

Starting interview to fill these gaps...

Q1: What areas of the codebase should NEVER be modified?
(These will be marked as forbidden work areas)
```
