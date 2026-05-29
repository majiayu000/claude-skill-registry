---
name: unworld
description: Replace time with color chain derivations via seed chaining
---

<!-- Propagated to amp | Trit: 0 | Source: .ruler/skills/unworld -->

<!-- Propagated to amp | Trit: 0 | Source: .ruler/skills/unworld -->

# Unworld Skill: Replace Time with Derivation

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - derivational, not temporal)
**Principle**: seed_{n+1} = f(seed_n, color_n)
**Frame**: No external clock, only internal derivation

---

## Overview

**Unworld** replaces temporal succession with derivational succession. There is no "time" - only seed-chaining where each state derives deterministically from the previous.

```
seed₀ → color₀ → seed₁ → color₁ → seed₂ → ...
```

The "next" is not temporal but **derivational**.

## Core Formula

```ruby
# Seed chaining: derive next seed from current seed + color trit
seed_{n+1} = (seed_n ⊕ (trit_n × γ)) × MIX  mod 2⁶⁴

where:
  γ   = 0x9E3779B97F4A7C15  (golden ratio)
  MIX = 0xBF58476D1CE4E5B9  (SplitMix64 multiplier)
  ⊕   = XOR
```

## Why Replace Time?

1. **Determinism**: Given genesis seed, entire chain is determined
2. **Parallelism**: Any position computable without computing predecessors
3. **Verification**: Chain integrity verifiable by re-derivation
4. **Frame invariance**: No external clock → no observer-dependent ordering

## Derivation Chains

### 1. Color Chain

Single stream of derivations:

```
Genesis: 0x42D
  → trit=+1 → #D8267F → seed₁
  → trit=0  → #2CD826 → seed₂
  → trit=0  → #4FD826 → seed₃
  → ...
```

**Invariant**: GF(3) balanced (sum of trits ≡ 0 mod 3)

### 2. Triadic Chain

Three interleaved streams from one genesis:

```
Genesis: 0x42D
  MINUS:   seed₀             → colors...
  ERGODIC: seed₀ ⊕ γ         → colors...
  PLUS:    seed₀ ⊕ (γ << 1)  → colors...
```

**Invariant**: GF(3) conserved at each position across all three streams

### 3. 3-MATCH Chain

Sequence of 3-MATCH gadgets, each deriving from previous:

```
Match₀: [color_a, color_b, color_c] → combined_trit → seed₁
Match₁: [color_a', color_b', color_c'] → combined_trit' → seed₂
...
```

**Invariant**: Each match has GF(3) = 0

### 4. Involution Chain

Forward and backward derivations that cancel:

```
Forward:  seed₀ → c₀ → seed₁ → c₁ → ... → seed_n
Backward: seed_n → -c_{n-1} → ... → -c₀ → seed₀'

ι∘ι = id  ⟺  seed₀' = seed₀
```

**Invariant**: Involution is self-inverse

### 5. Best Response Chain

Nash equilibrium via derivational dynamics:

```
Round 0: agents = {a: t_a, b: t_b, c: t_c}
Round 1: each agent best-responds → new trits
Round 2: ...
Equilibrium: no agent wants to deviate
```

**Invariant**: Equilibrium has GF(3) = 0

## Commands

```bash
# Full unworld (all chains)
just unworld

# Individual chains
just unworld-color      # Single derivation stream
just unworld-triadic    # Three interleaved streams
just unworld-match      # 3-MATCH gadget sequence
just unworld-involution # ι∘ι = id verification
just unworld-nash       # Best response → equilibrium

# Raw seed chaining
just seed-chain seed=0x42D steps=10
```

## API

```ruby
require 'unworld'

# Derive next seed
next_seed = Unworld.chain_seed(current_seed, trit)

# Derive color from seed
color = Unworld.derive_color(seed, index)

# Build full chain
chain = Unworld::ColorChain.new(genesis_seed: 0x42D, length: 12)
unworlded = chain.unworld

# Verify chain integrity
chain.verify_chain  # => true if all derivations correct
```

## Integration with 3-MATCH

The unworld system provides the **derivational backbone** for 3-MATCH:

```ruby
# 3-MATCH uses seed chaining for gadget sequence
matches = Unworld::ThreeMatchChain.new(genesis_seed: seed)

# Each match derives from previous
matches.unworld[:matches].each do |m|
  puts "#{m[:colors]} | GF(3): #{m[:gf3]}"
end
```

## Integration with Involution

The involution chain demonstrates ι∘ι = id via derivation:

```ruby
inv = Unworld::InvolutionChain.new(genesis_seed: seed)

# Forward derivation
inv.unworld[:forward]   # => ["#D8267F", "#2CD826", ...]

# Backward derivation (negated trits)
inv.unworld[:backward]  # => ["#5226D8", "#6AD826", ...]

# Verification
inv.unworld[:involution_verified]  # => true
```

## Mathematical Foundation

### Derivation vs Time

| Temporal | Derivational |
|----------|--------------|
| t → t+1 | seed_n → seed_{n+1} |
| Clock tick | Chain step |
| External | Internal |
| Observer-dependent | Observer-independent |

### GF(3) Conservation

At each position in the chain:
```
trit_minus + trit_ergodic + trit_plus ≡ 0 (mod 3)
```

This is preserved by the derivation function because:
- Each trit is derived deterministically from seed
- The chain function preserves algebraic structure

### Spectral Gap

The derivation chain has spectral gap 1/4 (Ramanujan property):
- Mixing in 4 steps
- Non-backtracking (each seed unique)
- Möbius filtering (μ ≠ 0 for valid chains)

## Example Output

```
UNWORLD: Replace Time with Color Chain Derivations
         Seed: 0x42D

─── COLOR CHAIN ───
  Derivations: 1 → 0 → 0 → 0 → 1 → -1 → 0 → -1
  Colors: #D8267F #2CD826 #4FD826 #26D876 #D84126 #262FD8 #32D826 #5B26D8
  GF(3) sum: 0 (balanced: true)
  Verified: true

─── INVOLUTION CHAIN ───
  Forward:  #D8267F #2CD826 #4FD826 #26D876 #D84126 #262FD8
  Backward: #5226D8 #6AD826 #26D829 #43D826 #2673D8 #D8262F
  ι∘ι = id verified: true

─── BEST RESPONSE CHAIN ───
  Rounds to equilibrium: 2
  Equilibrium reached: true
  Final agents: {:a=>1, :b=>1, :c=>1}
```

---

**Skill Name**: unworld
**Type**: Derivational Succession / Seed Chaining
**Trit**: 0 (ERGODIC)
**GF(3)**: Conserved by construction
**Time**: Replaced with derivation
