---
name: Test-Driven Development
description: This skill should be used when the user asks to "implement TDD", "write tests first", "follow RED-GREEN-REFACTOR", "use test-driven development", "create failing tests", or mentions TDD workflow patterns.
version: 1.0.0
---

# Test-Driven Development (TDD) Workflow

## Overview

Test-Driven Development enforces the RED → GREEN → REFACTOR discipline to ensure robust, well-tested code with clean design. This skill guides implementation of the three-phase TDD cycle for both Python and TypeScript/JavaScript codebases.

## TDD Three-Phase Cycle

### Phase 1: RED - Write Failing Test

Write the smallest possible test that fails for the right reason.

**Principles:**
- Test documents the intended behavior
- Test must fail initially (verify failure)
- Focus on one specific behavior per test
- Use descriptive test names that explain the "should"

**Test Structure:**
```
// Arrange - Set up test data
// Act - Execute the behavior
// Assert - Verify the result
```

### Phase 2: GREEN - Make Test Pass

Write the minimal implementation to make the test pass.

**Principles:**
- Implement only what's needed for the test to pass
- Don't optimize or refactor yet
- Hardcode values if necessary
- Focus on correctness, not elegance

### Phase 3: REFACTOR - Clean Up Code

Improve the code while keeping tests green.

**Focus Areas:**
- Extract repeated logic into functions
- Improve naming and readability
- Apply SOLID principles
- Remove duplication
- Optimize performance if needed

**Safety Net:** Run tests after each refactoring step.

## Implementation Workflow

### Step 1: Understand Requirements
- Clarify the feature's expected behavior
- Identify edge cases and error conditions
- Define acceptance criteria

### Step 2: Write Integration Test First
- Start with a higher-level test that describes user behavior
- Use realistic test data and scenarios
- Focus on the public interface

### Step 3: Follow TDD for Implementation
- Write unit test (RED)
- Implement minimal solution (GREEN)
- Refactor and clean up (REFACTOR)
- Repeat for each behavior

### Step 4: Verify Complete Coverage
- Run coverage report
- Ensure all new code paths are tested
- Add tests for any missing edge cases

## Test Categories

### Unit Tests
- Test individual functions/methods in isolation
- Use mocks for external dependencies
- Fast execution (< 100ms each)
- High coverage of business logic

### Integration Tests
- Test component interactions
- Use real database/API connections where appropriate
- Validate end-to-end workflows
- Slower but comprehensive

### Edge Case Tests
- Null/undefined inputs
- Empty collections
- Boundary values (min/max)
- Error conditions and exceptions

## Language-Specific Patterns

### Python (pytest)
```python
def test_should_calculate_total_with_tax():
    # Arrange
    cart = ShoppingCart()
    cart.add_item("item1", price=100.00)

    # Act
    total = cart.calculate_total(tax_rate=0.08)

    # Assert
    assert total == 108.00
```

### TypeScript (Jest)
```typescript
describe('ShoppingCart', () => {
  it('should calculate total with tax', () => {
    // Arrange
    const cart = new ShoppingCart();
    cart.addItem('item1', 100.00);

    // Act
    const total = cart.calculateTotal(0.08);

    // Assert
    expect(total).toBe(108.00);
  });
});
```

## Quality Gates

### Before Moving to GREEN
- [ ] Test fails for the right reason
- [ ] Test name clearly describes the behavior
- [ ] Test is minimal and focused
- [ ] All existing tests still pass

### Before Moving to REFACTOR
- [ ] New test passes
- [ ] Implementation is minimal
- [ ] No over-engineering
- [ ] All tests still pass

### After REFACTOR
- [ ] Code is clean and readable
- [ ] No duplication
- [ ] SOLID principles applied
- [ ] All tests pass
- [ ] Coverage maintained

## Common Pitfalls to Avoid

### Writing Too Much Code in GREEN
**Problem:** Implementing multiple features at once
**Solution:** Write only enough code to make the current test pass

### Skipping the RED Phase
**Problem:** Writing tests after implementation
**Solution:** Always write failing test first, verify it fails

### Not Refactoring
**Problem:** Accumulating technical debt
**Solution:** Refactor immediately after GREEN, while context is fresh

### Testing Implementation Details
**Problem:** Tests break when refactoring
**Solution:** Test public behavior, not internal implementation

## Tools and Commands

### Running Tests
```bash
# Python
pytest --cov=src tests/
pytest -v --cov-report=html

# TypeScript/Jest
npm test
npm run test:coverage
npm run test:watch
```

### Coverage Thresholds
- **Lines:** 80% minimum
- **Branches:** 80% minimum
- **Functions:** 90% minimum
- **New code:** 100% coverage required

## Additional Resources

### Reference Files
For detailed patterns and advanced techniques, consult:
- **`references/tdd-patterns.md`** - Common TDD patterns and best practices
- **`references/testing-pyramid.md`** - Testing strategy and test types
- **`references/mocking-strategies.md`** - Mock patterns for different scenarios

### Example Files
Working TDD examples in `examples/`:
- **`examples/python-tdd-example.py`** - Complete Python TDD workflow
- **`examples/typescript-tdd-example.ts`** - TypeScript TDD implementation
- **`examples/api-endpoint-tdd.py`** - TDD for API endpoints

### Scripts
Utility scripts in `scripts/`:
- **`scripts/run-tdd-cycle.sh`** - Automated TDD cycle runner
- **`scripts/coverage-check.sh`** - Coverage validation script
- **`scripts/test-watch.sh`** - Watch mode for continuous testing

## TDD in Context

### When to Use TDD
- New feature development
- Bug fixes with regression tests
- Refactoring existing code
- API design and validation

### When to Consider Alternatives
- Exploratory coding/prototyping
- UI/UX experimentation
- Performance optimization spikes
- External system integration discovery

## Success Metrics

### Quantitative
- Code coverage > 80%
- Test execution time < 5 minutes
- Test failure rate < 5%
- Defect density reduction

### Qualitative
- Confidence in refactoring
- Clear behavior documentation
- Faster debugging cycles
- Improved code design

Apply TDD discipline consistently to build robust, maintainable code with comprehensive test coverage and clean architecture.