---
name: oxcaml
description: Working with the OxCaml extensions to OCaml. Use when the oxcaml compiler is available and you need high-performance, unboxing, stack allocation, data-race-free parallelism
license: ISC
---

You are writing code for the OxCaml compiler, a performance-focused fork of
OCaml with Jane Street extensions. This guide covers OxCaml-specific features.
You should already know standard OCaml.

## Detailed Guides

For in-depth coverage of each feature, see:

| Feature | Guide |
|---------|-------|
| **Modes** (local, unique, once, portable, contended) | [SKILL-MODES.md](SKILL-MODES.md) |
| **Stack Allocation** (local_, stack_, exclave_) | [SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) |
| **Unboxed Types** (float#, int32#, mixed blocks) | [SKILL-UNBOXED.md](SKILL-UNBOXED.md) |
| **Kinds** (value, float64, bits32, kind products) | [SKILL-KINDS.md](SKILL-KINDS.md) |
| **Uniqueness** (unique/aliased, once/many) | [SKILL-UNIQUENESS.md](SKILL-UNIQUENESS.md) |
| **Comprehensions** (list/array builders) | [SKILL-COMPREHENSIONS.md](SKILL-COMPREHENSIONS.md) |
| **SIMD** (vector types, SSE/AVX intrinsics) | [SKILL-SIMD.md](SKILL-SIMD.md) |
| **Templates** (ppx_template, mangling) | [SKILL-TEMPLATES.md](SKILL-TEMPLATES.md) |
| **Zero-Alloc** ([@zero_alloc] checking) | [SKILL-ZERO-ALLOC.md](SKILL-ZERO-ALLOC.md) |
| **Base Library** (OxCaml extensions) | [SKILL-BASE.md](SKILL-BASE.md) |
| **Core Library** (OxCaml extensions) | [SKILL-CORE.md](SKILL-CORE.md) |

---

## Quick Reference: Syntax Cheat Sheet

```ocaml
(* Stack allocation *)
let f () = exclave_ stack_ (1, 2)      (* allocate on stack, return local *)
let g (x @ local) = ...                 (* local parameter *)

(* Unboxed types *)
let x : float# = #3.14                  (* unboxed float *)
let y : int32# = #42l                   (* unboxed int32 *)
type t = { a : int; b : float# }        (* mixed block record *)

(* Modes on values *)
let f (x @ local unique once) = ...     (* multiple modes *)
val g : t @ global -> t @ local         (* in signatures *)

(* Kinds on types *)
type ('a : float64) t = ...             (* kind annotation *)
val f : ('a : value). 'a -> 'a          (* kind-polymorphic *)

(* Comprehensions *)
[ x * 2 for x = 1 to 10 when x mod 2 = 0 ]
[| y for y in arr when y > 0 |]

(* Labeled tuples *)
let pair = ~x:1, ~y:2                   (* labeled tuple *)
let ~x, ~y = pair                       (* destructuring *)

(* Immutable arrays *)
let arr : int iarray = [: 1; 2; 3 :]
let x = arr.:(0)

(* Unboxed tuple destructuring - use #(...) pattern *)
let #(a, b) = some_unboxed_pair
let #(x, y, z) = fork_join3 par f1 f2 f3

(* Zero-alloc annotation *)
let[@zero_alloc] fast_add x y = x + y
```

---

## 1. Modes

Modes track runtime properties of values. Each mode axis is independent.

### Mode Axes

| Axis | Values | Default | Purpose |
|------|--------|---------|---------|
| Locality | `local`, `global` | `global` | Where value lives (stack vs heap) |
| Uniqueness | `unique`, `aliased` | `aliased` | Number of references |
| Linearity | `once`, `many` | `many` | How often closures can be called |
| Portability | `portable`, `shareable`, `nonportable` | `nonportable` | Cross-thread safety |
| Contention | `contended`, `shared`, `uncontended` | `uncontended` | Thread access patterns |

### Syntax

```ocaml
(* On parameters *)
let f (x @ local) = ...
let f (x @ local unique) = ...       (* multiple modes *)

(* On return types in signatures *)
val f : t @ local -> t @ global
val g : t @ unique once -> t @ aliased many

(* On expressions *)
let x = (expr : t @ local)

(* On let bindings *)
let local_ x = ...                    (* shorthand for local *)
let global_ x = ...

(* On record fields - modalities *)
type t = {
  global_ data : int;                 (* always global *)
  mutable x : int @@ aliased;         (* aliased modality *)
}
```

### Subtyping Rules

More restrictive modes can be used where less restrictive are expected:
- `local` ≤ `global` (can use local where global expected? NO - reversed)
- `global` ≤ `local` (can use global where local expected)
- `unique` ≤ `aliased` (can use unique where aliased expected)
- `many` ≤ `once` (can use many where once expected)
- `portable` ≤ `shareable` ≤ `nonportable`
- `uncontended` ≤ `shared` ≤ `contended`

---

## 2. Stack Allocation (Locality)

Stack-allocated values avoid GC overhead but cannot escape their scope.

### Key Constructs

```ocaml
(* Allocate on stack *)
let f () =
  let local_ x = (1, 2) in            (* stack-allocated tuple *)
  ...

(* Force stack allocation *)
let f () =
  stack_ (1, 2)                        (* explicitly stack-allocate *)

(* Return local value from function *)
let f () = exclave_
  stack_ (1, 2)                        (* return value allocated in caller's frame *)

(* Combined pattern for local returns *)
let f () = exclave_ stack_ (make_tuple ())
```

### Rules

1. Local values CANNOT escape their defining scope (no storing in globals, no returning without `exclave_`)
2. Local values CAN reference global values
3. Global values CANNOT reference local values
4. `exclave_` allocates in caller's stack frame and must be at tail position

### Common Patterns

```ocaml
(* Process local data without allocation *)
let sum_pairs (pairs @ local) =
  List.fold_left (fun acc (a, b) -> acc + a + b) 0 pairs

(* Return local from function *)
let make_pair x y = exclave_ stack_ (x, y)

(* Local references for accumulators *)
let count_positives lst =
  let local_ r = ref 0 in
  List.iter (fun x -> if x > 0 then r := !r + 1) lst;
  !r
```

---

## 3. Unboxed Types

Unboxed types store values directly without heap allocation.

### Built-in Unboxed Types

```ocaml
(* Numeric types - # suffix means unboxed *)
float#     (* 64-bit float, kind float64 *)
int32#     (* 32-bit int, kind bits32 *)
int64#     (* 64-bit int, kind bits64 *)
nativeint# (* native int, kind word *)
float32#   (* 32-bit float, kind float32 *)
int8#      (* 8-bit int - untagged *)
int16#     (* 16-bit int - untagged *)
int#       (* native int - untagged *)
char#      (* 8-bit char - untagged, same layout as int8# *)

(* Literals use # prefix *)
let x : float# = #3.14
let y : int32# = #42l
let z : int64# = #100L
let w : float32# = #1.0s
let a : int8# = #42s       (* int8# literal *)
let b : int16# = #42S      (* int16# literal *)
let c : char# = #'x'       (* char# literal *)

(* Boxed versions (heap-allocated) *)
let a : float = 3.14       (* boxed *)
let b : float# = #3.14     (* unboxed *)
```

### Untagged Int Arrays (New in 5.2.0minus-25)

Arrays of untagged types are packed for memory efficiency:

```ocaml
(* Untagged int arrays - tightly packed *)
let bytes : int8# array = [| #0s; #1s; #255s |]
let shorts : int16# array = [| #0S; #1S; #32767S |]
let ints : int# array = [| #0; #1; #42 |]
let chars : char# array = [| #'a'; #'b'; #'c' |]

(* int8# array: 1 byte per element *)
(* int16# array: 2 bytes per element *)
(* int# array: native word size per element *)
```

### Unboxed Records

```ocaml
(* Unboxed record - stored inline, not heap-allocated *)
type point = #{ x : float#; y : float# }

(* Create unboxed record *)
let p : point = #{ x = #1.0; y = #2.0 }

(* Access fields *)
let get_x (p : point) = p.#x
```

### Unboxed Tuples

```ocaml
(* Unboxed tuple syntax *)
type pair = #(float# * int32#)

let p : #(float# * int32#) = #(#1.0, #42l)
```

### Mixed Blocks

Records can mix boxed and unboxed fields:

```ocaml
type mixed = {
  name : string;          (* boxed *)
  value : float#;         (* unboxed, stored flat *)
  count : int32#;         (* unboxed *)
}
```

### or_null Type

Non-allocating option for nullable values:

```ocaml
type 'a or_null = Null | This of 'a

(* Use for optional unboxed values without allocation *)
let find_float arr idx : float# or_null =
  if idx < Array.length arr then This arr.(idx)
  else Null
```

---

## 4. Kinds

Kinds classify types by their runtime representation.

### Kind Hierarchy

```
any                           (* any layout *)
├── value                     (* standard OCaml boxed values *)
├── float64                   (* 64-bit floats *)
├── float32                   (* 32-bit floats *)
├── bits32                    (* 32-bit integers *)
├── bits64                    (* 64-bit integers *)
├── word                      (* native word size *)
└── void                      (* uninhabited *)
```

### Kind Annotations

```ocaml
(* On type parameters *)
type ('a : float64) container = ...

(* On type variables in signatures *)
val f : ('a : value). 'a -> 'a
val g : ('a : bits64). 'a -> 'a

(* On abstract types *)
type t : float64

(* Kind products for unboxed tuples *)
type pair : float64 & bits32    (* unboxed pair of float# and int32# *)
```

### Kind Abbreviations

```ocaml
value           = value_or_null mod non_null separable
immediate       = value mod external_
immediate64     = value mod external64
mutable_data    = value mod non_float
immutable_data  = value mod non_float immutable
```

### Mode Bounds on Kinds

Kinds can specify which modes a type crosses:

```ocaml
(* Type that cannot be used at mode local *)
type t : value mod global

(* Type that is always portable *)
type t : value mod portable
```

---

## 5. Uniqueness

Track values with exactly one reference for safe mutation/deallocation.

### Modes

- `unique`: Single reference exists
- `aliased`: Multiple references may exist

### Syntax

```ocaml
(* Unique parameter - consumed by function *)
val free : t @ unique -> unit

(* Aliased return - may have multiple references *)
val duplicate : t -> t * t @ aliased

(* Once closures - can only be invoked once *)
val delay_free : t @ unique -> (unit -> unit) @ once
```

### Uniqueness Rules

```ocaml
(* OK: match then use uniquely *)
let ok t =
  match t with
  | Con { field } -> free t

(* ERROR: using parts twice *)
let bad t =
  match t with
  | Con { field } ->
    free_field field;   (* uses field *)
    free t              (* uses t which contains field *)

(* OK: different branches *)
let ok t =
  match t with
  | Con { field } ->
    if cond then free_field field
    else free t
```

### Aliased Modality

Store aliased values in unique containers:

```ocaml
type 'a aliased_box = { value : 'a @@ aliased } [@@unboxed]

(* Container is unique but contents are aliased *)
val push : 'a @ aliased -> 'a aliased_box list @ unique -> 'a aliased_box list @ unique
```

---

## 6. Comprehensions

Python/Haskell-style list and array builders.

### List Comprehensions

```ocaml
(* Basic *)
[ x * 2 for x = 1 to 10 ]

(* With filter *)
[ x for x = 1 to 100 when x mod 2 = 0 ]

(* Nested iteration *)
[ (x, y) for x = 1 to 3 for y = 1 to 3 ]

(* Iterate over list *)
[ String.uppercase s for s in strings ]

(* Multiple conditions *)
[ x + y for x = 1 to 10 for y = 1 to 10 when x < y when x + y < 15 ]

(* Parallel iteration (evaluated together) *)
[ x + y for x = 1 to 3 and y = 10 to 12 ]
```

### Array Comprehensions

```ocaml
(* Same syntax with [| |] *)
[| x * x for x = 1 to 10 |]

(* Iterate over array *)
[| f elem for elem in source_array |]
```

### Immutable Array Comprehensions

```ocaml
[: x for x = 1 to 10 when x mod 2 = 0 :]
```

### Key Differences: `for` vs `and`

- `for ... for ...`: Nested (inner re-evaluated each outer iteration)
- `for ... and ...`: Parallel (both evaluated once upfront)

```ocaml
(* Nested: 9 elements *)
[ (x, y) for x = 1 to 3 for y = 1 to 3 ]

(* Parallel: 3 elements *)
[ (x, y) for x = 1 to 3 and y = 10 to 12 ]
(* = [(1,10); (2,11); (3,12)] *)
```

---

## 7. SIMD Vector Types

128-bit and 256-bit SIMD vectors for parallel numeric operations.

### Types

```ocaml
(* 128-bit vectors *)
int8x16    int8x16#      (* 16 x 8-bit ints *)
int16x8    int16x8#      (* 8 x 16-bit ints *)
int32x4    int32x4#      (* 4 x 32-bit ints *)
int64x2    int64x2#      (* 2 x 64-bit ints *)
float32x4  float32x4#    (* 4 x 32-bit floats *)
float64x2  float64x2#    (* 2 x 64-bit floats *)

(* 256-bit vectors *)
int8x32    int8x32#
int32x8    int32x8#
float64x4  float64x4#
(* etc. *)
```

### Usage

```ocaml
open Ocaml_simd_sse

let v = Float32x4.set 1.0 2.0 3.0 4.0
let v = Float32x4.sqrt v
let x, y, z, w = Float32x4.splat v

(* Load from arrays *)
let v = Int8x16.String.get text ~byte:0
```

### C Stubs

```ocaml
external vec_op : (int8x16[@unboxed]) -> (int8x16[@unboxed]) =
  "boxed_stub" "unboxed_stub"
```

---

## 8. Templates (ppx_template)

Generate multiple copies of code with different modes/kinds.

### Mode Templates

```ocaml
(* Define once, get local and global versions *)
let%template[@mode m = (global, local)] id
  : 'a. 'a @ m -> 'a @ m
  = fun x -> x

(* Generates: id (global) and id__local *)

(* Instantiate *)
let f x = (id [@mode local]) x
```

### Kind Templates

```ocaml
let%template[@kind k = (value, float64)] id
  : ('a : k). 'a -> 'a
  = fun x -> x

(* Generates: id (value) and id__float64 *)
```

### Exclave Conditional

```ocaml
let%template[@mode m = (global, local)] make_pair x y =
  (x, y) [@exclave_if_local m]

(* local version gets: exclave_ (x, y) *)
```

### Alloc Templates

```ocaml
let%template rec map
  : f:('a -> 'b @ m) -> 'a list -> 'b list @ m
  = fun ~f list ->
    match[@exclave_if_stack a] list with
    | [] -> []
    | hd :: tl -> f hd :: (map [@alloc a]) ~f tl
[@@alloc a @ m = (heap_global, stack_local)]
```

### Portable Functors

```ocaml
(* Short form for portable/nonportable functor variants *)
module%template.portable Make (M : S) : T
```

### Default Floating Attributes

```ocaml
[%%template:
[@@@mode.default m = (global, local)]

val min : t @ m -> t @ m -> t @ m
val max : t @ m -> t @ m -> t @ m]
```

---

## 9. Zero-Alloc Checking

Compile-time verification that functions don't allocate.

### Basic Usage

```ocaml
(* Check function doesn't allocate *)
let[@zero_alloc] fast_add x y = x + y

(* Allow local/stack allocations *)
let[@zero_alloc] with_local_pair x y =
  let p = stack_ (x, y) in
  fst p + snd p

(* Only check in optimized builds *)
let[@zero_alloc opt] complex_func x = ...

(* Strict: no allocation even on error paths *)
let[@zero_alloc strict] very_strict x = ...
```

### Assume Annotations

```ocaml
(* Trust this function is zero-alloc *)
let[@zero_alloc assume] external_wrapper x = external_func x

(* Assume for error paths *)
let[@cold][@zero_alloc assume error] handle_error e =
  log_error e;
  default_value
```

### In Signatures

```ocaml
val[@zero_alloc] f : int -> int
val[@zero_alloc strict] g : t -> t
val[@zero_alloc arity 2] h : int -> int -> int
```

### File-Level

```ocaml
[@@@zero_alloc all]  (* All functions must be zero-alloc *)

let[@zero_alloc ignore] allowed_to_alloc x = [x]  (* Opt out *)
```

---

## 10. Parallelism & Capsules

Safe parallel programming with thread isolation.

### Contention Modes

- `contended`: May be accessed from multiple threads concurrently
- `shared`: May be accessed from multiple threads (for shared state)
- `uncontended`: Single-thread access

### Portability Modes

- `portable`: Safe to move across thread boundaries, captures all values at contended
- `shareable`: May execute in parallel, captures shared state
- `nonportable`: Thread-local only, captures uncontended mutable state

### Capsules (Experimental)

Capsules isolate mutable state for safe parallelism:

```ocaml
(* Capsule contains thread-local mutable state *)
type 'a capsule

(* Access requires entering capsule context *)
val with_capsule : 'a capsule -> ('a @ local -> 'b) -> 'b
```

---

## 11. Miscellaneous Extensions

### Labeled Tuples

```ocaml
(* Create *)
let point = ~x:10, ~y:20

(* Type *)
type point = x:int * y:int

(* Destructure *)
let ~x, ~y = point

(* Partial match (needs type annotation) *)
let get_x (p : x:int * y:int) =
  let ~x, .. = p in x

(* Function returning labeled tuple *)
val dimensions : image -> width:int * height:int
```

### Immutable Arrays

```ocaml
(* Syntax uses : instead of | *)
let arr : string iarray = [: "a"; "b"; "c" :]

(* Access *)
let first = arr.:(0)

(* Covariant - allows safe subtyping *)
let arr2 : obj iarray = (arr : sub_obj iarray :> obj iarray)
```

### Include Functor

```ocaml
(* Instead of *)
module M = struct
  module T = struct
    type t = ...
    [@@deriving compare, sexp]
  end
  include T
  include Comparable.Make(T)
end

(* Write *)
module M = struct
  type t = ...
  [@@deriving compare, sexp]

  include functor Comparable.Make
end
```

### Let Mutable

```ocaml
(* Mutable local variable - no allocation *)
let triangle n =
  let mutable total = 0 in
  for i = 1 to n do
    total <- total + i
  done;
  total
```

Restrictions: Cannot escape scope, no closure capture, single variable only.

### Polymorphic Parameters

```ocaml
(* Function taking polymorphic argument *)
let create (f : 'a. 'a field -> 'a) =
  { a = f A; b = f B }

val create : ('a. 'a field -> 'a) -> t
```

### Small Numbers

```ocaml
(* Types *)
float32   float32#
int8      int8#
int16     int16#
char#

(* Literals *)
1.0s    (* float32 *)
#1.0s   (* float32# *)
42s     (* int8 *)
#42s    (* int8# *)
42S     (* int16 *)
#42S    (* int16# *)
#'a'    (* char# *)

(* Arrays - now supported and packed! *)
int8 array    int8# array     (* 1 byte per element *)
int16 array   int16# array    (* 2 bytes per element *)
char# array                   (* 1 byte per element *)

(* Pattern matching with char# ranges *)
match c with
| #'a'..#'z' -> `lowercase
| #'A'..#'Z' -> `uppercase
| _ -> `other
```

### Module Strengthening

```ocaml
(* Instead of *)
sig type t = M.t end

(* Write *)
S with M
```

---

## Common Patterns

### Zero-Alloc Hot Path

```ocaml
let[@zero_alloc] process_batch (data @ local) =
  let local_ acc = ref 0 in
  for i = 0 to Array.length data - 1 do
    acc := !acc + process_item data.(i)
  done;
  !acc
```

### Local Allocation in Loop

```ocaml
let process_all items =
  List.iter (fun item ->
    let local_ temp = compute item in
    use temp
  ) items
```

### Unique Resource Management

```ocaml
type handle

val open_handle : unit -> handle @ unique
val use_handle : handle @ unique -> result * handle @ unique
val close_handle : handle @ unique -> unit

let with_handle f =
  let h = open_handle () in
  let result, h = use_handle h in
  close_handle h;
  result
```

### Mode-Polymorphic Function

```ocaml
let%template[@mode m = (global, local)] map_pair f (a, b) =
  ((f a, f b) [@exclave_if_local m])
```

### Kind-Polymorphic Container

```ocaml
type%template ('a : k) box = { contents : 'a }
[@@kind k = (value, float64, bits64)]
```

---

## Debugging Tips

1. **Mode errors**: Check if you're trying to return local data globally
2. **Kind errors**: Ensure type parameters have correct layout annotations
3. **Zero-alloc failures**: Use `-zero-alloc-checker-details-cutoff -1` for full details
4. **Template issues**: Check mangled names with `__suffix` pattern

---

## Library Dependencies

### Core Libraries

- **`stdlib_stable`**: Immutable arrays (`Iarray`), `Float32`, `Int8`, `Int16`, `Char_u`
- **`base`**: Jane Street's standard library with comprehensive OxCaml mode support
  - **IMPORTANT**: Consult [SKILL-BASE.md](SKILL-BASE.md) for OxCaml-friendly functions!
  - Contains 116 modules with extensive local/exclave, mode, and unboxed type support
  - Key modules: `Modes` (modal wrappers), `Iarray` (immutable arrays with local ops),
    `Container_with_local`, and `__local` variants of most collection functions
- **`core`**: Extended library with I/O, async, and system features
  - See [SKILL-CORE.md](SKILL-CORE.md) for Iobuf, Time_ns, Bigstring extensions

### PPX Libraries

- **`ppx_template`**: Mode/kind polymorphism via code generation
  - See [SKILL-TEMPLATES.md](SKILL-TEMPLATES.md) for mangling details
- **`ppx_simd`**: SIMD shuffle/blend mask generation

### SIMD Libraries

- **`ocaml_simd`**: Base SIMD types
- **`ocaml_simd_sse`**: SSE intrinsics (128-bit)
- **`ocaml_simd_avx`**: AVX/AVX2 intrinsics (256-bit)
- See [SKILL-SIMD.md](SKILL-SIMD.md) for usage details
