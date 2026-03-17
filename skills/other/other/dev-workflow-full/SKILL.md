---
name: dev-workflow-full
description: Run the full ticket lifecycle end-to-end (Jira or GitHub issue). Chains initialize, start-work, prepare-commit, create-pr, and review-pr. Supports autopilot or pair mode. Use when the user says "full workflow", "end to end", or wants to go from ticket/issue to reviewed PR in one go.
---

# Full Dev Workflow

Run the complete ticket lifecycle back-to-back: create branch, implement, commit, open PR, and review.

## Pipeline

```
dev-workflow-initialize
        ↓
dev-workflow-start-work  (includes dev-workflow-prepare-commit when atomic)
        ↓
  [final commit if needed]   (dev-workflow-prepare-commit)
        ↓
dev-workflow-create-pr
        ↓
dev-workflow-review-pr
```

## Step 0: Choose Mode and Collect Info

**ALWAYS use the AskQuestion tool:**

- Title: "Workflow Mode"
- Questions:
  - id: "mode", prompt: "How would you like to run the workflow?", options:
    - id: "autopilot", label: "Autopilot - collect info upfront, then run everything without prompting"
    - id: "pair", label: "Pair - walk through each step together, I'll confirm at each decision point"

### If Autopilot: Collect Everything Upfront

Gather all required inputs in a **single AskQuestion call** before doing any work:

- id: "source", prompt: "What are you working from?", options:
  - id: "jira", label: "Jira ticket (e.g. RETIRE-123)"
  - id: "github", label: "GitHub issue (URL or owner/repo#N)"
  - id: "unticketed", label: "Unticketed work (use RETIRE-1908)"
- id: "open_cursor", prompt: "Open the new worktree in Cursor?", options:
  - id: "yes", label: "Yes, open in Cursor"
  - id: "no", label: "No, stay here"

If "jira" or "github", ask conversationally for the ticket number or issue URL/ref. Then run initialize with that source (see dev-workflow-initialize for Jira vs GitHub).

**Autopilot defaults** (applied automatically, no prompts):

| Decision Point | Default |
|---|---|
| Branch name | Auto-generated from ticket title |
| Branch/worktree conflict | Create with numeric suffix |
| Commit strategy | Atomic commits |
| Unstaged changes | Stage all changes |
| Minor code issues | Fix automatically |
| Lint errors | Fix automatically (`--fix`) |
| Test failures | **STOP** -- always stop on test failures regardless of mode |
| Commit message | Auto-generated conventional commit |
| Push after commit | Yes |
| Critical issues (secrets, etc.) | **STOP** -- always stop on critical issues regardless of mode |

### If Pair: Proceed Normally

Each sub-skill runs with its full interactive prompts. The user confirms at every decision point. This is the standard behavior of each individual skill.

## Step 1: Initialize

Use the `dev-workflow-initialize` skill to create the branch and worktree.

- **Autopilot**: Use the ticket or issue collected in Step 0 (Jira key, GitHub issue URL/ref, or unticketed). Skip the "Which Ticket or Issue?" prompt. Auto-generate branch name per source type. Skip "Open in Cursor?" (use collected answer). Skip "Start Implementation?" (always yes).
- **Pair**: All prompts go to the user as normal.

## Step 2: Start Work

Use the `dev-workflow-start-work` skill to implement the ticket.

- **Autopilot**: Present the implementation plan for review (always show the plan -- this is the one pause in autopilot). After user confirms, use atomic commit strategy automatically. Skip the commit strategy prompt. During implementation, use the `dev-workflow-prepare-commit` skill after each logical unit with all defaults (stage all, auto-fix minor issues, auto-fix lint, auto-generate message, auto-push).
- **Pair**: All prompts go to the user as normal (plan confirmation, commit strategy, per-commit decisions).

## Step 2.5: Final Commit (single-commit strategy only, pair mode)

Only applies in pair mode when the user chose "single commit at end". Use the `dev-workflow-prepare-commit` skill to review, lint, test, and commit. Auto-push when done.

This step never runs in autopilot (autopilot always uses atomic commits).

## Step 3: Create PR

Use the `dev-workflow-create-pr` skill to push and open the pull request.

- **Autopilot**: Push if needed. Generate PR description and create the PR. Skip "Start PR Review?" (always yes). Proceed directly to Step 4.
- **Pair**: All prompts go to the user as normal.

## Step 4: Review PR

Use the `dev-workflow-review-pr` skill to review the pull request.

- **Autopilot**: Review the current branch's PR automatically. Skip the "Which PR?" prompt.
- **Pair**: All prompts go to the user as normal.

## Step 5: Done

Report the final status:

```
Full workflow complete!

Mode: [Autopilot / Pair]
Ticket/Issue: [TICKET-ID or issue ref]
Branch: [BRANCH-NAME]
Worktree: [PATH]
Commits: [N] atomic commits
PR: [PR-URL]
Review: Posted inline comments
```

## Skipping Steps

If the user is partway through the workflow (e.g., already on a branch with work in progress), detect the current state and skip completed steps:

- **Already on a feature branch with a worktree**: Skip Step 1, start at Step 2
- **Implementation done, changes uncommitted**: Start at Step 2.5
- **Changes committed and pushed**: Start at Step 3
- **PR already exists**: Start at Step 4

Use `git status`, `git log`, and `gh pr view` to detect the current state.

## Hard Stops (Both Modes)

These always halt the pipeline regardless of mode:

- **Test failures**: Stop and report. Never skip failing tests.
- **Critical security issues**: Hardcoded secrets, API keys, credentials. Stop and report.
- **Git/gh errors**: Push failures, auth issues. Stop and report.

The user can re-run the workflow after fixing the issue and it will pick up from where it left off (see "Skipping Steps").
