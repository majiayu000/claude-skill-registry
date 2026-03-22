---
name: dev-local-review
description: Run a local code review using the CodeRabbit agent before pushing to catch issues early
argument-hint: "[--base branch]"
disable-model-invocation: false
---

Run a local code review before pushing to catch issues before they hit the PR
and burn a review round. Uses the built-in CodeRabbit code-reviewer agent
(`subagent_type: "coderabbit:code-reviewer"`) which runs entirely locally at
zero cost.

**This is not a substitute for the GitHub PR review.** The local review cannot
access CodeRabbit's learnings from past PRs or perform repo-wide architectural
analysis. It is a fast, free pre-push gate that catches the obvious issues.

## How it works

The skill uses Claude Code's built-in `coderabbit:code-reviewer` agent type.
This agent reads the diff locally and performs a thorough code review covering
correctness, style, documentation accuracy, and common issues. No external
service, CLI tool, or API key required.

## Usage

Invoke the skill before pushing:

```text
/dev-local-review
```

Or with a specific base branch:

```text
/dev-local-review --base develop
```

## When to use

- Before pushing fixes during `/dev-review-pr` — catch new issues locally
  instead of waiting for the GitHub bot
- Before creating a PR with `/dev-create-pr` — clean up obvious issues
  before the first review
- Any time you want a quick code quality check without pushing
- After `/dev-final-pass` for a second opinion from a different reviewer

## Workflow

### 1. Determine what to review

Check `git status` and `git diff --stat` to understand the scope of changes.
Use the base branch from the argument (default: `main`).

### 2. Run the CodeRabbit code-reviewer agent

Launch a single agent with `subagent_type: "coderabbit:code-reviewer"`. The
prompt must include:

- The list of modified and new files (from `git diff --stat` and `git status`)
- A summary of what the changes are about (infer from file paths and recent
  context)
- Instructions to be thorough and report specific file paths and line numbers
- The project's code quality requirements (C99, SDL3 GPU, CLAUDE.md conventions)

```text
Agent(
  subagent_type="coderabbit:code-reviewer",
  prompt="Review all changes compared to <base-branch>. [file list, context, instructions]"
)
```

### 3. Triage findings

When the agent returns, present findings sorted by severity (Major, Medium,
Low, Informational). For each finding, determine:

- **Actionable:** A real issue that should be fixed before pushing
- **Intentional:** Code that is correct as-is (e.g., strict `0.0f` epsilon
  for determinism tests)
- **Out of scope:** Suggestions about code not changed in this PR

### 4. Fix actionable findings

Implement all actionable fixes. Do not ask about each one individually —
fix them all, then report what was changed.

### 5. Re-run review (MANDATORY — cannot skip)

After fixing, run the agent again to verify no new issues were introduced.
The re-run prompt should note which issues were already addressed so the
agent focuses on finding new problems.

### 6. Repeat until zero feedback (MANDATORY — strict rule)

**This is an absolute rule with no exceptions.** The review loop MUST
continue until the CodeRabbit agent returns with **zero findings**. The
agent executing this skill is **not allowed** to decide on its own that
remaining feedback is "just a nitpick" or "informational" and stop the
loop early.

**The only two valid exit conditions are:**

1. **The review agent reports zero findings.** The loop ends. Proceed to
   "After a clean local review."
2. **The agent explicitly asks the user** whether to stop (presenting the
   remaining findings), **and the user agrees** to stop. Without user
   confirmation, the loop continues.

**Prohibited behaviors:**

- Deciding that remaining findings are "low severity" and stopping
- Classifying all remaining findings as "intentional" without user input
- Stopping after a fixed number of rounds (e.g., "typically 2-3 rounds")
- Summarizing remaining findings and moving on without fixing or asking
- Treating nitpicks, style suggestions, or informational comments as
  automatic reasons to exit the loop

**Each round of the loop:**

1. Run the CodeRabbit review agent
2. If zero findings → exit loop (clean)
3. If findings exist → fix actionable ones, ask user about ambiguous ones
4. Go to step 1

If the same finding keeps reappearing after being fixed, investigate the
root cause rather than stopping the loop. If genuinely stuck, ask the user
for guidance — do not silently exit.

## What it catches

Based on project experience, this review reliably catches:

- Missing bounds checks and safety guards
- Stale comments (e.g., `<math.h>` comment listing `fabsf, sqrtf` but code
  also uses `fminf`)
- Documentation/code mismatches (README describes N phases but code has M)
- Missing inline comments on struct fields
- Resource cleanup gaps on error paths
- Magic numbers that should be named constants
- Naming convention violations
- Bare C stdlib calls without `SDL_` prefix (fabsf, sinf, memset, strcmp,
  malloc, etc.) — use SDL equivalents or approved project wrappers
  (`forge_isfinite`, `forge_fmaxf`, `forge_fminf`) for cross-platform portability

## What it cannot do

- Access CodeRabbit's learnings from past PR interactions
- Perform repo-wide architectural analysis beyond the changed files
- Interact with PR feedback threads or resolve conversations
- Update GitHub approval state
- Guarantee a clean PR review (the GitHub bot may find additional issues)

## After a clean local review

A clean local review means the obvious issues are handled. Push and request
a full PR review:

1. **Push** the commits (single push, never piecemeal)
2. **Wait for CodeRabbit's PR review** — it may find additional issues the
   local review missed
3. If the PR review finds issues, use `/dev-review-pr` to handle them
