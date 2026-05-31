---
name: commit-push
description: commit and push all local changes to remote repo
disable-model-invocation: true
---

# Commit and Push

Commit all local changes following Conventional Commits format and push to remote.

## Gates

Complete **in order**. Do not run the next action until the **Pass** condition is satisfied (use command output as evidence, not memory).

1. **Diff understood** — **Pass when:** Outputs from `git status`, `git diff`, and `git diff --cached` are consistent with your one-sentence description of what changed (or you recorded that there is nothing to commit).
2. **Commit line chosen** — **Pass when:** You have a draft first line `type(scope): description` (or `type: description` if omitting scope) that matches the change set you intend to ship.
3. **Staging matches intent** — **Pass when:** After `git add`, `git diff --cached --stat` (and spot-check `git diff --cached` if needed) shows only the paths you meant to include; adjust staging before committing if not.
4. **Push target confirmed** — **Pass when:** Current branch and remote are the ones you intend (`git branch -vv`, `git remote -v`); then push.
5. **Remote caught up** — **Pass when:** `git status` is clean and `git status -sb` shows the branch is up to date with its configured upstream (no unexpected unpushed commits left for this task).

## Step 1: Gather Context

Run these commands in parallel to understand the changes:

```bash
# See all untracked and modified files
git status

# See staged and unstaged changes
git diff
git diff --cached

# See recent commit messages for style reference
git log --oneline -10
```

## Step 2: Analyze Changes

Review the changes and determine:
- **Type**: What kind of change is this?
  - `feat` - New feature or capability
  - `fix` - Bug fix
  - `docs` - Documentation only
  - `refactor` - Code restructure without behavior change
  - `test` - Adding or updating tests
  - `chore` - Maintenance, dependency updates
  - `perf` - Performance improvement
  - `ci` - CI/CD changes

- **Scope**: Which component is affected?
  - Examine the changed files and determine the appropriate scope
  - Use consistent scope names within the project (check `git log` for patterns)
  - *(omit scope for cross-cutting changes)*

- **Breaking**: Does this break backward compatibility? If yes, add **!** after scope.

## Step 3: Write Commit Message

Format:
```
type(scope): description

[optional body explaining why, not what]

[optional footer with issue references]
```

Rules:
- Use imperative mood: "add feature" not "added feature"
- Keep first line under 72 characters
- Focus on *why* in the body, the diff shows *what*
- Reference issues: `Closes #123` or `Fixes #456`

## Step 4: Stage, Commit, and Push

Satisfy **Gates** 1–3 before `git commit`; satisfy **Gate** 4 before `git push`; satisfy **Gate** 5 after push.

```bash
# Stage all changes (or selectively stage)
git add -A

# Gate 3: confirm staged set before committing
git diff --cached --stat

# Commit with message (use HEREDOC for multi-line)
git commit -m "$(cat <<'EOF'
type(scope): description

Optional body explaining the motivation.

Closes #123

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to remote
git push
```

## Examples

```bash
# Simple feature
git commit -m "feat(api): add pagination support to list endpoints"

# Bug fix with body
git commit -m "$(cat <<'EOF'
fix(auth): handle token expiration during long requests

The previous implementation did not account for tokens expiring
during the processing of long-running requests.

Fixes #42

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Breaking change
git commit -m "$(cat <<'EOF'
feat!(api): change response format for user endpoints

BREAKING CHANGE: The `status` field is now an object with `state` and
`message` properties instead of a plain string.

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Step 5: Verify

After pushing, satisfy **Gate 5**: run `git status` and `git status -sb` and confirm a clean tree and upstream sync (or an expected ahead/behind you can explain, e.g. fork workflow).
