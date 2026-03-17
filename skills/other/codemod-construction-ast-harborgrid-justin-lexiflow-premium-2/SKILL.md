---
name: codemod-construction-ast
description: Automate large-scale codebase refactoring using AST transformations on React code.
---

# Codemod Construction with ASTs

## Summary
Automate large-scale codebase refactoring using AST transformations on React code.

## Key Capabilities
- Parse React syntax (JSX) into manipulate ASTs (jscodeshift).
- Write robust transforms for prop renaming and component restructuring.
- Update imports and dependencies programmatically.

## PhD-Level Challenges
- Handle diverse coding styles and formatting preservation.
- Implement complex logic for hook migration (Class to Function).
- Verify AST transform correctness across the entire repo.

## Acceptance Criteria
- Deliver a codemod script for a specific refactor task.
- Apply the codemod successfully to the codebase.
- Provide unit tests for the transformation logic.
