---
name: code-simplify
description: Simplify and refine recently modified code for clarity, consistency, and maintainability while preserving all functionality. Use this skill when asked to simplify code, clean up recent changes, refine implementations, reduce complexity, or improve readability of code that was just written or modified. Focuses on recently touched code unless explicitly directed to a broader scope.
---

# Code Simplification

Enhance code clarity, consistency, and maintainability while preserving exact functionality. Prioritize readable, explicit code over compact solutions.

## Scope

Focus only on recently modified code unless explicitly instructed otherwise. Use `git diff` or `git diff --cached` to identify what changed. Read the project's AGENTS.md or CLAUDE.md for project-specific conventions and apply them consistently.

## Simplification Principles

**Reduce complexity**
- Flatten unnecessary nesting
- Eliminate redundant code and premature abstractions
- Consolidate related logic
- Remove comments that describe obvious code

**Improve clarity**
- Use clear, descriptive variable and function names
- Avoid nested ternary operators - prefer switch statements or if/else chains for multiple conditions
- Choose explicit code over clever one-liners
- Clarity over brevity - three similar lines beats a confusing abstraction

**Apply project standards**
- Follow patterns established in AGENTS.md/CLAUDE.md
- Match existing naming conventions
- Use established abstractions where appropriate

## What NOT to Do

- Change what the code does - only change how it does it
- Create overly clever solutions that are hard to understand
- Combine too many concerns into single functions
- Remove helpful abstractions that improve organization
- Prioritize "fewer lines" over readability
- Make code harder to debug or extend
- Over-simplify to the point of reducing maintainability

## Process

1. Identify recently modified code sections via git
2. Read AGENTS.md/CLAUDE.md for project conventions
3. Analyze for opportunities to improve clarity and consistency
4. Apply refinements that preserve all functionality
5. Verify the result is simpler and more maintainable
