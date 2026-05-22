---
name: lcov
description: LCOV tooling - finding gaps, parsing coverage files, marker syntax
---

# LCOV Tooling

## Finding Coverage Gaps

```bash
# Run coverage first
make check-coverage

# Uncovered lines
grep "^DA:" reports/coverage/coverage.info | grep ",0$"

# Uncovered branches
grep "^BRDA:" reports/coverage/coverage.info | grep ",0$"

# Uncovered functions
grep "^FNDA:0," reports/coverage/coverage.info
```

## coverage.info Format

```
SF:/path/to/file.c          # Source file
FN:42,function_name         # Function at line 42
FNDA:5,function_name        # Function called 5 times
DA:45,3                     # Line 45 executed 3 times
DA:46,0                     # Line 46 never executed (GAP!)
BRDA:50,0,0,2               # Line 50, block 0, branch 0, taken 2 times
BRDA:50,0,1,0               # Line 50, block 0, branch 1, never taken (GAP!)
end_of_record
```

Key patterns:
- `DA:line,0` = uncovered line
- `BRDA:line,block,branch,0` = uncovered branch
- `FNDA:0,name` = uncovered function

## Coverage Files

| Command | Output |
|---------|--------|
| `make check-coverage` | `reports/coverage/coverage.info`, `reports/coverage/summary.txt` |
| `make check-coverage TEST=unit/foo` | `reports/coverage/unit/foo.coverage.info`, `.coverage.txt` |

## Exclusion Markers

| Marker | Effect |
|--------|--------|
| `LCOV_EXCL_LINE` | Exclude entire line |
| `LCOV_EXCL_BR_LINE` | Exclude branch only |
| `LCOV_EXCL_START` / `LCOV_EXCL_STOP` | Block exclusion (wrapper.c only) |

Usage:
```c
assert(ptr != NULL);                    // LCOV_EXCL_BR_LINE
if (!ptr) PANIC("Invariant violated");  // LCOV_EXCL_BR_LINE
```

**Note:** Markers are NOT reliably honored inside `static` functions. Inline code instead.

See `coverage` skill for exclusion policy (what's allowed vs forbidden).

## Quick Workflow

```bash
# 1. Run coverage
make check-coverage

# 2. Check summary
cat reports/coverage/summary.txt

# 3. Find gaps in specific file
grep -A 1000 "SF:.*myfile.c" reports/coverage/coverage.info | \
  grep -m 1 -B 1000 "end_of_record" | grep ",0$"
```

## Related Skills

- `coverage` - Policy (100% requirement, exclusion rules)
- `testability` - Refactoring patterns for gaps
