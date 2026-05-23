---
name: standardizing-git-workflow
description: Rules for version control and commit messages. Use for every code submission.
---

# Git Commit and Branching

## When to use this skill
- Before running `git commit`.
- When starting a new feature.

## Committing Rules
- **Format**: `type: description` (e.g., `feat: add tour booking form`).
- **Types**:
    - `feat`: New feature.
    - `fix`: Bug fix.
    - `style`: UI/CSS changes without logic.
    - `refactor`: Code cleanup/structure change.
    - `docs`: Documentation updates.
- **The "Why" Rule**: In the commit body, explain *why* the change was made if the reason isn't obvious from the title.

## Branching Logic
- `main`: Production-ready code.
- `feat/feature-name`: For new features.
- `fix/bug-name`: For specifically fixing bugs.

## Instructions
- **Small Commits**: Commit one logical change at a time. Avoid 100-file "Work in progress" commits.
