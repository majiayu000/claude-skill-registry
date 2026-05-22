---
name: test-pattern-detector
description: Delegates test pattern detection to a lightweight agent. Use when you need to understand existing test conventions without loading test files into context.
---

# Test Pattern Detector Skill

This skill delegates test pattern detection to a specialized lightweight agent, keeping your context lean.

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **Writing new tests**: You need to match existing test naming and structure conventions
2. **Setting up test files**: You need to know the correct imports, setup/teardown patterns
3. **Choosing test location**: You need to know if tests go alongside source or in separate directory
4. **Mocking patterns**: You need to understand how the project handles mocks and fixtures
5. **Test framework usage**: You need to see how describe/it/test blocks are structured

## Why Use This Skill?

**Without this skill**: You would read 2-3 full test files (100-300 lines each) to understand patterns.

**With this skill**: The test-pattern-detector agent (haiku model) samples test files and returns a concise 40-60 line summary.

**Context savings**: 60-80% reduction in test-pattern-related context usage.

## Invocation

When you need test pattern information, invoke the agent:

```
Task(subagent_type="test-pattern-detector", prompt="
Analyze testing patterns in this project.
")
```

For specific language focus:

```
Task(subagent_type="test-pattern-detector", prompt="
Analyze testing patterns in this project.
Language: Python
Directory: tests/
")
```

## What test-pattern-detector Will Do

The agent will:

1. **Find test files**: Locate *.test.ts, test_*.py, *_test.go, etc.
2. **Sample 3 files**: Select representative unit, integration, and setup-heavy tests
3. **Read first 80 lines**: Extract patterns without full file context
4. **Identify conventions**: Naming, structure, fixtures, mocking, imports
5. **Return summary**: Concise structured output with example patterns

## Expected Output

You will receive a structured summary like:

```
## Test Pattern Summary

**Framework**: Jest 29
**Assertion Style**: expect() with matchers

**Naming Conventions**:
- Files: `*.test.ts` (co-located with source)
- Functions: `it('should [action] when [condition]')`
- Describe blocks: Yes, `describe('[ComponentName]', () => {})`

**Structure**:
- Location: Alongside source
- Setup: `beforeEach()` for component mounting
- Teardown: `afterEach(() => cleanup())`

**Fixtures & Mocking**:
- Fixtures: Factory functions in `tests/fixtures/`
- Mocking: `jest.mock()` for modules

**Import Pattern**:
```typescript
import { render, screen } from '@testing-library/react';
import { createMockUser } from '../fixtures/user';
```

**Test Function Pattern**:
```typescript
describe('UserProfile', () => {
  it('should display user name', () => {
    render(<UserProfile user={createMockUser()} />);
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
```
```

## Example Usage

**Scenario**: You need to write tests for a new UserService.

**Without skill**: Read 3 existing test files (450 lines total) to understand conventions.

**With skill**:
```
Task(subagent_type="test-pattern-detector", prompt="Analyze testing patterns in this project.")
```

**Result**: You know the naming convention, import pattern, and fixture usage in 50 lines of context.

## Do NOT Invoke When

- You already know the test patterns from earlier in the conversation
- The user has explicitly described how tests should be written
- You're modifying an existing test file (read that file directly)
- The project has no existing tests (nothing to detect)

## Consumers

This skill is particularly useful for:
- `test-creator` - Writing new tests that match conventions
- `bdd-test-runner` - Validating test infrastructure setup
- `coder` - Adding tests alongside new implementations
- `refactorer` - Ensuring refactored code has matching test patterns
