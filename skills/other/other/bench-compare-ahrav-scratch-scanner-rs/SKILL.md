---
name: bench-compare
description: Run Criterion benchmarks with baseline comparison for performance optimization work
---

# Benchmark Comparison Workflow

Compare benchmark results against a baseline to measure optimization impact.

## Usage

Invoke with optional benchmark filter:
- `/bench-compare` - Run all benchmarks
- `/bench-compare scan` - Run only scan-related benchmarks
- `/bench-compare throughput` - Run throughput benchmarks

## Workflow

### 1. Establish Baseline

Before making changes, save current benchmark results:

```bash
cargo bench --bench <name> -- --save-baseline before
```

Or for all benchmarks:
```bash
cargo bench -- --save-baseline before
```

### 2. Apply Changes

Make the optimization changes to the codebase.

### 3. Compare Results

Run benchmarks against the saved baseline:

```bash
cargo bench --bench <name> -- --baseline before
```

### 4. Analyze Output

Look for these patterns in Criterion output:
- `Performance has improved` - Optimization successful
- `Performance has regressed` - Changes hurt performance
- `No change in performance` - Within noise threshold

### 5. Report Summary

Provide a summary table:

| Benchmark | Before | After | Change |
|-----------|--------|-------|--------|
| name      | X ns   | Y ns  | -Z%    |

## Available Benchmarks

The project has these benchmark files in `benches/`:
- `scan.rs` - Core scanning performance
- `scanner_throughput.rs` - End-to-end throughput
- `vectorscan_overhead.rs` - Vectorscan integration overhead
- `rule_isolation.rs` - Per-rule cost isolation
- `hotspots.rs` - Known hot path benchmarks (requires `bench` feature)
- `validator.rs` - Validation step benchmarks (requires `bench` feature)
- Data structure benchmarks: `ring_buffer`, `fixed_set`, `fixed_vec`, `timing_wheel`, etc.

## Tips

- Use `--bench <name>` to run specific benchmarks for faster iteration
- The `hotspots` and `validator` benches require: `cargo bench --features bench`
- For memory bandwidth tests, use `memory_bandwidth.rs`
- Compare multiple runs to account for variance
