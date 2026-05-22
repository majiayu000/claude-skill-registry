---
name: dev-validation-quality-gates
description: Quality standards that must pass before commit
category: validation
---

# Quality Gates

These quality gates must pass before any commit.

## Code Quality Rules

### TypeScript
- [ ] No `any` types without justification
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] Proper type annotations on functions
- [ ] Correct import/export syntax

### Code Style
- [ ] No unused imports or variables
- [ ] No console.log in production code
- [ ] Consistent formatting (prettier)
- [ ] Meaningful variable/function names

### Testing
- [ ] New code has test coverage
- [ ] All existing tests still pass
- [ ] Tests cover edge cases

### Build
- [ ] Bundle size is reasonable
- [ ] No build warnings
- [ ] Production build succeeds

## Server-Authoritative Checks

For multiplayer features:
- [ ] Game logic runs on server
- [ ] Client doesn't trust itself for gameplay
- [ ] Input validation on server
- [ ] Hit detection validated server-side

## Performance Checks

For performance-critical features:
- [ ] No object creation in hot loops
- [ ] Proper use of refs for animation
- [ ] Memory disposal in cleanup
- [ ] Efficient rendering patterns

## Pre-Commit Checklist

Before committing, verify:
- [ ] All feedback loops pass
- [ ] Code follows existing patterns
- [ ] No error suppression
- [ ] Server processes killed (ports freed)
- [ ] Documentation updated if needed
