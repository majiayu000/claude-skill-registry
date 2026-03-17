---
name: Financial Integrity
description: Patterns for provable financial accuracy and invariant testing
---

# Financial Integrity

In the "Action Era", LivestockAI agents may autonomously propose sales or analyze profit. **Trust is our currency.** Calculations must be mathematically provable.

## Core Principle: The "Penny Perfect" Rule

All financial storage and calculation must treat money as an integer (minor units) or high-precision decimal.
**NEVER use standard generic `number` floating point math for money.**

## 1. Storage Standards

**Database:**
`DECIMAL(19, 4)` for unit prices (allows for precise small-unit costs like feed per gram).
`DECIMAL(19, 2)` for final transaction amounts (invoices, payments).

**TypeScript:**
Always use `decimal.js` via the project's currency utilities.

```typescript
// ❌ Dangerous
const total = 0.1 + 0.2 // 0.30000000000000004

// ✅ Safe
import { add } from '~/features/settings/currency'
const total = add(0.1, 0.2) // Decimal(0.3)
```

## 2. Invariant Testing (Property Tests)

Use `fast-check` to prove financial laws hold true for **all** inputs.

### Profit Law

`Profit = Revenue - (COGS + Expenses)`

```typescript
test('Profit Invariant', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), (revenue, cost) => {
      const profit = calculateProfit(revenue, cost)
      // Profit + Cost must always exactly equal Revenue
      return profit.add(cost).equals(revenue)
    }),
  )
})
```

### Allocation Law

When splitting a cost across N batches, the sum of parts must equal the total.
_Watch out for rounding leftovers._

**Pattern: The "Penny Allocate" Algorithm**
If splitting $100 among 3 batches:
Batch 1: $33.33
Batch 2: $33.33
Batch 3: $33.34 (Takes the remainder)

## 3. Immutability

Financial records (`invoices`, `sales`, `expenses`) should be "Append-Only" to the user.
If a mistake is made:

1. Create a **Reversal Transaction** (negative amount) to void the error.
2. Create a new **Correct Transaction**.
   _This preserves the audit trail._

## 4. Multi-Currency Safety

Always store `exchangeRate` and `currencyCode` at the **time of transaction**.
Never calculate historical value using _current_ exchange rates.

## Related Skills

- `financial-calculations` - The specific library calls implementation
- `property-testing` - The value verification method
