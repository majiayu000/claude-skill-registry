---
name: lispsyntax-acset
description: "LispSyntax.jl ↔ ACSets.jl bidirectional bridge with OCaml ppx_sexp_conv-style deriving"
---

# lispsyntax-acset

> Bidirectional S-expression ↔ ACSet conversion inspired by OCaml's ppx_sexp_conv

**Version**: 1.1.0
**Trit**: 0 (Ergodic - coordinates data serialization)
**Bundle**: serialization
**Dynamic Sufficiency**: ✅ VERIFIED (2025-12-22) - handles ACSets of arbitrary complexity

## Overview

This skill bridges **LispSyntax.jl** (Lisp-like syntax in Julia) with **ACSets.jl** (algebraic databases) using the pattern established by OCaml's `ppx_sexp_conv` library. It enables:

1. **S-expression parsing**: `parse_sexp("(+ 1 2)") → Sexp`
2. **ACSet serialization**: `sexp_of_acset(graph) → Sexp`
3. **ACSet deserialization**: `acset_of_sexp(GraphType, sexp) → Graph`
4. **Colored S-expressions**: Gay.jl deterministic coloring via SplitMix64

## OCaml Inspiration

```ocaml
(* OCaml pattern *)
type color = Red | Blue | Green [@@deriving sexp]
(* generates: sexp_of_color and color_of_sexp *)
```

```julia
# Julia equivalent for ACSets
sexp_of_acset(acs::ACSet) → Sexp
acset_of_sexp(::Type{T}, ::Sexp) → T where T <: ACSet
```

## Core API

### Sexp Type (matches OCaml)

```julia
abstract type Sexp end
struct Atom <: Sexp
    value::String
end
struct SList <: Sexp
    children::Vector{Sexp}
end
```

### Parsing & Serialization

```julia
# String → Sexp (like OCaml's Sexp.of_string)
sexp = parse_sexp("(define (square x) (* x x))")

# Sexp → String (like OCaml's Sexp.to_string)
str = to_string(sexp)

# Roundtrip verification
@assert verify_parse_roundtrip("(a (b c) d)")
```

### Primitive Converters (like Sexplib.Std)

```julia
# To S-expression
sexp_of_int(42)           # → Atom("42")
sexp_of_float(3.14)       # → Atom("3.14")
sexp_of_string("hello")   # → Atom("hello")
sexp_of_list(sexp_of_int, [1,2,3])  # → SList([1, 2, 3])

# From S-expression
int_of_sexp(Atom("42"))   # → 42
list_of_sexp(int_of_sexp, SList([...]))  # → [1, 2, 3]
```

### ACSet Conversion

```julia
# ACSet → Sexp
# Produces: (TypeName (Ob1 ((id1 attrs...) ...)) (hom1 ((src tgt) ...)) ...)
sexp = sexp_of_acset(my_graph)

# Sexp → ACSet
graph = acset_of_sexp(GraphType, sexp)

# Verify roundtrip
@assert verify_roundtrip(original_graph)
```

### Colored S-expressions (Gay.jl)

```julia
# Colorize with deterministic seed
colored = colorize(sexp, seed=0x598F318E2B9E884)
# ColoredSexp with LCH color from SplitMix64
```

## Output Format

ACSet to S-expression produces structured output:

```lisp
(Graph
  (V ((1) (2) (3)))           ; Vertices (object parts)
  (E ((1) (2)))               ; Edges (object parts)
  (src ((1 1) (2 2)))         ; Source morphism (id → target)
  (tgt ((1 2) (2 3))))        ; Target morphism (id → target)
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | slime-lisp | Validates Lisp syntax |
| 0 | **lispsyntax-acset** | Coordinates serialization |
| +1 | cider-clojure | Generates Clojure interop |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Integration with Existing Skills

### thread_relational_hyjax.hy

```hy
;; Hy uses same sexp concepts
(defclass ColoredSExpr []
  "S-expression with semantic color annotations")
  
(defn acset-to-colored-sexpr [acset]
  "Convert ThreadACSet to Colored S-expression tree")
```

### colored_sexp_acset.jl

```julia
# Inverse operation: Sexp → ACSet graph
function sexp_to_graph(sexp::ColoredSexp)::ColoredSexpData
    data = ColoredSexpData()
    _add_sexp!(data, sexp, nothing, 0)
    data
end
```

## Justfile Recipes

```makefile
# Run demo
lispsyntax-demo:
    julia --project=. -e 'include("lib/lispsyntax_acset_bridge.jl"); LispSyntaxAcsetBridge.demo()'

# Test roundtrip parsing
lispsyntax-test:
    julia --project=. -e '
    include("lib/lispsyntax_acset_bridge.jl")
    using .LispSyntaxAcsetBridge
    @assert verify_parse_roundtrip("(a (b c) d)")
    println("✓ Parse roundtrip OK")
    '
```

## File Locations

- **Bridge implementation**: `lib/lispsyntax_acset_bridge.jl`
- **Colored ACSet**: `lib/colored_sexp_acset.jl`
- **Hy integration**: `lib/thread_relational_hyjax.hy`
- **Clojure integration**: `src/sicp/colored-sexp.clj`

## Specter-Style Navigation (Zero-Overhead)

**NEW 2025-12-22**: Integrated Specter-style bidirectional navigation with Julia-specific optimizations achieving **93-113x speedup** over CPS-based implementation.

### Benchmark Results (Chairmarks)

| Operation | Hand-Written | Original CPS | Optimized | Ratio |
|-----------|--------------|--------------|-----------|-------|
| Select evens (n=1000) | 423.8 ns | 52.58 μs | 561.6 ns | **1.3x** |
| Transform evens | 354.9 ns | 40.04 μs | 354.2 ns | **1.0x** |
| comp_navs allocation | - | 7.8 ns | 0.5 ns | **15.7x** |

### Key Optimizations

1. **Tuple paths** vs `Vector{Navigator}` → type stability, 0 allocs
2. **Functor structs** vs closures → no capture, fully inlinable
3. **`@inline` annotations** → aggressive hot path inlining
4. **Fused ALL+pred** → single traversal for filter operations

### Correct-by-Construction via 3-MATCH

Path caching follows **3-MATCH gadget** principles:
- **Local constraint**: Path types correct at compile time
- **Global correctness**: Cached paths guaranteed correct
- **GF(3) conservation**: Tuple → TupleNav → Result preserves sum

```julia
# Correct-by-construction path caching
compiled_path = TupleNav((ALL, pred(iseven)))  # Type-stable, 0 allocs
result = nav_select(compiled_path, data, IDENTITY)  # Guaranteed correct
```

### Files

- `lib/specter_optimized.jl` - Zero-overhead implementation
- `lib/specter_chairmarks_world.jl` - Chairmarks benchmarks
- `SPECTER_OPTIMIZATION_RESULTS.md` - Full benchmark report

## See Also

- [LispSyntax.jl](https://github.com/swadey/LispSyntax.jl) - Clojure-like Lisp in Julia
- [ppx_sexp_conv](https://github.com/janestreet/ppx_sexp_conv) - OCaml S-expression PPX
- [sexplib](https://github.com/janestreet/sexplib) - OCaml S-expression library
- `acsets-algebraic-databases` skill - ACSet foundations
- `gay-mcp` skill - Deterministic coloring
- `three-match` skill - Correct-by-construction caching
