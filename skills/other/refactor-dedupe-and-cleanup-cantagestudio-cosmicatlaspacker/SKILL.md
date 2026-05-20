---
name: refactor-dedupe-and-cleanup
description: "[Code Quality] Removes code duplication and cleans up dead code. Use to eliminate copy-paste code, consolidate similar logic, and remove unused code paths."
---

# Refactor: Dedupe and Cleanup

Eliminate redundancy and remove dead code.

## Deduplication Patterns

### 1. Extract Common Method
Move duplicated logic to shared function.

### 2. Template Method Pattern
Abstract common structure, vary details.

### 3. Consolidate Conditional Expression
Combine conditions with same result.

## Dead Code Removal

### Types to Remove
1. Unreachable code - after return/throw
2. Unused variables - declared but never read
3. Unused functions - never called
4. Commented code - use git history instead
5. Unused imports - clutters namespace

### Safe Removal Process
1. Search for all references
2. Check for reflection/dynamic usage
3. Remove in small commits
4. Run full test suite