---
name: bench
description: Generate mitata benchmark files following project conventions
disable-model-invocation: true
arguments:
  - name: category
    description: The benchmark category (e.g., arithmetic, parsing, comparison)
    required: true
---

# Generate Benchmark

Generate a mitata benchmark file for the `{{ category }}` category.

## Project Conventions

This project uses mitata for benchmarking. Follow the patterns in `bench/`.

### Setup Import

Always import the shared setup:

```typescript
import { run, bench, group, baseline } from "mitata";
import {
  Decimal,
  decimalJs,
  bigJs,
  bignumberJs,
  dineroAmount,
} from "./setup";
```

### Benchmark Structure

```typescript
// Group related benchmarks
group("{{ category }} - operation name", () => {
  // Always include baseline (usually Decimal or native)
  baseline("Centimal", () => {
    // benchmark code
  });

  // Compare against other libraries
  bench("decimal.js", () => {
    // equivalent operation
  });

  bench("big.js", () => {
    // equivalent operation
  });

  bench("bignumber.js", () => {
    // equivalent operation
  });
});

// Run all benchmarks
await run();
```

### Example Pattern (from arithmetic.bench.ts)

```typescript
group("addition - small numbers", () => {
  baseline("Centimal", () => {
    Decimal.from("123.45").add(Decimal.from("67.89"));
  });

  bench("decimal.js", () => {
    decimalJs("123.45").plus("67.89");
  });

  bench("big.js", () => {
    bigJs("123.45").plus("67.89");
  });

  bench("bignumber.js", () => {
    bignumberJs("123.45").plus("67.89");
  });
});
```

### Test Data Recommendations

| Category | Test Cases |
|----------|------------|
| Arithmetic | Small numbers, large numbers, high precision |
| Parsing | Integers, decimals, scientific notation, edge cases |
| Comparison | Equal, not equal, less than, greater than |
| Percentage | Small %, large %, fractional % |
| Allocation | 2-way split, 3-way split, uneven ratios |

### Output Location

Create: `bench/{{ category }}.bench.ts`

## Your Task

1. Read existing benchmarks in `bench/` to understand patterns
2. Read `bench/setup.ts` to understand available test fixtures
3. Create `bench/{{ category }}.bench.ts` with comprehensive benchmarks
4. Ensure the new file is imported in `bench/run.ts` if needed
