---
name: kpi-verification-pass-rate
description: KPI for measuring first-pass verification success. Tracks how often verification passes on the first attempt. Use to reduce wasted cycles from verification failures.
---

# KPI: Verification Pass Rate

**Definition**: The percentage of times `./verify.sh` passes on the first attempt.

## Why This Matters

Every failed verification attempt:
- Wastes time re-running checks
- Indicates preventable issues
- Slows down the feedback loop

A high first-pass rate means fewer wasted cycles and faster development.

## Metrics

### Primary Metric
**First-Pass Success Rate** - Percentage of verification runs that pass without prior failures.

Formula:
```
Pass Rate = (Successful First Attempts) / (Total First Attempts) × 100%
```

### Target Benchmarks

| Performance | Pass Rate |
|-------------|-----------|
| Poor | <50% |
| Acceptable | 50-70% |
| Good | 70-90% |
| Excellent | >90% |

## Measurement

### Manual Tracking

Before each verify run, note:
- Is this the first attempt after changes?
- Did it pass or fail?
- What stage failed (format/lint/type/test/build)?

### Automated (Future)

Track via CI metrics when available.

## Improvement Strategies

### 1. Pre-flight Checks

Before running full verification, run quick checks:

```bash
# Quick lint check (fastest)
npm run lint:check

# Type check (catches most issues)
npm run typecheck
```

These catch ~80% of issues in seconds.

### 2. Incremental Testing

After each code change:
```bash
# Run affected tests only
npm run test -- --only-changed
```

### 3. IDE Integration

Configure your editor to show:
- Lint errors inline
- Type errors inline
- Format on save

Catch issues before you even run verify.

### 4. Dependency Validation

Before importing a package:
```bash
# Check if it exists and exports what you need
ls packages/<package-name>/src
```

Don't assume a port exists - verify first.

### 5. Learn from Failures

Each failure is data:
- What stage failed?
- What was the root cause?
- How could this have been prevented?

Record patterns in typescript-coding skill.

## Common Failure Patterns

| Stage | Common Causes | Prevention |
|-------|---------------|------------|
| Format | Forgot to format | Auto-format on save |
| Lint | Unused imports, missing types | Check lint before commit |
| Type | Wrong types, missing exports | Run typecheck frequently |
| Test | Logic errors, missing mocks | Write tests first |
| Build | Missing exports, circular deps | Check imports carefully |

## Pre-Verification Checklist

Before running `./verify.sh`:

- [ ] Code saved and formatted
- [ ] No lint errors in changed files
- [ ] Types look correct
- [ ] Tests updated for changes
- [ ] All imports resolve

## Anti-Patterns

- **"Verify and pray"** - Running verify.sh as your only check
- **Ignoring warnings** - Warnings often become errors
- **Mass changes** - Large changes = more failure modes
- **Skipping local verify** - CI failures are slower to debug
