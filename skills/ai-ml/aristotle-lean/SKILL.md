---
name: aristotle-lean
description: IMO Gold Medal level Lean4 theorem proving via Harmonic API
version: 1.0.0
---

# Aristotle Lean

**Trit**: -1 (MINUS)
**Domain**: Formal Verification / Theorem Proving
**Provider**: Harmonic (harmonic.fun)

## Overview

Aristotle is an IMO Gold Medal level Lean4 theorem prover that fills `sorry` holes in proofs, auto-generates counterexamples for false statements, and integrates with Mathlib and lake dependencies.

## API Configuration

```
Endpoint: aristotle.harmonic.fun
Auth: Auth0-based (requires signup/login at harmonic.fun)
```

## Capabilities

1. **Sorry Hole Filling**: Completes incomplete Lean4 proofs
2. **Dual Input**: Accepts English descriptions or Lean4 code
3. **Counterexample Generation**: Auto-generates counterexamples for false statements
4. **Project Integration**: Works with project theorems, lake dependencies, Mathlib
5. **PROVIDED SOLUTION Tag**: Use comment tag to mark solution regions

## Benchmarks

| Benchmark | Score |
|-----------|-------|
| MiniF2F   | 90%   |
| VERINA    | 96.8% |

## Usage Pattern

```lean
-- English prompt in comment
-- "Prove that the sum of two even numbers is even"

theorem sum_even (a b : ℕ) (ha : Even a) (hb : Even b) : Even (a + b) := by
  sorry  -- Aristotle fills this
```

```lean
-- PROVIDED SOLUTION: explicit solution marker
theorem my_theorem : P → Q := by
  -- PROVIDED SOLUTION
  sorry
```

## Integration with GF(3)

This skill participates in triadic composition:
- **Trit -1** (MINUS): Verification/validation/analysis
- **Conservation**: Σ trits ≡ 0 (mod 3) across skill triplets

## Related Skills

- lean4-metaprogramming (trit +1)
- mathlib-tactics (trit 0)
- proof-assistant (trit -1)
- formal-verification (trit -1)

---

**Skill Name**: aristotle-lean
**Type**: Formal Verification / Theorem Proving
**Trit**: -1 (MINUS)
**GF(3)**: Conserved in triplet composition

## Non-Backtracking Geodesic Qualification

**Condition**: μ(n) ≠ 0 (Möbius squarefree)

This skill is qualified for non-backtracking geodesic traversal:

1. **Prime Path**: No state revisited in skill invocation chain
2. **Möbius Filter**: Composite paths (backtracking) cancel via μ-inversion
3. **GF(3) Conservation**: Trit sum ≡ 0 (mod 3) across skill triplets
4. **Spectral Gap**: Ramanujan bound λ₂ ≤ 2√(k-1) for k-regular expansion

```
Geodesic Invariant:
  ∀ path P: backtrack(P) = ∅ ⟹ μ(|P|) ≠ 0
  
Möbius Inversion:
  f(n) = Σ_{d|n} g(d) ⟹ g(n) = Σ_{d|n} μ(n/d) f(d)
```
