---
name: chromatic-walk
description: 3 parallel agents explore codebase improvements via GF(3) balanced prime geodesics
version: 1.0.0
---


# Chromatic Walk Skill

**Trit**: 0 (ERGODIC - navigates between generation and validation)  
**Coordinator Color**: #D06546 (burnt sienna, transport of earth)  
**Seed**: 1069 (0x42D)

---

## Overview

Chromatic Walk enables **3 parallel agents** to explore codebase improvements using GF(3)-balanced derivation chains. Each agent holds a trit polarity, and together they form a self-boiling triad.

Walks are **prime geodesics**: non-backtracking paths that are unambiguously traversable in p-adic number systems.

```
Generator (⊕)  ─────┐
                    ├──→  GF(3) = 0  ──→  Prime Geodesic
Coordinator (○) ────┤
                    │
Validator (⊖)  ─────┘
```

---

## The 3-Agent Structure

| Role | Trit | Color | Action | Responsibility |
|------|------|-------|--------|----------------|
| **Generator** | +1 | #D82626 (Red) | Create | Propose code changes, new patterns |
| **Coordinator** | 0 | #26D826 (Green) | Transport | Formalize structure, derive next seed |
| **Validator** | -1 | #2626D8 (Blue) | Verify | Check invariants, reduce to essence |

---

## Prime Geodesic Foundation

See [PRIME_GEODESICS.md](./PRIME_GEODESICS.md) for full mathematical foundation.

### Why Non-Backtracking?

| Property | Prime Path | Composite Path |
|----------|------------|----------------|
| Factorization | **Unique** | Multiple |
| p-adic valuation | **Well-defined** | Ambiguous |
| Möbius μ(n) | ≠ 0 | = 0 (filtered) |
| Ihara zeta | **Contributes** | Ignored |

**Key insight**: Chromatic walks are prime geodesics in derivation space, traversable unambiguously by zeta functions.

### Zeta Function Traversability

| Zeta | Domain | Primes |
|------|--------|--------|
| Riemann ζ(s) | ℤ | Prime numbers |
| Ihara ζ_G(u) | Graphs | Non-backtracking cycles |
| Dedekind ζ_K(s) | Number fields | Prime ideals |
| Selberg Z(s) | Manifolds | Prime geodesics |

---

## Seed Chaining Across Agents

Each agent derives its seed from the shared genesis, offset by the golden ratio:

```ruby
genesis = 0x42D  # 1069
γ = 0x9E3779B97F4A7C15  # Golden ratio constant

seed_generator   = genesis                    # +1 stream
seed_coordinator = genesis ^ γ                # 0 stream  
seed_validator   = genesis ^ (γ << 1)         # -1 stream
```

### Derivation Chain (per step)

```
seed_{n+1} = (seed_n ⊕ (trit_n × γ)) × MIX  mod 2⁶⁴
```

---

## GF(3) Conservation Invariant

At every step of the walk:

```
trit_generator + trit_coordinator + trit_validator ≡ 0 (mod 3)
      (+1)      +       (0)       +      (-1)      =   0  ✓
```

### Self-Boiling Property

Like the Three Chromatic Samovars:
- Generator provides +1 (creative surplus)
- Validator provides -1 (critical reduction)  
- Coordinator provides 0 (transport without change)

---

## Walk Protocol

### Phase 1: Genesis
```bash
just chromatic-walk seed=1069
```

### Phase 2: Propose (Generator leads)
Generator proposes a codebase change with +1 trit.

### Phase 3: Formalize (Coordinator transports)
Coordinator structures the proposal, deriving the interface.

### Phase 4: Verify (Validator constrains)
Validator checks invariants and reduces.

### Phase 5: Commit (combined)
If GF(3) = 0 at walk end, the improvement is committed.

---

## Commands

```bash
just chromatic-walk seed=1069         # Initialize walk
just chromatic-walk-step seed=1069    # Run single step
just chromatic-walk-verify seed=1069  # Verify GF(3) conservation
```

---

## Triad Bundles

```
three-match (-1) ⊗ chromatic-walk (0) ⊗ gay-mcp (+1) = 0 ✓  [Core Walk]
ramanujan-expander (-1) ⊗ ihara-zeta (0) ⊗ moebius-inversion (+1) = 0 ✓  [Prime Netting]
```

---

## Goblin Integration

Chromatic-walk is the **0 Coordinator** in the goblin triad:

```
shadow-goblin (-1) ⊗ chromatic-walk (0) ⊗ agent-o-rama (+1) = 0 ✓
```

| Role | Trit | Color | Action |
|------|------|-------|--------|
| Shadow Goblin | -1 | #F0D127 | Validates walks |
| **Chromatic Walk** | **0** | **#46F27F** | **Transports derivations** |
| Agent-O-Rama | +1 | #E7B367 | Generates proposals |

### Coordinator Capabilities

As the 0 goblin, Chromatic Walk provides:
- **Transport**: Move context between generator and validator
- **Derive**: Compute next seed in derivation chain
- **Navigate**: Traverse between realms (Beautiful Realms)
- **Balance**: Ensure triad sums remain at GF(3) = 0

### Color Stream (Seed 1069, Stream 2)

```
Step 1: #46F27F (mint green)     ○ Transport
Step 2: #E2282A (vivid red)      ○ Derive
Step 3: #EE55F2 (hot pink)       ○ Navigate
```

## Related Skills

| Skill | Relation |
|-------|----------|
| **unworld** | Seed chaining foundation |
| **ihara-zeta** | Non-backtracking enumeration |
| **ramanujan-expander** | Spectral gap verification |
| **moebius-inversion** | Composite filtering |
| **gay-mcp** | Deterministic color generation |
| **shadow-goblin** | Validates walks (-1) |
| **agent-o-rama** | Generates proposals (+1) |

---

**Skill Name**: chromatic-walk  
**Type**: Multi-Agent Prime Geodesic Exploration  
**Trit**: 0 (ERGODIC)  
**GF(3)**: Conserved by construction  
**Backtracking**: Forbidden (composites are p-adically imprecise)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Stochastic
- **simpy** [○] via bicomodule
  - Stochastic processes

### Bibliography References

- `graph-theory`: 38 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
chromatic-walk (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.