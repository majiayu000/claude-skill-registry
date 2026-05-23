---
name: sheaf-cohomology
description: Čech cohomology for local-to-global consistency verification in code
  structure and data schemas.
license: UNLICENSED
metadata:
  source: local
---

# Sheaf Cohomology Skill: Local-to-Global Verification

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - validator/constraint)
**Color**: #2626D8 (Blue)
**Principle**: Local consistency → Global correctness
**Frame**: Čech cohomology with descent conditions

---

## Overview

**Sheaf Cohomology** validates that locally consistent data/code patches glue correctly into globally consistent structures. Uses:

1. **Čech cohomology**: H^n(U, F) obstruction classes
2. **Nerve of coverage**: N(U) simplicial complex from open cover
3. **Descent conditions**: Cocycle conditions for morphisms
4. **tree-sitter integration**: AST-level local consistency

**Correct by construction**: If local patches satisfy cocycle conditions, global structure is guaranteed.

## Core Formula

```
H⁰(U, F) = ker(d⁰)           # Global sections (agree everywhere)
H¹(U, F) = ker(d¹)/im(d⁰)    # Obstruction to gluing
H²(U, F) = ker(d²)/im(d¹)    # Higher obstructions
```

For code verification:
```ruby
# Three patches (files/modules) are consistent iff:
# On U_ij ∩ U_jk ∩ U_ik: g_ij ∘ g_jk = g_ik  (cocycle condition)

cocycle_satisfied?(patch_i, patch_j, patch_k)
  == (compose(g_ij, g_jk) == g_ik)
```

## Why Sheaf Cohomology for Code?

1. **Module boundaries**: Each module is an "open set"
2. **Import/export**: Transition functions between patches
3. **Type consistency**: Cocycle = type compatibility
4. **Refactoring safety**: H¹ = 0 means safe global transform

## Gadgets

### 1. ČechCoverVerifier

Verify local consistency across code patches:

```ruby
verifier = SheafCohomology::CechCoverVerifier.new(
  coverage: [:module_a, :module_b, :module_c]
)
verifier.add_transition(:module_a, :module_b, transition_ab)
verifier.add_transition(:module_b, :module_c, transition_bc)
verifier.add_transition(:module_a, :module_c, transition_ac)

verifier.cocycle_satisfied?  # => true if g_ab ∘ g_bc = g_ac
verifier.h1_obstruction      # => 0 if globally consistent
```

### 2. NerveConstructor

Build simplicial complex from coverage:

```ruby
nerve = SheafCohomology::NerveConstructor.new(
  opens: file_modules,
  intersections: shared_interfaces
)
nerve.simplices(0)  # => vertices (modules)
nerve.simplices(1)  # => edges (shared interfaces)
nerve.simplices(2)  # => triangles (triple overlaps)
nerve.euler_characteristic  # => χ(N(U))
```

### 3. DescentVerifier

Check morphism descent conditions:

```ruby
descent = SheafCohomology::DescentVerifier.new
descent.add_local_section(:patch_a, section_a)
descent.add_local_section(:patch_b, section_b)
descent.verify_descent!  # => raises if descent fails
descent.global_section   # => glued global section
```

### 4. TreeSitterSheaf

Integration with tree-sitter for AST verification:

```ruby
sheaf = SheafCohomology::TreeSitterSheaf.new(
  language: :clojure,
  coverage: :function_boundaries
)
sheaf.parse_file("src/core.clj")
sheaf.local_consistency_check  # => per-function type consistency
sheaf.global_gluing_check      # => cross-function compatibility
sheaf.h1_obstructions          # => list of gluing failures
```

## Commands

```bash
# Verify sheaf consistency
just sheaf-check

# Check specific coverage
just sheaf-coverage src/

# Compute cohomology obstructions
just sheaf-h1

# Integration with tree-sitter
just sheaf-ast src/*.clj
```

## API

```ruby
require 'sheaf_cohomology'

# Create verifier
verifier = SheafCohomology::Verifier.new(
  trit: -1,
  coverage_strategy: :ast_boundaries
)

# Add patches from tree-sitter
verifier.add_patches_from_ast(parsed_files)

# Check consistency
result = verifier.verify!
result[:h0]  # Global sections (fully consistent)
result[:h1]  # Gluing obstructions
result[:h2]  # Higher obstructions
result[:gf3_conserved]  # GF(3) sum = 0 with triad
```

## Integration with GF(3) Triads

Forms valid triads with ERGODIC (0) and PLUS (+1) skills:

```
sheaf-cohomology (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ unworld (0) ⊗ rama-gay-clojure (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ glass-bead-game (0) ⊗ rubato-composer (+1) = 0 ✓
```

## Mathematical Foundation

### Čech Complex

```
C⁰ = ∏_i F(U_i)
C¹ = ∏_{i<j} F(U_i ∩ U_j)
C² = ∏_{i<j<k} F(U_i ∩ U_j ∩ U_k)
```

### Differential Maps

```
d⁰: C⁰ → C¹:  (d⁰s)_{ij} = s_j|_{U_ij} - s_i|_{U_ij}
d¹: C¹ → C²:  (d¹g)_{ijk} = g_jk - g_ik + g_ij
```

### Cocycle Condition

```
g ∈ Z¹(U, F) ⟺ d¹g = 0 ⟺ g_ij + g_jk = g_ik on triple overlaps
```

## Example Output

```
─── Sheaf Cohomology Verification ───
Coverage: 5 modules, 8 interfaces, 3 triple overlaps

Local Consistency:
  ✓ module_a ∩ module_b: types compatible
  ✓ module_b ∩ module_c: types compatible
  ✓ module_a ∩ module_c: types compatible

Čech Cohomology:
  H⁰ = 1 (connected components)
  H¹ = 0 (no gluing obstructions)
  H² = 0 (no higher obstructions)

Global Structure: ✓ CONSISTENT
GF(3) Trit: -1 (MINUS/Validator)
```

---

**Skill Name**: sheaf-cohomology
**Type**: Local-to-Global Verification
**Trit**: -1 (MINUS)
**Color**: #2626D8 (Blue)
**GF(3)**: Forms valid triads with ERGODIC + PLUS skills
