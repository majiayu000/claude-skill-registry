---
name: libperf
description: >
  libperf - Performance testing utilities. benchmark function measures execution
  time and memory. validateDuration and validateMemory assert performance
  constraints. ScalingAnalyzer detects linear vs sublinear scaling. PerfRunner
  orchestrates benchmark suites. Use for performance testing, benchmarking, and
  detecting performance regressions.
---

# libperf Skill

## When to Use

- Writing performance tests for critical code paths
- Benchmarking function execution time and memory
- Detecting performance regressions in CI
- Validating scaling characteristics (O(n) vs O(n²))

## Key Concepts

**benchmark**: Runs a function multiple times and collects timing/memory stats.

**validateDuration/validateMemory**: Assert that benchmarks meet performance
requirements.

**ScalingAnalyzer**: Analyzes how performance scales with input size.

## Usage Patterns

### Pattern 1: Basic benchmark

```javascript
import { benchmark, validateDuration } from "@copilot-ld/libperf";

const result = await benchmark(
  async () => {
    await myFunction(input);
  },
  { iterations: 100 },
);

validateDuration(result, 50); // Assert max 50ms
```

### Pattern 2: Scaling analysis

```javascript
import { ScalingAnalyzer } from "@copilot-ld/libperf";

const analyzer = new ScalingAnalyzer();
const scaling = await analyzer.analyze(fn, [100, 1000, 10000]);
// scaling.type: "linear" | "sublinear" | "superlinear"
```

## Integration

Performance tests use `.perf.js` extension. Run via `npm run test:perf`.
