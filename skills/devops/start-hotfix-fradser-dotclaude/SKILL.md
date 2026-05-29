---
name: start-hotfix
allowed-tools: Bash(git:*), Read, Write
description: Start new hotfix branch
model: haiku
argument-hint: <version>
user-invocable: true
---

## Phase 1: Start Hotfix

**Goal**: Create hotfix branch using git-flow-next CLI.

**Actions**:
1. Run `git flow hotfix start $ARGUMENTS`
2. Update version in project files (package.json, Cargo.toml,
   VERSION, etc.)
3. Commit version bump: `chore: bump version to $ARGUMENTS`
   with `Co-Authored-By` footer
4. Push the branch: `git push -u origin hotfix/$ARGUMENTS`
