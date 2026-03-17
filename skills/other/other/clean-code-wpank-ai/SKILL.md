---
name: clean-code
model: standard
category: testing
description: Pragmatic coding standards for writing clean, maintainable code — naming, functions, structure, anti-patterns, and pre-edit safety checks. Use when writing new code, refactoring existing code, reviewing code quality, or establishing coding standards.
version: 2.0
---

# Clean Code

> Be **concise, direct, and solution-focused**. Clean code reads like well-written prose — every name reveals intent, every function does one thing, and every abstraction earns its place.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install clean-code
```


---

## Core Principles

| Principle | Rule | Practical Test |
|-----------|------|----------------|
| **SRP** | Single Responsibility — each function/class does ONE thing | "Can I describe what this does without using 'and'?" |
| **DRY** | Don't Repeat Yourself — extract duplicates, reuse | "Have I written this logic before?" |
| **KISS** | Keep It Simple — simplest solution that works | "Is there a simpler way to achieve this?" |
| **YAGNI** | You Aren't Gonna Need It — don't build unused features | "Does anyone need this right now?" |
| **Boy Scout** | Leave code cleaner than you found it | "Is this file better after my change?" |

---

## Naming Rules

Names are the most important documentation. A good name eliminates the need for a comment.

| Element | Convention | Bad | Good |
|---------|------------|-----|------|
| **Variables** | Reveal intent | `n`, `d`, `tmp` | `userCount`, `elapsed`, `activeUsers` |
| **Functions** | Verb + noun | `user()`, `calc()` | `getUserById()`, `calculateTotal()` |
| **Booleans** | Question form | `active`, `flag` | `isActive`, `hasPermission`, `canEdit` |
| **Constants** | SCREAMING_SNAKE | `max`, `timeout` | `MAX_RETRY_COUNT`, `REQUEST_TIMEOUT_MS` |
| **Classes** | Noun, singular | `Manager`, `Data` | `UserRepository`, `OrderService` |
| **Enums** | PascalCase values | `'pending'` string | `Status.Pending` |

> **Rule:** If you need a comment to explain a name, rename it.

### Naming Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Cryptic abbreviations (`usrMgr`, `cfg`) | Unreadable in 6 months | Spell it out — IDE autocomplete makes long names free |
| Generic names (`data`, `info`, `item`, `handler`) | Says nothing about purpose | Use domain-specific names that reveal intent |
| Misleading names (`getUserList` returns one user) | Actively deceives readers | Match name to behavior, or change the behavior |
| Hungarian notation (`strName`, `nCount`, `IUser`) | Redundant with type system | Let TypeScript/IDE show types; names describe purpose |

---

## Function Rules

| Rule | Guideline | Why |
|------|-----------|-----|
| **Small** | Max 20 lines, ideally 5-10 | Fits in your head |
| **One Thing** | Does one thing, does it well | Testable and nameable |
| **One Level** | One level of abstraction per function | Readable top to bottom |
| **Few Args** | Max 3 arguments, prefer 0-2 | Easy to call correctly |
| **No Side Effects** | Don't mutate inputs unexpectedly | Predictable behavior |

### Guard Clauses

Flatten nested conditionals with early returns. Never nest deeper than 2 levels.

```typescript
// BAD — 5 levels deep
function processOrder(order: Order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.customer) {
        if (order.customer.isVerified) {
          return submitOrder(order);
        }
      }
    }
  }
  throw new Error('Invalid order');
}

// GOOD — guard clauses flatten the structure
function processOrder(order: Order) {
  if (!order) throw new Error('No order');
  if (!order.items.length) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');
  if (!order.customer.isVerified) throw new Error('Customer not verified');

  return submitOrder(order);
}
```

### Parameter Objects

When a function needs more than 3 arguments, use an options object.

```typescript
// BAD — too many parameters, order matters
createUser('John', 'Doe', 'john@example.com', 'secret', 'admin', 'Engineering');

// GOOD — self-documenting options object
createUser({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  password: 'secret',
  role: 'admin',
  department: 'Engineering',
});
```

---

## Code Structure Patterns

| Pattern | When to Apply | Benefit |
|---------|--------------|---------|
| **Guard Clauses** | Edge cases at function start | Flat, readable flow |
| **Flat > Nested** | Any nesting beyond 2 levels | Reduced cognitive load |
| **Composition** | Complex operations | Small, testable pieces |
| **Colocation** | Related code across files | Easier to find and change |
| **Extract Function** | Comments separating "sections" | Self-documenting code |

### Composition Over God Functions

```typescript
// BAD — god function doing everything
async function processOrder(order: Order) {
  // Validate... (15 lines)
  // Calculate totals... (15 lines)
  // Process payment... (10 lines)
  // Send notifications... (10 lines)
  // Update inventory... (10 lines)
  return { success: true };
}

// GOOD — composed of small, focused functions
async function processOrder(order: Order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  const payment = await processPayment(order.customer, totals);
  await sendOrderConfirmation(order, payment);
  await updateInventory(order.items);
  return { success: true, orderId: payment.orderId };
}
```

---

## Return Type Consistency

Functions should return consistent types. Use discriminated unions for multiple outcomes.

```typescript
// BAD — returns different types
function getUser(id: string) {
  const user = database.find(id);
  if (!user) return false;     // boolean
  if (user.isDeleted) return null; // null
  return user;                 // User
}

// GOOD — discriminated union
type GetUserResult =
  | { status: 'found'; user: User }
  | { status: 'not_found' }
  | { status: 'deleted' };

function getUser(id: string): GetUserResult {
  const user = database.find(id);
  if (!user) return { status: 'not_found' };
  if (user.isDeleted) return { status: 'deleted' };
  return { status: 'found', user };
}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Comment every line | Noise obscures signal | Delete obvious comments; comment *why*, not *what* |
| Helper for one-liner | Unnecessary indirection | Inline the code |
| Factory for 2 objects | Over-engineering | Direct instantiation |
| `utils.ts` with 1 function | Junk drawer file | Put code where it's used |
| Deep nesting | Unreadable flow | Guard clauses and early returns |
| Magic numbers | Unclear intent | Named constants |
| God functions | Untestable, unreadable | Split by responsibility |
| Commented-out code | Dead code confusion | Delete it; git remembers |
| TODO sprawl | Never gets done | Track in issue tracker, not code |
| Premature abstraction | Wrong abstraction is worse than none | Wait for 3+ duplicates before abstracting |
| Copy-paste programming | Duplicated bugs | Extract shared logic |
| Exception-driven control flow | Slow and confusing | Use explicit conditionals |
| Stringly-typed code | Typos and missed cases | Use enums or union types |
| Callback hell | Pyramid of doom | Use async/await |

---

## Pre-Edit Safety Check

Before changing any file, answer these questions to avoid cascading breakage:

| Question | Why |
|----------|-----|
| **What imports this file?** | Dependents might break on interface changes |
| **What does this file import?** | You might need to update the contract |
| **What tests cover this?** | Tests might fail — update them alongside code |
| **Is this a shared component?** | Multiple consumers means wider blast radius |

```
File to edit: UserService.ts
├── Who imports this? → UserController.ts, AuthController.ts
├── Do they need changes too? → Check function signatures
└── What tests cover this? → UserService.test.ts
```

> **Rule:** Edit the file + all dependent files in the SAME task. Never leave broken imports or missing updates.

---

## Self-Check Before Completing

Before marking any task complete, verify:

| Check | Question |
|-------|----------|
| **Goal met?** | Did I do exactly what was asked? |
| **Files edited?** | Did I modify all necessary files, including dependents? |
| **Code works?** | Did I verify the change compiles and runs? |
| **No errors?** | Do lint and type checks pass? |
| **Nothing forgotten?** | Any edge cases or dependent files missed? |

---

## NEVER Do

1. **NEVER add comments that restate the code** — if the code needs a comment to explain *what* it does, rename things until it doesn't
2. **NEVER create abstractions for fewer than 3 use cases** — premature abstraction is worse than duplication
3. **NEVER leave commented-out code in the codebase** — delete it; version control exists for history
4. **NEVER write functions longer than 20 lines** — extract sub-functions until each does one thing
5. **NEVER nest deeper than 2 levels** — use guard clauses, early returns, or extract functions
6. **NEVER use magic numbers or strings** — define named constants with clear semantics
7. **NEVER edit a file without checking what depends on it** — broken imports and missing updates are the most common source of bugs in multi-file changes
8. **NEVER leave a task with failing lint or type checks** — fix all errors before marking complete

---

## References

Detailed guides for specific clean code topics:

| Reference | Description |
|-----------|-------------|
| [Anti-Patterns](references/anti-patterns.md) | 21 common mistakes with bad/good code examples across naming, functions, structure, and comments |
| [Code Smells](references/code-smells.md) | Classic code smells catalog with detection patterns — Bloaters, OO Abusers, Change Preventers, Dispensables, Couplers |
| [Refactoring Catalog](references/refactoring-catalog.md) | Essential refactoring patterns with before/after examples and step-by-step mechanics |
