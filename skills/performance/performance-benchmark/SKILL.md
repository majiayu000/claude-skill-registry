---
description: Runs performance benchmarks on YARS with long simulations to detect performance regressions
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Performance Benchmark

This skill runs performance benchmarks to measure simulation speed and detect performance regressions.

## Usage

Automatically invoked when:
- User asks to benchmark or test performance
- After optimization work
- Comparing performance before/after changes
- Validating that refactoring didn't slow down simulation

## Benchmark Tests

### Test 1: Braitenberg Extended Run
```bash
cd build
time timeout 120s ./bin/yars --iterations 10000 --xml ../xml/braitenberg_logging.xml
```

### Test 2: Falling Objects Physics Test
```bash
cd build
time timeout 120s ./bin/yars --iterations 10000 --xml ../xml/falling_objects.xml
```

## Success Criteria

- ✅ Simulations complete without timeout
- ✅ Time measurements recorded
- ✅ Performance within acceptable range
- ✅ No crashes during extended runs

## Reporting

Reports should include:
- Real/user/sys time for each test
- Iterations per second
- Comparison with previous benchmarks if available
- Any performance degradation warnings

## Notes

- Should be run with release build for accurate results
- Use timeout to prevent runaway simulations
- Benchmark results vary by hardware
- Track trends over time rather than absolute values
