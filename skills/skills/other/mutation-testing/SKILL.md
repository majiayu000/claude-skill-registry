---
name: mutation-testing
description: Validate test effectiveness with mutation testing using Stryker (TypeScript/JavaScript) and mutmut (Python). Find weak tests that pass despite code mutations. Use to improve test quality.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, TodoWrite
---

# Mutation Testing

Expert knowledge for mutation testing - validating that your tests actually catch bugs by introducing deliberate code mutations.

## Core Concept

- **Mutants**: Small code changes introduced automatically
- **Killed**: Test fails with mutation (good - test caught the bug)
- **Survived**: Test passes with mutation (bad - weak test)
- **Score**: Percentage of mutants killed (aim for 80%+)

## TypeScript/JavaScript (Stryker)

### Installation

```bash
# Using Bun
bun add -d @stryker-mutator/core @stryker-mutator/vitest-runner

# Using npm
npm install -D @stryker-mutator/core @stryker-mutator/vitest-runner
```

### Configuration

```typescript
// stryker.config.mjs
export default {
  packageManager: 'bun',
  reporters: ['html', 'clear-text', 'progress'],
  testRunner: 'vitest',
  coverageAnalysis: 'perTest',
  mutate: ['src/**/*.ts', '!src/**/*.test.ts'],
  thresholds: { high: 80, low: 60, break: 60 },
  incremental: true,
}
```

### Running Stryker

```bash
# Run mutation testing
bunx stryker run

# Incremental mode (only changed files)
bunx stryker run --incremental

# Specific files
bunx stryker run --mutate "src/utils/**/*.ts"

# Open HTML report
open reports/mutation/html/index.html
```

### Example: Weak Test

```typescript
// Source code
function calculateDiscount(price: number, percentage: number): number {
  return price - (price * percentage / 100)
}

// ❌ WEAK: Test passes even if we mutate calculation
test('applies discount', () => {
  expect(calculateDiscount(100, 10)).toBeDefined() // Too weak!
})

// ✅ STRONG: Test catches mutation
test('applies discount correctly', () => {
  expect(calculateDiscount(100, 10)).toBe(90)
  expect(calculateDiscount(100, 20)).toBe(80)
  expect(calculateDiscount(50, 10)).toBe(45)
})
```

## Python (mutmut)

### Installation

```bash
uv add --dev mutmut
```

### Running mutmut

```bash
# Run mutation testing
uv run mutmut run

# Show results
uv run mutmut results

# Show specific mutant
uv run mutmut show 1

# Generate HTML report
uv run mutmut html
open html/index.html
```

## Common Mutation Types

```typescript
// Arithmetic Operator
// Original: a + b → a - b, a * b, a / b

// Relational Operator
// Original: a > b → a >= b, a < b, a <= b

// Logical Operator
// Original: a && b → a || b

// Boolean Literal
// Original: true → false
```

## Mutation Score Targets

| Score | Quality | Action |
|-------|---------|--------|
| 90%+ | Excellent | Maintain quality |
| 80-89% | Good | Small improvements |
| 70-79% | Acceptable | Focus on weak areas |
| < 60% | Poor | Major improvements needed |

## Improving Weak Tests

### Pattern: Insufficient Assertions

```typescript
// Before: Mutation survives
test('calculates sum', () => {
  expect(sum([1, 2, 3])).toBeGreaterThan(0) // Weak!
})

// After: Mutation killed
test('calculates sum correctly', () => {
  expect(sum([1, 2, 3])).toBe(6)
  expect(sum([0, 0, 0])).toBe(0)
  expect(sum([])).toBe(0)
})
```

### Pattern: Boundary Conditions

```typescript
// After: Tests boundaries
test('validates age boundaries', () => {
  expect(isValidAge(18)).toBe(true)   // Min valid
  expect(isValidAge(17)).toBe(false)  // Just below
  expect(isValidAge(100)).toBe(true)  // Max valid
  expect(isValidAge(101)).toBe(false) // Just above
})
```

## Best Practices

- Start with core business logic modules
- Ensure 80%+ coverage before mutation testing
- Run incrementally (only changed files)
- Focus on important files first
- Don't expect 100% mutation score (equivalent mutants exist)

## Workflow

```bash
# 1. Ensure good coverage first
bun test --coverage
# Target: 80%+ coverage

# 2. Run mutation testing
bunx stryker run

# 3. Check report
open reports/mutation/html/index.html

# 4. Fix survived mutants
# 5. Re-run incrementally
bunx stryker run --incremental
# or: npx stryker run --incremental
```

## See Also

- `vitest-testing` - Unit testing framework
- `test-quality-analysis` - Detecting test smells
