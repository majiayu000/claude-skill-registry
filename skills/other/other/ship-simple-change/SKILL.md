---
name: ship-simple-change
description: Run the full push-and-PR flow for a simple change with no prompts after start. Collects files, ticket (or unticketed RETIRE-1908), and optional branch/commit message up front, then stages, lints, tests, commits, pushes, and creates the PR. Use when the user wants to push a change and open a PR in one go without interruption.
---

# Ship Simple Change

Automate the full flow: stage specified files → lint → test → commit → push → create PR. **Collect all required information up front**, then run **without further prompts**.

## When to Use

- User says "push this and create a PR", "ship this change", "commit, push, and open a PR uninterrupted"
- User wants to use the same flow as prepare-commit + create-pr but in one shot with no confirmations

## Phase 1: Collect Information Up Front

Before running any git or npm commands, gather (or infer) the following. If anything critical is missing, **ask once** in a single message:

| Input                | Required | Notes                                                                                                                 |
| -------------------- | -------- | --------------------------------------------------------------------------------------------------------------------- |
| **Files to include** | Yes      | Explicit paths (e.g. `maestro/utils/expoMenu.yml`) or "all staged" / "current changes". Do not stage unrelated files. |
| **Ticket**           | Yes      | Jira key (e.g. `RETIRE-1234`) or **unticketed** → use **RETIRE-1908** (placeholder for unticketed work).              |
| **Branch name**      | No       | Default: `[TICKET]-[kebab-case-summary]` from change summary (e.g. `RETIRE-1908-expo-menu-any-port`).                 |
| **Commit message**   | No       | Default: conventional commit generated from staged diff (`type: short description`).                                  |

**Single prompt if missing:**

```
To run the full flow without stopping, I need:
1. Which file(s) to include (e.g. path or "these changes").
2. Ticket: Jira key (e.g. RETIRE-1234) or say "unticketed" for RETIRE-1908.

Optional: branch name, or commit message (type + description).
```

After this, do **not** ask for confirmation before commit, push, or PR creation. Run through to the end and report the PR URL (or the step where you stopped and why).

## Phase 2: Execute Uninterrupted

Run these steps in order. Do not prompt the user between steps. Stop only on hard failures (critical issues in code, lint/test failure after fix attempt, or git/gh errors).

### Step 1: Ensure Correct Branch

- If **already on a feature branch** (not `main`/`master`): use it; ensure it tracks `origin` and is up to date if needed.
- If **on main**: create and checkout a new branch:
  - Branch name: user-provided or `[TICKET]-[kebab-summary]` (e.g. from file names or one-line summary).
  - Base: `origin/main`.

```bash
git fetch origin main
git checkout -b [BRANCH_NAME] origin/main
```

### Step 2: Stage Only Specified Files

- Stage exactly the files the user specified. Do not stage unrelated or untracked files (e.g. `.cursor/`, `report.xml`).

```bash
git add [FILE1] [FILE2] ...
git diff --staged --stat
```

### Step 3: Review Staged for Critical Issues Only

- Scan `git diff --staged` for **critical** issues only: hardcoded secrets, API keys, credentials, sensitive data.
- If found: **stop**, report file/line and what was found. Do not commit.
- Minor issues (e.g. console.log, extra blanks): note but do not block; fix only if trivial and no extra prompts.

### Step 4: Lint

```bash
npm run lint
```

- If lint fails: run `npm run lint -- --fix`, then `npm run lint` again.
- If it still fails: **stop** and report the errors. Do not commit.

### Step 5: Tests

```bash
npm test
```

- If tests fail: **stop** and report. Do not commit or push.

### Step 6: Generate Commit Message and Commit

- From `git diff --staged`, choose a **conventional type**: `feat` | `fix` | `docs` | `style` | `refactor` | `perf` | `test` | `chore`.
- Short description: imperative, ~50 chars, no scope in parentheses.
- Commit with **no** co-author or other trailers.

```bash
git commit -m "<type>: <short description>"
```

Example: `chore: make expo menu flow work for any port number`

### Step 7: Push

```bash
git push -u origin [BRANCH_NAME]
```

- If push fails (e.g. auth, network): **stop** and report.

### Step 8: Create PR

- **Jira link**: If branch/ticket starts with `RETIRE`, use `https://gustohq.atlassian.net/browse/[TICKET]`. Otherwise use `https://internal.guideline.tools/jira/browse/[TICKET]`.
- **Body**: Use the `[[[...]]]` block format from the repo PR template:

```
[[[
**jira:** [TICKET](URL)
**what:** One sentence (or bullets) summarizing the change.
**why:** Why the change was needed.
**who:** Who is affected (users, teams, or "no user impact").
]]]
```

- **Title**: Same as commit message: `type: short description`.
- Create the PR; do not ask before creating.

```bash
gh pr create --title "<type>: <short description>" --body "<body with [[[...]]] block>"
```

- If a PR for this branch already exists: report the existing PR URL and stop.

### Step 9: Report Result

- Output the PR URL (e.g. from `gh pr view --json url --jq '.url'`).
- If you stopped earlier (lint, test, critical issue, push failure), report the step and the reason.

## Conventions

- **Unticketed work**: Always use ticket **RETIRE-1908** and say so in the PR body (e.g. "Placeholder ticket for unticketed work" in **what** or **why** if useful).
- **Commit**: One commit per run. Message = conventional only; no trailers.
- **Base branch**: New branches are from `origin/main`. PR base is `main` unless the user specified otherwise up front.

## Error Handling (No Prompts)

| Situation                                     | Action                                           |
| --------------------------------------------- | ------------------------------------------------ |
| Critical issue in staged diff (secrets, etc.) | Stop; report file/line and issue. Do not commit. |
| Lint fails after `--fix`                      | Stop; report lint errors.                        |
| Tests fail                                    | Stop; report test failures.                      |
| Push fails                                    | Stop; report error.                              |
| PR already exists for branch                  | Report existing PR URL; do not create another.   |
| Branch is `main`                              | Create new branch from `origin/main` (Step 1).   |

Do not offer "proceed anyway" for critical issues or failing tests. Only stop and report.

## Related Skills

This skill is the **uninterrupted** variant of the same flow. For interactive steps (confirm message, confirm push, confirm PR), use instead:

- **prepare-commit** — commit with confirmations at each step
- **create-pr** — create PR after push, with option to review
- **start-ticket** — create worktree + branch from a Jira ticket (or RETIRE-1908 for unticketed work)

## Checklist (for the agent)

```
- [ ] Gathered files, ticket (or unticketed → RETIRE-1908), and optional branch/commit up front
- [ ] On correct branch (created from main if needed)
- [ ] Staged only specified files
- [ ] No critical issues in staged diff
- [ ] Lint passed (or fixed and re-run)
- [ ] Tests passed
- [ ] Committed with conventional message, no trailers
- [ ] Pushed to origin
- [ ] PR created with [[[...]]] body and correct Jira link
- [ ] Reported PR URL (or step + reason if stopped)
```
