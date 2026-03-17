---
name: pijul-sparse-skills
description: Sparsity-preserving skill versioning via Pijul patches with GF(3) projection gates
version: 1.0.0
trit: 0
role: ERGODIC
color: "#D2E98B"
requires:
  - pijul
  - flox-mcp
  - structured-decomp
---

# pijul-sparse-skills

Sparsity-preserving skill versioning where changes are stored as morphisms, not materialized states.

**Trit**: 0 (ERGODIC) - Coordinator role for projection gate decisions

---

## Philosophy

### Default: SPARSE Mode

```
┌─────────────────────────────────────────────────────────┐
│  SPARSE (default)                                       │
│  - Changes stored as patches (morphisms)                │
│  - No materialization unless required                   │
│  - Lazy evaluation of skill state                       │
│  - Minimal storage footprint                            │
└─────────────────────────────────────────────────────────┘
```

### Projection Only When:

| Trigger | Description | GF(3) |
|---------|-------------|-------|
| `--materialize` | Explicit flag | Any |
| `trit == 0` | ERGODIC coordination point | 0 |
| `--archive` | Explicit archive | Any |
| Conflict | Resolution requires full state | Any |

---

## Categorical Foundation

### Patches as Morphisms in Cat(Skills)

```
Ob(C) = { skill states }
Mor(C) = { patches transforming states }

For patches p, q:
  p ⊥ q (independent) ⟹ p;q = q;p (commute)
```

### Sparsity via Lazy Evaluation

```julia
# Sparse representation (default)
struct SparseSkill
    base_hash::UInt64      # Root state reference
    patches::Vector{Patch}  # Morphism chain, not applied
end

# Materialized only on demand
function materialize(s::SparseSkill)
    foldl(apply, s.patches; init=load(s.base_hash))
end
```

---

## GF(3) Projection Gates

### Gate Logic

```julia
function should_project(skill::Skill, flags::Flags)::Bool
    # Explicit materialization requested
    flags.materialize && return true
    
    # ERGODIC trit forces coordination checkpoint
    skill.trit == 0 && return true
    
    # Explicit archive
    flags.archive && return true
    
    # Conflict requires full state
    has_conflicts(skill) && return true
    
    # Otherwise: stay sparse
    return false
end
```

### Trit-Based Behavior

```
trit = -1 (MINUS/Validator):
  → Verify patch integrity without materializing
  → Check commutativity conditions
  → Validate GF(3) conservation
  
trit = 0 (ERGODIC/Coordinator):
  → PROJECT: Create materialized checkpoint
  → Coordinate merge points
  → Synchronize distributed states
  
trit = +1 (PLUS/Generator):
  → Generate new patches
  → Create without materializing target
  → Lazy forward references
```

---

## Workflow Examples

### Record Skill Change (Sparse)

```bash
cd .agents/skills/my-skill

# Edit SKILL.md
echo "new content" >> SKILL.md

# Record as patch (NOT materialized)
pijul record -m "Add GF(3) section"
# Stores: Patch{add_lines: [...], hash: 0x...}
```

### Sync Skills (Sparse Pull)

```bash
# Pull only patch metadata
pijul pull --partial origin

# View pending patches without applying
pijul log --pending

# Apply lazily (on access)
cat SKILL.md  # Materializes only this file
```

### Force Materialization (ERGODIC Gate)

```bash
# Explicit checkpoint
pijul reset --materialize

# Or via trit-aware tool
skill-checkpoint my-skill --trit 0
```

---

## Integration Patterns

### With flox-mcp

```clojure
;; Install pijul via flox MCP
(flox-install "pijul")

;; Record skill change
(shell "pijul" "record" "-m" (str "Update " skill-name))

;; Sparse pull from upstream
(shell "pijul" "pull" "--partial" upstream-url)
```

### With structured-decomp

```julia
# Tree decomposition of skill graph
tree = decompose(skill_graph)

# Each bag gets sparse representation
for bag in tree.bags
    bag.skills = map(to_sparse, bag.skills)
end

# Sheaf gluing respects sparsity
glue!(tree)  # Only materializes at boundaries
```

### With Gay.jl Colors

```julia
using Gay

# Patch hash → color for visual diff
function patch_color(patch::Patch)
    seed = reinterpret(UInt64, patch.hash)
    Gay.color_at(seed, 1)
end

# GF(3) conservation across patch chain
function verify_chain(patches::Vector{Patch})
    trits = [patch.trit for patch in patches]
    sum(trits) % 3 == 0
end
```

---

## Delta-State CRDT Bridge

### Patches as Delta-States

```
Pijul Patch ≅ Delta-CRDT Update

Both:
  - Commutative when independent
  - Compose via join semilattice
  - Support partial replication
```

### Merkle Search Tree Index

```
skills/
├── .pijul/
│   ├── patches/       # Merkle tree of patches
│   ├── sparse-index/  # Hash → patch mapping
│   └── projection-log # When/why materialized
```

---

## Commands

### Check Sparsity Status

```bash
pijul-sparse status
# Output:
#   my-skill: SPARSE (3 pending patches)
#   other-skill: MATERIALIZED (checkpoint 2024-01-07)
```

### Force Projection

```bash
pijul-sparse project my-skill --reason "coordination checkpoint"
```

### Verify Conservation

```bash
pijul-sparse verify-gf3
# Output:
#   Chain: patch_a(-1) + patch_b(0) + patch_c(+1) = 0 ✓
```

---

## References

- [pijul skill](../pijul/SKILL.md) - Core VCS operations
- [flox-mcp skill](../flox-mcp/SKILL.md) - Environment management
- [structured-decomp skill](../structured-decomp/SKILL.md) - Tree decompositions
- Mimram/Di Giusto: Categorical Patch Theory
- Almeida et al: Delta-State CRDTs
- Merkle Search Trees (Auvolat/Taïani)
- Irmin/MRDTs (Tarides)

---

## Triadic Composition

```
pijul-sparse-skills (0) + pijul (-1) + skill-creator (+1) = 0 ✓
     Coordinator          Validator      Generator
```

This skill coordinates the projection decision while `pijul` validates patches and `skill-creator` generates new content.

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
pijul-sparse-skills (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch5: Evaluation
- Ch6: Layering
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
