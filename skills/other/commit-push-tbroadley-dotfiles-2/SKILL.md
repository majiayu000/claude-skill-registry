---
name: commit-push
description: This skill should be used when the user asks to "commit and push", "push my changes", or wants to commit, push, and respond to PR comments.
user-invocable: true
---

# Commit, Push, and Ensure CI Passes

Commit changes, run local validation, push to remote, open a draft PR if needed, and ensure CI passes.

## Workflow

### 1. Pre-Commit Cleanup

Before running validation, clean up your changes:

- Remove comments and docstrings you added (user instructions take precedence if they want docstrings)
- Remove try-except blocks that suppress errors—code should fail early rather than log warnings and potentially behave incorrectly. Exception: when aggregating results from multiple operations to report at the end.
- Move imports to top of file

### 2. Run Local Validation

Before committing, run all local checks:

**Linting, Typechecking, and Formatting:**
- Run the project's linter (e.g., `ruff check`, `eslint`, `golangci-lint`)
- Run the typechecker (e.g., `basedpyright`, `mypy`, `tsc --noEmit`)
- Run the formatter (e.g., `ruff format --check`, `prettier --check`, `gofmt`)
- Fix any issues found before proceeding

**Tests:**
- Check if the project has slow tests marked with `@pytest.mark.slow` (search for `mark.slow` in test files)
- If slow tests exist: run `pytest -m "not slow"` for fast tests, then run affected slow tests
- If no slow test markers exist, run all tests: `pytest`, `npm test`, `go test ./...`
- To identify affected slow tests, check which test files import or exercise modified code
- If pytest-xdist is available (`uv pip show pytest-xdist`), use `-n auto` for parallel execution:
  ```bash
  pytest -n auto -m "not slow"  # fast tests in parallel
  pytest -n auto path/to/slow_test1.py path/to/slow_test2.py  # affected slow tests in parallel
  ```

### 3. DVC (Data Version Control)

If this is a DVC-tracked repository (has `.dvc` files or `dvc.yaml`):
- Run `dvc repro` to reproduce any affected pipelines
- Run `dvc push` to push data artifacts to remote storage
- This prevents `check-dvc` CI failures

**Fixing `check-dvc` CI failures:**
1. Run `dvc status --remote` to see which files are missing
2. Run `dvc push` to upload missing files to the remote
3. Commit any updated `.dvc` files if they changed

### 3b. Pivot (Pipeline Management)

If this is a Pivot-tracked repository (has `.pvt` files or `pipeline.py`):
- Run `pivot run` to execute any outdated pipeline stages
- Run `pivot push` to push outputs to S3
- Commit any updated `.pvt` or `.pivot/stages/*.lock` files
- This prevents `check-pivot` CI failures

**Fixing `check-pivot` CI failures:**
1. Run `pivot status` to see which stages need to run
2. Run `pivot run` to execute outdated stages (or `pivot run stage_name@variant` for specific stages)
3. Run `pivot push` to upload outputs to S3
4. Commit any updated `.pvt` or `.pivot/stages/*.lock` files

### 4. Commit and Push

Once local validation passes:

1. Run `git status` and `git diff` to see changes
2. Run `git log --oneline -3` to match commit message style
3. Stage changes with `git add`
4. Create commit with descriptive message ending with:
   ```
   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   ```
5. Push to remote with `git push`

### 5. Check if on Main Branch

Determine if you're pushing directly to the main branch:

```bash
current_branch=$(git branch --show-current)
main_branch=$(git remote show origin | grep 'HEAD branch' | cut -d: -f2 | xargs)

if [ "$current_branch" = "$main_branch" ]; then
  # Pushing directly to main - skip PR creation, go to step 10
  echo "On main branch, skipping PR workflow"
fi
```

**If on main/master:** Skip steps 6-9 and go directly to step 10 (Wait for CI on Direct Push).

**If on a feature branch:** Continue with step 6.

### 6. Determine PR Base Branch (Feature Branches Only)

Before creating a PR, determine the correct base branch:

```bash
# Get the main/master branch name
main_branch=$(git remote show origin | grep 'HEAD branch' | cut -d: -f2 | xargs)

# Find the merge-base with main
merge_base=$(git merge-base HEAD origin/$main_branch)

# Check if there's another branch between current branch and main
# This finds branches that contain the merge-base but are not main
intermediate_branch=$(git branch -r --contains $merge_base | grep -v "origin/$main_branch" | grep -v "origin/HEAD" | head -1 | xargs)

# If an intermediate branch exists and is an ancestor of HEAD, use it as base
if [ -n "$intermediate_branch" ]; then
  base_branch=${intermediate_branch#origin/}
else
  base_branch=$main_branch
fi
```

Use `$base_branch` as the PR base instead of always using main/master.

### 7. Open or Update Draft PR (Feature Branches Only)

Check if the current branch has an open PR:

```bash
gh pr view --json number,url,state,isDraft 2>/dev/null
```

**If no PR exists:**
- Create a draft PR targeting the correct base branch:
  ```bash
  gh pr create --draft --base $base_branch --title "..." --body "..."
  ```
- Assign the PR to Thomas Broadley:
  ```bash
  gh pr edit --add-assignee tbroadley
  ```
- Add an OKR label (choose the most relevant from available labels starting with `OKR-`):
  ```bash
  # List available OKR labels
  gh label list --search "OKR-"
  # Add the appropriate label using the API (gh pr edit --add-label can fail due to deprecated Projects classic)
  gh api repos/{owner}/{repo}/issues/{pr_number}/labels -f "labels[]=okr-..."
  ```

**If PR already exists:**
- Update the PR title and description to reflect all changes on the branch (not just the latest commit):
  ```bash
  # Review all commits on the branch vs base
  git log origin/$base_branch..HEAD --oneline
  git diff origin/$base_branch..HEAD --stat

  # Update the PR title and body via the API
  gh api repos/{owner}/{repo}/pulls/{pr_number} -X PATCH \
    -f title="<concise title reflecting all branch changes>" \
    -f body="$(cat <<'EOF'
  ## Summary
  <1-3 bullet points covering all changes on the branch>

  ## Test plan
  <how the changes were validated>
  EOF
  )"
  ```
- The title should be concise (<70 chars) and reflect the overall purpose of the branch
- The body should summarize all changes, not just the latest push
- Preserve any existing sections added by reviewers (e.g., deployment notes)

### 8. Wait for CI and Ensure It Passes (Feature Branches Only)

**First, check if the repo has GitHub Actions workflows:**

```bash
# Check for workflow files
if ! ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | head -1 > /dev/null; then
  echo "No GitHub Actions workflows found, skipping CI wait"
  # Skip to step 9
fi
```

If no workflows exist, skip waiting for CI and proceed to step 9.

**Before waiting for CI, check for merge conflicts:**

Merge conflicts prevent CI from running. Check immediately after pushing:

```bash
gh pr view --json mergeable,mergeStateStatus
```

- If `mergeable` is `false` or `mergeStateStatus` is `DIRTY`, there are merge conflicts
- If `mergeable` is `UNKNOWN`, wait a few seconds and check again (GitHub is still computing)

**If merge conflicts exist**, resolve them before waiting for CI (see "If CI cannot run" below).

**If no conflicts**, monitor CI status:

```bash
gh pr checks --watch
```

**If CI cannot run (e.g., merge conflict):**
1. Identify the blocker: `gh pr view --json mergeable,mergeStateStatus`
2. If merge conflict:
   ```bash
   git fetch origin $base_branch
   git rebase origin/$base_branch
   # Resolve conflicts
   git add .
   git rebase --continue
   ```
3. Run local validation again (steps 1-2)
4. Force push: `git push --force-with-lease`
5. Wait for CI again

**If CI fails:**
1. Check which jobs failed: `gh pr checks`
2. Get failure details: `gh run view <run_id> --log-failed`
3. Fix the failing tests/checks locally
4. Run local validation again (steps 1-2)
5. Commit the fixes and push
6. Repeat until CI passes

### 9. Respond to PR Comments (Feature Branches Only)

**IMPORTANT:** Never leave top-level comments on the PR (via `gh pr comment` or the issues comments API). Only reply directly within review comment threads using the replies API. Top-level comments like "Addressed review feedback" clutter the PR.

If there are existing PR review comments, check if pushed changes address them.

Fetch review comments:
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate
```

For each unresolved comment that was addressed:

1. Leave a reply:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
     -f body="Claude Code: <explanation of how this was addressed>"
   ```

2. Resolve the thread:
   ```bash
   gh api graphql -f query='
     mutation {
       resolveReviewThread(input: {threadId: "<thread_id>"}) {
         thread { isResolved }
       }
     }
   '
   ```

To get thread IDs:
```bash
gh api graphql -f query='
  query {
    repository(owner: "{owner}", name: "{repo}") {
      pullRequest(number: {pr_number}) {
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            comments(first: 1) {
              nodes {
                id
                databaseId
                body
              }
            }
          }
        }
      }
    }
  }
'
```

**Re-request review:** After addressing all comments from a reviewer, request their re-review:
```bash
gh pr edit --add-reviewer <reviewer-username>
```

To find reviewers who left comments:
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews --jq '.[].user.login' | sort -u
```

### 10. Wait for CI on Direct Push (Main Branch Only)

**First, check if the repo has GitHub Actions workflows:**

```bash
# Check for workflow files
if ! ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | head -1 > /dev/null; then
  echo "No GitHub Actions workflows found, skipping CI wait"
  # Task complete - no CI to wait for
fi
```

If no workflows exist, the task is complete.

**If workflows exist**, monitor CI using the workflow run:

```bash
# Watch the CI run for the latest commit
gh run watch
```

**If CI fails:**
1. Check which jobs failed: `gh run view --log-failed`
2. Fix the failing tests/checks locally
3. Run local validation again (steps 1-2)
4. Commit the fixes and push
5. Repeat until CI passes

## Notes

- Always run local validation before pushing to catch issues early
- Steps 6-9 only apply to feature branches (not main/master)
- Step 10 only applies when pushing directly to main/master
- Only respond to PR comments that were actually addressed by the changes
- Prefix all GitHub comments with "Claude Code: "
- If CI keeps failing after multiple attempts, report the issue to the user
- The goal is green CI before considering the task complete (on a draft PR for feature branches, or on the commit for direct pushes to main)

## GitHub API Workarounds

`gh pr edit` often fails with "Projects (classic) deprecation" errors. Use the API directly instead:

```bash
# Edit PR body
gh api repos/{owner}/{repo}/pulls/{number} -X PATCH -f body="..."

# Add reviewer
gh api repos/{owner}/{repo}/pulls/{number}/requested_reviewers -X POST -f "reviewers[]=username"

# Add label
gh api repos/{owner}/{repo}/issues/{number}/labels -f "labels[]=label-name"

# Add assignee
gh api repos/{owner}/{repo}/issues/{number}/assignees -f "assignees[]=username"
```
