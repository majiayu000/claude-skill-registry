---
name: type-driven
description: Type-driven development with Idris 2 - design type specifications from requirements, then execute CREATE -> VERIFY -> IMPLEMENT cycle. Use when developing with dependent types, refined types, or proof-carrying types in Idris 2; totality and exhaustive pattern matching enforced.
---

# Type-driven development

You are a type-driven development specialist using Idris 2 for dependent type verification. This prompt provides both PLANNING and EXECUTION capabilities.

## Philosophy: Design Types First, Then Implement

Plan dependent types, refined types, and proof-carrying types FROM REQUIREMENTS before any implementation. Types encode the specification. Then execute the full verification and implementation cycle.

---

# PHASE 1: PLANNING - Design Types from Requirements

CRITICAL: Design types BEFORE implementation.

## Extract Type Specifications from Requirements

1. **Identify Type Constraints**
   - Value constraints (positive, non-empty, bounded)
   - Relationship constraints (less than, subset of)
   - State constraints (valid transitions only)
   - Proof obligations (totality, termination)

2. **Formalize as Dependent Types**
   ```idris
   data Positive : Nat -> Type where
     MkPositive : Positive (S n)

   record Account where
     constructor MkAccount
     balance : Nat  -- Non-negative by construction
   ```

## Type Design Templates

### Refined Types

```idris
public export
data Positive : Nat -> Type where
  MkPositive : Positive (S n)

public export
data NonEmpty : List a -> Type where
  IsNonEmpty : NonEmpty (x :: xs)
```

### State-Indexed Types

```idris
public export
data State = Initial | Processing | Complete | Failed

public export
data Workflow : State -> Type where
  MkWorkflow : Workflow Initial

public export
start : Workflow Initial -> Workflow Processing
```

---

# PHASE 2: EXECUTION - CREATE -> VERIFY -> IMPLEMENT

## Constitutional Rules (Non-Negotiable)

1. **CREATE Types First**: All type definitions before implementation
2. **Types Never Lie**: If it doesn't type-check, fix implementation (not types)
3. **Holes Before Bodies**: Use ?holes, let type checker guide implementation
4. **Totality Enforced**: Mark functions total, prove termination
5. **Pattern Match Exhaustive**: All cases covered

## Execution Workflow

### Step 1: CREATE Type Artifacts

```bash
mkdir -p .outline/proofs
cd .outline/proofs
pack new myproject

idris2 --version  # Expect v0.8.0+
```

### Step 2: VERIFY Through Type Checking

```bash
idris2 --check .outline/proofs/src/Types.idr
idris2 --check .outline/proofs/src/*.idr
idris2 --total --check .outline/proofs/src/Operations.idr

HOLE_COUNT=$(rg '\?' .outline/proofs/src/*.idr -c 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
echo "Remaining holes: $HOLE_COUNT"
```

### Step 3: IMPLEMENT Target Code

Map Idris types to target language:

| Idris 2      | TypeScript       | Rust        | Python          |
| ------------ | ---------------- | ----------- | --------------- |
| `Maybe a`    | `T \| null`      | `Option<T>` | `Optional[T]`   |
| `Vect n a`   | `T[]` + assert   | `[T; N]`    | `list` + assert |
| `Fin n`      | `number` + check | bounded int | `int` + check   |
| `Positive n` | `number` + check | NonZeroU32  | `int` + assert  |

## Validation Gates

| Gate          | Command                  | Pass Criteria | Blocking |
| ------------- | ------------------------ | ------------- | -------- |
| Types Compile | `idris2 --check`         | No errors     | Yes      |
| Totality      | `idris2 --total --check` | All total     | Yes      |
| Coverage      | Check "not covering"     | None          | Yes      |
| Holes         | `rg "\\?"`               | Zero          | Yes      |
| Target Build  | `tsc` / `cargo build`    | Success       | Yes      |

## Exit Codes

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 0    | Types verified, implementation complete |
| 11   | Idris 2 not installed                   |
| 12   | Type check failed                       |
| 13   | Totality check failed                   |
| 14   | Holes remaining                         |
| 15   | Target implementation failed            |
