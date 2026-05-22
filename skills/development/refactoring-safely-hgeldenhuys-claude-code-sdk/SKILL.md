---
name: refactoring-safely
description: Safe refactoring strategies with Claude Code - large-scale changes, validation, rollback
version: 1.0.0
author: Claude Code SDK
tags: [refactoring, safety, large-scale, validation]
---

# Refactoring Safely

Safe refactoring strategies for Claude Code. Small steps, validated changes, easy rollback.

## Quick Reference

| Principle | Description |
|-----------|-------------|
| Test First | Ensure tests pass before refactoring |
| Small Steps | One change type at a time |
| Commit Often | Create savepoints for rollback |
| Verify Each Step | Run tests after each change |
| No Behavior Change | Refactoring preserves functionality |

## The Safe Refactoring Loop

```
1. Verify tests pass (baseline)
2. Make ONE small change
3. Run tests
4. If tests pass: commit
5. If tests fail: revert and retry smaller
6. Repeat
```

## Before Any Refactoring

### Prerequisites Checklist

- [ ] All tests passing
- [ ] Working directory clean (`git status`)
- [ ] On feature branch (not main)
- [ ] Tests cover the code being refactored
- [ ] Understand what the code does

### Create Baseline

```bash
# Ensure clean state
git status

# Run full test suite
bun test

# Create savepoint
git commit -m "chore: checkpoint before refactoring"
```

## Common Refactoring Patterns

### Extract Function/Method

**When:** Duplicate code, long functions, complex conditionals

```typescript
// Before: Long function with embedded logic
function processOrder(order: Order) {
  // 20 lines of validation
  // 30 lines of processing
  // 10 lines of notification
}

// After: Extracted functions
function processOrder(order: Order) {
  validateOrder(order);
  executeOrder(order);
  notifyCustomer(order);
}
```

**Safe Steps:**
1. Identify code to extract
2. Create new function with parameters
3. Copy code to new function
4. Replace original with function call
5. Run tests
6. Commit

### Rename Symbol

**When:** Name doesn't reflect purpose, inconsistent naming

```typescript
// Before
const d = new Date();

// After
const createdAt = new Date();
```

**Safe Steps:**
1. Use IDE/editor rename refactoring if available
2. Or use search-and-replace with word boundaries
3. Check all references updated
4. Run tests
5. Commit

### Move File/Module

**When:** Wrong directory, reorganizing structure

**Safe Steps:**
1. Update imports in the file being moved
2. Move file to new location
3. Update all import statements referencing the file
4. Run tests
5. Commit

### Inline Function

**When:** Function does too little, unnecessary indirection

```typescript
// Before
function isAdult(age: number) {
  return age >= 18;
}
const canVote = isAdult(user.age);

// After
const canVote = user.age >= 18;
```

**Safe Steps:**
1. Verify function has single call site (or few)
2. Copy function body to call site
3. Adjust variables as needed
4. Remove unused function
5. Run tests
6. Commit

## Workflow: Basic Refactoring

### Prerequisites
- [ ] Tests exist and pass
- [ ] Clean git state
- [ ] On feature branch

### Steps

1. **Establish Baseline**
   - [ ] Run `bun test` - all pass
   - [ ] Create checkpoint commit

2. **Plan Changes**
   - [ ] Identify what to refactor
   - [ ] Choose ONE refactoring type
   - [ ] List affected files

3. **Execute**
   - [ ] Make the change
   - [ ] Run tests immediately
   - [ ] Fix any failures

4. **Validate**
   - [ ] All tests pass
   - [ ] Manual smoke test if needed
   - [ ] No behavior changes

5. **Commit**
   - [ ] Descriptive commit message
   - [ ] Reference issue if applicable

### Validation
- [ ] Tests pass before and after
- [ ] Same functionality preserved
- [ ] Code is cleaner/clearer

## Test Coverage Considerations

### Before Refactoring

```bash
# Check coverage for files you'll touch
bun test --coverage

# Identify untested code
# Add tests for uncovered critical paths
```

### Minimum Coverage for Safety

| Risk Level | Minimum Coverage |
|------------|------------------|
| Critical business logic | 90%+ |
| General application code | 70%+ |
| Utility functions | 80%+ |
| UI components | 60%+ |

### Adding Tests First

If coverage is low:

1. Write characterization tests (capture current behavior)
2. Don't fix bugs during refactoring
3. Document unexpected behavior for later

```typescript
// Characterization test - captures current behavior
test('processOrder returns null for empty order', () => {
  // This might be a bug, but document it first
  expect(processOrder({})).toBeNull();
});
```

## Rollback Strategies

### Git-Based Rollback

```bash
# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert specific commit (creates new commit)
git revert <commit-hash>
```

### Stash-Based Recovery

```bash
# Save current work
git stash push -m "refactoring attempt 1"

# Try different approach
# ...

# If new approach fails, restore stash
git stash pop
```

### Branch-Based Safety

```bash
# Create experimental branch
git checkout -b refactor/extract-auth-module

# Do refactoring work
# ...

# If successful, merge to feature branch
git checkout feature/my-feature
git merge refactor/extract-auth-module

# If failed, just delete the branch
git branch -D refactor/extract-auth-module
```

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Multiple changes at once | Hard to identify what broke | One change type at a time |
| Skipping tests | Silent regressions | Always run tests |
| No commits | Lost progress | Commit after each successful change |
| Refactoring on main | Risky deploys | Always use feature branch |
| Changing behavior | Bugs introduced | Pure refactoring only |
| No baseline | Can't verify preservation | Establish baseline first |

## When to Stop Refactoring

- [ ] Tests are failing and you can't fix them quickly
- [ ] You're changing behavior, not just structure
- [ ] The refactoring scope is growing uncontrollably
- [ ] You're unsure what the code should do
- [ ] You've been refactoring the same area for hours

**Stop, commit what works, and reassess.**

## Decision Guide: Which Refactoring?

| Symptom | Refactoring |
|---------|-------------|
| Duplicate code | Extract function |
| Long function (>30 lines) | Extract function |
| Long parameter list | Introduce parameter object |
| Feature envy | Move method |
| Data clumps | Extract class |
| Primitive obsession | Replace with value object |
| Switch statements | Replace with polymorphism |
| Deep nesting | Extract function, early return |
| Comment explaining code | Extract function with good name |
| Unclear variable name | Rename |

## Reference Files

| File | Contents |
|------|----------|
| [STRATEGIES.md](./STRATEGIES.md) | Extract, inline, rename, move patterns |
| [LARGE-SCALE.md](./LARGE-SCALE.md) | Large-scale refactoring across files |
| [VALIDATION.md](./VALIDATION.md) | Test coverage, validation, rollback |
