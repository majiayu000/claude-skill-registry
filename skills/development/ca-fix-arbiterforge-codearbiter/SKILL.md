---
name: ca-fix
description: "Fix a confirmed bug: a failing regression test first, then a minimal fix, then the rest of the tdd gates."
argument-hint: "<what's happening vs. what should happen>"
---

# $ca-fix — regression-first bug fix

The only permitted entry to bug-fix work. No fix code is written before a regression test reproduces the defect and goes red for the right reason. Give the observed behavior and the expected behavior, plus a stack trace or reproduction when you have one.

**Orientation:** if `.codearbiter/code-map.md` is present, read it before diagnosing — a coarse concern→path→role map that helps locate the defect. Absent is fine; it is read-on-demand.

## Flow

Routes to the `tdd` skill, bug variant — Phase 1 is framed around confirming the defect, not building
new behavior:

1. **Reproduce** the bug consistently.
2. **Locate the root cause** — the exact code path producing the wrong behavior.
3. **Write a regression test** that fails in the current state for the precise reason the bug causes
   (not an unrelated error).
4. **Confirm it's red for the right reason** — the failure message matches the described defect.

Only then does `tdd` proceed: minimal fix to green, then the remaining `tdd` gates. The implementation
agent (`backend-author`, `frontend-author`, or `infra-author`) is selected by where the bug lives. If
the defect cannot be pinned by a failing test, STOP and surface the question.

## Routes to

`tdd` (`${CLAUDE_PLUGIN_ROOT}/routines/tdd/SKILL.md`) — all phases, Phase 1 framed for bug confirmation.

## When NOT to use

- New behavior → `$ca-feature`.
- A behavior-preserving restructure → `$ca-refactor`.
- "Why does it do this?" → `$ca-btw`.
- Persisting fix code already written → `$ca-commit` (the gates still apply).

## Hard gate

MUST NOT write fix code before the regression test is red for the right reason. MUST NOT accept a test
that passes against the broken state as proof of the defect.
