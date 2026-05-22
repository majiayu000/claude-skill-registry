---
name: Software Design Principles
description: Object-oriented design principles including object calisthenics, dependency inversion, fail-fast error handling, feature envy detection, and intention-revealing naming. Activates during code refactoring, design reviews, or when user requests design improvements.
---

# GitHub Copilot Skill: software-design-principles

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz) 
> for use with GitHub Copilot Agent Skills.

---

# Software Design Principles

Professional software design patterns and principles for writing maintainable, well-structured code.

## Critical Rules

🚨 **Fail-fast over silent fallbacks.** Never use fallback chains (`value ?? backup ?? 'unknown'`). If data should exist, validate and throw a clear error.

🚨 **No `any`. No `as`.** Type escape hatches defeat TypeScript's purpose. There's always a type-safe solution.

🚨 **Make illegal states unrepresentable.** Use discriminated unions, not optional fields. If a state combination shouldn't exist, make the type system forbid it.

🚨 **Inject dependencies, don't instantiate.** No `new SomeService()` inside methods. Pass dependencies through constructors.

🚨 **Intention-revealing names only.** Never use `data`, `utils`, `helpers`, `handler`, `processor`. Name things for what they do in the domain.

🚨 **No code comments.** Comments are a failure to express intent in code. If you need a comment to explain what code does, the code isn't clear enough—refactor it.

🚨 **Use Zod for runtime validation.** In TypeScript, use Zod schemas for parsing external data, API responses, and user input. Type inference from schemas keeps types and validation in sync.

## When This Applies

- Writing new code (these are defaults, not just refactoring goals)
- Refactoring existing code
- Code reviews and design reviews
- During TDD REFACTOR phase
- When analyzing coupling and cohesion

## Core Philosophy

Well-designed, maintainable code is far more important than getting things done quickly. Every design decision should favor:
- **Clarity over cleverness**
- **Explicit over implicit**
- **Fail-fast over silent fallbacks**
- **Loose coupling over tight integration**
- **Intention-revealing over generic**

## Code Without Comments

**Principle:** Never write code comments - prefer to write expressive code.

Well-named functions, classes, and variables should make the code self-documenting. Comments are often a sign that the code isn't clear enough.

**Instead of comments, use:**
- Intention-revealing names
- Small, focused functions
- Clear structure
- Domain language

**Bad (needs comments):**
```typescript
// Check if user can access resource
function check(u: User, r: Resource): boolean {
  // Admin users bypass all checks
  if (u.role === 'admin') return true
  // Check ownership
  if (r.ownerId === u.id) return true
  // Check shared access
  return r.sharedWith.includes(u.id)
}
```

**Good (self-documenting):**
```typescript
function canUserAccessResource(user: User, resource: Resource): boolean {
  if (user.isAdmin()) return true
  if (resource.isOwnedBy(user)) return true
  return resource.isSharedWith(user)
}
```

The code reads like prose - no comments needed.

## Object Calisthenics

Apply object calisthenics strictly to all code. Refactor existing code to comply with these principles:

### The Nine Rules

1. **One level of indentation per method**
   - Improves readability
   - Forces extraction of helper methods
   - Makes code easier to test

2. **Don't use the ELSE keyword**
   - Use early returns instead
   - Reduces nesting
   - Clarifies happy path

3. **Wrap all primitives and strings**
   - Create value objects
   - Encapsulate validation logic
   - Make domain concepts explicit

4. **First class collections**
   - Classes with collections should contain nothing else
   - Enables collection-specific operations
   - Improves cohesion

5. **One dot per line**
   - Reduces coupling
   - Prevents feature envy
   - Honors Law of Demeter

6. **Don't abbreviate**
   - Use full, descriptive names
   - Code is read more than written
   - Self-documenting code reduces comments

7. **Keep all entities small**
   - Small classes (< 150 lines)
   - Small methods (< 10 lines)
   - Small packages/modules
   - Easier to understand and maintain

8. **No classes with more than two instance variables**
   - High cohesion
   - Clear single responsibility
   - Easier to test

9. **No getters/setters/properties**
   - Tell, don't ask
   - Objects should do work, not expose data
   - Prevents feature envy

### When to Apply

**During refactoring:**
- Review code against all nine rules
- Identify violations
- Refactor to comply
- Verify tests still pass after each change

**During code review:**
- Check new code complies with calisthenics
- Suggest refactorings for violations
- Explain rationale using domain language

## Feature Envy Detection

**What is Feature Envy?**
When a method in one class is more interested in the data or behavior of another class than its own.

### Warning Signs

```typescript
// FEATURE ENVY - method is obsessed with Order's data
class InvoiceGenerator {
  generate(order: Order): Invoice {
    const total = order.getItems()
      .map(item => item.getPrice() * item.getQuantity())
      .reduce((sum, val) => sum + val, 0)

    const tax = total * order.getTaxRate()
    const shipping = order.calculateShipping()

    return new Invoice(total + tax + shipping)
  }
}
```

This method should live in the `Order` class - it's using Order's data extensively.

### How to Fix

**Move the method to the class it envies:**

```typescript
class Order {
  calculateTotal(): number {
    const subtotal = this.items
      .map(item => item.getPrice() * item.getQuantity())
      .reduce((sum, val) => sum + val, 0)

    const tax = subtotal * this.taxRate
    const shipping = this.calculateShipping()

    return subtotal + tax + shipping
  }
}

class InvoiceGenerator {
  generate(order: Order): Invoice {
    return new Invoice(order.calculateTotal())
  }
}
```

### Detection Protocol

During refactoring:
1. For each method, count references to external objects vs own object
2. If external references > own references → likely feature envy
3. Consider moving method to the envied class
4. Re-run tests to verify behavior preserved

## Dependency Inversion Principle

**Principle:** Depend on abstractions, not concretions. Do not directly instantiate dependencies within methods.

### The Problem: Hard Dependencies

```typescript
// TIGHT COUPLING - hard dependency
class OrderProcessor {
  process(order: Order): void {
    const validator = new OrderValidator()  // ❌ Direct instantiation
    if (!validator.isValid(order)) {
      throw new Error('Invalid order')
    }

    const emailer = new EmailService()  // ❌ Direct instantiation
    emailer.send(order.customerEmail, 'Order confirmed')
  }
}
```

**Issues:**
- Hard to test (can't mock dependencies)
- Hard to change (coupled to concrete implementations)
- Hidden dependencies (not visible in constructor)
- Violates Single Responsibility (creates AND uses)

### The Solution: Dependency Inversion

```typescript
// LOOSE COUPLING - dependencies injected
class OrderProcessor {
  constructor(
    private validator: OrderValidator,
    private emailer: EmailService
  ) {}

  process(order: Order): void {
    if (!this.validator.isValid(order)) {
      throw new Error('Invalid order')
    }

    this.emailer.send(order.customerEmail, 'Order confirmed')
  }
}
```

**Benefits:**
- Easy to test (inject mocks)
- Easy to change (swap implementations)
- Explicit dependencies (visible in constructor)
- Single Responsibility (only uses, doesn't create)

### Application Rules

**NEVER do this:**
```typescript
const service = new SomeService()  // ❌ Direct instantiation
const result = SomeUtil.staticMethod()  // ❌ Static method call
```

**ALWAYS do this:**
```typescript
this.service.doWork()  // ✓ Use injected dependency
this.util.calculate()  // ✓ Delegate to dependency
```

### Enforcement

During refactoring:
- Scan for `new` keywords inside methods (except value objects)
- Scan for static method calls to other classes
- Extract to constructor parameters or method parameters
- Verify tests pass after injection

## Fail-Fast Error Handling

**Principle:** Do not fall back to whatever data is available when expected data is missing. FAIL FAST with clear errors.

### The Problem: Silent Fallbacks

```typescript
// SILENT FAILURE - hides the problem
function extractName(content: Content): string {
  return content.eventType ?? content.className ?? 'Unknown'
}
```

**Issues:**
- You never know that `eventType` is missing
- 'Unknown' propagates through system
- Hard to debug when it causes issues later
- Masks real problems

### The Solution: Explicit Validation

```typescript
// FAIL FAST - immediate, clear error
function extractName(content: Content): string {
  if (!content.eventType) {
    throw new Error(
      `Expected 'eventType' to exist in content, but it was not found. ` +
      `Content keys: [${Object.keys(content).join(', ')}]`
    )
  }
  return content.eventType
}
```

**Benefits:**
- Fails immediately at the source
- Clear error message shows exactly what's wrong
- Easy to debug (stack trace points to problem)
- Forces fixing the root cause

### Application Rules

**NEVER use fallback chains:**
```typescript
value ?? backup ?? default ?? 'unknown'  // ❌
```

**ALWAYS validate and fail explicitly:**
```typescript
if (!value) {
  throw new Error(`Expected value, got ${value}. Context: ${debug}`)
}
return value  // ✓
```

### When to Apply

**During implementation:**
- When accessing data that "should" exist
- When preconditions must be met
- When invariants must hold

**Error message format:**
```typescript
throw new Error(
  `Expected [what you expected]. ` +
  `Got [what you actually got]. ` +
  `Context: [helpful debugging info like available keys, current state, etc.]`
)
```

## Naming Conventions

**Principle:** Use business domain terminology and intention-revealing names. Never use generic programmer jargon.

### Forbidden Generic Names

**NEVER use these names:**
- `data`
- `utils`
- `helpers`
- `common`
- `shared`
- `manager`
- `handler`
- `processor`

These names are meaningless - they tell you nothing about what the code actually does.

### Intention-Revealing Names

**Instead of generic names, use specific domain language:**

```typescript
// ❌ GENERIC - meaningless
class DataProcessor {
  processData(data: any): any {
    const utils = new DataUtils()
    return utils.transform(data)
  }
}

// ✓ INTENTION-REVEALING - clear purpose
class OrderTotalCalculator {
  calculateTotal(order: Order): Money {
    const taxCalculator = new TaxCalculator()
    return taxCalculator.applyTax(order.subtotal, order.taxRate)
  }
}
```

### Naming Checklist

**For classes:**
- Does the name reveal what the class is responsible for?
- Is it a noun (or noun phrase) from the domain?
- Would a domain expert recognize this term?

**For methods:**
- Does the name reveal what the method does?
- Is it a verb (or verb phrase)?
- Does it describe the business operation?

**For variables:**
- Does the name reveal what the variable contains?
- Is it specific to this context?
- Could someone understand it without reading the code?

### Refactoring Generic Names

When you encounter generic names:

1. **Understand the purpose**: What is this really doing?
2. **Ask domain experts**: What would they call this?
3. **Extract domain concept**: Is there a domain term for this?
4. **Rename comprehensively**: Update all references
5. **Verify tests**: Ensure behavior unchanged

### Examples

```typescript
// ❌ GENERIC
function getData(id: string): any
const userHelpers = new UserHelpers()
const result = processData(input)

// ✓ SPECIFIC
function findCustomerById(customerId: string): Customer
const addressValidator = new AddressValidator()
const confirmedOrder = confirmOrder(pendingOrder)
```

## Type-Driven Design

**Principle:** Follow Scott Wlaschin's type-driven approach to domain modeling. Express domain concepts using the type system.

### Make Illegal States Unrepresentable

Use types to encode business rules:

```typescript
// ❌ PRIMITIVE OBSESSION - illegal states possible
interface Order {
  status: string  // Could be any string
  shippedDate: Date | null  // Could be set when status != 'shipped'
}

// ✓ TYPE-SAFE - illegal states impossible
type UnconfirmedOrder = { type: 'unconfirmed', items: Item[] }
type ConfirmedOrder = { type: 'confirmed', items: Item[], confirmationNumber: string }
type ShippedOrder = { type: 'shipped', items: Item[], confirmationNumber: string, shippedDate: Date }

type Order = UnconfirmedOrder | ConfirmedOrder | ShippedOrder
```

### Avoid Type Escape Hatches

**STRICTLY FORBIDDEN without explicit user approval:**
- `any` type
- `as` type assertions (`as unknown as`, `as any`, `as SomeType`)
- `@ts-ignore` / `@ts-expect-error`

**Before using these, you MUST get user approval.**

There is always a better type-safe solution. These make code unsafe and defeat TypeScript's purpose.

### Use the Type System for Validation

```typescript
// ✓ TYPE-SAFE - validates at compile time
type PositiveNumber = number & { __brand: 'positive' }

function createPositive(value: number): PositiveNumber {
  if (value <= 0) {
    throw new Error(`Expected positive number, got ${value}`)
  }
  return value as PositiveNumber
}

// Can only be called with validated positive numbers
function calculateDiscount(price: PositiveNumber, rate: number): Money {
  // price is guaranteed positive by type system
}
```

## Prefer Immutability

**Principle:** Default to immutable data. Mutation is a source of bugs—unexpected changes, race conditions, and difficult debugging.

### The Problem: Mutable State

```typescript
// MUTABLE - hard to reason about
function processOrder(order: Order): void {
  order.status = 'processing'  // Mutates input!
  order.items.push(freeGift)   // Side effect!
}

// Caller has no idea their object changed
const myOrder = getOrder()
processOrder(myOrder)
// myOrder is now different - surprise!
```

### The Solution: Return New Values

```typescript
// IMMUTABLE - predictable
function processOrder(order: Order): Order {
  return {
    ...order,
    status: 'processing',
    items: [...order.items, freeGift]
  }
}

// Caller controls what happens
const myOrder = getOrder()
const processedOrder = processOrder(myOrder)
// myOrder unchanged, processedOrder is new
```

### Application Rules

- Prefer `const` over `let`
- Prefer spread (`...`) over mutation
- Prefer `map`/`filter`/`reduce` over `forEach` with mutation
- If you must mutate, make it explicit and contained

## YAGNI - You Aren't Gonna Need It

**Principle:** Don't build features until they're actually needed. Speculative code is waste—it costs time to write, time to maintain, and is often wrong when requirements become clear.

### The Problem: Speculative Generalization

```typescript
// YAGNI VIOLATION - over-engineered for "future" needs
interface PaymentProcessor {
  process(payment: Payment): Result
  refund(payment: Payment): Result
  partialRefund(payment: Payment, amount: Money): Result
  schedulePayment(payment: Payment, date: Date): Result
  recurringPayment(payment: Payment, schedule: Schedule): Result
  // ... 10 more methods "we might need"
}

// Only ONE method is actually used today
```

### The Solution: Build What You Need Now

```typescript
// YAGNI RESPECTED - minimal interface for current needs
interface PaymentProcessor {
  process(payment: Payment): Result
}

// Add refund() when you actually need refunds
// Add scheduling when you actually need scheduling
// Not before
```

### Application Rules

- Build the simplest thing that works
- Add capabilities when requirements demand them, not before
- "But we might need it" is not a requirement
- Unused code is a maintenance burden and a lie about the system
- Delete speculative code ruthlessly

## Integration with Other Skills

### With TDD Process

This skill is automatically applied during the **REFACTOR** state of the TDD process:

**TDD REFACTOR state post-conditions check:**
- ✓ Object calisthenics applied
- ✓ No feature envy
- ✓ Dependencies inverted
- ✓ Names are intention-revealing

**TDD Rule #8** enforces fail-fast error handling
**TDD Rule #9** enforces dependency inversion

### Standalone Usage

Activate when:
- Reviewing code for design quality
- Refactoring existing code
- Analyzing coupling and cohesion
- Planning architecture changes

## When Tempted to Cut Corners

- If you're about to use a fallback chain (`??` chains): STOP. Silent fallbacks hide bugs. When that `'unknown'` propagates through your system and causes a failure three layers later, you'll spend hours debugging. Fail fast with a clear error now.

- If you're about to use `any` or `as`: STOP. You're lying to the compiler to make an error go away. The error is telling you something—your types are wrong. Fix the types, not the symptoms.

- If you're about to instantiate a dependency inside a method: STOP. You're creating tight coupling that makes testing painful and changes risky. Take 30 seconds to inject it through the constructor.

- If you're about to name something `data`, `utils`, or `handler`: STOP. These names are meaningless. What does it actually DO? Name it for its purpose in the domain. Future you will thank present you.

- If you're about to add a getter just to access data: STOP. Ask why the caller needs that data. Can the object do the work instead? Tell, don't ask.

- If you're about to skip the refactor because "it works": STOP. Working code that's hard to change is technical debt. The refactor IS part of the work, not optional polish.

- If you're about to write a comment explaining code: STOP. Comments rot—they become lies as code changes. Instead, extract a well-named function, rename a variable, or restructure the code. If the code needs explanation, the code is the problem.

- If you're about to mutate a parameter: STOP. Return a new value instead. Mutation creates invisible dependencies—the caller doesn't know their data changed. Make data flow explicit.

- If you're about to build something "we might need later": STOP. You're guessing at future requirements, and you're probably wrong. Build what you need now. Add capabilities when they're actually required.

## When NOT to Apply

**Don't over-apply these principles:**
- **Value objects and DTOs** may violate object calisthenics (that's okay)
- **Simple scripts** don't need dependency inversion
- **Configuration objects** can have getters (they're data, not behavior)
- **Test code** can be less strict about calisthenics
- **Library integration code** may need type assertions

**Use judgment - principles serve code quality, not vice versa.**

## Summary Checklist

When refactoring or reviewing code, check:

- [ ] Object calisthenics: Does code follow the 9 rules?
- [ ] Feature envy: Do methods belong in the right classes?
- [ ] Dependencies: Are they injected, not instantiated?
- [ ] Error handling: Does code fail-fast with clear errors?
- [ ] Naming: Are names intention-revealing (no data/utils/helpers)?
- [ ] Types: Do types make illegal states impossible?
- [ ] Type safety: No `any`, No `as` assertions?
