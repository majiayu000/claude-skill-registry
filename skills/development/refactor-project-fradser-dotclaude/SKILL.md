---
name: refactor-project
description: Run project-wide refactoring with code-simplifier
argument-hint: (no arguments needed - refactors entire project)
allowed-tools: ["Task", "Read", "Write", "Bash(git:*)", "Grep", "Glob"]
user-invocable: true
---

# Refactor Project Command

## Core Principles

- **Fully automated**: Execute project-wide refactoring immediately without confirmation
- **Aggressive refactoring**: Apply thorough improvements across entire codebase
- **Self-discovery**: Agent discovers best practices from skills automatically
- **Cross-file focus**: Emphasize duplication reduction and consistent patterns
- **Git safety net**: Trust git to revert if needed, no preview confirmations

## Context

- This command is for project-wide refactoring across the entire codebase.
- This command executes immediately without preview or confirmation.
- Use git to revert if any issues arise.

## Step 1: Analyze Project Scope

Perform a quick analysis to determine the refactoring scope:

1. **Count code files**:
   - Use Glob to find all code files in the project
   - Filter to focus on source code (exclude node_modules, build outputs, etc.)
   - Group by file type/language

2. **Identify main directories**:
   - List primary source code directories
   - Show project structure overview

3. **Display scope summary** (informational only, no confirmation needed):
   - Total number of files to be refactored
   - Languages/file types detected
   - Main directories involved
   - Note: "Proceeding with project-wide refactoring automatically"

## Step 2: Launch Refactoring Agent

Immediately launch the refactoring agent:

1. Use Task tool with subagent_type="refactor:code-simplifier"
2. Pass:
   - "project-wide scope" indication
   - Emphasis on cross-file duplication reduction and consistent patterns
   - **Aggressive mode flag**: Apply thorough refactoring, remove legacy code
3. The agent will automatically:
   - Load the refactor:best-practices skill
   - Analyze the entire codebase
   - Detect frameworks, libraries, and languages
   - Discover and apply relevant best practices from skill references
   - Emphasize cross-file duplication and consistent patterns
   - **Aggressively refactor**: Remove backwards-compatibility hacks, unused code, rename properly
   - Preserve functionality while improving clarity, consistency, and maintainability
   - Apply Code Quality Standards as defined in the refactor:best-practices skill

## Step 3: Summary

After completion:

1. **Summarize Changes**:
   - Total files refactored (count and percentage of project)
   - What changed and why (categorized by improvement type)
   - Files touched (total count)
   - Best practices applied (which categories/patterns)
   - Cross-file improvements made (deduplication, consistency)
   - Quality standards enforced
   - Legacy code removed
   - Suggested tests to run
   - Recommendation to review changes in logical groups
   - Git rollback command if needed: `git reset --hard HEAD`

## Requirements

- **NO user confirmations** - execute immediately after displaying scope
- **Refactor entire project** - apply improvements across all discovered code files
- **Aggressive refactoring** - remove legacy compatibility code, unused exports, rename improperly named vars
- Follow the refactor:best-practices workflow and references in the refactor plugin skills
- Let the agent self-discover best practices from skills
- Preserve functionality while improving clarity, consistency, and maintainability
- Emphasize cross-file duplication reduction and consistent patterns
- Apply Code Quality Standards as defined in the refactor:best-practices skill
