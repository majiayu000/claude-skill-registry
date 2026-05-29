---
name: specter-navigator-gadget
description: Unified Specter/Navigator/3-MATCH architecture with bidirectional path compilation
source: Clojure Specter, SpecterACSet.jl, 3-MATCH constraint composition
license: MIT
trit: 0
gf3_triad: "möbius-path-filtering (-1) ⊗ specter-navigator-gadget (0) ⊗ color-envelope-preserving (+1)"
status: Production Ready
---

# Specter Navigator Gadget

## Core Concept

Integration of **Specter** (bidirectional navigation), **Navigator** (compiled path objects), and **3-MATCH** (constraint satisfaction) into a unified system for structure traversal and transformation.

A Navigator is a compiled path expression that can be used for both selecting and transforming values within nested data structures. Each Navigator encodes one or more constraints (Gadgets) from a 3-SAT-like problem space.

## Architecture

### Key Components

**1. Navigator** - Compiled path expressions
```julia
struct Navigator
    path::Vector{NavigationStep}  # Steps in the traversal
    constraints::Vector{Gadget}   # 3-MATCH constraints
    cache_key::UInt64            # Hash for inline caching
end
```

**2. Gadget** - Individual constraint unit
```julia
struct Gadget
    name::String
    predicate::Function           # Selection/filtering predicate
    compose_strategy::Symbol      # :all, :any, :sequential
end
```

**3. Navigation Steps** (various types)
- `ALL` - Navigate to all collection members
- `keypath(key)` - Navigate to dictionary key
- `pred(predicate)` - Filter by predicate
- `SEXP_HEAD` / `sexp_nth(n)` - S-expression navigation
- `INDEX(i)` - Direct indexing

### Compilation Pipeline

```
Path Expression
    ↓
coerce_nav() - converts to Navigator objects
    ↓
Constraint checking - verifies 3-MATCH satisfiability
    ↓
Inline caching via @late_nav / @compiled_select
    ↓
nav_select() / nav_transform() - execution
```

## API

### Macros

**`@late_nav(path_expr)`**
Compiles and caches a navigation path, returning a reusable Navigator:
```julia
nav = @late_nav([ALL, pred(iseven)])
results = nav_select(nav, [1,2,3,4,5], x -> [x])
# => [2, 4]
```

**`@compiled_select(path, structure)`**
Combines compilation, caching, and selection in one call:
```julia
results = @compiled_select([ALL, pred(iseven)], [1,2,3,4,5])
# => [2, 4]
```

### Core Functions

**`coerce_nav(path_expr) :: Navigator`**
Converts a path expression to a compiled Navigator object.

**`nav_select(nav::Navigator, structure, result_fn) :: Vector`**
Selects all values matching the path, applies result_fn to each.

**`nav_transform(nav::Navigator, structure, transform_fn) :: Structure`**
Transforms all values matching the path in-place.

**`compose_navigators(nav1, nav2) :: Navigator`**
Composes two Navigators into one. Verifies 3-MATCH constraint satisfiability.

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| First @late_nav call | O(|path|) | Compilation + caching |
| Subsequent @late_nav | O(1) | Cache lookup |
| nav_select | O(n⋅|path|) | n = structure size, linear in path length |
| Constraint checking | O(m) | m = number of gadgets, linear in constraint count |

## Integration with 3-MATCH

Each path expression can encode constraints that are verifiable via 3-SAT:

```julia
# Constraint 1: values must be even
# Constraint 2: values must be > 2
# Constraint 3: XOR of above (either even or >2, but not both)
nav = @late_nav([ALL, pred(x -> (iseven(x) && x ≤ 2) || (!iseven(x) && x > 2))])
```

The 3-MATCH system can:
- Verify path compositions are satisfiable before execution
- Detect infeasible path combinations early
- Optimize constraint ordering for faster filtering

## Bidirectionality

The same Navigator works for both selection and transformation:

```julia
# Select even numbers
selected = nav_select(nav, [1,2,3,4,5], x -> [x])

# Transform even numbers (multiply by 10)
transformed = nav_transform(nav, [1,2,3,4,5], x -> x * 10)
# => [1, 20, 3, 40, 5]
```

## Caching Strategy

**Global Cache**: `Dict{UInt64, Navigator}()`
- Key: hash(path_expr) - computed at compile time
- Value: compiled Navigator object
- Per-callsite - different code locations maintain separate entries

**Cache Invalidation**: Never (by design)
- Paths are immutable after compilation
- Cache entries are safe indefinitely
- Memory is the only constraint

## Composition with Möbius Filtering

See **möbius-path-filtering** skill for how non-orientable filtering eliminates invalid paths before Navigator compilation.

## Composition with Color Envelopes

See **color-envelope-preserving** skill for how GF(3) color conservation is enforced across Navigator compositions.

## Usage Patterns

### Nested Dictionary Navigation
```julia
data = Dict(
  "users" => [
    Dict("name" => "Alice", "age" => 30, "active" => true),
    Dict("name" => "Bob", "age" => 25, "active" => false)
  ]
)

# Select all active users' names
nav = @late_nav([keypath("users"), ALL, pred(u -> u["active"]), keypath("name")])
active_names = nav_select(nav, data, x -> [x])
# => ["Alice"]
```

### S-expression Navigation
```julia
sexp = :(define (square x) (* x x))

# Navigate to function definition head
nav = @late_nav([sexp_nth(1), SEXP_HEAD])
func_name = nav_select(nav, sexp, x -> [x])
# => :square
```

### Constraint-based Filtering
```julia
# Find numbers that are odd AND greater than 5
nav = @late_nav([
  ALL,
  pred(x -> isodd(x) && x > 5)
])
results = nav_select(nav, [1,3,5,7,9,11], x -> [x])
# => [7, 9, 11]
```

## Error Handling

**InvalidPathError** - Path expression doesn't compile
**UnsatisfiableConstraintError** - 3-MATCH constraints are contradictory
**TypeMismatchError** - Structure doesn't match expected shape for path

## Related Skills

- **möbius-path-filtering** - Eliminates topologically invalid paths
- **color-envelope-preserving** - Maintains GF(3) color invariants
- **three-match** - Core 3-SAT constraint satisfaction engine

## References

- Clojure Specter: https://github.com/redplanetlabs/specter
- SpecterACSet.jl: `/Users/bob/ies/music-topos/lib/specter_acset.jl`
- Inline caching paper: "Just in Time Specialization" - Bolz et al.
