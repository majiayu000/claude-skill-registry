---
name: rust-systems-engineering
description: 'Expert-level Rust systems programming for high-performance, critical
  systems like Reth (Ethereum execution client). Use when working on: performance
  optimization, systems-level code, blockchain execut'
---

---
name: rust-systems-engineering
description: Expert-level Rust systems programming for high-performance, critical systems like Reth (Ethereum execution client). Use when working on: performance optimization, systems-level code, blockchain execution layers, memory-critical paths, concurrent systems, or production-grade infrastructure requiring staff engineer precision. Specializes in: allocation reduction, redundancy elimination, prefetching, parallelization, and simplicity-first optimization.
---

# Rust Systems Engineering - Reth & High-Performance Critical Systems

Expert guidance for staff-level Rust systems programming with focus on Reth architecture patterns and production-grade performance engineering.

## Core Engineering Principles

### 1. Simplicity First
- **Measure before optimizing**: Use benchmarks and profilers to identify actual bottlenecks
- **Clear over clever**: Direct code paths beat abstraction layers in hot paths
- **Reduce indirection**: Virtual dispatch and excessive trait bounds add overhead
- **Delete code**: The fastest code is code that doesn't run

### 2. Modularity & Reusability
- Design components as independent, well-tested crates
- Each module should have clear boundaries and minimal coupling
- Follow Reth's philosophy: "Components should be reusable as standalone libraries"
- Document public APIs with examples and performance characteristics

### 3. Safety Without Compromise
- Leverage Rust's type system to eliminate entire bug classes
- Use `unsafe` only when measured performance gains justify it
- Document all safety invariants explicitly in comments
- Prefer safe abstractions that compile to efficient code

### 4. Production-Grade Observability
- Add structured logging with `tracing` for debugging production issues
- Instrument critical paths with metrics (latency, throughput, error rates)
- Include debug assertions that can be disabled in release builds
- Design systems to be debuggable under load

## Performance Optimization Framework

Apply these four principles in order:

### 1. Reduce Allocation
**Why**: Heap allocation is 10-100x slower than stack allocation. Memory pressure triggers GC-like behavior in allocators.

**Techniques**:
- **Stack allocation**: Use arrays instead of `Vec` when size is known: `[T; N]`
- **Buffer reuse**: Keep `Vec` across iterations, use `.clear()` instead of creating new
- **Arena allocators**: Use `bumpalo` or typed-arena for bulk allocations with same lifetime
- **`SmallVec`**: Inline small collections to avoid heap allocation
- **Zero-copy**: Use `&[u8]` slices and avoid cloning data
- **`Cow<'_, T>`**: Clone only when mutation is needed
- **Custom allocators**: Consider `jemalloc` or mimalloc for better performance profiles

**Red flags**:
- `.clone()` in hot loops
- Creating `Vec` or `String` per iteration
- Temporary allocations that could be reused
- Boxing when stack storage suffices

### 2. Spot Redundant Patterns & Simplify
**Why**: The best optimization is eliminating unnecessary work entirely.

**What to look for**:
- **Duplicate computations**: Cache results of pure functions
- **Unnecessary conversions**: Avoid format → parse → format chains
- **Redundant checks**: If type system guarantees invariant, don't check again
- **Over-generic code**: Monomorphization can help, but sometimes manual specialization wins
- **Algorithmic improvements**: O(n²) → O(n log n) beats micro-optimizations

**Simplification strategies**:
- Collapse nested matches/ifs into single match
- Replace complex iterator chains with simple loops when clearer
- Inline small functions in hot paths (verify with benchmarks)
- Remove abstraction layers that don't justify their cost
- Question every `Box`, `Rc`, `Arc` - is shared ownership truly needed?

### 3. Prefetch & Parallelize
**Why**: Modern CPUs excel at parallel work and predictable memory access.

**Prefetching**:
- **Linear access patterns**: Process arrays sequentially for cache-friendly access
- **Structure of arrays (SoA)**: Group same fields together instead of array of structs
- **Cache line awareness**: Align hot data to 64-byte boundaries
- **Avoid pointer chasing**: Minimize indirection in tight loops
- **Batch processing**: Process data in chunks that fit in L2/L3 cache

**Parallelization**:
- **Data parallelism**: Use `rayon` for embarrassingly parallel work: `.par_iter()`
- **Task parallelism**: Spawn tokio tasks for independent I/O-bound work
- **SIMD**: Use `std::simd` for vectorized operations on numeric data
- **Lock-free structures**: Use atomic operations instead of mutexes when possible
- **Staged concurrency**: Follow Reth's staged-sync pattern - pipeline distinct phases

**When NOT to parallelize**:
- Work is too fine-grained (overhead dominates)
- Dependencies between iterations
- Already bottlenecked on memory bandwidth

### 4. Aim for Simplicity
**Why**: Simple code is debuggable, maintainable, and often fastest after compiler optimization.

**Practices**:
- **Tight inner loops**: Keep hot paths focused and linear
- **Minimize branches**: CPU branch prediction works best with predictable patterns
- **Avoid allocations in loops**: See principle #1
- **Profile-guided decisions**: Let data guide optimization choices
- **Incremental optimization**: Change one thing at a time, measure impact
- **Document why, not what**: Explain performance-critical design choices

## Reth-Specific Architecture Patterns

### Staged-Sync Architecture
Reth follows Erigon's staged-sync model:
- Break blockchain sync into distinct stages (headers, bodies, execution, etc.)
- Each stage can be optimized independently
- Enables parallel processing of different chain segments
- Allows graceful interruption and resumption

**Apply this pattern**:
```rust
// Define clear stages with isolated concerns
trait SyncStage {
    async fn execute(&mut self, input: StageInput) -> Result<StageOutput>;
    fn name(&self) -> &str;
}

// Pipeline stages, measure each independently
async fn sync_pipeline(stages: Vec<Box<dyn SyncStage>>) -> Result<()> {
    for stage in stages {
        let start = Instant::now();
        stage.execute(input).await?;
        info!("{} completed in {:?}", stage.name(), start.elapsed());
    }
}
```

### Database Design (MDBX)
Reth uses MDBX for high-performance storage:
- Memory-mapped files for fast random access
- Copy-on-write for ACID properties without write-ahead log
- Separate storage for historical vs current state

**Key principles**:
- Batch writes in transactions
- Use cursors for sequential access
- Design schema for access patterns (not normalization)
- Consider data layout: hot data together, cold data separate

### Component Modularity
Each Reth component is a standalone crate:
- `reth-primitives`: Core types (blocks, transactions)
- `reth-db`: Database abstractions
- `reth-revm`: EVM execution
- `reth-network`: P2P layer

**Apply this**:
- Design public APIs independent of implementation
- Use traits for pluggable components
- Document performance contracts
- Provide both sync and async variants when appropriate

## Critical Systems Standards

### Error Handling
- **Type-safe errors**: Use `thiserror` for domain errors
- **Context propagation**: Add context with `anyhow` or custom types
- **Fast path optimization**: `Result` in hot paths, panic for programmer errors
- **Structured logging**: Log errors with context for debugging

```rust
#[derive(Debug, thiserror::Error)]
enum ExecutionError {
    #[error("Invalid transaction: {0}")]
    InvalidTransaction(String),
    #[error("State error: {0}")]
    StateError(#[from] StateError),
}

// In hot paths, consider returning error codes instead of Result
// when you need every nanosecond
```

### Testing Strategy
- **Unit tests**: Test individual functions with property-based testing (`proptest`)
- **Integration tests**: Test component interactions
- **Benchmarks**: Use `criterion` for statistical rigor
- **Fuzzing**: Use `cargo-fuzz` for finding edge cases
- **Regression tests**: Lock in performance with benchmark CI gates

### Profiling & Measurement
1. **Start with high-level metrics**: What's actually slow?
2. **CPU profiling**: `cargo flamegraph` or `perf record`
3. **Memory profiling**: `valgrind --tool=massif` or `heaptrack`
4. **Cache analysis**: `perf stat -d` or `cachegrind`
5. **Benchmark**: `cargo bench` with statistical analysis

**Always measure before and after optimizations.**

## Code Review Checklist

For every performance-critical change:
- [ ] Benchmarked before and after?
- [ ] Allocations minimized? (checked with `cargo instruments` or `dhat`)
- [ ] Redundant work eliminated?
- [ ] Parallelization opportunities explored?
- [ ] Code is simple and maintainable?
- [ ] Error paths don't allocate unnecessarily?
- [ ] Public API documented with performance characteristics?
- [ ] Tests cover edge cases and validate correctness?
- [ ] Tracing/metrics added for production debugging?

## Quick Reference Commands

```bash
# Profile CPU usage
cargo flamegraph --bin your-binary

# Benchmark with statistical analysis
cargo bench --bench your-bench

# Check assembly output
cargo asm --bin your-binary path::to::function

# Memory profiling (Linux)
heaptrack ./target/release/your-binary

# Cache analysis
perf stat -d ./target/release/your-binary

# Check allocation sites
RUSTFLAGS="-Z print-type-sizes" cargo +nightly build --release
```

## Resources

- [Reth Repository](https://github.com/paradigmxyz/reth)
- [Rust Performance Book](https://nnethercote.github.io/perf-book/)
- [The Rust Async Book](https://rust-lang.github.io/async-book/)
- [Tokio Documentation](https://tokio.rs/)
- [Rayon Documentation](https://docs.rs/rayon/)
