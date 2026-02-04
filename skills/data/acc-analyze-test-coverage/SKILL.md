---
name: acc-analyze-test-coverage
description: Analyzes PHP codebase for test coverage gaps. Detects untested classes, methods, branches, exception paths, and edge cases. Provides actionable recommendations.
---

# Test Coverage Analysis

Analyzes PHP codebase to identify untested code and coverage gaps.

## Detection Patterns

### 1. Classes Without Tests

```bash
# Find all PHP classes in src/
Glob: src/**/*.php

# Find all test files
Glob: tests/**/*Test.php

# Compare: class Foo in src/ should have FooTest in tests/
```

**Pattern Matching:**
```
src/Domain/User/User.php → tests/Unit/Domain/User/UserTest.php
src/Application/PlaceOrder/PlaceOrderHandler.php → tests/Unit/Application/PlaceOrder/PlaceOrderHandlerTest.php
```

### 2. Methods Without Tests

```php
// For each public method in class
Grep: "public function [a-z]" --glob "src/**/*.php"

// Check if test method exists
Grep: "test_methodName" --glob "tests/**/*Test.php"
```

**Detection Logic:**
```
Class: Order
├── confirm() → test_confirm_* exists? ✅/❌
├── cancel() → test_cancel_* exists? ✅/❌
├── ship() → test_ship_* exists? ✅/❌
└── addItem() → test_addItem_* / test_add_item_* exists? ✅/❌
```

### 3. Branches Not Covered

**If/Else Branches:**
```php
// Source code
public function process(Order $order): void
{
    if ($order->isPending()) {     // Branch 1: pending
        $this->processPending($order);
    } elseif ($order->isConfirmed()) { // Branch 2: confirmed
        $this->processConfirmed($order);
    } else {                       // Branch 3: other
        throw new InvalidStateException();
    }
}

// Required tests:
// - test_process_when_pending_*
// - test_process_when_confirmed_*
// - test_process_when_other_throws_exception
```

**Switch Statements:**
```php
// Source code
match ($status) {
    'pending' => $this->handlePending(),
    'confirmed' => $this->handleConfirmed(),
    'shipped' => $this->handleShipped(),
    default => throw new UnexpectedValueException(),
};

// Required tests: one per case + default
```

### 4. Exception Paths

```php
// Detect throw statements
Grep: "throw new" --glob "src/**/*.php"

// Each throw should have corresponding test with expectException
```

**Example:**
```php
// Source
public function withdraw(Money $amount): void
{
    if ($amount->greaterThan($this->balance)) {
        throw new InsufficientFundsException();  // Line 15
    }
}

// Required test
public function test_withdraw_throws_for_insufficient_funds(): void
{
    $this->expectException(InsufficientFundsException::class);
    // ...
}
```

### 5. Edge Cases

| Type | Values to Test | Detection |
|------|---------------|-----------|
| **Null** | `null` input | Parameters without type hint or nullable |
| **Empty** | `[]`, `''`, `0` | Collection/string/numeric parameters |
| **Boundary** | min, max, min-1, max+1 | Constants, validation limits |
| **Unicode** | `'émoji 🎉'` | String parameters |
| **Concurrent** | Race conditions | Shared state, repositories |

**Detection Patterns:**
```php
// Nullable parameters
Grep: "\?[A-Z]" --glob "src/**/*.php"  // ?Type
Grep: "null\|" --glob "src/**/*.php"   // Type|null

// Collections
Grep: "array \$" --glob "src/**/*.php"
Grep: "iterable" --glob "src/**/*.php"

// Numeric limits
Grep: "const MAX_" --glob "src/**/*.php"
Grep: "const MIN_" --glob "src/**/*.php"
```

## Analysis Process

### Phase 1: Inventory

1. List all production classes:
   ```
   Glob: src/**/*.php
   ```

2. List all test classes:
   ```
   Glob: tests/**/*Test.php
   ```

3. Build mapping:
   ```
   ProductionClass → [TestClass, TestClass]
   ```

### Phase 2: Class Coverage

For each production class:
1. Check if corresponding test exists
2. Calculate: `covered_classes / total_classes * 100`

### Phase 3: Method Coverage

For each public method:
1. Extract method names from production code
2. Search for `test_{method}` patterns in tests
3. Calculate: `tested_methods / total_methods * 100`

### Phase 4: Branch Coverage

For each conditional:
1. Count branches (if/elseif/else, match cases)
2. Search for tests covering each branch
3. Report uncovered branches

### Phase 5: Edge Cases

1. Identify nullable/optional parameters
2. Identify collections
3. Identify numeric limits
4. Check if edge case tests exist

## Output Format

```markdown
# Test Coverage Analysis Report

## Summary

| Metric | Value | Target |
|--------|-------|--------|
| Class Coverage | 75% | 90% |
| Method Coverage | 60% | 80% |
| Branch Coverage | 45% | 70% |

## Untested Classes

| Class | Location | Priority |
|-------|----------|----------|
| `PaymentProcessor` | src/Domain/Payment/ | High |
| `EmailNotifier` | src/Infrastructure/ | Medium |

## Untested Methods

| Class | Method | Reason |
|-------|--------|--------|
| `Order` | `splitShipment()` | No test found |
| `User` | `resetPassword()` | Only happy path tested |

## Uncovered Branches

| File | Line | Branch | Missing Test |
|------|------|--------|--------------|
| Order.php | 45 | else (cancelled) | test_ship_when_cancelled |
| User.php | 23 | null check | test_with_null_email |

## Missing Edge Cases

| Class | Method | Edge Case |
|-------|--------|-----------|
| `Cart` | `addItem()` | Empty cart, max items |
| `Money` | `add()` | Zero amount, overflow |

## Action Items

### Critical (Must Have)
1. Add `PaymentProcessorTest` — handles money
2. Add `test_order_ship_when_cancelled` — business rule

### High Priority
1. Add null checks for `User::resetPassword()`
2. Add boundary tests for `Cart::addItem()`

### Recommended Skills

| Gap | Skill | Action |
|-----|-------|--------|
| Missing unit test | `acc-create-unit-test` | Generate test class |
| Missing integration test | `acc-create-integration-test` | Generate DB test |
| Need test data | `acc-create-test-builder` | Generate builder |
```

## Severity Levels

| Level | Coverage | Action |
|-------|----------|--------|
| **Critical** | <50% | Immediate attention |
| **Warning** | 50-70% | Prioritize improvement |
| **Good** | 70-90% | Monitor and maintain |
| **Excellent** | >90% | Focus on edge cases |

## Integration with Generator

After analysis, recommend using:

- `acc-create-unit-test` — for missing unit tests
- `acc-create-integration-test` — for missing integration tests
- `acc-create-test-builder` — for complex test data
- `acc-create-mock-repository` — for repository tests
