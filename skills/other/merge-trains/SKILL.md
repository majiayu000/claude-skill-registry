---
name: merge-trains
description: Guide for working with merge-train branches -- creating PRs, choosing the right base branch, understanding labels, handling failures, and bypassing checks.
---

# Working with Merge Trains

## What Is a Merge Train?

A merge train is an automated batching system (inspired by [Rust rollups](https://forge.rust-lang.org/release/rollups.html)) that groups multiple PRs together for coordinated integration into the `next` branch. Instead of each PR going through the merge queue individually, teams push their PRs into a shared `merge-train/*` branch. Periodically, that branch is merged as a single unit into `next`.

## Active Merge-Train Branches

| Branch | Team / Domain | Slack Channel |
|---|---|---|
| `merge-train/avm` | AVM, barretenberg vm2 folder | `#team-bonobos` |
| `merge-train/barretenberg` | Barretenberg folder, but not vm2 folder | `#honk-team` |
| `merge-train/ci` | CI infrastructure / ci3 | `#help-ci` |
| `merge-train/docs` | Documentation | `#dev-rels` |
| `merge-train/fairies` | aztec-nr | `#team-fairies` |
| `merge-train/spartan` | Spartan / infra / yarn-project sequencer and prover orchestration | `#team-alpha` |

## How to Use a Merge Train

### Targeting a Merge Train with Your PR

1. Create your feature branch **off the appropriate merge-train branch** (not our default branch `next`).
2. Open your PR targeting that merge-train branch (e.g., base: `merge-train/barretenberg`).
3. When your PR is approved and merged, it gets squashed into the merge-train branch.
4. The merge-train PR (which targets `next`) automatically accumulates your commit.

### Key Rules for Contributors

- **Base branch matters**: Always branch from the branch specified in the CI_BASE_BRANCH environment variable. If it is not set, then ask the user their intent and offer to set CI_BASE_BRANCH in their shell's RC file. 
- **Your PR is squashed into the train**: Individual PRs targeting a merge-train branch are squash-merged as usual. You should not use the merge commit merge method, but the squash method.
- **The train itself is NOT squashed**: The merge-train PR (e.g., `merge-train/barretenberg` -> `next`) is merged with a **merge commit**, preserving the individual squashed commits. This is why the `ci-no-squash` label is automatically applied.
- **You generally don't need to worry about the train PR itself** -- it is fully automated (creation, body updates, approval, merge, and recreation). You only need to pay attention to it if an alert is sent to your team channel.

## CI Behavior for Merge Trains

- **Specialized CI modes**: PRs targeting `merge-train/docs` run docs-only CI. PRs targeting `merge-train/barretenberg` run barretenberg-only CI. This avoids running the full test suite for domain-specific changes.
- **Merge-queue mode**: When the merge-train PR enters GitHub's merge queue, it runs the full `merge-queue` CI mode (4 parallel grind runs on AMD64 + 1 ARM64). `merge-train/spartan` uses the heavier `merge-queue-heavy` mode (10 grind runs).
- **Full concurrency**: Merge-train PRs get unique CI concurrency groups (using `github.run_id`), so multiple CI runs can proceed in parallel without cancelling each other.
- **Test history tracking**: Test results are tracked for merge-train PRs, same as merge-queue runs.

## Handling Merge-Train Failures

### When CI Fails on the Merge-Train PR

Two options from the [merge-train-readme.md](https://github.com/AztecProtocol/aztec-packages/blob/next/.github/workflows/merge-train-readme.md):

**Option 1: Direct Fix** -- Push a fix directly to the merge-train branch. Use bypass merge to expedite (all users have this permission). You can use the ci-skip label to no-op CI if really necessary.

**Option 2: Fix in Next** -- Merge a revert or workaround into `next`. The fix will auto-propagate to the merge-train via the `merge-train-next-to-branches` workflow. Best when the root cause is in `next` or multiple trains are affected.

### When Auto-Merge Is Blocked

The auto-merge script will **not** enable auto-merge if the last merge-queue CI run for the PR concluded with `failure` or `cancelled`. Someone needs to either fix the issue and push, or force-merge.

### Merge Conflicts from Next

When merging `next` into a train branch causes conflicts, the `merge-next.sh` script:
- Aborts the merge
- Posts a comment on the latest `next` commit listing the conflicted files
- The team must manually resolve conflicts on their train branch

## Bypassing Checks / Force-Merging

If the user needs to bypass CI checks for their merge-train PR (e.g., a known flaky failure, an urgent merge, or CI infrastructure issues):

1. **Confirm intent**: Always confirm with the user that they want to skip CI, since this merges untested code into `next`.
2. **Add the `ci-skip` label**: Apply the `ci-skip` label to the merge-train PR. This causes CI to skip entirely. Use: `gh pr edit <PR_NUMBER> --add-label ci-skip`
3. **Force merge in the UI**: The user can then use GitHub's "Merge without waiting for requirements to be met" button (bypass merge) in the PR UI. All users have this permission. 

**Important**: Only do this when the user explicitly asks to bypass checks. Always confirm first since it skips all CI validation.

## Backport Trains

A related system exists for backport branches (`backport-to-*`). These use the same auto-merge mechanism but with different settings:
- Branch pattern: `backport-to-`
- Inactivity threshold: 8 hours (instead of 4)
- Merge strategy: merge commit
