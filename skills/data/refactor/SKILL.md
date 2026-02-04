---
name: refactor
description: Refactor code with code-simplifier
argument-hint: [files-or-directories-or-semantic-query]
allowed-tools: ["Task", "Read", "Bash(git:*)", "Grep", "Glob"]
user-invocable: true
---

# Refactor Command

Execute automated refactoring for $ARGUMENTS using `refactor:code-simplifier` agent.

## Phase 1: Determine Target Scope
**Goal**: Identify files to refactor based on arguments or session context.

**Actions**:
1. If arguments provided: verify as file/directory paths using Glob
2. If paths exist: use them directly as refactoring scope
3. If paths don't exist: treat arguments as semantic query, search codebase with Grep
4. If no arguments: run `git diff --name-only` to find recently modified code files
5. If no recent changes found: inform user and exit without refactoring

See `references/scope-determination.md` for search strategies and edge cases.

## Phase 2: Launch Refactoring Agent
**Goal**: Execute `refactor:code-simplifier` agent with aggressive mode enabled.

**Actions**:
1. Launch `refactor:code-simplifier` agent with target scope and aggressive mode flag
2. Pass scope determination method (paths, semantic query, or session context)
3. Agent auto-loads `refactor:best-practices` skill and applies language-specific patterns

See `references/agent-configuration.md` for detailed Task parameters.

## Phase 3: Summary
**Goal**: Report comprehensive summary of changes.

**Actions**:
1. Report total files refactored and changes categorized by improvement type
2. List best practices applied and legacy code removed
3. Suggest tests to run and provide rollback command: `git checkout -- <files>`

See `references/output-requirements.md` for detailed summary format.

## Requirements

- Execute immediately without user confirmation
- Refactor ALL matching files when semantic search returns multiple results
- Direct users to `/refactor-project` for project-wide scope
