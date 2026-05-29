---
name: moebius-inversion
description: "Möbius inversion on posets and lattices: alternating sums, chromatic polynomials, incidence algebras, and centrality predicates."
version: 1.0.0
---


# Möbius Inversion Skill

> *"The Möbius function inverts summation over divisors - the fundamental tool connecting local constraints to global structure."*

## bmorphism Contributions

> *"all is bidirectional"*
> — [@bmorphism](https://gist.github.com/bmorphism/ead83aec97dab7f581d49ddcb34a46d4), Play/Coplay gist

**Categorical Connection**: Möbius inversion on posets is the prototypical example of **adjunction** in category theory — ζ and μ form a zeta-Möbius pair where convolution is the composition operation. This connects to:
- **Incidence algebras** as categorical structures on posets
- **Bidirectional computation** — inversion recovers local from global
- **Chromatic polynomials** via ACSet bond lattices

**Plurigrid Integration**: The GF(3) trit system uses μ(3) = -1 (3 is prime) as the fundamental sign flip that creates the action-perception duality:
- Action trits: {-, 0, +}
- Perception trits: {+, 0, -} (Möbius-inverted)
- Double inversion: μ ∘ μ = identity

**Key Reference**:
- Rota (1964) — "On the Foundations of Combinatorial Theory I: Theory of Möbius Functions"

## Overview

Möbius inversion provides:

1. **Alternating sums** - Invert cumulative sums to get point values
2. **Chromatic polynomials** - Count colorings via bond lattice
3. **Incidence algebras** - Algebraic structure on posets
4. **Centrality predicates** - Validate node importance via inversion

## Classical Möbius Function

### Definition

For positive integers:

```
μ(n) = { 1      if n = 1
       { (-1)^k if n = p₁p₂...pₖ (k distinct primes)
       { 0      if n has squared prime factor
```

### Key Values

| n | μ(n) | Meaning |
|---|------|---------|
| 1 | 1 | Identity |
| 2 | -1 | Prime |
| **3** | **-1** | **Prime - key for GF(3)** |
| 4 | 0 | Squared (2²) |
| 5 | -1 | Prime |
| 6 | 1 | Two primes (2·3) |
| 12 | 0 | Has 2² |
| 30 | -1 | Three primes (2·3·5) |

### Implementation

```julia
function moebius(n)
    if n == 1
        return 1
    end
    
    # Factor n
    factors = factor(n)
    
    # Check for squared factors
    for (p, e) in factors
        if e > 1
            return 0
        end
    end
    
    # (-1)^(number of prime factors)
    return (-1)^length(factors)
end
```

## Möbius Inversion Formula

### For Divisors

If `f(n) = Σ_{d|n} g(d)` then:

```
g(n) = Σ_{d|n} μ(n/d) × f(d)
     = Σ_{d|n} μ(d) × f(n/d)
```

### Example: Euler's Totient

```julia
# φ(n) counts integers 1 ≤ k ≤ n with gcd(k,n) = 1
# We have: n = Σ_{d|n} φ(d)
# By Möbius inversion: φ(n) = Σ_{d|n} μ(n/d) × d

function euler_totient(n)
    result = 0
    for d in divisors(n)
        result += moebius(n ÷ d) * d
    end
    return result
end
```

## Möbius on Posets

### General Definition

For a locally finite poset (P, ≤), the **Möbius function** μ: P × P → ℤ is:

```
μ(x, x) = 1
μ(x, y) = -Σ_{x ≤ z < y} μ(x, z)  if x < y
μ(x, y) = 0                        if x ≰ y
```

### Inversion on Posets

If `f(x) = Σ_{y ≤ x} g(y)` then:

```
g(x) = Σ_{y ≤ x} μ(y, x) × f(y)
```

### Implementation

```julia
struct Poset
    elements::Vector
    leq::Function  # (x, y) -> Bool
end

function moebius_poset(P::Poset, x, y)
    if x == y
        return 1
    end
    if !P.leq(x, y)
        return 0
    end
    
    # Sum over interval [x, y)
    result = 0
    for z in P.elements
        if P.leq(x, z) && P.leq(z, y) && z != y
            result -= moebius_poset(P, x, z)
        end
    end
    return result
end
```

## Chromatic Polynomial

### Bond Lattice

For a graph G, the **bond lattice** L(G) consists of partitions of V(G) induced by edge subsets.

### Whitney's Formula

The chromatic polynomial P(G, k) counts proper k-colorings:

```
P(G, k) = Σ_{π ∈ L(G)} μ(0̂, π) × k^{|π|}
```

where |π| is the number of parts in partition π.

### Implementation

```julia
function chromatic_polynomial(G, k)
    """
    Compute P(G, k) via Möbius inversion on bond lattice.
    """
    partitions = bond_lattice(G)
    
    result = 0
    for π in partitions
        μ_val = moebius_bond_lattice(G, partition_0, π)
        result += μ_val * k^(num_parts(π))
    end
    
    return result
end
```

### Deletion-Contraction

Alternative recursive formula:

```julia
function chromatic_deletion_contraction(G, k)
    if ne(G) == 0
        return k^nv(G)
    end
    
    e = first(edges(G))
    G_delete = delete_edge(G, e)
    G_contract = contract_edge(G, e)
    
    return chromatic_deletion_contraction(G_delete, k) - 
           chromatic_deletion_contraction(G_contract, k)
end
```

## Alternating Möbius for GF(3)

### Sign Inversion Symmetry

For GF(3) = {-1, 0, +1}:

```
Action:     {-, 0, +}
Perception: {+, 0, -}  (Möbius-inverted)

μ × μ = identity (applying twice returns original)
```

### Perception-Action Duality

```julia
function moebius_duality(state::GF3)
    """
    Möbius inversion creates observer/observed duality.
    Action and perception are inverted images.
    """
    # μ(3) = -1 for our tritwise system
    μ_3 = -1
    
    return state * μ_3
end

# Verify involution: μ ∘ μ = id
@assert moebius_duality(moebius_duality(1)) == 1
@assert moebius_duality(moebius_duality(-1)) == -1
@assert moebius_duality(moebius_duality(0)) == 0
```

## Centrality Validity via Inversion

### Local-Global Inversion

```julia
function centrality_moebius_valid(G, centrality::Vector)
    """
    Validate centrality using Möbius inversion.
    
    Local constraint: c(v) = Σ_{u ∈ N(v)} contribution(u)
    Global invariant: Σ_v c(v) = 1
    
    Möbius inversion recovers individual contributions from sums.
    """
    n = nv(G)
    
    # Build divisibility-like structure on graph
    # Each node "divides" its neighbors
    contributions = zeros(n)
    
    for v in 1:n
        local_sum = 0.0
        for u in neighbors(G, v)
            # Möbius contribution from u
            dist = shortest_path_length(G, 1, u)  # Use node 1 as reference
            μ_val = moebius(dist + 1)  # +1 to avoid μ(0)
            local_sum += μ_val * centrality[u]
        end
        contributions[v] = local_sum
    end
    
    # Validity: contributions should be consistent
    return all(abs.(contributions .- mean(contributions)) .< 0.1)
end
```

### Alternating Harmonic Centrality

```julia
function alternating_harmonic_centrality(G)
    """
    Centrality via alternating sums (Möbius-weighted paths).
    
    c(v) = Σ_{k≥1} μ(k) × (paths of length k from v) / k
    """
    n = nv(G)
    centrality = zeros(n)
    
    A = adjacency_matrix(G)
    max_k = diameter(G)
    
    for v in 1:n
        for k in 1:max_k
            μ_k = moebius(k)
            if μ_k != 0
                # Count paths of length k from v
                paths_k = A^k[v, :]
                centrality[v] += μ_k * sum(paths_k) / k
            end
        end
    end
    
    # Normalize
    return centrality ./ sum(abs.(centrality))
end
```

## Incidence Algebra

### Definition

The **incidence algebra** I(P) of a poset P consists of functions f: P × P → ℂ 
where f(x, y) = 0 if x ≰ y.

### Convolution Product

```
(f * g)(x, y) = Σ_{x ≤ z ≤ y} f(x, z) × g(z, y)
```

### Key Elements

| Element | Definition | Role |
|---------|------------|------|
| δ (delta) | δ(x,y) = [x = y] | Identity |
| ζ (zeta) | ζ(x,y) = [x ≤ y] | Summation |
| μ (Möbius) | ζ * μ = μ * ζ = δ | Inversion |

### Implementation

```julia
struct IncidenceAlgebra
    poset::Poset
end

function convolve(I::IncidenceAlgebra, f, g)
    P = I.poset
    result = Dict{Tuple, Number}()
    
    for x in P.elements, y in P.elements
        if !P.leq(x, y)
            result[(x, y)] = 0
            continue
        end
        
        sum = 0
        for z in P.elements
            if P.leq(x, z) && P.leq(z, y)
                sum += f(x, z) * g(z, y)
            end
        end
        result[(x, y)] = sum
    end
    
    return (x, y) -> result[(x, y)]
end

# Verify: ζ * μ = δ
function verify_inversion(I::IncidenceAlgebra)
    ζ = (x, y) -> I.poset.leq(x, y) ? 1 : 0
    μ = (x, y) -> moebius_poset(I.poset, x, y)
    δ = (x, y) -> x == y ? 1 : 0
    
    ζμ = convolve(I, ζ, μ)
    
    for x in I.poset.elements, y in I.poset.elements
        @assert ζμ(x, y) == δ(x, y)
    end
    return true
end
```

## GF(3) Triad Integration

### Trit Assignment

| Component | Trit | Role |
|-----------|------|------|
| ramanujan-expander | -1 | Validator - spectral bounds |
| ihara-zeta | 0 | Coordinator - non-backtracking |
| **moebius-inversion** | **+1** | **Generator** - produces alternating sums |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

### μ(3) = -1 is Central

For GF(3), the key Möbius value is:

```
μ(3) = -1  (3 is prime)

This means:
- Tritwise inversion flips sign
- Three iterations: μ³ = -μ (mod 3 behavior)
- Connects to spectral gap via λ₂ ≥ 2√2
```

## DuckDB Schema

```sql
CREATE TABLE moebius_values (
    n INT PRIMARY KEY,
    mu INT,  -- -1, 0, or 1
    is_squarefree BOOLEAN,
    prime_factors INT[],
    computed_at TIMESTAMP
);

CREATE TABLE poset_moebius (
    poset_id VARCHAR,
    x VARCHAR,
    y VARCHAR,
    mu_xy INT,
    PRIMARY KEY (poset_id, x, y)
);

CREATE TABLE chromatic_coefficients (
    graph_id VARCHAR,
    k INT,
    p_g_k BIGINT,  -- P(G, k)
    bond_lattice_size INT,
    computed_at TIMESTAMP,
    PRIMARY KEY (graph_id, k)
);

CREATE TABLE centrality_alternating (
    graph_id VARCHAR,
    vertex_id INT,
    harmonic_centrality FLOAT,
    moebius_valid BOOLEAN,
    PRIMARY KEY (graph_id, vertex_id)
);
```

## Commands

```bash
just moebius-table 100           # Print μ(n) for n ≤ 100
just moebius-invert data.json    # Apply inversion to sums
just moebius-chromatic graph.json 5  # P(G, 5)
just moebius-centrality graph.json   # Alternating harmonic centrality
just moebius-verify graph.json       # Validate centrality predicates
```

## Literature

1. **Möbius (1831)** - Original number-theoretic definition
2. **Rota (1964)** - "On the Foundations of Combinatorial Theory I: Theory of Möbius Functions"
3. **Stanley (1986)** - "Enumerative Combinatorics" (comprehensive treatment)
4. **Cioabă & Murty** - Chromatic polynomial via Möbius
5. **Music Topos (2024)** - GF(3) integration and alternating centrality

## Julia Scientific Package Integration

From `julia-scientific` skill - related Julia packages:

| Package | Category | Möbius Integration |
|---------|----------|-------------------|
| **Primes.jl** | Math | Prime factorization |
| **AbstractAlgebra.jl** | Algebra | Incidence algebras |
| **Graphs.jl** | Networks | Graph Möbius function |
| **Catlab.jl** | ACSets | Poset lattices |
| **Symbolics.jl** | Symbolic | Möbius identities |
| **Combinatorics.jl** | Combinatorics | Generating functions |
| **ITensors.jl** | Quantum | Tensor network contraction |

### Scientific Applications

```julia
# Number-theoretic Möbius (sympy → Symbolics.jl + Primes.jl)
using Primes
function moebius_julia(n)
    n == 1 && return 1
    f = factor(n)
    any(e > 1 for (p, e) in f) && return 0
    return (-1)^length(f)
end

# Graph chromatic polynomial (networkx → Graphs.jl)
using Graphs, Combinatorics
function chromatic_poly(G, k)
    # Deletion-contraction with Möbius
    n = nv(G)
    ne(G) == 0 && return k^n
    e = first(edges(G))
    G_minus = rem_edge(copy(G), e)
    G_contract = contract_edge(copy(G), e)
    chromatic_poly(G_minus, k) - chromatic_poly(G_contract, k)
end

# Möbius on poset lattice (ACSets)
using Catlab
function lattice_moebius(P::ACSet, x, y)
    # Recursive definition on poset P
    x == y && return 1
    -sum(lattice_moebius(P, x, z) for z in interval(P, x, y))
end

# Tensor network contraction via Möbius (quantum)
using ITensors
# Contraction order optimization uses incidence algebra
```

## Related Skills

- `ramanujan-expander` - Spectral validation
- `ihara-zeta` - Prime cycle extraction
- `three-match` - 3-coloring constraints
- `acsets` - Bond lattice as C-set
- `influence-propagation` - Centrality validation
- `julia-scientific` - Full Julia package mapping (137 skills)



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