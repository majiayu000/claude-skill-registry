---
name: refactoring
description: Use when restructuring code to improve quality without changing external behavior. Emphasizes safety through tests and incremental changes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Refactoring Skill

Improve code structure and quality while preserving behavior.

## Core Principle

**Tests are your safety net.** Never refactor without tests.

## The Refactoring Cycle

1. **Ensure tests exist and pass**
2. **Make ONE small change**
3. **Run tests** (must still pass)
4. **Commit** (keep changes isolated)
5. **Repeat**

**Each step must be reversible.** If tests fail, revert and try smaller change.

## Pre-Refactoring Checklist

**STOP if any of these are false:**

- [ ] Tests exist for code being refactored
- [ ] All tests currently pass
- [ ] Understand what code does
- [ ] External behavior will remain unchanged
- [ ] Have time to do this properly (not rushing)

**If no tests exist:**

1. Add tests first
2. Verify tests pass
3. THEN refactor

## When to Refactor

### Code Smells That Suggest Refactoring

**Readability issues:**

- Long functions (> 50 lines)
- Deep nesting (> 3 levels)
- Unclear naming
- Magic numbers
- Complex conditionals

**Maintainability issues:**

- Duplication (same code in multiple places)
- God classes (too many responsibilities)
- Feature envy (method uses another class more than its own)
- Data clumps (same groups of parameters passed around)

**Complexity issues:**

- Cyclomatic complexity > 10
- Too many dependencies
- Tightly coupled code
- Difficult to test

### When NOT to Refactor

- **No tests exist** (add tests first)
- **Under deadline pressure** (defer to later)
- **Code works and is readable** (don't over-engineer)
- **Changing external behavior** (that's not refactoring, that's a feature/fix)
- **Right before release** (too risky)

## Classic Refactorings

### Extract Function

**Problem:** Function does too many things

```typescript
// Before: Long function doing multiple things
function processOrder(order: Order) {
  // Validate order
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order')
  }
  if (!order.customer || !order.customer.email) {
    throw new Error('Invalid customer')
  }

  // Calculate totals
  let subtotal = 0
  for (const item of order.items) {
    subtotal += item.price * item.quantity
  }
  const tax = subtotal * 0.08
  const shipping = subtotal > 50 ? 0 : 9.99
  const total = subtotal + tax + shipping

  // Save to database
  return database.save({
    ...order,
    subtotal,
    tax,
    shipping,
    total
  })
}

// After: Extracted into focused functions
function processOrder(order: Order) {
  validateOrder(order)
  const totals = calculateTotals(order)
  return saveOrder(order, totals)
}

function validateOrder(order: Order): void {
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order')
  }
  if (!order.customer || !order.customer.email) {
    throw new Error('Invalid customer')
  }
}

function calculateTotals(order: Order) {
  const subtotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  )
  const tax = subtotal * 0.08
  const shipping = subtotal > 50 ? 0 : 9.99
  const total = subtotal + tax + shipping

  return { subtotal, tax, shipping, total }
}

function saveOrder(order: Order, totals: Totals) {
  return database.save({ ...order, ...totals })
}
```

**Benefits:** Each function has single responsibility, easier to test, easier to understand

### Extract Variable

**Problem:** Complex expression that's hard to understand

```typescript
// Before: Dense, hard to parse
if (user.age >= 18 && user.country === 'US' && !user.banned && user.verified) {
  // ...
}

// After: Intent is clear
const isAdult = user.age >= 18
const isUSResident = user.country === 'US'
const hasGoodStanding = !user.banned && user.verified
const canPurchase = isAdult && isUSResident && hasGoodStanding

if (canPurchase) {
  // ...
}
```

**Benefits:** Self-documenting, easier to debug, easier to modify

### Inline Function/Variable

**Problem:** Unnecessary indirection that doesn't add clarity

```typescript
// Before: Over-abstraction
function getTotal(order: Order) {
  return calculateTotalAmount(order)
}

function calculateTotalAmount(order: Order) {
  return order.subtotal + order.tax
}

// After: Inline the unnecessary layer
function getTotal(order: Order) {
  return order.subtotal + order.tax
}
```

**When to inline:** Abstraction doesn't add value, makes code harder to follow

### Rename

**Problem:** Unclear or misleading names

```typescript
// Before: Unclear
function proc(d: any) {
  const r = d.x * d.y
  return r
}

// After: Self-explanatory
function calculateArea(dimensions: Dimensions) {
  const area = dimensions.width * dimensions.height
  return area
}
```

**Benefits:** Code is self-documenting, no need to guess what variables mean

### Replace Magic Number with Named Constant

**Problem:** Unexplained numbers in code

```typescript
// Before: What's 0.08? What's 9.99?
const tax = subtotal * 0.08
const shipping = subtotal > 50 ? 0 : 9.99

// After: Clear meaning
const TAX_RATE = 0.08
const FREE_SHIPPING_THRESHOLD = 50
const STANDARD_SHIPPING_COST = 9.99

const tax = subtotal * TAX_RATE
const shipping = subtotal > FREE_SHIPPING_THRESHOLD ? 0 : STANDARD_SHIPPING_COST
```

### Remove Duplication

**Problem:** Same code in multiple places

```typescript
// Before: Duplication
function formatUserName(user: User) {
  return `${user.firstName} ${user.lastName}`.trim()
}

function formatAdminName(admin: Admin) {
  return `${admin.firstName} ${admin.lastName}`.trim()
}

function formatAuthorName(author: Author) {
  return `${author.firstName} ${author.lastName}`.trim()
}

// After: One implementation
function formatFullName(person: { firstName: string; lastName: string }) {
  return `${person.firstName} ${person.lastName}`.trim()
}

// Usage
formatFullName(user)
formatFullName(admin)
formatFullName(author)
```

### Simplify Conditional

**Problem:** Complex nested if/else

```typescript
// Before: Nested conditionals
function getShippingCost(order: Order) {
  if (order.total > 100) {
    return 0
  } else {
    if (order.items.length > 5) {
      return 5.99
    } else {
      if (order.weight > 10) {
        return 15.99
      } else {
        return 9.99
      }
    }
  }
}

// After: Early returns, flat structure
function getShippingCost(order: Order) {
  if (order.total > 100) return 0
  if (order.items.length > 5) return 5.99
  if (order.weight > 10) return 15.99
  return 9.99
}

// Or: Look-up table
const SHIPPING_RULES = [
  { condition: (o: Order) => o.total > 100, cost: 0 },
  { condition: (o: Order) => o.items.length > 5, cost: 5.99 },
  { condition: (o: Order) => o.weight > 10, cost: 15.99 },
]

function getShippingCost(order: Order) {
  const rule = SHIPPING_RULES.find(r => r.condition(order))
  return rule?.cost ?? 9.99
}
```

### Replace Conditional with Polymorphism

**Problem:** Type checks scattered throughout code

```typescript
// Before: Type checking everywhere
function calculatePrice(item: Item) {
  if (item.type === 'book') {
    return item.basePrice * 0.9  // 10% discount
  } else if (item.type === 'electronics') {
    return item.basePrice * 1.15  // 15% markup
  } else if (item.type === 'clothing') {
    return item.basePrice
  }
}

// After: Polymorphism
interface Item {
  calculatePrice(): number
}

class Book implements Item {
  calculatePrice() {
    return this.basePrice * 0.9
  }
}

class Electronics implements Item {
  calculatePrice() {
    return this.basePrice * 1.15
  }
}

class Clothing implements Item {
  calculatePrice() {
    return this.basePrice
  }
}

// Usage: No type checking needed
const price = item.calculatePrice()
```

### Split Function

**Problem:** Function tries to do too many things

```typescript
// Before: Does validation, calculation, and saving
function processPayment(payment: Payment) {
  // Validation
  if (!payment.amount || payment.amount <= 0) {
    throw new Error('Invalid amount')
  }
  if (!payment.method) {
    throw new Error('Payment method required')
  }

  // Calculation
  const fee = payment.amount * 0.029 + 0.30
  const total = payment.amount + fee

  // Persistence
  const record = database.save({
    amount: payment.amount,
    fee,
    total,
    method: payment.method,
    timestamp: Date.now()
  })

  // Notification
  notificationService.send({
    user: payment.user,
    message: `Payment of $${total} processed`
  })

  return record
}

// After: Separate concerns
function processPayment(payment: Payment) {
  validatePayment(payment)
  const totals = calculatePaymentTotals(payment)
  const record = savePayment(payment, totals)
  notifyPaymentProcessed(payment.user, totals.total)
  return record
}
```

## Refactoring Workflow

### Step-by-Step Process

```bash
# 1. Ensure tests pass
npm test
# ✅ All tests passing

# 2. Make ONE refactoring change
# Example: Extract function

# 3. Run tests immediately
npm test
# ✅ Still passing

# 4. Commit with descriptive message
git add .
git commit -m "refactor: extract validateOrder function"

# 5. Repeat for next refactoring
# Make another small change, test, commit
```

### If Tests Fail After Refactoring

```bash
# Tests failed after refactoring

# Option 1: Revert and try smaller change
git reset --hard HEAD
# Make smaller, safer change

# Option 2: Debug and fix
# Find what broke
# Fix it
# Run tests again
```

## Refactoring Strategies

### The Boy Scout Rule

**"Leave code better than you found it"**

When touching code for any reason:

1. Fix obvious issues you see
2. Improve naming
3. Extract complex expressions
4. Add missing tests
5. Remove commented code

**Small improvements accumulate**

### Preparatory Refactoring

**Before adding feature, refactor to make it easy**

```
1. Need to add feature
2. Current code structure makes it hard
3. Refactor first to make space
4. Then add feature in clean code
```

**Quote:** "Make the change easy, then make the easy change"

### Opportunistic Refactoring

**Fix things you notice while working**

- Fixing bug? Clean up surrounding code
- Adding feature? Improve structure
- Reading code? Fix confusing names

### Planned Refactoring

**Dedicated time to improve code health**

- Tech debt tickets
- Refactoring sprints
- Clean-up sessions

## Refactoring Safety Checklist

**Before every change:**

- [ ] Tests exist
- [ ] Tests pass
- [ ] Understand what code does

**After every change:**

- [ ] Tests still pass
- [ ] No functionality changed
- [ ] Code is clearer
- [ ] Ready to commit

**If tests fail:**

- [ ] Understand why
- [ ] Fix or revert
- [ ] Never commit broken tests

## Integration with Other Skills

Apply these skills during refactoring:

- **boy-scout-rule** - Leave code better than found
- **simplicity-principles** - KISS, YAGNI, simple is better
- **solid-principles** - Single Responsibility, etc.
- **structural-design-principles** - Composition, encapsulation
- **test-driven-development** - Add tests if missing
- **proof-of-work** - Verify tests still pass
- **code-reviewer** - Review refactored code

## Common Refactoring Pitfalls

### ❌ Refactoring Without Tests

**Risk:** Change behavior without noticing

**Solution:** Add tests first, then refactor

### ❌ Too Many Changes at Once

**Risk:** Hard to debug if something breaks

**Solution:** One refactoring at a time, commit frequently

### ❌ Changing Behavior

**Risk:** It's not refactoring if behavior changes

**Solution:** Tests must still pass, functionality unchanged

### ❌ Over-Engineering

**Risk:** More complex after "refactoring"

**Solution:** Simpler is better, don't add unnecessary abstraction

### ❌ Refactoring Under Pressure

**Risk:** Mistakes due to rushing

**Solution:** Defer to when you have time to do it right

## Measuring Refactoring Success

**Good refactoring results in:**

- ✅ Easier to understand
- ✅ Easier to modify
- ✅ Easier to test
- ✅ Fewer lines of code (usually)
- ✅ Lower complexity
- ✅ Same or better performance
- ✅ All tests still pass

**If any test fails, it wasn't successful refactoring**

## Tools

**Automated refactoring tools:**

- IDE refactoring commands (safe)
- Rename variable/function (safe)
- Extract method (safe)
- Move file (safe)

**Manual refactoring:**

- Make small changes
- Test frequently
- Commit after each change
- Use version control as safety net

## Remember

1. **Tests first** - No refactoring without tests
2. **Small steps** - One change at a time
3. **Test after each step** - Must stay green
4. **Commit frequently** - Each safe change gets a commit
5. **Behavior unchanged** - If behavior changes, it's not refactoring

**Refactoring is about improving structure without changing what the code does.**
