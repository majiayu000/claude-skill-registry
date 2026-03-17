---
name: refactoring
description: Safe code refactoring with test protection and incremental changes. Improves structure without changing behavior. Use when extracting methods, reducing duplication, or restructuring code.
---

# Refactoring

Behavior-preserving code transformation protected by tests.

## Core Principle

> **Tests must pass before AND after every change.**

## When to Use

- Reducing duplication (DRY)
- Extracting methods/classes
- Improving naming and readability
- Simplifying complex conditionals
- Preparing code for new features

## MCP Workflow

```
# 1. Understand current structure
serena.get_symbols_overview(relative_path="target/file")

# 2. Check all usages before change
serena.find_referencing_symbols(name_path="TargetClass/method")

# 3. Verify test coverage
serena.search_for_pattern("test.*TargetClass", relative_path="test/")

# 4. Get target code
serena.find_symbol(name_path="TargetClass/method", include_body=True)

# 5. Safe rename
serena.rename_symbol(name_path="oldName", relative_path="file", new_name="newName")
```

## Workflow

### 1. Prepare
```
- Ensure tests exist and pass
- Identify refactoring scope
- Plan incremental steps
```

### 2. Refactor (small steps)
```
For each change:
  1. Make one refactoring move
  2. Run tests immediately
  3. If PASS: commit
  4. If FAIL: revert, try smaller step
```

### 3. Verify
```
- Run full test suite
- Review final structure
- Update docs if needed
```

## Common Patterns

### Extract Method
**When:** Function too long or has multiple responsibilities

```
BEFORE:
processOrder(order):
    # validate (10 lines)
    # calculate shipping (10 lines)
    # save (5 lines)

AFTER:
processOrder(order):
    validateOrder(order)
    shipping = calculateShipping(order)
    repository.save(order.copy(shipping=shipping))
```

### Extract Class
**When:** Class has too many responsibilities

```
OrderService with 6 methods
    -> OrderService (orchestration)
    -> OrderCalculator (calculations)
    -> OrderNotifier (notifications)
```

### Replace Conditional with Polymorphism
**When:** Repeated switch/if-else on type

```
BEFORE:
switch customer.type:
    case "REGULAR": return total * 0.05
    case "PREMIUM": return total * 0.10

AFTER:
interface CustomerType { calculateDiscount(total) }
class RegularCustomer implements CustomerType { ... }
class PremiumCustomer implements CustomerType { ... }
```

### Simplify Conditionals
```
BEFORE:
if a:
    if b:
        if c:
            return true
return false

AFTER:
return a and b and c
```

## Output Format

```markdown
## Refactoring: [Target]

| Item | Value |
|------|-------|
| Target | ClassName.method |
| Type | Extract / Rename / Simplify |
| Usages | N references |
| Tests | X tests covering |

### Steps
1. [Description] - Tests: PASS
2. [Description] - Tests: PASS

### Result
Files: N | Changes: +X/-Y | Tests: PASS
```

## Safety Checklist

- [ ] Tests exist and pass before starting
- [ ] Each step is independently committable
- [ ] No behavior changes
- [ ] All references updated
- [ ] Tests still pass after completion

## When NOT to Refactor

- No test coverage (add tests first)
- Under time pressure (do minimal fix)
- Code is about to be deleted
- Not sure about desired outcome
