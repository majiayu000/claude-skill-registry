---
name: writing-utility-helpers
description: Standardizes frequent utility functions for currency, dates, and strings. Use to maintain consistency in formatting.
---

# Utility Helper Functions

## When to use this skill
- Formatting prices in PKR or USD.
- Truncating long descriptions in cards.
- Pretty-printing dates for travel itineraries.

## Recommended Helpers
### Currency
```typescript
export const formatCurrency = (amount: number, currency = 'PKR') => {
    return new Intl.NumberFormat('en-PK', {
        style: 'currency',
        currency,
        maximumFractionDigits: 0,
    }).format(amount);
};
```

### String Truncation
```typescript
export const truncate = (str: string, length: number) => {
    return str.length > length ? str.substring(0, length) + '...' : str;
};
```

## Instructions
- **Location**: Store all helpers in `lib/utils.ts` or `utils/index.ts`.
- **DRY**: Check for existing helpers before writing new logic.
