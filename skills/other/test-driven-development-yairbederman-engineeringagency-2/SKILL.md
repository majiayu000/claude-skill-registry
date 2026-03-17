---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Delete means delete

## Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌───────┐      ┌───────┐      ┌──────────┐               │
│   │  RED  │ ───► │ GREEN │ ───► │ REFACTOR │ ───► (repeat) │
│   └───────┘      └───────┘      └──────────┘               │
│                                                             │
│   Write         Write          Clean up                    │
│   failing       minimal        (stay green)                │
│   test          code                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### RED - Write Failing Test

Write one minimal test showing what should happen.

- Test describes behavior, not implementation
- Test should fail for the right reason (feature missing, not typo)
- Run the test and confirm it fails

### GREEN - Write Minimal Code

Write the minimum code to make the test pass.

- Don't add features the test doesn't require
- Don't optimize
- Just make it pass

### REFACTOR - Clean Up

Improve code quality while keeping tests green.

- Remove duplication
- Improve naming
- Run tests after each change

## Pre-Completion Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

**Never fix bugs without a test.**

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
