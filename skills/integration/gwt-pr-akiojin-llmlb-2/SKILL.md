---
name: gwt-pr
description: "Create or update GitHub Pull Requests with the gh CLI, including deciding whether to create a new PR or only push based on existing PR merge status. Use when the user asks to open/create/edit a PR, generate a PR body/template, or says 'open a PR/create a PR/gh pr'. Defaults: base=develop, head=current branch (same-branch only; never create/switch branches)."
---

# GH PR

## Overview

Create or update GitHub Pull Requests with the gh CLI using a detailed body template and strict same-branch rules.

## Decision rules (must follow)

1. **Do not create or switch branches.** Always use the current branch as the PR head.
2. **Check local working tree state before push/PR operations.**
   - `git status --porcelain`
   - If output is non-empty (tracked or untracked changes), pause and ask the user what to do.
   - Present 3 options: continue as-is, abort, or manual cleanup then rerun.
   - **Do not** run `git stash`, `git commit`, or `git clean` automatically unless explicitly requested.
3. **Check for an existing PR for the current head branch.**
   - `gh pr list --head <head> --state all --json number,state,mergedAt,updatedAt,url,title,mergeCommit`
4. **If no PR exists** → create a new PR.
5. **If any PR exists and is NOT merged** (`mergedAt` is null) → push only and finish (do **not** create a new PR).
   - This applies to OPEN or CLOSED (unmerged) PRs.
   - Only update title/body/labels if the user explicitly requests changes.
6. **If all PRs for the head are merged** → check for post-merge commits (see below).
7. **If multiple PRs exist for the head** → use the most recently updated PR for reporting, but the create vs push decision is based on `mergedAt`.

## Post-merge commit check (critical)

When all PRs for the head branch are merged, you **must** check whether there are new commits after the merge:

1. **Get the merge commit SHA** of the most recent merged PR.
2. **Validate merge commit ancestry first**: `git merge-base --is-ancestor <merge_commit> HEAD`
3. **If the merge commit is an ancestor of `HEAD`**, count commits after the merge:
   - `git rev-list --count <merge_commit>..HEAD`
4. **If the merge commit is missing or not an ancestor of `HEAD`**, fallback to the branch upstream first:
   - `git rev-list --count origin/<head>..HEAD`
5. **If the upstream comparison fails**, fallback to the base branch comparison:
   - `git rev-list --count origin/<base>..HEAD`
6. **Decision**:
   - If the selected count is greater than 0 → create a new PR
   - If the selected count is 0 → report "No new changes since merge" and finish
   - If both fallback comparisons fail → stop and report `MANUAL CHECK`

### Why this matters

- **Scenario A**: PR merged → user makes local changes → pushes → changes are NOT in the merged PR
  - Without this check, the changes would be lost or require manual intervention
- **Scenario B**: PR merged → user says "create PR" without new changes → would create empty/duplicate PR
  - This check prevents unnecessary PR creation

## PR title rules (must follow)

1. **Format**: `<type>(<scope>): <subject>` — follow Conventional Commits.
2. **type**: must be one of `feat` / `fix` / `docs` / `chore` / `refactor` / `test` / `ci` / `perf`.
3. **scope**: optional. Use a short scope that clearly identifies the affected area (for example: `gui`, `core`, `pty`).
4. **subject**: keep it within 70 characters. Use the imperative mood (for example: "add ..." / "fix ..."). Do not capitalize the first letter or end with a period.
5. If the branch name has a prefix such as `feat/` or `fix/`, **the title type must match that prefix**.

## PR body rules (must follow)

### Section classification

| Section | Required | Notes |
|---------|----------|-------|
| Summary | **YES** | 1-3 bullet points. Include both the what and the why. |
| Changes | **YES** | Enumerate changes by file or module. |
| Testing | **YES** | List the commands run or the exact manual test steps. |
| Related Issues / Links | **YES** | Specify issue numbers, spec links, or "None". |
| Checklist | **YES** | Review every item and mark it checked or N/A. |
| Context | Conditional | Required when 3 or more files changed or the rationale is non-trivial. |
| Risk / Impact | Conditional | Required when the change is breaking, performance-sensitive, or needs rollback steps. |
| Screenshots | Conditional | Required only for UI changes. |
| Deployment | Optional | Include only when deployment steps exist. |
| Notes | Optional | Include only when reviewers need extra context. |

### Validation (agent must check before creating PR)

1. **Do not create a PR if any required section still contains `TODO`.**
2. If a conditional section does not apply, remove the entire section instead of leaving an empty TODO.
3. Each Summary bullet must be a **single sentence**. Do not use vague wording such as "several changes" or "various fixes."
4. Changes must be specific and include the changed file or module names.
5. Testing must be reproducible. Do not use vague wording such as "tested."
6. Add a reason comment to every unchecked checklist item (for example: `- [ ] Docs updated — N/A: no user-facing change`).
7. Related Issues must be written as `#123` or as a URL. If nothing applies, explicitly write "None".

## Issue/PR Comment Formatting (must follow)

- Final comment text must not contain escaped newline literals such as `\n`.
- Use real line breaks in comment bodies. Do not rely on escaped sequences for formatting.
- Before posting, verify the final body does not accidentally include escaped control sequences (`\n`, `\t`).
- If a raw escape sequence must be shown for explanation, include it only inside a fenced code block and clarify it is intentional.

## Issue Progress Comment Template (required for issue-based work)

When work is tracked in GitHub Issues, progress updates must use this template:

```markdown
Progress
- ...

Done
- ...

Next
- ...
```

- Post updates at least when starting work, after meaningful progress, and when blocked/unblocked.
- In `Next`, explicitly state blockers or the immediate next action.

## Workflow (recommended)

1. **Confirm repo + branches**
   - Repo root: `git rev-parse --show-toplevel`
   - Current branch (head): `git rev-parse --abbrev-ref HEAD`
   - Base branch defaults to `develop` unless user specifies.

2. **Check local working tree state (preflight)**
   - Run `git status --porcelain`.
   - If empty, continue.
   - If non-empty, show detected files and ask the user to choose:
     - Continue as-is
     - Abort
     - Manual cleanup first (`git commit` / `git stash` / `git clean`) and rerun
   - Proceed only when the user explicitly chooses continue.

3. **Fetch latest remote state**
   - `git fetch origin` to ensure accurate comparison

4. **Check branch sync against base (critical)**
   - Run `git rev-list --left-right --count "HEAD...origin/$base"`.
   - Parse the result as `ahead behind`.
   - If `behind > 0` and `ahead == 0` → stop and report `Branch update required before creating a PR.`
   - If `behind > 0` and `ahead > 0` → stop and report `Branch has diverged from base. Sync it before creating a PR.`
   - Continue only when `behind == 0`.

5. **Check existing PR for head branch**
   - Use decision rules above to pick action.
   - Treat `mergedAt` as the source of truth for "merged".

6. **If all PRs are merged, perform post-merge commit check**
   - Get merge commit: `gh pr list --head <head> --state merged --json mergeCommit -q '.[0].mergeCommit.oid'`
   - If the merge commit is an ancestor of `HEAD`, count `git rev-list --count <merge_commit>..HEAD`
   - If the merge commit is missing or not an ancestor, count `git rev-list --count origin/<head>..HEAD` first
   - Only if the upstream comparison fails, count `git rev-list --count origin/<base>..HEAD`
   - If the selected count is 0 → finish with message "No new changes since merge"
   - If the selected count is >0 → proceed to create new PR
   - If neither comparison is usable → stop with `MANUAL CHECK`

7. **Ensure the head branch is pushed**
   - If no upstream: `git push -u origin <head>`
   - Otherwise: `git push`

8. **Collect PR inputs (for new PR or explicit update)**
   - Title, Summary, Context, Changes, Testing, Risk/Impact, Deployment, Screenshots, Related Links, Notes
   - Optional: labels, reviewers, assignees, draft

9. **Build PR body from template**
   - Read the template from the gwt-pr skill path (not the current project path):
     - `PR_BODY_TEMPLATE=".gemini/skills/gwt-pr/references/pr-body-template.md"`
   - Read `${PR_BODY_TEMPLATE}` and fill all required placeholders.
   - **If a conditional section does not apply, remove the entire section.**
   - **Remove any `<!-- GUIDE: ... -->` comments from the final output.**
   - **If any required section still contains TODO, do not create the PR and ask the user for the missing information.**

10. **Create or update the PR**
    - Create: `gh pr create -B <base> -H <head> --title "<title>" --body-file <file>`
    - Update (only if user asked): `gh pr edit <number> --title "<title>" --body-file <file>`

11. **Return PR URL**
    - `gh pr view <number> --json url -q .url`

12. **Post-PR CI/merge check (automatic).**
    - After PR creation or push, load `.gemini/skills/gwt-fix-pr/SKILL.md` and follow its workflow to inspect CI status, merge state, and review feedback.
    - If all CI checks are still pending, poll (30s interval) until complete.
    - If conflicts, review issues, or CI failures are detected, proceed with the gwt-fix-pr workflow to diagnose and fix.

## Command snippets (bash)

```bash
head=$(git rev-parse --abbrev-ref HEAD)
base=develop
PR_BODY_TEMPLATE=".gemini/skills/gwt-pr/references/pr-body-template.md"

if [ ! -f "$PR_BODY_TEMPLATE" ]; then
  echo "PR template not found: $PR_BODY_TEMPLATE" >&2
  exit 1
fi

# Preflight: local working tree state
status_lines=$(git status --porcelain)
if [ -n "$status_lines" ] && [ "${ALLOW_DIRTY_WORKTREE:-0}" != "1" ]; then
  echo "Detected local uncommitted/untracked changes:" >&2
  echo "$status_lines" >&2
  echo "Choose one before continuing: continue as-is, abort, or manual cleanup then rerun." >&2
  echo "Set ALLOW_DIRTY_WORKTREE=1 only after explicit user confirmation to continue." >&2
  exit 1
fi

# Fetch latest remote state
git fetch origin

# Check branch sync against base before PR creation
divergence=$(git rev-list --left-right --count "HEAD...origin/$base" 2>/dev/null) || {
  echo "Failed to compare HEAD with origin/$base" >&2
  exit 1
}
ahead_count=$(echo "$divergence" | awk '{print $1}')
behind_count=$(echo "$divergence" | awk '{print $2}')

if [ "${behind_count:-0}" -gt 0 ] && [ "${ahead_count:-0}" -gt 0 ]; then
  echo "Branch has diverged from base. Sync it before creating a PR." >&2
  exit 1
fi

if [ "${behind_count:-0}" -gt 0 ]; then
  echo "Branch update required before creating a PR." >&2
  exit 1
fi

# Check existing PRs for the head branch
pr_json=$(gh pr list --head "$head" --state all --json number,state,mergedAt,mergeCommit)
pr_count=$(echo "$pr_json" | jq 'length')
unmerged_count=$(echo "$pr_json" | jq 'map(select(.mergedAt == null)) | length')

if [ "$pr_count" -eq 0 ]; then
  action=create
elif [ "$unmerged_count" -gt 0 ]; then
  action=push_only
else
  # All PRs are merged - check for post-merge commits
  merge_commit=$(echo "$pr_json" | jq -r 'sort_by(.mergedAt) | last | .mergeCommit.oid')
  new_commits=""

  if [ -n "$merge_commit" ] && [ "$merge_commit" != "null" ] && \
     git merge-base --is-ancestor "$merge_commit" HEAD 2>/dev/null; then
    new_commits=$(git rev-list --count "$merge_commit"..HEAD 2>/dev/null || echo "")
  fi

  if [ -n "$new_commits" ]; then
    if [ "$new_commits" -gt 0 ]; then
      echo "Found $new_commits commit(s) after merge - creating new PR"
      action=create
    else
      echo "No new commits since merge - nothing to do"
      action=none
    fi
  else
    upstream_commits=$(git rev-list --count "origin/$head"..HEAD 2>/dev/null || echo "")

    if [ -n "$upstream_commits" ]; then
      if [ "$upstream_commits" -gt 0 ]; then
        echo "Found $upstream_commits commit(s) ahead of origin/$head - creating new PR"
        action=create
      else
        echo "No new commits ahead of origin/$head - nothing to do"
        action=none
      fi
    else
      fallback_commits=$(git rev-list --count "origin/$base"..HEAD 2>/dev/null || echo "")

      if [ -n "$fallback_commits" ]; then
        if [ "$fallback_commits" -gt 0 ]; then
          echo "Upstream comparison unavailable; found $fallback_commits commit(s) ahead of origin/$base - creating new PR"
          action=create
        else
          echo "Upstream comparison unavailable and no commits ahead of origin/$base - nothing to do"
          action=none
        fi
      else
        echo "Manual check required: could not determine whether new commits exist after the last merge" >&2
        action=manual_check
      fi
    fi
  fi
fi

# Execute action
case "$action" in
  create)
    cp "$PR_BODY_TEMPLATE" /tmp/pr-body.md

    git push -u origin "$head"
    gh pr create -B "$base" -H "$head" --title "..." --body-file /tmp/pr-body.md
    ;;
  push_only)
    echo "Existing unmerged PR found - pushing changes only"
    git push
    gh pr list --head "$head" --state open --json url -q '.[0].url'
    ;;
  none)
    echo "No action needed - no new changes since last merge"
    ;;
  manual_check)
    echo "Manual check required - post-merge commit status could not be determined" >&2
    exit 1
    ;;
esac
```

## References

- `.gemini/skills/gwt-pr/references/pr-body-template.md`: PR body template
