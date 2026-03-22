---
name: gh-pr-review-fix
description: Fetch unresolved GitHub PR review threads, normalize them, fix them end-to-end, verify the results, and re-check until the PR is clean or blocked. Use when the user wants GitHub PR comments resolved with minimal verified fixes. Do not use for local review files, Codex reviews, or Zen reviews; review-remediation owns those.
---

# GitHub PR Review Fix

Use this skill as the sole GitHub PR review remediation workflow.

## Autonomous Invocation

If the user explicitly invokes `$gh-pr-review-fix` with no extra detail:

1. Read the repo `AGENTS.md`.
2. Infer the target repo and PR with `scripts/prepare_pr_bundle.py`.
3. Fetch a normalized unresolved-thread bundle.
4. Prioritize valid findings by file and severity.
5. Apply the minimal fixes that fully resolve the findings.
6. Run repo-native verification.
7. Create one scoped conventional commit and push if checks pass.
8. Re-fetch unresolved threads and continue until zero remain or the workflow is blocked.

Stop and ask only when the repo/PR cannot be inferred, GitHub auth is unavailable, the worktree is too ambiguous to safely stage, or repo policy conflicts with automatic remediation.

## Workflow

1. Read the repo `AGENTS.md`.
2. Prepare the target bundle:
   - `python3 scripts/prepare_pr_bundle.py --out <json>`
   - or pass `--repo`, `--pr`, or `--url` when the target is known
3. Render the review summary:
   - `/home/bjorn/.codex/skill-support/bin/review-pack render --input <json> --format md`
4. Work file-by-file:
   - resolve correctness and safety findings first
   - prefer reviewer suggestion blocks when they are valid
   - keep changes minimal and scoped
5. Verify with repo-native checks before considering a finding done.
6. Use `$commit` only if you need help staging a mixed tree; otherwise keep this workflow self-contained.
7. Re-run `scripts/prepare_pr_bundle.py` after each pass to confirm what remains unresolved.
8. If the task becomes passive or continuous monitoring rather than active remediation, switch to `$babysit-pr`.

## Use When

- The user asks to fix GitHub PR review comments end-to-end.
- The current task is centered on unresolved review threads in a PR.

## Do Not Use When

- The input is a local review file, Codex review, Zen review, or manual notes.
- The task is passive PR monitoring.
- The task is only CI remediation with no review-thread context.

## Direct Tool Policy

- Use GitHub CLI or GitHub connector/API as the source of truth for PR metadata and review threads.
- Use Context7 for current API docs when the fix touches changing library APIs.
- Use Exa or `web.run` only when a review fix needs current external confirmation.
- Do not route through `context7-research` or `web-research-stack`.

## Outputs

- normalized PR review bundle
- short prioritized remediation summary
- verified fixes
- commit and push summary when a commit is created
- terminal status: `completed`, `blocked`, or `needs-user`

## Resources

- `scripts/prepare_pr_bundle.py`
