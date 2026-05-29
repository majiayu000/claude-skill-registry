---
name: pre-agent-ontology
description: Pre-Agent Ontology Skill
version: 1.0.0
---

# Pre-Agent Ontology Skill

**Trit**: 0 (ERGODIC - coordinates the ontology)

Foundational 5-layer ontology for agent-o-rama. Agents are not primitives—they emerge from derivations, stalks, and sections when gluing succeeds.

## Related Skills
- **unworld**: Derivational succession (Layer 1)
- **sheaf-cohomology**: Gluing verification (Layer 2)
- **bisimulation-game**: Observational equivalence (Layer 2)
- **acsets**: Categorical database structure (Layer 2)

---

## 5-Layer Hierarchy

```
Layer 4: EMERGENT        agent, skill, experiment
            ↑
Layer 3: OPERATIONAL     node, emit, aggregation, result
            ↑
Layer 2: SHEAF           stalk, section, cohomology
            ↑
Layer 1: DERIVATIONAL    derivation, chain
            ↑
Layer 0: PRE-ONTOLOGICAL seed, trit, γ (gamma)
```

### Layer 0: Pre-Ontological (Absolute Primitives)

| Term | Type | Definition |
|------|------|------------|
| seed | uint64 | Deterministic state replacing time |
| trit | {-1, 0, +1} | GF(3) charge element |
| γ | constant | 0x9E3779B97F4A7C15 (golden ratio bits) |

### Layer 1: Derivational

| Term | Type | Definition |
|------|------|------------|
| derivation | (Seed × Trit) → (Seed × Section) | Fundamental computation unit |
| chain | [Seed] | Sequence of derived seeds |

**Rule**: `seed_{n+1} = splitmix64(seed_n ⊕ (trit_n × γ))`

### Layer 2: Sheaf-Theoretic

| Term | Type | Definition |
|------|------|------------|
| stalk | Set(Section) | Collection of sections over one trit |
| section | local data | Output of derivation, can glue |
| cohomology | (H⁰, H¹) | Global sections and obstructions |

**Stalk Distribution (2-3-2)**:
```
MINUS:   2 elements, trit=-1, role=validator
ERGODIC: 3 elements, trit=0,  role=coordinator
PLUS:    2 elements, trit=+1, role=generator

Verification: 2(-1) + 3(0) + 2(+1) = 0 ✓
```

### Layer 3: Operational

| Term | Sheaf Correspondence |
|------|---------------------|
| node | section-producer |
| emit | stalk transition |
| aggregation | gluing (cocycle check) |
| result | global section (H⁰ element) |

### Layer 4: Emergent

| Term | Definition |
|------|------------|
| agent | Fiber bundle over trit poset {-1, 0, +1} |
| skill | Executable section (self-contained knowledge) |
| experiment | Derivation chain evaluation |

**Key**: `Agent = Observation(Bundle(Stalk₋₁, Stalk₀, Stalk₊₁))`

---

## 5 Stability Invariants

| ID | Invariant | Formula | Verified By |
|----|-----------|---------|-------------|
| I1 | GF(3) Conservation | `Σ trits ≡ 0 (mod 3)` | aggregation, trifurcate |
| I2 | Determinism | `derive(s,t) = derive(s,t)` | seed chaining |
| I3 | Order Independence (SPI) | `parallel(f) = sequential(f)` | spi-parallel-verify |
| I4 | Gluing (Cocycle) | `g_ij ∘ g_jk = g_ik` | cohomology check |
| I5 | Bisimulation | `A ~ B ⟺ ∀obs. obs(A) = obs(B)` | bisimulation-game |

---

## Key Primitives

### Seed
64-bit unsigned integer replacing temporal state. Same seed → identical derivation chains.

### Trit
GF(3) element in {-1, 0, +1}. Forms a field under modular arithmetic.

### Derivation
Fundamental computation: `(Seed × Trit) → (Seed × Section)`

Replaces temporal succession with seed-based chaining.

### Stalk
Collection of sections over a single trit value. Organized as fiber bundle.

### Section
Local data produced by derivation. Sections glue to form global sections when cocycle condition holds.

---

## Trifurcation Pattern (MANDATORY)

Every operation MUST split into three sub-derivations:

```
             intent
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
    MINUS    ERGODIC   PLUS
    (-1)      (0)      (+1)
   validate  coordinate generate
       │        │        │
       └────────┼────────┘
                ▼
           aggregate
         (verify Σ=0)
```

| Sub-Agent | Trit | Role | Skills |
|-----------|------|------|--------|
| MINUS | -1 | Validator | spi-parallel-verify, bisimulation-game |
| ERGODIC | 0 | Coordinator | glass-bead-game, triad-interleave |
| PLUS | +1 | Generator | gflownet, self-evolving-agent |

---

## Clojure Implementation

### Constants
```clojure
(def GENESIS-SEED 0x42D)
(def GAMMA 0x9E3779B97F4A7C15)
(def MIX1 0xBF58476D1CE4E5B9)
(def MIX2 0x94D049BB133111EB)
```

### Derivation
```clojure
(defn derive-seed [seed trit]
  (let [adjusted (bit-xor seed (* trit GAMMA))]
    (splitmix64-next adjusted)))

(defn derivation-chain [genesis-seed trits]
  (reductions derive-seed genesis-seed trits))
```

### GF(3) Arithmetic
```clojure
(defn gf3-add [a b]
  (let [sum (+ a b)]
    (cond (> sum 1)  (- sum 3)
          (< sum -1) (+ sum 3)
          :else      sum)))

(defn gf3-conserved? [trits]
  (zero? (reduce gf3-add 0 trits)))
```

### Trifurcate Pattern
```clojure
;; Scatter: emit three roles
(aor/agg-start-node
 "scatter"
 "execute-role"
 (fn [agent-node {:keys [intent]}]
   (aor/emit! agent-node "execute-role" {:intent intent :role :minus})
   (aor/emit! agent-node "execute-role" {:intent intent :role :ergodic})
   (aor/emit! agent-node "execute-role" {:intent intent :role :plus})))

;; Gather: verify conservation
(aor/agg-node
 "execute-role"
 nil
 aggs/+vec-agg
 (fn [agent-node requests _]
   (let [results (mapv execute-role requests)
         trits (mapv :trit results)
         conserved? (gf3-conserved? trits)]
     (aor/result! agent-node {:conserved conserved? :trits trits}))))
```

---

## Verification Checklist

Before any operation completes:

- [ ] GF(3) sum ≡ 0 (mod 3)
- [ ] All three trits represented (trifurcation)
- [ ] Cocycle condition satisfied (sections glue)
- [ ] Deterministic (same seed → same result)
- [ ] Order-independent (SPI holds)

---

## Sources

- [ONTOLOGY.md](file:///Users/alice/agent-o-rama/agent-o-rama/dev/terms/ONTOLOGY.md)
- [derivation.md](file:///Users/alice/agent-o-rama/agent-o-rama/dev/terms/derivation.md)
- [CONTINUITY.md](file:///Users/alice/agent-o-rama/agent-o-rama/examples/clj/src/com/rpl/agent/CONTINUITY.md)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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