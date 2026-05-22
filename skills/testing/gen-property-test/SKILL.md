---
name: gen-property-test
description: Generate fast-check property tests following project conventions
disable-model-invocation: true
arguments:
  - name: method
    description: The Decimal method to test (e.g., add, multiply, divide)
    required: true
---

# Generate Property Test

Generate a property-based test for the `{{ method }}` method on the Decimal class.

## Project Conventions

This project uses fast-check for property-based testing. Follow these patterns:

### Custom Arbitrary

Use the existing `decimalArb` pattern from `src/core/decimal.property.test.ts`:

```typescript
import * as fc from "fast-check";
import { Decimal } from "./decimal";

// Arbitrary for valid decimal values
const decimalArb = fc
  .tuple(
    fc.bigInt({ min: -10n ** 18n, max: 10n ** 18n }),
    fc.integer({ min: 0, max: 8 })
  )
  .map(([significand, scale]) => {
    const str = significand.toString();
    if (scale === 0) return Decimal.from(str);
    const insertPoint = str.length - scale;
    if (insertPoint <= 0) {
      return Decimal.from(`0.${"0".repeat(-insertPoint)}${str.replace("-", "")}`);
    }
    return Decimal.from(`${str.slice(0, insertPoint)}.${str.slice(insertPoint)}`);
  });
```

### Test Structure

```typescript
import { describe, test, expect } from "bun:test";
import * as fc from "fast-check";

describe("{{ method }} properties", () => {
  test("property name", () => {
    fc.assert(
      fc.property(decimalArb, (a) => {
        // Return boolean for invariant
        return /* invariant expression */;
      })
    );
  });
});
```

### Mathematical Invariants to Consider

For arithmetic operations, consider these properties:

| Property | Formula | Applies To |
|----------|---------|------------|
| Identity | `a.op(identity) = a` | add(0), multiply(1) |
| Commutativity | `a.op(b) = b.op(a)` | add, multiply |
| Associativity | `(a.op(b)).op(c) = a.op(b.op(c))` | add, multiply |
| Inverse | `a.op(a.inverse()) = identity` | add/negate, multiply/reciprocal |
| Distributivity | `a.mul(b.add(c)) = a.mul(b).add(a.mul(c))` | multiply over add |
| Idempotence | `op(a, a) = a` | min, max |
| Absorption | `min(a, max(a, b)) = a` | min/max |

### Output Location

Add tests to: `src/core/decimal.property.test.ts`

## Your Task

1. Read `src/core/decimal.property.test.ts` to understand existing patterns
2. Read `src/core/decimal.ts` to understand the `{{ method }}` implementation
3. Generate property tests for `{{ method }}` covering relevant invariants
4. Add tests to the existing property test file in the appropriate describe block
