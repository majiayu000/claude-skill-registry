---
name: ship
description: Build, commit, push & version bump workflow - automates the complete release cycle
tags: [workflow, git, automation, release]
---

# /ship - Build, Commit, Push & Version Bump

Automates the complete ship workflow for ccboard:

## Workflow Steps

1. **Build Verification**
   - Run `cargo build --all` to ensure compilation succeeds
   - Run `cargo clippy --all-targets` to catch warnings
   - Run `cargo test --all` to verify tests pass
   - If any step fails, stop and report errors

2. **Stage Changes**
   - Run `git status` to show current state
   - Stage all changes with `git add -A`
   - Show what will be committed with `git diff --cached --stat`

3. **Commit**
   - Write a conventional commit message based on the changes:
     - `feat:` for new features
     - `fix:` for bug fixes
     - `refactor:` for refactoring
     - `docs:` for documentation
     - `chore:` for maintenance
   - Commit format: `<type>: <description>`
   - Add Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

4. **Version Bump** (optional)
   - Check if Cargo.toml version needs bumping
   - If user confirms, update version in all workspace crates
   - Amend the commit with version bump

5. **Push**
   - Push to current branch with `git push`
   - If branch has no upstream, use `git push -u origin <branch>`

6. **Summary**
   - Report what was shipped:
     - Commit hash
     - Branch name
     - Files changed
     - Version (if bumped)

## Usage

```bash
# Basic usage - ship current changes
/ship

# With version bump
/ship bump

# Dry run - show what would be done
/ship --dry-run
```

## Safeguards

- Always run full build + test suite before committing
- Never force push
- Never skip hooks (no --no-verify)
- Show clear summary of what will be committed before proceeding
- Fail fast on any build/test error

## Expected Outcome

All changes committed, tested, and pushed to remote with proper conventional commit message.
