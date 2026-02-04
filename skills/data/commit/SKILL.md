---
name: commit
description: This skill should be used when the user requests "commit", "git commit", "create commit", or wants to commit staged/unstaged changes following conventional commits format
user-invocable: true
allowed-tools: ["Bash(git:*)", "Read", "Write", "Glob", "AskUserQuestion", "Skill"]
argument-hint: "[no arguments needed]"
model: haiku
version: 0.2.0
---

## Background Knowledge

**Format**: `<type>[scope]: <description>` + mandatory body + optional footers

- **Title**: ALL LOWERCASE, <50 chars, imperative mood, no period. Add `!` for breaking changes
- **Types**: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`, `style`
- **Body** (REQUIRED): Bullet summary (`- ` prefix, imperative verbs) + explanation paragraph. ≤72 chars/line
- **Footer**: `Co-Authored-By` REQUIRED; optional `Closes #123`, `BREAKING CHANGE: ...`

See `references/format-rules.md` for complete specification and examples.

## Phase 1: Configuration Verification

**Goal**: Load project-specific git configuration and valid scopes.

**Actions**:
1. **FIRST**: Read `.claude/git.local.md` to load project configuration
2. If file not found, **load `git:config-git` skill** using the Skill tool to create it
3. Extract valid scopes from `scopes:` list in YAML frontmatter
4. Store these scopes for validation in Phase 3 and Phase 5

## Phase 2: Safety Validation

**Goal**: Perform safety checks before committing.

**Actions**:
1. Detect sensitive files (credentials, secrets, .env files)
2. Warn about large files (>1MB) and large commits (>500 lines)
3. Use `AskUserQuestion` tool for confirmation if issues found

## Phase 3: Change Analysis

**Goal**: Identify logical units of work and infer commit scopes.

**Actions**:
1. Run `git diff --cached` and `git diff` to get code differences (MUST NOT traverse files directly)
2. Analyze diff to identify coherent logical units
3. Infer scope(s) from file paths and changes using the valid scopes loaded in Phase 1
4. If inferred scope not in the valid scopes list, **load `git:config-git` skill** using the Skill tool to update configuration

## Phase 4: AI Code Quality Check

**Goal**: Remove AI-generated slop before committing.

**Actions**:
1. Run `git diff main...HEAD` to compare against main branch
2. Remove AI patterns: extra comments, unnecessary defensive checks, `any` casts, inconsistent style
3. Ensure changes follow project's established patterns

## Phase 5: Commit Creation

**Goal**: Create atomic commits following Conventional Commits format.

**Actions** (repeat for each logical unit):
1. Draft commit message per `references/format-rules.md`
2. Validate: title <50 chars lowercase imperative; body has bullets + explanation paragraph; footer has `Co-Authored-By`
3. Stage relevant files and create commit
