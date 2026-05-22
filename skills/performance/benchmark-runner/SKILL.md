# Benchmark Runner Workflow

Multi-step workflow for running performance benchmarks on ccswarm.

## Overview

This skill guides you through running, analyzing, and comparing performance benchmarks for the ccswarm system.

## Benchmark Types

### 1. Microbenchmarks
Fine-grained performance measurements for specific functions.

### 2. Integration Benchmarks
End-to-end performance for complete workflows.

### 3. Load Testing
System behavior under sustained load.

## Running Benchmarks

### 1. Setup
```bash
# Ensure criterion is available
cargo install cargo-criterion

# Build in release mode first
cargo build --release --workspace
```

### 2. Run All Benchmarks
```bash
# Run with criterion
cargo criterion --workspace

# Or standard bench
cargo bench --workspace
```

### 3. Run Specific Benchmarks
```bash
# By crate
cargo bench -p ccswarm

# By benchmark name
cargo bench --bench session_benchmark

# By filter
cargo bench -- "orchestrator"
```

## Benchmark Configuration

### Criterion Config
```rust
// benches/bench.rs
use criterion::{criterion_group, criterion_main, Criterion};

fn benchmark_task_delegation(c: &mut Criterion) {
    c.bench_function("delegate_task", |b| {
        b.iter(|| {
            // Benchmark code
        })
    });
}

criterion_group!(benches, benchmark_task_delegation);
criterion_main!(benches);
```

### Cargo.toml
```toml
[[bench]]
name = "orchestrator_bench"
harness = false
```

## Analysis

### 1. View Results
```bash
# Results are in target/criterion/
open target/criterion/report/index.html
```

### 2. Compare with Baseline
```bash
# Save baseline
cargo bench -- --save-baseline before

# Make changes, then compare
cargo bench -- --baseline before
```

### 3. Profiling
```bash
# With flamegraph
cargo flamegraph --bench orchestrator_bench

# With perf (Linux)
perf record cargo bench --bench orchestrator_bench
perf report
```

## Key Metrics

### Session Management
- Session creation time
- Context compression ratio
- Message throughput

### Orchestration
- Task delegation latency
- Agent assignment time
- Consensus round time

### Memory
- Peak memory usage
- Memory per agent
- Context size

## Benchmark Checklist

- [ ] Clean build before benchmarking
- [ ] Disable CPU frequency scaling
- [ ] Close other applications
- [ ] Run multiple iterations
- [ ] Compare with baseline
- [ ] Document results

## CI Integration

### GitHub Actions
```yaml
benchmark:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: dtolnay/rust-toolchain@stable
    - run: cargo bench -- --save-baseline ci
    - uses: actions/upload-artifact@v4
      with:
        name: benchmark-results
        path: target/criterion/
```

## Interpreting Results

### Good Performance
- < 1ms for task delegation
- < 100ms for full workflow
- < 10MB memory per agent

### Warning Signs
- High variance (> 20%)
- Memory growth over time
- Degradation vs baseline

## Optimization Workflow

1. Run baseline benchmark
2. Profile to identify hotspots
3. Implement optimization
4. Run comparison benchmark
5. Document improvements
