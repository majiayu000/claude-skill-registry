---
name: triadic-skill-orchestrator
description: Orchestrates multiple skills in GF(3)-balanced triplets. Assigns MINUS/ERGODIC/PLUS trits to skills ensuring conservation. Use for multi-skill workflows, parallel skill dispatch, or maintaining GF(3) invariants across skill compositions.
---

# Triadic Skill Orchestrator

Orchestrates skills in GF(3)-balanced triplets with deterministic trit assignment.

## Core Workflow

1. **Trit Assignment** — Assign skills to MINUS(-1)/ERGODIC(0)/PLUS(+1) based on seed
2. **GF(3) Conservation** — Verify Σ trits ≡ 0 (mod 3)
3. **Parallel Dispatch** — Fan out to 3 skills simultaneously
4. **Role Mapping** — VALIDATOR/COORDINATOR/GENERATOR per trit
5. **Color Integration** — gay-mcp provides deterministic coloring

## Trit Assignment Algorithm

```clojure
(defn assign-trits [skill-names seed]
  (let [groups (partition-all 3 skill-names)]
    (mapcat (fn [[s0 s1 s2]]
              (let [t0 (mod (sha256-int (str seed "::0::" s0)) 3)
                    t1 (mod (sha256-int (str seed "::1::" s1)) 3)
                    t2 (mod (- 0 t0 t1) 3)]  ; Force conservation
                [{:skill s0 :trit (- t0 1)}
                 {:skill s1 :trit (- t1 1)}
                 {:skill s2 :trit (- t2 1)}]))
            groups)))
```

## GF(3) Conservation Check

```clojure
(defn verify-gf3 [assignments]
  (let [sum (reduce + (map :trit assignments))]
    {:conserved (zero? (mod sum 3))
     :sum sum
     :mod3 (mod sum 3)}))
```

## Role Assignments

| Trit | Role | Function | Color Range |
|------|------|----------|-------------|
| -1 | VALIDATOR | Verify, constrain, check | Cold (180-300°) |
| 0 | COORDINATOR | Mediate, synthesize, balance | Neutral (60-180°) |
| +1 | GENERATOR | Create, execute, produce | Warm (0-60°, 300-360°) |

## Denotation

> **This skill coordinates triadic skill applications to ensure no trit imbalance exists, dispatching skills in GF(3)-balanced triplets with deterministic seed propagation.**

```
Effect: SkillSet → (Task × Seed) → [Result₋₁, Result₀, Result₊₁]
Invariant: ∀ dispatch: Σ(trit) ≡ 0 (mod 3)
Fixed Point: When skill outputs stabilize across reruns with different seeds
```

## Invariant Set

| Invariant | Definition | Verification |
|-----------|------------|--------------|
| `Conservation` | Σ(trit) ≡ 0 (mod 3) after every dispatch | Sum check on each triplet |
| `TritBalance` | Each skill receives exactly -1, 0, or +1 | Assignment validation |
| `SeedDeterminism` | Same seed → same trit assignment | Replay test |
| `RoleInjection` | Each role (VALIDATOR/COORDINATOR/GENERATOR) appears exactly once | Role counting |

## Narya Compatibility

| Field | Definition |
|-------|------------|
| `before` | Skill states before dispatch |
| `after` | Skill states after dispatch |
| `delta` | Trit assignments made |
| `birth` | Initial skill set with no assignments |
| `impact` | 1 if any skill changed equivalence class |

## Condensation Policy

**Trigger**: When a skill triplet produces identical outputs for 3 consecutive dispatches with different seeds.

**Action**: Mark triplet as saturated, collapse to canonical representative.

## Parallel Dispatch

```clojure
(defn dispatch-skill [skill-assignment task]
  (let [{:keys [skill trit]} skill-assignment
        role (case trit
               -1 "VALIDATOR"
               0  "COORDINATOR"
               1  "GENERATOR")]
    {:skill skill :trit trit :role role :task task}))
```

## Integration with gay-mcp

Each skill gets a deterministic color from its trit:

```python
from gay import SplitMixTernary

gen = SplitMixTernary(seed=0x42D)
for skill in skills:
    color = gen.color_at(skill.index)
    trit = color['trit']  # Maps to role
    hex_color = color['hex']  # Visual identifier
```

## Justfile Recipes

```just
# Orchestrate 3 skills for a task
triadic-orchestrate TASK SEED="0x42D":
  bb scripts/triadic_skill_orchestrator.bb run "{{TASK}}" {{SEED}} \
    finder-color-walk google-workspace gay-mcp

# Verify GF(3) conservation for skill triplet
triadic-verify *SKILLS:
  bb scripts/triadic_skill_orchestrator.bb verify {{SKILLS}}

# List available skills
triadic-list:
  bb scripts/triadic_skill_orchestrator.bb list

# Run orchestrator with custom skills
triadic-custom TASK SEED *SKILLS:
  bb scripts/triadic_skill_orchestrator.bb run "{{TASK}}" {{SEED}} {{SKILLS}}
```

## Example Output

```
╔═══════════════════════════════════════════════════════════════╗
║     TRIADIC SKILL ORCHESTRATOR                                ║
╚═══════════════════════════════════════════════════════════════╝

Task: Sync files with Drive
Seed: 0x42D
Skills: 3

Assignments:
  finder-color-walk: +1 (PLUS)
  google-workspace: -1 (MINUS)
  gay-mcp: 0 (ERGODIC)

GF(3) Conservation: ✓ OK (sum=0, mod3=0)

Dispatching...
[GENERATOR] finder-color-walk (trit=+1): Sync files with Drive
[VALIDATOR] google-workspace (trit=-1): Sync files with Drive
[COORDINATOR] gay-mcp (trit=0): Sync files with Drive
```

## Valid Triads

| Skill 1 (MINUS) | Skill 2 (ERGODIC) | Skill 3 (PLUS) |
|-----------------|-------------------|----------------|
| sheaf-cohomology | ordered-locale | gay-mcp |
| bisimulation-game | google-workspace | triad-interleave |
| say-narration | parallel-fanout | finder-color-walk |

## Reference Script

See [scripts/triadic_skill_orchestrator.bb](file:///Users/alice/agent-o-rama/agent-o-rama/scripts/triadic_skill_orchestrator.bb) for full implementation.

---

**Skill Name**: triadic-skill-orchestrator  
**Type**: Skill Composition / Parallel Dispatch  
**Trit**: 0 (ERGODIC - coordinator)  
**GF(3)**: Enforced via third-trit correction
