---
name: stack-push
description: 'Push all branches in a stack and create or update dependent PRs,
  targeting each PR at its parent branch.'
version: 1.0.0
alwaysApply: false
category: workflow-automation
tags:
- git
- stacked-diffs
- pr
- push
- github
tools:
- Bash
- TodoWrite
complexity: medium
model_hint: standard
estimated_tokens: 900
dependencies:
- sanctum:stack-create
- sanctum:pr-prep
- sanctum:git-workspace-review
---

# Stack Push

Push all branches in a stack and open (or update) one PR
per slice, with each PR targeting its parent branch as base.

## When to Use

Run `stack-push` after `stack-create` has initialized the
branch topology and at least one commit exists on each
slice branch.
Also run it after adding commits to any slice to update
open PRs.

## Prerequisites

- `stack-create` completed: branches exist with commits
- `gh` CLI authenticated (`gh auth status`)
- Each slice branch has at least one commit beyond its base

## Required Progress Tracking

Create `TodoWrite` items before starting:

1. `stack-push:branches-listed`
2. `stack-push:branches-pushed`
3. `stack-push:prs-opened`
4. `stack-push:stack-summary-posted`

## Step 1: List Stack Branches (`branches-listed`)

Identify all branches in the stack.
By convention they share a `stack/<feature-name>/` prefix:

```bash
STACK=stack/my-feature
BASE=master

git branch --list "${STACK}/*" | sed 's/^[* ]*//'
```

Verify each branch has commits beyond the base:

```bash
for branch in $(git branch --list "${STACK}/*" \
    | sed 's/^[* ]*//'); do
  count=$(git rev-list --count \
    "$(git merge-base ${BASE} ${branch})..${branch}")
  echo "${branch}: ${count} commit(s)"
done
```

Any branch showing `0 commits` must have work added before
pushing.

## Step 2: Push Branches (`branches-pushed`)

Push every slice branch to the remote in stack order
(base slice first):

```bash
for branch in $(git branch --list "${STACK}/*" \
    | sed 's/^[* ]*//' | sort); do
  git push --set-upstream origin "${branch}"
  echo "pushed: ${branch}"
done
```

### jj Accelerator (if available)

```bash
jj git push --all
```

## Step 3: Open or Update PRs (`prs-opened`)

Create one PR per slice, targeting its parent branch.
For the first slice the parent is `master`; for subsequent
slices the parent is the previous slice's branch.

```bash
PREV_BASE=master

for branch in $(git branch --list "${STACK}/*" \
    | sed 's/^[* ]*//' | sort); do

  # Check if a PR already exists for this branch
  existing=$(gh pr list \
    --head "${branch}" \
    --json number \
    --jq '.[0].number' 2>/dev/null)

  if [ -n "${existing}" ]; then
    echo "PR #${existing} already open for ${branch} -- skipping"
  else
    gh pr create \
      --base "${PREV_BASE}" \
      --head "${branch}" \
      --title "[$(echo ${branch} | sed 's|.*/||')] <title>" \
      --body "Part of stack \`${STACK}\`." \
      --draft
    echo "opened PR for ${branch} (base: ${PREV_BASE})"
  fi

  PREV_BASE="${branch}"
done
```

Fill in the actual PR titles and bodies before removing
the `--draft` flag.
Run `Skill(sanctum:pr-prep)` on each slice to generate
quality-gated descriptions.

## Step 4: Post Stack Summary (`stack-summary-posted`)

After all PRs are open, post a summary comment on the
first PR (the root of the stack) listing the full chain:

```bash
ROOT_PR=$(gh pr list \
  --head "${STACK}/$(git branch --list \
    "${STACK}/*" | sed 's/^[* ]*//' | sort | head -1 \
    | sed 's|.*/||')" \
  --json number --jq '.[0].number')

# Build the stack table
BODY="## Stack\n\n| # | Branch | PR |\n|---|--------|----|\n"
N=1
for branch in $(git branch --list "${STACK}/*" \
    | sed 's/^[* ]*//' | sort); do
  pr_num=$(gh pr list --head "${branch}" \
    --json number --jq '.[0].number')
  BODY="${BODY}| ${N} | \`${branch}\` | #${pr_num} |\n"
  N=$((N+1))
done

gh pr comment "${ROOT_PR}" --body "$(printf "${BODY}")"
```

## Notes

- Always push in stack order so GitHub sees the parent
  branch before the child PR is opened
- Use `--draft` by default; promote slices to ready
  individually as they pass review
- After any `git rebase --update-refs` run, re-push with
  `git push --force-with-lease` (never `--force`)
- When a base PR merges, run `Skill(sanctum:stack-rebase)`
  to cascade the rebase before updating the next PR's base
