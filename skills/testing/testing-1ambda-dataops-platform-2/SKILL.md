---
name: testing
description: Comprehensive testing strategies including TDD, unit, integration, E2E, and property-based testing. Ensures code quality and prevents regressions. Use when writing tests, implementing features test-first, or improving coverage.
---

# Testing

Testing strategies for code quality and regression prevention.

## When to Use

- Implementing features (test-first)
- Fixing bugs (reproduce with test)
- Improving test coverage
- Refactoring safely

## MCP Workflow

```
# 1. Find existing test patterns
serena.search_for_pattern("test|spec|describe", relative_path="test/")

# 2. Check test utilities
serena.get_symbols_overview(relative_path="test/support/")

# 3. Find similar tests
serena.find_symbol("*Test", depth=1, include_body=False)

# 4. Framework testing patterns
context7.get-library-docs("<testing-framework>", topic="testing")
```

## Test Pyramid

```
       /\
      /E2E\        Few, slow, high confidence
     /------\
    /Integration\  Some, medium speed
   /--------------\
  /  Unit Tests    \ Many, fast, focused
 /------------------\
```

## TDD Workflow

### 1. RED (Failing Test)
```
- Write minimal test for expected behavior
- Run test - verify it FAILS correctly
- Commit: "test: add failing test for [feature]"
```

### 2. GREEN (Pass It)
```
- Write minimal code to pass
- Run test - verify it PASSES
- Commit: "feat: implement [feature]"
```

### 3. REFACTOR
```
- Improve code structure
- Run tests - must still pass
- Commit: "refactor: improve [component]"
```

## Test Structure (AAA)

```
test "should [behavior] when [condition]":
    # Arrange - setup
    input = create_test_input()
    sut = create_system_under_test()

    # Act - execute
    result = sut.execute(input)

    # Assert - verify
    assert result.status == expected
```

## Test Doubles

| Type | Purpose | Use When |
|------|---------|----------|
| Stub | Canned responses | Predictable input |
| Mock | Verify interactions | Verify calls |
| Spy | Record + real impl | Both needed |
| Fake | Working test impl | Real is slow |

**Mock at boundaries:** external APIs, databases, file systems.
**Don't mock:** private methods, value objects, simple utilities.

## Bug Fix Pattern

```
1. REPRODUCE: Write failing test
2. VERIFY: Confirm it fails correctly
3. FIX: Implement minimal fix
4. CONFIRM: Test passes
5. EXPAND: Add edge case tests
```

## Output Format

```markdown
## Testing: [Scope]

| Category | Count | Status |
|----------|-------|--------|
| Unit | N | PASS/FAIL |
| Integration | M | PASS/FAIL |

### New Tests
1. `test_should_create_when_valid`
2. `test_should_reject_duplicate`

### Issues
- [failures or gaps]
```

## Quality Checklist

- [ ] Tests are independent (no shared state)
- [ ] Names describe behavior
- [ ] Each test verifies one concept
- [ ] Edge cases covered
- [ ] No flaky tests
