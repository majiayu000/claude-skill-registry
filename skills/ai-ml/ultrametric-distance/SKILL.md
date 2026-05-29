---
name: ultrametric-distance
description: Non-Archimedean distance metrics for hierarchical clustering and p-adic analysis
version: 1.0.0
---


# Ultrametric Distance Skill

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - validator/constrainer)
**Principle**: d(x,z) ≤ max(d(x,y), d(y,z)) — Strong Triangle Inequality

---

## Overview

**Ultrametric Distance** provides non-Archimedean distance functions where the strong triangle inequality holds. Essential for:

1. **Hierarchical clustering**: Natural tree structures emerge
2. **p-adic analysis**: Number-theoretic computations
3. **Phylogenetic trees**: Evolution distance metrics
4. **Version control**: Commit ancestry distances

## Core Property

```
Ultrametric Inequality:
  d(x, z) ≤ max(d(x, y), d(y, z))

  Unlike Euclidean: d(x,z) ≤ d(x,y) + d(y,z)
  Ultrametric is STRONGER: max instead of sum
```

## Key Insight

In ultrametric space, ALL triangles are isoceles with the unequal side being the shortest.

## Python Implementation

```python
import math
from typing import List, Tuple, Callable

def ultrametric_distance(x: List[float], y: List[float]) -> float:
    """Compute ultrametric (sup-norm) distance."""
    return max(abs(a - b) for a, b in zip(x, y))

def p_adic_valuation(n: int, p: int) -> int:
    """Compute p-adic valuation v_p(n) = max k such that p^k | n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def p_adic_distance(x: int, y: int, p: int) -> float:
    """
    Compute p-adic distance: d_p(x,y) = p^(-v_p(x-y))
    
    Properties:
    - d_p(x,x) = 0
    - d_p(x,y) = d_p(y,x)
    - d_p(x,z) ≤ max(d_p(x,y), d_p(y,z))  # Ultrametric!
    """
    if x == y:
        return 0.0
    v = p_adic_valuation(abs(x - y), p)
    return p ** (-v)

def verify_ultrametric(d: Callable, points: List) -> dict:
    """Verify that distance function satisfies ultrametric inequality."""
    violations = []
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            for k, z in enumerate(points):
                dxz = d(x, z)
                dxy = d(x, y)
                dyz = d(y, z)
                if dxz > max(dxy, dyz) + 1e-10:
                    violations.append({
                        'x': x, 'y': y, 'z': z,
                        'd(x,z)': dxz,
                        'max(d(x,y),d(y,z))': max(dxy, dyz)
                    })
    return {
        'is_ultrametric': len(violations) == 0,
        'violations': violations[:5],
        'total_violations': len(violations)
    }
```

## Hierarchical Clustering (UPGMA)

```python
def ultrametric_upgma(distance_matrix: List[List[float]]) -> dict:
    """
    Build ultrametric tree via UPGMA clustering.
    Returns dendrogram as nested dict.
    """
    n = len(distance_matrix)
    clusters = [{i} for i in range(n)]
    heights = [0.0] * n
    tree = {i: {'leaf': i, 'height': 0} for i in range(n)}
    
    while len(clusters) > 1:
        # Find closest pair
        min_dist = float('inf')
        merge_i, merge_j = 0, 1
        
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Average linkage distance
                d = sum(distance_matrix[a][b] 
                       for a in clusters[i] 
                       for b in clusters[j]) / (len(clusters[i]) * len(clusters[j]))
                if d < min_dist:
                    min_dist, merge_i, merge_j = d, i, j
        
        # Merge clusters
        new_cluster = clusters[merge_i] | clusters[merge_j]
        new_height = min_dist / 2
        new_node = {
            'left': tree[merge_i],
            'right': tree[merge_j],
            'height': new_height,
            'members': list(new_cluster)
        }
        
        # Update
        tree[merge_i] = new_node
        del tree[merge_j]
        clusters[merge_i] = new_cluster
        del clusters[merge_j]
    
    return tree[0]
```

## Git Commit Distance

```python
def commit_ultrametric_distance(repo, commit_a: str, commit_b: str) -> int:
    """
    Ultrametric distance between commits = depth to common ancestor.
    
    d(A, B) = depth(merge_base(A, B))
    
    Satisfies ultrametric: branching creates natural hierarchy.
    """
    import subprocess
    
    # Find merge base
    merge_base = subprocess.check_output(
        ['git', 'merge-base', commit_a, commit_b],
        cwd=repo
    ).decode().strip()
    
    # Count commits from merge base to root
    depth = int(subprocess.check_output(
        ['git', 'rev-list', '--count', merge_base],
        cwd=repo
    ).decode().strip())
    
    return depth
```

## Julia Implementation

```julia
module UltrametricDistance

"""
    p_adic_distance(x::Int, y::Int, p::Int) -> Float64

Compute p-adic distance between integers.
"""
function p_adic_distance(x::Int, y::Int, p::Int)
    x == y && return 0.0
    diff = abs(x - y)
    v = 0
    while diff % p == 0
        diff ÷= p
        v += 1
    end
    return Float64(p)^(-v)
end

"""
    ultrametric_ball(center, radius, points, d)

Return all points within ultrametric ball.
Note: In ultrametric space, every point in the ball is a center!
"""
function ultrametric_ball(center, radius, points, d)
    filter(p -> d(center, p) ≤ radius, points)
end

"""
    is_ultrametric(d, points) -> Bool

Verify ultrametric inequality for all triples.
"""
function is_ultrametric(d, points)
    for x in points, y in points, z in points
        d(x, z) > max(d(x, y), d(y, z)) && return false
    end
    return true
end

end # module
```

## Integration with GF(3)

Ultrametric distances map naturally to trits:

```python
def distance_to_trit(d: float, thresholds: Tuple[float, float] = (0.33, 0.66)) -> int:
    """
    Map ultrametric distance to trit.
    
    Close (d < 0.33)   → +1 (PLUS, same cluster)
    Medium (0.33-0.66) →  0 (ERGODIC, sibling clusters)  
    Far (d > 0.66)     → -1 (MINUS, distant branches)
    """
    if d < thresholds[0]:
        return 1
    elif d < thresholds[1]:
        return 0
    else:
        return -1
```

## Commands

```bash
# Verify p-adic distances
python -c "from ultrametric import p_adic_distance; print(p_adic_distance(12, 20, 2))"

# Build UPGMA tree
python -m ultrametric.upgma --input distances.csv --output tree.json

# Git commit distance
git-ultrametric HEAD~5 main
```

## Properties

| Property | Euclidean | Ultrametric |
|----------|-----------|-------------|
| Triangle | d(x,z) ≤ d(x,y) + d(y,z) | d(x,z) ≤ max(d(x,y), d(y,z)) |
| Ball centers | Unique | Every interior point |
| Triangles | Arbitrary | Isoceles (short base) |
| Topology | Connected | Totally disconnected |

---

**Skill Name**: ultrametric-distance
**Type**: Distance Metric / Clustering
**Trit**: -1 (MINUS)
**Use Case**: Hierarchical validation, tree construction, version ancestry

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
ultrametric-distance (+) + SDF.Ch3 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)


### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
