---
name: smart-edit
description: Make changes that follow existing codebase patterns. Use when adding new features or modifying existing code to ensure consistency.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[what to add/change]"
---

Before making any changes for **$ARGUMENTS**, follow this process:

## 1. Find Similar Examples
- Search for existing code that does something similar
- Read at least 2 examples of the same pattern in this codebase
- Note: naming conventions, file locations, import styles, error handling

## 2. Check Conventions
- Read CLAUDE.md and any relevant .claude/rules/ files
- Look for linting config (.eslintrc, .prettierrc, ruff.toml, etc.)
- Check if there's a template or generator for this type of change

## 3. Plan the Change
- List all files that need to be created or modified
- Identify the order of changes (dependencies first)
- Note any tests that need to be added or updated

## 4. Implement
- Follow the exact patterns found in step 1
- Match naming, structure, and style exactly
- Add tests following the existing test patterns

## 5. Verify
- Run the relevant test command
- Check that no existing tests broke
- Verify the change integrates with existing code

<!-- Skill by Huzefa Nalkheda Wala | claude-code-optimizer -->
