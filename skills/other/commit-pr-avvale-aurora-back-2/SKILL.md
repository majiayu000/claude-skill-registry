---
name: commit-pr
description: >
  Commit, push changes, and create a Pull Request on GitHub.
  Trigger: User runs /commit-pr command.
disable-model-invocation: true
---

## When to Use

- User explicitly runs `/commit-pr` command
- User asks to "commit and create a PR"
- User wants to submit changes for review

---

## Prerequisites

- `gh` CLI must be installed and authenticated
- Repository must be hosted on GitHub

```bash
# Verify gh is available and authenticated
gh auth status
```

---

## Execution Flow

### Step 1: Execute Commit Flow

First, execute the full `/commit` workflow:

1. Analyze changes (`git status`, `git diff`)
2. Generate commit message (Conventional Commits)
3. Stage and commit
4. Push to remote

See `.claude/skills/commit/SKILL.md` for details.

### Step 2: Gather PR Context

```bash
# Get current branch
git branch --show-current

# Get base branch (usually main)
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'

# Get all commits in this branch (not in base)
git log origin/main..HEAD --oneline

# Get full diff against base
git diff origin/main...HEAD --stat
```

### Step 3: Generate PR Content

**Title:** Based on the commit message or branch purpose

- If single commit: Use commit message as title
- If multiple commits: Summarize the feature/fix

**Body:** Structured summary using this template:

```markdown
## Summary
<1-3 bullet points describing the changes>

## Test plan
- [ ] <Testing checklist items>

---
Generated with [Claude Code](https://claude.ai/code)
```

### Step 4: Create Pull Request

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
- <change 1>
- <change 2>

## Test plan
- [ ] <test item 1>
- [ ] <test item 2>

---
Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

**Optional flags:**
- `--base <branch>` - Target branch (default: main)
- `--draft` - Create as draft PR
- `--label <label>` - Add labels
- `--assignee @me` - Assign to self
- `--reviewer <user>` - Request review

### Step 5: Verify and Report

```bash
# Get PR URL
gh pr view --web
```

---

## Output Format

After successful execution, display:

```
Commit: <hash> <type>(<scope>): <subject>
Branch: <branch-name> -> main
PR: #<number> <title>
URL: https://github.com/<org>/<repo>/pull/<number>
Status: Ready for review
```

---

## PR Title Guidelines

| Commit Type | PR Title Example |
|-------------|------------------|
| `feat` | Add ISBN validation to book creation |
| `fix` | Fix token refresh race condition |
| `refactor` | Extract validation logic to service |
| `docs` | Update API documentation |
| `test` | Add unit tests for book handler |

**Rules:**
- Capitalize first letter
- No period at end
- Be descriptive but concise
- Include scope if helpful

---

## PR Body Guidelines

### Summary Section
- 1-3 bullet points
- Focus on WHAT and WHY
- Link to issues if applicable: `Closes #123`

### Test Plan Section
- List manual testing steps
- Note any automated tests added
- Include edge cases to verify

### Example Body

```markdown
## Summary
- Add ISBN-10 and ISBN-13 validation in CreateBookHandler
- Implement checksum verification for both formats
- Add descriptive error messages for invalid ISBNs

Closes #234

## Test plan
- [ ] Create book with valid ISBN-10
- [ ] Create book with valid ISBN-13
- [ ] Verify error for invalid checksum
- [ ] Verify error for malformed ISBN

---
Generated with [Claude Code](https://claude.ai/code)
```

---

## Edge Cases

### PR Already Exists
```bash
# Check if PR exists for current branch
gh pr list --head $(git branch --show-current)
```

If PR exists, show link instead of creating new one.

### Branch Not Pushed
The commit flow handles this automatically with `git push -u origin <branch>`.

### No GitHub Remote
```
Error: Repository doesn't have a GitHub remote.
This command requires a GitHub-hosted repository.
```

### gh Not Authenticated
```
Error: GitHub CLI not authenticated.
Run: gh auth login
```

---

## Commands Reference

```bash
# GitHub CLI
gh auth status                      # Check authentication
gh pr create --title "..." --body "..."  # Create PR
gh pr list --head <branch>          # Check existing PRs
gh pr view --web                    # Open PR in browser
gh pr view --json url               # Get PR URL

# Git context
git branch --show-current           # Current branch
git log origin/main..HEAD --oneline # Commits in branch
git diff origin/main...HEAD --stat  # Changes summary
```

---

## Related Skills

- **commit**: Base commit and push workflow
- **conventional-commits**: Commit message format

---

## Workflow Example

```
User: /commit-pr

Claude:
1. [Runs git status, git diff]
2. [Analyzes changes]
3. [Generates commit message]

   Committing: feat(library/book): add ISBN validation

4. [git add . && git commit]
5. [git push -u origin feature/isbn-validation]

   Pushed to origin/feature/isbn-validation

6. [Generates PR content]
7. [gh pr create]

   Commit: a1b2c3d feat(library/book): add ISBN validation
   Branch: feature/isbn-validation -> main
   PR: #42 Add ISBN validation to book creation
   URL: https://github.com/org/repo/pull/42
   Status: Ready for review
```
