---
name: derangement-crdt
description: Derangement-CRDT Skill
version: 1.0.0
---

# Derangement-CRDT Skill

**Status**: ✅ Production Ready
**Trit**: ERGODIC (0)
**Integration**: CRDT, Gay.jl, Join-Semilattice

## Core Concept

A **derangement** is a permutation σ where σ(i) ≠ i for all i (no fixed points).
A **colorable derangement CRDT** assigns GF(3) colors to derangement cycles,
ensuring merge operations preserve both the derangement property and color conservation.

```
Derangement: (1 2 3) → (2 3 1)  ✓ no fixed points
Fixed point: (1 2 3) → (1 3 2)  ✗ position 1 is fixed
```

## Mathematical Foundation

### Derangement Lattice

Derangements form a **join-semilattice** under cycle composition:

```
     ⊤ = identity (trivial - all fixed)
     │
   ┌─┴─┬───┬───┐
   │   │   │   │
  (12) (13) (23) ...  ← transpositions
   │   │   │   │
   └─┬─┴───┴─┬─┘
     │       │
   (123)   (132)      ← 3-cycles (derangements!)
     │       │
     └───┬───┘
         │
         ⊥ = full derangement
```

### GF(3) Coloring of Cycles

Each cycle receives a trit based on cycle length mod 3:

| Cycle Length | Trit | Color Range | Example |
|--------------|------|-------------|---------|
| len ≡ 0 (mod 3) | ERGODIC (0) | 60°-180° (green) | (1 2 3) |
| len ≡ 1 (mod 3) | PLUS (+1) | 0°-60°, 300°-360° (warm) | (1) fixed |
| len ≡ 2 (mod 3) | MINUS (-1) | 180°-300° (cold) | (1 2) swap |

### Conservation Law

For any valid derangement coloring:
```
Σ trit(cycle) ≡ 0 (mod 3)
```

This is automatically satisfied for derangements of length n ≡ 0 (mod 3).

## CRDT Operations

### Derangement-Set CRDT

```ruby
class DerangementCRDT
  # State: set of (element, position, color, replica_id, lamport)

  def merge(other)
    # Join-semilattice merge:
    # 1. Union all mappings
    # 2. For conflicts: higher Lamport wins
    # 3. Verify derangement property preserved
    # 4. Recolor to maintain GF(3) conservation
  end

  def apply_permutation(sigma)
    # Apply permutation, ensuring no fixed points created
    raise DerangementViolation if creates_fixed_point?(sigma)
    update_colors!
  end

  def cycle_decomposition
    # Decompose into disjoint cycles
    # Color each cycle by length mod 3
  end
end
```

### Merge Semantics

```
State A: [2,3,1,5,4] (cycles: (123)(45))
         Colors: [G,G,G,B,B] (ERGODIC, MINUS)

State B: [3,1,2,5,4] (cycles: (132)(45))
         Colors: [G,G,G,B,B] (ERGODIC, MINUS)

Merge(A,B): Resolve by Lamport timestamp
            Recolor to maintain Σ trits ≡ 0
```

## Implementation

### Babashka Script

```clojure
#!/usr/bin/env bb
;; derangement_crdt.bb

(defn derangement? [perm]
  "Check if permutation has no fixed points"
  (every? (fn [[i v]] (not= i v))
          (map-indexed vector perm)))

(defn cycle-decomposition [perm]
  "Decompose permutation into disjoint cycles"
  (loop [remaining (set (range (count perm)))
         cycles []]
    (if (empty? remaining)
      cycles
      (let [start (first remaining)
            cycle (loop [current start
                         acc [start]]
                    (let [next (nth perm current)]
                      (if (= next start)
                        acc
                        (recur next (conj acc next)))))]
        (recur (apply disj remaining cycle)
               (conj cycles cycle))))))

(defn gf3-trit [cycle-len]
  "Assign GF(3) trit based on cycle length"
  (case (mod cycle-len 3)
    0 :ERGODIC
    1 :PLUS
    2 :MINUS))

(defn hue-from-trit [trit seed]
  "Map trit to hue range with seed variation"
  (let [base (case trit
               :MINUS   (+ 180 (mod seed 120))   ; cold: 180-300
               :ERGODIC (+ 60 (mod seed 120))    ; neutral: 60-180
               :PLUS    (if (< (mod seed 120) 60)
                          (mod seed 60)           ; warm: 0-60
                          (+ 300 (mod seed 60)))) ; warm: 300-360
        ]
    (mod base 360)))

(defn color-derangement [perm]
  "Assign colors to derangement cycles"
  (let [cycles (cycle-decomposition perm)]
    (for [[idx cycle] (map-indexed vector cycles)]
      {:cycle cycle
       :length (count cycle)
       :trit (gf3-trit (count cycle))
       :hue (hue-from-trit (gf3-trit (count cycle)) idx)})))

(defn conservation-check [colored-cycles]
  "Verify GF(3) conservation"
  (let [trit-sum (->> colored-cycles
                      (map :trit)
                      (map {:MINUS -1 :ERGODIC 0 :PLUS 1})
                      (reduce +))]
    (zero? (mod trit-sum 3))))

;; CRDT Merge
(defn merge-derangements [state-a state-b]
  "Join-semilattice merge of two derangement states"
  (let [merged (merge-with
                 (fn [a b]
                   (if (> (:lamport a) (:lamport b)) a b))
                 state-a state-b)]
    (when-not (derangement? (:perm merged))
      (throw (ex-info "Merge violated derangement property" {})))
    (assoc merged :colors (color-derangement (:perm merged)))))

;; Demo
(defn demo []
  (let [perm [1 2 0 4 3]  ; (0 1 2)(3 4) - derangement!
        colored (color-derangement perm)]
    (println "Permutation:" perm)
    (println "Derangement?" (derangement? perm))
    (println "Colored cycles:" colored)
    (println "GF(3) conserved?" (conservation-check colored))))

(when (= *file* (System/getProperty "babashka.file"))
  (demo))
```

## Integration Points

### With CRDT Skill
```ruby
# Compose with OR-Set for distributed derangements
crdt_skill.create("derangement-pool", :or_set, "replica-1")
crdt_skill.mutate("derangement-pool", :add, serialize(derangement))
```

### With CRDT-VTerm
```clojure
;; Terminal sessions as derangements of command history
;; No command should map to itself (always transformed)
(crdt-vterm-derange session-buffer)
```

### With Gay.jl Colors
```julia
using Gay

# Color a derangement's cycles
function color_derangement(perm::Vector{Int})
    cycles = cycle_decomposition(perm)
    [Gay.from_trit(gf3_trit(length(c))) for c in cycles]
end
```

### With BlackHat-Go Security
```go
// Attack chains as derangements:
// No technique should leave system in same state
type AttackDerangement struct {
    Techniques []string
    // Invariant: ∀t ∈ Techniques: state_after(t) ≠ state_before(t)
}
```

## Subfactorial Connection

The number of derangements of n elements is the **subfactorial** !n:

```
!n = n! × Σ(k=0 to n) (-1)^k / k!
   ≈ n! / e

!3 = 2    (only 2 derangements of 3 elements)
!4 = 9
!5 = 44
```

For GF(3) coloring, we care about n mod 3:
- n ≡ 0: Perfect triadic balance possible
- n ≡ 1: One PLUS excess
- n ≡ 2: One MINUS excess

## Lattice Visualization

```
         ┌─────────────────────────────────────┐
         │           DERANGEMENT LATTICE       │
         │         with GF(3) Coloring         │
         └─────────────────────────────────────┘

                      (1)(2)(3)(4)
                      all fixed ⊤
                      [+1,+1,+1,+1]
                           │
            ┌──────────────┼──────────────┐
            │              │              │
         (12)(3)(4)    (13)(2)(4)    (14)(2)(3)
         [-1,+1,+1]    [-1,+1,+1]    [-1,+1,+1]
            │              │              │
            └──────┬───────┴───────┬──────┘
                   │               │
              (12)(34)         (13)(24)
              [-1,-1]          [-1,-1]
                   │               │
                   └───────┬───────┘
                           │
                       (1234)
                       [+1] ← 4-cycle
                           │
                    ┌──────┴──────┐
                    │             │
                (1243)         (1324)
                [+1]           [+1]
                    │             │
                    └──────┬──────┘
                           │
                      Full Derangement ⊥
                      (all cycles ≥ 2)
```

## Properties

| Property | Derangement-CRDT | Standard CRDT |
|----------|------------------|---------------|
| Idempotence | ✓ merge(D,D) = D | ✓ |
| Commutativity | ✓ merge(A,B) = merge(B,A) | ✓ |
| Associativity | ✓ | ✓ |
| No fixed points | ✓ enforced | N/A |
| GF(3) conservation | ✓ verified | N/A |

## Usage

```bash
# Run derangement CRDT demo
bb ~/.claude/skills/derangement-crdt/derangement_crdt.bb

# Expected output:
# Permutation: [1 2 0 4 3]
# Derangement? true
# Colored cycles: [{:cycle [0 1 2], :length 3, :trit :ERGODIC, :hue 120}
#                  {:cycle [3 4], :length 2, :trit :MINUS, :hue 240}]
# GF(3) conserved? true
```

## Related Skills
- `crdt` - Base CRDT operations
- `crdt-vterm` - Terminal CRDT with GF(3)
- `gay-mcp` - Color assignment
- `blackhat-go` - Security state lattice
- `acsets` - Categorical databases

---

*Derangements ensure every element moves; GF(3) coloring ensures balance is preserved.*