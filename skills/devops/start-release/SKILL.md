---
name: start-release
allowed-tools: Bash(git:*), Read, Write
description: Start new release branch
model: haiku
argument-hint: <version>
user-invocable: true
---

## Phase 1: Start Release

**Goal**: Create release branch using git-flow-next CLI.

**Actions**:
1. Run `git flow release start $ARGUMENTS`
2. Update version in project files (package.json, Cargo.toml,
   VERSION, etc.)
3. Commit version bump: `chore: bump version to $ARGUMENTS`
   with `Co-Authored-By` footer
4. Push the branch: `git push -u origin release/$ARGUMENTS`

**Note**: CHANGELOG.md is updated during finish-release, not here.
