---
name: refactoring-code
description: Improve code structure without changing behavior. Use when code is hard to read, modify, or test. Covers Extract Method, Rename, and other safe refactorings.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Refactoring Code

## The Refactoring Hat

When refactoring, you change **structure** without changing **behavior**. Always have tests passing before and after.

## Workflows

- [ ] **Tests Green**: Ensure all tests pass before starting
- [ ] **Analyze**: Use Grep to understand dependencies
- [ ] **Small Steps**: Make one small change at a time
- [ ] **Verify Usages**: Use Grep to find all usages before changes
- [ ] **Commit Often**: Commit after each successful refactoring
- [ ] **Tests Green**: Verify tests still pass after each change

## Common Refactorings

### Extract Method
When a code block does one thing, extract it to a named method.

1. Use Grep to verify extraction won't break callers
2. Extract the method
3. Run tests

### Rename for Clarity
Names should reveal intent.

1. Use Grep to find ALL usages
2. Use Edit with replace_all for codebase-wide rename
3. Verify no missed references

### Remove Dead Code
1. Use Grep to verify code is unused
2. If zero references, safe to remove
3. If references exist, trace to understand usage

## Code Smells to Address

- **Long Method**: Extract smaller methods
- **Long Parameter List**: Introduce parameter object
- **Duplicate Code**: Extract to shared function (use Grep to locate duplicates)
- **Feature Envy**: Move method to the class it uses most
- **Data Clumps**: Group related data into objects
- **Primitive Obsession**: Replace primitives with value objects

## Safety Rules

1. Never refactor and add features simultaneously
2. **Always use Grep to find all usages before removing/renaming**
3. Run tests after every change
4. Use targeted Edit operations instead of broad find-replace
5. Commit working states frequently
