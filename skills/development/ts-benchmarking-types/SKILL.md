---
name: benchmarking-types
description: Guidance for measuring TypeScript type instantiations using @ark/attest. Use when optimizing type-level performance, writing type benchmarks, or debugging slow type evaluation.
---

# Benchmarking Types with @ark/attest

Measure TypeScript type instantiations to optimize type-level performance.

## Critical Concepts

### Baseline Expression

Include a "baseline expression" at the top of benchmark files to exclude API setup overhead.

* The baseline warms up the type evaluation machinery and caches common type computations
* __CRITICAL__: The baseline expression must be __different__ from any benchmark expression
* If the baseline is identical to a benchmark, that benchmark will reuse cached types → 0 instantiations (false result)

### Type Caching

TypeScript caches type evaluations __per exact type__:

* `Simplify.All<Map<1, 2>>` and `Simplify.All<Map<3, 4>>` are different → no caching benefit
* If baseline uses `Simplify.All<Map<0, 0>>` and benchmark uses `Simplify.All<Map<0, 0>>` → cached (low instantiations)
* Use similar but distinct types in baseline vs benchmarks

### Instantiation Costs

* Each benchmark measures instantiations for that specific expression in isolation
* Costs are __not cumulative__ - every expression re-evaluates from scratch (except cached types)
* Complex pattern matches (e.g., `Map<K, V> extends Map<infer K2, infer V2>`) can be expensive (~1800+ inst)

## Example

```typescript
import { bench } from '@ark/attest'
import { type } from 'arktype'

// Baseline expression - similar to benchmarks but not identical
type('boolean')

bench('single-quoted', () => {
  const _ = type("'nineteen characters'")
  // Would be 2697 without baseline, now 610
}).types([610, 'instantiations'])

bench('keyword', () => {
  const _ = type('string')
  // Would be 2507 without baseline, now 356
}).types([356, 'instantiations'])
```

## Best Practices

* Always include a baseline that exercises your API but with different inputs than benchmarks
* Use `.bench-d.ts` suffix for type benchmark files (convention)
* Benchmark files are type-only - no runtime execution
* Update baseline values when intentionally changing performance characteristics
* Beware: Complex built-in types (Map, Set) have inherent pattern-matching costs in TypeScript

## Resources

* [arktype attest documentation](https://github.com/arktypeio/arktype/tree/main/ark/attest)
