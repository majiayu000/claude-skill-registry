---
name: git-workflow
description: "Git workflow rules for git-review: branch naming, commit format, merge policy, review gate enforcement, and security rules. Use when creating branches, committing, or preparing merges."
---

# Git Workflow

## No Ticket, No Work (ENFORCED by hook)

Every piece of work MUST have a Linear ticket before starting:
- Create the ticket in Linear FIRST
- Create a branch referencing the ticket ID
- The `enforce-ticket.sh` hook blocks prompts on branches without ticket IDs
- This applies to ALL work: features, fixes, docs, chores

## Branch Naming (ENFORCED by hook)

Format: `<type>/<ticket-id>-<short-description>`

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

Examples:
- `feat/eng-4-line-level-review`
- `docs/eng-5-developer-tooling`
- `fix/eng-6-parser-infinite-loop`

Rules:
- Every branch MUST have a Linear ticket
- Branch name MUST start with a type prefix
- Branch name MUST contain the ticket ID (e.g., `eng-4`)
- Use lowercase with hyphens

## Commit Message Format

```
feat(ENG-X): short description of what changed

- Bullet points explaining key changes
- Reference the ticket ID in the prefix
```

Prefixes: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

## Merge Policy

- NEVER commit or push directly to main (enforced by hook)
- NEVER merge without a completed git-review from the user (enforced by hook)
- Merge to main via PR after tests pass AND user has reviewed all hunks via `git-review`
- Merge BEFORE starting dependent work (if ENG-4 needs ENG-3, merge ENG-3 first)
- One branch per Linear ticket — no stacking features on the same branch
- Short-lived branches (1-2 days max)

## Review Gate (ENFORCED by hook)

Every PR requires the user to review changes with git-review first:
1. Agent finishes work, runs tests, pushes branch
2. User runs `git-review main..<branch>` to review all hunks
3. User marks all hunks as reviewed in the TUI
4. `git-review gate check` passes (all hunks reviewed)
5. Only then can a PR be created and merged

Agents MUST NOT create PRs or merge themselves. The user does both after their review.

## Worktrees for Parallel Agents

- Each agent works in its own worktree: `.trees/<ticket-id>/`
- Prevents file conflicts between parallel agents
- Clean up worktrees after merging: `git worktree remove .trees/<ticket-id>`

## What NOT to Do

- NEVER stack features on one branch (one ticket = one branch)
- NEVER branch off an unmerged feature branch (branch from main only)
- NEVER force push without explicit user approval
- NEVER work on main — create a feature branch first

## Security Rules

- Sanitize all file paths to prevent directory traversal
- Validate git refs before passing to shell commands
- Never pass unsanitized user input to `std::process::Command`
- Never hardcode API keys or credentials

## Pre-Commit Hook Awareness

- `cargo fmt` runs automatically on commit (if configured)
- After any code change, run `cargo fmt` before `git diff` to see true changes
- Hook scripts (.claude/hooks/) are NOT auto-formatted — edit carefully
- The `protect-hooks.sh` hook prompts before any hook modification
