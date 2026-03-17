# Big Bang 80/20: Deterministic Receipts Skill

**Auto-trigger**: Whenever you see "validation", "test passed", "review", "evidence", "proof", "benchmark", "receipt"

## Core Concept

**Deterministic Receipts** replace human review with reproducible evidence.

Never say "code looks good". Instead say "[Receipt] cargo make lint passed with 0 warnings. [Receipt] All 347 tests passed. [Receipt] SLO check passed in 4.2s."

## The Anti-Pattern: Narrative Review

**❌ BAD**:
```
"I reviewed the code. It looks good. The error handling seems correct.
Performance should be fine. I think this is ready."
```

**Why it fails**:
- "Looks good" = opinion, not evidence
- "Should be fine" = guess, not measurement
- "I think" = belief, not proof
- Unreproducible (someone else might disagree)

## The Pattern: Receipts

**✅ GOOD**:
```
[Receipt] cargo make check: PASSED (0 errors, 0 warnings)
[Receipt] cargo make lint: PASSED (0 clippy violations)
[Receipt] cargo make test: PASSED (347/347 tests passed, 0 flaky)
[Receipt] cargo make slo-check: PASSED (check: 4.2s, test: 28s, lint: 58s)
[Receipt] Benchmark: parse_1000_files = 4.8s ± 0.2s (SLO: <5s) ✓
[Receipt] Memory profiling: peak 87MB < 100MB limit ✓
[Receipt] Coverage: 94% > 85% target ✓
```

**Why this works**:
- Reproducible (anyone can run `cargo make lint`)
- Measurable (0 violations, not "probably fine")
- Auditable (timestamps, version numbers)
- Objective (no opinion involved)

## Receipt Categories

### 1. Compilation Receipts

```bash
[Receipt] cargo make check: ✓ PASS (clean compilation)
[Receipt] RUSTFLAGS: -D warnings (deny all warnings)
[Receipt] Edition 2021, MSRV 1.75+
```

**Proves**: Code compiles error-free, no warnings.

### 2. Test Receipts

```bash
[Receipt] cargo make test: ✓ PASS
[Receipt] Results: 347/347 tests passed
[Receipt] Execution time: 28.2s
[Receipt] No flaky tests (re-run 3x, same results)
[Receipt] Test coverage: 94%
```

**Proves**: All tests pass, no flaky behavior, reasonable coverage.

### 3. Lint Receipts

```bash
[Receipt] cargo make lint: ✓ PASS
[Receipt] Clippy: 0 violations (all/pedantic/nursery/cargo denied)
[Receipt] Format: 0 changes needed (rustfmt)
[Receipt] Security audit: 0 vulnerabilities
[Receipt] Unwrap violations: 0 in production code
```

**Proves**: Code follows project standards, no dangerous patterns.

### 4. Performance Receipts

```bash
[Receipt] SLO Check: ✓ PASS
[Receipt] Compilation: 4.2s < 5s target ✓
[Receipt] Tests: 28.1s < 30s target ✓
[Receipt] Lint: 57.8s < 60s target ✓

[Receipt] Benchmarks (criterion):
  - parse_1000_files: 4.8s ± 0.2s (SLO: <5s) ✓
  - generate_code: 87ms ± 5ms (SLO: <100ms) ✓
  - cache_lookup: 0.3μs ± 0.02μs (SLO: <1μs) ✓

[Receipt] Memory profiling (valgrind):
  - Peak RSS: 87MB (limit: 100MB) ✓
  - Heap allocations: 1.2M (≤1.5M) ✓
```

**Proves**: Code meets performance targets, no regressions.

### 5. Integration Receipts

```bash
[Receipt] End-to-end tests: ✓ PASS
[Receipt] Integration with ggen-core: ✓ PASS
[Receipt] CLI smoke tests: ✓ PASS
[Receipt] Real-world scenario (fortune500): ✓ PASS
```

**Proves**: Code works with other systems, no integration issues.

### 6. Security Receipts

```bash
[Receipt] Path traversal check: ✓ PASS
[Receipt] SQL injection check: ✓ PASS
[Receipt] XSS vector analysis: ✓ PASS
[Receipt] Input validation: All user inputs sanitized
[Receipt] Error messages: No sensitive data leaked
[Receipt] Dependencies: cargo audit = 0 vulnerabilities
```

**Proves**: Code is secure, no common vulnerabilities.

## Receipt Checklist (Pre-Done)

Before marking work "done", collect receipts:

```json
{
  "compilation": {
    "cargo_make_check": "✓",
    "no_warnings": "✓",
    "rust_edition": "2021"
  },
  "tests": {
    "all_pass": "✓ 347/347",
    "no_flaky": "✓ (3 re-runs)",
    "coverage": "✓ 94%"
  },
  "linting": {
    "clippy": "✓ 0 violations",
    "rustfmt": "✓ formatted",
    "security_audit": "✓ 0 vulns"
  },
  "performance": {
    "compilation_time": "✓ 4.2s < 5s",
    "test_time": "✓ 28s < 30s",
    "slo_check": "✓ all pass"
  },
  "integration": {
    "cli_tests": "✓",
    "core_integration": "✓",
    "real_world": "✓"
  },
  "ready_for_merge": true
}
```

## Integration with ggen Toolchain

### Cargo Make Receipts

```bash
# Run full validation pipeline
cargo make pre-commit

# Receipt output:
# ✓ [00:04] cargo make check        (0 errors, 0 warnings)
# ✓ [00:58] cargo make lint         (0 clippy violations)
# ✓ [00:29] cargo make test-unit    (347/347 tests)
# ✓ [00:15] cargo make test         (all tests, 0 flaky)
# ✓ [00:32] cargo make bench        (SLOs met)
```

Each target produces timestamped, reproducible output = receipt.

### Test Receipts (Chicago TDD)

```rust
// Test passes → Receipt
#[test]
fn test_lockfile_upsert() {
    let manager = LockfileManager::new(temp_dir.path());
    manager.upsert("pkg", "1.0.0", "sha256", "url").unwrap();
    let entry = manager.get("pkg").unwrap().unwrap();
    assert_eq!(entry.version, "1.0.0");
}

// Test output = Receipt:
// test test_lockfile_upsert ... ok (0.003s)
```

State changed → invariant verified → Receipt generated.

### Andon Signal Receipts

```
RED signal detected:
[Receipt] error[E0382]: value used after move
[Receipt] Location: crates/ggen-core/src/lib.rs:142

ACTION: STOP. Fix immediately.

After fix:
[Receipt] cargo make check: ✓ PASS (compilation clean)
[Receipt] Andon cleared. Ready to continue.
```

## Using Receipts in Communication

### Before (No Evidence)
```
You: "I fixed the bug and the code looks good."
User: "How do you know it's fixed?"
You: "I tested it and it works."
User: "Did you run the full test suite?"
You: "No, just a few manual tests."
User: "Does it meet the SLOs?"
You: "Probably, seems fast."
```

### After (With Receipts)
```
You: "[Receipt] Bug fixed in ggen-core/src/lib.rs:142
[Receipt] cargo make check: ✓ (clean compilation)
[Receipt] cargo make test: ✓ (347/347 tests pass, including regression test)
[Receipt] cargo make slo-check: ✓ (all SLOs met)
[Receipt] Related tests: test_lockfile_upsert, test_path_validation
[Receipt] No performance regression (same benchmarks as before)"

User: "Great, ready to merge."
```

**Reproducible, measurable, objectively correct.**

## Types of Invalid Receipts

❌ **Don't use these**:

| Invalid | Why | Better Receipt |
|---------|-----|-----------------|
| "Code looks good" | Opinion | [Receipt] cargo make lint: ✓ |
| "Tests should pass" | Prediction | [Receipt] cargo make test: ✓ |
| "I checked it works" | Anecdotal | [Receipt] All 347 tests pass |
| "Performance is fine" | Vague | [Receipt] Parse 1000 files: 4.8s (SLO <5s) ✓ |
| "No security issues" | Assumed | [Receipt] cargo audit: 0 vulnerabilities ✓ |

✅ **Use these**:

- `[Receipt] cargo make X: ✓ PASS`
- `[Receipt] Test result: N/M passed`
- `[Receipt] Benchmark: metric = value (target) ✓/✗`
- `[Receipt] Coverage: N% > target N% ✓`
- `[Receipt] Timestamp: [date] [version]`

## Audit Trail

Receipts create an **auditable trail**:

```
Commit 507d111
Date: 2026-01-03 18:00:15
Receipt: cargo make check ✓
Receipt: cargo make test ✓ (347/347)
Receipt: cargo make slo-check ✓
Receipt: SLO times: check 4.2s, test 28s, lint 58s
Status: VERIFIED GOOD ✓
```

Anyone can replay: `git checkout 507d111 && cargo make pre-commit`

Same output = Code is reproducibly correct.

## Receipts for Convergence

In EPIC 9 convergence:

```
Candidate 1 (Agent 3):
  [Receipt] cargo make check: ✓
  [Receipt] cargo make test: ✓ (340/347)
  [Receipt] cargo make lint: ✗ (5 clippy violations)
  [Receipt] Benchmark: 6.2s (SLO <5s) ✗
  Score: Fails lint + performance

Candidate 2 (Agent 7):
  [Receipt] cargo make check: ✓
  [Receipt] cargo make test: ✓ (347/347)
  [Receipt] cargo make lint: ✓ (0 violations)
  [Receipt] Benchmark: 4.8s (SLO <5s) ✓
  Score: Perfect

Decision: Select Candidate 2 (all receipts passing)
```

Selection pressure is deterministic, measurable, reproducible.

## Key Takeaway

**Evidence > Narrative**
**Receipts > Review**
**Reproducible > Opinion**
**Measurable > Vague**

Replace "I think it's good" with "[Receipt] cargo make pre-commit: ✓ PASS"
