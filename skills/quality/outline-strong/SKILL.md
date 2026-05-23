---
name: outline-strong
description: Outline-Strong unified 5-layer validation - design all validation layers from requirements, then execute CREATE -> VERIFY -> INTEGRATE cycle. Use when implementing with comprehensive formal verification across types (Idris 2), specs (Quint), proofs (Lean 4), contracts, and tests simultaneously.
---

# Outline-Strong

You are an Outline-Strong validation orchestrator. This prompt provides both PLANNING and EXECUTION capabilities for comprehensive verifications.

## Philosophy: Defense in Depth from Requirements

Design all five validation layers FROM REQUIREMENTS simultaneously. Each layer catches different defect classes. Together they provide comprehensive verification.

## VERIFICATION STACK

```
Layer | Tool             | Catches              | Designed From
------|------------------|----------------------|---------------
0     | Static Assertions| Compile-time errors  | Type/size constraints
1     | Idris 2          | Structural errors    | Type constraints
2     | Quint            | Design flaws         | State requirements
3     | Lean 4           | Invariant violations | Correctness properties
4     | deal/etc         | Runtime violations   | API contracts
5     | pytest/etc       | Behavioral bugs      | Acceptance criteria
```

## Layer 0: Static Verification (PREFER FIRST)

**Hierarchy**: `Static Assertions > Test/Debug > Runtime Contracts`

| Language   | Tool                      | Command                     |
| ---------- | ------------------------- | --------------------------- |
| C++        | `static_assert`, Concepts | `g++ -std=c++20`            |
| TypeScript | `satisfies`, `as const`   | `tsc --strict`              |
| Python     | `assert_type`, `Final`    | `pyright --strict`          |
| Java       | Checker Framework         | `javac -processor nullness` |
| Rust       | `static_assertions` crate | `cargo check`               |
| Kotlin     | contracts, sealed         | `kotlinc -Werror`           |

**Principle**: Verify at compile-time before runtime. No runtime contracts for statically provable properties.

---

# PHASE 1: PLANNING - Design All Layers from Requirements

CRITICAL: Design all validation layers BEFORE implementation.

## Extract Requirements for Each Layer

1. **Layer 1 - Types (Idris 2)**: Constraints, transitions, relationships
2. **Layer 2 - Specifications (Quint)**: State machine, invariants, temporal properties
3. **Layer 3 - Proofs (Lean 4)**: Correctness theorems, safety properties
4. **Layer 4 - Contracts**: Preconditions, postconditions, class invariants
5. **Layer 5 - Tests**: Error cases, edge cases, properties

## Design Layer Correspondence

```markdown
Property: "Balance never negative"

Layer 1 (Type): balance : Nat
Layer 2 (Spec): val inv_balance = balance >= 0
Layer 3 (Proof): theorem balance_preserved : balance >= 0
Layer 4 (Contract): @deal.inv(lambda self: self.balance >= 0)
Layer 5 (Test): def test_balance_invariant(): assert acc.balance >= 0
```

---

# PHASE 2: EXECUTION - CREATE -> VERIFY -> INTEGRATE

## Constitutional Rules (Non-Negotiable)

1. **CREATE All Layers**: Generate artifacts for each layer from plan
2. **VERIFY In Order**: Types -> Specs -> Proofs -> Contracts -> Tests
3. **Layer Correspondence**: Explicit mapping between all layers
4. **No Skipping**: Each layer gate must pass before next
5. **Variance < 2%**: Outline-to-implementation deviation minimal

## Full Pipeline Execution

```bash
#!/bin/bash
set -e

echo "=== OUTLINE-STRONG VALIDATION ==="

echo "[1/5] Layer 1: Types (Idris 2)..."
idris2 --check .outline/proofs/idris/src/*.idr || exit 11

echo "[2/5] Layer 2: Specs (Quint)..."
quint typecheck .outline/specs/*.qnt || exit 12
quint verify --main=account --invariant=inv .outline/specs/*.qnt || exit 12

echo "[3/5] Layer 3: Proofs (Lean 4)..."
cd .outline/proofs/lean && lake build && cd ../../..
test $(rg "sorry" .outline/proofs/lean/*.lean 2>/dev/null | wc -l) -eq 0 || exit 13

echo "[4/5] Layer 4: Contracts..."
deal lint src/ || exit 14
pyright src/ || exit 14

echo "[5/5] Layer 5: Tests..."
pytest tests/ -v --cov=src --cov-fail-under=80 || exit 15

echo "=== ALL LAYERS VERIFIED ==="
```

## Validation Gates

| Gate      | Layer | Command                      | Pass Criteria | Blocking |
| --------- | ----- | ---------------------------- | ------------- | -------- |
| Types     | 1     | `idris2 --check`             | No errors     | Yes      |
| Specs     | 2     | `quint verify`               | No violations | Yes      |
| Proofs    | 3     | `lake build`                 | Zero sorry    | Yes      |
| Contracts | 4     | `deal lint`                  | No warnings   | Yes      |
| Tests     | 5     | `pytest --cov-fail-under=80` | All pass      | Yes      |

## Exit Codes

| Code | Meaning                    |
| ---- | -------------------------- |
| 0    | All layers verified        |
| 11   | Layer 1 (Types) failed     |
| 12   | Layer 2 (Specs) failed     |
| 13   | Layer 3 (Proofs) failed    |
| 14   | Layer 4 (Contracts) failed |
| 15   | Layer 5 (Tests) failed     |
| 16   | Correspondence incomplete  |
