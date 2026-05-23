---
name: done
description: Finish a task by committing changes, rebasing on main, and creating a PR
disable-model-invocation: true
user-invocable: true
argument-hint: [optional commit message]
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Task Completion Workflow

You are finishing a development task. Follow these steps in order to commit changes, rebase on main, and create a pull request.

## CRITICAL RULES

- **NEVER** include AI tool references in commits, PRs, or code comments
- **NO** "Co-Authored-By: Claude" or similar AI attributions
- All git history must appear human-authored
- Follow conventional commit format: `<type>: <description>`

## Step 1: Pre-flight Checks

Run these checks **sequentially**:

1. Verify in git repository:
   ```bash
   git rev-parse --git-dir
   ```

2. Get current branch:
   ```bash
   git branch --show-current
   ```

3. Check for changes:
   ```bash
   git status --porcelain
   ```

**Stop conditions:**
- If not in git repo → **Error**: "Not in a git repository"
- If on `main` branch → **Error**: "Cannot commit directly to main branch. Create a feature branch first."
- If no changes (empty output) → **Error**: "No changes to commit"

If all checks pass, proceed to Step 2.

## Step 2: Analyze and Commit Changes

### 2.1 Review Changes

Run these commands to understand what changed:

```bash
git status
git diff HEAD
```

If there are already staged files, also check:
```bash
git diff --staged
```

### 2.2 Analyze Changes

Based on the diff output, determine:

- **Commit type**: Choose from:
  - `feat` - New feature
  - `fix` - Bug fix
  - `refactor` - Code restructuring without behavior change
  - `docs` - Documentation only
  - `style` - Formatting, whitespace, missing semicolons
  - `test` - Adding or updating tests
  - `chore` - Build process, dependencies, tooling

- **Description**: Write a concise summary (< 72 characters) that completes the sentence: "This commit will..."
  - Good: "add user authentication middleware"
  - Good: "fix null pointer dereference in login handler"
  - Bad: "changes" or "updates stuff"

- **Body** (optional): Add if the change is complex and needs explanation

### 2.3 Security Check

Check if any changed files match sensitive patterns:
```bash
git status --porcelain | grep -E '\.(env|key|pem)|credentials|secrets'
```

If matches found:
- **Warn the user**: "Detected potential sensitive files: [list]. Are you sure you want to commit these?"
- **Wait for user confirmation** before proceeding
- If user declines, stop here

### 2.4 Stage Files

Prefer staging specific files rather than using `git add .`:

```bash
git add <file1> <file2> <file3>
```

Only use `git add .` if justified (many files changed, all safe to commit).

### 2.5 Create Commit

**If $ARGUMENTS is provided**: Use it as the commit message directly:
```bash
git commit -m "$ARGUMENTS"
```

**Otherwise**: Generate the commit message using the format:
```
<type>: <description>
```

Example:
```bash
git commit -m "feat: add user authentication middleware"
```

**CRITICAL**: Do NOT add any Co-Authored-By or AI attribution trailers.

### 2.6 Verify Commit

Check the commit was created:
```bash
git log -1 --oneline
```

If commit failed (pre-commit hooks, etc.):
- Show the error message to the user
- **STOP**: Let the user fix the issue
- User can run `/done` again after fixing

## Step 3: Rebase on origin/main

### 3.1 Fetch Latest

Update the remote tracking branches:
```bash
git fetch origin
```

### 3.2 Rebase

Rebase current branch onto origin/main:
```bash
git rebase origin/main
```

### 3.3 Handle Rebase Result

**If rebase succeeds**: Proceed to Step 4.

**If conflicts are detected** (non-zero exit code):

**STOP** and inform the user:

```
Rebase conflicts detected. To resolve:

1. Check conflict status:
   git status

2. Open conflicted files and resolve conflicts (look for <<<<<<< markers)

3. Stage resolved files:
   git add <resolved-file>

4. Continue the rebase:
   git rebase --continue

5. After resolving all conflicts, run /done again to create the PR

To abort the rebase:
   git rebase --abort
```

**DO NOT** attempt automatic conflict resolution. This requires human judgment.

## Step 4: Create Pull Request

### 4.1 Gather Context

Get branch and commit information:

```bash
# Current branch name
git branch --show-current

# All commits in this branch (not in main)
git log origin/main..HEAD --oneline

# Full commit details
git log origin/main..HEAD

# Summary of changed files
git diff origin/main...HEAD --stat
```

### 4.2 Analyze Commits

Review ALL commits in the branch to understand the overall change:
- If **single commit**: PR title = commit message (which already includes the type prefix)
- If **multiple commits**: Summarize the overall feature/fix with appropriate type prefix (feat, fix, refactor, etc.)

### 4.3 Generate PR Title

- **MUST** start with conventional commit type prefix: `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, or `chore:`
- Use clear, concise language after the prefix
- Keep under 72 characters total
- No AI attribution

Example titles:
- "feat: add user authentication middleware"
- "fix: null pointer dereference in login handler"
- "refactor: session management for improved performance"
- "docs: add API documentation for auth endpoints"
- "chore: update dependencies to latest versions"

### 4.4 Generate PR Body

Use this format:

```markdown
## Summary

- [Key change 1]
- [Key change 2]
- [Key change 3]

## Test plan

- [ ] [Test scenario 1]
- [ ] [Test scenario 2]
- [ ] [Test scenario 3]
```

Guidelines:
- 3-5 bullet points in Summary
- Focus on "what" and "why", not implementation details
- Test plan should be actionable checklist items
- **NO** "Generated with Claude Code" or AI attribution footer

### 4.5 Push Branch (if needed)

Before creating the PR, check if the branch has been pushed:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

**If this command fails** (no upstream branch set):

Push the branch and set upstream:
```bash
git push -u origin <branch-name>
```

**If this command succeeds** (upstream branch exists):

Check if local is ahead of remote:
```bash
git status -sb
```

If the output shows `[ahead N]` or `[ahead N, behind M]`:
- After rebase, the branch needs a force push
- Run: `git push --force-with-lease`

### 4.6 Create PR

Use heredoc for proper formatting:

```bash
gh pr create --title "PR title here" --body "$(cat <<'EOF'
## Summary

- Key change 1
- Key change 2
- Key change 3

## Test plan

- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test scenario 3
EOF
)" --base main
```

### 4.7 Handle PR Creation Result

**If successful**:
- Display the PR URL to the user

**If PR already exists**:
- Show error message
- If possible, extract and display the existing PR URL from the error
- Inform user: "A PR already exists for this branch"

**If GitHub CLI not found**:
- Show installation instructions:
  ```
  GitHub CLI (gh) not found. Install it:
  - macOS: brew install gh
  - Linux: See https://github.com/cli/cli#installation

  After installation, authenticate: gh auth login
  ```

## Error Handling

For any command that fails:
1. Show the **exact error message** from the command
2. Provide **actionable next steps** for the user
3. **DO NOT** proceed to the next phase
4. User can fix the issue and run `/done` again

## Notes

- The workflow automatically handles pushing the branch if needed (Step 4.5)
- Prefer clear, atomic commits over large batch commits
- The PR description should help reviewers understand the context quickly
- If pre-commit hooks modify files, they'll need to be staged and committed again
- After rebase, force push with `--force-with-lease` is safer than `--force` (protects against overwriting others' work)

## Usage Examples

**Basic usage (auto-generated commit message):**
```
/done
```

**With custom commit message:**
```
/done "feat: add new authentication feature"
```

**With multi-line commit message:**
```
/done "feat: add authentication

Implements OAuth2 flow with JWT tokens.
Includes session management and refresh tokens."
```
