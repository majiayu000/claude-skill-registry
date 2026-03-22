---
name: review-changes
description: End-to-end review pipeline — creates a handoff, generates a review (self-review or paste-ready for another provider), then offers to fix findings. Use when you want to review your changes before pushing.
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Bash, Read, Edit, Grep, Glob, Write
argument-hint: "[optional session name or issue reference]"
read-only: false
destructive: true
idempotent: false
open-world: true
user-invocable: true
tags: review, code-quality, pipeline
capabilities: review.orchestrate, review.pipeline
activation-intents: review my changes, run review pipeline, self review changes
activation-events: user-prompt, session-start
activation-artifacts: .chalk/reviews/**, **/*
risk-level: high
---

# Review Changes

Orchestrate the full review pipeline: handoff → review → fix. This skill chains three phases with user checkpoints between each.

## Phase 1: Create Handoff

Run the full handoff generation inline (do not invoke `/create-handoff` as a sub-skill — execute the steps directly):

### Step 1.1: Determine the session name

1. If the user provided `$ARGUMENTS`, sanitize it using a shell command — not LLM interpretation — to produce a safe kebab-case string:
   ```sh
   echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9-]+/-/g; s/^-+//; s/-+$//; s/-{2,}/-/g'
   ```
   Use the output as the session name. If the sanitized result is empty, fall back to option 2.
2. Otherwise, infer from the current branch name (e.g. `feature/issue-24-authentication` → `issue-24-authentication`)
3. If on `main`/`master`, ask the user what to name the session

### Step 1.2: Create the session directory

```sh
SESSION_DIR=".chalk/reviews/sessions/${session_name}"
mkdir -p "$SESSION_DIR"
```

If a handoff file already exists with content, ask the user whether to overwrite or skip to Phase 2.

### Step 1.3: Determine the base branch

1. `git merge-base main HEAD`
2. If that fails, try `origin/main`, then `master`, `origin/master`

Store as `{base}`.

### Step 1.4: Gather context

```sh
git log --oneline {base}..HEAD
git diff --stat {base}..HEAD
git diff {base}..HEAD
```

### Step 1.5: Detect and run project checks

Auto-detect the project's build/check tooling and run what's available:

- **Node.js** (`package.json`): detect pm from lockfile, run build/typecheck/lint/test
- **Rust** (`Cargo.toml`): cargo check, cargo test --no-run, cargo clippy
- **Go** (`go.mod`): go build, go vet, go test -short
- **Python** (`pyproject.toml`/`requirements.txt`): py_compile, pytest --co
- **Make** (`Makefile` with build/check/test targets): make build/check/test
- If nothing detected, note "No build system detected"

If any check fails, note the failure honestly — do NOT try to fix it.

### Step 1.6: Write the handoff

Write to `$SESSION_DIR/handoff.md`:

```markdown
# Handoff

## Scope
- Item: {item reference}
- Goal: {1-sentence summary}

## What Changed
{bullet list of logical changes}

## Files Changed
{bullet list from git diff --stat}

## Risk Areas
{bullet list of things that could break}

## Commands Run
{bullet list with pass/fail status}

## Known Gaps
{bullet list of things NOT done}

## Suggested Focus For Reviewers
{bullet list prioritized by risk}
```

### Step 1.7: Report handoff

Show the handoff file path and a brief summary of what was captured.

---

## Phase 2: Review

**Ask the user how they want to proceed:**

Present these options:
- **Self-review** — Claude reviews the changes right now in this session
- **Copy for external review** — Generate a paste-ready prompt to use with another AI (Codex, Gemini, GPT, etc.)

### Option A: Self-review

If the user chooses self-review:

1. Read the full diff: `git diff {base}..HEAD`
2. Read the handoff from Phase 1
3. Review the changes using the same structured format as the universal reviewer template:

```markdown
## Verdict
- Block merge: yes|no
- Blocking findings: P0=<n>, P1=<n>

## Findings

| ID | Severity | Category | File:Line | Issue | Failure mode | Suggested fix | Confidence |
|---|---|---|---|---|---|---|---|

## Testing Gaps
-

## Open Questions
-
```

4. Write the findings to `$SESSION_DIR/self.findings.md`
5. Present the findings summary to the user

### Option B: External review

If the user chooses external review:

1. Bootstrap the review pipeline scripts if not already present — invoke `/create-review` which will create the scripts and templates with their exact, version-controlled content. Do NOT generate the scripts inline.
2. Generate the review pack: `bash .chalk/reviews/scripts/pack.sh "{base}" "{session_name}"`
3. Generate the prompt: `bash .chalk/reviews/scripts/render-prompt.sh "reviewer" "" "" "" "{session_name}"`
4. Copy to clipboard if possible
5. Tell the user: "Prompt copied — paste it into your reviewer. When you have the findings, save them to `$SESSION_DIR/{reviewer-name}.findings.md` and tell me to continue."
6. **Wait for the user to come back.** When they say they're ready or tell you to continue, proceed to Phase 3.

---

## Phase 3: Fix Findings

**Ask the user:** "Want me to fix the findings?"

If yes:

### Step 3.1: Load findings

Discover all `*.findings.md` files in the session directory using the Glob tool:

```
.chalk/reviews/sessions/{session_name}/*.findings.md
```

Do NOT use shell `ls` — use the Glob tool for safe discovery.

### Step 3.2: Parse and prioritize

Extract the findings table from each file. Sort by severity: P0 > P1 > P2 > P3.

Deduplicate findings that target the same file and line (or lines within 5 of each other) across reviewers.

### Step 3.3: Present findings

Show a prioritized summary table and ask the user:
- **All** — fix P0-P2
- **Blocking only** — fix P0 and P1
- **Let me choose** — pick specific IDs

### Step 3.4: Apply fixes

For each finding:

1. **Validate the file path** — must be relative and within the repo. Reject absolute paths or `..` traversal
2. **Read the file** with at least 30 lines of surrounding context
3. **Design the fix** using the suggested fix as guidance
4. **Show the proposed fix and ask for confirmation before applying**
5. **Apply** using Edit tool

### Step 3.5: Update resolution log

Write `.chalk/reviews/sessions/{session_name}/resolution.md`:

```markdown
# Finding Resolution Log

## Summary
- Session: {session_name}
- Item: {from session name}
- Reviewers: {list of sources}
- Decision owner:

## Findings

| ID | Severity | Source | File:Line | Decision | Notes |
|---|---|---|---|---|---|

## Follow-up Tasks
-

## Final Gate
- Build:
- Tests:
- Ready to merge: yes/no
```

### Step 3.6: Final summary

Show results table, resolution log path, and suggest:
- Run build/tests to verify
- Run `/commit` to commit the fixes
- Create or update the PR

If no:

Tell the user the findings are saved at their session path and they can run `/fix-findings` later when ready.

---

## Rules

- Do NOT modify source code during Phase 1 or Phase 2 — only during Phase 3 with user confirmation
- Be honest about failures in the handoff
- Always ask before proceeding to the next phase — never auto-advance
- Keep the self-review objective and rigorous — do not rubber-stamp your own changes
- All file paths from findings must be validated as relative and within the repo
- If multiple reviewers have conflicting suggestions, present both and let the user choose
