---
name: github-pr-creation
description: Creates GitHub Pull Requests with automated validation and task tracking. Use when user wants to create PR, open pull request, submit for review, or check if ready for PR. Analyzes commits, validates task completion, generates Conventional Commits title and description, suggests labels. NOTE - for merging existing PRs, use github-pr-merge instead.
---

# GitHub PR Creation

Creates Pull Requests with task validation, test execution, and Conventional Commits formatting.

## Quick Start

```bash
# 1. Verify GitHub CLI
gh --version && gh auth status

# 2. Gather information (the AI Assistant does this directly)
git log develop..HEAD --oneline        # Commits to include
git diff develop --stat                 # Files changed
git rev-parse --abbrev-ref HEAD        # Current branch

# 3. Run project tests
make test  # or: pytest, npm test

# 4. Create PR (after generating content)
gh pr create --title "..." --body "..." --base develop --label feature
```

## Core Workflow

### 1. Verify Environment

```bash
gh --version && gh auth status
```

If not installed: `brew install gh` then `gh auth login`

### 2. Confirm Target Branch

**Always ask user**:
```
I'm about to create a PR from [current-branch] to [target-branch]. Is this correct?
- feature branch → develop (90% of cases)
- develop → master/main (releases)
```

### 3. Gather Information

Execute these commands and analyze results directly:

```bash
# Current branch
git rev-parse --abbrev-ref HEAD

# Commits since base branch
git log [base-branch]..HEAD --pretty=format:"%H|%an|%ai|%s"

# Commits with full details (for context)
git log [base-branch]..HEAD --oneline

# Files changed
git diff [base-branch] --stat

# Remote tracking status
git status -sb
```

### 4. Search for Task Documentation

Look for task files in these locations (in order):
1. `.kiro/specs/*/tasks.md`
2. `docs/specs/*/tasks.md`
3. `specs/*/tasks.md`
4. Any `tasks.md` in project root

Extract from task files:
- Task IDs (format: `Task X` or `Task X.Y`)
- Task titles and descriptions
- Requirements (format: `Requirements: X, Y, Z`)

### 5. Analyze Commits

For each commit, identify:
- **Type**: feat, fix, refactor, docs, test, chore, ci, perf, style
- **Scope**: component/module affected (kebab-case)
- **Task references**: look for `task X.Y`, `Task X`, `#X.Y` patterns
- **Breaking changes**: exclamation mark after type/scope, or `BREAKING CHANGE` in body

Map commits to documented tasks when task files exist.

### 6. Verify Task Completion

If task documentation exists:
1. Identify main task from branch name (e.g., `feature/task-2-*` → Task 2)
2. Find all sub-tasks (e.g., Task 2.1, 2.2, 2.3)
3. Check which sub-tasks are referenced in commits
4. Report missing sub-tasks

**If tasks incomplete**: STOP and inform user with:
```
✗ Task 2 INCOMPLETE: 1/3 sub-tasks missing
- Task 2.1: ✓ Implemented
- Task 2.2: ✓ Implemented
- Task 2.3: ✗ MISSING
```

### 7. Run Tests

Detect and run project tests:
- If Makefile with `test` target: `make test`
- If package.json: `npm test`
- If Python project: `pytest`

**Tests MUST pass before creating PR.**

### 8. Determine PR Type

| Branch Flow | PR Type | Title Prefix |
|-------------|---------|--------------|
| feature/* → develop | Feature | `feat(scope):` |
| fix/* → develop | Bugfix | `fix(scope):` |
| hotfix/* → main | Hotfix | `hotfix(scope):` |
| develop → main | Release | `release:` |
| refactor/* → develop | Refactoring | `refactor(scope):` |

### 9. Generate PR Content

Use appropriate template from `references/pr_templates.md` based on PR type.

**Title format**: `<type>(<scope>): <description>`
- Type: dominant commit type (feat > fix > refactor)
- Scope: most common scope from commits, or task-related scope (kebab-case)
- Description: imperative, lowercase, no period, max 50 chars

**Body**: Select template based on PR type and populate with gathered data.

### 10. Suggest Labels

| Commit Type | Labels |
|-------------|--------|
| feat | feature, enhancement |
| fix | bug, bugfix |
| refactor | refactoring, tech-debt |
| docs | documentation |
| ci | ci/cd, infrastructure |
| security | security |
| hotfix | urgent, priority:high |

Check available labels: `gh label list`

### 11. Create PR

**Show content to user first**, then:

```bash
gh pr create --title "[title]" --body "$(cat <<'EOF'
[body content]
EOF
)" --base [base_branch] --label [labels]
```

## Information Gathering Checklist

Before generating PR, ensure you have:

- [ ] Current branch name
- [ ] Base branch confirmed with user
- [ ] List of commits with types and scopes
- [ ] Files changed summary
- [ ] Task documentation (if exists)
- [ ] Task completion status
- [ ] Test results (must pass)
- [ ] Available labels in repo

## Error Handling

**Missing GitHub CLI**: `brew install gh && gh auth login`

**Incomplete Tasks**: Show status, ask user to complete or proceed anyway.

**Failed Tests**: Show failures, ask user to fix before PR.

**No tasks.md**: Proceed with commit-based PR, generate content from commits only.

## Important Rules

- **NEVER** modify repository files (read-only analysis)
- **ALWAYS** confirm target branch with user
- **ALWAYS** run tests before creating PR
- **ALWAYS** show PR content for approval before creating
- **NEVER** create PR without user confirmation
- **ALWAYS** use HEREDOC for body to preserve formatting

## Related Skills

- **git-commit** - Commit message format and conventions

## References

- `references/pr_templates.md` - Complete PR templates for all types
- `references/conventional_commits.md` - Commit format guide

## When to use this skill

Creates GitHub Pull Requests with automated validation and task tracking. Use when user wants to create PR, open pull request, submit for review, or check if ready for PR. Analyzes commits, validates task completion, generates Conventional Commits title and description, suggests labels. NOTE - for merging existing PRs, use github-pr-merge instead.

## How to use this skill

Refer to the instructions above or standard agent usage for this skill type.
