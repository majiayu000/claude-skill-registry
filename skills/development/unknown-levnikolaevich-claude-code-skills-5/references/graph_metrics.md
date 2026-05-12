# Graph Metrics & Thresholds

<!-- SCOPE: Robert C. Martin coupling metrics, Lakos aggregate metrics, SDP validation, thresholds. -->
<!-- Sources: Clean Architecture Ch14, dependency-cruiser metrics, "Large-Scale C++ Software Design" by John Lakos -->

## Per-Module Metrics (Robert C. Martin)

| Metric | Formula | Range | Description |
|--------|---------|-------|-------------|
| **Ca** (Afferent coupling) | count of incoming deps | 0..N | How many modules depend on this one |
| **Ce** (Efferent coupling) | count of outgoing deps | 0..N | How many modules this one depends on |
| **I** (Instability) | Ce / (Ca + Ce) | 0..1 | 0 = maximally stable, 1 = maximally unstable |

**Edge case:** If Ca + Ce = 0 (isolated module), I = 0.

**Interpretation:**
- I = 0: Module has only incoming dependencies (stable, hard to change, many dependents)
- I = 1: Module has only outgoing dependencies (unstable, easy to change, no dependents)
- "Not all components should be stable" — a system needs both stable and unstable modules

## Stable Dependencies Principle (SDP)

Per Clean Architecture Ch14: "Depend in the direction of stability."

```
FOR EACH edge (A -> B) IN graph:
  IF I(A) < I(B):
    # A is MORE stable than B, but A depends on LESS stable B
    # This means changes to B (easy to change) force changes to A (hard to change)
    violation: "SDP: {A} (I={I_A}) depends on less stable {B} (I={I_B})"
    severity: HIGH
    fix: "Apply DIP: extract interface in {A}, implement in {B}"
```

## Thresholds per Layer Type

Thresholds depend on the module's role in the architecture. Domain modules SHOULD be stable; infrastructure modules CAN be unstable.

| Layer | Expected I | Max Ce | Exceeds threshold |
|-------|-----------|--------|-------------------|
| domain / core | 0.0 - 0.3 | 3 | HIGH if I > 0.5 |
| application / service | 0.3 - 0.6 | 8 | MEDIUM if I > 0.7 |
| infrastructure / api | 0.5 - 1.0 | 15 | LOW if Ce > 20 |
| shared / common | 0.0 - 0.2 | 5 | HIGH if I > 0.3 |
| features (vertical) | 0.3 - 0.7 | 10 | MEDIUM if Ce > 15 |

**When layer is unknown** (custom architecture, no preset matched):
- Use universal thresholds: MEDIUM if I > 0.8, HIGH if Ce > 15
- Skip layer-specific SDP checks

## Aggregate Metrics (John Lakos)

### CCD (Cumulative Component Dependency)

```
FOR EACH module M IN graph:
  DependsOn(M) = count of all modules transitively reachable from M, including M itself

CCD = sum(DependsOn(M) for M in graph)
```

**Interpretation:** Total coupling burden of the system. Higher CCD = more impact from changes.

### NCCD (Normalized CCD)

```
N = number of modules
CCD_balanced = N * log2(N)  # CCD of a balanced binary tree with N nodes
NCCD = CCD / CCD_balanced
```

| NCCD | Interpretation | Finding |
|------|---------------|---------|
| < 1.0 | Better than balanced tree | No issue |
| 1.0 - 1.5 | Comparable to balanced tree | No issue |
| 1.5 - 2.0 | Moderately coupled | MEDIUM: "Graph complexity exceeds balanced tree threshold" |
| > 2.0 | Highly coupled (likely has cycles) | HIGH: "Graph highly coupled, likely contains cycles" |

## Deferred to v2

Require AST/bytecode analysis (cannot reliably detect via grep):

| Metric | Formula | Why deferred |
|--------|---------|-------------|
| **A** (Abstractness) | abstract_classes / all_classes | Need to identify abstract classes/interfaces |
| **D** (Distance from Main Sequence) | \|A + I - 1\| | Depends on A metric |

---

**Version:** 1.0.0
**Last Updated:** 2026-02-11
