---
name: legacy-code-safety
description: Use when modifying, removing, or refactoring code that lacks test coverage. Emphasizes the danger of untested changes and the RGR workflow to add characterization tests before modifications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Legacy Code Safety

> "Changing untested code is like performing surgery blindfolded."

## DANGER: The Risk of Modifying Untested Code

**Modifying code without tests is one of the HIGHEST-RISK activities in software development.**

When you change untested code:

- You CANNOT know what behaviors you're breaking
- You have NO safety net to catch mistakes
- You're relying on hope instead of evidence
- You're creating technical debt on top of technical debt

**In dynamically-typed languages (Python, JavaScript, Ruby, PHP), this risk is EXPONENTIALLY higher:**

- No compiler to catch type errors
- No static analysis to verify correctness
- Tests are your ONLY safety mechanism
- Runtime is when you discover your mistakes

## The Golden Rule

**NEVER modify untested code without adding tests first.**

If code lacks tests:

1. STOP
2. Add characterization tests
3. Verify tests pass
4. THEN make your changes

## The RGR Workflow for Legacy Code

This is NOT standard TDD. This is **characterization testing** - capturing current behavior before changing it.

### Standard TDD (New Features)

1. RED: Write failing test for NEW behavior
2. GREEN: Implement to make test pass
3. REFACTOR: Clean up implementation

### Legacy Code RGR (Existing Code)

1. RED: Write test that SHOULD pass (captures current behavior)
2. GREEN: Verify it passes (confirms you captured reality correctly)
3. REFACTOR: NOW you can safely modify with a safety net

### The Critical Difference

**TDD:** You know what the behavior SHOULD be, write test for ideal

**Legacy RGR:** You DON'T know all behaviors, capture what EXISTS

### Why "RED" for Passing Tests?

The "RED" step means "you're in the red zone" - working with dangerous untested code. Even though you expect the test to pass, you're at risk until you have that passing test as proof.

## Characterization Testing Process

### Step 1: Identify All Behaviors

Before writing tests, understand what the code currently does:

```typescript
// Legacy function - no tests
function calculateShipping(order) {
  let cost = 9.99

  if (order.total > 100) {
    cost = 0
  }

  if (order.weight > 50) {
    cost += 25
  }

  if (order.destination === 'HI' || order.destination === 'AK') {
    cost += 15
  }

  return cost
}
```

**Questions to answer:**

- What inputs does it accept?
- What outputs does it produce?
- What are the edge cases?
- Are there side effects?
- What happens with invalid input?

### Step 2: Write Tests for Current Behavior

**Document what EXISTS, not what should exist:**

```typescript
describe('calculateShipping (characterization)', () => {
  // Capture base case
  test('standard shipping', () => {
    const order = { total: 50, weight: 10, destination: 'CA' }
    expect(calculateShipping(order)).toBe(9.99)
  })

  // Capture free shipping threshold
  test('free shipping over $100', () => {
    const order = { total: 150, weight: 10, destination: 'CA' }
    expect(calculateShipping(order)).toBe(0)
  })

  // Capture weight surcharge
  test('heavy package surcharge', () => {
    const order = { total: 50, weight: 75, destination: 'CA' }
    expect(calculateShipping(order)).toBe(34.99) // 9.99 + 25
  })

  // Capture regional surcharge
  test('Hawaii surcharge', () => {
    const order = { total: 50, weight: 10, destination: 'HI' }
    expect(calculateShipping(order)).toBe(24.99) // 9.99 + 15
  })

  // Discovered edge case: free shipping + weight
  test('free shipping with heavy package', () => {
    const order = { total: 150, weight: 75, destination: 'CA' }
    expect(calculateShipping(order)).toBe(25) // 0 + 25 (is this right?)
  })

  // Discovered edge case: all conditions
  test('all surcharges with free shipping threshold', () => {
    const order = { total: 150, weight: 75, destination: 'HI' }
    expect(calculateShipping(order)).toBe(40) // 0 + 25 + 15
  })
})
```

### Step 3: Verify Tests Pass

**These tests MUST pass immediately:**

```bash
npm test
```

If they don't pass:

- You misunderstood the current behavior
- Fix the test, not the code
- The test should document reality

### Step 4: NOW You Can Refactor

**With tests in place, you have a safety net:**

```typescript
// NOW we can safely refactor
function calculateShipping(order: Order): number {
  const BASE_COST = 9.99
  const FREE_SHIPPING_THRESHOLD = 100
  const HEAVY_PACKAGE_WEIGHT = 50
  const HEAVY_PACKAGE_SURCHARGE = 25
  const REMOTE_DESTINATIONS = ['HI', 'AK']
  const REMOTE_SURCHARGE = 15

  let cost = order.total > FREE_SHIPPING_THRESHOLD ? 0 : BASE_COST

  if (order.weight > HEAVY_PACKAGE_WEIGHT) {
    cost += HEAVY_PACKAGE_SURCHARGE
  }

  if (REMOTE_DESTINATIONS.includes(order.destination)) {
    cost += REMOTE_SURCHARGE
  }

  return cost
}
```

**Run tests again:**

```bash
npm test  # All tests still pass
```

You've improved the code WITHOUT breaking existing behavior.

## When This Skill Applies

Use this skill when:

- [ ] Deleting code that has no tests
- [ ] Modifying functions without test coverage
- [ ] Refactoring untested modules
- [ ] Changing behavior in legacy systems
- [ ] Test coverage is below 80% for code you're touching
- [ ] You inherit code from previous developers
- [ ] You're working in a codebase with poor test discipline

**Even if the change seems "simple", if there are no tests, use this workflow.**

## Language-Specific Risk Levels

### HIGH RISK: Dynamic/Weakly-Typed Languages

**Python, JavaScript, Ruby, PHP:**

- NO compile-time type checking
- NO static analysis of type correctness
- Tests are your ONLY safety net
- Runtime is when errors appear
- User discovers bugs, not compiler

**Extra caution required:**

- Write MORE tests
- Test edge cases thoroughly
- Check for None/null/undefined
- Verify types explicitly
- Add type hints/annotations when possible

### MEDIUM RISK: Static/Strongly-Typed Languages

**Go, Rust, TypeScript (strict mode), Java:**

- Type system catches some errors
- Compiler validates correctness
- Still need tests for BEHAVIOR
- Types don't test business logic

**Type safety helps, but:**

- Types verify structure, not logic
- Tests still required for correctness
- Don't rely solely on type system

## The Strangler Fig Pattern

For large legacy systems, don't try to test everything at once:

### What Is It?

Named after the strangler fig vine that grows around a tree:

1. Vine grows alongside tree
2. Eventually replaces tree entirely
3. Original tree can be removed

Applied to code:

1. Wrap legacy code with new interface
2. Add tests to the wrapper
3. Gradually move logic to new code
4. Eventually remove legacy code

### Implementation

**Phase 1: Wrap**

```typescript
// Legacy code (untested, scary)
function legacyCalculatePrice(item) {
  // ... 500 lines of spaghetti ...
}

// New wrapper (tested)
function calculatePrice(item: Item): number {
  // Add validation and tests here
  validateItem(item)

  // Call legacy for now
  return legacyCalculatePrice(item)
}
```

**Phase 2: Test the Boundary**

```typescript
describe('calculatePrice wrapper', () => {
  test('validates input', () => {
    expect(() => calculatePrice(null)).toThrow()
  })

  test('handles normal items', () => {
    const item = { id: 1, price: 10 }
    expect(calculatePrice(item)).toBe(10)
  })

  // Characterization tests for legacy behavior
  test('matches legacy for discounts', () => {
    const item = { id: 1, price: 10, discount: 0.2 }
    expect(calculatePrice(item)).toBe(8)
  })
})
```

**Phase 3: Replace Internals**

```typescript
function calculatePrice(item: Item): number {
  validateItem(item)

  // New implementation (tested, clean)
  const basePrice = item.price
  const discount = item.discount ?? 0
  return basePrice * (1 - discount)

  // Legacy code removed!
}
```

**Phase 4: Expand**

Now that one function is safe, repeat for next function.

### Benefits

- Incremental progress
- Always have working system
- Tests added gradually
- Risk minimized
- Can stop anytime

### When to Use

- Large untested codebase
- Can't stop for months to add tests
- Need to deliver features while improving
- High-risk production system

## Pre-Modification Checklist

Before touching ANY untested code:

- [ ] Identified all entry points (who calls this code?)
- [ ] Identified all exit points (what does this code call?)
- [ ] Understood current behavior (what does it do now?)
- [ ] Written characterization tests for current behavior
- [ ] All characterization tests pass
- [ ] Documented any surprising behaviors found
- [ ] Considered using Strangler Fig for large changes

**ONLY AFTER ALL CHECKS PASS:**

- [ ] Make your intended changes
- [ ] Run tests (verify behavior preserved or intentionally changed)
- [ ] Add tests for NEW behavior if applicable
- [ ] Document breaking changes if any

## Red Flags

Stop immediately if:

- "I'll just make a quick change, no need for tests"
- "It's a small change, what could go wrong?"
- "I don't have time to write tests"
- "The code is too complex to test"
- "I'll add tests later" (you won't)

**These are rationalizations for dangerous behavior.**

## Common Objections (and Responses)

### "But tests will take longer than the change!"

**Response:** The initial change is fast. Finding and fixing the bugs you introduced takes much longer. Tests save time.

### "The code is too complex to test!"

**Response:** If it's too complex to test, it's too complex to change safely. Simplify first, or use Strangler Fig pattern.

### "We need to ship this feature NOW!"

**Response:** Shipping a broken feature is slower than shipping a tested feature late. Technical debt compounds.

### "This code has worked fine without tests for years!"

**Response:** Until now. The moment you change it, that safety is gone. Past stability doesn't predict future stability.

### "I understand the code, I won't break it!"

**Response:** Confidence is not a substitute for evidence. Even experts make mistakes.

## Success Metrics

How to know you've done this right:

**Green flags:**

- All characterization tests pass before changes
- All tests still pass after changes
- New behavior has new tests
- Test coverage increased
- Code is more readable
- Confidence is high

**Red flags:**

- Tests fail after changes (and you don't know why)
- Skipped edge cases "to save time"
- Changed behavior without updating tests
- Test coverage decreased or stagnant
- More confused than before

## Integration with Other Skills

Use these related skills:

- **test-driven-development**: For new behavior, use TDD after characterization tests exist
- **refactoring**: With tests in place, refactor safely
- **boy-scout-rule**: While adding tests, improve code quality
- **proof-of-work**: Document test results as evidence
- **debugging**: When characterization tests reveal unexpected behavior

## Tools and Techniques

### Code Coverage Tools

Use coverage tools to identify untested code:

```bash
# JavaScript/TypeScript
npm test -- --coverage

# Python
pytest --cov=mypackage

# Ruby
bundle exec rspec --require spec_helper

# Go
go test -cover ./...
```

**Target coverage:**

- Critical paths: 100%
- Business logic: 90%+
- Overall codebase: 80%+

### Mutation Testing

Verify tests actually catch bugs:

```bash
# JavaScript
npm install -D stryker

# Python
pip install mutmut
```

Mutation testing changes your code slightly and verifies tests fail. If tests still pass after mutation, they're not effective.

### Approval Testing

For complex outputs (HTML, JSON, reports):

```typescript
test('generates invoice', () => {
  const invoice = generateInvoice(order)
  expect(invoice).toMatchSnapshot()
})
```

First run captures current output. Future runs verify it hasn't changed.

## Real-World Example

### Scenario

Legacy payment processor, 2000 lines, no tests, needs to add new payment method.

### Step 1: Identify Scope

Don't test everything - test what you'll touch:

```typescript
// Will modify this
function processPayment(payment, method) {
  // ... many lines ...
}

// Will NOT modify these
function logTransaction(transaction) { }
function sendEmail(user, content) { }
```

### Step 2: Add Characterization Tests

```typescript
describe('processPayment (characterization)', () => {
  test('processes credit card payment', () => {
    const payment = { amount: 100, currency: 'USD' }
    const method = { type: 'credit_card', number: '4111...' }

    const result = processPayment(payment, method)

    expect(result.success).toBe(true)
    expect(result.transactionId).toBeDefined()
    expect(result.amount).toBe(100)
  })

  // More tests for existing payment methods...
})
```

### Step 3: Tests Pass

```bash
npm test
# ✅ All tests passing
```

### Step 4: Add New Feature

```typescript
function processPayment(payment, method) {
  // Existing code preserved
  if (method.type === 'credit_card') {
    return processCreditCard(payment, method)
  }

  // NEW: Add cryptocurrency support
  if (method.type === 'crypto') {
    return processCrypto(payment, method)
  }

  throw new Error(`Unknown payment method: ${method.type}`)
}
```

### Step 5: Add Tests for New Behavior

```typescript
test('processes cryptocurrency payment', () => {
  const payment = { amount: 100, currency: 'USD' }
  const method = { type: 'crypto', address: '0x123...' }

  const result = processPayment(payment, method)

  expect(result.success).toBe(true)
  expect(result.transactionId).toBeDefined()
})
```

### Step 6: All Tests Pass

```bash
npm test
# ✅ All tests passing (old + new)
```

### Result

- New feature added safely
- Existing behavior preserved
- Tests ensure no regression
- Future changes safer

## Remember

1. **Untested code is dangerous code** - especially in dynamic languages
2. **Characterize before changing** - Capture current behavior first
3. **RGR workflow for legacy** - Different from TDD, specific to untested code
4. **Strangler Fig for large systems** - Gradual improvement beats big bang
5. **Tests are proof** - Confidence without evidence is just hope
6. **No shortcuts** - "Quick changes" create slow bugs

**Legacy code is not an excuse for reckless changes. It's a reason for EXTRA caution.**
