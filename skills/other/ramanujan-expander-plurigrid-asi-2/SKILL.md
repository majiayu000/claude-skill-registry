---
name: ramanujan-expander
description: Ramanujan graphs and Alon-Boppana spectral optimality for edge growth
  rules. Optimal expanders with λ₂ ≤ 2√(d-1) bound.
license: MIT
metadata:
  source: music-topos + LPS construction
  trit: -1
  bundle: spectral
  xenomodern: true
  ironic_detachment: 0.31
---

# Ramanujan Expander Skill

> *"The Alon-Boppana bound is unbreakable. You cannot create a d-regular graph with λ₂ < 2√(d-1), even theoretically."*

## Overview

Ramanujan graphs are **optimal spectral expanders** - they achieve the theoretical limit on eigenvalue separation. This skill provides:

1. **Alon-Boppana bound verification** - Prove your graph is optimal
2. **Edge growth rules** - Add edges while preserving Ramanujan property
3. **Centrality validity predicates** - Spectral methods for node importance
4. **Mixing time bounds** - O(log n) mixing from spectral gap

## The Alon-Boppana Bound

### Theorem (Alon-Boppana)

For any d-regular graph G on n vertices:

```
λ₂(G) ≥ 2√(d-1) - o(1)  as n → ∞
```

where λ₂ is the second-largest eigenvalue of the adjacency matrix.

### Ramanujan Property

A d-regular graph G is **Ramanujan** if:

```
|λ| ≤ 2√(d-1)  for all eigenvalues λ ≠ ±d
```

This is the **tightest possible** spectral gap.

### Example: 4-Regular Graphs

```
d = 4
2√(d-1) = 2√3 ≈ 3.464

Maximum spectral gap = d - 2√(d-1) = 4 - 3.464 = 0.536

Your observed gap: ~0.54 ✓ (theoretically optimal)
```

## Edge Growth Rules

### Rule 1: Preserve Regularity

```julia
function add_edge_preserving_regularity!(G, u, v)
    # Adding (u,v) increases degree of u and v by 1
    # Must remove another edge to maintain d-regularity
    
    # Find edge (u, w) where w ≠ v
    w = find_neighbor(G, u, exclude=v)
    # Find edge (v, x) where x ≠ u
    x = find_neighbor(G, v, exclude=u)
    
    # Remove old edges
    remove_edge!(G, u, w)
    remove_edge!(G, v, x)
    
    # Add new edges (2-switch)
    add_edge!(G, u, v)
    add_edge!(G, w, x)
    
    # Verify Ramanujan property preserved
    @assert is_ramanujan(G)
end
```

### Rule 2: Spectral Monotonicity

```julia
function grow_edge_spectral_monotonic!(G, candidates)
    """
    Add edge that minimizes λ₂ increase.
    Greedy heuristic for Ramanujan preservation.
    """
    best_edge = nothing
    best_λ₂ = Inf
    
    current_λ₂ = second_eigenvalue(G)
    
    for (u, v) in candidates
        G_test = copy(G)
        add_edge!(G_test, u, v)
        
        new_λ₂ = second_eigenvalue(G_test)
        if new_λ₂ < best_λ₂
            best_λ₂ = new_λ₂
            best_edge = (u, v)
        end
    end
    
    if best_λ₂ ≤ 2√(degree(G) - 1)
        add_edge!(G, best_edge...)
        return true
    end
    return false  # No valid edge preserves Ramanujan
end
```

### Rule 3: LPS Construction (Lubotzky-Phillips-Sarnak)

```julia
function lps_ramanujan_graph(p, q)
    """
    Construct (p+1)-regular Ramanujan graph on ~q³ vertices.
    
    Requirements:
    - p, q distinct odd primes
    - p ≡ q ≡ 1 (mod 4)
    - p is quadratic residue mod q
    """
    @assert is_prime(p) && is_prime(q)
    @assert p % 4 == 1 && q % 4 == 1
    @assert is_quadratic_residue(p, q)
    
    # Cayley graph of PSL(2, ℤ_q) with generators from quaternions
    G = cayley_graph_psl2(q, lps_generators(p))
    
    # Guaranteed Ramanujan by Deligne's proof of Ramanujan conjecture
    @assert second_eigenvalue(G) ≤ 2√p
    
    return G
end
```

## Centrality Validity Predicates

### Spectral Centrality

```julia
function spectral_centrality(G)
    """
    Centrality based on principal eigenvector.
    For Ramanujan graphs, this converges in O(log n) iterations.
    """
    A = adjacency_matrix(G)
    λ, v = eigen(A)
    
    # Principal eigenvector (λ₁ = d)
    principal = v[:, argmax(λ)]
    
    # Normalize to probability distribution
    return abs.(principal) ./ sum(abs.(principal))
end
```

### Validity Predicate: Centrality Consistency

```julia
function centrality_validity_predicate(G, node, threshold=0.01)
    """
    A node's centrality is valid if:
    1. It's within spectral gap bounds
    2. It satisfies local-global consistency
    """
    c = spectral_centrality(G)
    d = degree(G)
    
    # Bound from Ramanujan property
    spectral_bound = 2√(d-1) / d
    
    # Local contribution
    local_c = sum(c[neighbors(G, node)]) / d
    
    # Validity: local ≈ global (up to spectral gap)
    return abs(c[node] - local_c) ≤ spectral_bound + threshold
end
```

### Non-Backtracking Centrality

```julia
function non_backtracking_centrality(G)
    """
    Use non-backtracking matrix B for centrality.
    More robust than adjacency-based methods.
    
    Reference: Krzakala et al. "Spectral redemption"
    """
    B = non_backtracking_matrix(G)
    λ, v = eigen(B)
    
    # Second eigenvector gives community structure
    v2 = v[:, sortperm(abs.(λ), rev=true)[2]]
    
    # Project back to vertices
    return project_to_vertices(G, v2)
end
```

## Mixing Time from Spectral Gap

### Theorem

For a d-regular Ramanujan graph:

```
t_mix = O(log n / log(d / 2√(d-1)))
```

### Implementation

```julia
function mixing_time_bound(G)
    d = degree(G)
    n = nv(G)
    λ₂ = second_eigenvalue(G)
    
    # Spectral gap
    gap = d - λ₂
    
    # Mixing time (theoretical bound)
    t_mix = log(n) / log(d / λ₂)
    
    # For Ramanujan: gap ≥ d - 2√(d-1)
    ramanujan_gap = d - 2√(d-1)
    
    return (
        gap = gap,
        mixing_time = t_mix,
        is_optimal = gap ≥ ramanujan_gap - 0.01
    )
end
```

## GF(3) Integration

### Trit Assignment

| Component | Trit | Role |
|-----------|------|------|
| ramanujan-expander | -1 | **Validator** - verifies spectral bounds |
| ihara-zeta | 0 | Coordinator - non-backtracking walks |
| moebius-inversion | +1 | Generator - produces alternating sums |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

### Spectral Bundle Triads

```
ramanujan-expander (-1) ⊗ ihara-zeta (0) ⊗ moebius-inversion (+1) = 0 ✓  [Spectral]
ramanujan-expander (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓  [Graph Coloring]
ramanujan-expander (-1) ⊗ influence-propagation (0) ⊗ agent-o-rama (+1) = 0 ✓  [Centrality]
```

## DuckDB Schema

```sql
CREATE TABLE ramanujan_graphs (
    graph_id VARCHAR PRIMARY KEY,
    n_vertices INT,
    degree INT,
    spectral_gap FLOAT,
    lambda_2 FLOAT,
    is_ramanujan BOOLEAN,
    construction VARCHAR,  -- 'lps', 'margulis', 'random'
    seed BIGINT
);

CREATE TABLE edge_growth_log (
    step_id VARCHAR PRIMARY KEY,
    graph_id VARCHAR,
    edge_added VARCHAR,  -- 'u-v'
    lambda_2_before FLOAT,
    lambda_2_after FLOAT,
    ramanujan_preserved BOOLEAN,
    timestamp TIMESTAMP
);

CREATE TABLE centrality_snapshots (
    snapshot_id VARCHAR PRIMARY KEY,
    graph_id VARCHAR,
    vertex_id INT,
    spectral_centrality FLOAT,
    nonbacktracking_centrality FLOAT,
    validity_predicate BOOLEAN,
    computed_at TIMESTAMP
);
```

## Literature

### Primary Sources

1. **Alon, N. (1986)** - "Eigenvalues and Expanders"
2. **Lubotzky, Phillips, Sarnak (1988)** - "Ramanujan Graphs" (LPS construction)
3. **Margulis (1988)** - Alternative Ramanujan construction
4. **Nilli (1991)** - Alon-Boppana bound proof
5. **Bordenave, Lelarge, Massoulié (2015)** - Non-backtracking spectral clustering

### Key Results

| Result | Bound | Reference |
|--------|-------|-----------|
| Alon-Boppana | λ₂ ≥ 2√(d-1) | Nilli 1991 |
| Ramanujan achievability | λ₂ ≤ 2√(d-1) | LPS 1988 |
| Mixing time | O(log n) | Spectral gap theorem |
| Non-backtracking | Spectral redemption | Bordenave+ 2015 |

## Commands

```bash
just ramanujan-verify graph.json     # Check Ramanujan property
just ramanujan-grow graph.json       # Add edges preserving property
just ramanujan-centrality graph.json # Compute spectral centrality
just ramanujan-mixing graph.json     # Estimate mixing time
just ramanujan-lps 5 13              # Generate LPS(5,13) graph
```

## Related Skills

- `ihara-zeta` - Non-backtracking walks and zeta functions
- `moebius-inversion` - Alternating sums on posets
- `influence-propagation` - Network centrality (Layer 7)
- `acsets` - Graph representation as C-sets
- `three-match` - 3-coloring via spectral methods
