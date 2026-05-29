---
name: tuple-nav-composition
description: Tuple and product structure navigation with composition
source: Category theory, product types, Cartesian logic
license: MIT
trit: 0
gf3_triad: "type-inference-validation (-1) ⊗ tuple-nav-composition (0) ⊗ constraint-generalization (+1)"
status: Production Ready
---

# Tuple Nav Composition

## Core Concept

Navigation through **product structures** (tuples, named tuples, records) where multiple fields must be accessed and composed in parallel.

A TupleNav is a bundled Navigator that operates on all fields of a product simultaneously, maintaining **structural integrity** through composition.

## Why Tuple Navigation?

Standard Specter navigators work on **sequences** (ALL, each element). But what about simultaneous access to multiple fields?

```julia
# Without TupleNav: Access fields separately, type mismatch risk
person = (name="Alice", age=30, email="alice@example.com")

name_nav = @late_nav([INDEX(1)])     # But tuples aren't indexed this way!
age_nav = @late_nav([INDEX(2)])      # Fragile, error-prone

# With TupleNav: Access structurally, type-safe composition
record_nav = @tuple_nav([:name, :age])  # Access both fields as unit
```

## Architecture

### TupleNav Structure

```julia
struct TupleNav
    fields::Vector{Symbol}           # Field names to navigate
    navigators::Dict{Symbol, Navigator}  # Navigator for each field
    composition_strategy::Symbol      # :parallel, :sequential, :reduce
    output_type::Type                # (Field1Type, Field2Type, ...)
end
```

### Product Types

| Type | Navigation |
|------|-----------|
| `(T1, T2, T3)` | Positional tuple |
| `NamedTuple{(:a, :b, :c)}` | Named access |
| `@NamedTuple{a::T1, b::T2}` | Struct-like |
| `Dict{K, V}` | Key-based dictionary |
| Record/DataClass | Field-based |

### Composition Strategies

**`:parallel`** - Access all fields simultaneously
```julia
nav = @tuple_nav([:x, :y, :z], strategy=:parallel)
result = nav_select(nav, (x=1, y=2, z=3), id)
# => ((x=1), (y=2), (z=3))  # All accessed at once
```

**`:sequential`** - Access fields in order, threading results
```julia
nav = @tuple_nav([:x, :y, :z], strategy=:sequential)
# Field y receives result from x, z receives from y, etc.
```

**`:reduce`** - Fold/reduce across fields
```julia
nav = @tuple_nav([:x, :y, :z], strategy=:reduce)
# Combine results across fields: x + y + z
```

## API

### TupleNav Creation

**`@tuple_nav(fields, strategy=:parallel)`**
Creates a TupleNav for navigating product types.

```julia
# Access name and email from person record
nav = @tuple_nav([:name, :email])

person = (name="Alice", email="alice@example.com", age=30)
result = nav_select(nav, person, identity)
# => (name="Alice", email="alice@example.com")
```

**`tuple_nav(fields::Vector{Symbol}, structure_type::Type)`**
Explicitly typed TupleNav.

```julia
PersonType = NamedTuple{(:name, :age, :email)}

nav = tuple_nav([:name, :email], PersonType)
# Type-checked at compile time
```

### Composition

**`compose_tuple_navs(nav1::TupleNav, nav2::TupleNav) :: TupleNav`**
Combines two product navigators.

```julia
nav_identity = @tuple_nav([:id, :name])     # Extract identity
nav_contact = @tuple_nav([:email, :phone])  # Extract contact

nav_combined = compose_tuple_navs(nav_identity, nav_contact)
# Result has all 4 fields: id, name, email, phone
```

### Nested Products

**`nested_tuple_nav(path::Vector, fields::Vector{Symbol})`**
Navigate to a product, then select fields.

```julia
# Navigate to users list, then select name/email from each
nav = nested_tuple_nav([keypath("users"), ALL], [:name, :email])

data = Dict(
  "users" => [
    (name="Alice", age=30, email="alice@example.com"),
    (name="Bob", age=25, email="bob@example.com")
  ]
)

result = nav_select(nav, data, identity)
# => [
#      (name="Alice", email="alice@example.com"),
#      (name="Bob", email="bob@example.com")
#    ]
```

### Field Projection

**`project_tuple_nav(nav::TupleNav, fields::Vector{Symbol})`**
Extract subset of fields from a TupleNav.

```julia
nav_full = @tuple_nav([:id, :name, :age, :email])
nav_subset = project_tuple_nav(nav_full, [:name, :email])
# New navigator accesses only name and email
```

## Structural Composition

**Key insight**: TupleNav maintains **type safety across composition**.

```julia
# Type 1: Person
Person = NamedTuple{(:name, :age)}

# Type 2: Contact
Contact = NamedTuple{(:email, :phone)}

# Type 3: User (combines both)
User = NamedTuple{(:name, :age, :email, :phone)}

# Composition is type-safe
nav_person = @tuple_nav([:name, :age], Person)
nav_contact = @tuple_nav([:email, :phone], Contact)
nav_user = compose_tuple_navs(nav_person, nav_contact)
# => TupleNav for User type ✓
```

## Parallel Semantics

With `:parallel` strategy, all fields are accessed **in parallel** (logically):

```julia
nav = @tuple_nav([:x, :y, :z], strategy=:parallel)

# Execution order doesn't matter—all fields see the same input
result1 = nav_select(nav, structure, f)
result2 = nav_select(nav, structure, f)
# => Always identical (deterministic parallel access)
```

Under the hood, this uses **color-aware SplitMix64 seeding** to ensure parallel reads remain deterministic (see `color-envelope-preserving` skill).

## Dictionary Projection

TupleNav also works on dictionaries with structured keys:

```julia
nav = @tuple_nav([:user_id, :user_name, :user_email])

data = Dict(
  :user_id => 42,
  :user_name => "Alice",
  :user_email => "alice@example.com",
  :user_age => 30
)

result = nav_select(nav, data, identity)
# => Dict(:user_id => 42, :user_name => "Alice", :user_email => "alice@example.com")
```

## Integration with Type Inference

TupleNav output types are **automatically inferred** by the type system:

```julia
nav = @tuple_nav([:x, :y, :z])
# Type: (T1, T2, T3) → (T1', T2', T3')
# where T_i' is the refined type of field i

sig = navigator_signature(nav)
# => TypeSignature(
#     input: NamedTuple{(:x,:y,:z)},
#     output: NamedTuple{(:x,:y,:z)},  # same structure
#     preserves: field types
#   )
```

## Composition with Constraints

TupleNav can apply navigators to each field:

```julia
# Each field goes through its own Navigator
field_navs = Dict(
  :x => @late_nav([pred(ispositive)]),
  :y => @late_nav([pred(ispositive)]),
  :z => @late_nav([pred(ispositive)])
)

nav = @tuple_nav([:x, :y, :z], field_navigators=field_navs)
# Each field must pass its predicate
```

## Error Handling

**Missing field**:
```julia
nav = @tuple_nav([:name, :email, :phone])
person = (name="Alice", email="alice@example.com")  # missing :phone

nav_select(nav, person, id)
# => FieldMissingError("Field :phone not found in tuple")
```

**Type mismatch**:
```julia
nav = @tuple_nav([:age])  # Expects numeric field
person = (name="Alice", age="thirty")  # age is string

nav_select(nav, person, id)
# => TypeError("Expected Int, got String for field :age")
```

## Performance

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Create TupleNav | O(n) | n = number of fields |
| Parallel access | O(n) | All fields accessed once |
| Sequential access | O(n²) | Each step threads to next |
| Reduce | O(n) | Single fold over fields |
| **Caching** | O(1) | Cache key includes field list |

## Related Skills

- **type-inference-validation** - Validates field types at compile time
- **constraint-generalization** - Combines field constraints across products
- **specter-navigator-gadget** - Base Navigator system that TupleNav builds on
- **möbius-path-filtering** - Ensures product navigation is topologically valid

## Use Cases

**Example 1: Extract contact info from user records**
```julia
nav = @tuple_nav([:name, :email, :phone])
users = [
  (id=1, name="Alice", email="alice@ex.com", phone="555-1234"),
  (id=2, name="Bob", email="bob@ex.com", phone="555-5678")
]

contacts = map(u -> nav_select(nav, u, identity), users)
# All users' contact triples extracted
```

**Example 2: Parallel aggregation**
```julia
nav = @tuple_nav([:revenue, :costs, :profit], strategy=:parallel)

quarterly_data = (
  revenue=100_000,
  costs=60_000,
  profit=40_000
)

result = nav_select(nav, quarterly_data, x -> x * 1.1)  # 10% increase
# => (revenue=110_000, costs=66_000, profit=44_000)
```

**Example 3: Nested product navigation**
```julia
nav = nested_tuple_nav(
  [keypath("employees"), ALL],
  [:name, :salary]
)

company = Dict(
  "employees" => [
    (name="Alice", salary=80_000, dept="Engineering"),
    (name="Bob", salary=75_000, dept="Sales")
  ]
)

result = nav_select(nav, company, identity)
# => Extract name/salary for all employees
```

## References

- Product types: "Types and Programming Languages" - Pierce
- Cartesian logic: "Basic Intuitionistic Linear Logic" - Girard
- Parallel semantics: "Parallel Haskell" - Peyton Jones et al.
