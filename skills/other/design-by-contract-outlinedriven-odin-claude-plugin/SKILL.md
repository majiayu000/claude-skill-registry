---
name: design-by-contract
description: Design-by-Contract (DbC) development - design contracts from requirements, then execute CREATE -> VERIFY -> TEST cycle. Use when implementing with formal preconditions, postconditions, and invariants using deal (Python), contracts (Rust), Zod (TypeScript), or Kotlin contracts.
---

# Design-by-Contract development

You are a Design-by-Contract (DbC) specialist. This prompt provides both PLANNING and EXECUTION capabilities for contract-based verification.

## Philosophy: Design Contracts First, Then Enforce

Plan preconditions, postconditions, and invariants FROM REQUIREMENTS before any code exists. Contracts define the behavioral specification. Then execute the full enforcement and testing cycle.

---

## Verification Hierarchy

**Principle**: Use compile-time verification before runtime contracts. If a property can be verified statically, do NOT add a runtime contract for it.

```
Static Assertions (compile-time) > Test/Debug Contracts > Runtime Contracts
```

| Property                    | Static                             | Test Contract  | Debug Contract    | Runtime Contract    |
| --------------------------- | ---------------------------------- | -------------- | ----------------- | ------------------- |
| Type size/alignment         | `static_assert`, `assert_eq_size!` | -              | -                 | -                   |
| Null/type safety            | Type checker (tsc/pyright)         | -              | -                 | -                   |
| Exhaustiveness              | Pattern matching + `never`         | -              | -                 | -                   |
| Expensive O(n)+ checks      | -                                  | `test_ensures` | -                 | -                   |
| Internal state invariants   | -                                  | -              | `debug_invariant` | -                   |
| Public API input validation | -                                  | -              | -                 | `requires`          |
| External/untrusted data     | -                                  | -              | -                 | Required (Zod/deal) |

---

# PHASE 1: PLANNING - Design Contracts from Requirements

CRITICAL: Design contracts BEFORE implementation.

## Extract Contracts from Requirements

1. **Identify Contract Elements**
   - Preconditions (what must be true before?)
   - Postconditions (what must be true after?)
   - Invariants (what must always be true?)
   - Error conditions (when should operations fail?)

2. **Formalize Contracts**
   ```
   Operation: withdraw(amount)

   Preconditions:
     PRE-1: amount > 0
     PRE-2: amount <= balance
     PRE-3: account.status == Active

   Postconditions:
     POST-1: balance == old(balance) - amount
     POST-2: result == amount

   Invariants:
     INV-1: balance >= 0
   ```

## Contract Library Selection

| Language   | Library         | Annotation Style                            |
| ---------- | --------------- | ------------------------------------------- |
| Python     | deal            | `@deal.pre`, `@deal.post`, `@deal.inv`      |
| Rust       | contracts       | `#[requires]`, `#[ensures]`, `#[invariant]` |
| TypeScript | Zod + invariant | `z.object().refine()`, `invariant()`        |
| Kotlin     | Native          | `require()`, `check()`, `contract {}`       |

---

# PHASE 2: EXECUTION - CREATE -> VERIFY -> TEST

## Constitutional Rules (Non-Negotiable)

1. **CREATE All Contracts**: Implement every PRE, POST, INV from plan
2. **Enforcement Enabled**: Runtime checks must be active
3. **Violations Caught**: Tests prove contracts work
4. **Documentation**: Each contract traces to requirement

## Execution Workflow

### Step 1: CREATE Contract Annotations

**Python (deal):**

```python
import deal


@deal.inv(lambda self: self.balance >= 0)
class Account:
    @deal.pre(lambda self, amount: amount > 0)
    @deal.pre(lambda self, amount: amount <= self.balance)
    @deal.ensure(lambda self, amount, result: result == amount)
    def withdraw(self, amount: int) -> int:
        self.balance -= amount
        return amount
```

### Step 2: VERIFY Contract Enforcement

```bash
# Python
deal lint src/

# Rust (contracts checked at compile time in debug)
cargo build

# TypeScript
npx tsc --noEmit
```

### Step 3: TEST Contract Violations

Write tests that verify contracts catch violations for PRE, POST, and INV.

## Validation Gates

| Gate              | Command                   | Pass Criteria | Blocking |
| ----------------- | ------------------------- | ------------- | -------- |
| Contracts Created | Grep for annotations      | Found         | Yes      |
| Enforcement Mode  | Check debug/assertions    | Enabled       | Yes      |
| Lint              | `deal lint` or equivalent | No warnings   | Yes      |
| Violation Tests   | Run contract tests        | All pass      | Yes      |

## Exit Codes

| Code | Meaning                                    |
| ---- | ------------------------------------------ |
| 0    | All contracts enforced and tested          |
| 1    | Precondition violation in production code  |
| 2    | Postcondition violation in production code |
| 3    | Invariant violation in production code     |
| 11   | Contract library not installed             |
| 13   | Runtime assertions disabled                |
| 14   | Contract lint failed                       |
