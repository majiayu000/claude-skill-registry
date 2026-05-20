---
name: validate-chalk
description: Validate chalk.json schema and docs completeness — check that project context is sufficient for skills to operate
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[optional: 'fix' to auto-fix issues, or 'json' for machine-readable output]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: validation, chalk, quality
---

Audit the `.chalk/` directory to verify that `chalk.json` and PROFILE docs are complete, correct, and sufficient for skills to operate. Reports gaps and optionally fixes them.

## When to Use

- Before running skills that depend on project context (capture-pr-visuals, create-pr, etc.)
- After initial setup to verify completeness
- Periodically to detect stale docs
- In CI to enforce chalk quality

## Workflow

### Step 1: Check chalk.json exists and is valid

1. Read `.chalk/chalk.json`
2. Validate required fields:
   - `version` — must be `"1.0"`
   - `project.name` — must exist and be non-empty
3. Check recommended fields and report if missing:
   - `project.description`, `project.language`, `project.framework`, `project.type`
   - `dev.command`, `dev.port`, `dev.url`
   - `test.command`
   - `build.command`
   - `routes` — at least one route
   - `sourceLayout.root`
4. Validate field values make sense:
   - `dev.port` is a valid port number (1-65535)
   - `dev.url` starts with `http`
   - `routes[].path` and `routes[].name` are non-empty
   - `sourceLayout` paths exist on disk

### Step 2: Check PROFILE docs exist

Verify these files exist:
- `.chalk/docs/product/PROFILE.md`
- `.chalk/docs/engineering/PROFILE.md`
- `.chalk/docs/engineering/coding-style.md`
- `.chalk/docs/ai/PROFILE.md`
- `.chalk/docs/design/PROFILE.md`

For each file:
- Check it exists
- Check it has more than 20 lines of content (not just stubs)
- Check it doesn't contain `<!-- STUB -->` markers
- Check it has a `Last updated:` line

### Step 3: Check for v1 legacy structure

Detect old numbered files that should have been migrated:
- `0_PRODUCT_PROFILE.md`, `0_ENGINEERING_PROFILE.md`, `1_architecture.md`, `3_techstack.md`, etc.
- If found, warn that migration is needed and suggest running `/setup-chalk` with migration

### Step 4: Cross-validate chalk.json against docs

- If `chalk.json` lists routes, check that `engineering/PROFILE.md` mentions them
- If `chalk.json` lists a framework, check that `engineering/PROFILE.md` documents it
- If `chalk.json` has `sourceLayout`, verify the directories actually exist on disk

### Step 5: Report

Print a summary:

```
Chalk Validation Report
=======================

chalk.json:
  ✓ version: 1.0
  ✓ project.name: my-app
  ✓ project.framework: next
  ✗ routes: missing (run /setup-docs to detect)
  ✗ test.command: missing

Docs:
  ✓ product/PROFILE.md (142 lines, updated 2026-03-10)
  ✓ engineering/PROFILE.md (298 lines, updated 2026-03-10)
  ✗ engineering/coding-style.md: MISSING
  ✓ ai/PROFILE.md (87 lines, updated 2026-03-10)
  ⚠ design/PROFILE.md: contains STUB markers

Legacy:
  ⚠ Found 0_ENGINEERING_PROFILE.md — migration needed

Score: 7/11 checks passed
```

### Step 6: Auto-fix (if `fix` argument provided)

If the user passed `fix` as an argument:
- Run `/setup-docs` to populate missing PROFILE docs
- Run route detection to fill `chalk.json` routes
- Run source layout detection to fill `chalk.json` sourceLayout
- Migrate v1 files if found (with user confirmation)

## Rules

- Never modify files without the `fix` argument — report-only by default
- Don't fail on missing optional fields — just warn
- Required fields that cause failure: `chalk.json` must exist, `version` and `project.name` must be present
- Be specific about what's missing and how to fix it
