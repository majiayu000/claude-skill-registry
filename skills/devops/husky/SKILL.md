---
name: husky
description: Generates Husky Git hooks configuration with pre-commit checks. Creates .husky/pre-commit file for running linting, testing, and formatting before commits.
---

# Husky Skill

## Purpose
Generate Husky configuration for Git hooks with proper pre-commit checks.

## Instructions

### Step 1: Initialize Husky (Already Done During npm install)
The `prepare` script in package.json automatically runs `husky` during `npm install`.
This creates the `.husky/` directory structure.

### Step 2: Create Pre-Commit Hook
**CRITICAL**: After Husky initialization, you MUST create or replace the `.husky/pre-commit` file with the proper content.

**Do NOT rely on auto-generated default** - it creates a default hook with just `npm test` which is insufficient.

## Output
Create the file: `.husky/pre-commit`

## Implementation Steps

1. **Create `.husky/pre-commit` file** with this content:
- Lint to check all code
- Stylelint to check Vue and SCSS files for style issues
- Unit tests to ensure code changes don't break tests
- Lint-staged to auto-fix and format staged files

2. **Make the hook executable**


## Notes
- Pre-commit hook ensures code quality before commits are made
- Husky is initialized automatically via the `prepare` script
- The agent MUST create/replace the pre-commit hook file after initialization
