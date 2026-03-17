---
name: import
description: CSV and OFX transaction import parsing. Use when working on files in src/lib/import/.
---

# Import Guidelines

## Flow

File Drop → Parse (CSV/OFX) → Column Mapping → Formatting → Preview → Import

## Money Handling

**All amounts stored as integers in minor units:**

```typescript
import { toMinorUnitsForCurrency } from "@/lib/domain/currency";

toMinorUnitsForCurrency(12.34, "USD"); // 1234 (cents)
toMinorUnitsForCurrency(1234, "JPY");  // 1234 (0 decimals)
toMinorUnitsForCurrency(1.234, "KWD"); // 1234 (3 decimals)
```

**Currency resolution order:** OFX CURDEF → Account → User default → Vault default → USD

## CSV Parser

Auto-detects: separator, headers, date/number formats.

## Duplicate Detection

Uses Levenshtein distance: date window ±3 days, amount tolerance 1 cent, description 80% similarity.

## Critical Rules

- Never trust user input - validate all parsed data
- Handle encoding: UTF-8, Latin-1, Windows-1252
- Preserve `originalRow` for debugging
- Handle negative formats like `(123.45)`
- Return structured errors, don't throw

## Testing

Test with real bank exports covering different date formats (US/EU/ISO), number formats, edge cases, large files.
