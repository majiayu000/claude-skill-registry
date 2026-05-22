---
name: code-refactoring-small
description: Refactor overly large code units into smaller, more focused components. Use when code has grown too large or complex.
---

# Code Refactoring: Keep Code Small

Refactor overly large code you just added or extended into smaller, more focused components.

## When to Use This Skill

Use this skill when:
- Functions or methods are too long (typically >50 lines)
- Classes have too many responsibilities
- Files have grown too large or handle multiple concerns
- Code has deeply nested blocks
- After implementing a feature and noticing bloat

## Instructions

### Step 1: Identify the Bloat

Review your recent changes (committed or uncommitted) to find:
- Functions or methods that are too long
- Classes that have too many responsibilities
- Files that have grown too large
- Deeply nested code blocks

### Step 2: Clarify Scope (If Needed)

If the bloat is not obvious, ask the user to clarify which specific code units
they want refactored before proceeding.

### Step 3: Refactor

Once the bloat is identified:
- Extract logical sub-operations into separate functions/methods
- Split large classes following Single Responsibility Principle
- Move related functionality into separate modules/files
- Reduce nesting levels by extracting guard clauses or helper functions
- Ensure each unit does one thing well (UNIX Philosophy)

### Step 4: Verify

After refactoring:
- Run linters and tests if available
- Verify the code still works as expected
- Check that the solution is clearer and more maintainable
- Ensure the refactoring improved readability

## Goal

Break down large, complex code units into smaller, focused components that are:
- Easier to understand
- Easier to test
- Easier to maintain

Each function, class, or file should have a clear, single purpose.
