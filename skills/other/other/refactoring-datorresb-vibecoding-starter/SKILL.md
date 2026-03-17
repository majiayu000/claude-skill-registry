---
name: refactoring
description: Safe refactoring patterns for improving code structure without changing behavior. Use when simplifying code, eliminating duplication, improving readability, or restructuring for maintainability.
---

# Refactoring Skill

## Core Principle

**Refactoring changes code structure without changing behavior.**

Refactoring is NOT about adding features or fixing bugs. It's about making code easier to understand, maintain, and extend. Every refactoring should be:

- **Safe** — Behavior remains unchanged
- **Testable** — Tests verify behavior preservation
- **Incremental** — Small steps, frequent commits
- **Reversible** — Can roll back if needed

---

## When to Refactor

### Good Times to Refactor

✅ **Before adding a feature** — Make room for new functionality
✅ **During code review** — Improve code before merge
✅ **When you touch existing code** — Leave it better than you found it
✅ **When you see duplication** — DRY principle
✅ **When code is hard to test** — Improve testability
✅ **When you struggle to understand code** — Simplify for future readers

### Bad Times to Refactor

❌ **While debugging** — Fix the bug first, refactor later
❌ **Near a deadline** — Risk vs. reward is poor
❌ **Without tests** — Can't verify behavior preservation
❌ **In unfamiliar code** — Understand first, refactor later
❌ **Just because** — Must have a clear purpose

---

## Refactoring Patterns

### 1. Extract Function

**Problem:** Long function doing multiple things

**Solution:** Extract logical blocks into named functions

**Before:**
```python
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Order has no items")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Calculate
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.08
    total = subtotal + tax

    # Save
    db.save(order)
    send_confirmation_email(order.customer.email, order.id)
```

**After:**
```python
def process_order(order):
    validate_order(order)
    calculate_totals(order)
    save_and_notify(order)

def validate_order(order):
    if not order.items:
        raise ValueError("Order has no items")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_totals(order):
    subtotal = sum(item.price * item.quantity for item in order.items)
    order.tax = subtotal * 0.08
    order.total = subtotal + order.tax

def save_and_notify(order):
    db.save(order)
    send_confirmation_email(order.customer.email, order.id)
```

**Benefits:** Easier to test, understand, and modify each piece independently

---

### 2. Extract Variable

**Problem:** Complex expression that's hard to understand

**Solution:** Break into named intermediate variables

**Before:**
```javascript
if (user.age >= 18 && user.country === 'US' &&
    (user.verified || user.trustScore > 0.8)) {
    allowPurchase();
}
```

**After:**
```javascript
const isAdult = user.age >= 18;
const isUSUser = user.country === 'US';
const isTrusted = user.verified || user.trustScore > 0.8;
const canPurchase = isAdult && isUSUser && isTrusted;

if (canPurchase) {
    allowPurchase();
}
```

**Benefits:** Self-documenting, easier to debug, reusable logic

---

### 3. Replace Magic Numbers

**Problem:** Unexplained numeric literals throughout code

**Solution:** Named constants with clear meaning

**Before:**
```python
def calculate_shipping(weight):
    if weight < 5:
        return 4.99
    elif weight < 20:
        return 9.99
    else:
        return 14.99
```

**After:**
```python
LIGHT_PACKAGE_THRESHOLD = 5  # pounds
MEDIUM_PACKAGE_THRESHOLD = 20  # pounds
LIGHT_SHIPPING_COST = 4.99
MEDIUM_SHIPPING_COST = 9.99
HEAVY_SHIPPING_COST = 14.99

def calculate_shipping(weight):
    if weight < LIGHT_PACKAGE_THRESHOLD:
        return LIGHT_SHIPPING_COST
    elif weight < MEDIUM_PACKAGE_THRESHOLD:
        return MEDIUM_SHIPPING_COST
    else:
        return HEAVY_SHIPPING_COST
```

**Benefits:** Clear meaning, easy to update, self-documenting

---

### 4. Simplify Conditional Logic

**Problem:** Nested or complex conditionals

**Solution:** Early returns, guard clauses, or strategy pattern

**Before:**
```javascript
function calculateDiscount(user, order) {
    if (user) {
        if (user.isPremium) {
            if (order.total > 100) {
                return order.total * 0.2;
            } else {
                return order.total * 0.1;
            }
        } else {
            if (order.total > 100) {
                return order.total * 0.05;
            }
        }
    }
    return 0;
}
```

**After:**
```javascript
function calculateDiscount(user, order) {
    if (!user) return 0;

    const discountRate = getDiscountRate(user, order);
    return order.total * discountRate;
}

function getDiscountRate(user, order) {
    if (user.isPremium) {
        return order.total > 100 ? 0.2 : 0.1;
    }
    return order.total > 100 ? 0.05 : 0;
}
```

**Benefits:** Reduced nesting, clearer logic flow, easier to extend

---

### 5. Replace Duplication with Abstraction

**Problem:** Same code repeated in multiple places

**Solution:** Extract to shared function/class

**Before:**
```python
def send_welcome_email(user):
    subject = f"Welcome {user.name}!"
    body = render_template("welcome.html", user=user)
    smtp.send(user.email, subject, body)
    log.info(f"Sent welcome email to {user.email}")

def send_reset_email(user, token):
    subject = "Password Reset Request"
    body = render_template("reset.html", user=user, token=token)
    smtp.send(user.email, subject, body)
    log.info(f"Sent reset email to {user.email}")
```

**After:**
```python
def send_email(user, subject, template, **kwargs):
    body = render_template(template, user=user, **kwargs)
    smtp.send(user.email, subject, body)
    log.info(f"Sent {template} email to {user.email}")

def send_welcome_email(user):
    send_email(user, f"Welcome {user.name}!", "welcome.html")

def send_reset_email(user, token):
    send_email(user, "Password Reset Request", "reset.html", token=token)
```

**Benefits:** DRY principle, single place to update email logic

---

### 6. Improve Naming

**Problem:** Unclear or misleading names

**Solution:** Descriptive, intention-revealing names

**Before:**
```javascript
function calc(a, b) {
    const tmp = a * b;
    const res = tmp * 0.08;
    return tmp + res;
}
```

**After:**
```javascript
function calculateOrderTotal(subtotal, taxRate) {
    const tax = subtotal * taxRate;
    return subtotal + tax;
}
```

**Benefits:** Self-documenting, no need for comments

---

### 7. Split Large Classes

**Problem:** Class doing too many things (God Object)

**Solution:** Extract responsibilities into focused classes

**Before:**
```python
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def hash_password(self):
        # Password hashing logic
        pass

    def send_email(self, subject, body):
        # Email sending logic
        pass

    def save_to_db(self):
        # Database logic
        pass

    def generate_report(self):
        # Reporting logic
        pass
```

**After:**
```python
class User:
    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

class PasswordHasher:
    @staticmethod
    def hash(password):
        # Password hashing logic
        pass

class EmailService:
    @staticmethod
    def send(recipient, subject, body):
        # Email sending logic
        pass

class UserRepository:
    @staticmethod
    def save(user):
        # Database logic
        pass

class UserReportGenerator:
    def generate(self, user):
        # Reporting logic
        pass
```

**Benefits:** Single Responsibility Principle, easier to test and maintain

---

## Refactoring Workflow

### Step 1: Ensure Tests Exist

Before refactoring:

```bash
# Run existing tests
npm test  # JavaScript
pytest    # Python
cargo test  # Rust

# If tests don't exist or are insufficient:
# STOP and write tests first
```

**Rule:** Never refactor without tests. Tests are your safety net.

---

### Step 2: Make One Small Change

**Keep refactorings atomic:**

✅ Good: Extract one function
✅ Good: Rename one variable
✅ Good: Replace one magic number

❌ Bad: Extract function + rename variables + restructure class
❌ Bad: Refactor multiple files at once

---

### Step 3: Run Tests After Each Change

After every refactoring step:

```bash
# Run tests immediately
npm test
# Tests should still pass

# If tests fail:
# 1. You changed behavior (not just structure)
# 2. Revert and try again
git checkout -- .
```

---

### Step 4: Commit Frequently

Commit after each successful refactoring:

```bash
git add .
git commit -m "refactor: extract validate_order function

Extracted order validation logic into separate function for better
testability and readability. No behavior change."
```

**Commit message pattern:**
```
refactor: <what you changed>

<why you changed it>. No behavior change.
```

---

### Step 5: Review Before Pushing

Before pushing refactored code:

- [ ] All tests pass
- [ ] No behavior changed (tests prove this)
- [ ] Code is simpler/clearer
- [ ] No dead code left behind
- [ ] Documentation updated if needed

---

## Code Smells (When to Refactor)

### Smell: Long Function

**Signs:**
- Function > 50 lines
- Multiple levels of indentation
- Hard to name because it does too many things

**Refactoring:** Extract Function, Extract Class

---

### Smell: Duplicated Code

**Signs:**
- Same code block in multiple places
- Similar logic with minor variations
- Copy-paste programming

**Refactoring:** Extract Function, Extract Superclass, Use Template Method

---

### Smell: Large Class

**Signs:**
- Class > 500 lines
- Too many methods
- Multiple reasons to change (violates SRP)

**Refactoring:** Extract Class, Split Responsibilities

---

### Smell: Long Parameter List

**Signs:**
- Function takes > 3 parameters
- Parameters are related (should be object)
- Adding parameters frequently

**Refactoring:** Introduce Parameter Object, Replace with Builder

---

### Smell: Primitive Obsession

**Signs:**
- Using primitives instead of small objects
- Type codes (using int constants for types)
- String parsing throughout codebase

**Refactoring:** Replace with Value Object, Extract Class

---

### Smell: Feature Envy

**Signs:**
- Method uses data from another class more than its own
- Method would be better in another class

**Refactoring:** Move Method, Extract Method and Move

---

## Safety Checklist

Before starting refactoring:

- [ ] Tests exist and pass
- [ ] Tests have good coverage (>80% for code being refactored)
- [ ] You understand the code behavior
- [ ] No deadline pressure
- [ ] Git working directory is clean

During refactoring:

- [ ] Making one small change at a time
- [ ] Running tests after each change
- [ ] Committing after each successful refactoring
- [ ] No behavior changes (tests prove it)

After refactoring:

- [ ] All tests pass
- [ ] Code is simpler
- [ ] No dead code remains
- [ ] Documentation updated
- [ ] Ready for code review

---

## Integration with Other Skills

### With Code Review

- Refactor before requesting review
- Self-review using code-review skill patterns
- Smaller refactorings = easier reviews

### With Testing Strategy

- Write tests before refactoring (if missing)
- Use test-driven refactoring
- Tests prove behavior preservation

### With Git Hygiene

- Commit refactorings separately from features
- Use "refactor:" prefix in commit messages
- Keep refactoring commits small and focused

---

## Common Pitfalls

❌ **Refactoring without tests** — Can't prove behavior unchanged
❌ **Big bang refactoring** — Too risky, hard to review
❌ **Refactoring while adding features** — Mix of concerns
❌ **Refactoring unfamiliar code** — Understand first
❌ **Refactoring for perfection** — Good enough is good enough
❌ **Breaking backward compatibility** — If public API, be careful

✅ **Small, tested, incremental refactorings**
✅ **Clear purpose and benefit**
✅ **Preserve behavior**
✅ **Frequent commits**

---

**Remember:** Refactoring is about making code better without changing what it does. Keep changes small, test frequently, commit often. If tests fail after refactoring, you changed behavior—revert and try again.
