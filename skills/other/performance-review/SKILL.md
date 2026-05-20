---
name: compact-reviewer:performance-review
description: Use when reviewing Compact circuits for performance issues, optimizing constraint counts, analyzing proof generation time, or identifying gas and cost optimization opportunities.
---

# Performance Review Skill

Analyze circuit efficiency and identify optimization opportunities in Compact contracts.

## When to Use

This skill activates for queries about:
- Circuit performance and efficiency
- Constraint count optimization
- Proof generation time
- Gas/cost optimization
- Performance bottlenecks

**Trigger words**: performance, optimization, constraints, circuit efficiency, proof generation, gas, cost

## Quick Reference

### Constraint Cost Table

| Operation | Cost | Notes |
|-----------|------|-------|
| Addition (`+`) | 0 | Free in R1CS |
| Subtraction (`-`) | 0 | Free |
| Multiplication (`*`) | 1 | Single constraint |
| Division (`/`) | ~1 | Includes inverse |
| Equality (`==`) | ~1 | Direct check |
| Inequality (`<`, `>`) | ~254 | Bit decomposition |
| Hash (Pedersen) | ~1,000 | Optimized |
| SHA256 | ~25,000 | Expensive |
| Merkle proof (depth N) | ~N×1,000 | Per-level hash |

### Complexity Estimation

```
Total Constraints ≈
  (Hash Ops × 1,000) +
  (SHA256 Ops × 25,000) +
  (Comparisons × 254) +
  (Merkle Depth × 1,000) +
  (Loop Iterations × Body Cost)
```

### Quick Wins

| Optimization | Savings | Effort |
|-------------|---------|--------|
| Replace SHA256 → Pedersen | 25x per hash | Low |
| Use `==` instead of `<` | ~253 constraints | Low |
| Reduce Merkle depth | ~1,000 per level | Medium |
| Move computation to witness | Variable | Medium |

## Review Process

### 1. Count Expensive Operations

Scan the contract for:

```compact
// High-cost operations
persistentHash()      // ~1,000 constraints
persistentCommit()    // ~1,000 constraints
sha256()              // ~25,000 constraints ❌ Avoid
ecMul()               // ~5,000-10,000 constraints

// Medium-cost operations
if x < y { }          // ~254 constraints (bit decomposition)
for i in 0..N { }     // Multiplies inner constraints by N

// Low-cost operations
x + y                 // Free
x * y                 // 1 constraint
x == y                // ~1 constraint
```

### 2. Analyze Loops

For each loop:

```
1. What operations are inside?
2. How many iterations?
3. Can any operations move outside?
4. Is the loop necessary?
```

**Example**:
```compact
// ❌ Inefficient: hash inside loop
for i in 0..10 {
    hashes[i] = hash(data[i]);  // 10 × 1,000 = 10,000 constraints
}

// ✅ Consider: can this be done in witness?
```

### 3. Check Type Choices

Smaller types mean cheaper comparisons:

| Type | Comparison Cost |
|------|-----------------|
| Uint<8> | ~8 constraints |
| Uint<64> | ~64 constraints |
| Uint<254> | ~254 constraints |

### 4. Evaluate Merkle Usage

```compact
// Merkle tree with depth 20
const proof = get_merkle_proof();  // ~20,000 constraints

// Consider: Is depth 20 necessary?
// Depth 10 would be ~10,000 constraints
```

## References

- [Constraint Optimization](./references/constraint-optimization.md) - Optimization techniques
- [Circuit Complexity](./references/circuit-complexity.md) - Cost breakdown

## Related Skills

- [design-architecture](../design-architecture/SKILL.md) - Structural efficiency
- [compact-core/standard-library](../../../compact-core/skills/standard-library/SKILL.md) - Efficient functions
