---
name: qa
description: Lightweight conversational QA mode — user reports bugs in plain language, agent clarifies minimally, files GitHub issues that survive refactors. Trigger when the user says "QA", "QA session", wants to file bugs conversationally, or starts ad-hoc reporting without a fixed deliverable shape. Differentiates from branch-scoped review and PR-scoped review.
---

Run an interactive QA session. The user describes problems. You clarify lightly, explore the codebase in the background for domain language, and file issues that are durable and user-focused. Each issue is independent — never batch.

## For Each Reported Issue

### 1. Listen, lightly clarify

Let the user describe the problem in their own words. Ask **at most 2-3 short questions**, only on:
- Expected vs actual behavior
- Steps to reproduce (if not already obvious)
- Consistent vs intermittent

Do NOT over-interview.

### 2. Explore in background

Dispatch an Explore agent in parallel while the user talks. Goal is **NOT** to find a fix — it is to:
- Learn the domain language used in that area (read `UBIQUITOUS_LANGUAGE.md` if present)
- Understand what the feature is supposed to do
- Identify the user-facing behavior boundary

Context informs the issue body; the issue body itself does NOT cite files, line numbers, or internal module names.

### 3. Assess scope

Single issue or breakdown? Break down when fix spans multiple independent areas, separable concerns parallelize across people, or user describes multiple distinct failure modes.

### 4. File via `gh issue create`

Do NOT ask the user to review the body first — file it, share URLs.

**Issue body rules:**
- No file paths, no line numbers
- Use the project's domain language; never internal symbol names
- Describe behavior, not code: "the sync service fails to apply the patch", not "applyPatch() throws on line 42"
- Reproduction steps are mandatory
- 30-second readability — concise

### Single-Issue Template

```
## What happened
Plain-language actual behavior.

## What I expected
Plain-language expected behavior.

## Steps to reproduce
1. Concrete step using domain terms
2. Concrete step
3. Concrete step (include relevant inputs/flags)

## Additional context
Observations from the user or background exploration.
```

## Reproduction-Step Examples

**Web app:**
1. Sign in as a Pro-tier user
2. Open the export dialog from the Reports tab
3. Choose CSV format and click Export
4. Observe: download fails silently with no toast.

**CLI tool:**
1. Run `mycli migrate --target=v3 --dry-run`
2. Pipe stderr to a file
3. Observe: stderr contains a stack trace despite `--dry-run`.

## Continuation

Keep going until the user signals done. One issue per round-trip. Never batch.

## Modality Differentiation Appendix

| Skill            | Scope                              | Trigger                                       | Artifact                                      |
| ---------------- | ---------------------------------- | --------------------------------------------- | --------------------------------------------- |
| **qa**           | Ad-hoc conversational exploration  | User-driven, free-form bug reports            | Multiple GitHub issues per session            |
| *branch review*  | Active branch diff vs base         | Explicit invocation on current work           | Single structured review report               |
| *PR review*      | A specific GitHub PR vs its base   | PR URL or number, runs `gh pr view`           | PR comments + summary report                  |

Use **qa** when the user is exploring; use branch review when finishing branch work; use PR review when reviewing someone else's PR.
