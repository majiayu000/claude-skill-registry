---
name: create-handoff
description: Generate a handoff document after implementation work is complete — summarizes changes, risks, and review focus areas for the review pipeline. Use when done coding and ready to hand off for review.
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Bash, Read, Glob, Grep, Write
argument-hint: "[optional session name or issue reference]"
read-only: false
destructive: false
idempotent: true
open-world: true
user-invocable: true
tags: review, handoff, collaboration
capabilities: review.handoff.create, review.pipeline
activation-intents: create handoff, write handoff, hand off changes
activation-events: user-prompt
activation-artifacts: .chalk/reviews/**
risk-level: low
---

# Create Handoff

Generate a structured handoff document summarizing implementation work for the review pipeline.

## Step 1: Determine the session name

Derive a session name from context:

1. If the user provided `$ARGUMENTS`, sanitize it to a safe kebab-case string (lowercase, strip any characters that aren't alphanumeric or hyphens, collapse multiple hyphens) and use that as the item name
2. Otherwise, infer from the current branch name (e.g. `feature/issue-24-authentication` → `issue-24-authentication`)
3. If on `main`/`master`, ask the user what to name the session

## Step 2: Create the review session

Create the session directory and handoff file:

```sh
SESSION_DIR=".chalk/reviews/${session_name}"
HANDOFF_PATH="$SESSION_DIR/handoff.md"
mkdir -p "$SESSION_DIR"
```

If the handoff file already exists with content beyond the template, ask the user whether to overwrite or create a new timestamped session.

## Step 3: Determine the base branch

Figure out what the current branch was based on:

1. Check for a merge base with `main`: `git merge-base main HEAD`
2. If that fails, try `origin/main`
3. If that fails, try `master` / `origin/master`

Store this as `{base}` for later steps.

## Step 4: Gather context

Run these to understand the scope of changes:

```sh
git log --oneline {base}..HEAD
git diff --stat {base}..HEAD
git diff {base}..HEAD
```

## Step 5: Detect and run project checks

Auto-detect the project's build/check tooling and run what's available. Check for these in order:

**Node.js** — if `package.json` exists:
- Detect package manager: `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, else npm
- Run build: `{pm} run build 2>&1 | tail -5`
- Run typecheck: `{pm} run typecheck 2>&1 | tail -5` OR `npx tsc --noEmit 2>&1 | tail -5`
- Run lint: `{pm} run lint 2>&1 | tail -5`
- Run test: `{pm} run test 2>&1 | tail -5`

**Rust** — if `Cargo.toml` exists:
- `cargo check 2>&1 | tail -5`
- `cargo test --no-run 2>&1 | tail -5`
- `cargo clippy 2>&1 | tail -5`

**Go** — if `go.mod` exists:
- `go build ./... 2>&1 | tail -5`
- `go vet ./... 2>&1 | tail -5`
- `go test ./... -short 2>&1 | tail -5`

**Python** — if `pyproject.toml` or `requirements.txt` exists:
- `python -m py_compile` on changed `.py` files
- `python -m pytest --co -q 2>&1 | tail -5` (collect only, don't run)

**Make** — if `Makefile` exists with `build`/`check`/`test` targets:
- `make build 2>&1 | tail -5`
- `make check 2>&1 | tail -5`
- `make test 2>&1 | tail -5`

If no build system is detected, note "No build system detected — skipped automated checks".

**Important:** If any check fails, note the failure — do NOT try to fix it. The handoff should report the current state honestly.

## Step 6: Write the handoff

Write to `HANDOFF_PATH`. Use this format:

```markdown
# Handoff

## Scope
- Item: {item reference — e.g. "#24 — Add authentication" or "Refactor IPC layer"}
- Goal: {1-sentence summary of what was accomplished}

## What Changed
{bullet list of logical changes — describe WHAT each change does, not just file names}

## Files Changed
{bullet list of every file modified/created, from git diff --stat}

## Risk Areas
{bullet list of things that could break, have edge cases, or need careful review}

## Commands Run
{bullet list of every command run and its pass/fail status}

## Known Gaps
{bullet list of things NOT done — e.g. "no tests written", "error handling incomplete", "hardcoded values"}

## Suggested Focus For Reviewers
{bullet list of what reviewers should look at most carefully — prioritize by risk}
```

## Step 7: Report to the user

Show:
- The handoff file path
- A brief summary of what was captured
- Suggest next step: run `/create-review` to generate a review prompt for any AI reviewer

## Rules

- Do NOT modify any source code — this skill is read-only except for the handoff file
- Be honest about failures — if build/typecheck fail, report that clearly
- Keep descriptions concrete and actionable — avoid vague statements like "various improvements"
- List ALL files from `git diff --stat`, don't summarize or skip any
- If there are no commits ahead of base, warn the user that there's nothing to hand off
