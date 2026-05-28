---
name: sniper-check
description: Use when validating code quality after modifications. Runs sniper agent in isolated forked context for clean, fast validation.
context: fork
agent: fuse-ai-pilot:sniper
user-invocable: true
argument-hint: "[file-or-directory]"
---

**Target:** $ARGUMENTS

# Sniper Check

## Overview

Quick code quality validation using the sniper agent in an isolated forked context. Executes the full 6-phase workflow without polluting the main conversation context.

| Feature | Detail |
|---------|--------|
| **Context** | Forked (isolated sub-agent) |
| **Agent** | sniper (Sonnet) |
| **Phases** | 6-phase code-quality workflow |
| **Result** | Only final report returns to parent |

---

## When to Use

| Scenario | Use |
|----------|-----|
| After code modifications | `/sniper-check src/` |
| Validate specific file | `/sniper-check path/to/file.ts` |
| Full project check | `/sniper-check .` |
| After refactoring | `/sniper-check src/components/` |

---

## Workflow

Execute the mandatory 6-phase `code-quality` workflow:

1. **PHASE 1+2 (PARALLEL)**: Launch both in parallel:
   - `explore-codebase` (Haiku) → Architecture discovery
   - `research-expert` (Sonnet) → Documentation verification
2. **PHASE 3**: Grep all usages → Impact analysis
3. **PHASE 4**: Run linters → Detect errors
4. **PHASE 5**: Apply corrections → Minimal changes
5. **PHASE 6**: Re-run linters → Zero errors

**CRITICAL**: Phases 1+2 must run in PARALLEL (two Task calls in one message).

---

## Critical Rules

| Rule | Reason |
|------|--------|
| Never skip phases 1+2 | Documentation-backed fixes only |
| Always run phases in order | Dependencies between phases |
| Zero linter errors | Non-negotiable exit criteria |
| Minimal changes only | Smallest fix necessary |

---

## Report Format

Return a validation report with:

- Architecture summary (from explore-codebase)
- Documentation references (from research-expert)
- Impact analysis table (usages, risk level)
- Errors fixed (critical, high, medium, low)
- SOLID compliance status
- Final linter status (must be ZERO errors)
