---
name: arcanea-refactoring-ritual
description: Transform messy code into clean code through disciplined refactoring. Code smells, refactoring patterns, and the courage to improve without breaking. Leave every codebase better than you found it.
version: 2.0.0
author: Arcanea
tags: [refactoring, clean-code, patterns, maintenance, quality, development]
triggers:
  - refactoring
  - clean up
  - code smells
  - improve code
  - legacy code
  - technical debt
---

# The Refactoring Ritual

> *"Refactoring is not about rewriting. It's about improving structure while preserving behavior, one small step at a time."*

---

## The Refactoring Philosophy

### What Is Refactoring?

```
REFACTORING IS:
• Improving code structure
• Without changing behavior
• In small, safe steps
• With tests as your safety net

REFACTORING IS NOT:
• Rewriting from scratch
• Adding features
• Fixing bugs
• Performance optimization
```

### The Refactoring Mantra

```
╔═══════════════════════════════════════════════════════════════════╗
║                    THE REFACTORING CYCLE                           ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   1. DETECT    │ Notice the smell                                 ║
║   2. TEST      │ Ensure coverage exists                           ║
║   3. REFACTOR  │ Apply one transformation                         ║
║   4. VERIFY    │ Run tests, confirm behavior                      ║
║   5. COMMIT    │ Save the improvement                             ║
║   6. REPEAT    │ Next smell                                       ║
║                                                                    ║
║   Never do step 3 without step 2.                                 ║
║   Never skip step 4.                                              ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Code Smells

### The Smell Catalog

```
BLOATERS (Too Big):
• Long Method          - Method doing too much
• Large Class          - Class with too many responsibilities
• Long Parameter List  - Method needs too many inputs
• Data Clumps          - Same data appears together repeatedly
• Primitive Obsession  - Overuse of primitives vs objects

OBJECT-ORIENTATION ABUSERS:
• Switch Statements    - Type checking instead of polymorphism
• Parallel Inheritance - Subclass in one hierarchy forces another
• Refused Bequest      - Subclass doesn't use parent's gifts
• Alternative Classes  - Different classes, same interface

CHANGE PREVENTERS:
• Divergent Change     - One class changed for multiple reasons
• Shotgun Surgery      - One change requires many class edits
• Parallel Inheritance - (see above)

DISPENSABLES (Can Remove):
• Comments             - Explaining bad code
• Dead Code            - Unreachable code
• Speculative Generality - "We might need this someday"
• Duplicate Code       - Same logic in multiple places
• Lazy Class           - Class that doesn't do enough
• Data Class           - Class with only getters/setters

COUPLERS (Too Connected):
• Feature Envy         - Method uses another class more than its own
• Inappropriate Intimacy - Classes know too much about each other
• Message Chains       - a.getB().getC().getD().doThing()
• Middle Man           - Class that only delegates
```

---

## Refactoring Patterns

### Extract Method

```
BEFORE:
┌────────────────────────────────────────────────────────────────┐
│ function printOrder(order) {                                   │
│     console.log("Order Details:");                             │
│     console.log("Customer: " + order.customer);                │
│     console.log("Items:");                                     │
│     for (const item of order.items) {                          │
│         console.log("  - " + item.name + ": $" + item.price);  │
│     }                                                          │
│     let total = 0;                                             │
│     for (const item of order.items) {                          │
│         total += item.price;                                   │
│     }                                                          │
│     console.log("Total: $" + total);                           │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

AFTER:
┌────────────────────────────────────────────────────────────────┐
│ function printOrder(order) {                                   │
│     printHeader(order);                                        │
│     printItems(order.items);                                   │
│     printTotal(order.items);                                   │
│ }                                                              │
│                                                                │
│ function printHeader(order) {                                  │
│     console.log("Order Details:");                             │
│     console.log("Customer: " + order.customer);                │
│ }                                                              │
│                                                                │
│ function printItems(items) {                                   │
│     console.log("Items:");                                     │
│     for (const item of items) {                                │
│         console.log("  - " + item.name + ": $" + item.price);  │
│     }                                                          │
│ }                                                              │
│                                                                │
│ function printTotal(items) {                                   │
│     const total = items.reduce((sum, item) => sum + item.price, 0);│
│     console.log("Total: $" + total);                           │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘
```

### Replace Conditional with Polymorphism

```
BEFORE:
┌────────────────────────────────────────────────────────────────┐
│ function getSpeed(vehicle) {                                   │
│     switch (vehicle.type) {                                    │
│         case 'car':                                            │
│             return vehicle.baseSpeed * 1.2;                    │
│         case 'bicycle':                                        │
│             return vehicle.baseSpeed * 0.5;                    │
│         case 'plane':                                          │
│             return vehicle.baseSpeed * 10;                     │
│     }                                                          │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

AFTER:
┌────────────────────────────────────────────────────────────────┐
│ class Vehicle {                                                │
│     getSpeed() { return this.baseSpeed; }                      │
│ }                                                              │
│                                                                │
│ class Car extends Vehicle {                                    │
│     getSpeed() { return this.baseSpeed * 1.2; }                │
│ }                                                              │
│                                                                │
│ class Bicycle extends Vehicle {                                │
│     getSpeed() { return this.baseSpeed * 0.5; }                │
│ }                                                              │
│                                                                │
│ class Plane extends Vehicle {                                  │
│     getSpeed() { return this.baseSpeed * 10; }                 │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘
```

### Introduce Parameter Object

```
BEFORE:
┌────────────────────────────────────────────────────────────────┐
│ function createUser(name, email, age, country, city, zipCode) {│
│     // ...                                                     │
│ }                                                              │
│                                                                │
│ function updateUser(id, name, email, age, country, city, zip) {│
│     // ...                                                     │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

AFTER:
┌────────────────────────────────────────────────────────────────┐
│ interface UserData {                                           │
│     name: string;                                              │
│     email: string;                                             │
│     age: number;                                               │
│     address: Address;                                          │
│ }                                                              │
│                                                                │
│ interface Address {                                            │
│     country: string;                                           │
│     city: string;                                              │
│     zipCode: string;                                           │
│ }                                                              │
│                                                                │
│ function createUser(data: UserData) { ... }                    │
│ function updateUser(id: string, data: UserData) { ... }        │
└────────────────────────────────────────────────────────────────┘
```

### Replace Magic Number with Constant

```
BEFORE:
┌────────────────────────────────────────────────────────────────┐
│ if (user.age >= 18) {                                          │
│     // allow access                                            │
│ }                                                              │
│                                                                │
│ const discount = price * 0.15;                                 │
│                                                                │
│ setTimeout(callback, 86400000);                                │
└────────────────────────────────────────────────────────────────┘

AFTER:
┌────────────────────────────────────────────────────────────────┐
│ const LEGAL_AGE = 18;                                          │
│ const MEMBER_DISCOUNT_RATE = 0.15;                             │
│ const ONE_DAY_MS = 24 * 60 * 60 * 1000;                        │
│                                                                │
│ if (user.age >= LEGAL_AGE) {                                   │
│     // allow access                                            │
│ }                                                              │
│                                                                │
│ const discount = price * MEMBER_DISCOUNT_RATE;                 │
│                                                                │
│ setTimeout(callback, ONE_DAY_MS);                              │
└────────────────────────────────────────────────────────────────┘
```

---

## Working with Legacy Code

### The Legacy Code Dilemma

```
CHALLENGE:
Legacy code often has no tests.
You can't refactor without tests.
You can't add tests without refactoring.

SOLUTION: Characterization Tests
┌────────────────────────────────────────────────────────────────┐
│ 1. Call the code you want to change                            │
│ 2. Write assertions based on ACTUAL output                     │
│ 3. This documents current behavior                             │
│ 4. Now you can safely refactor                                 │
│                                                                │
│ // Characterization test                                       │
│ test('calculateTotal returns what it returns', () => {         │
│     const result = calculateTotal(items);                      │
│     expect(result).toBe(157.23); // Whatever it actually is    │
│ });                                                            │
└────────────────────────────────────────────────────────────────┘
```

### The Strangler Pattern for Legacy

```
┌─────────────────────────────────────────────────────────────────┐
│                    STRANGLER REFACTORING                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Identify a seam (boundary in the code)                      │
│  2. Write tests for behavior at that seam                       │
│  3. Introduce new implementation alongside old                  │
│  4. Route traffic to new implementation                         │
│  5. Remove old implementation when safe                         │
│                                                                  │
│  Phase 1:     Phase 2:     Phase 3:     Phase 4:                │
│  ┌─────┐      ┌─────┐      ┌─────┐      ┌─────┐                 │
│  │ Old │      │ Old │      │ Old │      │     │                 │
│  │     │  →   │─────│  →   │═════│  →   │ New │                 │
│  │     │      │ New │      │ New │      │     │                 │
│  └─────┘      └─────┘      └─────┘      └─────┘                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Breaking Dependencies

```
DEPENDENCY INJECTION:
┌────────────────────────────────────────────────────────────────┐
│ BEFORE (Hard to test):                                         │
│ class OrderService {                                           │
│     process(order) {                                           │
│         const db = new Database();  // ← Hard dependency       │
│         db.save(order);                                        │
│     }                                                          │
│ }                                                              │
│                                                                │
│ AFTER (Testable):                                              │
│ class OrderService {                                           │
│     constructor(database) {                                    │
│         this.database = database;   // ← Injected             │
│     }                                                          │
│     process(order) {                                           │
│         this.database.save(order);                             │
│     }                                                          │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘
```

---

## Safe Refactoring Techniques

### The Mikado Method

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE MIKADO METHOD                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Set a goal (the refactoring you want)                       │
│  2. Try to achieve it directly                                  │
│  3. When it breaks, note what needs to change first             │
│  4. Revert your changes                                         │
│  5. Achieve the prerequisite first                              │
│  6. Repeat until goal is achievable                             │
│                                                                  │
│  Goal: Rename UserManager to UserService                        │
│                    │                                             │
│         ┌─────────┴─────────┐                                   │
│         ▼                   ▼                                   │
│  Update imports      Update config                              │
│         │                   │                                   │
│         ▼                   ▼                                   │
│  Fix tests          Fix dependency injection                    │
│                                                                  │
│  Work from leaves to root.                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Parallel Change (Expand-Migrate-Contract)

```
PHASE 1: EXPAND
┌────────────────────────────────────────────────────────────────┐
│ Add new interface alongside old                                 │
│                                                                │
│ // Old interface still works                                   │
│ function getUser(id) { ... }                                   │
│                                                                │
│ // New interface added                                         │
│ function getUserById(id) { ... }                               │
└────────────────────────────────────────────────────────────────┘

PHASE 2: MIGRATE
┌────────────────────────────────────────────────────────────────┐
│ Update callers to use new interface                            │
│                                                                │
│ // Old: still works but deprecated                             │
│ // New: callers being updated                                  │
└────────────────────────────────────────────────────────────────┘

PHASE 3: CONTRACT
┌────────────────────────────────────────────────────────────────┐
│ Remove old interface when all callers migrated                 │
│                                                                │
│ // Only new interface remains                                  │
│ function getUserById(id) { ... }                               │
└────────────────────────────────────────────────────────────────┘
```

---

## Refactoring Catalog

### Quick Reference

```
┌──────────────────────────────────────────────────────────────────┐
│ SMELL                    │ REFACTORING                           │
├──────────────────────────┼───────────────────────────────────────┤
│ Long Method              │ Extract Method                        │
│ Large Class              │ Extract Class                         │
│ Long Parameter List      │ Introduce Parameter Object            │
│ Duplicate Code           │ Extract Method, Pull Up Method        │
│ Feature Envy             │ Move Method                           │
│ Switch Statements        │ Replace with Polymorphism             │
│ Primitive Obsession      │ Replace Primitive with Object         │
│ Data Clumps              │ Extract Class                         │
│ Shotgun Surgery          │ Move Method, Inline Class             │
│ Divergent Change         │ Extract Class                         │
│ Middle Man               │ Remove Middle Man                     │
│ Message Chains           │ Hide Delegate                         │
│ Comments                 │ Extract Method, Rename                │
│ Magic Numbers            │ Replace with Symbolic Constant        │
│ Dead Code                │ Remove Dead Code                      │
└──────────────────────────┴───────────────────────────────────────┘
```

---

## Refactoring Checklist

```
BEFORE REFACTORING:
□ Tests exist and pass
□ Code is under version control
□ Goal is clear
□ Scope is limited

DURING REFACTORING:
□ One change at a time
□ Tests run after each change
□ Commit frequently
□ No new features

AFTER REFACTORING:
□ All tests still pass
□ Code is cleaner
□ Behavior unchanged
□ Documented if needed
```

### The Refactoring Mantras

```
"Make it work, make it right, make it fast"
"Leave the code better than you found it"
"Small steps, always working"
"Tests are your safety net"
"The best refactoring is invisible to users"
```

---

*"Refactoring is an investment in the future. Every improvement compounds, making the next change easier."*
