---
name: merge-train-infra
description: Reference for merge-train automation internals -- workflows, scripts, CI integration, and configuration. Use when modifying or debugging merge-train infrastructure.
---

# Merge-Train Infrastructure

This skill covers the automation internals of the merge-train system. For contributor-facing guidance (creating PRs, labels, handling failures), see the `merge-trains` skill.

## Automation Lifecycle

The merge-train system is fully automated via GitHub Actions in `.github/workflows/merge-train-*.yml`:

1. **PR Creation** (`merge-train-create-pr.yml`): Triggered on push to `merge-train/*` branches. Creates a PR targeting `next` with the `ci-no-squash` label (and `ci-full-no-test-cache` for spartan). Skips merge commits and commits already in `next`.

2. **Body Updates** (`merge-train-update-pr-body.yml`): Triggered on push to `merge-train/**`. Updates the PR body with meaningful commits (those containing PR references like `(#1234)`). The body uses `BEGIN_COMMIT_OVERRIDE` / `END_COMMIT_OVERRIDE` markers for release-please.

3. **Next Integration** (`merge-train-next-to-branches.yml`): Triggered on push to `next`. Merges `next` into each active merge-train branch via `scripts/merge-train/merge-next.sh`. Uses `continue-on-error: true` so a conflict in one branch does not block others. Skips branches whose PR already has auto-merge enabled.

4. **Auto-Merge** (`merge-train-auto-merge.yml`): Runs hourly via cron (`0 * * * *`). Calls `scripts/merge-train/auto-merge.sh` for both merge-train (4-hour inactivity) and backport-train (8-hour inactivity) branches. Uses separate GitHub tokens: `AZTEC_BOT_GITHUB_TOKEN` for API calls and `MERGE_TRAIN_GITHUB_TOKEN` for approvals. Will not auto-merge if the last merge-queue CI run failed or was cancelled.

5. **Recreation & Wakeup** (`merge-train-recreate.yml`): Triggered when a PR is closed (merged). If the merged PR's head branch starts with `merge-train/`, recreates the branch from the base branch (usually `next`). Then runs `scripts/merge-train/wakeup-prs.sh` to add the `ci-wakeup-pr-after-merge` label to all open PRs targeting the branch that have passed CI and have automerge enabled. This triggers a CI re-run (typically a no-op via tree-hash cache) so those PRs can proceed through the merge queue. The label is immediately removed by a step in `ci3.yml` so it can be re-applied on subsequent merges.

6. **Failure Notification** (`merge-queue-dequeue-notify.yml`): Triggered when a PR is dequeued from the merge queue. If the PR's head branch starts with `merge-train/` and the PR was NOT merged, sends a Slack notification via `ci3/merge_train_failure_slack_notify`.

## CI Integration Details

### CI Mode Selection (`.github/ci3_labels_to_env.sh`)

Merge-train branches influence CI mode:
- `merge_group` events or `ci-merge-queue` label → `merge-queue` mode
- If the merge-group event is for `merge-train/spartan` → upgraded to `merge-queue-heavy` mode (10 parallel grind runs instead of 4)
- Target branch `merge-train/docs` → `ci-docs` mode
- Target branch `merge-train/barretenberg` → `ci-barretenberg` mode

### CI Concurrency (`.github/workflows/ci3.yml`)

```yaml
group: ci3-${{ (startsWith(github.event.pull_request.head.ref, 'merge-train/') && github.run_id) || ... }}
```

Merge-train PRs get **full concurrency** (each run has its own unique group via `github.run_id`), while non-merge-train PRs share a group by branch name with cancel-in-progress.

### Instance Postfix (`.github/ci3.sh`)

```bash
if [[ "${PR_HEAD_REF:-}" == merge-train/* ]]; then
    export INSTANCE_POSTFIX=${PR_COMMITS:-}
fi
```

Merge-train PRs get a unique instance postfix (commit count) to allow parallel EC2 instances.

### CI Modes in bootstrap.sh

- `ci-docs`: Only builds and tests documentation
- `ci-barretenberg`: Only builds and tests barretenberg (AVM disabled)
- `ci-barretenberg-full`: Full barretenberg CI including acir_tests
- `merge-queue`: 4x AMD64 full + 1x ARM64 fast in parallel
- `merge-queue-heavy`: 10x AMD64 full + 1x ARM64 fast in parallel (used for `merge-train/spartan`)

### Test History Tracking (`ci3/run_test_cmd`)

```bash
if [[ "$is_merge_queue" -eq 1 || ("${TARGET_BRANCH:-}" =~ ^v[0-9]) || ("${TARGET_BRANCH:-}" == merge-train/*) ]]; then
    track_test_history=1
fi
```

### Failure Notification (`ci3/bootstrap_ec2`)

When a CI run fails on an EC2 instance, it calls `merge_train_failure_slack_notify` to send failure notifications to the appropriate Slack channel based on the branch name.

## Creating a New Merge Train

1. Create a branch from `next` with naming pattern `merge-train/{team}`
2. Add the branch to the matrix in `.github/workflows/merge-train-next-to-branches.yml`
3. Add the branch-to-Slack-channel mapping in `ci3/merge_train_failure_slack_notify`
4. Optionally add CI mode overrides in `.github/ci3_labels_to_env.sh` and `bootstrap.sh`
5. Push code to the branch -- automation handles PR creation from there

## Key Files Reference

### Workflows

| File | Purpose |
|---|---|
| `.github/workflows/merge-train-readme.md` | User-facing documentation |
| `.github/workflows/merge-train-create-pr.yml` | Auto-creates PRs for train branches |
| `.github/workflows/merge-train-auto-merge.yml` | Hourly cron to auto-merge inactive trains |
| `.github/workflows/merge-train-next-to-branches.yml` | Syncs `next` into all train branches; defines active branches |
| `.github/workflows/merge-train-recreate.yml` | Recreates branch after merge |
| `.github/workflows/merge-train-update-pr-body.yml` | Updates PR body with commit list |
| `.github/workflows/merge-queue-dequeue-notify.yml` | Slack notification on merge-queue dequeue |
| `.github/workflows/squashed-pr-check.yml` | Squash enforcement (skipped for `ci-no-squash`) |

### Scripts

| File | Purpose |
|---|---|
| `scripts/merge-train/auto-merge.sh` | Auto-merge logic -- checks inactivity, last CI status, approves and merges |
| `scripts/merge-train/merge-next.sh` | Merges `next` into a train branch, handles conflicts, cancels stale CI runs |
| `scripts/merge-train/update-pr-body.sh` | Updates PR body with meaningful commits |
| `scripts/merge-train/squash-pr.sh` | Squashes PR commits (used by `ci-squash-and-merge` label) |
| `scripts/merge-train/wakeup-prs.sh` | Adds `ci-wakeup-pr-after-merge` label to qualifying PRs after branch recreation |

### CI Configuration

| File | Purpose |
|---|---|
| `.github/ci3_labels_to_env.sh` | CI mode selection based on labels and target branches |
| `.github/ci3.sh` | Instance postfix for merge-train parallelism |
| `ci3/merge_train_failure_slack_notify` | Slack failure notification with branch-to-channel mapping |
| `ci3/run_test_cmd` | Test history tracking for merge-train branches |
| `ci3/bootstrap_ec2` | EC2 failure notification trigger |
| `bootstrap.sh` | CI mode definitions (`ci-docs`, `ci-barretenberg`, etc.) |

### Other Scripts

| File | Purpose |
|---|---|
| `scripts/auto_close_issues.py` | Auto-closes issues referenced in merged merge-train PRs (GitHub's native auto-close doesn't work for intermediate branches) |
| `scripts/find_orphaned_issues_in_prs.py` | Finds PRs in merge-train commits that reference still-open issues |
| `scripts/dedupe_release_notes.py` | Deduplicates release notes from merge-train merges |
| `scripts/commits` | Pretty git log that groups merge-train children by subsystem |
| `scripts/filter_history` | Filters git history, identifying merge-train merge commits as "containers" |
