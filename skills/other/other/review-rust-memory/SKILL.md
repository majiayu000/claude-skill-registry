---
name: review-rust-memory
description: Review and enforce Rust memory optimization patterns. Use when writing, reviewing, or debugging Rust code for memory efficiency. Covers allocation reduction, data layout, string handling, collection sizing, Copy-on-Write, arena allocation, stack vs heap tradeoffs, zero-copy parsing, memory profiling, and leak prevention.
---

# Rust Memory Optimization Patterns, Footguns & Standards

**Context**: Feather-Flow is a schema validation framework with static analysis as a first-class citizen. See **[HOW_FEATHERFLOW_WORKS.md](../../../HOW_FEATHERFLOW_WORKS.md)** for the full architecture. Memory efficiency matters most in the compile pipeline: schema propagation walks the entire DAG, DataFusion plans every SQL model, and analysis passes run per-model — so allocation costs scale with model count.

A practical reference for writing memory-efficient Rust — common anti-patterns, the correct alternatives, and rules to enforce in code review.

## Core Rules

1. **Measure before optimizing** — `DHAT`, `heaptrack`, or `jemalloc` profiling before guessing
2. **Minimize allocations** — the fastest allocation is the one that doesn't happen
3. **Right-size your collections** — `Vec::with_capacity`, not push-and-pray
4. **`Cow<str>` over `String` clones** — borrow when you can, own when you must
5. **Stack over heap** — `SmallVec`, `ArrayString`, inline buffers for small, bounded data
6. **Zero-copy parsing** — borrow from the input buffer, don't allocate per field
7. **Shrink your types** — field ordering, smaller integer types, `Box<[T]>` over `Vec<T>` for sealed data
8. **Drop early, drop explicitly** — release memory as soon as you're done with it
9. **Flatten nested allocations** — `Vec<Vec<T>>` is two allocations per inner vec; flatten when possible
10. **Profile your allocator** — `jemalloc` or `mimalloc` can halve fragmentation in long-running processes
11. **Avoid `String` for fixed vocabularies** — enums, interning, or `&'static str`
12. **No `clone()` as a reflex** — restructure ownership, use references, share with `Arc`

---

## Rule 1: Measure Before Optimizing

Memory optimization without profiling is guesswork. Rust's ownership model prevents leaks, but it doesn't prevent excessive allocation, fragmentation, or bloated data structures.

### Tools

| Tool | What it tells you |
|------|-------------------|
| `DHAT` (via `dhat-rs`) | Allocation count, total bytes, peak live bytes, allocation hotspots |
| `heaptrack` | Allocation timeline, flamegraphs of allocation sites, leak detection |
| `jemalloc` `malloc_stats` | Fragmentation, active vs mapped memory, arena utilization |
| `std::mem::size_of::<T>()` | Compile-time struct size (includes padding) |
| `std::mem::align_of::<T>()` | Alignment requirement (drives padding) |
| `/proc/self/status` (Linux) | VmRSS (resident set), VmPeak, VmSwap |

### The Rule

> **Never optimize memory without profiling first.** Add `dhat-rs` as a dev dependency, run your hottest code path under it, and fix the top allocation sites.
>
> ```rust
> // In a benchmark or integration test:
> #[global_allocator]
> static ALLOC: dhat::Alloc = dhat::Alloc;
>
> fn main() {
>     let _profiler = dhat::Profiler::new_heap();
>     // ... run workload ...
>     // Drop _profiler to print stats
> }
> ```

---

## Rule 2: Minimize Allocations

Every `Box::new`, `Vec::push` (that grows), `String::from`, and `format!` hits the allocator. In hot paths, the allocator is often the bottleneck.

### The Footgun

```rust
// BAD — allocation per iteration
fn process_items(items: &[Item]) -> Vec<String> {
    let mut results = Vec::new();
    for item in items {
        let label = format!("item-{}", item.id);   // allocates a String
        let upper = label.to_uppercase();            // allocates another String
        results.push(upper);                         // may reallocate the Vec
    }
    results
}
```

### The Fix

```rust
// GOOD — pre-allocate, reuse buffer
fn process_items(items: &[Item]) -> Vec<String> {
    let mut results = Vec::with_capacity(items.len());
    let mut buf = String::with_capacity(64);

    for item in items {
        buf.clear();
        use std::fmt::Write;
        write!(&mut buf, "item-{}", item.id).unwrap();
        results.push(buf.to_uppercase());
    }
    results
}

// EVEN BETTER — return references if the caller doesn't need ownership
fn process_items(items: &[Item]) -> Vec<String> {
    items.iter()
        .map(|item| format!("ITEM-{}", item.id))
        .collect()  // single allocation via collect's size_hint
}
```

### The Rule

> **In hot paths, count your allocations.** Each `format!`, `to_string()`, `to_owned()`, `clone()`, and `vec![]` is a call to the allocator.
> - Reuse buffers with `.clear()` instead of creating new ones
> - `write!` into an existing `String` instead of `format!` creating a new one
> - `collect()` with `size_hint` is one allocation; a loop with `push` may be many

---

## Rule 3: Right-Size Your Collections

`Vec` starts at capacity 0, then grows by doubling (0 → 4 → 8 → 16 → 32...). Each growth copies all elements to a new, larger buffer and frees the old one. For a 1000-element vec built with `push`, that's ~10 reallocations and ~2000 elements copied.

### The Footgun

```rust
// BAD — 10+ reallocations for known-size data
fn collect_names(users: &[User]) -> Vec<String> {
    let mut names = Vec::new();
    for user in users {
        names.push(user.name.clone());
    }
    names
}

// BAD — HashMap resizes 5+ times building a known-size map
fn build_index(items: &[Item]) -> HashMap<u64, &Item> {
    let mut map = HashMap::new();
    for item in items {
        map.insert(item.id, item);
    }
    map
}
```

### The Fix

```rust
// GOOD — single allocation, no reallocations
fn collect_names(users: &[User]) -> Vec<String> {
    let mut names = Vec::with_capacity(users.len());
    for user in users {
        names.push(user.name.clone());
    }
    names
}

// BETTER — collect uses size_hint automatically
fn collect_names(users: &[User]) -> Vec<String> {
    users.iter().map(|u| u.name.clone()).collect()
}

// GOOD — HashMap with capacity
fn build_index(items: &[Item]) -> HashMap<u64, &Item> {
    let mut map = HashMap::with_capacity(items.len());
    for item in items {
        map.insert(item.id, item);
    }
    map
}
```

### Sealed collections: `Vec<T>` → `Box<[T]>`

When a collection won't be modified after creation, convert it to a boxed slice. This drops the `capacity` field (saving 8 bytes on the stack) and shrinks the heap allocation to exact size.

```rust
// GOOD — sealed data, no wasted capacity
let items: Box<[Item]> = build_items().into_boxed_slice();
```

### The Rule

> **Always use `with_capacity` when the size is known or estimable.** `collect()` does this automatically for iterators with accurate `size_hint`.
> - `Vec::with_capacity(n)` — one allocation
> - `HashMap::with_capacity(n)` — one allocation
> - `String::with_capacity(n)` — for string building
> - After building, `.into_boxed_slice()` or `.shrink_to_fit()` to release excess capacity

---

## Rule 4: `Cow<str>` Over `String` Clones

`Cow<'a, str>` (Clone-on-Write) borrows when possible and only allocates when mutation is needed. This is the single biggest memory win for functions that usually pass data through unchanged.

### The Footgun

```rust
// BAD — clones the string even when no modification is needed
fn normalize(input: &str) -> String {
    if input.contains('\t') {
        input.replace('\t', "    ")   // allocates only when tabs exist
    } else {
        input.to_string()             // UNNECESSARY allocation
    }
}

// BAD — forces every caller to allocate
fn process(name: String) {
    println!("{name}");
}
let s = "hello";
process(s.to_string()); // pointless allocation
```

### The Fix

```rust
// GOOD — borrows when unchanged, allocates only when modified
use std::borrow::Cow;

fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains('\t') {
        Cow::Owned(input.replace('\t', "    "))
    } else {
        Cow::Borrowed(input)
    }
}

// GOOD — accept borrowed or owned
fn process(name: &str) {
    println!("{name}");
}

// ALSO GOOD — when you need flexibility
fn process(name: impl AsRef<str>) {
    println!("{}", name.as_ref());
}
```

### The Rule

> **Use `Cow<str>` for functions that sometimes modify strings and sometimes don't.** The borrow case is zero-allocation.
> - Return `Cow<'_, str>` instead of `String` from transformation functions
> - Accept `&str` or `impl AsRef<str>` instead of `String` for read-only parameters
> - `Cow::Borrowed` for the fast path (no change), `Cow::Owned` for the slow path (modification needed)

---

## Rule 5: Stack Over Heap for Small, Bounded Data

Heap allocation involves a syscall (or at minimum, allocator bookkeeping). For small, fixed-size data, the stack is free.

### The Footgun

```rust
// BAD — heap allocation for a tiny, bounded vec
fn get_keywords(input: &str) -> Vec<&str> {
    input.splitn(5, ',').collect()  // at most 5 elements, but Vec heap-allocates
}

// BAD — String for a bounded identifier
struct Model {
    name: String,  // model names are ≤64 chars by convention
}
```

### The Fix

```rust
// GOOD — SmallVec stays on the stack for small counts
use smallvec::SmallVec;

fn get_keywords(input: &str) -> SmallVec<[&str; 8]> {
    input.splitn(5, ',').collect()  // no heap allocation for ≤8 elements
}

// GOOD — ArrayString for bounded strings (from the `arrayvec` crate)
use arrayvec::ArrayString;

struct Model {
    name: ArrayString<64>,  // 64 bytes on the stack, no heap allocation
}

// GOOD — tinyvec for no-dependency alternative
use tinyvec::ArrayVec;

fn get_pair(a: u32, b: u32) -> ArrayVec<[u32; 4]> {
    let mut v = ArrayVec::new();
    v.push(a);
    v.push(b);
    v
}
```

### When to use what

| Data | Stack option | When heap is fine |
|------|-------------|-------------------|
| ≤ ~8 items, known bound | `SmallVec<[T; N]>` | Unknown or large count |
| ≤ ~128 byte string, known bound | `ArrayString<N>` | Unbounded user input |
| Fixed small count | `ArrayVec<[T; N]>` | Dynamic size needed |
| Enum variants, status codes | Inline in the struct | Never needs heap |

### The Rule

> **If the data has a small, known upper bound, keep it on the stack.** `SmallVec`, `ArrayVec`, and `ArrayString` avoid the allocator entirely for the common case.

---

## Rule 6: Zero-Copy Parsing

Parsing a large input buffer into a structure that borrows from the buffer — instead of copying substrings — can reduce memory usage by 2-10x.

### The Footgun

```rust
// BAD — copies every field out of the input
struct Record {
    name: String,
    value: String,
}

fn parse_records(input: &str) -> Vec<Record> {
    input.lines()
        .map(|line| {
            let (name, value) = line.split_once('=').unwrap();
            Record {
                name: name.to_string(),    // allocation
                value: value.to_string(),  // allocation
            }
        })
        .collect()
}
```

### The Fix

```rust
// GOOD — borrows from the input buffer, zero allocations per field
struct Record<'a> {
    name: &'a str,
    value: &'a str,
}

fn parse_records(input: &str) -> Vec<Record<'_>> {
    input.lines()
        .filter_map(|line| {
            let (name, value) = line.split_once('=')?;
            Some(Record {
                name: name.trim(),
                value: value.trim(),
            })
        })
        .collect()  // one allocation for the Vec, zero for the records
}

// GOOD — serde zero-copy deserialization
use serde::Deserialize;

#[derive(Deserialize)]
struct Event<'a> {
    #[serde(borrow)]
    event_type: &'a str,
    #[serde(borrow)]
    payload: &'a serde_json::value::RawValue,
}
```

### The Rule

> **When parsing structured data, borrow from the source buffer.** Lifetimes are free; allocations are not.
> - Use `&'a str` fields instead of `String` when the source outlives the parsed structure
> - `#[serde(borrow)]` for zero-copy JSON/YAML deserialization
> - If ownership is needed later, provide an `.into_owned()` method

---

## Rule 7: Shrink Your Types

Every byte in a struct is multiplied by every instance. A 4-byte savings on a type with 1M instances saves 4MB.

### Field ordering and padding

Rust lays out struct fields with alignment padding. Field order matters.

```rust
// BAD — 24 bytes (with padding)
struct Bad {
    a: u8,    // 1 byte + 7 padding
    b: u64,   // 8 bytes
    c: u8,    // 1 byte + 7 padding
}

// GOOD — 16 bytes (fields ordered large to small)
struct Good {
    b: u64,   // 8 bytes
    a: u8,    // 1 byte
    c: u8,    // 1 byte + 6 padding
}
// Check: assert_eq!(std::mem::size_of::<Good>(), 16);
```

### Smaller integer types

```rust
// BAD — 8 bytes for a port number
struct Config {
    port: u64,  // max 65535, u64 is wasteful
}

// GOOD — 2 bytes
struct Config {
    port: u16,
}
```

### `Box<T>` for large enum variants

```rust
// BAD — the entire enum is as large as the biggest variant
enum Ast {
    Literal(i64),                              // 8 bytes
    BinaryOp { left: Box<Ast>, op: Op, right: Box<Ast> },  // 24 bytes
    Function { name: String, args: Vec<Ast> }, // 48 bytes ← inflates all variants
}

// GOOD — Box the large variant
enum Ast {
    Literal(i64),
    BinaryOp { left: Box<Ast>, op: Op, right: Box<Ast> },
    Function(Box<FunctionCall>),  // 8 bytes (pointer)
}

struct FunctionCall {
    name: String,
    args: Vec<Ast>,
}
```

### `Option<NonZero*>` for niche optimization

```rust
use std::num::NonZeroU32;

// size_of::<Option<u32>>()        == 8  (tag + value)
// size_of::<Option<NonZeroU32>>() == 4  (niche: 0 represents None)
struct Record {
    id: Option<NonZeroU32>,  // 4 bytes instead of 8
}
```

### The Rule

> **Order struct fields from largest alignment to smallest.** Use `size_of` and `align_of` to verify.
> - Large enum variants → `Box` the payload
> - Optional integers → `NonZeroU*` for niche optimization
> - Counts that fit in `u32` don't need `usize` (on 64-bit, saves 4 bytes each)
> - After optimization, assert sizes in a test: `assert_eq!(size_of::<MyType>(), expected)`

---

## Rule 8: Drop Early, Drop Explicitly

Rust drops values at the end of their scope. If you're done with a large allocation halfway through a function, it sits in memory until the function returns.

### The Footgun

```rust
// BAD — `raw_data` lives until the function returns
fn process(path: &Path) -> Result<Summary> {
    let raw_data = std::fs::read_to_string(path)?;  // could be 100MB
    let parsed = parse(&raw_data);
    let summary = summarize(&parsed);

    // ... 200 more lines of computation ...
    // raw_data is still alive, holding 100MB

    Ok(summary)
}
```

### The Fix

```rust
// GOOD — drop raw_data as soon as parsing is done
fn process(path: &Path) -> Result<Summary> {
    let parsed = {
        let raw_data = std::fs::read_to_string(path)?;
        parse(&raw_data)
    }; // raw_data dropped here

    let summary = summarize(&parsed);
    // ... rest of computation with 100MB freed ...
    Ok(summary)
}

// ALSO GOOD — explicit drop
fn process(path: &Path) -> Result<Summary> {
    let raw_data = std::fs::read_to_string(path)?;
    let parsed = parse(&raw_data);
    drop(raw_data); // explicit: free the 100MB now

    let summary = summarize(&parsed);
    Ok(summary)
}
```

### The Rule

> **Scope or `drop()` large allocations as soon as you're done with them.** Don't let 100MB sit around because you still need a 1KB summary derived from it.
> - Inner blocks `{ ... }` for scoped lifetimes
> - `drop(x)` for explicit deallocation
> - `Vec::clear()` + `Vec::shrink_to_fit()` if you need to reuse the variable but release memory

---

## Rule 9: Flatten Nested Allocations

`Vec<Vec<T>>` is one allocation for the outer vec plus one allocation per inner vec. For 10,000 inner vecs, that's 10,001 heap allocations and scattered memory (poor cache locality).

### The Footgun

```rust
// BAD — 10,001 allocations for 10,000 groups
fn group_by_key(items: &[Item]) -> Vec<Vec<&Item>> {
    let mut groups: HashMap<u64, Vec<&Item>> = HashMap::new();
    for item in items {
        groups.entry(item.key).or_default().push(item);
    }
    groups.into_values().collect()
}

// BAD — String per row per column
struct Table {
    rows: Vec<Vec<String>>,  // N*M allocations
}
```

### The Fix

```rust
// GOOD — flat buffer with index
struct FlatGroups<'a> {
    items: Vec<&'a Item>,      // one allocation
    offsets: Vec<usize>,       // one allocation (group boundaries)
}

impl<'a> FlatGroups<'a> {
    fn group(&self, i: usize) -> &[&'a Item] {
        let start = self.offsets[i];
        let end = self.offsets.get(i + 1).copied().unwrap_or(self.items.len());
        &self.items[start..end]
    }
}

// GOOD — single String buffer with slices for a table
struct Table {
    buffer: String,                // one allocation for all cell data
    cells: Vec<(usize, usize)>,   // (start, len) into buffer — one allocation
    columns: usize,
}
```

### The Rule

> **Flatten `Vec<Vec<T>>` into a single `Vec<T>` + offset array when the inner vecs are built once and read many times.** This reduces allocations from N+1 to 2 and improves cache locality.

---

## Rule 10: Choose Your Allocator

The default system allocator (`malloc`/`free`) is general-purpose but not always optimal. For long-running processes with varied allocation patterns, a purpose-built allocator can significantly reduce fragmentation and peak RSS.

### Options

```rust
// jemalloc — good for long-running servers, reduces fragmentation
#[global_allocator]
static ALLOC: tikv_jemallocator::Jemalloc = tikv_jemallocator::Jemalloc;

// mimalloc — good general-purpose performance, lower latency
#[global_allocator]
static ALLOC: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

### Arena allocation for batch processing

When you allocate many small objects that all share the same lifetime (e.g., AST nodes during parsing), arena allocation is ideal — one bulk allocation, one bulk deallocation, zero individual frees.

```rust
use bumpalo::Bump;

fn parse_ast<'a>(bump: &'a Bump, source: &str) -> &'a AstNode<'a> {
    let node = bump.alloc(AstNode {
        kind: NodeKind::Root,
        children: bumpalo::vec![in bump],
    });
    // ... parse into bump-allocated nodes ...
    node
}
// All allocations freed at once when `bump` is dropped
```

### The Rule

> **For CLI tools processing batches, arenas (`bumpalo`) eliminate per-object free overhead.**
> **For long-running processes, `jemalloc` or `mimalloc` reduce fragmentation.**
> - Benchmark before switching — the default allocator is fine for many workloads
> - Arena allocation is ideal when all objects share a lifetime (parsing, compilation passes)

---

## Rule 11: Avoid `String` for Fixed Vocabularies

If a value comes from a known, finite set, a heap-allocated `String` is pure waste.

### The Footgun

```rust
// BAD — heap allocation for a value that's always one of 5 options
struct Column {
    data_type: String,  // "integer", "text", "boolean", "float", "timestamp"
}

// BAD — storing the same string thousands of times
struct Record {
    status: String,  // "active" appears 50,000 times → 50,000 allocations
}
```

### The Fix

```rust
// GOOD — enum is zero bytes of heap allocation
enum DataType {
    Integer,
    Text,
    Boolean,
    Float,
    Timestamp,
}

// GOOD — &'static str for open-ended but long-lived strings
struct Column {
    data_type: &'static str,
}

// GOOD — string interning for dynamic but repetitive strings
use string_interner::StringInterner;

struct Schema {
    interner: StringInterner,
    columns: Vec<InternedColumn>,
}

struct InternedColumn {
    name: DefaultSymbol,       // 4 bytes, not 24+ for a String
    data_type: DefaultSymbol,  // shares storage with other columns
}
```

### The Rule

> **Fixed vocabulary → enum.** Repeated strings → interning. Static strings → `&'static str`.
> - `String` is for genuinely dynamic, user-provided data
> - Enums have zero allocation cost and enable exhaustive matching
> - Interning eliminates duplicate storage for repeated values

---

## Rule 12: No `clone()` as a Reflex

`clone()` is an allocation (for heap types). Every `clone()` in a hot path should be justified.

### The Footgun

```rust
// BAD — cloning to satisfy the borrow checker
fn process(data: &Data) -> Result<Output> {
    let name = data.name.clone();      // why?
    let items = data.items.clone();    // 1000 items cloned
    transform(&name, &items)
}

// BAD — cloning in a loop
fn find_matches(haystack: &[Record], needle: &str) -> Vec<Record> {
    haystack.iter()
        .filter(|r| r.name == needle)
        .cloned()        // clones every matching record
        .collect()
}
```

### The Fix

```rust
// GOOD — borrow instead of clone
fn process(data: &Data) -> Result<Output> {
    transform(&data.name, &data.items)
}

// GOOD — return references, let caller decide about ownership
fn find_matches<'a>(haystack: &'a [Record], needle: &str) -> Vec<&'a Record> {
    haystack.iter()
        .filter(|r| r.name == needle)
        .collect()
}

// GOOD — Arc for shared ownership without cloning the data
fn process(data: Arc<Data>) -> Result<Output> {
    let data_ref = Arc::clone(&data);  // cheap reference count increment
    transform(&data_ref.name, &data_ref.items)
}
```

### The Rule

> **Every `clone()` should answer: "Why can't this be a reference?"**
> - Borrow (`&T`) when you just need to read
> - `Arc<T>` when multiple owners need shared access
> - `Cow<'_, T>` when you usually borrow but sometimes need to own
> - `clone()` only when ownership transfer is genuinely required

---

## Summary Cheat Sheet

| Rule | Anti-pattern | Fix |
|------|-------------|-----|
| Measure first | Guessing at hotspots | `dhat-rs`, `heaptrack`, `size_of` |
| Minimize allocations | `format!` in hot loops | Reuse buffers, `write!` into existing `String` |
| Right-size collections | `Vec::new()` + repeated push | `Vec::with_capacity(n)`, `collect()` |
| Cow over clone | `input.to_string()` when unmodified | `Cow::Borrowed(input)` |
| Stack over heap | `Vec` for ≤8 items | `SmallVec`, `ArrayVec`, `ArrayString` |
| Zero-copy parsing | `String` fields from parsed input | `&'a str` fields, `#[serde(borrow)]` |
| Shrink types | Random field order, oversized ints | Largest-first ordering, `u16`/`u32`, `Box` big variants |
| Drop early | Large data lives to end of scope | Inner blocks, explicit `drop()` |
| Flatten nested allocs | `Vec<Vec<T>>` | Flat `Vec<T>` + offset array |
| Choose allocator | Default malloc for everything | `jemalloc`/`mimalloc`, `bumpalo` for arenas |
| Avoid String for enums | `String` for fixed options | `enum`, `&'static str`, interning |
| No reflex clone | `.clone()` to appease borrow checker | References, `Arc`, `Cow`, restructured ownership |

---

## Feather-Flow-Specific Patterns

These patterns address the concrete memory hotspots in this codebase. They apply during schema propagation, compilation, and static analysis — the hot paths where model count is the multiplier.

### FF-1: `Arc<RelSchema>` for the Schema Catalog

`RelSchema` (containing `Vec<TypedColumn>`, each with `Vec<ColumnProvenance>`) is cloned 2-3 times per model during schema propagation. With N models, that's 2N-3N deep clones of nested Vecs.

```rust
// BAD — current pattern: clone into two separate maps
schema_catalog.insert(name.to_string(), rel_schema.clone());
yaml_schemas.insert(name.clone(), rel_schema);

// Then AGAIN when converting for propagation:
let yaml_string_map: HashMap<String, RelSchema> = yaml_schemas
    .iter()
    .map(|(k, v)| (k.to_string(), v.clone()))  // clones ALL schemas again
    .collect();

// GOOD — share ownership with Arc
let shared = Arc::new(rel_schema);
schema_catalog.insert(name.to_string(), Arc::clone(&shared));
yaml_schemas.insert(name.clone(), shared);

// Conversion becomes cheap:
let yaml_string_map: HashMap<String, Arc<RelSchema>> = yaml_schemas
    .iter()
    .map(|(k, v)| (k.to_string(), Arc::clone(v)))  // ref count bump, not deep clone
    .collect();
```

### FF-2: Build Function Registries Once

`FeatherFlowProvider` rebuilds ~45 UDF HashMap entries per model. For 100 models, that's 4,500 HashMap insertions with String key allocations — for the same static set of functions.

```rust
// BAD — current pattern: rebuild per model in topological loop
for model in &topo_order {
    let provider = FeatherFlowProvider::with_user_functions(
        &catalog, user_functions, user_table_functions,
    );
    // Inside: duckdb_scalar_udfs() creates Vec of Arc<ScalarUDF>
    // Then collects into HashMap<String, Arc<ScalarUDF>> — per model
}

// GOOD — build once, share by reference
let scalar_fns: HashMap<String, Arc<ScalarUDF>> = functions::duckdb_scalar_udfs()
    .into_iter()
    .map(|f| (f.name().to_uppercase(), f))
    .collect();
let aggregate_fns: HashMap<String, Arc<AggregateUDF>> = functions::duckdb_aggregate_udfs()
    .into_iter()
    .map(|f| (f.name().to_uppercase(), f))
    .collect();

for model in &topo_order {
    let provider = FeatherFlowProvider::with_prebuilt_functions(
        &catalog, &scalar_fns, &aggregate_fns, user_functions,
    );
}
```

### FF-3: Cache Arrow Schema Conversions

`rel_schema_to_arrow()` converts `RelSchema` → Arrow `SchemaRef` on every `get_table_source()` call. If model A references upstream B three times, B's schema is converted three times.

```rust
// BAD — convert on every lookup
fn get_table_source(&self, name: &str) -> Option<SchemaRef> {
    let schema = self.catalog.get(name)?;
    Some(rel_schema_to_arrow(schema))  // allocates Fields + Arc<Schema>
}

// GOOD — cache conversions
struct FeatherFlowProvider<'a> {
    catalog: &'a SchemaCatalog,
    arrow_cache: HashMap<String, SchemaRef>,  // SchemaRef is Arc<Schema>, cheap to clone
}

fn get_table_source(&mut self, name: &str) -> Option<SchemaRef> {
    if let Some(cached) = self.arrow_cache.get(name) {
        return Some(Arc::clone(cached));
    }
    let schema = self.catalog.get(name)?;
    let arrow = rel_schema_to_arrow(schema);
    self.arrow_cache.insert(name.to_string(), Arc::clone(&arrow));
    Some(arrow)
}
```

### FF-4: Pre-Compute Lookup Maps Once

`categorize_dependencies()` rebuilds a lowercase lookup map from `known_models` on every call — once per model per compilation.

```rust
// BAD — O(models²) string allocations
fn categorize_dependencies(
    deps: HashSet<String>,
    known_models: &HashSet<String>,
    external_tables: &HashSet<String>,
) -> (Vec<String>, Vec<String>) {
    // Rebuilds this map for EVERY model
    let known_models_map: HashMap<String, &String> =
        known_models.iter().map(|s| (s.to_lowercase(), s)).collect();
    // ...
}

// GOOD — build once, pass in
struct DependencyResolver {
    known_lower: HashMap<String, String>,  // lowercase → original
    external_lower: HashSet<String>,
}

impl DependencyResolver {
    fn new(known_models: &HashSet<String>, external: &HashSet<String>) -> Self {
        Self {
            known_lower: known_models.iter()
                .map(|s| (s.to_lowercase(), s.clone()))
                .collect(),
            external_lower: external.iter()
                .map(|s| s.to_lowercase())
                .collect(),
        }
    }

    fn categorize(&self, deps: HashSet<String>) -> (Vec<String>, Vec<String>) {
        // Reuses pre-built maps — zero per-model allocation
    }
}
```

### FF-5: Avoid Newtype-to-String Round-Trips

`ModelName`, `TableName`, and `FunctionName` implement `Borrow<str>` and `AsRef<str>`, but many call sites convert to `String` for HashMap lookups.

```rust
// BAD — allocates a String just to look up in a HashMap
let known_models: HashSet<String> = project.models.keys()
    .map(|k| k.to_string())  // N allocations
    .collect();

// GOOD — use the newtype directly (it impls Borrow<str>)
let known_models: HashSet<&str> = project.models.keys()
    .map(|k| k.as_str())  // zero allocations
    .collect();

// GOOD — or keep HashMap<ModelName, V> and look up with .get(name.as_str())
// since ModelName: Borrow<str>, HashMap::get accepts &str directly
```

### FF-6: `with_capacity` in Schema Operations

`RelSchema::merge()`, `with_nullability()`, `with_source_table()` all create fresh Vecs without capacity hints, despite knowing the exact output size.

```rust
// BAD — grows by doubling
fn merge(left: &RelSchema, right: &RelSchema) -> Self {
    let mut columns = left.columns.clone();
    columns.extend(right.columns.iter().cloned());
    Self { columns }
}

// GOOD — single allocation, exact size
fn merge(left: &RelSchema, right: &RelSchema) -> Self {
    let mut columns = Vec::with_capacity(left.columns.len() + right.columns.len());
    columns.extend(left.columns.iter().cloned());
    columns.extend(right.columns.iter().cloned());
    Self { columns }
}
```

---

## Code Review Checklist

When reviewing Rust code for memory efficiency, check:

**General patterns:**
- **No `Vec::new()` in hot paths** when the size is known — use `with_capacity`
- **No `String` clones** where `&str` or `Cow<str>` suffices
- **No `clone()` to appease the borrow checker** — restructure ownership or use references
- **No `String` for fixed vocabularies** — enums, `&'static str`, or interning
- **No `Vec<Vec<T>>`** for read-mostly data — flatten with offset arrays
- **Struct field ordering** — largest alignment first to minimize padding
- **Large enum variants** are `Box`ed — small variants don't pay the size tax
- **Early drops** — large allocations scoped or `drop()`ed when no longer needed
- **Zero-copy parsing** where input outlives parsed data — `&'a str` over `String`
- **`Box<[T]>`** for sealed collections — `Vec` wastes capacity bytes
- **Stack allocation** for small bounded data — `SmallVec`, `ArrayString`
- **Allocator choice documented** if non-default — `jemalloc`/`mimalloc` with benchmarks

**Feather-Flow-specific:**
- **No `RelSchema.clone()`** where `Arc<RelSchema>` sharing works — especially in catalog/propagation code
- **Function registries built once** — not per-model in the topological loop
- **Arrow schema conversions cached** — `rel_schema_to_arrow()` not called repeatedly for the same table
- **Lookup maps built once** — no per-model `HashMap` construction from `known_models`
- **Newtypes used as-is** — no `.to_string()` on `ModelName`/`TableName` for HashMap lookups when `Borrow<str>` suffices
- **`with_capacity` on schema operations** — `merge()`, `with_nullability()`, diagnostic Vecs

For detailed examples and advanced patterns, see [examples.md](examples.md).

---

## Verification

**After every unit of work, run `make ci` before moving on.** This ensures format, clippy, tests, and docs all pass. Do not proceed to the next task until CI is green.
