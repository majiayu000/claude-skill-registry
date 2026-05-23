---
name: code-priority
description: Guide design decisions using the State > Coupling > Complexity > Code priority framework. Use when evaluating tradeoffs, reviewing design choices, deciding between implementations, or when code volume seems to be prioritized over deeper concerns.
---

# INSTRUCTIONS

Apply the code optimization priority framework: sacrifice lower priorities to improve higher ones.

## The Priority Hierarchy

```
State > Coupling > Complexity > Code
```

| Priority | Focus | Why It Matters |
|----------|-------|----------------|
| **1. State** | Minimize mutable state | Stateless code works identically in sequential, parallel, and distributed contexts |
| **2. Coupling** | Reduce dependencies | Loose coupling enables independent change and testing |
| **3. Complexity** | Simplify logic | Lower cognitive load, fewer bugs |
| **4. Code** | Reduce volume | Less to read and maintain |

## Core Principle

> "It's okay to increase coupling if it makes your code more stateless."

Each level can be sacrificed to improve a higher-priority concern:
- **More code** is acceptable for **less complexity**
- **More complexity** is acceptable for **less coupling**
- **More coupling** is acceptable for **less state**

## Decision Framework

When evaluating design choices:

```
1. Does Option A have less mutable state than Option B?
   Yes → Prefer Option A (even if more coupled/complex/verbose)
   No  ↓
2. Does Option A have less coupling than Option B?
   Yes → Prefer Option A (even if more complex/verbose)
   No  ↓
3. Does Option A have less complexity than Option B?
   Yes → Prefer Option A (even if more verbose)
   No  ↓
4. Prefer the option with less code
```

## Why This Order?

**State is hardest to reason about:**
- Requires tracking "before" and "after" conditions
- Creates implicit dependencies between operations
- Breaks parallelization and distribution
- Explodes test setup complexity

**Beginners optimize the wrong thing:**
- Code volume is most visible, so it gets optimized first
- But state, coupling, and complexity matter more for maintainability
- Experience teaches that a few extra lines are cheap; hidden state is expensive

## Practical Examples

### Prefer Stateless (Accept More Coupling)

```python
# More state, less coupling
class Processor:
    def __init__(self):
        self.result = None

    def process(self, data):
        self.result = transform(data)

    def get_result(self):
        return self.result

# Less state, more coupling (PREFERRED)
def process(data, transformer):
    return transformer(data)
```

### Prefer Less Coupling (Accept More Code)

```python
# Less code, more coupling
def create_user(data):
    user = User(**data)
    db.save(user)           # Coupled to global db
    email.send_welcome()    # Coupled to global email
    return user

# More code, less coupling (PREFERRED)
def create_user(data, repository, notifier):
    user = User(**data)
    repository.save(user)
    notifier.send_welcome(user)
    return user
```

### Prefer Less Complexity (Accept More Code)

```python
# Less code, more complexity
result = data if condition else (default if not other else fallback)

# More code, less complexity (PREFERRED)
if condition:
    result = data
elif other:
    result = fallback
else:
    result = default
```

## Review Checklist

When reviewing code or design:

- [ ] Is state being introduced where a pure function would work?
- [ ] Are global/shared dependencies creating hidden coupling?
- [ ] Is clever code sacrificing readability for brevity?
- [ ] Is the author optimizing for code volume over deeper concerns?

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Global singletons | Maximum coupling + hidden state | Dependency injection |
| Mutable shared state | Race conditions, test complexity | Immutable data, message passing |
| Clever one-liners | Complexity hidden in density | Explicit multi-line logic |
| Premature DRY | Wrong abstraction, coupling | Tolerate duplication until pattern is clear |

## Integration with Other Practices

This framework complements:
- **Tidy First**: Structural improvements often reduce coupling
- **TDD**: Tests reveal hidden state and coupling problems early
- **Refactoring**: Many patterns specifically target state and coupling

## Reference

Based on: [curun1r's comment on Hacker News](https://news.ycombinator.com/item?id=11042400), attributed to Sandi Metz's design principles
