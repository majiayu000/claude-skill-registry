---
name: Multi-Currency
description: Currency settings and formatting for global users in LivestockAI
---

# Multi-Currency

LivestockAI supports multiple currencies with user-configurable settings.

## Supported Currencies

| Currency        | Symbol | Code | Regions |
| --------------- | ------ | ---- | ------- |
| Nigerian Naira  | ₦      | NGN  | Nigeria |
| US Dollar       | $      | USD  | Global  |
| Euro            | €      | EUR  | Europe  |
| British Pound   | £      | GBP  | UK      |
| Indian Rupee    | ₹      | INR  | India   |
| Kenyan Shilling | KSh    | KES  | Kenya   |

## User Settings

Currency preference is stored in `user_settings`:

```typescript
interface UserSettings {
  currency: 'NGN' | 'USD' | 'EUR' | 'GBP' | 'INR' | 'KES'
  dateFormat: 'DD/MM/YYYY' | 'MM/DD/YYYY' | 'YYYY-MM-DD'
  weightUnit: 'kg' | 'lb'
  language: 'en' | 'fr' | 'es' | 'pt' | 'sw' | 'ha'
}
```

## Using Currency in Components

```typescript
import { useFormatCurrency } from '~/features/settings'

function PriceDisplay({ amount }: { amount: number }) {
  const { format, formatCompact, symbol } = useFormatCurrency()

  return (
    <div>
      <span>{format(amount)}</span>      {/* ₦1,234.56 */}
      <span>{formatCompact(amount)}</span> {/* ₦1.2K */}
      <span>{symbol}</span>               {/* ₦ */}
    </div>
  )
}
```

## Currency Presets

```typescript
// app/features/settings/currency-presets.ts
export const CURRENCY_PRESETS = {
  NGN: {
    code: 'NGN',
    symbol: '₦',
    name: 'Nigerian Naira',
    locale: 'en-NG',
    decimals: 2,
  },
  USD: {
    code: 'USD',
    symbol: '$',
    name: 'US Dollar',
    locale: 'en-US',
    decimals: 2,
  },
  // ...
}
```

## Formatting Functions

```typescript
// Format with user's currency setting
const { format } = useFormatCurrency()
format(1234.56) // "₦1,234.56"

// Compact format for large numbers
const { formatCompact } = useFormatCurrency()
formatCompact(1500000) // "₦1.5M"

// Get just the symbol
const { symbol } = useFormatCurrency()
// "₦"
```

## Database Storage

All monetary values are stored as DECIMAL(19,2) without currency symbol:

```typescript
// Store
await db.insertInto('sales').values({
  totalAmount: toDbString(1234.56), // "1234.56"
})

// Display
const amount = toNumber(sale.totalAmount)
format(amount) // "₦1,234.56" (based on user settings)
```

## Related Skills

- `financial-calculations` - Decimal arithmetic
- `i18n-patterns` - Locale-aware formatting
