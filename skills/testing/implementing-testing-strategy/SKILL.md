---
name: implementing-testing-strategy
description: Quality assurance protocols using Vitest. Use for critical logic like pricing and availability calculations.
---

# Testing Strategy

## When to use this skill
- Building core business logic (e.g., "Calculate Group Discount").
- Before major refactors.

## Tools
- **Vitest**: Fast, Vite-compatible runner.
- **React Testing Library**: For component testing (optional/high-priority items only).

## Example Test
```typescript
import { calculatePrice } from './pricing';
import { expect, test } from 'vitest';

test('applies 10% discount for groups > 5', () => {
    expect(calculatePrice(100, 6)).toBe(540); 
});
```

## Instructions
- **Focus**: Test logic, not the UI (avoid testing that "a button is blue").
- **Mocks**: Mock Appwrite SDK calls locally to avoid hitting the live API during tests.
