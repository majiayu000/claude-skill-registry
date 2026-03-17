---
name: debugging-methodology
description: Master systematic debugging with proven techniques, profiling tools, and disciplined root cause analysis. Use when investigating bugs, test failures, performance issues, or unexpected behavior.
---

# Debugging Methodology

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Random fixes waste time and create new bugs. Complete Phase 1 before proposing fixes.

## The Four Phases

### Phase 1: Root Cause Investigation

**1. Read Error Messages Carefully**
- Read stack traces completely; note line numbers, file paths, error codes

**2. Reproduce Consistently**
- Can you trigger it reliably? Exact steps? Minimal reproduction?
- If not reproducible, gather more data -- don't guess

**3. Check Recent Changes**
- Git diff, recent commits, new dependencies, config changes

**4. Gather Evidence (Multi-Component Systems)**
```bash
# Trace at each component boundary
echo "=== Layer 1: Workflow ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

echo "=== Layer 2: Build script ==="
env | grep IDENTITY || echo "IDENTITY not in environment"
```

**5. Trace Data Flow** -- Where does bad value originate? Keep tracing up until you find the source.

### Phase 2: Pattern Analysis

1. Find working examples of similar code
2. Compare against references -- list every difference
3. Understand dependencies (settings, config, environment)

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis**: "I think X is the root cause because Y"
2. **Test Minimally**: Smallest possible change, one variable at a time
3. **Verify**: Worked? -> Phase 4. Didn't? -> NEW hypothesis (don't add more fixes)

### Phase 4: Implementation

1. **Create Failing Test** -- simplest possible reproduction, automated
2. **Implement Single Fix** -- ONE change at a time
3. **Verify** -- test passes? No other tests broken?

**If 3+ Fixes Failed**: Question architecture. STOP and discuss fundamentals.

---

## Debugging Tools

### JavaScript/TypeScript
```typescript
debugger;  // Pause execution
console.table(arrayOfObjects);
console.time('op'); /* code */ console.timeEnd('op');
console.trace();  // Stack trace
performance.mark('start'); /* code */ performance.mark('end');
performance.measure('op', 'start', 'end');
```

### Python
```python
breakpoint()  # Python 3.7+
# Post-mortem
try: risky_operation()
except: import pdb; pdb.post_mortem()
# Profile
import cProfile; cProfile.run('slow_function()', 'stats')
```

### Go
```go
import "runtime/debug"
debug.PrintStack()
// CPU profiling
import "runtime/pprof"
f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
```

---

## Advanced Techniques

### Git Bisect
```bash
git bisect start
git bisect bad                    # Current is bad
git bisect good v1.0.0            # This was good
git bisect good   # or bad, repeat until found
git bisect reset
```

### Differential Debugging

| Aspect | Working | Broken |
|--------|---------|--------|
| Environment | Dev | Prod |
| Node version | 18.16.0 | 18.15.0 |
| Data | Empty DB | 1M records |

---

## Patterns by Issue Type

- **Intermittent**: Add logging with timing, look for race conditions, stress test
- **Performance**: Profile first, common culprits: N+1, unnecessary re-renders, sync I/O
- **Production**: Gather evidence (Sentry/logs/metrics), reproduce locally, test fixes in staging

## Red Flags -- STOP and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too |
| "Emergency, no time" | Systematic is FASTER than thrashing |
| "Multiple fixes saves time" | Can't isolate what worked |
| "I see the problem" | Seeing symptoms != understanding root cause |

## Quick Debugging Checklist

- [ ] Spelling errors / typos
- [ ] Case sensitivity
- [ ] Null/undefined values
- [ ] Off-by-one errors
- [ ] Async timing / race conditions
- [ ] Scope issues / type mismatches
- [ ] Missing dependencies / env vars
- [ ] Cache issues
