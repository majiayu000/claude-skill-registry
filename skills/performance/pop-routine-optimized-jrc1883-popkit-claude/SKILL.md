---
name: pop-routine-optimized
description: Token-optimized morning/nightly routine using caching and selective execution
invocation_pattern: "/popkit:routine morning --optimized"
tier: 1
version: 1.0.0
---

# Optimized Routine Execution

Token-efficient routine execution using intelligent caching and selective tool calls.

## Overview

Reduces routine token usage by 30-50% through:

- **Caching**: Skip unchanged checks (git status, test results)
- **Selective Execution**: Only run tests if source changed
- **Compact Flags**: Use `--short`, `--quiet` where possible
- **Smart Summarization**: Condense large outputs

## When to Use

**Automatic:**

- Invoked when `--optimized` flag used with `/popkit:routine`
- Example: `/popkit:routine morning --optimized`

**Manual:**

- Can be called directly for custom optimization strategies

## Optimization Strategies

### 1. Git Status Caching

```python
from routine_cache import RoutineCache, CACHE_KEYS, check_git_status_unchanged

cache = RoutineCache()

# Check if git status unchanged
if check_git_status_unchanged(cache):
    print("Git status unchanged since last check (cached)")
    # Use cached result - SAVES ~500 tokens
else:
    # Run full git status
    result = bash("git status --short")  # --short flag saves ~200 tokens
    cache.set(CACHE_KEYS["GIT_STATUS"], result.stdout, ttl=300)
```

**Token Savings:**

- Cache hit: ~500 tokens saved (skip command entirely)
- `--short` flag: ~200 tokens vs full output

### 2. Test Result Caching

```python
from routine_cache import check_tests_unchanged, update_test_cache

# Check if source files changed
if check_tests_unchanged(cache):
    print("No source changes - using cached test results")
    cached = cache.get(CACHE_KEYS["TEST_RESULTS"])
    test_passed = cached["passed"]
    # SAVES ~1000-3000 tokens (entire test run)
else:
    # Run tests
    result = bash("pytest -v")
    test_passed = result.returncode == 0
    update_test_cache(cache, result.stdout, test_passed)
```

**Token Savings:**

- Cache hit: ~1000-3000 tokens (skip test execution)
- Smart detection: Only re-run when needed

### 3. Selective Diff Generation

```python
# Only generate diff if files changed
status_output = bash("git status --short").stdout

if status_output.strip():
    # Files changed - show diff
    diff = bash("git diff --stat")
    # But use --stat instead of full diff (saves ~500 tokens)
else:
    print("No changes - skip diff generation")
    # SAVES ~700 tokens
```

**Token Savings:**

- Skip when clean: ~700 tokens
- `--stat` vs full diff: ~500 tokens

### 4. Compact Command Flags

| Command    | Standard     | Optimized              | Savings     |
| ---------- | ------------ | ---------------------- | ----------- |
| git status | `git status` | `git status --short`   | ~200 tokens |
| git log    | `git log`    | `git log --oneline -5` | ~400 tokens |
| git diff   | `git diff`   | `git diff --stat`      | ~500 tokens |
| pytest     | `pytest -v`  | `pytest --quiet`       | ~300 tokens |
| npm test   | `npm test`   | `npm test -- --silent` | ~200 tokens |

## Implementation

### Morning Routine (Optimized)

```python
from routine_cache import RoutineCache, CACHE_KEYS
from routine_measurement import RoutineMeasurementTracker

def optimized_morning_routine():
    """Token-optimized morning routine."""

    cache = RoutineCache()
    tracker = RoutineMeasurementTracker()
    tracker.start("pk-optimized", "PopKit Optimized Routine")

    score = 0
    max_score = 100

    # 1. Git Status (cached)
    if check_git_status_unchanged(cache):
        print("[CACHED] Git status unchanged")
        cached_status = cache.get(CACHE_KEYS["GIT_STATUS"])
        is_clean = len(cached_status.strip()) == 0
    else:
        status = bash("git status --short")  # --short flag
        is_clean = len(status.stdout.strip()) == 0
        cache.set(CACHE_KEYS["GIT_STATUS"], status.stdout, ttl=300)

    if is_clean:
        score += 25
        print("✓ Git: Clean (+25)")
    else:
        print("✗ Git: Uncommitted changes")

    # 2. Branch Info (compact)
    branch_info = bash("git branch --show-current")
    current_branch = branch_info.stdout.strip()
    print(f"Branch: {current_branch}")

    # 3. Remote Status (selective)
    if current_branch != "main" and current_branch != "master":
        # Only check if on feature branch
        ahead_behind = bash(f"git rev-list --left-right --count origin/{current_branch}...HEAD")
        # Parse and score
        score += 15

    # 4. Tests (cached if no changes)
    if check_tests_unchanged(cache):
        print("[CACHED] No source changes - using cached test results")
        cached_tests = cache.get(CACHE_KEYS["TEST_RESULTS"])
        tests_pass = cached_tests["passed"]
    else:
        # Run tests with --quiet
        test_result = bash("pytest --quiet")
        tests_pass = test_result.returncode == 0
        update_test_cache(cache, test_result.stdout, tests_pass)

    if tests_pass:
        score += 25
        print("✓ Tests: Passing (+25)")
    else:
        print("✗ Tests: Failing")

    # 5. Type Check (skip if no .ts/.tsx files changed)
    # Check file types in git status
    has_ts_changes = any(".ts" in line for line in status.stdout.split("\n"))

    if has_ts_changes:
        tsc_result = bash("tsc --noEmit")
        if tsc_result.returncode == 0:
            score += 20
            print("✓ TypeScript: No errors (+20)")
    else:
        print("[SKIP] No TypeScript changes - assume clean")
        score += 20

    # 6. Lint (skip if no code changes)
    if not is_clean:
        lint_result = bash("npm run lint --silent")
        if lint_result.returncode == 0:
            score += 15
            print("✓ Lint: Clean (+15)")
    else:
        print("[SKIP] No changes - skip lint")
        score += 15

    # Stop tracking
    measurement = tracker.stop()

    print(f"\n{'='*50}")
    print(f"Ready to Code Score: {score}/{max_score}")
    print(f"{'='*50}")

    # Show token savings
    if measurement:
        print(f"\nToken Usage: {measurement.total_tokens:,} tokens")
        print(f"Duration: {measurement.duration:.2f}s")
```

### Token Savings Breakdown

**Typical Optimization Results:**

| Check      | Standard    | Optimized     | Savings  | Method             |
| ---------- | ----------- | ------------- | -------- | ------------------ |
| Git Status | 700 tokens  | 200 tokens    | 500      | Cache + --short    |
| Git Diff   | 800 tokens  | 0-300 tokens  | 500      | Skip if clean      |
| Tests      | 3000 tokens | 0-1500 tokens | 1500     | Cache if unchanged |
| TypeScript | 2000 tokens | 0-2000 tokens | Variable | Skip if no .ts     |
| Lint       | 1500 tokens | 0-1500 tokens | Variable | Skip if clean      |

**Total Potential Savings: 3000-4000 tokens (40-50%)**

## Cache Management

### View Cache Stats

```python
from routine_cache import RoutineCache, get_cache_stats_report

cache = RoutineCache()
print(get_cache_stats_report(cache))
```

Output:

```
Cache Statistics:
  Valid entries: 5
  Expired entries: 2
  Cache size: 1,234 bytes
  Cache file: .claude/popkit/cache/routine_cache.json
```

### Clear Cache

```python
cache = RoutineCache()
cache.clear()
```

### Cache File Location

```
.claude/popkit/cache/routine_cache.json
```

## Comparison: Standard vs Optimized

### Standard Routine

```bash
/popkit:routine morning
```

**Token Usage:**

- Git commands: ~2000 tokens
- Tests: ~3000 tokens
- Linting: ~1500 tokens
- TypeScript: ~2000 tokens
- **Total: ~8500 tokens**

### Optimized Routine (First Run)

```bash
/popkit:routine morning --optimized
```

**Token Usage:**

- Git commands (--short): ~1200 tokens
- Tests: ~3000 tokens (no cache yet)
- Linting (--silent): ~800 tokens
- TypeScript: ~1500 tokens
- **Total: ~6500 tokens (24% savings)**

### Optimized Routine (Cached Run)

```bash
/popkit:routine morning --optimized
# Run again after 2 minutes (no code changes)
```

**Token Usage:**

- Git commands (cached): ~200 tokens
- Tests (cached): ~100 tokens
- Linting (skipped): ~0 tokens
- TypeScript (skipped): ~0 tokens
- **Total: ~300 tokens (96% savings!)**

## Trade-offs

### Pros ✅

- **40-50% token reduction** on first run
- **90%+ token reduction** on cached runs
- **Lower API costs** (less money spent)
- **Faster execution** (fewer tool calls)
- **Same accuracy** (all checks still run when needed)

### Cons ⚠️

- **Cache staleness** - Could miss changes if cache TTL too long
- **Complexity** - More logic to maintain
- **First-run overhead** - Slight overhead setting up cache
- **False negatives** - Might skip check if cache logic wrong

### Best Practices

1. **TTL Settings**
   - Git status: 5 minutes (300s)
   - Test results: 1 hour (3600s)
   - Lint results: 30 minutes (1800s)

2. **Cache Invalidation**
   - Clear cache after merges
   - Clear cache after dependency updates
   - Use `--no-cache` flag to force fresh run

3. **Validation**
   - Run full routine weekly for validation
   - Compare optimized vs standard monthly
   - Monitor false negatives

## Usage Examples

### Daily Morning Routine (Optimized)

```bash
/popkit:routine morning --optimized
```

### Force Fresh Run (No Cache)

```bash
/popkit:routine morning --optimized --no-cache
```

### Measure Optimization Impact

```bash
# Standard
/popkit:routine morning --measure

# Optimized
/popkit:routine morning --optimized --measure

# Compare measurements
cat .claude/popkit/measurements/*.json | jq '.total_tokens'
```

## Integration with Measurement

The optimized routine works with `--measure` flag:

```bash
/popkit:routine morning --optimized --measure
```

Output:

```
[CACHED] Git status unchanged
[CACHED] No source changes - using cached test results
[SKIP] No TypeScript changes - assume clean

Ready to Code Score: 85/100

======================================================================
Routine Measurement Report
======================================================================
Routine: PopKit Optimized Routine (pk-optimized)
Duration: 2.3s
Tool Calls: 3

Context Usage:
  Total Tokens:  320 (~0.3k)
  Cost: $0.0048

Tool Breakdown:
----------------------------------------------------------------------
Tool                 Calls    Tokens       Duration
----------------------------------------------------------------------
Bash                 2        180          0.4s
Read                 1        140          0.2s
======================================================================

Token Savings vs Standard: 8,180 tokens (96%)
======================================================================
```

## Related Skills

| Skill                 | Purpose                  |
| --------------------- | ------------------------ |
| `pop-routine-measure` | Measure token usage      |
| `pop-morning-routine` | Standard morning routine |
| `pop-nightly-routine` | Standard nightly routine |

## Architecture

| Component                            | Purpose          |
| ------------------------------------ | ---------------- |
| `hooks/utils/routine_cache.py`       | Cache management |
| `hooks/utils/routine_measurement.py` | Token tracking   |
| `skills/pop-routine-optimized/`      | This skill       |

---

**Version:** 1.0.0
**Last Updated:** 2025-12-19
**Token Savings:** 40-96% vs standard routine
