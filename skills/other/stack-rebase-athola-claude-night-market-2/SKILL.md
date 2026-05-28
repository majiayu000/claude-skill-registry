---
name: stack-rebase
description: Cascades a rebase through an entire PR stack after a base PR merges or upstream changes. Use when a stack needs to incorporate new base branch commits.
alwaysApply: false
category: workflow-automation
tags:
- git
- stacked-diffs
- rebase
- pr
- cascade
tools: []
complexity: medium
model_hint: standard
estimated_tokens: 900
dependencies:
- sanctum:stack-create
- sanctum:stack-push
- sanctum:git-workspace-review
---

# Stack Rebase

Cascade a rebase through an entire PR stack after a base
PR merges or the upstream base branch changes.

## When to Use

Run `stack-rebase` in any of these situations:

- The first PR in the stack merged into `master`; the
  second PR now needs to target `master` directly
- `master` has moved forward and stack branches need to
  incorporate the new commits
- A mid-stack PR was revised and descendants need to
  pick up the change

## Prerequisites

- All slice branches exist locally (`git branch --list`)
- Remote is up to date (`git fetch origin`)
- Working tree is clean (`git status`)
- Git 2.38+ for `--update-refs`

## Required Progress Tracking

Create `TodoWrite` items before starting:

1. `stack-rebase:fetch-complete`
2. `stack-rebase:trigger-identified`
3. `stack-rebase:rebase-complete`
4. `stack-rebase:conflicts-resolved`
5. `stack-rebase:force-pushed`
6. `stack-rebase:prs-updated`

## Step 1: Fetch Remote State (`fetch-complete`)

```bash
git fetch origin
```

If the merged PR's branch still exists on remote, note
that GitHub retains the branch after merge.
The merged branch itself is no longer a valid stack base.

## Step 2: Identify the Trigger (`trigger-identified`)

Determine what changed:

**Case A — Base PR merged into master:**
The slice that was the old "root" is now in `master`.
All remaining slices need to rebase onto `master`.

```bash
# Confirm the merged branch is now in master
git branch -r --merged origin/master | grep "${MERGED_BRANCH}"
```

**Case B — Master moved forward:**
Slices are behind `master` but the stack topology is
unchanged.
Rebase the root slice onto `master`; `--update-refs`
carries all descendants.

**Case C — Mid-stack revision:**
A slice was amended.
All descendant slices need to rebase onto it.

## Step 3: Run the Cascading Rebase (`rebase-complete`)

### Case A and B: Rebase root slice onto master

```bash
STACK=stack/my-feature
BASE=master

# Check out the root slice
ROOT_SLICE=$(git branch --list "${STACK}/*" \
  | sed 's/^[* ]*//' | sort | head -1)

git checkout "${ROOT_SLICE}"

# Rebase with --update-refs rewrites all stack branches
git rebase --update-refs origin/${BASE}
```

`--update-refs` scans the reflog and updates every local
branch ref that points to a commit being rebased.
All slice branches in the stack are rewritten in one pass.

### Case C: Rebase from a mid-stack slice

```bash
# Check out the first slice BELOW the amended one
CHILD_SLICE=stack/my-feature/add-api  # example

git checkout "${CHILD_SLICE}"
git rebase --update-refs stack/my-feature/add-schema
```

### jj Accelerator (if available)

```bash
# jj rebases all descendants automatically on any change
# To rebase the whole stack onto master:
jj rebase -d master \
  -r "ancestors(${STACK}/add-ui) & !ancestors(master)"
```

## Step 4: Resolve Conflicts (`conflicts-resolved`)

If the rebase pauses with conflicts:

```bash
# See which file conflicts
git status

# After resolving each file:
git add <resolved-file>
git rebase --continue
```

Repeat until the rebase completes.
If a conflict is too complex, abort and investigate:

```bash
git rebase --abort
```

Then examine the diff between the conflicting commits
before retrying.

## Step 5: Force-Push Updated Branches (`force-pushed`)

After a successful rebase, push all slice branches.
Use `--force-with-lease` to guard against remote changes
made since the last fetch:

```bash
for branch in $(git branch --list "${STACK}/*" \
    | sed 's/^[* ]*//' | sort); do
  git push --force-with-lease origin "${branch}"
  echo "force-pushed: ${branch}"
done
```

Never use `--force` (drops the remote-change guard).

### jj Accelerator (if available)

```bash
jj git push --all --allow-new
```

## Step 6: Update PR Bases (`prs-updated`)

**Case A only**: After the root slice merged and you
rebased remaining slices onto `master`, the next PR in
the stack now targets the wrong base.
Update its base via the GitHub CLI:

```bash
NEXT_PR=456   # PR number of the new stack root

gh pr edit "${NEXT_PR}" --base master
```

For PRs further down the stack, their bases remain the
previous slice branch, which `--update-refs` already
rewrote; no base edit is needed for them.

Verify the full stack is consistent:

```bash
for branch in $(git branch --list "${STACK}/*" \
    | sed 's/^[* ]*//' | sort); do
  pr_num=$(gh pr list --head "${branch}" \
    --json number,baseRefName \
    --jq '.[0] | "#\(.number) base=\(.baseRefName)"')
  echo "${branch}: ${pr_num}"
done
```

## Conflict Prevention Tips

- Keep slices small: the smaller each PR, the less surface
  area for conflicts during rebase
- Rebase frequently: rebasing onto a freshly merged master
  once a day is cheaper than resolving a week of drift
- Avoid amending commits that are already under review;
  prefer a fixup commit and squash at merge time

## Notes

- `git rebase --update-refs` requires Git 2.38+; confirm
  with `git version` before running
- If `--update-refs` is unavailable, manually check out
  and rebase each slice branch in order from root to tip
- After force-pushing, GitHub automatically marks PR
  reviews as stale; remind reviewers to re-approve
- The `stack-push` skill documents how to re-post the
  stack summary comment after a rebase changes PR SHAs
