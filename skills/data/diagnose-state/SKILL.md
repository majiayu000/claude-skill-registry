---
name: diagnose-state
description: Read state.json and diagnose PR statuses, errors, stuck entries, and anomalies.
user-invocable: true
---

You are a diagnostics tool for the claude-code-reviewer service. Your job is to read and analyze the PR state file.

## Input

The user may provide an optional argument: a PR identifier like `owner/repo#N` or just `N` (PR number).

## Data Source

Read the state file at `data/state.json`. It follows the `StateFileV2` format defined in `src/types.ts`:
- Top-level: `{ "version": 2, "prs": { "owner/repo#N": PRState, ... } }`
- Each `PRState` has: identity (owner, repo, number), status, PR metadata, review history, skip tracking, error tracking, comment/review tracking, timestamps, debounce

If the file doesn't exist or is empty, report that and stop.

## Modes

### Summary Mode (no argument)

Present a dashboard of all tracked PRs:

1. **Status Distribution** — count PRs by status (`pending_review`, `reviewing`, `reviewed`, `changes_pushed`, `error`, `skipped`, `closed`, `merged`). Show as a table.

2. **Error Entries** — for each PR with `status: "error"`, show:
   - PR identifier (`owner/repo#N`)
   - `lastError.phase`, `lastError.message`, `lastError.sha` (7 chars), `lastError.occurredAt`
   - `consecutiveErrors` count
   - Whether it's stuck (consecutiveErrors >= `maxRetries` from `config.yaml`, default: 3)

3. **Skipped PRs** — for each PR with `status: "skipped"`, show:
   - PR identifier and title
   - `skipReason` (draft / wip_title / diff_too_large)
   - `skipDiffLines` if reason is diff_too_large

4. **Anomaly Detection** — flag these conditions:
   - Any PR in `reviewing` status (indicates a crash — `store.ts` resets these on startup, so this only appears in a raw file read before restart or during an active review)
   - Any PR with `consecutiveErrors >= maxRetries` (stuck at max retries — read `review.maxRetries` from `config.yaml`, default: 3)
   - Any `reviewed` PR with no `commentId` AND no `reviewId` (review posted but no tracking ID)
   - Any `reviewed` PR where `lastReviewedSha !== headSha` (stale review — new push since last review)
   - Any `reviewed` PR where `comment-verifier.ts` may have requeued it (reviewId/commentId is null but status is still `reviewed`)

5. **Summary Line** — total PRs, active (non-terminal), terminal (closed + merged)

### Single-PR Mode (with argument)

Look up the PR by key. If only a number is given, search all entries for a matching `number` field. If not found, report that.

Display all fields of the `PRState` grouped:

1. **Identity** — owner, repo, number, key
2. **Status** — current status, with interpretation
3. **PR Metadata** — title, isDraft, headSha (abbreviated to 7 chars), baseBranch
4. **Review History** — show `lastReviewedSha` (7 chars), `lastReviewedAt`, then format each `ReviewRecord` as a table row:
   - `sha` (7 chars) | `reviewedAt` | `verdict` | `posted` | findings count (by severity: issue/suggestion/nitpick/question/praise) | `commentId`/`reviewId`
   - Show total findings breakdown across all reviews
5. **Skip Tracking** — skipReason, skipDiffLines, skippedAtSha
6. **Error Tracking** — lastError (phase, message, sha, occurredAt), consecutiveErrors
7. **Comment/Review Tracking** — commentId, commentVerifiedAt, reviewId, reviewVerifiedAt
8. **Timestamps** — firstSeenAt, updatedAt, closedAt, lastPushAt, lastReviewedAt
9. **Anomalies** — same checks as summary mode, applied to this PR

## Output Format

Use markdown tables and clear section headers. Keep it scannable. Use ⚠ prefix for anomalies and errors.
