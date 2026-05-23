---
name: start-hotfix
allowed-tools: Bash(git:*), Read, Write, Skill
description: Start new hotfix branch
model: haiku
argument-hint: [hotfix-name]
user-invocable: true
---

## Your Task

1. **Load the `gitflow:gitflow-workflow` skill** using the `Skill` tool to access GitFlow workflow capabilities.
2. Gather context: current branch, existing hotfix branches, latest tag, version files.
3. Normalize the provided hotfix name from `$ARGUMENTS` to `$HOTFIX_NAME` using the normalization procedure defined in the `gitflow-workflow` skill references (strip `hotfix/` prefix if present, convert to kebab-case).
4. Identify production base branch for the active workflow (usually `main` for Classic GitFlow, or `production` for GitLab Flow).
5. Create or resume `hotfix/$HOTFIX_NAME` from the production base branch.
6. Increment patch version (if the repo uses SemVer + tags) and update version files.
7. Push the branch to origin if newly created.
