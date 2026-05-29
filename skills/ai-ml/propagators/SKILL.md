---
name: propagators
description: Sussman/Radul propagator networks for constraint propagation and bidirectional
version: 1.0.0
---

# Propagators Skill

> *"The Art of the Propagator" — Radul & Sussman, 2009*

## Core Concept

Propagators are autonomous machines that:
1. **Watch** cells for new information
2. **Compute** derived values
3. **Add** information to other cells
4. Repeat until **fixpoint**

```
  ┌──────┐         ┌──────┐
  │cell A│────────▶│cell B│
  └──────┘  prop   └──────┘
      │                │
      │    ┌──────┐    │
      └───▶│cell C│◀───┘
           └──────┘
```

**No control flow.** Information flows until nothing new can be derived.

## Why It's Strange

1. **Bidirectional** — constraints work both ways
2. **Monotonic** — cells only gain information, never lose it
3. **Mergeable** — conflicting info produces refined info (or contradiction)
4. **Concurrent** — all propagators run "simultaneously"

## Cell Lattice

Cells hold values from a **join-semilattice**:

```
        ⊤ (contradiction)
       /|\
      / | \
     /  |  \
   3.14  e  √2
     \  |  /
      \ | /
       \|/
        ⊥ (nothing)
```

- ⊥ = "I know nothing"
- Value = "I know this specific thing"
- ⊤ = "Contradiction! Conflicting claims"

## Basic Operations

```scheme
;; Create cells
(define-cell a)
(define-cell b)
(define-cell c)

;; Add propagator: c = a + b
(p:+ a b c)

;; Set values (can be in any order!)
(add-content a 3)
(add-content b 4)

;; c automatically becomes 7
(content c)  ; → 7

;; BIDIRECTIONAL: set c, derive a!
(add-content c 10)
(add-content b 4)
(content a)  ; → 6 (inferred!)
```

## Partial Information

```scheme
;; Intervals
(define-cell x)
(add-content x (make-interval 0 10))   ; x ∈ [0, 10]
(add-content x (make-interval 5 15))   ; x ∈ [5, 10] (intersection!)

;; Symbolic
(add-content x 'positive)
(add-content x 7)  ; Consistent: 7 is positive

;; Contradiction
(add-content x 'negative)  ; → ⊤ (7 is not negative!)
```

## Implementation

### Minimal Propagator in Python

```python
class Cell:
    def __init__(self):
        self.content = Nothing()
        self.neighbors = []  # Propagators to notify
    
    def add_content(self, value):
        merged = merge(self.content, value)
        if merged != self.content:
            self.content = merged
            self.alert_propagators()
    
    def alert_propagators(self):
        for prop in self.neighbors:
            schedule(prop)

class Propagator:
    def __init__(self, inputs, output, func):
        self.inputs = inputs
        self.output = output
        self.func = func
        for cell in inputs:
            cell.neighbors.append(self)
    
    def run(self):
        values = [c.content for c in self.inputs]
        if all(v.is_known() for v in values):
            result = self.func(*[v.value for v in values])
            self.output.add_content(result)

# Adder propagator (a + b = c, bidirectional)
def make_adder(a, b, c):
    Propagator([a, b], c, lambda x, y: x + y)
    Propagator([a, c], b, lambda x, z: z - x)
    Propagator([b, c], a, lambda y, z: z - y)
```

### Scoped Propagators (Gay.jl)

```julia
# From your codebase: scoped_propagators.jl
abstract type ScopedPropagator end

struct ConeUp <: ScopedPropagator      # ↑ Bottom-up (colimit)
    cells::Vector{Cell}
end

struct DescentDown <: ScopedPropagator  # ↓ Top-down (limit)
    cells::Vector{Cell}
end

struct AdhesionHoriz <: ScopedPropagator  # ↔ Beck-Chevalley
    left::Vector{Cell}
    right::Vector{Cell}
end
```

## Dependency-Directed Backtracking

When contradiction (⊤) is reached:

```scheme
(define-cell x)
(define-cell y)

;; Track provenance
(add-content x (supported 5 '(assumption-1)))
(add-content y (supported 7 '(assumption-2)))

;; Contradiction!
(add-content x (supported 10 '(assumption-3)))

;; System identifies: assumption-1 OR assumption-3 must go
;; Backtrack to consistent state
```

## Applications

| Domain | Use Case |
|--------|----------|
| **CAD** | Constraint-based modeling |
| **Physics** | Unit conversion, equations |
| **Type inference** | Bidirectional typing |
| **Planning** | Constraint satisfaction |
| **Pricing** | Epistemic arbitrage |

## Relationship to Other Models

| Model | Propagators |
|-------|-------------|
| Dataflow | Similar but propagators are bidirectional |
| Constraint Logic | Propagators = constraint propagation |
| Reactive | Similar but propagators reach fixpoint |
| SAT/SMT | Unit propagation is a propagator |

## Literature

1. **Radul & Sussman (2009)** - "The Art of the Propagator"
2. **Steele (1980)** - "The Definition and Implementation of Constraint Languages"
3. **Apt (1999)** - "The Essence of Constraint Propagation"

---

## Neighbor Awareness (Co-Occurrence Patterns)

### Basin Affinity

From `interaction_entropy.duckdb` skill co-occurrence analysis:

```yaml
skill: propagators
basin: NEUTRAL
avg_basin_energy: 1.0
interleave_role: generator (+1)
```

### Co-Occurring Skills (Constraint Partners)

Skills frequently invoked together in propagator networks:

| Skill | Role | Trit | Affinity Pattern |
|-------|------|------|------------------|
| **gay-mcp** | Generator | +1 | Color cells by value |
| **duckdb-temporal-versioning** | Generator | +1 | Store cell states |
| **datalog-fixpoint** | Coordinator | 0 | Fixpoint iteration |
| **specter-acset** | Coordinator | 0 | Navigate cell networks |
| **unworld** | Coordinator | 0 | Seed-derived constraints |
| **sheaf-cohomology** | Validator | -1 | Verify cell consistency |
| **three-match** | Validator | -1 | GF(3) conservation |

### GF(3) Triad Partners

Natural skill groupings that satisfy GF(3) conservation (sum = 0):

```
propagators (+1) ⊗ datalog-fixpoint (0) ⊗ sheaf-cohomology (-1) = 0 ✓
propagators (+1) ⊗ specter-acset (0) ⊗ three-match (-1) = 0 ✓
propagators (+1) ⊗ unworld (0) ⊗ moebius-inversion (-1) = 0 ✓
propagators (+1) ⊗ acsets (0) ⊗ temporal-coalgebra (-1) = 0 ✓
```

### Basin Transition Flows

Energy flow patterns in constraint propagation:

```
NEUTRAL → NEUTRAL:  LATERAL ↔  energy_delta =  0.000  (propagating)
NEUTRAL → PLUS:     RISE ↑     energy_delta = +0.382  (information gain)
NEUTRAL → MINUS:    DESCENT ↓  energy_delta = -0.382  (contradiction)
```

### Interleave Topology

Position in the constraint satisfaction pipeline:

```
Level 1: ⊕ generator  (propagators)                 NEUTRAL basin  [PROPAGATE]
Level 2: ○ coordinator (datalog-fixpoint)           NEUTRAL basin  [FIXPOINT]
Level 3: ○ coordinator (specter-acset)              NEUTRAL basin  [NAVIGATE]
Level 4: ⊖ validator   (sheaf-cohomology)           NEUTRAL basin  [VERIFY]
```

### Upstream Skills (Constraint Producers)

Skills that produce constraints for propagation:

| Skill | Constraint Type | Propagation Pattern |
|-------|-----------------|---------------------|
| **acsets** | ACSet schema | Cell per part, morphism propagators |
| **datalog-fixpoint** | Derived relations | Rule → propagator |
| **gay-mcp** | Color constraints | Trit conservation |
| **unworld** | Seed-derived | Chain constraints |

### Downstream Skills (Fixpoint Consumers)

Skills that consume propagator fixpoints:

| Skill | Usage Pattern | Output |
|-------|---------------|--------|
| **sheaf-cohomology** | Verify consistency | H¹ = 0 check |
| **three-match** | Verify GF(3) | Conservation proof |
| **specter-acset** | Navigate result | Selected values |
| **duckdb-temporal-versioning** | Store fixpoint | Persistent state |

### Skill Invocation Chains

Common multi-skill sequences observed:

```clojure
;; Constraint satisfaction pipeline
(-> (acsets :define-schema)
    (propagators :build-network)
    (datalog-fixpoint :run-to-fixpoint)
    (sheaf-cohomology :verify-consistency))

;; Bidirectional type inference
(-> (propagators :type-cells)
    (specter-acset :navigate-types)
    (three-match :verify-gf3))

;; Epistemic arbitrage
(-> (propagators :scoped-network)
    (gay-mcp :color-by-confidence)
    (duckdb-temporal-versioning :store-arbitrage))

;; Triadic cell network
(-> (gay-mcp :tripartite-seeds)
    (propagators :triadic-cells)
    (three-match :verify-balance))
```

### MCP Tool Coordination

When invoked via MCP, coordinates with:

```yaml
mcp_neighbors:
  - tool: acset_colim
    relation: "cell structure from ACSets"
    direction: upstream
  - tool: datalog_query
    relation: "rule-based propagators"
    direction: upstream
  - tool: sheaf_verify
    relation: "verify cell consistency"
    direction: downstream
  - tool: gay_mcp
    relation: "color cells by value"
    direction: downstream
  - tool: duckdb_query
    relation: "store fixpoint states"
    direction: downstream
```

### Propagator Network Example

```python
# Full pipeline with neighbor coordination
def propagate_with_neighbors(constraints, initial_values):
    # Build propagator network
    cells = {}
    propagators = []

    for var in constraints.variables:
        cells[var] = Cell()

    for constraint in constraints.all:
        prop = build_propagator(constraint, cells)
        propagators.append(prop)

    # Set initial values (from upstream)
    for var, value in initial_values.items():
        cells[var].add_content(value)

    # Run to fixpoint (like datalog-fixpoint)
    while schedule.has_work():
        prop = schedule.pop()
        prop.run()

    # Verify via sheaf-cohomology (downstream)
    for cell_name, cell in cells.items():
        if cell.content == CONTRADICTION:
            # Dependency-directed backtracking
            deps = cell.get_dependencies()
            sheaf_cohomology.report_obstruction(cell_name, deps)

    # Color cells via gay-mcp (downstream)
    for i, (name, cell) in enumerate(cells.items()):
        cell.color = gay_mcp.color_at(seed, i)

    # Store via duckdb (downstream)
    duckdb_insert(db, "propagator_fixpoints", (
        num_cells=len(cells),
        num_propagators=len(propagators),
        reached_fixpoint=True,
        timestamp=now()
    ))

    return cells
```

---

**Skill Name**: propagators
**Type**: Constraint Propagation Generator
**Trit**: +1 (PLUS - Generator)
**GF(3)**: Forms valid triads with coordinators (0) and validators (-1)
**Applications**: Bidirectional constraints, type inference, epistemic arbitrage, CAD modeling

---

## End-of-Skill Interface

## GF(3) Integration

```julia
# Triadic propagator network
struct TriadicCell
    trit::Int  # -1, 0, +1
    value::Any
    neighbors::Vector{Propagator}
end

# Conservation: sum of connected cells = 0 (mod 3)
function verify_gf3(cells::Vector{TriadicCell})
    sum(c.trit for c in cells) % 3 == 0
end
```

## r2con Speaker Resources

| Speaker | Relevance | Repository/Talk |
|---------|-----------|-----------------|
| **alkalinesec** | ESILSolve constraint propagation | [esilsolve](https://github.com/aemmitt-ns/esilsolve) |
| **condret** | ESIL symbolic cells | [radare2 ESIL](https://github.com/radareorg/radare2) |
| **Pelissier_S** | Symbolic execution | r2con 2020 talk |

## Related Skills

- `epistemic-arbitrage` - Uses scoped propagators
- `constraint-logic` - Logical foundation
- `dataflow` - One-way version
- `interaction-nets` - Another "no control" model

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
propagators (+) + SDF.Ch3 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch7: Propagators
- Ch5: Evaluation
- Ch4: Pattern Matching
- Ch6: Layering
- Ch10: Adventure Game Example
- Ch2: Domain-Specific Languages
- Ch1: Flexibility through Abstraction

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
