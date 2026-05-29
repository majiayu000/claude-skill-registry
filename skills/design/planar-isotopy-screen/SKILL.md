---
name: planar-isotopy-screen
description: Planar Isotopy Screen Mapping
version: 1.0.0
---

# Planar Isotopy Screen Mapping

Maps thread states and observations to screen positions using planar isotopy principles.

## Trit Value
**0 (ERGODIC)** - Coordinate between spatial regions

## Purpose
Transform abstract thread relationships into concrete screen positions while preserving topological invariants:
- **Adjacency**: Neighboring trits occupy adjacent screen regions
- **Handedness**: MINUS→left, ERGODIC→center, PLUS→right
- **Conservation**: Screen area sum is invariant under isotopy

## Screen Region Mapping

```
┌─────────────────┬─────────────────┬─────────────────┐
│                 │                 │                 │
│     MINUS       │    ERGODIC      │     PLUS        │
│    (left)       │    (center)     │    (right)      │
│                 │                 │                 │
│  Cold hues      │  Neutral hues   │  Warm hues      │
│  180-300°       │  60-180°        │  0-60°,300-360° │
│                 │                 │                 │
│  Validator      │  Coordinator    │  Generator      │
│                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

## Position Computation

```clojure
(defn seed->screen-position [seed trit screen-width screen-height]
  "Map seed deterministically to (x, y) within trit's region.

   Uses SplitMix64 decomposition:
   - High bits → x offset
   - Low bits → y offset"
  (let [region (trit->region trit screen-width)
        [rand1 seed'] (splitmix64 seed)
        [rand2 _] (splitmix64 seed')
        x (+ (:x region) (* (:width region) (/ rand1 MASK64)))
        y (* screen-height (/ rand2 MASK64))]
    {:x x :y y :region trit}))
```

## Observation Lines

When thread A observes thread B, draw a line between their screen positions:

```clojure
(defn observation-line [observer observed]
  {:from (seed->screen-position (:seed observer) (:trit observer))
   :to (seed->screen-position (:seed observed) (:trit observed))
   :gf3-sum (mod (+ (:trit observer) (:trit observed)) 3)})
```

## Planar Isotopy Invariants

1. **No crossings for conserved observations**: Lines between threads with GF(3) sum = 0 should not cross
2. **Triadic bundling**: Triad members form non-crossing triangles
3. **Seed progression**: Moving a thread moves its position deterministically

## Integration with Mutual Thread Observation

```python
from mutual_thread_observation import MutualThreadObservationSystem

system = MutualThreadObservationSystem()
# ... register threads ...

# Get screen positions
for tid, state in system.thread_states.items():
    pos = seed_to_screen_position(state.seed, state.trit)
    print(f"{tid}: ({pos['x']:.0f}, {pos['y']:.0f}) in {pos['region_label']}")
```

## macOS Integration

Use with macos-use MCP for actual screen interaction:

```bash
# Get element at thread's screen position
bb -e '(require \'[mutual-thread-demo :as mtd])
       (let [pos (mtd/seed->screen-position seed trit)]
         (println (:x pos) (:y pos)))'
```

Then use `mcp__macos-use__macos-use_click_and_traverse` at those coordinates.

## Related Skills
- `mutual-thread-observation` - Core observation system
- `gay-mcp` - Deterministic color from seed
- `acsets-algebraic-databases` - Schema modeling
- `bisimulation-game` - Observational equivalence

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
planar-isotopy-screen (○) + SDF.Ch3 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch10: Adventure Game Example

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
