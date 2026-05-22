---
name: git-flow
description: Git branching strategy, commit conventions, and merge workflow. Use when creating branches, writing commit messages, merging, or planning git operations.
---

# Git Flow — Skill

## Purpose

Enforce consistent git practices across all phases — planning, implementation, and validation.

## When to Use

- Creating or naming a branch
- Writing a commit message
- Merging work back to a base branch
- Planning implementation steps that involve git operations

## Branching Conventions

1. **Avoid direct commits to `main` when possible.** Prefer feature/fix branches for isolated work.
2. **Branch naming**: `feature/<short-kebab-description>` for features, `fix/<short-kebab-description>` for fixes.
3. **Branch from `main`**.
4. **One logical task per branch.** Do not mix unrelated changes.

## Commit Conventions

1. **Format**: `type(scope): subject`
   - `type`: feat, fix, refactor, test, docs, chore
   - `scope`: module or component name (e.g., `router`, `handler`, `timeout`)
   - `subject`: imperative mood, lowercase, no period, under 72 characters
2. **One logical change per commit.** Every commit must leave the codebase runnable.
3. **Include traceability**: Add `Fulfills: REQ-XX-NNN` in the commit body when the commit completes a requirement.
4. **Push after every commit.** The remote is backup and audit trail.

## Merge Conventions

1. **Merge with `--no-ff`** to preserve feature branch history.
2. **Delete the feature branch** after a successful merge.
3. **Verify tests pass** before merging.

## Pre-Commit Self-Check

1. Run `git diff --staged` and review every changed line.
2. Confirm no debug prints, commented-out code, or TODOs remain.
3. Confirm the commit message accurately describes the change.
4. Confirm the code runs without errors.

## Quality Checklist

- [ ] Branch name follows `feature/<name>` or `fix/<name>` convention
- [ ] Each commit has one logical change
- [ ] Commit messages follow `type(scope): subject` format
- [ ] Commit body includes `Fulfills: REQ-XX-NNN` where applicable
- [ ] All commits pushed to remote
- [ ] Feature branch merged with `--no-ff`
- [ ] Feature branch deleted after merge
