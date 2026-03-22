---
name: rule-testing
description: 'Rule mapping for testing'
---

# Rule testing

Apply this rule whenever work touches:
- `*.spec.ts`
- `*.e2e.spec.ts`

All test code in this repository runs under Jest with ts-jest. Tests must be deterministic, isolated, and free of real-world data.

### Test file conventions

| Pattern | Purpose |
|---|---|
| `{name}.spec.ts` | Unit tests, co-located with source |
| `{name}.e2e.spec.ts` | End-to-end / integration tests |
| `{name}.test-cases.ts` | Shared test data and fixtures |

The test environment loads variables from `.env-files/.env.test`.

### Data generation

Never hardcode test values that could be randomized. Use the following tools:

- **`@faker-js/faker`** for primitive values (strings, numbers, dates, UUIDs).
- **`zocker`** for generating objects that conform to a Zod schema.
- **Shared stubs** from `@carrot-fndn/shared/testing`:
  - `stubRuleInput()` - creates a valid `RuleInput` with sensible defaults.
  - `stubDocument()` - creates a valid document fixture.
  - `createStubFromSchema()` - generates a stub from any Zod schema.

### No real data policy

Tests must never contain real-world identifiable information. Use obviously synthetic values:

| Field | Fake example |
|---|---|
| Company name | `VERDE CAMPO LTDA`, `EXEMPLO INDUSTRIAS` |
| CNPJ | `11.222.333/0004-55`, `77.888.999/0001-22` |
| Vehicle plate | `FKE1A23`, `HIJ3K56` |
| Address | `Rua Modelo, 100`, `Av. Principal, 500` |
| Person name | `Pedro Santos`, `Ana Ferreira` |

This applies to raw OCR text fixtures as well: both the input text and expected assertion values must use fake data consistently.

### Table-driven tests

When a function must be tested against multiple scenarios, use `it.each`:

```ts
it.each([
  { input: 0, expected: 'zero' },
  { input: 1, expected: 'one' },
  { input: 2, expected: 'two' },
])('converts $input to "$expected"', ({ input, expected }) => {
  expect(numberToWord(input)).toBe(expected);
});
```

### Partial assertions

Prefer `expect.objectContaining` when only a subset of fields matters for the assertion. This keeps tests resilient to unrelated field additions:

```ts
expect(result).toEqual(
  expect.objectContaining({
    status: 'APPROVED',
    score: expect.any(Number),
  }),
);
```
