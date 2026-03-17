---
name: feature-branch-pr
description: Enforce feature work on a dedicated git branch and submission via pull request. Use when implementing any feature, fix, or refactor so work is isolated, reviewed, and merged via PR.
license: MIT
metadata:
  version: "1.0.0"
  workflow: "branch -> implement -> commit -> push -> PR"
---

# Feature Branch + PR Workflow

## Overview

Use a consistent git workflow so every feature/change is done in a branch and submitted as a PR.

## Workflow

### 1. Confirm PR Requirements
- Identify target branch (e.g., `main` or `develop`).
- Ask for branch naming rules if not specified.
- Confirm if a PR template, labels, or issue references are required.

### 2. Create Branch
- Create a new branch before modifying code.
- Auto-pick branch name using phase number + short feature name.
- Use format: `phase-<number>-<short-name>` (e.g., `phase-5-1-scout-llm`).
- If the phase has substeps (e.g., 5.1), include them (e.g., `phase-5-1`).

Example:
```bash
git switch -c phase-<number>-<short-name>
```

### 3. Implement + Commit
- Implement changes and tests on the branch only.
- Follow the repo's commit conventions.
- Keep commits scoped to the feature.

### 4. Push Branch
- Push the branch to origin.

Example:
```bash
git push -u origin feature/<short-slug>
```

### 5. Open PR
- Open a PR targeting the agreed branch.
- Include test results, scope summary, and any required references (issues, docs).
- If a PR template exists, fill it out fully.

### 6. Keep Work in PR Scope
- Do not merge locally.
- Wait for review; address feedback with additional commits on the same branch.

## Notes

- If branch naming conventions or PR requirements are unclear, ask the user before proceeding.
- If the repo uses issue-based workflow, include the issue ID in the branch name and PR title.
