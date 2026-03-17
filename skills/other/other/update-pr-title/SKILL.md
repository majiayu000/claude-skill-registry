---
name: update-pr-title
description: Updates the PR title based on the changes in the PR using conventional commit format.
allowed-tools: Bash(gh:*), Bash(git:*), Read
---

# Update PR Title Skill

Updates the current PR's title based on analysis of the changes.

## Usage

Invoke with `/update-pr-title` or `/update-pr-title <PR-number>`.

## Workflow

1. **Get PR info**: Run `gh pr view` to get the current PR (or specified PR number)
2. **Get diff**: Run `gh pr diff` to see the changes
3. **Analyze**: Review the diff to understand what changed
4. **Generate title**: Create a conventional commit-style title:
   - `feat(scope): description` for new features
   - `fix(scope): description` for bug fixes
   - `refactor(scope): description` for refactoring
   - `docs(scope): description` for documentation
   - `chore(scope): description` for maintenance
5. **Update**: Run `gh pr edit --title "new title"` to update the PR

## Execution

Run autonomously without user confirmation. Execute all steps and report the result.

### Step 1: Get PR Information

```bash
gh pr view --json number,title,headRefName
```

If a PR number was provided as an argument, use:
```bash
gh pr view <PR-number> --json number,title,headRefName
```

### Step 2: Get the Diff

```bash
gh pr diff
```

### Step 3: Analyze and Update

After analyzing the diff:
1. Determine the primary type of change (feat/fix/refactor/docs/chore)
2. Identify the scope (affected area/package)
3. Write a concise description of the change
4. Update the PR:

```bash
gh pr edit --title "type(scope): description"
```

## Output

Report the old title and new title after updating.
