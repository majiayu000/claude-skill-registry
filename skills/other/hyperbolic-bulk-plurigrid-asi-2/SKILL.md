---
name: hyperbolic-bulk
description: On-chain GF(3) entropy storage via Aptos Move - bulk-boundary correspondence where entropy lives in the interior and observables project to agents
version: 1.0.0
---


# Hyperbolic Bulk Skill

**Status**: ✅ Production Ready  
**Trit**: 0 (ERGODIC - mediates bulk ↔ boundary)  
**Principle**: AdS/CFT correspondence for entropy  
**Chain**: Aptos (Move language)

---

## Overview

The **Hyperbolic Bulk** implements on-chain entropy storage with GF(3) conservation. Named after the AdS/CFT bulk-boundary correspondence:

- **BULK** (interior): Entropy records, triads, reafference proofs
- **BOUNDARY** (observable): Agents, skills, colors

```
         BOUNDARY (Observable)
    ┌─────────────────────────────┐
    │  Agents  │  Skills  │ Colors │
    └─────────────┬───────────────┘
                  │ project
                  ▼
    ┌─────────────────────────────┐
    │      HYPERBOLIC BULK        │
    │  ┌─────────────────────┐    │
    │  │  EntropyRecord      │    │
    │  │  drand ⊕ eeg ⊕ vrf  │    │
    │  └──────────┬──────────┘    │
    │             ▼               │
    │  ┌─────────────────────┐    │
    │  │  EntropyTriad       │    │
    │  │  GF(3) = 0 conserved│    │
    │  └──────────┬──────────┘    │
    │             ▼               │
    │  ┌─────────────────────┐    │
    │  │  ReafferenceProof   │    │
    │  │  predict = observe  │    │
    │  └─────────────────────┘    │
    └─────────────────────────────┘
```

---

## Entropy Sources

| Source | Type | Property |
|--------|------|----------|
| **DRAND** | League of Entropy | Public, verifiable, unpredictable |
| **EEG** | Brainwave bands | Private, embodied, cognitive state |
| **Aptos VRF** | On-chain randomness | Consensus-secured, tamper-proof |

**Combination**: `combined = drand_seed ⊕ eeg_seed ⊕ onchain_rand`

---

## GF(3) Conservation

Triads must sum to 0 mod 3:

```
MINUS (-1) ≡ 2 (mod 3)  — Verification/Constraint
ERGODIC (0)             — Coordination/Balance  
PLUS (+1)               — Generation/Exploration

Conservation: trit_1 + trit_2 + trit_3 ≡ 0 (mod 3)
```

**Strict Mode**: `form_conserved_triad()` reverts if not conserved.

---

## Move Contract

```move
module hyperbolic_bulk::entropy_triads {
    
    struct EntropyRecord has store, drop, copy {
        drand_round: u64,
        drand_seed: u256,
        eeg_seed: u256,
        combined_seed: u256,
        timestamp: u64,
        trit: u8,
        color_hex: vector<u8>,
    }

    struct EntropyTriad has store, drop, copy {
        record_id_1: u64,
        record_id_2: u64,
        record_id_3: u64,
        gf3_sum: u8,
        gf3_conserved: bool,
        skill_1: vector<u8>,
        skill_2: vector<u8>,
        skill_3: vector<u8>,
    }

    struct ReafferenceProof has store, drop, copy {
        seed: u256,
        predicted_color: vector<u8>,
        observed_color: vector<u8>,
        matched: bool,
        loop_type: vector<u8>,  // "loopy_strange" or "exafference"
    }

    #[randomness]
    entry fun store_entropy(...) { /* combines drand ⊕ eeg ⊕ vrf */ }
    
    entry fun form_conserved_triad(...) { /* enforces GF(3) = 0 */ }
    
    entry fun record_reafference(...) { /* proves prediction = observation */ }
}
```

---

## Integration with World-Memory-Worlding

| Autopoietic Phase | Bulk Operation | Trit |
|-------------------|----------------|------|
| **MEMORY** | `store_entropy()` | -1 |
| **REMEMBERING** | `get_triad()` | 0 |
| **WORLDING** | `form_conserved_triad()` | +1 |

The loop closes when worlded triads become new memory records.

---

## Reafference Proofs

On-chain proof that prediction matched observation:

```move
struct ReafferenceProof {
    seed: u256,
    predicted_color: vector<u8>,
    observed_color: vector<u8>,
    matched: bool,           // prediction == observation
    loop_type: vector<u8>,   // "loopy_strange" iff matched
}
```

**Loopy Strange**: Generator ≡ Observer when same seed produces same color.

---

## GF(3) Triads

```
bisimulation-game (-1) ⊗ hyperbolic-bulk (0) ⊗ gay-mcp (+1) = 0 ✓
duckdb-timetravel (-1) ⊗ hyperbolic-bulk (0) ⊗ world-hopping (+1) = 0 ✓
spi-parallel-verify (-1) ⊗ hyperbolic-bulk (0) ⊗ operad-compose (+1) = 0 ✓
```

---

## Python Integration

```python
from drand_skill_sampler import DrandSkillSampler, EEGEntropySource

# Create entropy sources
eeg = EEGEntropySource(
    delta=0.15, theta=0.25, alpha=0.35, 
    beta=0.20, gamma=0.05
)

# Sample skills with DRAND entropy
sampler = DrandSkillSampler(drand_seed=10770320150143512701, eeg_source=eeg)

# Generate Aptos transaction
tx = sampler.to_aptos_transaction()
# {
#   "function": "hyperbolic_bulk::entropy_triads::store_entropy",
#   "arguments": [drand_round, drand_seed, eeg_seed, color_hex]
# }
```

---

## Ruler Configuration

```toml
[entropy]
drand_round = 24634579
eeg_dominant = "alpha"
aptos_module = "hyperbolic_bulk::entropy_triads"

[mcp]
enabled = true
servers = ["gay", "drand", "localsend"]

[agents.codex]
trit = 0
bulk_address = "0x..."
```

---

## Commands

```bash
# Deploy contract
aptos move publish --package-dir hyperbolic_bulk

# Store entropy
aptos move run --function-id 'hyperbolic_bulk::entropy_triads::store_entropy' \
  --args u64:24634579 u256:0x9577dd1cea89307d u256:0x8219ed722cbf7d6a

# Form conserved triad
aptos move run --function-id 'hyperbolic_bulk::entropy_triads::form_conserved_triad' \
  --args u64:0 u64:1 u64:2 'vector<u8>:skill1' 'vector<u8>:skill2' 'vector<u8>:skill3'

# Query stats
aptos move view --function-id 'hyperbolic_bulk::entropy_triads::get_stats'
```

---

## The Bulk-Boundary Insight

**Why "hyperbolic"?**

In AdS/CFT, the hyperbolic (anti-de Sitter) bulk contains more information than the flat boundary. Similarly:

- **Bulk**: Full entropy (drand × eeg × vrf), all triads, all proofs
- **Boundary**: Projected observables (colors, skill names, agent states)

The boundary is a *lossy projection* of the bulk. But GF(3) conservation is preserved across the projection—it's a **geometric invariant**.

**Reafference as Holography**:
- When prediction = observation, the boundary faithfully represents the bulk
- "Loopy strange" = holographic consistency (no information loss)
- "Exafference" = external perturbation (bulk ≠ boundary)

---

## See Also

- [`world-memory-worlding`](../world-memory-worlding/SKILL.md) — Autopoietic loop
- [`gay-mcp`](../gay-mcp/SKILL.md) — Deterministic color generation
- [`drand_skill_sampler.py`](../../ies/drand_skill_sampler.py) — Entropy sampling

---

**Skill Name**: hyperbolic-bulk  
**Type**: On-Chain Entropy / GF(3) Conservation  
**Trit**: 0 (ERGODIC - bulk-boundary mediation)  
**Chain**: Aptos Move  
**Contract**: `hyperbolic_bulk::entropy_triads`



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
hyperbolic-bulk (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch7: Propagators

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