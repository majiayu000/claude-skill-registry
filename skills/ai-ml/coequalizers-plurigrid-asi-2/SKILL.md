---
name: coequalizers
description: Quotient redundant skill paths via coequalizers, preserving GF(3) conservation
version: 1.0.0
trit: 0
---

# Coequalizers Skill

> **Quotient redundant skill paths via categorical coequalizers**

**Version**: 1.0.0  
**Trit**: 0 (ERGODIC - coordinates equivalences)  
**Domain**: category-theory, skill-composition, colimits, behavioral-equivalence

---

## Overview

The **coequalizers** skill provides:

1. **Behavioral equivalence checking** via bisimulation (from temporal-coalgebra)
2. **Parallel morphism quotienting** via coequalizers (colimits)
3. **Skill overlap detection** and gluing (from oapply-colimit pushouts)
4. **GF(3) conservation** in quotient spaces
5. **MCP integration** for cross-agent skill synchronization

---

## Core Concept

### What Are Coequalizers?

A **coequalizer** is the colimit of two parallel morphisms:

```
    X ──f──→ Y
    │  g     │
    └────────→ q
             ↓
             Q  (coequalizer)

Universal property: q ∘ f = q ∘ g
```

**In Sets**: Q = Y / ~ where ~ is the smallest equivalence relation such that f(x) ~ g(x) for all x ∈ X.

**For skills**: If two skill paths produce behaviorally equivalent outputs, the coequalizer gives the canonical quotient.

---

## Key Patterns from asi Repository

### 1. oapply-colimit: Pushout = Coproduct + Coequalizer

From `/skills/oapply-colimit/SKILL.md`:

```julia
function oapply(d::UndirectedWiringDiagram, xs::Vector{ResourceSharer})
    # Step 1: Coproduct of state spaces
    S = coproduct((FinSet ∘ nstates).(xs))
    
    # Step 2: Pushout identifies shared variables via COEQUALIZER
    S′ = pushout(portmap, junctions)  # ← Uses coequalizer internally
    
    # Step 3: Induced dynamics sum at junctions
    return ResourceSharer(induced_interface, induced_dynamics)
end
```

**Key insight**: Pushouts decompose as coproduct + coequalizer. This is how skills with **shared interfaces** are glued together.

### 2. Bisimulation-game: Behavioral Equivalence

From `/skills/bisimulation-game/SKILL.md`:

```python
def bisimilar(skill₁, skill₂, input, depth=10):
    """
    Recursively check if skills produce same observations.
    
    Two skills are bisimilar if:
    - They produce same immediate output
    - Their continuations are pairwise bisimilar
    """
    obs₁ = observe(skill₁, input)
    obs₂ = observe(skill₂, input)
    
    if obs₁ != obs₂:
        return False
    
    # Recursive check on continuations
    if depth > 0:
        for (next₁, inp₁), (next₂, inp₂) in zip(
            skill₁.continuations(input),
            skill₂.continuations(input)
        ):
            if not bisimilar(next₁, next₂, inp₁, depth-1):
                return False
    
    return True
```

**Application**: Use bisimulation to establish equivalence relation ~ before applying coequalizer.

### 3. Adhesive Rewriting: Incremental Query Updating

From `/skills/topos-adhesive-rewriting/SKILL.md`:

```julia
# Decomposition: Q ≅ Q_G +_{Q_L} Q_R
# This IS a coequalizer construction!

function quotient_system(system::SkillSystem, equivalences)
    # Build parallel morphisms from equivalence pairs
    equiv_indices = parts(system, :Equivalence)
    
    # Compute coequalizer (built into Catlab)
    quotient = coequalizer(system, equiv_indices)
    
    # Verify GF(3) conservation
    @assert verify_gf3_conservation(quotient)
    
    return quotient
end
```

**Key**: Adhesive categories (like C-Sets) have well-behaved coequalizers for incremental updates.

### 4. Browser-history-acset: Path Equivalence

From `/skills/browser-history-acset/path_equivalence_test.jl`:

```julia
# Path composition via subpart chains
@assert subpart(acs, subpart(acs, 1, :url_of), :domain_of) == 1

# Multiple visit paths may lead to same outcome
# Coequalizer identifies equivalent paths
```

**Application**: Navigation paths through skill graphs that produce same results should be identified.

### 5. Sheaves on Ordered Locale: Directional Restrictions

From `/skills/ordered-locale/sheaves.py`:

```python
def gluing(cover: List[FrozenSet], family: Dict[FrozenSet, T]) -> Optional[T]:
    """
    Glue a compatible family over a cover.
    
    This is the sheaf condition - dual to coequalizer.
    """
    # Check compatibility on overlaps
    for U_i, U_j in pairs(cover):
        overlap = U_i & U_j
        if overlap:
            res_i = restrict(U_i, overlap, family[U_i])
            res_j = restrict(U_j, overlap, family[U_j])
            if res_i != res_j:
                return None  # Incompatible family
    
    # Glue: coequalizer of restrictions
    return reduce(lambda a, b: a | b, family.values(), frozenset())
```

**Key**: Sheaf gluing IS the dual of coequalizer. Overlapping skill contexts must agree.

### 6. IrreversibleMorphisms: Lossy Transformations

From `/skills/compositional-acset-comparison/IrreversibleMorphisms.jl`:

```julia
# Irreversible morphisms: information loss
const MORPHISM_CLASSIFICATION = Dict(
    :parent_manifest => :irreversible,     # Append-only chain
    :source_column => :irreversible,       # Lossy embedding
    # ...
)

# Coequalizers preserve irreversibility classification
# If f, g both irreversible, coeq(f,g) is irreversible
```

**Application**: Track information loss through quotients. GF(3) trit sum must be preserved.

---

## Implementation Strategy

### Schema: Skills with Equivalences

```julia
using Catlab.CategoricalAlgebra
using AlgebraicRewriting

@present SchSkillCoequalizer(FreeSchema) begin
    Skill::Ob
    Application::Ob
    Equivalence::Ob
    
    app_src::Hom(Application, Skill)
    app_tgt::Hom(Application, Skill)
    equiv_app1::Hom(Equivalence, Application)
    equiv_app2::Hom(Equivalence, Application)
    
    Trit::AttrType
    Behavior::AttrType
    
    skill_trit::Attr(Skill, Trit)
    app_behavior::Attr(Application, Behavior)
end

@acset_type SkillSystem(SchSkillCoequalizer,
    index=[:app_src, :app_tgt, :equiv_app1, :equiv_app2])
```

---

## GF(3) Integration

### Trit Assignment

- **Coequalizers** have trit = 0 (ERGODIC)
- They **coordinate** between validators (-1) and generators (+1)
- **Preserve** trit sums: if inputs sum to 0 mod 3, output preserves this

### Synergistic Triads

```
bisimulation-game (-1) ⊗ coequalizers (0) ⊗ oapply-colimit (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ coequalizers (0) ⊗ topos-adhesive (+1) = 0 ✓
browser-history-acset (-1) ⊗ coequalizers (0) ⊗ ordered-locale (sheaves) (+1) = 0 ✓
```

---

## Commands

```bash
just coequalizer-find SKILLS...          # Find equivalences among skills
just coequalizer-quotient SYSTEM         # Compute quotient
just coequalizer-verify GF3              # Verify GF(3) conservation
just coequalizer-disperse AGENTS...      # Sync across agents
just coequalizer-pushout SKILL1 SKILL2   # Compose with overlap
```

---

## References

### From asi Repository

- `oapply-colimit` - Pushout = coproduct + coequalizer
- `bisimulation-game` - Behavioral equivalence testing
- `topos-adhesive-rewriting` - Incremental query updating via coequalizers
- `browser-history-acset` - Path equivalence in ACSets
- `ordered-locale` (sheaves.py) - Gluing as dual of coequalizer
- `compositional-acset-comparison` (IrreversibleMorphisms.jl) - Lossy morphisms

### Papers

- Lack & Sobociński, "Adhesive and Quasiadhesive Categories" (RAIRO 2005)
- Patterson et al., "Categorical Data Structures for Technical Computing" (Compositionality 2022)
- Brown, "Incremental Query Updating in Adhesive Categories" (Topos Institute 2025)

### Web Resources

- [nLab: Coequalizer](https://ncatlab.org/nlab/show/coequalizer)
- [Catlab.jl Documentation](https://algebraicjulia.github.io/Catlab.jl/)

---

## Related Skills

- `bisimulation-game` (-1) - Behavioral equivalence
- `oapply-colimit` (+1) - Pushout composition
- `topos-adhesive-rewriting` (+1) - Incremental updates
- `temporal-coalgebra` (-1) - Coalgebraic bisimulation
- `ordered-locale` (0) - Sheaf gluing

---

**Skill Name**: coequalizers  
**Type**: Category-Theoretic Skill Composition  
**Trit**: 0 (ERGODIC - coordinates equivalences)  
**GF(3)**: Conserved via triadic composition

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
coequalizers (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch8: Degeneracy
- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
