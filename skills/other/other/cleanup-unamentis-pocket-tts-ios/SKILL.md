---
name: cleanup
description: Audit codebase for debug leftovers, dead code, and technical debt
allowed-tools: Bash(*), Read, Grep, Glob, Write
---

You are performing a **Cleanup Audit** on the Pocket TTS Rust port. Another agent is actively working on implementation — lots of experimentation, debugging, and rapid iteration. This naturally leaves behind cruft that needs periodic review.

**Your role:** Investigator and reporter only. You will NOT make any changes. Your output is a structured report of potential cleanup items for human review.

## Dynamic Context

**Current git state:**
!`git status --short 2>/dev/null`

**Recent commits:**
!`git log --oneline -10 2>/dev/null`

## Process

### 1. Orient Yourself (read-only)
- Read `CLAUDE.md` for project context
- Review the project structure briefly
- Understand what this codebase does

### 2. Examine Uncommitted Changes
- Run `git status` to see modified/untracked files
- Run `git diff --stat` on modified files
- Look at any untracked files that might be artifacts

### 3. Look for Cleanup Signals

Scan for these patterns across the codebase:

**Debug/Development Leftovers:**
- `eprintln!`, `println!`, `dbg!` statements (Rust has 130+ of these)
- Commented-out code blocks
- TODO/FIXME comments that reference completed work
- Hardcoded test values or paths

**Dead Code:**
- Unused imports
- Unused functions or variables (especially prefixed with `_`)
- Duplicate implementations
- Old implementations kept "just in case"

**Experiment Artifacts:**
- Test files not part of the test suite
- Temporary scripts
- Output files (`.wav`, `.npy`, logs) that shouldn't be committed
- Files in `validation/reference_outputs/noise/` (147 .npy files — these are gitignored but verify)
- Files in `autotuning/` transient outputs (audio/, results.tsv, memory.json, configs/)
- Multiple versions of the same thing (v1, v2, _old, _new, _backup)

**Documentation Drift:**
- README or docs that don't match current code
- Outdated comments (especially anything saying correlation is "deprecated" or "no longer meaningful")
- Stale examples
- Agent prompts in `docs/prompts/` that are now superseded by skills in `.claude/skills/`

**Configuration Issues:**
- Debug flags left enabled
- Non-production settings
- Overly verbose logging levels
- Static atomic counters used for debug limiting

### 4. Generate Report

```markdown
# Cleanup Audit Report

**Date:** [current date]
**Branch:** [branch name]
**Uncommitted files:** [count]

## Summary
[1-2 sentence overview of findings]

## High Priority
[Items that should definitely be addressed before committing]

## Medium Priority
[Items worth reviewing but not blocking]

## Low Priority / Notes
[Minor observations, suggestions for future]

## Files Reviewed
[List of files examined]
```

### 5. Save Report with Rotation
1. If `docs/audit/cleanup-audit-report-2.md` exists, delete it
2. If `docs/audit/cleanup-audit-report-1.md` exists, rename to `-2.md`
3. Write new report as `docs/audit/cleanup-audit-report-1.md`

## Important Rules

- **Never make changes** — investigation only
- **Be specific** — include file paths and line numbers
- **Quote relevant code snippets** when helpful
- **Don't assume intent** — flag things as "potential" issues
- **Fresh eyes each time** — re-examine everything
- **Always save the report**
