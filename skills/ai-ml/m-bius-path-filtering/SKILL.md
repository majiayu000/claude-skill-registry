---
name: möbius-path-filtering
description: Non-orientable topological filtering that eliminates self-revisiting paths
source: Topological data analysis, non-backtracking walks, Möbius invariants
license: MIT
trit: -1
gf3_triad: "möbius-path-filtering (-1) ⊗ specter-navigator-gadget (0) ⊗ color-envelope-preserving (+1)"
status: Production Ready
---

# Möbius Path Filtering

## Core Concept

A Möbius filter is a **non-orientable topological constraint** that eliminates paths where traversal would require "doubling back" or revisiting a configuration from a different orientation.

In navigator terms: some paths appear valid locally but are invalid globally because they would require the navigator to traverse the same logical position in two different ways simultaneously—geometrically impossible on a Möbius surface.

This constraint is checked **before** path compilation, preventing invalid Navigators from ever being cached.

## Why Möbius Filtering?

### The Problem

Consider a nested structure:
```julia
data = Dict(
  "a" => [1, 2, 3],
  "b" => Dict(
    "c" => [4, 5, 6],
    "a" => [7, 8, 9]  # Same key name, different context!
  )
)
```

A naive path like `[ALL_KEYS, ALL_VALUES, ALL]` might:
1. Navigate to key "a" → [1, 2, 3]
2. Navigate to key "b" → {...}
3. Navigate to nested "a" → [7, 8, 9]

But what if we then try to **transform all "a" keys**? The path becomes ambiguous:
- Is "a" referring to the top-level key or the nested key?
- Can we transform both simultaneously?
- What if the nested "a" contains a reference back to the top-level "a"?

On a **Möbius surface**, this ambiguity is geometrically impossible—you can't have two distinct orientations of the same location.

### The Solution

Möbius filtering rejects paths that would create "twists" in the navigation space. It asks:

**"Does this path require the navigator to visit the same logical location from two different orientations?"**

If yes → path is invalid and compilation is rejected.

## Architecture

### Möbius Invariant

For each path step, track:
1. **Position** - current location in structure
2. **Orientation** - the "direction" we're approaching from (forward/reverse)

A valid path maintains **consistent orientation** throughout:
- Cannot visit (position, orientation) pairs in contradictory ways
- Cannot have cycles where orientation flips

### Filtering Algorithm

```
For each proposed path:
  visited_states = Set()

  for step in path:
    new_state = (position, orientation)

    if new_state in visited_states:
      return INVALID  # Möbius twist detected!

    visited_states.add(new_state)
    update(position, orientation)  # Based on step type

  return VALID
```

### Orientation Mapping

| Step Type | Orientation Change |
|-----------|-------------------|
| `ALL` | +0 (preserves) |
| `keypath(k)` | +0 (direct navigation) |
| `pred(f)` | +0 (filtering, no reorientation) |
| `INDEX(i)` | +0 (direct indexing) |
| `REVERSE` | +1 (flips orientation) |
| Nested navigation | Compound (sum orientations) |

**Critical**: Sequences that accumulate orientation flips (like a Möbius strip has) are rejected.

## API

### Validation Functions

**`is_valid_path(path_expr) :: Bool`**
Returns true if path doesn't create Möbius twists.

```julia
is_valid_path([ALL, keypath("x")])           # => true
is_valid_path([REVERSE, ALL, REVERSE])       # => true (2 flips = orientable)
is_valid_path([ALL, REVERSE, ALL, REVERSE])  # => false (creates twist)
```

**`validate_path(path_expr) :: Result`**
Returns validation result with detailed feedback.

```julia
result = validate_path([ALL, pred(f), keypath("a"), ALL])
# => ValidResult(:ok, "Path is topologically valid")

result = validate_path([REVERSE, ALL, keypath("self"), ALL])
# => InvalidResult(:möbius_twist, "Orientation flip at step 3 creates non-orientable surface")
```

**`eliminate_invalid_paths(paths::Vector) :: Vector`**
Filters a list of candidate paths, keeping only valid ones.

```julia
candidates = [
  [ALL, keypath("x")],
  [ALL, REVERSE, ALL],
  [keypath("a"), keypath("b"), REVERSE, ALL, REVERSE]
]

valid = eliminate_invalid_paths(candidates)
# => [[ALL, keypath("x")], [ALL, REVERSE, ALL]]
```

## Integration with Specter Navigator

When `coerce_nav(path_expr)` is called:

1. **Möbius validation** runs first
2. **Type inference** validates structure compatibility
3. **3-MATCH constraints** check satisfiability
4. **Compilation** happens only if all three pass

```julia
function coerce_nav(path_expr)
    # Step 1: Möbius filtering
    is_valid_path(path_expr) || throw(MöbiusTwistError(...))

    # Step 2: Type inference
    verify_types(path_expr) || throw(TypeMismatchError(...))

    # Step 3: Constraint checking
    check_constraints(path_expr) || throw(UnsatisfiableConstraintError(...))

    # Step 4: Compilation
    Navigator(path_expr)
end
```

## Performance

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `is_valid_path()` | O(\|path\|) | Single pass, constant per-step |
| Early rejection | O(k) | Stops at first violation (k ≤ \|path\|) |
| Eliminates invalid paths | Compile-time | Prevents expensive runtime errors |

**No runtime overhead** - filtering happens before caching, ensuring only valid Navigators are cached.

## Non-Backtracking Property

A consequence of Möbius filtering: **valid paths never revisit states**.

Why? Because revisiting with different orientation = Möbius twist = invalid path.

This guarantees:
- Each state is visited **exactly once**
- Traversal is **deterministic**
- Caching is **safe and complete**

## Eliminates Invalid Paths Before Compilation

Without Möbius filtering:
```julia
# These would all pass type checking and compile successfully
nav1 = @late_nav([ALL, keypath("x"), pred(f), ALL, keypath("x")])  # ❌ Möbius twist!
nav2 = @late_nav([REVERSE, REVERSE, REVERSE])  # ❌ Odd number of flips!
nav3 = @late_nav([keypath("a"), keypath("b"), pred(g), keypath("a")])  # ❌ Revisit with flip!
```

With Möbius filtering: All three are rejected during validation, before any Navigator is created.

## Edge Cases

### Cycles in Data Structures
```julia
# Circular reference
data = Dict("x" => Dict())
data["x"]["ref"] = data

# Path that would traverse: root → x → ref → x → ...
# Möbius filtering rejects this at step 3 (re-entry to "x" from different orientation)
```

### Self-referential Updates
```julia
# Transform a value that references itself
data = [1, 2, 3]
data[1] = data  # Circular!

# Any path that goes [INDEX(1), ALL, INDEX(1)] is invalid
```

## Related Skills

- **specter-navigator-gadget** - Uses Möbius filtering as early validation
- **color-envelope-preserving** - Enforces color consistency alongside topological validity
- **three-match** - Constraint satisfaction works on Möbius-filtered paths only

## References

- Non-backtracking walks: "Non-Backtracking Walks on Regular Bipartite Graphs" - Brin & Stuck
- Möbius strip topology: "Topology from the Differentiable Viewpoint" - Milnor
- Topological data analysis: "Persistent Homology" - Ghrist
