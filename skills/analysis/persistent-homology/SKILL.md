---
name: persistent-homology
description: Topological data analysis for stable feature verification across filtrations
version: 1.0.0
---

# Persistent Homology Skill: Stable Feature Verification

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - validator/analyzer)
**Color**: #2626D8 (Blue)
**Principle**: Stable features → Robust structure
**Frame**: Filtration with persistence diagrams

---

## Overview

**Persistent Homology** identifies topological features that persist across scales. Implements:

1. **Filtration**: Nested sequence of complexes by parameter
2. **Betti numbers**: β₀ (components), β₁ (holes), β₂ (voids)
3. **Persistence diagrams**: Birth-death pairs for features
4. **radare2 integration**: Binary analysis for structure holes

**Correct by construction**: Features with long persistence are stable/significant; short-lived features are noise.

## Core Formula

```
Filtration: K₀ ⊆ K₁ ⊆ ... ⊆ Kₙ  (by threshold ε)
Homology:   H_k(K_i) for each level
Persistence: (birth_i, death_j) for each feature

Stability Theorem:
  d_B(Dgm(f), Dgm(g)) ≤ ||f - g||_∞
```

For code complexity:
```ruby
# Filtration by cyclomatic complexity threshold
filtration = [
  threshold_0: simple_functions,
  threshold_5: moderate_functions,
  threshold_10: complex_functions,
  threshold_20: very_complex_functions
]

# Persistent features survive across thresholds
stable_structure = features.select { |f| f.persistence > 5 }
```

## Why Persistent Homology for Code?

1. **Complexity filtration**: Track structure across complexity levels
2. **Structural holes**: β₁ > 0 means cyclic dependencies
3. **Stability**: Long-lived features are fundamental
4. **Noise filtering**: Short-lived features are incidental

## Gadgets

### 1. ComplexityFiltration

Build filtration from code complexity:

```ruby
filtration = PersistentHomology::ComplexityFiltration.new(
  source: :codebase,
  metric: :cyclomatic_complexity
)
filtration.add_file("src/core.clj")
filtration.build!

filtration.levels           # => [0, 5, 10, 15, 20]
filtration.complex_at(10)   # => simplicial complex at threshold 10
filtration.inclusion(5, 10) # => inclusion map K_5 → K_10
```

### 2. BettiCalculator

Compute Betti numbers across filtration:

```ruby
betti = PersistentHomology::BettiCalculator.new(filtration)
betti.compute!

betti.beta_0(level: 5)   # => connected components
betti.beta_1(level: 10)  # => 1-dimensional holes (cycles)
betti.beta_2(level: 15)  # => 2-dimensional voids
betti.euler_characteristic(level: 10)  # => χ = β₀ - β₁ + β₂
```

### 3. PersistenceDiagram

Track feature birth/death:

```ruby
diagram = PersistentHomology::PersistenceDiagram.new(filtration)
diagram.compute!

diagram.pairs           # => [(birth, death), ...]
diagram.dimension(1)    # => 1-dim features only
diagram.persistence(feature)  # => death - birth
diagram.stable_features(threshold: 5)  # => long-lived only
diagram.bottleneck_distance(other_diagram)  # => stability metric
```

### 4. Radare2Analyzer

Integration with radare2 for binary analysis:

```ruby
analyzer = PersistentHomology::Radare2Analyzer.new(
  binary_path: "/path/to/binary",
  analysis_level: 2
)
analyzer.analyze!

analyzer.function_call_graph    # => build complex from CFG
analyzer.complexity_filtration  # => filter by function size
analyzer.structural_holes       # => β₁ features (circular calls)
analyzer.persistence_diagram    # => stable binary structures
```

### 5. StabilityVerifier

Verify structural stability:

```ruby
verifier = PersistentHomology::StabilityVerifier.new
verifier.add_version(:v1, filtration_v1)
verifier.add_version(:v2, filtration_v2)

result = verifier.verify!
result[:bottleneck_distance]     # => how different
result[:stable_preserved]        # => long-lived features kept
result[:new_stable_features]     # => emerged stable features
result[:lost_stable_features]    # => disappeared features
result[:gf3_conserved]           # => triad conservation
```

## Mathematical Foundation

### Simplicial Homology

```
Chain complex: C_n(K) → C_{n-1}(K) → ... → C_0(K)
Boundary map:  ∂_n: C_n → C_{n-1}
Cycles:        Z_n = ker(∂_n)
Boundaries:    B_n = im(∂_{n+1})
Homology:      H_n = Z_n / B_n
Betti number:  β_n = dim(H_n)
```

### Persistence Module

```
Filtration: K_0 ⊆ K_1 ⊆ ... ⊆ K_n
Induced maps: H_k(K_i) → H_k(K_j) for i ≤ j
Persistence: feature born at i, dies at j
```

### Stability Theorem

```
d_B(Dgm(f), Dgm(g)) ≤ ||f - g||_∞

Where d_B is bottleneck distance between diagrams
```

### Betti Numbers Interpretation

```
β₀ = connected components (clusters)
β₁ = 1-dimensional holes (loops, cycles)
β₂ = 2-dimensional voids (cavities)
β_n = n-dimensional holes
```

## Example Output

```
─── Persistent Homology Analysis ───
Source: src/ (42 files, 1337 functions)
Metric: Cyclomatic complexity
Filtration levels: [0, 5, 10, 15, 20, 25]

Betti Numbers by Level:
  Level  0: β₀=42  β₁=0   β₂=0   (42 isolated functions)
  Level  5: β₀=15  β₁=3   β₂=0   (modules forming, 3 cycles)
  Level 10: β₀=8   β₁=5   β₂=1   (more structure)
  Level 15: β₀=3   β₁=7   β₂=2   (complex dependencies)
  Level 20: β₀=1   β₁=12  β₂=3   (highly connected)

Persistence Diagram (1-dim):
  Feature A: born=5,  died=20  (persistence=15) ★ STABLE
  Feature B: born=10, died=25  (persistence=15) ★ STABLE
  Feature C: born=15, died=17  (persistence=2)  (noise)

Stable Features (persistence > 5):
  ★ 2 stable 1-dimensional holes (cyclic dependencies)
  ★ 1 stable 2-dimensional void (higher-order structure)

Structural Assessment:
  Cyclic dependencies detected: 2 persistent cycles
  Recommendation: Refactor cycles at birth level 5, 10

GF(3) Trit: -1 (MINUS/Analyzer)
```

---

**Skill Name**: persistent-homology
**Type**: Topological Data Analysis / Stable Feature Verification
**Trit**: -1 (MINUS)
**Color**: #2626D8 (Blue)
**GF(3)**: Forms valid triads with ERGODIC + PLUS skills
**Stability**: Bottleneck distance bounds feature perturbation

---

## End-of-Skill Interface

## Commands

```bash
# Compute persistent features
just homology-persist

# Analyze specific codebase
just homology-filter src/

# Binary analysis with radare2
just homology-binary /path/to/binary

# Compare versions
just homology-diff v1 v2
```

## API

```ruby
require 'persistent_homology'

# Create analyzer
analyzer = PersistentHomology::Analyzer.new(
  trit: -1,
  filtration_metric: :complexity
)

# Build filtration
analyzer.add_codebase("src/")
filtration = analyzer.build_filtration!

# Compute persistence
diagram = analyzer.compute_persistence!

# Get stable features
stable = diagram.stable_features(threshold: 5)
stable.each do |feature|
  puts "#{feature.dimension}-dim: born=#{feature.birth}, died=#{feature.death}"
end
```

## Integration with GF(3) Triads

Forms valid triads with ERGODIC (0) and PLUS (+1) skills:

```
persistent-homology (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓
persistent-homology (-1) ⊗ unworld (0) ⊗ cider-clojure (+1) = 0 ✓
persistent-homology (-1) ⊗ glass-bead-game (0) ⊗ rubato-composer (+1) = 0 ✓
```

## r2con Speaker Resources

Binary analysis repositories from r2con speakers for Radare2Analyzer integration:

| Speaker | Repository | Relevance |
|---------|-----------|-----------|
| oddcoder | [oddcoder/rair](https://github.com/oddcoder/rair) | RAIR Rust port for persistent CFG analysis |
| mr_phrazer | [mrphrazer/msynth](https://github.com/mrphrazer/msynth) | MBA deobfuscation for complexity filtration |
| alkalinesec | [aemmitt-ns/ESILSolve](https://github.com/aemmitt-ns/ESILSolve) | Symbolic exec for structural hole detection |
| Pelissier_S | ESIL side-channel | Side-channel simulation for homology persistence |
| condret | [radareorg/r2ghidra](https://github.com/radareorg/r2ghidra) | ESIL core for binary Betti numbers |