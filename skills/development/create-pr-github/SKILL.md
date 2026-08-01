---
name: create-pr-github
description: Create and (optionally) merge a GitHub pull request (prefer GitHub chat
  tools; gh/wrappers are fallback), following the repo policy to use rebase and merge
  for a linear history.
---

---
name: create-pr-github
description: Create and (optionally) merge a GitHub pull request (prefer GitHub chat tools; gh/wrappers are fallback), following the repo policy to use rebase and merge for a linear history.
compatibility: Preferred: GitHub chat tools configured for the repo. Fallback: git + GitHub CLI (gh) authenticated, plus network access.
---

# Create PR (GitHub)

## Purpose
Create a GitHub pull request in a consistent, policy-compliant way, and include the repo’s preferred merge method guidance (rebase and merge).

This skill prefers using GitHub chat tools because they can be permanently allowed in VS Code and avoid terminal pager/editor issues. If chat tools are unavailable (or repo context is unknown), fall back to the repo wrapper script `scripts/pr-github.sh`.

## Hard Rules
### Must
- Work on a non-`main` branch.
- Ensure the working tree is clean before creating a PR.
- Push the branch to `origin` before creating the PR.
- Before creating the PR, post the **exact Title and Description** in chat.
- Use the standard PR body template (Problem / Change / Verification).
- Use **Rebase and merge** for merging PRs to maintain a linear history (see `CONTRIBUTING.md`).

### Must Not
- Create PRs from `main`.
- Use “Squash and merge” or “Create a merge commit”.
- Use `--fill` or any heuristic that guesses title/body (not supported by the wrapper).

## Actions

### 0. Title + Description (Required)
Before running any PR creation command, provide in chat:

- **PR title** (exact)
- **PR description** (exact), using this template:

```markdown
## Problem
<why is this change needed?>

## Change
<what changed?>

## Verification
<how was it validated?>
```

### Recommended: One-Command Wrapper
Create a PR:
```bash
echo "## Summary\n\nPR description" | scripts/pr-github.sh create --title "<type(scope): summary>" --body-from-stdin
```

Create and merge (only when explicitly requested):
```bash
echo "## Summary\n\nPR description" | scripts/pr-github.sh create-and-merge --title "<type(scope): summary>" --body-from-stdin
```

### 1. Pre-flight Checks
```bash
git branch --show-current
git status --short
```

### 2. Push the Branch
```bash
git push -u origin HEAD
```

### 3. Create the PR
#### Preferred: GitHub chat tools
Use the GitHub PR creation tool with an explicit title + body (same template as above).

Notes:
- This requires repo context (`owner` + `repo`) and your pushed branch name.
- If you do not know `owner`/`repo` reliably, use the wrapper fallback below.

#### Fallback: `gh` CLI
```bash
echo "## Summary\n\nPR description" | PAGER=cat gh pr create \
  --base main \
  --head "$(git branch --show-current)" \
  --title "<type(scope): summary>" \
  --body-file -
```

### 4. Merge (Only When Explicitly Requested)
This repository requires **rebase and merge**.

#### Preferred: GitHub chat tools
Use the GitHub PR merge tool with `merge_method=rebase`.

#### Fallback: `gh` CLI
```bash
PAGER=cat gh pr merge <pr-number> --rebase --delete-branch
```

### 5. If Rebase-Merge Is Blocked (Conflicts)
```bash
git pull --rebase origin main
# resolve conflicts

git push --force-with-lease
```

Then retry the merge.
