---
name: gwt-pr-check
description: "Check GitHub PR status with the gh CLI, including unmerged PR detection and post-merge new-commit detection for the current branch."
---

# GH PR Check

## Overview

Check PR status for the current branch with `gh` and report a recommended next action.

This skill is **check-only**:

- Do not create/switch branches
- Do not push
- Do not create/edit PRs

## Decision rules (must follow)

1. Resolve repository, `head` branch, and `base` branch.
   - `head`: current branch (`git rev-parse --abbrev-ref HEAD`)
   - `base`: default `develop` unless user specifies
2. Optionally collect local working tree state:
   - `git status --porcelain`
   - Report as context only; do not mutate files.
3. Fetch latest remote refs before comparing:
   - `git fetch origin`
4. List PRs for head branch:
   - `gh pr list --head <head> --state all --json`
   - `number,state,mergedAt,updatedAt,url,title,mergeCommit,baseRefName,headRefName`
5. Classify:
   - No PR found -> `NO_PR` + recommended action `CREATE_PR`
   - Any PR where `mergedAt == null`
     -> `UNMERGED_PR_EXISTS` + recommended action `PUSH_ONLY`
   - All PRs merged -> perform post-merge commit check
6. Post-merge commit check (critical when all PRs are merged):
   - Select latest merged PR by `mergedAt`
   - Get merge commit SHA from `mergeCommit.oid`
   - Verify merge commit ancestry before counting:
     - `git merge-base --is-ancestor <merge_commit> HEAD`
   - If merge commit is ancestor of `HEAD`, count commits after merge:
     - `git rev-list --count <merge_commit>..HEAD`
   - If count > 0 -> `ALL_MERGED_WITH_NEW_COMMITS` + `CREATE_PR`
   - If count == 0 -> `ALL_MERGED_NO_NEW_COMMITS` + `NO_ACTION`
7. Fallback when merge commit SHA is missing or not an ancestor of `HEAD`:
   - First compare against branch upstream (preferred):
     - `git rev-list --count origin/<head>..HEAD`
   - Count > 0 -> `ALL_MERGED_WITH_NEW_COMMITS` + `CREATE_PR` (fallback)
   - Count == 0 -> `ALL_MERGED_NO_NEW_COMMITS` + `NO_ACTION` (fallback)
   - If upstream comparison fails, compare against base:
     - `git rev-list --count origin/<base>..HEAD`
   - If base comparison fails -> `CHECK_FAILED` + `MANUAL_CHECK`

## Output contract

Return a human-readable summary by default.

Do not return raw JSON as the default output.
If JSON is explicitly requested by the user, append it after the human summary.

Recommended status values:

- `NO_PR`
- `UNMERGED_PR_EXISTS`
- `ALL_MERGED_WITH_NEW_COMMITS`
- `ALL_MERGED_NO_NEW_COMMITS`
- `CHECK_FAILED`

Recommended action values:

- `CREATE_PR`
- `PUSH_ONLY`
- `NO_ACTION`
- `MANUAL_CHECK`

### Language rule

- Follow the user's input language for all headings and messages.
- If the language is ambiguous, use English.

### Default output template

Output 1-3 lines using a signal prefix + action keyword on line 1.

| Prefix | Action | Meaning |
| --- | --- | --- |
| `>>` | `CREATE PR` | Create a new PR |
| `>` | `PUSH ONLY` | Push to existing PR |
| `--` | `NO ACTION` | Nothing to do |
| `!!` | `MANUAL CHECK` | Manual check required |

Per-status format:

- **NO_PR**:
  `>> CREATE PR — No PR exists for <head> -> <base>.`
- **UNMERGED_PR_EXISTS** (2 lines):

  ```text
  > PUSH ONLY — Unmerged PR open for `<head>`.
     PR: #<number> <url>
  ```

- **ALL_MERGED_WITH_NEW_COMMITS** (2 lines):

  ```text
  >> CREATE PR — <N> new commit(s) after last merge (#<pr_number>).
     head: <head> -> base: <base>
  ```

- **ALL_MERGED_NO_NEW_COMMITS**:
  `-- NO ACTION — All PRs merged, no new commits on <head>.`
- **CHECK_FAILED** (2 lines):

  ```text
  !! MANUAL CHECK — Could not determine PR status.
     Reason: <reason>
     head: <head> -> base: <base>
  ```

Append the following line **only** when the worktree is dirty:

```text
   (!) Worktree has uncommitted changes.
```

### Status-to-action mapping (must use)

| Status | Prefix | Action | Template |
| --- | --- | --- | --- |
| `NO_PR` | `>>` | `CREATE PR` | No PR exists |
| `UNMERGED_PR_EXISTS` | `>` | `PUSH ONLY` | Unmerged PR open |
| `ALL_MERGED_WITH_NEW_COMMITS` | `>>` | `CREATE PR` | N new commit(s) |
| `ALL_MERGED_NO_NEW_COMMITS` | `--` | `NO ACTION` | All PRs merged |
| `CHECK_FAILED` | `!!` | `MANUAL CHECK` | Could not determine |

### Example outputs

**NO_PR:**

```text
>> CREATE PR — No PR exists for `feature/my-branch` -> `develop`.
```

**UNMERGED_PR_EXISTS:**

```text
> PUSH ONLY — Unmerged PR open for `feature/my-branch`.
   PR: #456 https://github.com/org/repo/pull/456
```

**ALL_MERGED_WITH_NEW_COMMITS:**

```text
>> CREATE PR — 3 new commit(s) after last merge (#123).
   head: feature/my-branch -> base: develop
```

**ALL_MERGED_NO_NEW_COMMITS:**

```text
-- NO ACTION — All PRs merged, no new commits on `feature/my-branch`.
```

**CHECK_FAILED:**

```text
!! MANUAL CHECK — Could not determine PR status.
   Reason: Could not resolve merge commit and fallback comparison failed
   head: feature/my-branch -> base: develop
```

**With dirty worktree (appended to any status):**

```text
>> CREATE PR — 3 new commit(s) after last merge (#123).
   head: feature/my-branch -> base: develop
   (!) Worktree has uncommitted changes.
```

## Workflow (recommended)

1. Verify repo context:
   - `git rev-parse --show-toplevel`
   - `git rev-parse --abbrev-ref HEAD`
2. Confirm auth:
   - `gh auth status`
3. Collect context:
   - `git status --porcelain`
   - `git fetch origin`
4. List PRs for head branch and classify using rules above.
5. When all PRs are merged, validate merge commit ancestry before counting commits.
6. If merge commit is not usable, fallback to `origin/<head>..HEAD` first.
7. Print human-readable result using the default template.
8. Append JSON only if the user explicitly asks for machine-readable output.

## Quick start

```bash
# Human-readable output
python3 ".claude/skills/gwt-pr-check/scripts/check_pr_status.py" --repo "."

# Explicit base branch
python3 ".claude/skills/gwt-pr-check/scripts/check_pr_status.py" --repo "." --base develop

# Append machine-readable JSON after the summary
python3 ".claude/skills/gwt-pr-check/scripts/check_pr_status.py" --repo "." --json
```

## Command snippet (bash)

```bash
head="${HEAD_BRANCH:-$(git rev-parse --abbrev-ref HEAD)}"
base="${BASE_BRANCH:-develop}"

dirty=0
if [ -n "$(git status --porcelain)" ]; then
  dirty=1
fi

git fetch origin

pr_json="$(gh pr list --head "$head" --state all --json number,state,mergedAt,updatedAt,url,title,mergeCommit)"
pr_count="$(echo "$pr_json" | jq 'length')"
unmerged_count="$(echo "$pr_json" | jq 'map(select(.mergedAt == null)) | length')"

if [ "$pr_count" -eq 0 ]; then
  status="NO_PR"
  action="CREATE_PR"
  reason="No PR found for head branch"
elif [ "$unmerged_count" -gt 0 ]; then
  status="UNMERGED_PR_EXISTS"
  action="PUSH_ONLY"
  reason="At least one PR for the head branch is not merged"
else
  merge_commit="$(echo "$pr_json" | jq -r 'sort_by(.mergedAt) | last | .mergeCommit.oid')"
  merge_commit_ancestor=0
  if [ -n "$merge_commit" ] && [ "$merge_commit" != "null" ] && \
     git merge-base --is-ancestor "$merge_commit" HEAD 2>/dev/null; then
    merge_commit_ancestor=1
    new_commits="$(
      git rev-list --count "$merge_commit"..HEAD 2>/dev/null || echo ""
    )"
  else
    new_commits=""
  fi

  if [ -n "$new_commits" ]; then
    if [ "$new_commits" -gt 0 ]; then
      status="ALL_MERGED_WITH_NEW_COMMITS"
      action="CREATE_PR"
      reason="$new_commits commits found after last merge"
    else
      status="ALL_MERGED_NO_NEW_COMMITS"
      action="NO_ACTION"
      reason="No commits found after last merge"
    fi
  else
    upstream_commits="$(
      git rev-list --count "origin/$head"..HEAD 2>/dev/null || echo ""
    )"
    if [ -n "$upstream_commits" ]; then
      if [ "$upstream_commits" -gt 0 ]; then
        status="ALL_MERGED_WITH_NEW_COMMITS"
        action="CREATE_PR"
        reason="Fallback check found commits ahead of origin/$head"
      else
        status="ALL_MERGED_NO_NEW_COMMITS"
        action="NO_ACTION"
        reason="Fallback check found no commits ahead of origin/$head"
      fi
    else
    fallback_commits="$(
      git rev-list --count "origin/$base"..HEAD 2>/dev/null || echo ""
    )"
    if [ -n "$fallback_commits" ]; then
      if [ "$fallback_commits" -gt 0 ]; then
        status="ALL_MERGED_WITH_NEW_COMMITS"
        action="CREATE_PR"
        reason="Fallback check found commits ahead of origin/$base"
      else
        status="ALL_MERGED_NO_NEW_COMMITS"
        action="NO_ACTION"
        reason="Fallback check found no commits ahead of origin/$base"
      fi
    else
      status="CHECK_FAILED"
      action="MANUAL_CHECK"
      reason="Could not resolve merge commit and fallback comparison failed"
    fi
    fi
  fi
fi

latest_merged_pr="$(
  echo "$pr_json" \
    | jq -r 'sort_by(.mergedAt) | last | .number // empty'
)"
unmerged_pr="$(
  echo "$pr_json" \
    | jq -r 'map(select(.mergedAt == null)) | first | .number // empty'
)"
unmerged_pr_url="$(
  echo "$pr_json" \
    | jq -r 'map(select(.mergedAt == null)) | first | .url // empty'
)"

case "$status" in
  NO_PR)
    echo ">> CREATE PR — No PR exists for \`$head\` -> \`$base\`."
    ;;
  UNMERGED_PR_EXISTS)
    echo "> PUSH ONLY — Unmerged PR open for \`$head\`."
    echo "   PR: #$unmerged_pr $unmerged_pr_url"
    ;;
  ALL_MERGED_WITH_NEW_COMMITS)
    n="${new_commits:-$upstream_commits}"
    echo ">> CREATE PR — $n new commit(s) after last merge (#$latest_merged_pr)."
    echo "   head: $head -> base: $base"
    ;;
  ALL_MERGED_NO_NEW_COMMITS)
    echo "-- NO ACTION — All PRs merged, no new commits on \`$head\`."
    ;;
  *)
    echo "!! MANUAL CHECK — Could not determine PR status."
    echo "   Reason: $reason"
    echo "   head: $head -> base: $base"
    ;;
esac

if [ "$dirty" -eq 1 ]; then
  echo "   (!) Worktree has uncommitted changes."
fi
```

## Related skill

- `gwt-pr`: creates/updates PRs
- `gwt-fix-pr`: diagnoses and fixes failing PRs
