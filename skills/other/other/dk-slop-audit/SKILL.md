---
name: dk-slop-audit
description: "Run a codebase hygiene audit. Scans for misplaced files, dead code, temp files, security issues, structural problems, dependency slop, and git slop. Outputs a prioritized report with P0-P4 findings. Use periodically or before releases. Triggers on: 'audit the codebase', 'find slop', 'hygiene check', 'clean up', or /dk-slop-audit."
argument-hint: "[optional: directory or category to focus on]"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-slop-audit — Codebase Hygiene Auditor

Systematically scan the codebase for slop — code that degrades quality through misplacement, abandonment, inconsistency, or negligence. Produce a prioritized, actionable report.

## Scope

<audit_scope> $ARGUMENTS </audit_scope>

If a scope is provided, focus on that directory or category. Otherwise, audit the entire repository.

## What is slop?

Slop is anything that makes a developer say "wait, why is this here?" or "is this still used?" It's the entropy that accumulates when people add things but never clean up.

## Process

### Step 1: Map the project structure

Use Glob and Bash (`ls`) to understand the directory layout, build systems, and language boundaries. Read the root CLAUDE.md and any project-level CLAUDE.md files to understand intentional patterns — things that look unusual but are deliberate are not slop.

### Step 2: Scan each category

Work through each category using parallel subagents where possible. Each subagent scans one category and returns findings.

**Category 1 — Misplaced Files**: Files in the wrong directory. A Python script in a frontend dir. A test file in src. A config file at the wrong level.

**Category 2 — Dead & Orphaned Code**: Unused imports, functions nothing calls, commented-out code blocks, orphaned tests for deleted functionality, stale feature flags.

**Category 3 — Temp & Scratch Files**: Files named temp_*, scratch_*, debug_*, old_*, backup_*. One-off scripts (populate_data, fix_migration, quick_test). Log files or build artifacts committed to git.

**Category 4 — Security & Config Slop**: Hardcoded localhost URLs/ports/credentials. Committed .env files, API keys, tokens. Default passwords in non-example files. Overly permissive CORS/auth settings.

**Category 5 — Structural Slop**: Duplicate logic across files. Inconsistent naming conventions. God files (>500 lines doing multiple things). Circular imports. Docs describing behavior the code no longer has.

**Category 6 — Dependency Slop**: Unused dependencies. Pinned versions with known vulnerabilities. Multiple packages doing the same thing. Dev dependencies in production lists.

**Category 7 — Git & Project Slop**: Files that should be in .gitignore. TODO/FIXME/HACK comments older than 6 months (check git blame). Stale branches referenced in configs.

### Step 3: Verify before reporting

Do not flag something as dead code without checking for dynamic imports, reflection, or framework magic. Do not flag a file as misplaced without understanding the project's conventions. Do not flag test fixtures, example files, or template files — they exist for a purpose.

### Step 4: Grade each finding

- **P0 — Critical**: Active security risk. Committed secrets, exposed credentials, hardcoded tokens.
- **P1 — High**: Actively misleading. Files in wrong directories, dead code developers waste time reading, docs describing wrong behavior.
- **P2 — Medium**: Technical debt that compounds. Duplicated logic, unused dependencies inflating builds, stale configs.
- **P3 — Low**: Code quality friction. Naming inconsistency, oversized files, minor convention violations.
- **P4 — Trivial**: Cosmetic. Extra whitespace, old comments, minor style nits.

## Output

### Create `slops/all_slops.md`

```markdown
# Slop Audit — harness-kit

**Audited**: [date]
**Scope**: [directories audited]
**Total findings**: [N] (P0: [n], P1: [n], P2: [n], P3: [n], P4: [n])

## Summary by Priority

### P0 — Critical
| # | Finding | File(s) | Category |
|---|---------|---------|----------|

[...repeat for each priority level...]

## Findings by Category

### Misplaced Files
- SLOP-001 — P1 — `path/to/file` — [short description]

[...repeat for each category with findings...]
```

### Create detail files for P0-P2

For findings P0, P1, and P2, create `slops/SLOP-NNN-<slug>.md`:

```markdown
# SLOP-NNN: [Short Title]

**Priority**: P[0-2]
**Category**: [category name]
**File(s)**: `path/to/file`
**Age**: [git blame date or estimate]

## What's Wrong
[2-3 sentences]

## Evidence
[Code snippets, grep results, or structural observations]

## Suggested Fix
[Concrete action]

## Risk of Fixing
[Low/Medium/High — could fixing this break something?]
```

P3 and P4 findings go in the summary only — no individual detail files.

### Print summary

After creating all files, print:
- Total findings per priority
- Top 5 most impactful fixes (best effort-to-impact ratio)
- Any categories with zero findings (confirms they were checked)
