---
name: 145-java-refactoring-high-performance
description: Use when you need to refactor Java code for high performance — including memory/allocation reduction, CPU hot-path optimization, and syntax/API/control-flow improvements. This should trigger for requests such as Review Java code for high performance; Optimize Java hot path; Reduce Java allocations; Improve Java latency/throughput. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java rules for High Performance

Identify and apply practical Java high-performance techniques using a measure-first approach, with emphasis on allocation reduction, data layout, concurrency discipline, and evidence-based validation.

**What is covered in this Skill?**

- Measure-first workflow for Java code optimization
- JVM/runtime-aware coding guidance
- Allocation reduction techniques with bad/good patterns
- CPU hot-path simplification and loop-level efficiency patterns
- Concurrency/backpressure and timeout/cancellation discipline
- I/O, parsing, and serialization efficiency patterns
- Persistence/query and caching strategy guidance
- Java-centric decision workflow: keep/revert based on measured impact

**Scope:** Practical optimization in application code and APIs. Apply only where profiling indicates real bottlenecks.

## Constraints

Performance optimization must be evidence-driven and safe, focused on Java code changes that preserve correctness and maintainability.

- **MEASURE-FIRST**: Establish baseline behavior and identify Java code hot paths before optimization
- **NO PREMATURE OPTIMIZATION**: Only optimize code paths identified by profiling evidence
- **BEFORE APPLYING**: Read the relevant reference(s) for bad/good examples and measurement workflow
- **EDGE CASE**: If hotspot evidence is unclear, ask clarifying questions before changing code

## When to use this skill

- Review Java code for high performance
- Optimize Java hot path
- Reduce Java allocations
- Improve Java latency
- Improve Java throughput

## Workflow

1. **Identify Java hotspot and baseline behavior**

Confirm the performance-sensitive Java path and baseline behavior before changing code.

2. **Select the relevant reference(s) by bottleneck**

Pick and read only the reference(s) matching the observed hotspot: `references/145-refactoring-high-performance-java-memory-allocation.md` for allocation pressure, primitives vs. wrappers, escape analysis, collection sizing, data layout, and deduplication; `references/145-refactoring-high-performance-java-cpu.md` for CPU-bound hot paths, bit-level parsing, branchless arithmetic, loop unrolling, Unsafe caution, and SIMD/vectorization; `references/145-refactoring-high-performance-java-code-syntax.md` for code shape, lambdas, API return conventions, parsing syntax, I/O strategy, concurrency, and control-flow improvements.

3. **Apply targeted optimizations**

Implement minimal, evidence-backed changes scoped to the chosen domain(s): memory/allocation, CPU/low-level, or code shape/control flow (and adjacent concurrency, I/O, and persistence/caching in Java code).

4. **Validate and compare code-level outcomes**

Compare before/after behavior and keep only Java code changes with meaningful, verified gains.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/145-refactoring-high-performance-java-memory-allocation.md](references/145-refactoring-high-performance-java-memory-allocation.md)
- [references/145-refactoring-high-performance-java-cpu.md](references/145-refactoring-high-performance-java-cpu.md)
- [references/145-refactoring-high-performance-java-code-syntax.md](references/145-refactoring-high-performance-java-code-syntax.md)
