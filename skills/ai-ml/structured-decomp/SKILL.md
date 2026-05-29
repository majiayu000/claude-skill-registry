---
name: structured-decomp
description: StructuredDecompositions.jl sheaves on tree decompositions for FPT algorithms with bidirectional navigation
version: 1.0.0
---


# Structured Decompositions Skill

> Sheaves on tree decompositions with bidirectional navigation

**Version**: 1.1.0
**Trit**: 0 (Ergodic - coordinates decomposition)

## bmorphism Contributions

> *"Compositional Algorithms on Compositional Data: Deciding Sheaves on Presheaves"*
> — [ACT 2023](https://act2023.github.io/papers/paper45.pdf), Benjamin Merlin Bumpus et al.

> *"any computational problem which can be represented as a sheaf with respect to these topologies can be decided in linear time on classes of inputs which admit decompositions of bounded width"*
> — [arXiv:2302.05575](https://arxiv.org/abs/2302.05575)

**Key Insight**: Structured decompositions define **Grothendieck topologies** on categories of data (adhesive categories). This leads to algorithms on objects of any C-set category - structures such as: symmetric graphs, directed graphs, hypergraphs, databases, simplicial complexes, port graphs.

**Implementation**: Concrete implementations in the [AlgebraicJulia](https://algebraicjulia.github.io/StructuredDecompositions.jl) ecosystem.

Related to bmorphism's work on:
- [plurigrid/act](https://github.com/plurigrid/act) - cognitive category theory building blocks
- [Towards Foundations of Categorical Cybernetics](https://arxiv.org/abs/2105.06332) - cybernetic systems via parametrised optics

## Core Concept

**StrDecomp** = Functor `d: ∫G → C` where:
- **∫G** = category of elements of shape graph
- **C** = target category (Graph, FinSet, etc.)

```julia
using StructuredDecompositions

# Create decomposition from graph
d = StrDecomp(graph)

# Access components
bags(d)           # Local substructures
adhesions(d)      # Overlaps (shared boundaries)
adhesionSpans(d)  # Span morphisms
```

## The 𝐃 Functor

Lifts decision problems to decomposition space:

```julia
# Define problem as functor
k_coloring(G) = homomorphisms(G, K_k)

# Lift and solve
solution = 𝐃(k_coloring, decomp, CoDecomposition)
(answer, witness) = decide_sheaf_tree_shape(k_coloring, decomp)
```

## Specter-Style Navigation for Decompositions

Bidirectional paths for navigating decomposition structures:

```julia
using SpecterACSet

# Navigate bags
select([decomp_bags, ALL, acset_parts(:V)], decomp)

# Navigate adhesions with bidirectional transform
transform([decomp_adhesions, ALL], 
          adh -> reindex_adhesion(adh, mapping), 
          decomp)
```

### Decomposition Navigators

| Navigator | Select | Transform |
|-----------|--------|-----------|
| `decomp_bags` | All bag ACSets | Update bags |
| `decomp_adhesions` | All adhesion ACSets | Update adhesions |
| `decomp_spans` | Span morphisms | Reindex spans |
| `adhesion_between(i,j)` | Specific adhesion | Update specific |

## FPT Complexity

Runtime: **O(f(width) × n)** where width = max adhesion size

The sheaf condition ensures local solutions glue to global:

```julia
# Sheaf condition: sections over overlaps must agree
function verify_sheaf_condition(decomp, local_solutions)
    for (i, j) in adhesion_pairs(decomp)
        adh = adhesion(decomp, i, j)
        s_i = restrict(local_solutions[i], adh)
        s_j = restrict(local_solutions[j], adh)
        s_i == s_j || return false
    end
    return true
end
```

## Integration with lispsyntax-acset

Serialize decompositions to S-expressions for inspection:

```julia
# Decomposition → Sexp
sexp = sexp_of_strdecomp(decomp)

# Navigate sexp representation
bag_names = select([SEXP_CHILDREN, pred(is_bag), SEXP_HEAD, ATOM_VALUE], sexp)

# Roundtrip
decomp2 = strdecomp_of_sexp(GraphType, sexp)
```

## Adhesion as Colored Boundary

With Gay.jl deterministic coloring:

```julia
using Gay

struct ColoredAdhesion
    left_bag::ACSet
    right_bag::ACSet
    adhesion::ACSet
    color::String  # Deterministic from seed + index
end

function color_decomposition(decomp, seed)
    [ColoredAdhesion(
        bags(decomp)[i],
        bags(decomp)[j],
        adhesion(decomp, i, j),
        Gay.color_at(seed, idx)
    ) for (idx, (i, j)) in enumerate(adhesion_pairs(decomp))]
end
```

## GF(3) Triads

```
dmd-spectral (-1) ⊗ structured-decomp (0) ⊗ koopman-generator (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ structured-decomp (0) ⊗ colimit-reconstruct (+1) = 0 ✓
```

## Time-Varying Data (Brunton + Spivak Integration)

For DMD/Koopman analysis on decomposed data:

```julia
@present SchTimeVaryingDecomp(FreeSchema) begin
    Interval::Ob
    Snapshot::Ob
    State::Ob
    
    timestamp::Hom(Snapshot, Interval)
    observable::Hom(Snapshot, State)
    
    Time::AttrType
    Value::AttrType
end

# Colimit reconstructs dynamics
# DMD = colimit of snapshot diagram over intervals
```

## Julia Scientific Package Integration

From `julia-scientific` skill - related Julia packages:

| Package | Category | Integration |
|---------|----------|-------------|
| **StructuredDecompositions.jl** | Core | Sheaves on tree decomps |
| **Catlab.jl** | ACSets | Schema definitions |
| **AlgebraicRewriting.jl** | Rewriting | Local transformations |
| **Graphs.jl** | Networks | Graph decomposition |
| **MetaGraphs.jl** | Networks | Attributed graphs |
| **ITensors.jl** | Quantum | Tensor network decomp |
| **COBREXA.jl** | Bioinformatics | Metabolic network decomp |
| **GraphNeuralNetworks.jl** | ML | Message passing on decomps |

### Cross-Domain Decomposition Patterns

```julia
# Metabolic network decomposition
using StructuredDecompositions, COBREXA
model = load_model("ecoli.json")
decomp = tree_decomposition(reaction_graph(model))
local_fba = [fba(submodel) for submodel in bags(decomp)]

# Molecular graph decomposition for ML
using StructuredDecompositions, MolecularGraph, AtomicGraphNets
mol = smilestomol("c1ccccc1")  # benzene
mol_decomp = tree_decomposition(mol)
features = [featurize(bag) for bag in bags(mol_decomp)]

# Quantum tensor network
using StructuredDecompositions, ITensors
tn = tensor_network(circuit)
decomp = mps_decomposition(tn)
```

## References

- Bumpus et al. "Structured Decompositions" arXiv:2207.06091
- algebraicjulia.github.io/StructuredDecompositions.jl
- Nathan Marz: Specter inline caching patterns

## See Also

- `julia-scientific` - Full Julia package mapping (137 skills)
- `acsets` - Algebraic databases foundation
- `specter-acset` - Bidirectional navigation


## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Tree Decomposition
- **etetoolkit** [○] via bicomodule

### Bibliography References

- `algorithms`: 19 citations in bib.duckdb

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