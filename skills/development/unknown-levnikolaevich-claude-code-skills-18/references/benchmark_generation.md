<!-- SOURCE-OF-TRUTH: shared/references/benchmark_generation.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Benchmark Generation Guide

<!-- SCOPE: Auto-generating benchmarks for target functions when no existing benchmark exists. -->

Templates for generating minimal benchmarks per stack when no existing benchmark is found.

---

## When to Generate

| Condition | Action |
|-----------|--------|
| Existing `*_bench_test.go`, `*.bench.ts`, `conftest.py` with benchmark | Use existing |
| No benchmark found via ci_tool_detection.md | Generate from templates below |

---

## Templates by Stack

### Go

```go
// File: {target_file}_bench_test.go
package {package}

import "testing"

func Benchmark{FunctionName}(b *testing.B) {
    // Setup: prepare representative input
    input := {representative_input}

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        {FunctionName}(input)
    }
}
```

**Run:** `go test -bench=Benchmark{FunctionName} -benchmem -count=5 -run=^$ ./{package}`

### Python (pytest-benchmark)

```python
# File: test_{target}_benchmark.py
import pytest
from {module} import {function_name}

@pytest.fixture
def sample_input():
    """Representative input for benchmarking."""
    return {representative_input}

def test_{function_name}_benchmark(benchmark, sample_input):
    result = benchmark({function_name}, sample_input)
    assert result is not None
```

**Run:** `pytest test_{target}_benchmark.py --benchmark-only --benchmark-json=bench.json`

**Fallback (no pytest-benchmark):**
```python
# File: bench_{target}.py
import timeit
from {module} import {function_name}

input_data = {representative_input}
times = timeit.repeat(lambda: {function_name}(input_data), number=1000, repeat=5)
print(f"Median: {sorted(times)[2]:.6f}s")
```

### TypeScript (Vitest)

```typescript
// File: {target}.bench.ts
import { bench, describe } from 'vitest'
import { {functionName} } from './{target}'

describe('{functionName} benchmark', () => {
  const input = {representativeInput}

  bench('{functionName}', () => {
    {functionName}(input)
  })
})
```

**Run:** `npx vitest bench {target}.bench.ts`

### Rust

```rust
// File: benches/{target}_bench.rs
use criterion::{criterion_group, criterion_main, Criterion};
use {crate}::{function_name};

fn bench_{function_name}(c: &mut Criterion) {
    let input = {representative_input};
    c.bench_function("{function_name}", |b| b.iter(|| {function_name}(&input)));
}

criterion_group!(benches, bench_{function_name});
criterion_main!(benches);
```

**Run:** `cargo bench -- {function_name}`

### .NET (BenchmarkDotNet)

```csharp
// File: Benchmarks/{FunctionName}Benchmark.cs
using BenchmarkDotNet.Attributes;

[MemoryDiagnoser]
public class {FunctionName}Benchmark
{
    private {InputType} _input;

    [GlobalSetup]
    public void Setup() => _input = {representative_input};

    [Benchmark]
    public void {FunctionName}() => Target.{FunctionName}(_input);
}
```

**Run:** `dotnet run -c Release --project Benchmarks/`

---

## Input Selection

| Strategy | When |
|----------|------|
| Real data sample | Production-like data available |
| Worst-case input | Algorithmic complexity focus |
| Typical-case input | Average performance focus |
| Multiple sizes | Scaling behavior analysis |

**Rule:** Input must be deterministic (no random data in benchmarks).

---

## Cleanup

| Situation | Action |
|-----------|--------|
| All hypotheses removed | Delete generated benchmark file |
| Any optimization applied | Keep benchmark as regression guard |

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
