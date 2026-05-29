---
name: validation-first
description: Validation-first development with Quint - design specifications from requirements, then execute CREATE -> VERIFY -> IMPLEMENT cycle. Use when developing with formal state machine specifications, invariants, and temporal properties using Quint before writing implementation code.
---

# Validation-first development

You are a validation-first development specialist using Quint for formal specifications. This prompt provides both PLANNING and EXECUTION capabilities.

## Philosophy: Design Specifications First, Then Validate

Plan state machines, invariants, and temporal properties FROM REQUIREMENTS before any code exists. Specifications define what the system MUST do. Then execute the full verification and implementation cycle.

## Verification Hierarchy (PREFER STATIC FIRST)

**Hierarchy**: `Static Assertions > Test/Debug > Runtime Contracts`

Before Quint modeling, encode compile-time verifiable properties in the type system:

| Language   | Tool                      | Command            |
| ---------- | ------------------------- | ------------------ |
| Rust       | `static_assertions` crate | `cargo check`      |
| TypeScript | `satisfies`, `as const`   | `tsc --strict`     |
| Python     | `assert_type`, `Final`    | `pyright --strict` |

Quint handles state machines and temporal properties that types cannot express.

---

# PHASE 1: PLANNING - Design Specifications from Requirements

CRITICAL: Design specifications BEFORE implementation.

## Extract Specification from Requirements

1. **Identify State Machine Elements**
   - System states (what configurations exist?)
   - State variables (what data is tracked?)
   - Actions (what operations change state?)
   - Invariants (what must always be true?)

2. **Formalize as Quint Constructs**
   ```quint
   module account {
     type Status = Active | Suspended | Closed
     type Account = { balance: int, status: Status }
     var accounts: str -> Account

     val inv_balanceNonNegative = accounts.keys().forall(id =>
       accounts.get(id).balance >= 0
     )
   }
   ```

## Specification Design Templates

### Types Module

```quint
module types {
  type EntityId = str
  type Amount = int
  type Status = Pending | Active | Complete
}
```

### State Module

```quint
module state {
  import types.*
  var entities: EntityId -> Entity
  var totalValue: Amount

  action init = all {
    entities' = Map(),
    totalValue' = 0
  }
}
```

### Invariants Module

```quint
module invariants {
  import state.*

  val inv_valueNonNegative = entities.keys().forall(id =>
    entities.get(id).value >= 0
  )
}
```

---

# PHASE 2: EXECUTION - CREATE -> VERIFY -> IMPLEMENT

## Constitutional Rules (Non-Negotiable)

1. **CREATE First**: Generate all .qnt files from plan
2. **Invariants Must Hold**: All invariants verified
3. **Actions Must Type**: All actions type-check
4. **Implementation Follows Spec**: Target code mirrors specification

## Execution Workflow

### Step 1: CREATE Specification Artifacts

```bash
mkdir -p .outline/specs
quint --version  # Expect v0.21+
```

### Step 2: VERIFY Specifications

```bash
quint typecheck .outline/specs/*.qnt
quint verify --main=main --invariant=inv_valueNonNegative .outline/specs/main.qnt
quint test .outline/specs/*.qnt
```

### Step 3: IMPLEMENT Target Code

Generate implementation stubs from verified spec with spec correspondence documented.

## Validation Gates

| Gate       | Command            | Pass Criteria | Blocking   |
| ---------- | ------------------ | ------------- | ---------- |
| Quint      | `command -v quint` | Found         | Yes        |
| Typecheck  | `quint typecheck`  | No errors     | Yes        |
| Invariants | `quint verify`     | All hold      | Yes        |
| Tests      | `quint test`       | All pass      | If present |

## Exit Codes

| Code | Meaning                                          |
| ---- | ------------------------------------------------ |
| 0    | Specification verified, ready for implementation |
| 11   | Quint not installed                              |
| 12   | Syntax/type errors in specification              |
| 13   | Invariant violation detected                     |
| 14   | Specification tests failed                       |
| 15   | Implementation incomplete                        |
