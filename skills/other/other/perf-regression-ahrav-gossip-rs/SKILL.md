---
name: perf-regression
description: Performance regression testing workflow for hot path changes
user-invocable: false
---

# Performance Regression Workflow

**IMPORTANT**: Follow this workflow before merging any feature that touches hot paths (`src/engine/`, regex changes, validation logic).

## When This Applies

Invoke this skill when modifying:
- `src/engine/` modules (scratch.rs, stream_decode.rs, work_items.rs)
- Regex patterns or validation logic
- Data structures in `src/stdx/`
- Rule definitions in `default_rules.yaml` or `src/rules/`

## Workflow Steps

### 1. Stash Changes and Build Baseline

```bash
git stash push -m "feature-name"
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

### 2. Run Baseline Scans (3x each)

```bash
for i in 1 2 3; do
  ./target/release/scanner-rs ../gitleaks 2>&1 | tail -1
  ./target/release/scanner-rs ../linux 2>&1 | tail -1
  ./target/release/scanner-rs ../tigerbeetle 2>&1 | tail -1
done
```

Record average throughput for each repository.

### 3. Run Baseline Benchmarks

```bash
cargo bench --bench scanner_throughput -- --save-baseline before
cargo bench --bench vectorscan_overhead -- --save-baseline before
```

### 4. Restore Changes and Rebuild

```bash
git stash pop
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

### 5. Run Comparison Scans and Benchmarks

```bash
# Same scan loop as step 2
for i in 1 2 3; do
  ./target/release/scanner-rs ../gitleaks 2>&1 | tail -1
  ./target/release/scanner-rs ../linux 2>&1 | tail -1
  ./target/release/scanner-rs ../tigerbeetle 2>&1 | tail -1
done

# Compare against baseline
cargo bench --bench scanner_throughput -- --baseline before
cargo bench --bench vectorscan_overhead -- --baseline before
```

### 6. Analyze Results

Calculate average throughput delta per repository:

```
% change = (after_throughput - baseline_throughput) / baseline_throughput * 100
```

## Acceptance Criteria

| Regression Level | Action |
|------------------|--------|
| None (<2%) | Ship as-is |
| Minor (2-5%) | Document reason, acceptable for correctness |
| Moderate (5-10%) | Requires compelling justification |
| Major (>10%) | Must investigate and optimize |

## PR Documentation

Include in PR description:
- Average throughput delta per test repository
- Criterion benchmark comparison summary
- Justification for any regression >2%

## Output Format

Report results as:

```markdown
## Performance Regression Results

### Scan Throughput

| Repository | Baseline | After | Delta |
|------------|----------|-------|-------|
| gitleaks | X MB/s | Y MB/s | +/-Z% |
| linux | X MB/s | Y MB/s | +/-Z% |
| tigerbeetle | X MB/s | Y MB/s | +/-Z% |

### Criterion Benchmarks

[Paste relevant benchmark comparison output]

### Verdict

[None/Minor/Moderate/Major] regression - [justification if >2%]
```
