---
name: start-feature
allowed-tools: Bash(git:*), Read, Skill
description: Start new feature branch
model: haiku
argument-hint: [feature-name]
user-invocable: true
---

## Your Task

1. **Load the `gitflow:gitflow-workflow` skill** using the `Skill` tool to access GitFlow workflow capabilities.
2. Gather context: current branch, existing feature branches, git status.
3. Normalize the provided feature name from `$ARGUMENTS` to `$FEATURE_NAME` using the normalization procedure defined in the `gitflow-workflow` skill references (strip `feature/` prefix if present, convert to kebab-case).
4. Identify base branch for the active workflow (usually `develop` for Classic GitFlow, or `main` for GitHub Flow).
5. Create or resume `feature/$FEATURE_NAME` from the base branch.
6. Push the branch to origin if newly created.
