---
name: flaky-detect
description: Identify flaky tests from CI history and test execution patterns. Use when debugging intermittent test failures, auditing test reliability, or improving CI stability.
version: 1.0.0
---

# Flaky Detect Skill

## Purpose

Identify flaky tests (tests that pass and fail non-deterministically) by analyzing CI history, execution patterns, and test characteristics. Google research shows 4.56% of tests are flaky, costing millions in developer productivity.

## Research Foundation

| Finding | Source | Reference |
|---------|--------|-----------|
| 4.56% flaky rate | Google (2016) | [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) |
| ML Classification | FlaKat (2024) | [arXiv:2403.01003](https://arxiv.org/abs/2403.01003) - 85%+ accuracy |
| LLM Auto-repair | FlakyFix (2023) | [arXiv:2307.00012](https://arxiv.org/html/2307.00012v4) |
| Flaky Taxonomy | Luo et al. (2014) | "An Empirical Analysis of Flaky Tests" |

## When This Skill Applies

- User reports "tests sometimes fail" or "intermittent failures"
- CI has been unstable or unreliable
- User wants to audit test suite reliability
- Pre-release quality assessment
- Debugging non-deterministic behavior

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Find flaky tests" | Analyze CI history for flaky patterns |
| "Why does CI keep failing?" | Identify flaky tests causing failures |
| "Test suite is unreliable" | Full flaky test audit |
| "This test sometimes passes" | Analyze specific test for flakiness |
| "Audit test reliability" | Comprehensive flaky detection |
| "Quarantine flaky tests" | Identify and isolate flaky tests |

## Flaky Test Taxonomy (Google Research)

| Category | Percentage | Root Causes |
|----------|------------|-------------|
| **Async/Timing** | 45% | Race conditions, insufficient waits, timeouts |
| **Test Order** | 20% | Shared state, execution order dependencies |
| **Environment** | 15% | File system, network, configuration differences |
| **Resource Limits** | 10% | Memory, threads, connection pools |
| **Non-deterministic** | 10% | Random values, timestamps, UUIDs |

## Detection Methods

### 1. CI History Analysis

Parse GitHub Actions / CI logs to find inconsistent results:

```python
def analyze_ci_history(repo, days=30):
    """Analyze CI runs for flaky patterns"""
    runs = get_ci_runs(repo, days)
    test_results = {}

    for run in runs:
        for test in run.tests:
            if test.name not in test_results:
                test_results[test.name] = {"pass": 0, "fail": 0}

            if test.passed:
                test_results[test.name]["pass"] += 1
            else:
                test_results[test.name]["fail"] += 1

    # Identify flaky tests (pass rate between 5% and 95%)
    flaky = []
    for test, results in test_results.items():
        total = results["pass"] + results["fail"]
        if total >= 5:  # Enough data
            pass_rate = results["pass"] / total
            if 0.05 < pass_rate < 0.95:
                flaky.append({
                    "test": test,
                    "pass_rate": pass_rate,
                    "total_runs": total
                })

    return sorted(flaky, key=lambda x: x["pass_rate"])
```

### 2. Code Pattern Analysis

Scan test code for flaky patterns:

```python
FLAKY_PATTERNS = [
    # Timing issues
    (r'setTimeout|sleep|delay', "timing", "Uses explicit delays"),
    (r'Date\.now\(\)|new Date\(\)', "timing", "Uses current time"),

    # Async issues
    (r'\.then\([^)]*\)(?!.*await)', "async", "Promise without await"),
    (r'async.*(?!await)', "async", "Async without await"),

    # Order dependencies
    (r'Math\.random\(\)', "random", "Uses random values"),
    (r'uuid|nanoid', "random", "Uses generated IDs"),

    # Environment
    (r'process\.env', "environment", "Environment-dependent"),
    (r'fs\.(read|write)', "environment", "File system access"),
    (r'fetch\(|axios\.|http\.', "network", "Network calls"),
]

def scan_for_flaky_patterns(test_file):
    """Scan test file for flaky patterns"""
    content = read_file(test_file)
    matches = []

    for pattern, category, description in FLAKY_PATTERNS:
        if re.search(pattern, content):
            matches.append({
                "category": category,
                "description": description,
                "pattern": pattern
            })

    return matches
```

### 3. Re-run Analysis

Run tests multiple times to detect flakiness:

```bash
# Run tests 10 times, track results
for i in {1..10}; do
  npm test -- --reporter=json >> test-results.jsonl
done

# Analyze for inconsistency
python analyze_reruns.py test-results.jsonl
```

## Output Format

```markdown
## Flaky Test Report

**Analysis Period**: Last 30 days
**Total Tests**: 450
**Flaky Tests Found**: 12 (2.7%)

### Critical Flaky Tests (< 50% pass rate)

#### 1. `test/api/login.test.ts:45`
**Pass Rate**: 42% (21/50 runs)
**Category**: Timing
**Pattern**: Uses `Date.now()` for token expiry

```typescript
// Flaky code
it('should expire token after 1 hour', () => {
  const token = createToken();
  const expiry = Date.now() + 3600000;  // Flaky!
  expect(token.expiresAt).toBe(expiry);
});
```

**Root Cause**: Test creates token and checks expiry in same millisecond sometimes, different millisecond other times.

**Recommended Fix**: Use mocked time
```typescript
it('should expire token after 1 hour', () => {
  vi.setSystemTime(new Date('2024-01-01T00:00:00Z'));
  const token = createToken();
  expect(token.expiresAt).toBe(new Date('2024-01-01T01:00:00Z').getTime());
  vi.useRealTimers();
});
```

### High Flaky Tests (50-80% pass rate)

#### 2. `test/db/connection.test.ts:23`
**Pass Rate**: 68% (34/50 runs)
**Category**: Resource
**Pattern**: Connection pool exhaustion

[... more tests ...]

### Summary by Category

| Category | Count | Impact |
|----------|-------|--------|
| Timing | 5 | HIGH |
| Async | 3 | HIGH |
| Environment | 2 | MEDIUM |
| Order | 1 | MEDIUM |
| Network | 1 | LOW |

### Recommendations

1. **Quick Win**: Fix 5 timing tests with `vi.setSystemTime()` (+0.5% stability)
2. **Medium Effort**: Add proper async handling (+0.3% stability)
3. **Infrastructure**: Add test isolation for DB tests (+0.2% stability)

### Quarantine Candidates

These tests should be skipped in CI until fixed:

```javascript
// vitest.config.ts
export default {
  test: {
    exclude: [
      'test/api/login.test.ts',       // Timing flaky
      'test/db/connection.test.ts',   // Resource flaky
    ]
  }
}
```

**Note**: Track quarantined tests in `.aiwg/testing/flaky-quarantine.md`
```

## Quarantine Process

### 1. Identify

```bash
# Run flaky detection
python scripts/flaky_detect.py --ci-history 30 --threshold 95
```

### 2. Quarantine

```javascript
// Mark test as flaky
describe.skip('flaky: login expiry', () => {
  // FLAKY: https://github.com/org/repo/issues/123
  // Root cause: timing-dependent
  // Fix in progress: PR #456
});
```

### 3. Track

Create tracking issue:
```markdown
## Flaky Test: test/api/login.test.ts:45

- **Pass Rate**: 42%
- **Category**: Timing
- **Root Cause**: Uses real system time
- **Quarantined**: 2024-12-12
- **Fix PR**: #456
- **Target Unquarantine**: 2024-12-15
```

### 4. Fix and Unquarantine

After fix:
```bash
# Verify fix with multiple runs
for i in {1..20}; do npm test -- test/api/login.test.ts; done

# Remove from quarantine if all pass
```

## Integration Points

- Works with `flaky-fix` skill for automated repairs
- Reports to CI dashboard
- Feeds into `/flow-gate-check` for release decisions
- Tracks in `.aiwg/testing/flaky-registry.md`

## Script Reference

### flaky_detect.py
Analyze CI history for flaky tests:
```bash
python scripts/flaky_detect.py --repo owner/repo --days 30
```

### flaky_scanner.py
Scan code for flaky patterns:
```bash
python scripts/flaky_scanner.py --target test/
```
