---
name: Financial Calculations
description: Decimal precision and financial math patterns in LivestockAI
---

# Financial Calculations

LivestockAI uses decimal.js for precise financial calculations. All monetary values are stored as DECIMAL(19,2) in the database.

## Currency Utilities

Located in `app/features/settings/currency.ts`:

```typescript
import {
  toDecimal,
  toNumber,
  toDbString,
  formatCurrency,
  multiply,
  divide,
  sumAmounts,
} from '~/features/settings/currency'
```

## Core Functions

### Converting Values

```typescript
// From any input to Decimal
const amount = toDecimal('1234.56')
const amount2 = toDecimal(1234.56)

// To number for display
const num = toNumber('1234.56') // 1234.56

// To string for database
const dbVal = toDbString(1234.56) // "1234.56"
```

### Arithmetic Operations

```typescript
// Multiplication (quantity × price)
const total = multiply(100, 5.5) // Decimal(550)

// Division (with null safety)
const perUnit = divide(total, 100) // Decimal(5.50) or null

// Subtraction
const profit = subtract(revenue, costs)

// Sum multiple amounts
const totalCost = sumAmounts(feedCost, laborCost, overheadCost)
```

### Formatting

```typescript
// Format for display (uses user settings)
formatCurrency(1234.56) // "₦1,234.56" or "$1,234.56"

// Compact format
formatCurrencyCompact(1500000) // "₦1.5M"

// Percentage
calculatePercentage(50, 200) // 25
```

## React Hook

In components, use the `useFormatCurrency` hook:

```typescript
import { useFormatCurrency } from '~/features/settings'

function PriceDisplay({ amount }: { amount: number }) {
  const { format, symbol } = useFormatCurrency()

  return <span>{format(amount)}</span> // "₦1,234.56"
}
```

## Database Storage

All monetary values are stored as `DECIMAL(19,2)`:

```typescript
// Inserting
await db.insertInto('sales').values({
  totalAmount: toDbString(1234.56), // "1234.56"
})

// Reading
const sale = await db.selectFrom('sales').executeTakeFirst()
const amount = toNumber(sale.totalAmount) // 1234.56
```

## Business Logic Examples

### Batch Total Cost

```typescript
export function calculateBatchTotalCost(
  initialQuantity: number,
  costPerUnit: number,
): string {
  if (initialQuantity <= 0 || costPerUnit < 0) {
    return toDbString(0)
  }
  return toDbString(multiply(initialQuantity, costPerUnit))
}
```

### Profit Calculation

```typescript
export function calculateProfit(
  revenue: MoneyInput,
  costs: MoneyInput,
): Decimal {
  return subtract(revenue, costs)
}
```

## Related Skills

- `multi-currency` - Currency settings and formatting
- `three-layer-architecture` - Service layer calculations
