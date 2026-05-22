---
name: merge
description: Intelligently merge branches with context-aware conflict resolution
allowed-tools: Bash(git :*), Bash(gh :*), Read, Edit, MultiEdit, Task
argument-hint: <branch-name>
---

# Merge

Merge branches intelligently by understanding feature context and resolving conflicts efficiently.

## Context

- Current branch: !`git branch --show-current`
- Working tree status: !`git status --short`
- Target branch: $1
- Recent commits: !`git log --oneline -5`

## Workflow

1. **CONTEXT GATHERING**:
   - `git branch --show-current` to identify current branch
   - `git status` to ensure clean working tree
   - **CRITICAL**: Abort if uncommitted changes exist

2. **FEATURE ANALYSIS**:
   - Search PR with `gh pr list --head <branch-name>`
   - Get PR details with `gh pr view <number> --json title,body,files`
   - Use Task agents to gather context from PR/issue descriptions

3. **MERGE ATTEMPT**:
   - `git fetch origin <branch-name>`
   - `git merge origin/<branch-name> --no-commit`
   - Check status with `git status --porcelain`

4. **CONFLICT DETECTION**:
   - Clean merge: `git commit` with descriptive message
   - Conflicts: Parse `git diff --name-only --diff-filter=U`

5. **SMART RESOLUTION**: For each conflicted file:
   - Read file to understand conflict markers
   - Apply resolution based on context:
     - **Feature additions**: Keep both if non-overlapping
     - **Bug fixes**: Prefer incoming if fixing known issue
     - **Refactors**: Analyze intent and merge carefully
   - Use MultiEdit to resolve all conflicts
   - **STOP**: If >10 files conflicted, ask user

6. **VERIFICATION**:
   - `git diff --cached` to review changes
   - Check no conflict markers remain: `grep -r "<<<<<<< HEAD"`
   - `git add -A` and commit

## Conflict Resolution by Type

- **package.json**: Merge dependencies, prefer higher versions
- **Config files**: Combine settings unless mutually exclusive
- **Source code**: Use PR/issue context to understand intent
- **Tests**: Keep all tests unless duplicates
- **Imports**: Merge all, deduplicate

## Rules

- ALWAYS gather context before merging
- NEVER blindly accept theirs/ours without analysis
- ABORT if conflicts exceed 10 files
- Max 3 resolution attempts per file
- If stuck: `git merge --abort` and report blockers
