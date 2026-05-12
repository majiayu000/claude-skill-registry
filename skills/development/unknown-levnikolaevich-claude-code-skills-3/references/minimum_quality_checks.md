# Minimum Quality Checks

Non-negotiable checks that ANY Quality Gate implementation must perform, regardless of execution mode (full ln-510 pipeline, inline, or Team Lead integration).

## Why This Exists

API-535 post-mortem: inline QG implementation skipped agent code review. Result: 3 CRITICAL + 6 HIGH bugs shipped to Done. Static analysis (ruff/mypy) and convention review (ln-402) cannot catch algorithm logic, performance patterns, or domain-specific correctness issues.

## Mandatory Check Matrix

| # | Check | Tool | Skippable? | Catches |
|---|-------|------|------------|---------|
| 1 | Static analysis (lint + typecheck) | ruff, mypy, or project equivalent | NO | Syntax, types, dead code |
| 2 | Regression tests | Project test suite | NO | Broken existing behavior |
| 3 | Task-level review | ln-402 or equivalent checklist | NO | Architecture, conventions, DRY |
| 4 | **Agent code review** | **At least 1 external agent** (Claude or Codex) with `references/agents/prompt_templates/modes/code.md` | **NO** | **Algorithm logic, performance, domain correctness, security** |

## Agent Code Review Requirements

When agent review cannot be delegated to ln-510 (inline mode, Team Lead, manual pipeline):

1. **Prompt:** Use `references/agents/prompt_templates/review_base.md` + `modes/code.md`
2. **Scope:** `git diff` of all Story changes (not just last task)
3. **Minimum agents:** 1 (prefer 2 with different focus: correctness vs performance)
4. **Critical verification:** Every agent suggestion with confidence >= 80% must be independently verified by the executor before accepting/rejecting
5. **Output:** Agent findings feed into Quality Score calculation (SUGGESTIONS → CONCERN weight)

## Bug Classes Only Agents Catch

These bug types are invisible to static analysis and convention review:

| Bug Class | Example (API-535) | Why Static Analysis Misses It |
|-----------|-------------------|-------------------------------|
| Algorithm semantics | `break` in loop loses duplicate matches | Valid Python syntax, correct types |
| Collection key collision | `{hash: obj for obj in list}` overwrites duplicates | Types correct, no architecture violation |
| Unbounded operations | `list(query.all())` on user-controlled data | No type error, no lint rule |
| Session state leaks | `set_limit()` mutates connection pool state | Requires DB driver + pooling knowledge |
| N+1 / sequential queries | Loop of individual DB calls | Valid code, requires performance reasoning |
| Encapsulation bypass | `obj._private` with `# noqa` | Lint rule explicitly suppressed |
