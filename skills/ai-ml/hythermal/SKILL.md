---
name: hythermal
description: HyThermal Skill
version: 1.0.0
---

# HyThermal Skill

> Hy + Thermal: Relational ACSet dynamics with Langevin temperature control

**Version**: 1.0.0
**Trit**: 0 (ERGODIC - bridges relational structure and thermal flow)
**Bundle**: dynamics
**Fusion of**: `hyjax-relational` + `langevin-dynamics`

---

## Overview

**HyThermal** fuses relational thinking (ACSets/C-Sets) with Langevin dynamics for temperature-controlled exploration of concept spaces. Instead of treating thread analysis as static graphs, HyThermal models concepts as particles in a thermal bath:

- **Concepts** = Particles with positions in embedding space
- **Relations** = Potential energy between particles
- **Temperature** = Exploration vs exploitation control
- **Fokker-Planck** = Equilibrium distribution of concept activations

## Core Equation

```
dC(t) = -∇E(C(t)) dt + √(2T) dW(t)

Where:
  C = concept embedding positions
  E = relational energy (sum of edge potentials)
  T = temperature (exploration parameter)
  dW = Brownian motion (seeded via Gay.jl)
```

At equilibrium: `p∞(C) ∝ exp(-E(C)/T)` — Concepts cluster near low-energy (high-coherence) configurations.

## Hy Syntax for Thermal ACSet

```hy
;; Define thermal schema
(defschema ThermalThread
  (Ob Thread Message Concept)
  (Hom thread_msg (-> Message Thread)
       discusses (-> Message Concept)
       related (-> Concept Concept))
  (Attr position (-> Concept R^n)
        temperature (-> Thread Float)
        energy (-> Concept Float)))

;; Langevin step in Hy
(defn thermal-step [acset dt T seed]
  (let [concepts (parts acset :Concept)
        gradient (compute-relational-gradient acset)
        noise (gay-randn seed (len concepts))]
    (for [c concepts]
      (setv (. acset [:position c])
            (+ (. acset [:position c])
               (* (- dt) (get gradient c))
               (* (sqrt (* 2 T dt)) (get noise c)))))))

;; Run to equilibrium
(defn thermal-equilibrate [acset T n-steps seed]
  (for [step (range n-steps)]
    (thermal-step acset 0.01 T (gay-split seed step)))
  acset)
```

## Colored Thermal S-expressions

```lisp
(thermal-acset-gold
  (threads-red
    (thread T-001 :temp 0.01 :energy -4.52)
    (thread T-002 :temp 0.1 :energy -2.18))
  (concepts-green
    (concept skill :pos [0.3 0.7] :trit +1)
    (concept MCP :pos [0.5 0.2] :trit 0)
    (concept thermal :pos [0.8 0.9] :trit -1))
  (relations-purple
    (edge skill MCP :weight 2 :potential -0.8)
    (edge MCP thermal :weight 1 :potential -0.3)))
```

## Relational Energy Function

```python
def relational_energy(acset, positions):
    """
    E(C) = Σ_edges w_ij * d(c_i, c_j)^2 - Σ_hubs hub_score(c)

    Low energy = Concepts tightly connected + high hub scores
    """
    E = 0.0
    for edge in acset.parts('related'):
        i, j = acset.src(edge), acset.tgt(edge)
        w = acset.attr(edge, 'weight')
        E += w * np.linalg.norm(positions[i] - positions[j])**2

    for c in acset.parts('Concept'):
        E -= acset.attr(c, 'hub_score')

    return E
```

## Capabilities

### 1. thermal-thread-analysis

Run thermal dynamics on thread concept graph:

```bash
just hythermal-analyze threads.jsonl --temp 0.01 --steps 1000
```

Output:
```
HYTHERMAL ANALYSIS - 30 THREADS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Temperature: 0.01
Steps: 1000
Final energy: -12.45

EQUILIBRIUM CONCEPT POSITIONS:
  skill     [0.42, 0.73] trit=+1 (hub)
  MCP       [0.38, 0.71] trit=0  (near skill)
  thermal   [0.15, 0.22] trit=-1 (isolated)

THERMAL CLUSTERS:
  Cluster 1 (T=0.01): [skill, MCP, subagent] E=-8.2
  Cluster 2 (T=0.01): [thermal, langevin]    E=-4.1
```

### 2. temperature-sweep

Explore different temperatures:

```python
from hythermal import temperature_sweep

results = temperature_sweep(
    acset=thread_acset,
    temperatures=[0.001, 0.01, 0.1, 1.0],
    n_steps=500,
    seed=0x1069
)

for T, metrics in results.items():
    print(f"T = {T}:")
    print(f"  Final energy: {metrics['energy']:.3f}")
    print(f"  Cluster count: {metrics['n_clusters']}")
    print(f"  Mixing time: {metrics['tau_mix']:.0f}")
```

### 3. fokker-planck-concepts

Verify concept distribution reaches Gibbs equilibrium:

```python
from hythermal import verify_concept_gibbs

verification = verify_concept_gibbs(
    acset=equilibrated_acset,
    temperature=0.01
)

print(f"KL divergence from Gibbs: {verification['kl']:.4f}")
print(f"Converged: {verification['converged']}")
```

### 4. thermal-colored-sexp

Generate colored S-expression with thermal annotations:

```hy
(defn thermal-sexp [acset]
  `(thermal-acset-gold
    (threads-red
      ~@(lfor t (parts acset :Thread)
          `(thread ~t :temp ~(. acset [:temperature t])
                      :energy ~(thread-energy acset t))))
    (concepts-green
      ~@(lfor c (parts acset :Concept)
          `(concept ~(name c)
                    :pos ~(. acset [:position c])
                    :trit ~(gay-trit (hash (name c))))))
    (relations-purple
      ~@(lfor e (parts acset :related)
          `(edge ~(src e) ~(tgt e)
                 :weight ~(. acset [:weight e])
                 :potential ~(edge-potential acset e))))))
```

## GF(3) Thermal Triad

| Trit | Skill | Thermal Role |
|------|-------|--------------|
| -1 | fokker-planck-analyzer | Validates equilibrium |
| 0 | **hythermal** | Bridges structure + dynamics |
| +1 | entropy-sequencer | Optimizes sequences |

**Conservation**: (-1) + (0) + (+1) = 0

## Integration Points

### With hyjax-relational
```hy
;; Import relational schema
(require hyjax-relational [SchThread parts attr])

;; Extend with thermal attributes
(defschema ThermalThread (extend SchThread)
  (Attr position temperature energy))
```

### With langevin-dynamics
```python
from langevin_dynamics import LangevinSDE, solve_langevin
from hythermal import relational_energy, relational_gradient

sde = LangevinSDE(
    loss_fn=lambda C: relational_energy(acset, C),
    gradient_fn=lambda C: relational_gradient(acset, C),
    temperature=0.01,
    base_seed=0xDEADBEEF
)

solution = solve_langevin(sde, initial_positions, time_span=(0, 10))
```

### With gay-mcp
```python
from gay_mcp import GayIndexedRNG

rng = GayIndexedRNG(base_seed=0x1069)

for step in range(n_steps):
    color = rng.color_at(step)
    noise = rng.randn_from_color(color)
    # Thermal noise is now auditable via color
```

## Configuration

```yaml
# hythermal.yaml
thermal:
  default_temperature: 0.01
  dt: 0.01
  n_steps: 1000

equilibration:
  verify_gibbs: true
  kl_threshold: 0.01

embedding:
  dim: 64
  method: spectral  # or random, pretrained

visualization:
  plot_trajectory: true
  animate_dynamics: false

gf3:
  seed: 0x1069
  verify_conservation: true
```

## DuckDB Schema Extension

```sql
-- Extend thread schema with thermal columns
ALTER TABLE concepts ADD COLUMN position FLOAT[];
ALTER TABLE concepts ADD COLUMN energy FLOAT;
ALTER TABLE threads ADD COLUMN temperature FLOAT DEFAULT 0.01;

-- Thermal trajectory table
CREATE TABLE thermal_trajectory (
    step INT,
    concept_id VARCHAR,
    position FLOAT[],
    energy FLOAT,
    color_hex VARCHAR,
    trit INT
);

-- View: Equilibrium state
CREATE VIEW thermal_equilibrium AS
SELECT
    c.name,
    c.position,
    c.energy,
    c.hub_score,
    CASE WHEN c.energy < -1.0 THEN 'stable' ELSE 'metastable' END as state
FROM concepts c
WHERE EXISTS (
    SELECT 1 FROM thermal_trajectory t
    WHERE t.concept_id = c.concept_id
    AND t.step = (SELECT MAX(step) FROM thermal_trajectory)
);
```

## Example Workflow

```bash
# 1. Load threads into thermal ACSet
just hythermal-load threads.jsonl

# 2. Initialize concept positions
just hythermal-embed --method spectral --dim 64

# 3. Run thermal dynamics
just hythermal-run --temp 0.01 --steps 1000 --seed 0x1069

# 4. Verify equilibrium
just hythermal-verify-gibbs

# 5. Generate thermal S-expression
just hythermal-sexp > thermal-analysis.sexp

# 6. Temperature sweep study
just hythermal-sweep --temps 0.001,0.01,0.1,1.0
```

## Philosophical Frame

> *"what would it mean to become the Fokker-Planck equation—identity as probability flow?"*
> — bmorphism

HyThermal extends this question to relational structures: **What does it mean for a concept network to become its equilibrium distribution?**

At low temperature, concepts crystallize into tight semantic clusters. At high temperature, they diffuse and mix. The "identity" of a thread is not a fixed point but a probability distribution over concept configurations — shaped by relational energy and thermal noise.

## Related Skills

- `hyjax-relational` - ACSet thread analysis
- `langevin-dynamics` - SDE solver
- `fokker-planck-analyzer` - Equilibrium validation
- `entropy-sequencer` - Sequence optimization
- `gay-mcp` - Deterministic coloring

---

**Skill Name**: hythermal
**Type**: Analysis + Dynamics
**Trit**: 0 (ERGODIC)
**Key Property**: Bridges static relational structure with dynamic thermal exploration
**Status**: New

## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Autodiff + Scientific Computing
- **jax** [O] via bicomodule (thermal gradient computation)
- **scipy** [O] via bicomodule (SDE integration)

### Bibliography References

- `dynamical-systems`: 41 citations in bib.duckdb
- `category-theory`: 139 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
hythermal (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch2: Domain-Specific Languages
- Ch1: Flexibility through Abstraction

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