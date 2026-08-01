---
name: spacing-001
description: '"Fix the spacing on this component. The cards feel disconnected, like
  they''re floating islands instead of a related group."'
---

# Test B: With Skill

**Date:** 2024-12-24

## Prompt
"Fix the spacing on this component. The cards feel disconnected, like they're floating islands instead of a related group."

## Claude's Diagnosis

1. **Gap too large**: `gap-6` (1.5rem/24px) creates excessive white space between cards
2. **Heavy shadow**: The `shadow` class creates a strong drop shadow that emphasizes separation
3. **Section padding imbalance**: Large vertical padding (`py-12`) but only horizontal padding creates a boxy feeling
4. **Heading distance**: `mb-8` pushes the heading far from the cards it describes

## Claude's Fix

```tsx
<div className="grid grid-cols-3 gap-4">
  <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
```

Key changes:
- `gap-6` → `gap-4` (24px → 16px)
- Kept `p-6` (padding unchanged)
- `shadow` → `shadow-sm`
- Added `border border-gray-100`
- `mb-8` → `mb-6`

## Notable

- Did NOT mention Law of Proximity by name
- Did NOT explicitly identify padding = gap as the core issue
- Only reduced gap, kept padding same (partial fix)
- Added border (design embellishment)
- Values are on 4px grid
