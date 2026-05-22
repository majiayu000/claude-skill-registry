---
name: tdd-obra
description: Test-Driven Development methodology enforcing RED-GREEN-REFACTOR cycle. Use for writing tests first, preventing regression, and ensuring code correctness. Based on obra/superpowers.
version: 1.0.0
category: development
last_updated: 2026-01-19
source: https://github.com/obra/superpowers
related_skills:
  - systematic-debugging
  - writing-plans
  - subagent-driven
---

# Test-Driven Development (TDD) Skill

## Overview

This skill enforces strict test-first development methodology. The core principle: "Write the test first. Watch it fail. Write minimal code to pass." If you didn't watch the test fail, you don't know if it tests the right thing.

## Quick Start

1. **Write one failing test** - Minimal test demonstrating desired behavior
2. **Verify RED** - Run test, confirm it fails (not errors)
3. **Write minimal code** - Just enough to pass
4. **Verify GREEN** - All tests pass
5. **Refactor** - Clean up while maintaining green

## When to Use

- Starting new features or modules
- Fixing bugs (write failing test reproducing bug first)
- Refactoring existing code
- Any production code development
- Code review verification

## Iron Law

**Produce no production code without a failing test first.**

Any code written before tests must be deleted entirely - no exceptions for keeping it as reference material.

## Red-Green-Refactor Cycle

### RED Phase

Write one minimal test demonstrating desired behavior:
- Use clear, descriptive test names
- Test real behavior, not mocks
- One assertion focus per test

### Verify RED (Mandatory)

Run tests and confirm:
- Test fails (not errors)
- Failure message matches expectations
- Failure occurs because feature is missing, not due to typos

### GREEN Phase

Write simplest code passing the test:
- No over-engineering or feature additions
- No refactoring other code
- Implement only what satisfies the test

### Verify GREEN (Mandatory)

Confirm:
- Target test passes
- All existing tests remain passing
- No errors or warnings appear

### REFACTOR Phase

After green only, clean up implementation:
- Remove duplication
- Improve naming
- Extract helpers
- Maintain all passing tests

## Why Tests-After Fails

| Approach | Validates |
|----------|-----------|
| Tests-first | "What should this do?" |
| Tests-after | "What did I build?" |

Tests written after code:
- Pass immediately, proving nothing
- May test the wrong thing
- Verify implementation rather than behavior
- Miss edge cases forgotten during coding
- Never demonstrate the test catching real bugs

## Common Rationalizations (All Invalid)

These are "Red Flags" requiring complete restart with proper TDD:
- "Too simple to test"
- "I'll test after"
- "Already manually tested"
- "Tests slow me down"
- "I know this works"

## Bug Fix Pattern

```
1. Write failing test reproducing the bug
2. Verify test fails for expected reason
3. Implement minimal fix
4. Verify all tests pass
5. Refactor if needed
6. Commit with test and fix together
```

## Verification Checklist

Before completing work:
- [ ] Every function has a test
- [ ] Each test was watched failing first
- [ ] Tests failed for expected reasons
- [ ] Minimal code passes each test
- [ ] All tests pass without warnings
- [ ] Tests employ real code with minimal mocking
- [ ] Edge cases and errors are covered

## Best Practices

### Do

1. Write test name as behavior specification
2. Use AAA pattern: Arrange, Act, Assert
3. Test edge cases explicitly
4. Keep tests independent
5. Run full suite frequently
6. Commit test and implementation together

### Don't

1. Write tests after implementation
2. Test implementation details
3. Use excessive mocking
4. Skip verification steps
5. Batch multiple behaviors in one test
6. Ignore flaky tests

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Test passes immediately | Wrote code first | Delete code, start over with test |
| Test errors instead of fails | Syntax or setup issue | Fix test setup, not production code |
| Tests pass but feature broken | Testing wrong thing | Review test assertions |
| Flaky tests | Async or state issues | Fix test isolation |

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Test-First Rate | 100% | Tests written before code |
| RED Verification | 100% | All tests watched failing |
| Coverage | >80% | Line coverage baseline |
| Critical Path Coverage | 100% | Auth, payments, security |
| Test Independence | 100% | No test order dependencies |

## Related Skills

- [systematic-debugging](../systematic-debugging/SKILL.md) - Debug with methodology
- [writing-plans](../planning/writing-plans/SKILL.md) - Plan implementations
- [subagent-driven](../subagent-driven/SKILL.md) - Structured development

---

## Version History

- **1.0.0** (2026-01-19): Initial release adapted from obra/superpowers
