---
name: stack-mode
description: 'Shared stack detection and multi-PR iteration contract for commands
  that need to operate across a whole PR stack targeting a common base branch
  (e.g., /pr-review --stack, /fix-pr --stack).'
version: 1.0.0
alwaysApply: false
category: workflow-automation
tags:
- git
- stacked-diffs
- pr
- review
- fix-pr
- iteration
tools:
- Bash
- TodoWrite
complexity: medium
model_hint: standard
estimated_tokens: 1100
dependencies:
- sanctum:stack-create
- sanctum:stack-push
- sanctum:stack-rebase
- leyline:git-platform
---

# Stack Mode

Shared contract for commands that need to operate across a
whole stack of dependent PRs in one invocation.
Used by `/pr-review --stack` and `/fix-pr --stack`.

The goal is one simple thing: when a PR is part of a stack
targeting a common base branch, loop the command's normal
workflow across every PR in the stack in base-to-tip order
and emit one consolidated summary on the stack root.

## When to Use

Load this skill when a command accepts a `--stack` flag
(or auto-detects stack membership) and needs to iterate
its normal workflow across multiple PRs.

Do NOT load this skill for single-PR workflows. The
per-PR workflow stays unchanged; stack mode wraps it.

## Contract

A calling command MUST:

1. Accept a `--stack` boolean flag AND a `--base <branch>`
   override (default: `master`).
2. Call Step 1 below to resolve stack membership BEFORE
   running its main workflow.
3. Run its main workflow per PR in the resolved order.
4. Emit per-PR outputs unchanged (thread replies, issue
   links, etc.).
5. Emit ONE stack-level summary comment on the root PR
   using the format in Step 4.
6. Respect per-PR Gate rules (every PR still needs its own
   thread resolution + issue tracking).

A calling command MAY:

- Auto-detect stack membership and prompt the user rather
  than requiring `--stack` explicitly.
- Short-circuit iteration when a per-PR failure leaves
  downstream PRs with stale context.

## Required Progress Tracking

The caller creates `TodoWrite` items:

1. `stack-mode:membership-resolved`
2. `stack-mode:iteration-complete`
3. `stack-mode:root-summary-posted`

## Step 1: Resolve Stack Membership (`membership-resolved`)

Given a starting PR number `$PR_NUM` and optional base
`$BASE` (default: `master`), try three strategies in
order and stop at the first that yields a stack of size
>= 2.

### Strategy A: Branch-name convention (cheapest)

```bash
START_HEAD=$(gh pr view "$PR_NUM" \
  --json headRefName -q .headRefName)

# stack/<feature-name>/<slice-name>
if [[ "$START_HEAD" =~ ^stack/([^/]+)/.+$ ]]; then
  FEATURE="${BASH_REMATCH[1]}"
  PREFIX="stack/${FEATURE}/"

  # All local branches with the same prefix
  STACK_BRANCHES=$(git branch --list "${PREFIX}*" \
    | sed 's/^[* ]*//' | sort)

  # Map branches -> PR numbers (skip branches with no PR)
  STACK_PRS=()
  for branch in $STACK_BRANCHES; do
    pr=$(gh pr list --head "$branch" \
      --json number --jq '.[0].number')
    [ -n "$pr" ] && STACK_PRS+=("$pr")
  done

  echo "strategy=A prs=${STACK_PRS[*]}"
fi
```

### Strategy B: Stack summary comment (most reliable)

`stack-push` posts a `## Stack` markdown table on the
root PR with columns `# | Branch | PR`. Parse it:

```bash
# Find the root PR of the stack containing $PR_NUM
# The current PR may be the root, or may link to it via
# a "Part of stack `stack/<feature>`" phrase in its body
BODY=$(gh pr view "$PR_NUM" --json body -q .body)

# Look for a "## Stack" table in THIS PR's comments
TABLE=$(gh pr view "$PR_NUM" --json comments \
  --jq '.comments[] | select(.body | contains("## Stack"))
        | .body' | head -1)

# If not on this PR, look for the root PR reference
if [ -z "$TABLE" ]; then
  ROOT_REF=$(echo "$BODY" \
    | grep -oE 'stack/[^ `]+' | head -1)
  # ... resolve ROOT_REF -> root PR number and re-fetch
fi

# Parse the table: extract all `#<num>` from the PR column
STACK_PRS=($(echo "$TABLE" \
  | grep -oE '#[0-9]+' | tr -d '#' | sort -un))

echo "strategy=B prs=${STACK_PRS[*]}"
```

### Strategy C: Base-chain walk (fallback)

Walk both directions from `$PR_NUM`:

- Up: repeatedly resolve `baseRefName` until it equals
  `$BASE`. Each visited head is a stack member.
- Down: find open PRs whose `baseRefName` equals one of
  the visited heads. Recurse.

```bash
# Ascend from $PR_NUM to the root
CUR=$PR_NUM
CHAIN=($CUR)
while true; do
  BASE_REF=$(gh pr view "$CUR" \
    --json baseRefName -q .baseRefName)
  [ "$BASE_REF" = "$BASE" ] && break

  PARENT=$(gh pr list --head "$BASE_REF" \
    --state open --json number --jq '.[0].number')
  [ -z "$PARENT" ] && break

  CHAIN=("$PARENT" "${CHAIN[@]}")
  CUR=$PARENT
done

# Descend from the root collecting children
ROOT=${CHAIN[0]}
FRONTIER=("$ROOT")
while [ ${#FRONTIER[@]} -gt 0 ]; do
  PARENT=${FRONTIER[0]}
  FRONTIER=("${FRONTIER[@]:1}")

  PARENT_HEAD=$(gh pr view "$PARENT" \
    --json headRefName -q .headRefName)

  CHILDREN=($(gh pr list --base "$PARENT_HEAD" \
    --state open --json number --jq '.[].number'))

  for c in "${CHILDREN[@]}"; do
    CHAIN+=("$c")
    FRONTIER+=("$c")
  done
done

STACK_PRS=("${CHAIN[@]}")
echo "strategy=C prs=${STACK_PRS[*]}"
```

### Ordering

Regardless of strategy, order the final list **base-to-tip**
(root PR first, leaf PR last). The root is the PR whose
`baseRefName` equals `$BASE`.

```bash
ROOT_PR=""
for p in "${STACK_PRS[@]}"; do
  base=$(gh pr view "$p" --json baseRefName -q .baseRefName)
  if [ "$base" = "$BASE" ]; then
    ROOT_PR=$p
    break
  fi
done
```

If the stack size is 1, the command MUST fall back to
single-PR mode and emit a warning: `stack-mode: only one
PR found; --stack has no effect, proceeding as single-PR`.

### GitLab / Bitbucket

See `Skill(leyline:git-platform)` for `glab` / Bitbucket
equivalents of the `gh` calls above. The three strategies
translate directly: GitLab MR dependencies replace
base-chain walks, and the `glab mr view --output json`
shape matches `gh pr view`.

## Step 2: Confirm With User (if not explicit)

When the caller did NOT pass `--stack` but Step 1 resolved
a stack of size >= 2, print the stack and ask:

```
Detected stack of N PRs rooted at #<root>:
  1. #<root>   <title>
  2. #<p2>     <title>
  ...

Run the workflow on the full stack? [y/N]
```

Default to "N" (single-PR mode). With `--stack` explicit,
skip this prompt.

## Step 3: Iterate (`iteration-complete`)

Run the caller's main workflow once per PR in base-to-tip
order:

```bash
FAILED_PRS=()
for p in "${STACK_PRS[@]}"; do
  echo "=== stack-mode: PR #$p ($(($idx+1))/${#STACK_PRS[@]}) ==="

  # Caller hook: run the single-PR workflow on $p
  # This includes Gate 1 (thread resolution) and
  # Gate 2 (issue tracking) per the caller's contract.
  if ! run_single_pr_workflow "$p"; then
    FAILED_PRS+=("$p")
    # Stop iteration: downstream PRs may now be stale
    break
  fi
done
```

If any PR fails, the command MUST stop and report
`stack-mode: halted at #<pr>; downstream PRs untouched`.
Downstream PRs are intentionally left alone because
their context may have shifted.

## Step 4: Post Stack Summary on Root (`root-summary-posted`)

After successful iteration, post ONE consolidated summary
comment on the root PR. This does NOT replace per-PR
summaries: it links them together.

```markdown
## Stack <Command Name> Summary

**Stack**: N PRs rooted at #<root>, base `<base-branch>`
**Command**: <command> (e.g., /fix-pr, /pr-review)
**Run**: <timestamp>

| # | PR | Branch | Status | Per-PR Summary |
|---|----|--------|--------|----------------|
| 1 | #<root> | `stack/<feat>/<root-slice>` | <done/skipped/failed> | [link to comment] |
| 2 | #<p2>   | `stack/<feat>/<slice-2>`    | <done/skipped/failed> | [link to comment] |
| ... | ... | ... | ... | ... |

### Cross-PR Notes

- <Any observations that spanned multiple PRs>
- <Issues created that reference multiple stack PRs>
- <Base-PR-merged cascade reminders, if any>

### Next Steps

- If root PR merges, run `Skill(sanctum:stack-rebase)` to
  cascade the base update through descendants.
- Reviewers: rebase-triggered stale-review flags on
  descendants are expected after any force-push.
```

Post via `gh pr comment "$ROOT_PR" --body-file <file>`.

## Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Stack of size 1 | Step 1 returns one PR | Emit warning, fall back to single-PR mode |
| Base chain loops | Visited set on ascent | Halt, report `stack-mode: cycle detected` |
| Mid-stack PR failed its Gates | Caller raises | Halt iteration, leave downstream untouched |
| Strategy B table malformed | Parse fails | Fall through to Strategy C |
| Auth scope insufficient | `gh` returns 403 | Halt with clear error; caller surfaces to user |

## Notes

- Stack mode is ADDITIVE: single-PR behavior is unchanged.
  Only the iteration and root summary are new.
- Per-PR Gate 1 (thread resolution) and Gate 2 (issue
  tracking) remain unchanged: each PR still passes its
  own gates independently.
- Never merge Gate 1 across the stack. A resolved thread
  on one PR is not a resolved thread on another.
- The root summary is idempotent: re-running stack mode
  should update (not duplicate) the summary comment.
  Match on `## Stack <Command Name> Summary` as the key.
- `stack-mode` is a read/orchestration skill; it does NOT
  push, rebase, or edit branches. Those concerns live in
  `stack-create`, `stack-push`, and `stack-rebase`.
