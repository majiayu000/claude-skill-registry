---
name: refactor-helper
description: Refactor code to improve quality, performance, and maintainability. Use when refactoring code, improving code structure, or modernizing legacy code.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Refactor Helper

**Version**: 1.0.0
**Purpose**: Safe, systematic code refactoring

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Refactor | "refactor this", "リファクタリングして", "clean up code" |
| Improve | "improve this code", "コード改善" |
| Modernize | "update to modern syntax", "モダン化" |

---

## Refactoring Principles

### 1. Make Small Changes

```
✅ GOOD: One refactoring per commit
❌ BAD: Multiple unrelated changes in one commit
```

### 2. Ensure Tests Pass

```bash
# Before refactoring
npm test

# After each change
npm test
```

### 3. Keep Behavior Unchanged

```
Refactoring = Improving structure WITHOUT changing behavior
```

---

## Common Patterns

### Extract Function

```typescript
// Before
function processOrder(order: Order) {
  // validate
  if (!order.items.length) throw new Error('Empty');
  if (order.total < 0) throw new Error('Invalid total');

  // calculate
  const subtotal = order.items.reduce((s, i) => s + i.price, 0);
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  // save
  db.save({ ...order, total });
}

// After
function validateOrder(order: Order): void {
  if (!order.items.length) throw new Error('Empty');
  if (order.total < 0) throw new Error('Invalid total');
}

function calculateTotal(items: Item[]): number {
  const subtotal = items.reduce((s, i) => s + i.price, 0);
  const tax = subtotal * 0.1;
  return subtotal + tax;
}

function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order.items);
  db.save({ ...order, total });
}
```

### Replace Conditionals with Polymorphism

```typescript
// Before
function getPrice(type: string, base: number): number {
  switch (type) {
    case 'premium': return base * 0.8;
    case 'vip': return base * 0.7;
    default: return base;
  }
}

// After
interface PricingStrategy {
  calculate(base: number): number;
}

class RegularPricing implements PricingStrategy {
  calculate(base: number) { return base; }
}

class PremiumPricing implements PricingStrategy {
  calculate(base: number) { return base * 0.8; }
}
```

### Simplify Conditionals

```typescript
// Before
if (user !== null && user !== undefined && user.isActive === true) {
  if (user.role === 'admin' || user.role === 'moderator') {
    // ...
  }
}

// After
const isActiveUser = user?.isActive ?? false;
const hasPrivileges = ['admin', 'moderator'].includes(user?.role ?? '');

if (isActiveUser && hasPrivileges) {
  // ...
}
```

### Remove Dead Code

```bash
# Find unused exports
npx ts-prune

# Find unused dependencies
npx depcheck
```

---

## Workflow

### Step 1: Identify Smell

| Code Smell | Refactoring |
|------------|-------------|
| Long function | Extract Function |
| Duplicate code | Extract and reuse |
| Complex conditionals | Simplify/Polymorphism |
| God class | Split responsibilities |
| Feature envy | Move method |

### Step 2: Write Tests (if missing)

```typescript
describe('processOrder', () => {
  it('should calculate total correctly', () => {
    const order = { items: [{ price: 100 }] };
    expect(processOrder(order).total).toBe(110);
  });
});
```

### Step 3: Refactor

Small, incremental changes with tests after each.

### Step 4: Verify

```bash
npm test
npm run lint
npm run typecheck
```

---

## Checklist

- [ ] Tests exist and pass before refactoring
- [ ] Each change is small and focused
- [ ] Tests pass after each change
- [ ] No behavior changes
- [ ] Code is more readable
- [ ] Commit with clear message
