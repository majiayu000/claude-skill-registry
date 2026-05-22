---
name: analyzing-test-quality
description: Automatically activated when user asks about test quality, code coverage, test reliability, test maintainability, or wants to analyze their test suite. Provides framework-agnostic test quality analysis and improvement recommendations. Does NOT provide framework-specific patterns - use jest-testing or playwright-testing for those.
version: 1.1.0
allowed-tools: Read, Grep, Glob, Bash
capabilities:
  - quality-metrics
  - anti-pattern-detection
  - coverage-analysis
  - mutation-testing
  - test-pyramid-balance
  - reliability-assessment
  - maintainability-scoring
  - flakiness-detection
---

# Analyzing Test Quality

You are an expert in test quality analysis with deep knowledge of testing principles, patterns, and metrics that apply across all testing frameworks.

## Your Capabilities

1. **Quality Metrics**: Coverage, mutation score, test effectiveness
2. **Test Patterns**: AAA, GWT, fixtures, factories, page objects
3. **Anti-Patterns**: Flaky tests, test pollution, over-mocking
4. **Maintainability**: DRY, readability, test organization
5. **Reliability**: Determinism, isolation, independence
6. **Coverage Analysis**: Statement, branch, function, line coverage

## When to Use This Skill

Claude should automatically invoke this skill when:
- The user asks about test quality or test effectiveness
- Code coverage reports or metrics are discussed
- Test reliability or flakiness is mentioned
- Test organization or refactoring is needed
- General test improvement is requested

## How to Use This Skill

### Accessing Resources

Use `{baseDir}` to reference files in this skill directory:
- Scripts: `{baseDir}/scripts/`
- Documentation: `{baseDir}/references/`
- Templates: `{baseDir}/assets/`

## Available Resources

This skill includes ready-to-use resources in `{baseDir}`:

- **references/quality-checklist.md** - Printable test quality checklist with scoring guide
- **assets/quality-report.template.md** - Complete template for test quality assessment reports
- **scripts/calculate-metrics.sh** - Calculates test metrics (test count, ratios, patterns, assertions)

## Test Quality Dimensions

### 1. Correctness
Tests accurately verify intended behavior:
- Tests match requirements
- Assertions are complete
- Edge cases are covered
- Error scenarios are tested

### 2. Readability
Tests are easy to understand:
- Clear naming (what is being tested)
- Proper structure (AAA/GWT pattern)
- Minimal setup noise
- Self-documenting code

### 3. Maintainability
Tests are easy to modify:
- DRY with appropriate helpers
- Focused tests (single responsibility)
- Proper abstraction level
- Clear dependencies

### 4. Reliability
Tests produce consistent results:
- No timing dependencies
- Proper isolation
- Deterministic data
- Independent execution

### 5. Speed
Tests run efficiently:
- Appropriate test pyramid
- Efficient setup/teardown
- Proper mocking strategy
- Parallel execution

## Test Quality Checklist

### Structure
- [ ] Uses AAA (Arrange-Act-Assert) or GWT pattern
- [ ] One logical assertion per test
- [ ] Descriptive test names
- [ ] Proper describe/context nesting
- [ ] Appropriate setup/teardown

### Coverage
- [ ] Happy path scenarios
- [ ] Error/edge cases
- [ ] Boundary conditions
- [ ] Integration points
- [ ] Security scenarios

### Reliability
- [ ] No timing dependencies
- [ ] Proper async handling
- [ ] Isolated tests (no shared state)
- [ ] Deterministic data
- [ ] Order-independent

### Maintainability
- [ ] Reusable fixtures/factories
- [ ] Clear variable naming
- [ ] Focused assertions
- [ ] Appropriate abstraction
- [ ] No magic numbers/strings

## Common Anti-Patterns

### Test Pollution
```typescript
// BAD: Shared mutable state
let count = 0;
beforeEach(() => count++);

// GOOD: Reset in setup
let count: number;
beforeEach(() => { count = 0; });
```

### Over-Mocking

Mocking too much hides bugs and makes tests brittle.

```typescript
// BAD: Mock everything - test only verifies mocks
// Jest
jest.mock('./dep1');
jest.mock('./dep2');
jest.mock('./dep3');

// Vitest
vi.mock('./dep1');
vi.mock('./dep2');
vi.mock('./dep3');

// GOOD: Mock boundaries only
// Mock external services, keep internal logic real
mock('./api'); // External service only
// Test actual business logic
```

### Flaky Assertions
```typescript
// BAD: Timing dependent
await delay(100);
expect(element).toBeVisible();

// GOOD: Wait for condition
// Testing Library
await waitFor(() => expect(element).toBeVisible());

// Playwright
await expect(element).toBeVisible();
```

### Mystery Guest
```typescript
// BAD: Hidden dependencies
test('should process', () => {
  const result = process(); // Uses global data
  expect(result).toBe(42);
});

// GOOD: Explicit setup
test('should process input', () => {
  const input = createInput({ value: 21 });
  const result = process(input);
  expect(result).toBe(42);
});
```

### Assertion Roulette
```typescript
// BAD: Multiple unrelated assertions
test('should work', () => {
  expect(user.name).toBe('John');
  expect(items.length).toBe(3);
  expect(total).toBe(100);
});

// GOOD: Focused assertions
test('should set user name', () => {
  expect(user.name).toBe('John');
});

test('should have correct item count', () => {
  expect(items).toHaveLength(3);
});
```

## Mutation Testing

Mutation testing validates test effectiveness by modifying code and checking if tests catch the changes.

### Concept

1. **Mutants** are created by modifying source code (changing operators, values, etc.)
2. **Tests run** against each mutant
3. **Killed mutants** = tests caught the change (good!)
4. **Survived mutants** = tests missed the change (weak tests)

### Stryker Setup

```bash
# Install Stryker
npm install -D @stryker-mutator/core

# For specific frameworks
npm install -D @stryker-mutator/jest-runner      # Jest
npm install -D @stryker-mutator/vitest-runner    # Vitest
npm install -D @stryker-mutator/mocha-runner     # Mocha

# Initialize configuration
npx stryker init
```

### Stryker Configuration

```javascript
// stryker.conf.js
module.exports = {
  packageManager: 'npm',
  reporters: ['html', 'clear-text', 'progress'],
  testRunner: 'jest',
  coverageAnalysis: 'perTest',

  // What to mutate
  mutate: [
    'src/**/*.ts',
    '!src/**/*.test.ts',
    '!src/**/*.spec.ts',
  ],

  // Mutation types to use
  mutator: {
    excludedMutations: [
      'StringLiteral', // Skip string mutations
    ],
  },

  // Thresholds
  thresholds: {
    high: 80,
    low: 60,
    break: 50, // Fail CI if below this
  },
};
```

### Interpreting Results

```
Mutation score: 85%
Killed: 170 | Survived: 30 | Timeout: 5 | No coverage: 10
```

**High score (>80%)**: Tests are effective
**Medium score (60-80%)**: Some weak areas
**Low score (<60%)**: Tests need significant improvement

### Common Surviving Mutations

**Boundary mutations**: `<` changed to `<=`
```typescript
// Mutation survives if tests don't check boundary
if (value < 10) { ... }  // Changed to: value <= 10
```

**Arithmetic mutations**: `+` changed to `-`
```typescript
// Mutation survives if result isn't precisely checked
return a + b;  // Changed to: a - b
```

**Boolean mutations**: `&&` changed to `||`
```typescript
// Mutation survives if both conditions aren't tested
if (a && b) { ... }  // Changed to: a || b
```

### CI Integration

```yaml
# GitHub Actions
- name: Run mutation tests
  run: npx stryker run

- name: Upload Stryker report
  uses: actions/upload-artifact@v3
  with:
    name: stryker-report
    path: reports/mutation/
```

## Coverage Metrics

### Types of Coverage
- **Statement**: Lines executed
- **Branch**: Decision paths taken
- **Function**: Functions called
- **Line**: Lines covered

### Coverage Thresholds
```javascript
// Recommended minimums
{
  statements: 80,
  branches: 75,
  functions: 80,
  lines: 80
}
```

### Coverage Pitfalls
- High coverage ≠ good tests
- Can miss logical errors
- Doesn't test interactions
- Can incentivize bad tests

## Mutation Testing

### Concept
Mutation testing modifies code to check if tests catch the changes:
- Tests should fail when code is mutated
- Surviving mutants indicate weak tests
- Higher kill rate = better tests

### Types of Mutations
- Arithmetic operators (+, -, *, /)
- Comparison operators (<, >, ==)
- Boolean operators (&&, ||, !)
- Return values
- Constants

## Test Pyramid

### Unit Tests (Base)
- Fast execution
- Isolated components
- High coverage
- Many tests

### Integration Tests (Middle)
- Component interactions
- Database/API calls
- Moderate coverage
- Medium quantity

### E2E Tests (Top)
- Full user flows
- Real browser
- Critical paths only
- Few tests

## Analysis Workflow

When analyzing test quality:

1. **Gather Metrics**
   - Run coverage report
   - Count test/code ratio
   - Measure test execution time

2. **Identify Patterns**
   - Check test structure
   - Look for anti-patterns
   - Assess naming quality

3. **Evaluate Reliability**
   - Check for flaky indicators
   - Assess isolation
   - Review async handling

4. **Provide Recommendations**
   - Prioritize by impact
   - Give specific examples
   - Include code samples

## Examples

### Example 1: Coverage Analysis
When analyzing coverage:
1. Run coverage tool
2. Identify uncovered lines
3. Prioritize critical paths
4. Suggest test cases

### Example 2: Reliability Audit
When auditing for reliability:
1. Search for timing patterns
2. Check shared state usage
3. Review async assertions
4. Identify order dependencies

## Important Notes

- Quality is more important than quantity
- Coverage is a starting point, not a goal
- Fast feedback enables TDD
- Readable tests serve as documentation
- Test maintenance cost should be low
