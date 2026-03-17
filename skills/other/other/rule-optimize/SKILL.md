---
name: rule-optimize
description: Workflow for modifying and benchmarking detection rules
disable-model-invocation: true
---

# Rule Optimization Workflow

Use after modifying rules in `default_rules.yaml` (loaded by `src/rules/`).

## Checklist

1. [ ] Run `cargo test` to verify no regressions
2. [ ] Build release: `RUSTFLAGS="-C target-cpu=native" cargo build --release`
3. [ ] Benchmark against test repos:
   ```bash
   ./target/release/scanner-rs ../linux ../gitleaks ../tigerbeetle ../trufflehog
   ```
4. [ ] Compare throughput/findings against baseline
5. [ ] Document anchor/keyword choice if non-obvious (add inline comment)

## Pattern Guidelines

When adding or modifying rules:

### Anchors
- Prefer structured prefixes (`sgp_`, `hvs.`, `AKIA`) over service name keywords
- Avoid generic patterns like `[a-fA-F0-9]{40}` that match git SHAs
- Add inline comments explaining non-obvious anchor/keyword choices

### Performance
- Test rule isolation: `cargo bench --bench rule_isolation -- <rule_id>`
- Check for backtracking: avoid `.*` followed by greedy quantifiers
- Prefer character classes over alternation when possible

### Validation
- Ensure validators don't make network calls in hot paths
- Use entropy checks for high-entropy secrets
- Add checksum validation where applicable (AWS keys, etc.)

## Baseline Comparison

Before making changes, capture baseline:
```bash
# Run 3x and record median throughput
for i in 1 2 3; do
  ./target/release/scanner-rs ../linux 2>&1 | tail -1
done
```

After changes, compare:
```bash
# Calculate % change
# Acceptable: <2% regression
# Investigate: 2-5% regression
# Block: >5% regression without justification
```

## Related Skills

- `/bench-compare` - Criterion benchmark comparison
- `/perf-regression` - Full performance regression workflow
- `/test-strategy` - Choose testing approach for rule changes
