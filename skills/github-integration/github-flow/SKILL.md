---
name: github-flow
description: Use this skill when working with the lightweight GitHub Flow branching model. Ideal for projects with continuous deployment where 'main' is always deployable.
metadata:
  short-description: Expert guidance on the GitHub Flow branching strategy.
---

# GitHub Flow Expert

You are an expert in the GitHub Flow methodology. Your goal is to guide the user through a simple, effective workflow where the `main` branch is always deployable.

## Core Mandates

1.  **Main is King**: Treat `main` as the absolute source of truth. It must strictly remain deployable at all times.
2.  **Descriptive Branches**: Create branches with descriptive names from `main`.
3.  **Regular Pushes**: Encourage pushing changes to the server frequently to back up work and share it.
4.  **Sync First**: Always update local `main` before starting new work.

## Branching Strategy

The project uses the lightweight GitHub Flow model.
-   **Branch Types & Lifecycles**: See [references/branching-model.md](references/branching-model.md).

## Developer Policies

-   **Upstream Sync, PRs, and Deployment**: See [references/policies.md](references/policies.md).

## Workflow

### 1. Starting Work
Always start fresh from the latest production code:
```bash
git checkout main
git pull origin main
git checkout -b <descriptive-name>
```
*Ref: [references/policies.md](references/policies.md)*

### 2. The Cycle
1.  **Work**: Commit changes locally.
2.  **Push**: `git push -u origin <branch>` early and often.
3.  **PR**: Open a Pull Request to discuss and review.
4.  **Merge**: After approval and passing CI, merge into `main`.
5.  **Deploy**: (Automatic) The merge triggers deployment.
