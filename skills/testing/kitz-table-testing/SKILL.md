---
name: table-testing
description: Table-driven testing patterns using @kitz/test. Triggers on creating test cases, parameterized tests, or when writing .test.ts files.
---

# Table-Driven Testing

## Import

```typescript
import { Test } from '@kitz/test'
```

## Function Mode (Preferred)

Types are inferred from the function signature:

```typescript
// Basic - input/output pairs
Test.on(add)
  .cases(
    [[2, 3], 5],
    [[-1, 1], 0],
    [[0, 0], 0],
  )
  .test()

// Snapshot mode - no expected output
Test.on(parseValue)
  .cases(
    [['42']],
    [['hello']],
  )
  .test()
```

## Describe Mode

For custom types or grouping:

```typescript
Test.describe('Transform')
  .inputType<string>()
  .outputType<string>()
  .cases(
    ['hello', 'HELLO'],
    ['world', 'WORLD'],
  )
  .test(({ input, output }) => {
    expect(input.toUpperCase()).toBe(output)
  })
```

## Chained Describes

Use for nested groupings:

```typescript
Test.describe('String > uppercase', [
  ['hello', 'HELLO'],
])
  .describe('String > lowercase', [
    ['HELLO', 'hello'],
  ])
  .test(({ input, output }) => {
    // runs for each describe block
  })
```

## Matrix Testing

Cartesian product of inputs:

```typescript
Test.on(format)
  .matrix({
    locale: ['en', 'fr', 'de'],
    currency: ['USD', 'EUR'],
    amount: [100, 1000],
  })
  .test()
```

## Output Transformation

Transform expected outputs before comparison:

```typescript
Test.on(serialize)
  .cases(
    [{ a: 1 }, '{"a":1}'],
  )
  .onOutput(JSON.parse) // parse expected before comparing
  .test()
```

## Custom Assertions

Override default assertion:

```typescript
Test.on(approximateCalc)
  .cases(
    [[1.1], 1],
    [[2.9], 3],
  )
  .test(({ input, output, actual }) => {
    expect(actual).toBeCloseTo(output, 0)
  })
```

## Key Rules

* __NEVER wrap `Test.on()` or `Test.describe()` in Vitest `describe` blocks__ - they create their own
* Use `>` separator for nested describes: `'Parent > Child'`
* Function mode infers types automatically - prefer it when testing a single function
* Snapshot mode (no expected output) uses Vitest's snapshot system
