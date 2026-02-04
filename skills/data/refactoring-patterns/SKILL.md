---
name: refactoring-patterns
description: Apply when improving code structure without changing behavior: reducing duplication, simplifying complexity, or improving readability.
version: 1.0.0
tokens: ~650
confidence: high
sources:
  - https://refactoring.guru/refactoring/catalog
  - https://martinfowler.com/books/refactoring.html
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [refactoring, code-quality, patterns, clean-code]
---

## When to Use

Apply when improving code structure without changing behavior: reducing duplication, simplifying complexity, or improving readability.

## Patterns

### Pattern 1: Extract Function
```typescript
// Source: https://refactoring.guru/extract-method
// BEFORE
function processOrder(order: Order) {
  // Validate
  if (!order.items.length) throw new Error('Empty');
  if (!order.customer) throw new Error('No customer');

  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  total *= 1.1; // Tax

  // Save
  db.orders.create({ ...order, total });
}

// AFTER
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order.items);
  saveOrder(order, total);
}

function validateOrder(order: Order) { /* ... */ }
function calculateTotal(items: Item[]) { /* ... */ }
function saveOrder(order: Order, total: number) { /* ... */ }
```

### Pattern 2: Replace Conditional with Polymorphism
```typescript
// Source: https://refactoring.guru/replace-conditional-with-polymorphism
// BEFORE
function getPrice(item: Item) {
  switch (item.type) {
    case 'book': return item.basePrice * 0.9;
    case 'electronics': return item.basePrice * 1.1;
    case 'food': return item.basePrice;
  }
}

// AFTER
interface PricingStrategy {
  calculate(basePrice: number): number;
}

const strategies: Record<string, PricingStrategy> = {
  book: { calculate: (p) => p * 0.9 },
  electronics: { calculate: (p) => p * 1.1 },
  food: { calculate: (p) => p },
};

function getPrice(item: Item) {
  return strategies[item.type].calculate(item.basePrice);
}
```

### Pattern 3: Introduce Parameter Object
```typescript
// Source: https://refactoring.guru/introduce-parameter-object
// BEFORE
function searchProducts(
  query: string,
  minPrice: number,
  maxPrice: number,
  category: string,
  inStock: boolean,
  sortBy: string,
  page: number
) { /* ... */ }

// AFTER
interface SearchParams {
  query: string;
  priceRange?: { min: number; max: number };
  category?: string;
  inStock?: boolean;
  sortBy?: string;
  page?: number;
}

function searchProducts(params: SearchParams) { /* ... */ }
```

### Pattern 4: Replace Magic Numbers
```typescript
// Source: https://refactoring.guru/replace-magic-number-with-symbolic-constant
// BEFORE
if (user.age >= 18) { /* ... */ }
setTimeout(fn, 86400000);

// AFTER
const LEGAL_AGE = 18;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (user.age >= LEGAL_AGE) { /* ... */ }
setTimeout(fn, ONE_DAY_MS);
```

### Pattern 5: Guard Clauses (Early Return)
```typescript
// Source: https://refactoring.guru/replace-nested-conditional-with-guard-clauses
// BEFORE
function getPayment(employee: Employee) {
  let result;
  if (employee.isSeparated) {
    result = separatedAmount();
  } else {
    if (employee.isRetired) {
      result = retiredAmount();
    } else {
      result = normalAmount();
    }
  }
  return result;
}

// AFTER
function getPayment(employee: Employee) {
  if (employee.isSeparated) return separatedAmount();
  if (employee.isRetired) return retiredAmount();
  return normalAmount();
}
```

### Pattern 6: Compose Method
```typescript
// Source: https://refactoring.guru/compose-method
// Goal: Each function does ONE thing at ONE level of abstraction
function processUser(userData: UserInput) {
  const validated = validateUserData(userData);
  const normalized = normalizeUserData(validated);
  const enriched = enrichWithDefaults(normalized);
  return saveUser(enriched);
}
```

## Anti-Patterns

- **Refactoring without tests** - Tests must pass before AND after
- **Big bang refactor** - Small incremental changes
- **Premature abstraction** - Wait for duplication (Rule of 3)
- **Refactoring during feature work** - Separate commits

## Verification Checklist

- [ ] Tests pass before refactoring
- [ ] Tests pass after refactoring
- [ ] Behavior unchanged
- [ ] Each commit is atomic (compilable)
- [ ] Code review before merge
