---
name: code-refactoring-patterns
description: Systematic approach to refactoring code for improved maintainability, performance, and clarity while preserving functionality
license: MIT
metadata:
  adapted-by: ai-skills
  category: code-quality
---

# Code Refactoring Patterns

A comprehensive guide to refactoring code systematically while maintaining functionality and improving quality.

## When to Refactor

- Code smells detected (duplicated code, long functions, etc.)
- Before adding new features to complex areas
- After understanding improves ("now I see a better way")
- When tests are in place
- Performance optimization needed

## Refactoring Rules

1. **Never refactor without tests**: Write tests first if they don't exist
2. **Small steps**: Make one change at a time
3. **Run tests after each change**: Ensure nothing breaks
4. **Commit often**: Each working refactor is a commit
5. **Don't mix refactoring with feature work**: Separate concerns

## Common Code Smells

### 1. Long Method/Function

**Smell**: Functions over 20-30 lines

**Refactor**: Extract Method

```typescript
// Before
function processOrder(order: Order) {
  // Validate order (10 lines)
  // Calculate totals (15 lines)
  // Apply discounts (12 lines)
  // Send confirmation (8 lines)
}

// After
function processOrder(order: Order) {
  validateOrder(order);
  const totals = calculateTotals(order);
  const finalPrice = applyDiscounts(totals, order);
  sendConfirmation(order, finalPrice);
}
```

### 2. Duplicated Code

**Smell**: Same code in multiple places

**Refactor**: Extract Function/Class

```typescript
// Before
function formatUserName(user: User) {
  return `${user.firstName} ${user.lastName}`;
}

function formatAuthorName(author: Author) {
  return `${author.firstName} ${author.lastName}`;
}

// After
function formatFullName(person: { firstName: string; lastName: string }) {
  return `${person.firstName} ${person.lastName}`;
}
```

### 3. Long Parameter List

**Smell**: Functions with 4+ parameters

**Refactor**: Parameter Object

```typescript
// Before
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  phone: string,
  address: string
) { }

// After
interface UserDetails {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: string;
}

function createUser(details: UserDetails) { }
```

### 4. Large Class

**Smell**: Classes with many responsibilities

**Refactor**: Extract Class

```typescript
// Before
class UserManager {
  createUser() { }
  deleteUser() { }
  sendEmail() { }
  generateReport() { }
  logActivity() { }
}

// After
class UserService {
  createUser() { }
  deleteUser() { }
}

class EmailService {
  sendEmail() { }
}

class ReportService {
  generateReport() { }
}
```

### 5. Feature Envy

**Smell**: Method uses data from another class more than its own

**Refactor**: Move Method

```typescript
// Before
class Order {
  calculate() {
    return this.customer.getDiscount() * this.amount;
  }
}

// After
class Customer {
  calculateOrderAmount(order: Order) {
    return this.getDiscount() * order.amount;
  }
}
```

## Refactoring Techniques

### Extract Method

Break large functions into smaller, named pieces:

```typescript
// Before
function renderUser(user: User) {
  console.log(`<div>`);
  console.log(`  <h1>${user.firstName} ${user.lastName}</h1>`);
  console.log(`  <p>${user.email}</p>`);
  console.log(`</div>`);
}

// After
function renderUser(user: User) {
  console.log(`<div>`);
  console.log(`  ${renderUserHeader(user)}`);
  console.log(`  ${renderUserEmail(user)}`);
  console.log(`</div>`);
}

function renderUserHeader(user: User) {
  return `<h1>${user.firstName} ${user.lastName}</h1>`;
}

function renderUserEmail(user: User) {
  return `<p>${user.email}</p>`;
}
```

### Rename for Clarity

Use descriptive names:

```typescript
// Before
function calc(a: number, b: number) {
  return a * b * 0.08;
}

// After
function calculateSalesTax(amount: number, quantity: number) {
  const TAX_RATE = 0.08;
  return amount * quantity * TAX_RATE;
}
```

### Introduce Explaining Variable

Make complex expressions clear:

```typescript
// Before
if (platform.toUpperCase().includes('MAC') && 
    browser.toUpperCase().includes('IE') &&
    wasInitialized() && resized) {
  // do something
}

// After
const isMacOS = platform.toUpperCase().includes('MAC');
const isIE = browser.toUpperCase().includes('IE');
const wasResized = wasInitialized() && resized;

if (isMacOS && isIE && wasResized) {
  // do something
}
```

### Replace Conditional with Polymorphism

Use inheritance/interfaces instead of switch/if-else chains:

```typescript
// Before
function getSpeed(vehicle: Vehicle) {
  switch (vehicle.type) {
    case 'car': return vehicle.speed * 1.0;
    case 'bike': return vehicle.speed * 0.8;
    case 'truck': return vehicle.speed * 0.6;
  }
}

// After
interface Vehicle {
  getSpeed(): number;
}

class Car implements Vehicle {
  getSpeed() { return this.speed * 1.0; }
}

class Bike implements Vehicle {
  getSpeed() { return this.speed * 0.8; }
}
```

### Simplify Conditional Logic

Use early returns and guard clauses:

```typescript
// Before
function processPayment(payment: Payment) {
  if (payment.isValid()) {
    if (payment.amount > 0) {
      if (payment.method === 'card') {
        // process card payment
      } else {
        // invalid method
      }
    } else {
      // invalid amount
    }
  } else {
    // invalid payment
  }
}

// After
function processPayment(payment: Payment) {
  if (!payment.isValid()) {
    throw new Error('Invalid payment');
  }
  
  if (payment.amount <= 0) {
    throw new Error('Invalid amount');
  }
  
  if (payment.method !== 'card') {
    throw new Error('Invalid method');
  }
  
  // process card payment
}
```

## Refactoring Workflow

### Step 1: Understand Current Code

```bash
# Read the code thoroughly
cat src/feature.ts

# Check tests
cat src/feature.test.ts

# Find all usages
grep -r "functionName" src/
```

### Step 2: Ensure Tests Exist

```bash
# Run existing tests
npm test src/feature.test.ts

# Add missing tests if needed
```

### Step 3: Refactor in Small Steps

```bash
# Make one refactoring change
# Run tests
npm test

# Commit if tests pass
git add . && git commit -m "refactor: extract method calculateTotal"

# Repeat for next refactoring
```

### Step 4: Verify No Regression

```bash
# Run full test suite
npm test

# Check type errors
npx tsc --noEmit

# Verify lint
npm run lint
```

### Step 5: Performance Check

```bash
# Compare before/after if performance-critical
npm run benchmark
```

## Refactoring Checklist

Before refactoring:
- [ ] Tests exist and pass
- [ ] Understand current behavior
- [ ] Know why refactoring is needed
- [ ] Have time to complete refactoring

During refactoring:
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Keep commits small and focused
- [ ] Don't add features during refactoring

After refactoring:
- [ ] All tests pass
- [ ] No type errors
- [ ] Lint passes
- [ ] Code review completed
- [ ] Documentation updated if needed

## Integration Points

Complements:
- **verification-loop**: For validation after refactoring
- **tdd-workflow**: For test-first approach
- **coding-standards-enforcer**: For style consistency
- **testing-patterns**: For test design

## Refactoring Anti-Patterns

❌ **Don't**:
- Refactor without tests
- Mix refactoring with feature work
- Make large changes at once
- Refactor code you don't understand
- Skip verification steps

✅ **Do**:
- Write tests first
- Separate refactoring commits
- Make incremental changes
- Understand code before refactoring
- Run tests frequently
