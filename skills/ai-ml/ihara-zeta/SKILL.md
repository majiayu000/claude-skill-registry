---
name: ihara-zeta
description: "Ihara zeta function for graphs: non-backtracking walks, prime cycles, and spectral analysis via det(I - uB)."
version: 1.0.0
---


# Ihara Zeta Function Skill

> *"The Ihara zeta function encodes all non-backtracking closed walks - the 'prime cycles' of a graph."*

## Overview

The Ihara zeta function generalizes the Riemann zeta function to graphs:

1. **Prime cycles** - Non-backtracking closed walks (graph analog of primes)
2. **Determinant formula** - ζ_G(u)^{-1} = det(I - uB) relation
3. **Ramanujan connection** - Riemann Hypothesis analog for graphs
4. **Non-backtracking matrix** - Central object for spectral clustering

## Definition

### Ihara Zeta Function

For a graph G, the **Ihara zeta function** is:

```
ζ_G(u) = ∏_{[C]} (1 - u^{|C|})^{-1}
```

where:
- Product is over equivalence classes [C] of **primitive** closed non-backtracking walks
- |C| is the length of the cycle
- Primitive = not a power of a shorter cycle

### Non-Backtracking Walk

A walk `v₀ → v₁ → v₂ → ... → vₖ` is **non-backtracking** if:

```
vᵢ₊₁ ≠ vᵢ₋₁  for all i
```

(Never immediately return to the previous vertex)

## The Determinant Formula

### Bass-Hashimoto Formula

```
ζ_G(u)^{-1} = (1 - u²)^{|E| - |V|} · det(I - uB)
```

where **B** is the non-backtracking matrix.

### Non-Backtracking Matrix

Indexed by **directed edges** (e, f) where head(e) = tail(f) and e ≠ f⁻¹:

```julia
function non_backtracking_matrix(G)
    # Directed edges: 2|E| entries
    directed_edges = [(u,v) for (u,v) in edges(G) 
                      for dir in [(u,v), (v,u)]]
    
    m = length(directed_edges)
    B = zeros(m, m)
    
    for (i, e) in enumerate(directed_edges)
        for (j, f) in enumerate(directed_edges)
            # e = (a→b), f = (c→d)
            # Connect if b = c AND a ≠ d (non-backtracking)
            if e[2] == f[1] && e[1] != f[2]
                B[i, j] = 1
            end
        end
    end
    
    return B
end
```

## Prime Cycles and Möbius

### Connection to Number Theory

| Number Theory | Graph Theory |
|---------------|--------------|
| Prime number p | Prime cycle C |
| log p | Length |C| |
| Riemann zeta ζ(s) | Ihara zeta ζ_G(u) |
| Prime Number Theorem | Cycle counting asymptotics |
| Riemann Hypothesis | Ramanujan property |

### Möbius Function on Paths

A path of length n is **prime** (non-backtracking) iff μ(n) ≠ 0:

```julia
function is_prime_path(path)
    """
    Check if path is non-backtracking (prime).
    Equivalent to μ(length) ≠ 0 in our encoding.
    """
    for i in 2:length(path)-1
        if path[i-1] == path[i+1]
            return false  # Backtracking detected
        end
    end
    return true
end

function moebius_filter(paths)
    """
    Filter to prime (non-backtracking) paths using Möbius.
    μ(n) ≠ 0 ⟺ n is squarefree ⟺ no repeated factors ⟺ no backtracking.
    """
    return filter(is_prime_path, paths)
end
```

## Ramanujan and Riemann Hypothesis

### Graph Riemann Hypothesis

A d-regular graph G satisfies the **Graph Riemann Hypothesis** if all poles of ζ_G(u) 
in |u| < 1/√(d-1) lie on the circle |u| = 1/√(d-1).

**Theorem**: G is Ramanujan ⟺ G satisfies the Graph Riemann Hypothesis.

### Verification

```julia
function check_graph_riemann_hypothesis(G)
    d = degree(G)
    B = non_backtracking_matrix(G)
    
    # Eigenvalues of B
    eigenvalues = eigvals(B)
    
    # Poles of zeta at 1/λ for each eigenvalue λ
    poles = 1 ./ eigenvalues
    
    # Check: all poles with |u| < 1/√(d-1) lie on |u| = 1/√(d-1)
    critical_radius = 1 / √(d - 1)
    
    for pole in poles
        r = abs(pole)
        if r < critical_radius && abs(r - critical_radius) > 0.001
            return false  # Pole inside critical circle but not on it
        end
    end
    
    return true
end
```

## Spectral Clustering via Non-Backtracking

### The Spectral Redemption Theorem

**Bordenave-Lelarge-Massoulié (2015)**:

> Non-backtracking spectral clustering succeeds down to the information-theoretic threshold, where adjacency-based methods fail.

```julia
function non_backtracking_clustering(G, k)
    """
    Cluster graph into k communities using non-backtracking eigenvectors.
    
    Succeeds where spectral clustering on adjacency matrix fails
    (the 'spectral redemption' phenomenon).
    """
    B = non_backtracking_matrix(G)
    
    # Get top k+1 eigenvectors (skip trivial)
    λ, V = eigen(B)
    idx = sortperm(abs.(λ), rev=true)
    
    # Project directed edge eigenvectors to vertices
    vertex_embeddings = project_to_vertices(G, V[:, idx[2:k+1]])
    
    # Cluster in embedding space
    return kmeans(vertex_embeddings, k)
end
```

## Zeta Function Computation

### Direct Computation

```julia
function ihara_zeta_coefficient(G, n)
    """
    Coefficient of u^n in log ζ_G(u).
    
    = (1/n) × (number of primitive closed non-backtracking walks of length n)
    """
    B = non_backtracking_matrix(G)
    
    # tr(B^n) counts all closed non-backtracking walks of length n
    # Möbius inversion extracts primitive ones
    total = tr(B^n)
    
    # Subtract non-primitive (powers of shorter cycles)
    primitive_count = 0
    for d in divisors(n)
        if d < n
            primitive_count += moebius(n ÷ d) * ihara_zeta_coefficient(G, d) * d
        end
    end
    
    return (total - primitive_count) / n
end
```

### Via Determinant

```julia
function ihara_zeta_inverse(G, u)
    """
    Compute ζ_G(u)^{-1} using Bass-Hashimoto formula.
    """
    B = non_backtracking_matrix(G)
    n_vertices = nv(G)
    n_edges = ne(G)
    
    # ζ_G(u)^{-1} = (1 - u²)^{|E| - |V|} × det(I - uB)
    return (1 - u^2)^(n_edges - n_vertices) * det(I - u * B)
end
```

## GF(3) Triad Integration

### Trit Assignment

| Component | Trit | Role |
|-----------|------|------|
| ramanujan-expander | -1 | Validator - spectral bounds |
| **ihara-zeta** | **0** | **Coordinator** - non-backtracking structure |
| moebius-inversion | +1 | Generator - alternating sums |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

### The Tritwise Triangle

```
         Ihara Zeta (Graphs)
              /\
             /  \
            /    \
           /      \
    Möbius -------- Chromatic
  (Number Theory)  (Combinatorics)
```

All three connect via:
- **Ihara ↔ Möbius**: Prime cycles counted by Möbius inversion
- **Möbius ↔ Chromatic**: P(G,k) via Möbius on bond lattice
- **Chromatic ↔ Ihara**: Both encode graph structure

## DuckDB Schema

```sql
CREATE TABLE prime_cycles (
    cycle_id VARCHAR PRIMARY KEY,
    graph_id VARCHAR,
    vertices VARCHAR[],
    length INT,
    is_primitive BOOLEAN,
    equivalence_class INT,
    seed BIGINT
);

CREATE TABLE zeta_coefficients (
    graph_id VARCHAR,
    n INT,
    coefficient FLOAT,
    primitive_count INT,
    computed_at TIMESTAMP,
    PRIMARY KEY (graph_id, n)
);

CREATE TABLE non_backtracking_spectrum (
    graph_id VARCHAR PRIMARY KEY,
    eigenvalues FLOAT[],
    spectral_radius FLOAT,
    satisfies_grh BOOLEAN,  -- Graph Riemann Hypothesis
    is_ramanujan BOOLEAN
);
```

## Commands

```bash
just ihara-zeta graph.json           # Compute zeta function
just ihara-primes graph.json 10      # List prime cycles up to length 10
just ihara-grh graph.json            # Check Graph Riemann Hypothesis
just ihara-cluster graph.json 3      # Non-backtracking clustering
just ihara-spectrum graph.json       # Eigenvalues of B matrix
```

## Literature

1. **Ihara (1966)** - Original definition for p-adic groups
2. **Bass (1992)** - Determinant formula (Bass-Hashimoto)
3. **Hashimoto (1989)** - Non-backtracking matrix connection
4. **Stark-Terras (1996)** - Survey of graph zeta functions
5. **Bordenave et al. (2015)** - Spectral redemption via non-backtracking

## Related Skills

- `ramanujan-expander` - Spectral gap and Alon-Boppana
- `moebius-inversion` - Alternating sums, prime extraction
- `three-match` - Graph coloring (chromatic polynomial)
- `acsets` - Graph representation



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