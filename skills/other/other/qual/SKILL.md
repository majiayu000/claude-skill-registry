---
name: qual
description: Use when you want a deeper multi-angle quality review before shipping, especially after substantial or risky changes.
argument-hint: [path]
---

target_path = $ARGUMENTS

If target_path provided, analyze that path. Otherwise, files changed since the default branch. Full-codebase analysis requires explicit user request.

## Architecture

You coordinate specialist teammates who analyze in independent context windows. Separation matters — your implementation bias doesn't leak into their findings, and their diverse perspectives catch what a single pass misses.

Two waves: **detect** then **simplify**. Wave 2 exists because LLMs reliably over-engineer fixes — even your own wave 1 fixes are suspect and need an independent simplification pass.

## Wave 1: Detect

Spawn specialist teammates from `${CLAUDE_SKILL_DIR}/agents/`. Each teammate gets the target file list and the project's detected stack.

| Teammate | Agent file | Focus |
|----------|-----------|-------|
| Skeptic | `skeptic.md` | Bugs, security, performance, correctness |
| Silent-failure hunter | `silent-failure.md` | Hidden errors, swallowed exceptions |
| Pattern harmonizer | `patterns.md` | Divergent implementations, inconsistent patterns |
| Comment auditor | `comments.md` | Misleading/stale/useless comments |

**Wave 1 teammates are read-only** — analysis tools only, no editing. Mixing analysis and editing in one pass leads to fixes that miss the bigger picture.

The Simplifier runs in wave 2, not here.

### Actionability Gate

Every finding must pass all five criteria. This filter prevents the report from being dominated by noise — LLM analysis without it produces 60%+ false positives:

1. **Scoped** — within the target path or recent changes
2. **Specific** — points to a concrete code path, not a general observation
3. **Certain** — "this WILL cause X", not "this could theoretically..."
4. **Non-intentional** — not a deliberate pattern justified by comments, tests, or conventions
5. **Discrete** — has a single, focused fix (not "rewrite this module")

Deduplicate across lenses: when multiple teammates flag the same underlying issue, merge into one finding citing all relevant lenses. Keep the highest severity.

### Triage

| Severity | Boundary |
|----------|----------|
| CRITICAL | Security vulnerabilities, data loss risks, silent failures hiding bugs |
| HIGH | Logic errors, missing error handling on critical paths |
| MEDIUM | Pattern inconsistencies, genuine maintainability issues |
| LOW | Minor improvements |
| IGNORE | False positives, justified patterns, style-only concerns |

**Conflict resolution:** Safety > style. Cohesion > fragmentation. Direct code > abstraction. Pattern consistency > local optimization. Type annotations > JSDoc.

### Approval Gate

Present findings grouped by severity. Each finding: severity, confidence, location, issue, recommended fix, source lens(es).

**Stop. Wait for user to select which fixes to apply.**

After approval: implement selected fixes, verify with quality gates. If a fix breaks something, revert rather than cascade.

## Wave 2: Simplify

Spawn one Simplifier teammate (`simplifier.md`) on the post-fix codebase. Same actionability gate, triage, and approval gate flow as wave 1.
