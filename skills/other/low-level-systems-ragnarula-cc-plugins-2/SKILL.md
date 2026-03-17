---
name: low-level-systems
description: Use this skill when designing or reviewing systems programming, embedded systems, performance-critical code, or anything involving direct memory management, OS interfaces, or hardware interaction. Applies systems programming thinking to specifications, designs, and implementations.
version: 0.1.0
---

# Low-level Systems Engineering

## When to Apply

Use this skill when the system involves:
- Manual memory management or custom allocators
- Performance-critical hot paths
- Direct OS/kernel interfaces (syscalls, drivers)
- Embedded or resource-constrained environments
- FFI boundaries or ABI stability requirements
- Lock-free or wait-free data structures

## Mindset

Low-level systems experts think in terms of what the machine actually does, not abstractions.

**Questions to always ask:**
- What's the memory layout? Is it cache-friendly?
- Who owns this memory? When is it freed?
- What's the worst-case latency, not just average?
- Can this block? For how long?
- What happens on allocation failure?
- Is this code deterministic? Can it be preempted?
- What are the alignment requirements?

**Assumptions to challenge:**
- "Memory is abundant" - It's not in embedded, or when you're in a hot loop.
- "Allocation is cheap" - malloc can block, fragment, or fail.
- "The compiler optimizes it" - Verify. Read the assembly.
- "It's fast enough" - Profile. Measure cycles, cache misses, branch mispredicts.
- "Order doesn't matter" - Compilers and CPUs reorder. Use barriers.
- "Types are just types" - They have sizes, alignment, and ABI implications.

## Practices

### Memory Ownership
Every allocation has exactly one owner. Document ownership transfer explicitly. Use RAII or defer patterns for cleanup. **Don't** allocate without a clear free path, rely on garbage collection in hot paths, or leave ownership ambiguous.

### Allocation Strategy
Prefer stack allocation for small, fixed-size data. Use arenas or pools for same-lifetime objects. Pre-allocate where possible. **Don't** allocate in hot loops, use unbounded dynamic allocation in real-time contexts, or ignore allocation failure.

### Cache Efficiency
Keep hot data together. Prefer arrays of structs over pointer-chasing. Minimize cache line bouncing in concurrent code. **Don't** scatter related data across heap, use linked lists for traversal-heavy workloads, or ignore false sharing.

### Determinism
Bound all loops and recursion. Avoid dynamic allocation in deterministic contexts. Document worst-case execution time. **Don't** use unbounded operations in real-time code, ignore preemption, or assume consistent timing.

### Unsafe Boundaries
Isolate unsafe code into minimal, well-documented modules. Validate all inputs at boundaries. Wrap unsafe operations in safe interfaces. **Don't** scatter unsafe code throughout, skip bounds checks at FFI boundaries, or assume callers are trusted.

### ABI Stability
Freeze public struct layouts. Use opaque pointers for internal types. Version your interfaces. **Don't** change struct layout in stable APIs, expose internal types, or ignore calling conventions.

### Error Handling
Handle every error case explicitly. Prefer error codes over exceptions in C. Propagate errors; don't swallow them. **Don't** ignore return codes, panic in library code, or use exceptions across FFI boundaries.

### Concurrency Primitives
Use the weakest ordering that's correct. Prefer message passing over shared memory. Document synchronization requirements. **Don't** use SeqCst everywhere "to be safe", hold locks across blocking operations, or assume atomics are free.

## Vocabulary

Use precise terminology:

| Instead of | Say |
|------------|-----|
| "fast" | "O(1)" / "< 100 cycles" / "cache-resident" |
| "memory safe" | "no UB" / "bounds-checked" / "lifetime-safe" |
| "thread safe" | "atomic" / "lock-free" / "synchronized via X" |
| "efficient" | "zero-copy" / "in-place" / "stack-allocated" |
| "pointer" | "owning pointer" / "borrowed reference" / "raw pointer" |
| "call" | "blocking call" / "syscall" / "inline" |

## SDD Integration

**During Specification:**
- Ensure NFRs specify memory constraints, latency bounds, target platforms
- Flag requirements that imply unbounded resource usage
- Ask about failure modes for resource exhaustion

**During Design:**
- Document memory ownership for each component
- Specify allocation strategy (stack, arena, pool, heap)
- Identify hot paths and their performance budgets
- Define ABI boundaries and stability guarantees

**During Review:**
- Verify ownership is clear and cleanup is guaranteed
- Check for allocations in hot paths
- Validate unsafe code is isolated and documented
- Confirm error handling is exhaustive
