---
name: pr-workflow
description: |
  Pull request lifecycle: commit, codex review, sync, review, fix, status,
  cleanup, and PR mining. Use when user wants to commit changes, get a
  second-opinion code review from Codex, push changes, create a PR, check PR
  status, fix review comments, clean up branches after merge, or mine tribal
  knowledge from PR reviews. Use for "commit my changes", "codex review",
  "push my changes", "create a PR", "pr status", "fix PR comments",
  "clean up branches", "mine PRs", or "address feedback".
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Task
  - Skill
  - AskUserQuestion
routing:
  force_route: true
  not_for: "general disagreement ('push back on a design'), committing to an idea ('commit to this approach'), pushing out the door, push notifications, social media reviews, metaphorical commit/merge ('commit to a decision', 'merge ideas in your head', 'merge the branches in your head', 'move forward and commit'), 'commit' meaning resolve/decide rather than git-commit — only for git push/commit/PR operations"
  triggers:
    - "push changes"
    - "push my changes"
    - "push to GitHub"
    - "push to remote"
    - "create PR"
    - "sync to GitHub"
    - "PR status"
    - "branch status"
    - "merge readiness"
    - "fix PR comments"
    - "resolve PR feedback"
    - "pr-fix"
    - "cleanup branches"
    - "clean up branches"
    - "merged branches"
    - "delete merged branch"
    - "prune branches"
    - "mine PRs"
    - "extract review comments"
    - "tribal knowledge"
    - "process PR feedback"
    - "address review comments"
    - "submit PR"
    - "create pull request"
    - "send for review"
    - "open PR"
    - "generate branch name"
    - "validate branch name"
    - "name branch"
    - "branch convention"
    - "git branch name"
    - "check CI"
    - "CI status"
    - "actions status"
    - "did CI pass"
    - "build status"
    - "CI passed"
    - "stage and commit"
    - "commit changes"
    - "commit these"
    - "commit my changes"
    - "commit my files"
    - "codex review"
    - "second opinion"
    - "code review codex"
    - "gpt review"
    - "cross-model review"
    - "git push"
    - "push to origin"
    - "push my branch"
    - "push the branch"
    - "ship it"
    - "ship this"
    - "ship this work"
    - "merge these fixes"
    - "merge this work"
    - "merge this in"
    - "make a pull request"
    - "draft a PR"
    - "draft pr"
    - "publish my changes"
    - "publish this"
    - "publish my work"
    - "let's get this reviewed"
    - "send this to GitHub"
    - "send to github"
    - "wrap up and merge"
    - "wrap this up and merge"
  category: git-workflow
  pairs_with:
    - verification-before-completion
    - code-linting
    - systematic-code-review
---

# PR Workflow Skill

Umbrella skill for the entire pull request lifecycle. Routes to the correct reference based on the PR task requested.

## Routing

Detect the user's intent and load the appropriate reference file:

| Intent | Trigger phrases | Reference |
|--------|----------------|-----------|
| **Sync** (default) | "push", "create PR", "sync", "ship this" | `${CLAUDE_SKILL_DIR}/references/sync.md` |
| **Pipeline** | "submit PR", "full PR", "end-to-end PR", "open PR" | `${CLAUDE_SKILL_DIR}/references/pipeline.md` |
| **Fix** | "fix PR comments", "address review", "pr-fix", "resolve feedback" | `${CLAUDE_SKILL_DIR}/references/fix.md` |
| **Status** | "pr status", "branch status", "is my PR ready", "check CI" | `${CLAUDE_SKILL_DIR}/references/status.md` |
| **Cleanup** | "clean up branches", "delete merged branch", "prune" | `${CLAUDE_SKILL_DIR}/references/cleanup.md` |
| **Feedback** | "process PR feedback", "address reviews", "what did reviewers say" | `${CLAUDE_SKILL_DIR}/references/feedback.md` |
| **Miner** | "mine PRs", "extract review comments", "tribal knowledge", "reviewer patterns" | `${CLAUDE_SKILL_DIR}/references/miner.md` |
| **Branch name** | "generate branch name", "validate branch name", "name branch", "branch convention", "git branch name" | `${CLAUDE_SKILL_DIR}/references/branch-name.md` |
| **CI check** | "check CI", "CI status", "actions status", "did CI pass", "build status", "CI passed" | `${CLAUDE_SKILL_DIR}/references/ci-check.md` |
| **Commit** | "commit changes", "stage and commit", "commit my changes", "commit my files", "commit these" | `${CLAUDE_SKILL_DIR}/references/commit.md` |
| **Codex review** | "codex review", "second opinion", "code review codex", "gpt review", "cross-model review" | `${CLAUDE_SKILL_DIR}/references/codex-review.md` |

**Default action**: When invoked with no arguments or ambiguous intent, load `sync.md` (the most common PR use case).

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| "push", "create PR", "sync", "ship this" | `sync.md` | **Sync** (default) |
| "submit PR", "full PR", "end-to-end PR", "open PR" | `pipeline.md` | **Pipeline** |
| "fix PR comments", "address review", "pr-fix", "resolve feedback" | `fix.md` | **Fix** |
| "pr status", "branch status", "is my PR ready", "check CI" | `status.md` | **Status** |
| "clean up branches", "delete merged branch", "prune" | `cleanup.md` | **Cleanup** |
| "process PR feedback", "address reviews", "what did reviewers say" | `feedback.md` | **Feedback** |
| "mine PRs", "extract review comments", "tribal knowledge", "reviewer patterns" | `miner.md` | **Miner** |
| "generate branch name", "validate branch name", "name branch", "branch convention", "git branch name" | `branch-name.md` | **Branch name** |
| "check CI", "CI status", "actions status", "did CI pass", "build status", "CI passed" | `ci-check.md` | **CI check** |
| "commit changes", "stage and commit", "commit my changes", "commit my files", "commit these" | `commit.md` | **Commit** |
| "codex review", "second opinion", "code review codex", "gpt review", "cross-model review" | `codex-review.md` | **Codex review** |

## Mandatory PR Body Structure

`gh pr create --body "..."` is how every agent in this toolkit opens PRs, and it **bypasses `.github/pull_request_template.md` entirely** — GitHub only applies that file to the web UI and to a bare `gh pr create` with no `--body`. So the structure must be reproduced in the `--body` string by hand.

Every agent-authored PR body uses the same three sections as `.github/pull_request_template.md`, in this order: **Summary → Changes → Notes**. This keeps PR bodies consistent across models (Opus, Sonnet, and every other harness produce the same shape).

Tests run as GitHub Actions, so the Checks tab is the test record. Let CI carry the proof: keep command output (ruff exit, pytest counts, gate traces, dogfood runs) out of the body. Pasting `$ pytest → N passed` duplicates the Checks tab and bloats the PR — leave it to CI.

### Write for Density

Aim for high meaning per word: each line states one fact about the change, declaratively, so a reviewer understands it fast. Density is the target, not minimal length — a large change keeps the three sections and carries the detail it needs; it earns that length by packing each line with signal. Four rules carry the vibe:

1. **One fact per line.** Each Changes line reads verb + what + where; Summary states the goal and why. Plain words, high meaning.
2. **Summary states the goal.** 1-3 plain sentences or a few crisp bullets. Keep metrics to the single number that matters.
3. **One line per change.** When a change has many sub-items, state the shape and count ("add 21 PR-creation trigger phrases") and let the diff enumerate them. Keep rationale to the clause that earns its place.
4. **Notes carries non-obvious signal — required when a trigger applies.** Omit it for routine PRs and drop the section when nothing qualifies. Note it, one terse declarative line per point, when a reviewer cannot infer the signal from the diff: a non-obvious decision, a deliberate omission, a follow-up, a gotcha, a "supersedes #N". Note it too when a RISK/VERIFICATION trigger holds — manual verification was performed; part of the change sits outside CI coverage; migration/rollout ordering matters; a security-sensitive surface changed (e.g. `Not covered by CI — terraform plan is manual`). State each caveat as one fact and let CI carry command output. Skip what is always true (a PR can be reverted; CI runs the tests).

**Worked example — the shape to emulate (#608-good vs #710-bad):**

| Section | Dense (emulate, like #608) | Bloated (rewrite toward dense, the #710 shape) |
|---------|-----------------|--------------------------------|
| Summary | "Registers 3 hooks in settings.json; integrates `pre-route.py` into /do Phase 2 as a deterministic pre-filter." | One 5-sentence block stuffed with jargon and four metrics. |
| Changes | "`SKILL.md` — add 21 PR-creation trigger phrases." | One bullet inlining all 21 phrases verbatim; another a 3-sentence rationale paragraph. |
| Notes | "Not covered by CI — the Terraform plan is applied manually." or "Apply the column migration before deploying." (a required risk/verification caveat) — or omitted entirely when nothing qualifies | "Roll back by reverting the branch commits. Tests run in CI — see Checks." (always-true filler) plus a pasted `pytest -v` dump and a Scope & Risk wall. |

The dense column reads in seconds because each cell carries facts; the bloated column buries the same facts in volume (and re-states what the Checks tab already shows). Aim every body at the dense column.

Copy this canonical skeleton into `--body`:

```markdown
## Summary
<!-- State the goal plainly: 1-3 sentences or a few crisp bullets, one fact per line. Name the ADR/issue if any. Keep metrics to the single number that matters. -->

## Changes
<!-- One line per change: verb + what + where. State shape and count for many sub-items; let the diff enumerate them. -->
- `path/or/area` — what changed

## Notes
<!-- Omit for routine PRs (drop the section when nothing qualifies). Note it, one terse declarative line per point, when a reviewer cannot infer the signal from the diff: a non-obvious decision, a deliberate omission, a follow-up, a gotcha, a "supersedes #N". Note it too when a RISK/VERIFICATION trigger holds — manual verification was performed; part of the change sits outside CI coverage; migration/rollout ordering matters; a security-sensitive surface changed (e.g. `Not covered by CI — terraform plan is manual`). Let CI carry command output. Skip what is always true (a PR can be reverted; CI runs the tests). -->
```

The sync (`sync.md` Step 5) and pipeline (`pipeline.md` Phase 5) references carry this same skeleton at their `gh pr create` call sites. When either path writes a `--body`, it uses this structure and the density rules above.

## Instructions

1. Identify the user's PR task from their message
2. Load the matching reference file from the table above
3. Follow the instructions in that reference file exactly
4. When the task creates a PR, build the `--body` from the canonical three-section skeleton above (Summary / Changes / Notes), because `--body` bypasses the GitHub template file. Tests run in CI — the Checks tab is the test record, so keep command output out of the body
