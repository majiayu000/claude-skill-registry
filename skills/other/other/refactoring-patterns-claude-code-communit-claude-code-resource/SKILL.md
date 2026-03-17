---
name: refactoring-patterns
description: Safe refactoring techniques — extract method, rename, move, inline, and structural patterns. Includes code smell identification and transformation recipes. Use when refactoring code or improving structure.
---

# Refactoring Patterns

## Safety Rules

Before any refactoring, verify all of the following:

- [ ] Tests exist covering the code you will change
- [ ] All tests pass before you start
- [ ] Perform one transformation at a time
- [ ] Run tests after every single transformation
- [ ] Commit after each successful step
- [ ] Name every transformation in your commit message (e.g., "refactor: Extract Method -- validateEmail")
- [ ] Never change behavior and structure in the same commit
- [ ] If a step breaks tests, revert immediately and try a smaller step

## Code Smell Catalog

| Smell                  | Symptoms                                                   | Typical Refactoring                          |
|------------------------|------------------------------------------------------------|----------------------------------------------|
| Long Method            | Method over 20 lines; multiple levels of abstraction       | Extract Method                               |
| Large Class            | Class over 300 lines; too many responsibilities            | Extract Class                                |
| Feature Envy           | Method uses more data from another class than its own      | Move Method                                  |
| Data Clump             | Same group of fields/params appear together repeatedly     | Introduce Parameter Object                   |
| Primitive Obsession    | Using primitives instead of small domain objects           | Replace Primitive with Value Object          |
| Shotgun Surgery        | One change requires edits across many files                | Move Method, Inline Class                    |
| Divergent Change       | One class changed for many different reasons               | Extract Class                                |
| Dead Code              | Unreachable code, unused variables, commented-out blocks   | Remove Dead Code                             |
| Long Parameter List    | Method takes more than 3 parameters                        | Introduce Parameter Object                   |
| Switch Statements      | Repeated switch/if-else on the same type field             | Replace Conditional with Polymorphism        |
| Duplicate Code         | Same logic in multiple places                              | Extract Method, Extract Superclass           |
| Magic Numbers          | Unexplained literal values in logic                        | Replace Magic Number with Named Constant     |

### Smell Examples

**Long Method:**
```typescript
function processOrder(order: Order) {
  // validate (10 lines) + calculate totals (15 lines)
  // apply discounts (12 lines) + check inventory (8 lines)
  // create invoice (10 lines) + send notification (6 lines)
}
```

**Feature Envy:**
```typescript
class Order {
  calculateShipping() {
    if (this.customer.address.country === "US") {
      if (this.customer.tier === "premium") return 0;
      return this.customer.address.isRemote ? 15 : 5;
    }
    return 25;
  }
}
```

**Data Clump:**
```typescript
function createUser(name: string, street: string, city: string, state: string, zip: string) {}
function updateAddress(street: string, city: string, state: string, zip: string) {}
```

## Named Refactorings

| Refactoring                               | Input                             | Output                                 |
|-------------------------------------------|-----------------------------------|----------------------------------------|
| Extract Method                            | Code block inside a method        | New method + call site                 |
| Extract Class                             | Fields and methods from a class   | New class with focused responsibility  |
| Inline Method                             | Trivial method                    | Body placed at all call sites          |
| Rename                                    | Unclear name                      | Intention-revealing name               |
| Move Method                               | Method in wrong class             | Method in the class that owns the data |
| Introduce Parameter Object                | Multiple related parameters       | Single object parameter                |
| Replace Conditional with Polymorphism     | Type-based switch/if-else         | Subclasses with overridden method      |
| Replace Magic Number with Named Constant  | Literal number in code            | Named constant                         |
| Decompose Conditional                     | Complex boolean expression        | Named methods for conditions           |
| Remove Dead Code                          | Unused code                       | Deletion                               |

### Extract Method

**Recipe:** (1) Identify code to extract. (2) Create method with intention-revealing name. (3) Copy code in. (4) Local variables become locals; outer scope reads become parameters; modified-and-used-after become return values. (5) Replace original with call. (6) Run tests.

```typescript
// Before
function printInvoice(invoice: Invoice) {
  console.log("=== Invoice ===");
  let total = 0;
  for (const item of invoice.items) { total += item.price * item.quantity; }
  const tax = total * 0.08;
  console.log(`Total: ${total + tax}`);
}

// After
function printInvoice(invoice: Invoice) {
  console.log("=== Invoice ===");
  console.log(`Total: ${calculateGrandTotal(invoice.items)}`);
}

function calculateGrandTotal(items: InvoiceItem[]): number {
  const subtotal = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  return subtotal + subtotal * 0.08;
}
```

### Extract Class

**Recipe:** (1) Identify cohesive fields and methods. (2) Create new class. (3) Move fields. (4) Move methods. (5) Delegate from original. (6) Run tests after each move.

```typescript
// Before
class User {
  name: string; email: string;
  street: string; city: string; state: string; zip: string;
  fullAddress(): string { return `${this.street}, ${this.city}, ${this.state} ${this.zip}`; }
}

// After
class Address {
  constructor(public street: string, public city: string, public state: string, public zip: string) {}
  full(): string { return `${this.street}, ${this.city}, ${this.state} ${this.zip}`; }
}

class User {
  name: string; email: string; address: Address;
}
```

### Introduce Parameter Object

**Recipe:** (1) Create type for the parameter group. (2) Add object parameter. (3) Update callers. (4) Remove old params. (5) Run tests.

```typescript
// Before
function searchProducts(minPrice: number, maxPrice: number, category: string, inStock: boolean) {}

// After
interface ProductFilter { minPrice: number; maxPrice: number; category: string; inStock: boolean; }
function searchProducts(filter: ProductFilter) {}
```

### Replace Conditional with Polymorphism

**Recipe:** (1) Create base interface with the varying method. (2) Create subclass per case. (3) Move case logic into subclass. (4) Replace conditional with method call. (5) Run tests.

```typescript
// Before
function calculateArea(shape: Shape): number {
  switch (shape.type) {
    case "circle":    return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    case "triangle":  return (shape.base * shape.height) / 2;
  }
}

// After
interface Shape { area(): number; }
class Circle implements Shape {
  constructor(private radius: number) {}
  area() { return Math.PI * this.radius ** 2; }
}
class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area() { return this.width * this.height; }
}
class Triangle implements Shape {
  constructor(private base: number, private height: number) {}
  area() { return (this.base * this.height) / 2; }
}
```

### Decompose Conditional

**Recipe:** (1) Extract condition into a named method. (2) Extract then-branch if non-trivial. (3) Extract else-branch if non-trivial. (4) Run tests.

```typescript
// Before
if (date.getMonth() >= 5 && date.getMonth() <= 8 && !isHoliday(date)) {
  rate = quantity * summerRate;
} else {
  rate = quantity * regularRate + serviceFee;
}

// After
if (isSummerBusinessDay(date)) { rate = summerCharge(quantity); }
else { rate = regularCharge(quantity); }
```

### Remove Dead Code

**Recipe:** (1) Verify truly unused (search references, check exports). (2) Delete. (3) Run tests. (4) Commit as `refactor: Remove Dead Code -- <what>`.

Dead code includes: unreachable branches, unused functions, commented-out blocks, unused variables and imports, removed feature flag code. Never comment out code "for later" -- version control preserves history.

## Strangler Fig Pattern

For large-scale refactors that cannot be completed in a single step:

1. **Identify the boundary** of the legacy code to replace
2. **Build the new implementation** alongside the old one
3. **Route traffic incrementally** using a facade or feature flag
4. **Verify each increment** in production
5. **Remove the old implementation** once all traffic uses the new code

```typescript
// Step 1: Facade delegates to old code
class PaymentProcessor {
  process(payment: Payment): Result { return this.legacyProcessor.process(payment); }
}

// Step 2-3: Route with feature flag
class PaymentProcessor {
  process(payment: Payment): Result {
    if (featureFlag.isEnabled("new-payment-processor"))
      return this.newProcessor.process(payment);
    return this.legacyProcessor.process(payment);
  }
}

// Step 4-5: After verification, remove old code
class PaymentProcessor {
  process(payment: Payment): Result { return this.newProcessor.process(payment); }
}
```

### Strangler Fig Checklist

- [ ] Both old and new paths are tested
- [ ] Rollback is possible at every stage by toggling the flag
- [ ] Monitoring and alerts cover both paths
- [ ] Old code is deleted only after the new path is proven in production

## Refactoring Workflow Summary

```
1. Identify the smell
2. Choose the named refactoring
3. Verify tests pass (write them if missing)
4. Apply one transformation
5. Run tests
6. Commit: "refactor: <Refactoring Name> -- <target>"
7. Repeat from step 4 until the smell is resolved
```
