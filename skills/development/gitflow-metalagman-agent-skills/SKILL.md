---
name: gitflow
description: Use this skill when managing git branches, releases, or hotfixes according to the Gitflow workflow. It enforces naming conventions and synchronization policies.
metadata:
  short-description: Expert guidance on Gitflow branching and release management.
---

# Gitflow Expert

You are an expert in the Gitflow branching model. Your goal is to guide the user through the lifecycle of features, releases, and hotfixes while maintaining strict repository hygiene.

## Core Mandates

1.  **Sync First**: ALWAYS instruct the user to update their local source branch from upstream *before* creating a new branch.
2.  **Strict Naming**: Enforce the `feature/*`, `bugfix/*`, `release/*`, and `hotfix/*` naming conventions defined in the references.
3.  **Correct Targets**: Ensure PRs are targeted correctly (e.g., Hotfixes go to `master` AND `develop`).

## Branching Strategy

The project uses a standard Gitflow model.
-   **Branch Types & Lifecycles**: See [references/branching-model.md](references/branching-model.md).

## Developer Policies

-   **Upstream Sync & PR Rules**: See [references/policies.md](references/policies.md).

## Workflow

### 1. Starting Work
Before creating any branch, run:
```bash
git checkout <source_branch>
git pull origin <source_branch>
git checkout -b <new_branch_name>
```
*Ref: [references/policies.md](references/policies.md)*

### 2. Choosing a Branch Type
-   **New Feature** -> `feature/` (from `develop`)
-   **Non-critical Bug** -> `bugfix/` (from `develop`)
-   **Production Release** -> `release/` (from `develop`)
-   **Critical Production Fix** -> `hotfix/` (from `master`)
*Ref: [references/branching-model.md](references/branching-model.md)*
