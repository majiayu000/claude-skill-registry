---
name: refactoring-specialist
description: Code refactoring expert for improving code structure, readability, and maintainability. Use when user asks to refactor, clean up, or improve code quality.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  hooks:
    after_complete:
      - trigger: self-improving-agent
        mode: background
        reason: "Learn from refactoring patterns"
      - trigger: session-logger
        mode: auto
        reason: "Log refactoring activity"
---

# Refactoring Specialist

Expert guidance on refactoring code to improve structure, readability, and maintainability while preserving functionality.

## When This Skill Activates

Activates when you:
- Ask to refactor code
- Request cleanup or improvement
- Mention "technical debt" or "code smell"
- Want to improve code quality

## Refactoring Principles

1. **Preserve Behavior**: Refactoring must not change external behavior
2. **Small Steps**: Make small, incremental changes
3. **Test Coverage**: Ensure tests pass before and after
4. **Commit Often**: Commit after each successful refactoring

## Code Smells to Address

### 1. Long Method
**Symptom:** Function > 20-30 lines

**Refactoring:** Extract Method
```typescript
// Before:
function processOrder(order) {
  // 50 lines of code
}

// After:
function processOrder(order) {
  validateOrder(order);
  calculateTotals(order);
  saveOrder(order);
  sendConfirmation(order);
}
```

### 2. Duplicate Code
**Symptom:** Similar code in multiple places

**Refactoring:** Extract Method / Template Method
```typescript
// Before:
class UserService {
  async validateEmail(email) {
    if (!email || !email.includes('@')) return false;
    const domain = email.split('@')[1];
    return domain.length > 0;
  }
}
class AdminService {
  async validateEmail(email) {
    if (!email || !email.includes('@')) return false;
    const domain = email.split('@')[1];
    return domain.length > 0;
  }
}

// After:
class EmailValidator {
  async validate(email) {
    if (!email || !email.includes('@')) return false;
    return email.split('@')[1].length > 0;
  }
}
```

### 3. Large Class
**Symptom:** Class doing too many things

**Refactoring:** Extract Class
```typescript
// Before:
class User {
  // Authentication
  // Profile management
  // Notifications
  // Reporting
}

// After:
class User { /* Core user data */ }
class UserAuth { /* Authentication */ }
class UserProfile { /* Profile management */ }
class UserNotifier { /* Notifications */ }
```

### 4. Long Parameter List
**Symptom:** Function with 4+ parameters

**Refactoring:** Introduce Parameter Object
```typescript
// Before:
function createUser(name, email, age, address, phone, role) { ... }

// After:
function createUser(user: UserData) { ... }

interface UserData {
  name: string;
  email: string;
  age: number;
  address: string;
  phone: string;
  role: string;
}
```

### 5. Feature Envy
**Symptom:** Method uses more data from other classes

**Refactoring:** Move Method
```typescript
// Before:
class Order {
  calculatePrice(customer) {
    const discount = customer.getDiscountLevel();
    // ...
  }
}

// After:
class Customer {
  calculatePriceForOrder(order) {
    const discount = this.discountLevel;
    // ...
  }
}
```

### 6. Data Clumps
**Symptom**: Same data appearing together

**Refactoring**: Extract Value Object
```typescript
// Before:
function drawShape(x, y, width, height) { ... }
function moveShape(x, y, width, height, dx, dy) { ... }

// After:
class Rectangle {
  constructor(x, y, width, height) { ... }
}
function drawShape(rect: Rectangle) { ... }
```

### 7. Primitive Obsession
**Symptom**: Using primitives instead of small objects

**Refactoring**: Replace Primitive with Object
```typescript
// Before:
function createUser(name, email, phone) { ... }

// After:
class Email {
  constructor(value) {
    if (!this.isValid(value)) throw new Error('Invalid email');
    this.value = value;
  }
  // ...
}
```

### 8. Switch Statements
**Symptom**: Large switch on type

**Refactoring**: Replace Conditional with Polymorphism
```typescript
// Before:
function calculatePay(employee) {
  switch (employee.type) {
    case 'engineer': return employee.salary * 1.2;
    case 'manager': return employee.salary * 1.5;
    case 'sales': return employee.salary * 1.1;
  }
}

// After:
interface Employee {
  calculatePay(): number;
}
class Engineer implements Employee {
  calculatePay() { return this.salary * 1.2; }
}
```

### 9. Temporary Field
**Symptom**: Variables only used in certain scenarios

**Refactoring**: Extract Class
```typescript
// Before:
class User {
  calculateRefund() {
    this.tempRefundAmount = 0;
    // complex calculation
    return this.tempRefundAmount;
  }
}

// After:
class RefundCalculator {
  calculate(user) {
    // ...
  }
}
```

### 10. Comments
**Symptom**: Code needs extensive comments

**Refactoring**: Extract Method with clear name
```typescript
// Before:
// Calculate the total price including discounts
// and tax based on user location
function calc(u, i) {
  let t = 0;
  // discount logic
  if (u.vip) t *= 0.9;
  // tax logic
  if (u.state === 'CA') t *= 1.08;
  return t;
}

// After:
function calculateTotalPrice(user: User, items: Item[]): number {
  let total = items.sum(i => i.price);
  if (user.isVIP) {
    total = applyVIPDiscount(total);
  }
  return applyTax(total, user.state);
}
```

## Refactoring Steps

1. **Identify the smell** - What makes this code hard to work with?
2. **Determine the refactoring** - Which technique applies?
3. **Ensure tests pass** - Green before starting
4. **Apply the refactoring** - Make the change
5. **Run tests** - Verify behavior unchanged
6. **Commit** - Small, atomic commits

## Safe Refactoring Practices

- Use your IDE's refactoring tools (Rename, Extract, Move)
- Run tests frequently (after each change)
- Keep commits small and focused
- Write a descriptive commit message
- Consider code reviews for complex refactorings

## Before Refactoring

- [ ] Tests are passing
- [ ] I understand what the code does
- [ ] I have identified the specific code smell
- [ ] I know which refactoring to apply
- [ ] I have a rollback plan

## After Refactoring

- [ ] Tests still pass
- [ ] Code is more readable
- [ ] Code is easier to maintain
- [ ] No new code smells introduced
- [ ] Documentation updated if needed

## References

- `references/smells.md` - Complete code smell catalog
- `references/techniques.md` - Refactoring techniques
- `references/checklist.md` - Refactoring checklist
