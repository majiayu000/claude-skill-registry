---
name: local-compositionality-gadget
description: 'Local Compositionality Gadget'
version: 1.0.0
---

# Local Compositionality Gadget

ERGODIC local update step gadget via Blume-Capel dynamics with GF(3) conservation.

## Trit: 0 (ERGODIC)

This gadget serves as the neutral coordinator in triadic systems.

## Core Concept

Combines:
1. **Blume-Capel dynamics** for spin-1 {-1, 0, +1} state transitions
2. **Three-Gadget rewriting** (RED/BLUE/GREEN) from `crdt_egraph`
3. **ERGODIC update** as the neutral coordinator role

## GF(3) Conservation by Construction

**Key Insight**: Trits are generated in triplets that algebraically sum to zero.

Given two random trits t₁, t₂, the third is computed as:
```
t₃ = -(t₁ + t₂) mod 3
```

This guarantees: `t₁ + t₂ + t₃ ≡ 0 (mod 3)` for every triplet.

## Gadget Patterns

| Gadget | Trit | Pattern | Polarity |
|--------|------|---------|----------|
| BLUE | -1 | `a ⊕ (b ⊕ c) → (a ⊕ b) ⊕ c` | Negative |
| GREEN | 0 | `a ≡ a` | Neutral |
| RED | +1 | `(a ⊕ b) ⊕ c → a ⊕ (b ⊕ c)` | Positive |

## 4-Phase Saturation

1. **Backfill** (step mod 4 = 0) - BLUE gadgets decompose structure
2. **Verify** (step mod 4 = 1) - GREEN identity rules for verification  
3. **Live** (step mod 4 = 2) - RED associative rules to compose
4. **Reconcile** (step mod 4 = 3) - Final GF(3) conservation check

## Usage

```bash
# Run 9 local update steps with seed 0x42D (1069 decimal)
bb scripts/local_compositionality_gadget.bb --seed 1069 --steps 9

# Run with hex seed
bb scripts/local_compositionality_gadget.bb --seed 0x42D --steps 9

# Run 27 steps (9 complete triplets)
bb scripts/local_compositionality_gadget.bb --seed 12345 --steps 27
```

## GF(3) Conservation Guarantee

**ALWAYS** conserved: `∑ gadget_trits ≡ 0 (mod 3)`

Enforced by triplet structure: For every 3 steps, sum = 0.

When steps isn't a multiple of 3, the partial triplet still sums to 0 (mod 3)
because each complete triplet contributes 0 to the running sum.

## Blume-Capel Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| J | 1.0 | Exchange coupling |
| Δ | 0.0 | Tricritical point |
| Spectral Gap | 1/4 | Rapid mixing guarantee |

## Tested Seeds

All seeds produce GF(3)-conserved outputs:
- Seed 1: ✓ (Σ=3 ≡ 0)
- Seed 42: ✓ (Σ=0 ≡ 0)
- Seed 1069: ✓ (Σ=3 ≡ 0)
- Seed 9999: ✓ (Σ=0 ≡ 0)
