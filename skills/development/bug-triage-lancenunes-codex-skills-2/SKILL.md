---
name: bug-triage
description: Reproduce, isolate, and fix a bug (or failing build/test), then summarize root cause, fix, and verification steps. Use when the user reports a bug, regression, or failing build/test and wants a fix.
---

# Bug triage

## Goal
Turn an ambiguous bug report into:
- a reliable repro (or a clear “cannot reproduce yet” with next info to collect)
- a root-cause explanation
- a minimal, reviewed fix
- verification steps (commands + manual checks)

## First checks
1) Read any repo-specific guidance (`AGENTS.md`, `CONTRIBUTING.md`, README).
2) Clarify impact: severity, who is affected, and whether it’s a regression.

## If info is missing, ask for it
- Exact steps to reproduce (starting state + inputs).
- Expected vs actual behavior.
- Error text / stack trace / logs (full, unedited if possible).
- Environment: OS, runtime versions (Node/Bun), browser, commit hash/tag.
- Frequency: always / sometimes / only certain data.
- “Last known good” version or approximate date when it started.

## Workflow (checklist)
1) Reproduce locally
   - Prefer the simplest, fastest repro.
   - If it’s flaky, try to reduce nondeterminism (seed, fixed time, retries).
2) Localize the failure
   - Narrow to a file/function/component/config.
   - Use `rg` to find relevant code paths and error strings.
3) Identify root cause
   - Form a hypothesis, confirm with logs/breakpoints, then refine.
   - If it’s a regression and git history exists, consider `git bisect`.
4) Implement the minimal fix
   - Fix the cause, not the symptom.
   - Avoid drive-by refactors and formatting churn.
5) Verify
   - Run the project’s standard checks (lint/tests/build).
   - Re-run the repro steps and confirm the fix.

## Repo-aware command hints
Use what the repo actually uses:
- If `bun.lock` exists: prefer `bun ...` (e.g. `bun lint`, `bun build`, `bun dev`).
- Otherwise: use the project’s documented commands (`npm`, `pnpm`, `yarn`, etc.).
 - If `bun.lock` exists but `bun` is not available, tell the user and ask whether to install `bun` or use the repo’s alternative package manager.

## Deliverable (paste this in the chat / PR / issue)
Use this format:
- **Summary:** ...
- **Repro:** ...
- **Root cause:** ...
- **Fix:** ...
- **Verification:** ...
- **Risk/notes:** ...

If you need a bug-report structure to ask the user for, use `references/bug-report-template.md`.
