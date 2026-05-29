---
name: audit
description: Comprehensive codebase audit for release readiness. Parallel exploration of docs, code, config, tests, and specs to identify cruft, then interactive triage with clear action options.
---

# Codebase Audit

Systematic review of the entire codebase to identify cruft, outdated content, and issues before release. Uses parallel exploration for discovery, then interactive triage for decisions.

## When to Use

- Pre-release cleanup
- Periodic codebase health check
- After major refactoring
- When onboarding to understand technical debt

## Workflow

### Phase 1: Discovery (Parallel Exploration)

Launch 5 parallel Explore agents to review different areas:

```
Task tool (subagent_type: Explore) - run all 5 in parallel:

1. DOCS: Review *.md files for outdated content, stale TODOs,
   inconsistencies, wrong command syntax, aspirational features
   documented as current

2. CODE: Review src/ for dead code, unresolved TODOs/FIXMEs,
   duplicate functions, commented-out code, debug artifacts,
   unused imports/exports

3. CONFIG: Review package.json, tsconfig, etc. for unused deps,
   misplaced deps (dev vs prod), broken scripts, stale configs,
   version drift

4. TESTS: Review tests/ for skipped tests, dead mocks, duplicate
   test names, flaky patterns, missing coverage, outdated fixtures

5. SPECS: Review .kspec/ for stale spec items, orphaned tasks,
   status mismatches, empty stubs, inbox items that should be
   promoted, accumulating session files
```

Each agent should report findings with:
- File and location
- What the issue is
- Why it's cruft (outdated, redundant, broken, etc.)
- Recommended action

### Phase 2: Compilation

Organize all findings by severity:

| Severity | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Blocks release, breaks functionality | Runtime deps in devDeps, security vulns, broken required scripts |
| **HIGH** | Should fix, user-facing or misleading | Wrong docs, incorrect command syntax, misleading task statuses |
| **MEDIUM** | Recommended, technical debt | Unresolved TODOs, duplicate code, test improvements |
| **LOW** | Nice to have, minor cleanup | Doc cross-refs, test name clarity, helper consolidation |

Present compiled summary to user before triage.

### Phase 3: Triage (Interactive)

Go through items one-by-one using AskUserQuestion:

```
For each item, present options:

- Fix now      → Execute the fix immediately
- Task         → Create task with context notes
- Inbox        → Add to inbox for later review
- Punt         → Skip, not worth tracking
- Discuss      → Need more context before deciding
```

**Triage principles:**
- One item at a time (don't batch)
- User decides disposition
- Execute decisions immediately
- Add context notes to tasks/inbox

### Phase 4: Execution

For each decision type:

**Fix now:**
```bash
# Delete dead files
rm path/to/dead-file.js

# Quick edits
# Use Edit tool for small fixes

# Commit cleanup changes at end
git add -A && git commit -m "chore: Audit cleanup - [summary]"
```

**Task:**
```bash
kspec task add --title "Description" --priority N --slug slug-name --tag relevant-tag
kspec task note @slug "Context: file location, what needs doing, why"
```

**Inbox:**
```bash
kspec inbox add "Description of item for later" --tag tag1 --tag tag2
```

### Phase 5: Summary

At end of triage, report:

```
## Audit Summary

### Fixed Now
- Item 1
- Item 2

### Tasks Created (N)
| Task | Priority | Description |
|------|----------|-------------|
| @slug | PN | Brief description |

### Inbox Added (N)
- Item description

### Punted (N)
- Reason for each

### Remaining
- Any items not yet triaged
```

Commit any direct fixes made during audit.

## Key Principles

- **Parallel discovery** - Explore agents run concurrently for speed
- **Severity-first** - Critical items get triaged first
- **Interactive triage** - User controls every decision
- **Immediate execution** - Don't batch, act on each decision
- **Full tracking** - Everything either fixed or tracked
- **Clean commit** - End with committed state

## Quick Reference

```bash
# Get session context first
kspec session start

# After triage, commit fixes
git add -A && git commit -m "chore: Audit cleanup"

# Create task with context
kspec task add --title "..." --priority N --slug slug --tag tag
kspec task note @slug "Context..."

# Add to inbox
kspec inbox add "Description" --tag tag

# Check what was created
kspec task list --status pending
kspec inbox list
```

## Exploration Prompts

Use these prompts for the parallel Explore agents:

**Docs:**
> Review documentation files for cruft in preparation for release. Look for: outdated content, stale TODOs, inconsistencies between docs, wrong command syntax, features documented that don't exist. Check README.md, AGENTS.md, CLAUDE.md, and other .md files.

**Code:**
> Review src/ directory for code cruft. Look for: dead code, unused exports, unresolved TODO/FIXME comments, duplicate functions, commented-out code, debug artifacts, unused imports. Note file paths and line numbers.

**Config:**
> Review configuration files for cruft. Look for: unused dependencies, misplaced deps (devDeps vs deps), broken npm scripts, stale tsconfig/eslint options, version inconsistencies. Check package.json, tsconfig.json, and config files.

**Tests:**
> Review tests/ for cruft. Look for: skipped tests (.skip/.todo), dead mock files, duplicate test names, flaky patterns, missing coverage, outdated fixtures. Verify temp directory isolation pattern.

**Specs:**
> Review .kspec/ for spec and task cruft. Look for: stale spec items, orphaned tasks, incorrect statuses, empty stubs, inbox items that should be promoted, tasks with empty slugs.

## Tips

- Run tests before and after to catch regressions
- Check git status frequently during fixes
- For complex fixes, create tasks rather than fixing inline
- Group related fixes in a single commit
- If unsure about a fix, punt and discuss later
