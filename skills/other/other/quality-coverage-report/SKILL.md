---
name: quality-coverage-report
description: Generate test coverage reports showing which code paths are tested. Use to identify untested code and improve test coverage.
mcp_fallback: none
category: quality
agent: test-engineer
user-invocable: false
---

# Test Coverage Report Skill

Generate and analyze test coverage reports.

## When to Use

- After running tests
- Before creating PR
- Identifying untested code
- Improving test coverage

## Quick Reference

```bash
# Python coverage
pytest --cov=src --cov-report=html tests/

# View report
open htmlcov/index.html

# Terminal report
pytest --cov=src --cov-report=term-missing tests/
```

## Coverage Metrics

### Line Coverage

Percentage of code lines executed by tests:

```text
src/module.mojo
  Lines: 45/50 (90%)
  Missing: 12, 18, 23, 35, 41
```

### Branch Coverage

Percentage of decision branches taken:

```text
Branches: 8/10 (80%)
Missing branches: line 12->15, line 18->20
```

## Coverage Goals

| Category | Minimum | Target | Critical |
|----------|---------|--------|----------|
| Line coverage | 80% | 90% | 100% |
| Branch coverage | 70% | 85% | 95% |
| Critical paths | - | - | 100% |

## Coverage Report

```text
Coverage Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File                Lines    Missing    Coverage
────────────────────────────────────────────────
src/tensor.mojo       150         5      96.7%
src/nn.mojo          200        30      85.0%
src/utils.mojo        50        10      80.0%
────────────────────────────────────────────────
TOTAL                400        45      88.8%

Minimum coverage: 80% ✅
Target coverage: 90% ❌
Critical paths: 100% ✅
```

## Improving Coverage

1. **Identify gaps** - Find uncovered lines in report
2. **Write tests** - Add tests for untested code
3. **Re-run** - Generate new report
4. **Verify** - Check coverage improved
5. **Repeat** - Until targets met

## Coverage Workflow

```bash
# 1. Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing tests/

# 2. Identify missing coverage
# Review "Missing" column in output

# 3. Write tests for gaps
# ... create test files ...

# 4. Re-run
pytest --cov=src --cov-report=html tests/

# 5. Check improvement
# Compare htmlcov/index.html
```

## CI Integration

```yaml
- name: Test Coverage
  run: |
    pytest --cov=src --cov-report=xml
    codecov -f coverage.xml
```

## Error Handling

| Error | Fix |
|-------|-----|
| "No module named pytest" | Install: `pip install pytest-cov` |
| "Cannot find tests/" | Verify test directory exists |
| No coverage report | Ensure tests ran successfully |

## References

- Related skill: `phase-test-tdd` for test generation
- Related skill: `quality-run-linters` for complete quality check
- Pytest docs: <https://docs.pytest.org/en/stable/>
