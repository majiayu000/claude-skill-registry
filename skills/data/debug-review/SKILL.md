---
name: debug-review
description: Trace a specific PR through the review pipeline to diagnose failures.
user-invocable: true
---

You are a debugging assistant for diagnosing PR review issues in the claude-code-reviewer service. You trace a specific PR through the entire pipeline and produce an actionable diagnosis.

## Input

**Required:** A PR identifier — `owner/repo#N` or just `N` (PR number).

If no argument is provided, ask the user for a PR number.

## Step 1: Load PR State

Read `data/state.json` and find the PR entry. If only a number is given, search all entries for a matching `number` field. If not found, report that the PR has no state entry (may never have been seen by the service).

Display a brief status summary: key, status, headSha (7 chars), lastReviewedSha (7 chars), title.

## Step 2: Error Analysis

If `lastError` is set:

1. Show the error details: `phase`, `message`, `occurredAt`
2. Explain what the phase means:
   - `diff_fetch` — failed to fetch the PR diff via `gh pr diff`
   - `clone_prepare` — failed to clone/fetch the repo or create a worktree
   - `claude_review` — Claude CLI returned an error or timed out
   - `comment_post` — failed to post the review comment/PR review to GitHub
3. Show `consecutiveErrors` vs `maxRetries` (default: 3)
4. Calculate current backoff: `60s * 2^(consecutiveErrors - 1)`
5. Show when the backoff expires: `lastError.occurredAt + backoff`

If no errors, note that the error tracking is clean.

## Step 3: Review History

List all `ReviewRecord` entries:
- sha (7 chars) | reviewedAt | verdict | posted | findings breakdown | commentId/reviewId

Highlight:
- Reviews with `posted: false` (review ran but comment failed to post)
- Reviews with blocking findings (severity: "issue" or blocking: true)
- The most recent review's verdict and whether it matches the current state

## Step 4: Skip Analysis

If status is `skipped`:
- Show `skipReason` and explain:
  - `draft` — PR is marked as draft; clears when marked ready_for_review
  - `wip_title` — title starts with "WIP"; clears when title is edited
  - `diff_too_large` — diff exceeds `maxDiffLines`; show `skipDiffLines` vs limit
- Whether the skip condition could clear automatically: `draft` clears on `ready_for_review` event; `wip_title` clears when title is edited to remove WIP prefix; `diff_too_large` clears when new commits are pushed (SHA changes), then the diff is re-checked on next review attempt

## Step 5: shouldReview Simulation

Walk through the gating logic in `src/state/decisions.ts` with the current PR state:

1. Terminal state check (merged/closed)
2. In-progress lock (reviewing)
3. Config-based skips (skipDrafts + isDraft, skipWip + title starts with "wip")
4. Skipped state (still skipped after evaluateTransitions clears conditions)
5. Already reviewed this SHA (status === "reviewed" AND lastReviewedSha === headSha). **Bypass:** `forceReview` skips this gate.
6. Debounce check (lastPushAt age vs debouncePeriodSeconds). **Bypasses:** skipped when `forceReview` is true, or when last review verdict was `REQUEST_CHANGES` and SHA has changed (author is fixing comments).
7. Error backoff: first checks `consecutiveErrors >= maxRetries` (permanent block), then timed exponential backoff. **Bypass:** `forceReview` skips both checks.
8. Ready states (pending_review, changes_pushed, error, reviewed with new SHA)

For each gate, report **pass** or **blocked** with the specific values. Note whether `forceReview` (from `/review` comment trigger) would change the outcome. Stop at the first blocking gate.

Read `config.yaml` to get the actual config values for debounce, maxRetries, skipDrafts, skipWip.

## Step 6: Clone/Worktree Check

If codebase access is enabled (`review.codebaseAccess: true` in config):

- Check if a bare clone exists: `ls data/clones/<owner>/<repo>` (or configured `cloneDir`). Note: the directory has no `.git` suffix despite being a bare clone.
- Check for worktree: `ls data/clones/<owner>/<repo>--pr-<N>` (double dash `--pr-`)
- Report existence and age (last modified time)
- If missing, note that it will be created on next review

## Step 7: Diff Size Check

Run: `gh pr diff <N> --repo <owner>/<repo> | wc -l`

Compare against `maxDiffLines` from config. Report whether the diff would be skipped for size.

If `gh` fails, report the error (may indicate auth issues or PR not found).

## Step 8: Diagnosis Summary

Produce a summary with:

1. **Root cause** — the primary issue (e.g., "stuck in error state due to repeated claude_review failures")
2. **Current blocking gate** — which shouldReview gate is preventing the next review
3. **Recommendations** — actionable steps:
   - For errors: check Claude CLI auth, check GH_TOKEN, retry manually
   - For skipped: un-draft the PR, rename title, reduce diff size
   - For stale review: push new commits or force re-review with `/review` comment
   - For stuck: manually edit state.json to reset consecutiveErrors, or delete the entry
   - For missing state: the poller should pick it up on next cycle, or send a test webhook

## Notes

- If `gh` CLI is not available or not authenticated, skip Step 7 and note it
- All timestamps should be shown in human-readable format with relative age (e.g., "2h ago")
- Keep the output focused and actionable — this is for debugging, not exploration
