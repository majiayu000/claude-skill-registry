---
name: constraint-generalization
description: Generalization and composition of constraints across navigators
source: Constraint logic programming, constraint satisfaction, abstract interpretation
license: MIT
trit: +1
gf3_triad: "type-inference-validation (-1) ⊗ tuple-nav-composition (0) ⊗ constraint-generalization (+1)"
status: Production Ready
---

# Constraint Generalization

## Core Concept

Given proven constraints on individual paths, **synthesize new constraints** that hold across composed paths. This skill moves from "validation" (rejecting bad paths) to "generation" (creating better paths).

Example: If path A proves outputs are even, and path B proves outputs are positive, the **composed path AB proves outputs are both even AND positive**.

## Why Constraint Generalization?

Without it, constraints are lost during composition:

```julia
nav_even = @late_nav([ALL, pred(iseven)])      # proves: even
nav_positive = @late_nav([ALL, pred(x > 0)])   # proves: positive

# Compose them:
nav_composed = compose_navigators(nav_even, nav_positive)
# What can we prove about the result?
# Without generalization: nothing! Constraints are forgotten.

# With generalization:
# => Proves: even(x) ∧ positive(x)
# => More refined type: EvenPositiveInt
```

This **refinement typing** enables:
- **Automatic constraint propagation** downstream
- **Fewer re-checks** (prove once, use many times)
- **Smarter composition** (know which paths can combine)
- **Proof generation** (formal certificates for constraints)

## Architecture

### Constraint Representation

```julia
struct Constraint
    predicate::Function           # The boolean test
    name::Symbol                  # :even, :positive, :non_null, ...
    arity::Int                    # 1 for unary, 2 for binary, etc.
    proof::Proof                  # Evidence constraint holds
    refinement_type::RefinementType  # Int → EvenInt
end
```

### Constraint Composition

**CNF (Conjunctive Normal Form)** for constraint composition:

```
C₁ ∧ C₂ ∧ C₃ = (iseven AND positive AND nonzero)

Satisfiable? Check via 3-MATCH:
  - Find x where iseven(x) ∧ positive(x) ∧ nonzero(x)
  - If no x exists → constraints are contradictory
  - If x exists → constraints compose validly
```

### Constraint Lattice

```
        ⊤ (True, no constraint)
       / \
    even  odd
     / \   / \
    ... ∧ ... (conjunctions)
     \ /   \ /
     ⊥ (False, unsatisfiable)
```

Generalization works upward in this lattice: from specific constraints to general ones.

## API

### Constraint Extraction

**`extract_constraints(navigator::Navigator) :: Vector{Constraint}`**
Pulls constraints from a compiled Navigator.

```julia
nav = @late_nav([ALL, pred(x -> iseven(x) && x > 0)])
constraints = extract_constraints(nav)
# => [
#      Constraint(:even, iseven, proof=...),
#      Constraint(:positive, x > 0, proof=...)
#    ]
```

**`named_constraint(name::Symbol, predicate::Function) :: Constraint`**
Creates a named, reusable constraint.

```julia
constraint_even = named_constraint(:even, iseven)
constraint_gt5 = named_constraint(:gt5, x -> x > 5)
constraint_string = named_constraint(:string, x -> isa(x, String))
```

### Constraint Composition

**`compose_constraints(c1::Constraint, c2::Constraint) :: ComposedConstraint`**
Combines two constraints, proving they're satisfiable together.

```julia
c_even = named_constraint(:even, iseven)
c_positive = named_constraint(:positive, x > 0)

c_composed = compose_constraints(c_even, c_positive)
# => ComposedConstraint(
#     name: :even_and_positive,
#     predicate: x -> iseven(x) && x > 0,
#     proof: (satisfiable evidence),
#     refinement_type: EvenPositiveInt
#   )
```

**`compose_constraints(constraints::Vector) :: ComposedConstraint`**
Composes multiple constraints at once.

```julia
constraints = [
  named_constraint(:even, iseven),
  named_constraint(:gt5, x -> x > 5),
  named_constraint(:lt100, x -> x < 100)
]

composed = compose_constraints(constraints)
# => Constraint proven satisfiable for ints in [6, 8, 10, ..., 98]
```

### Constraint Generalization

**`generalize_constraint(constraint::Constraint) :: GeneralConstraint`**
Finds the most general constraint that subsumes the given one.

```julia
c_eq42 = named_constraint(:eq42, x -> x == 42)
general = generalize_constraint(c_eq42)
# => :positive (42 is positive—more general)
# => Or :nonzero, :nonnegative, etc. (depending on strategy)
```

**`abstract_constraint(constraint::Constraint, level::Int) :: GeneralConstraint`**
Applies abstract interpretation to weaken constraints.

```julia
c_detailed = named_constraint(:detailed, x -> iseven(x) && x > 5 && x < 100)

abstract_constraint(c_detailed, 1)  # Weaken slightly
# => iseven(x) && x > 5

abstract_constraint(c_detailed, 2)  # Weaken more
# => iseven(x)

abstract_constraint(c_detailed, 3)  # Very weak
# => numeric(x)  # Only knows it's a number
```

### Refinement Types

**`refine_type(base_type::Type, constraint::Constraint) :: RefinementType`**
Creates a refined type with proven constraint.

```julia
refine_type(Int, named_constraint(:even, iseven))
# => RefinementType(Int, :even)
# Meaning: "An Int that is proven even"

refine_type(String, named_constraint(:nonempty, x -> length(x) > 0))
# => RefinementType(String, :nonempty)
# Meaning: "A String that is proven non-empty"
```

### Proof Certificates

**`generate_proof(constraint::Constraint) :: ProofCertificate`**
Creates a formal proof that the constraint is satisfiable.

```julia
c = named_constraint(:even_positive, x -> iseven(x) && x > 0)
proof = generate_proof(c)
# => ProofCertificate(
#     constraint: c,
#     witnesses: [2, 4, 6, 8, ...],  # Examples that satisfy
#     satisfiability: SAT,             # Satisfiable
#     hardness: #P,                    # Complexity class
#     explanation: "Constraint is satisfiable; even positive integers exist"
#   )
```

## Constraint Propagation

Once constraints are proven, they propagate through compositions:

```
Path A: X → even(X)
Path B: Y → positive(Y)

Compose A then B:
  => even(X) ∧ positive(Y)
  => If Y = A(X), then: positive(even(X))
  => Generalization: IntegersEvenAndPositive type

Compose again with Path C:
Path C: Z → Z < 100

  => even(X) ∧ positive(Y) ∧ (Y < 100)
  => Refines to: {2, 4, 6, ..., 98}
```

## Integration with 3-MATCH

Constraint composition uses 3-MATCH for satisfiability:

```julia
constraints = [
  :even,        # iseven(x)
  :positive,    # x > 0
  :lt100        # x < 100
]

# 3-MATCH checks:
# Satisfiable? (iseven(x) ∧ x > 0 ∧ x < 100)
# => YES: x ∈ {2, 4, 6, ..., 98}

# If constraints were contradictory:
constraints_bad = [:even, :odd]  # Can't be both!
# => 3-MATCH: UNSAT
# => Reject composition
```

## Integration with Type Inference

Refined types emerge from constraint composition:

```julia
nav = @late_nav([ALL, pred(x -> iseven(x) && x > 0)])

# Type inference sees:
# Input: Vector{Int}
# Constraints: [even, positive]
# Output type: Vector{EvenPositiveInt}  ← Refined!

sig = navigator_signature(nav)
# => TypeSignature(
#     input: Vector{Int},
#     output: Vector{EvenPositiveInt},  # Refined output type!
#     constraints: [even, positive],
#     proof: ...
#   )
```

## Constraint Algebra

Constraints form an **algebraic structure** under generalization:

```
Lattice operations:
  even ∧ positive = even_positive    (Meet/AND)
  even ∨ positive = numeric           (Join/OR, generalize)
  ¬even = odd                         (Complement)
  ⊤ = True                           (Top, no constraint)
  ⊥ = False                          (Bottom, unsatisfiable)

Example derivations:
  even ∧ positive → nonnegative  (generalization)
  odd ∧ gt5 → numeric            (upper bound)
  string ∧ nonempty → string     (redundant, but valid)
```

## Practical Examples

### Example 1: Filtering Pipeline
```julia
# Stage 1: Filter for positive numbers
nav1 = @late_nav([ALL, pred(x -> x > 0)])
constraints1 = extract_constraints(nav1)
# => [:positive]

# Stage 2: Further filter for even
nav2 = @late_nav([ALL, pred(iseven)])
constraints2 = extract_constraints(nav2)
# => [:even]

# Compose stages
final_constraints = compose_constraints(
  constraints1[1],
  constraints2[1]
)
# => Constraint(:even_positive, x -> iseven(x) && x > 0)

# Proof:
proof = generate_proof(final_constraints)
# => Witnesses: [2, 4, 6, 8, ...]
```

### Example 2: Product Navigation with Constraints
```julia
# Navigate to (x, y) pairs where x is positive and y is negative
nav = @tuple_nav([:x, :y])

constraints = compose_constraints([
  named_constraint(:x_positive, px -> px > 0),
  named_constraint(:y_negative, py -> py < 0)
])

# Refined output type: Tuple{PositiveInt, NegativeInt}
```

### Example 3: Iterative Constraint Refinement
```julia
# Start with loose constraint
c1 = named_constraint(:numeric, x -> isnumeric(x))

# Refine iteratively
c2 = compose_constraints(c1, named_constraint(:positive, x -> x > 0))
# => numeric ∧ positive = positive

c3 = compose_constraints(c2, named_constraint(:even, iseven))
# => positive ∧ even = even_positive

c4 = compose_constraints(c3, named_constraint(:lt100, x -> x < 100))
# => even_positive ∧ lt100 = {2, 4, 6, ..., 98}
```

## Error Handling

**Unsatisfiable constraints**:
```julia
c_even = named_constraint(:even, iseven)
c_odd = named_constraint(:odd, isodd)

compose_constraints(c_even, c_odd)
# => UnsatisfiableConstraintError("No integer is both even and odd")
```

**Type conflicts**:
```julia
c_string = named_constraint(:string, x -> isa(x, String))
c_numeric = named_constraint(:numeric, x -> isnumeric(x))

compose_constraints(c_string, c_numeric)
# => TypeError("String and Numeric constraints are disjoint")
```

## Performance

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| extract_constraints | O(n) | n = path length |
| compose_constraints | O(m³) | m = number of constraints (SAT checking) |
| generalize_constraint | O(1) | Pre-computed lattice |
| refine_type | O(1) | Type annotation |
| generate_proof | O(2^m) | SAT solver on constraint space |

Note: Proof generation is expensive but cached—proofs are reused.

## Related Skills

- **type-inference-validation** - Proves constraint satisfiability
- **tuple-nav-composition** - Applies generalized constraints to products
- **specter-navigator-gadget** - Navigator system that uses constraints
- **three-match** - Underlying SAT solver for constraint composition
- **color-envelope-preserving** - Maintains GF(3) along with constraints

## References

- Constraint logic programming: "Introduction to CLP" - Jaffar & Maher
- Refinement types: "Refinement Types for TypeScript" - Rondon et al.
- Abstract interpretation: "The Cousot-Cousot Approach to Program Analysis" - Cousot
- Proof assistants: "Formal Proof Assistants" - Coq/Isabelle documentation
