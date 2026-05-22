---
name: quality-complexity-check
description: Analyze code complexity metrics including cyclomatic complexity and nesting depth. Use to identify code that needs refactoring.
mcp_fallback: none
category: quality
agent: test-engineer
user-invocable: false
---

# Complexity Check Skill

Analyze and report code complexity metrics.

## When to Use

- Code review process
- Identifying refactoring candidates
- Maintaining code quality
- Before major releases

## Quick Reference

```bash
# Analyze Python code
./scripts/check_complexity.py

# Generate full report
./scripts/complexity_report.sh > complexity.txt

# Check Mojo code
./scripts/check_mojo_complexity.sh
```

## Complexity Metrics

### Cyclomatic Complexity (CC)

Measures decision points (if, for, while):

| CC Range | Assessment | Action |
|----------|------------|--------|
| 1-10 | Simple | Keep as is |
| 11-20 | Moderate | Consider refactoring |
| 21+ | Complex | Needs refactoring |

### Nesting Depth

Maximum levels of nesting in function:

| Depth | Assessment | Action |
|-------|------------|--------|
| 1-3 | Good | Keep as is |
| 4-5 | High | Consider flattening |
| 6+ | Very High | Refactor required |

### Function Length

Lines of code in function:

| LOC | Assessment | Action |
|-----|------------|--------|
| 1-20 | Good | Keep as is |
| 21-50 | Acceptable | Monitor |
| 51+ | Too long | Consider splitting |

## Refactoring Patterns

### Extract Function (High CC)

```python
# Before (CC: 15)
def process(data):
    if condition1:
        if condition2:
            if condition3:
                for item in data:
                    if item.valid:
                        # process

# After (CC: 5)
def process(data):
    if not is_valid(data):
        return
    filtered = filter_valid_items(data)
    return process_items(filtered)
```

### Flatten Nesting

Replace nested ifs with early returns:

```python
# Before (depth: 5)
fn process(data):
    if check1(data):
        if check2(data):
            if check3(data):
                # complex logic

# After (depth: 2)
fn process(data):
    if not check1(data): return
    if not check2(data): return
    if not check3(data): return
    # complex logic
```

## Workflow

```bash
# 1. Analyze code
./scripts/check_complexity.py

# 2. Review high-complexity functions
grep "CC:" complexity.txt | grep -E "CC: [2-9][0-9]|CC: [1-9][0-9]{2}"

# 3. Plan refactoring
# ... extract functions, flatten nesting ...

# 4. Re-analyze
./scripts/check_complexity.py

# 5. Verify improved
git diff complexity.txt
```

## Error Handling

| Issue | Fix |
|-------|-----|
| Script not found | Check `scripts/` directory |
| Syntax errors | Fix code syntax before analyzing |
| No output | Verify source files exist |

## Thresholds

Project thresholds:

- Max CC per function: 15
- Max nesting depth: 4
- Max function length: 50 LOC
- Minimum test coverage: 80%

## References

- Related skill: `phase-cleanup` for refactoring guidelines
- Related skill: `quality-run-linters` for complete quality check
