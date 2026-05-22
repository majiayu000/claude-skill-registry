---
name: validation
description: Validate code quality, test coverage, performance, and security. Use when verifying implemented features meet all standards and requirements before marking complete.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Feature Validation Skill

## Purpose

This skill provides systematic validation of implemented features, ensuring code quality, test coverage, performance, security, and requirement fulfillment before marking work complete.

## When to Use

- After implementation and testing are complete
- Before creating pull request
- Before marking feature as done
- When verifying all acceptance criteria met
- Final quality gate before deployment

## Validation Workflow

### 1. Code Quality Validation

**Run Quality Checks:**
```bash
# Format check (Black)
black --check src/ tests/

# Type checking (mypy)
mypy src/

# Linting (flake8, if configured)
flake8 src/ tests/

# All checks together
make lint  # If Makefile configured
```

**Quality Checklist:**
Refer to `quality-checklist.md` for comprehensive review

**Key Quality Metrics:**
- [ ] All functions have type hints
- [ ] All public functions have docstrings (Google style)
- [ ] No files exceed 500 lines
- [ ] No lint errors or warnings
- [ ] Code formatted with Black
- [ ] Type checking passes with mypy
- [ ] No code duplication (DRY principle)
- [ ] Single responsibility principle followed

**Automated Script:**
```bash
# Use validation script
python scripts/run_checks.py --quality
```

**Deliverable:** Quality report with pass/fail

---

### 2. Test Coverage Validation

**Run Tests with Coverage:**
```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Check coverage threshold
pytest --cov=src --cov-fail-under=80

# View HTML coverage report
open htmlcov/index.html
```

**Coverage Checklist:**
- [ ] Overall coverage ≥ 80%
- [ ] Core business logic ≥ 90%
- [ ] Utilities and helpers ≥ 85%
- [ ] No critical paths untested
- [ ] All branches covered
- [ ] Edge cases tested
- [ ] Error conditions tested

**Identify Coverage Gaps:**
```bash
# Show untested lines
pytest --cov=src --cov-report=term-missing

# Generate detailed HTML report
pytest --cov=src --cov-report=html
```

**Deliverable:** Coverage report with gaps identified

---

### 3. Test Quality Validation

**Review Test Suite:**
- [ ] All tests passing
- [ ] No skipped tests (without justification)
- [ ] No flaky tests (intermittent failures)
- [ ] Tests run quickly (unit tests < 1 min)
- [ ] Tests are independent (no order dependency)
- [ ] Tests clean up after themselves
- [ ] Mock external dependencies properly
- [ ] Test names are clear and descriptive

**Run Tests Multiple Times:**
```bash
# Run tests 10 times to check for flaky tests
for i in {1..10}; do pytest || break; done

# Run in random order
pytest --random-order
```

**Test Markers:**
```bash
# Verify no slow tests in unit tests
pytest tests/unit/ -m "not slow"

# Run integration tests separately
pytest tests/integration/
```

**Deliverable:** Test quality assessment

---

### 4. Performance Validation

**Performance Checklist:**
Refer to `performance-benchmarks.md` for target metrics

**Key Performance Metrics:**
- [ ] Response time < target (e.g., < 200ms for p95)
- [ ] Throughput meets requirements (e.g., 1000 req/s)
- [ ] Memory usage within bounds (e.g., < 100MB)
- [ ] CPU usage reasonable (e.g., < 50%)
- [ ] No memory leaks detected
- [ ] Database queries optimized (< 5 queries per operation)

**Performance Testing:**
```bash
# Run performance tests
pytest tests/performance/ -v

# Profile code
python -m cProfile -o profile.stats script.py
python -m pstats profile.stats

# Memory profiling
python -m memory_profiler script.py
```

**Benchmark Against Requirements:**
```python
# Example performance test
def test_performance_requirement():
    """Verify operation meets performance requirement."""
    start = time.time()
    result = expensive_operation()
    duration = time.time() - start

    assert duration < 1.0, f"Took {duration}s, required < 1.0s"
```

**Deliverable:** Performance report with metrics

---

### 5. Security Validation

**Security Checklist Review:**
Review `security-checklist.md` from analysis phase and verify:

**Input Validation:**
- [ ] All user inputs validated and sanitized
- [ ] SQL injection prevented (parameterized queries)
- [ ] Command injection prevented (no shell=True with user input)
- [ ] Path traversal prevented (sanitized file paths)
- [ ] XSS prevented (escaped output)

**Authentication & Authorization:**
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks at every access point
- [ ] Session management secure
- [ ] Credentials not hardcoded

**Data Protection:**
- [ ] Sensitive data encrypted in transit
- [ ] Sensitive data encrypted at rest (if applicable)
- [ ] PII handling compliant
- [ ] Secrets in environment variables (not code)
- [ ] Error messages don't leak sensitive info

**Dependency Security:**
```bash
# Check for vulnerable dependencies
pip-audit

# Or use safety
safety check --json

# Check for outdated dependencies
pip list --outdated
```

**Deliverable:** Security validation report

---

### 6. Requirements Validation

**Verify Acceptance Criteria:**
Review original requirements from analysis phase:
- [ ] All functional requirements implemented
- [ ] All acceptance criteria met
- [ ] User stories fulfilled
- [ ] Edge cases handled
- [ ] Error scenarios handled

**Manual Testing:**
```bash
# Test CLI (if applicable)
python -m src.tools.feature.main --help
python -m src.tools.feature.main create --name test

# Test with sample data
python -m src.tools.feature.main --input samples/test.json

# Test error cases
python -m src.tools.feature.main --invalid-option
```

**Regression Testing:**
- [ ] Existing functionality not broken
- [ ] No breaking changes to public APIs
- [ ] Backward compatibility maintained (if required)

**Deliverable:** Requirements validation checklist

---

### 7. Documentation Validation

**Code Documentation:**
- [ ] All public functions have docstrings
- [ ] Docstrings follow Google style
- [ ] Complex logic has inline comments
- [ ] Type hints present and accurate
- [ ] README updated (if applicable)

**Technical Documentation:**
- [ ] Architecture documented
- [ ] API contracts documented
- [ ] Configuration documented
- [ ] Setup instructions complete
- [ ] Known issues documented

**User Documentation:**
- [ ] Usage guide written (if applicable)
- [ ] Examples provided
- [ ] Troubleshooting guide included
- [ ] FAQ updated

**CHANGELOG Update:**
- [ ] Changes documented in CHANGELOG.md
- [ ] Version bumped appropriately
- [ ] Breaking changes highlighted

**Deliverable:** Documentation review checklist

---

### 8. Integration Validation

**Integration Testing:**
```bash
# Run integration tests
pytest tests/integration/ -v

# Test with real dependencies (in test environment)
pytest tests/integration/ --no-mock
```

**Integration Checklist:**
- [ ] Integrates correctly with existing code
- [ ] No circular dependencies
- [ ] Module imports work correctly
- [ ] Configuration loads correctly
- [ ] External services connect (if applicable)

**End-to-End Testing:**
```bash
# Test complete workflows
pytest tests/e2e/ -v

# Manual E2E testing
./scripts/manual_test.sh
```

**Deliverable:** Integration test report

---

### 9. Final Validation

**Run Complete Validation Suite:**
```bash
# Use automated validation script
python scripts/run_checks.py --all

# Or run individual checks
python scripts/run_checks.py --quality
python scripts/run_checks.py --tests
python scripts/run_checks.py --coverage
python scripts/run_checks.py --security
```

**Pre-PR Checklist:**
- [ ] All quality checks passing
- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Performance requirements met
- [ ] Security validated
- [ ] Requirements fulfilled
- [ ] Documentation complete
- [ ] Integration verified
- [ ] No known critical bugs

**Create Validation Report:**
```markdown
# Validation Report: [Feature Name]

## Quality ✅
- Black: PASS
- mypy: PASS
- flake8: PASS (0 errors, 0 warnings)

## Testing ✅
- Unit tests: 45 passed
- Integration tests: 12 passed
- Coverage: 87% (target: 80%)

## Performance ✅
- Response time (p95): 145ms (target: < 200ms)
- Throughput: 1200 req/s (target: 1000 req/s)
- Memory usage: 75MB (target: < 100MB)

## Security ✅
- No vulnerable dependencies
- Input validation: Complete
- Secrets management: Secure

## Requirements ✅
- All acceptance criteria met
- No regressions detected

## Documentation ✅
- Code documentation: Complete
- Technical docs: Complete
- CHANGELOG: Updated

## Status: READY FOR PR ✅
```

**Deliverable:** Final validation report

---

## Quality Standards

### Code Quality Metrics

**Complexity:**
- Cyclomatic complexity < 10 per function
- Max nesting depth: 4 levels

**Maintainability:**
- Files < 500 lines
- Functions < 50 lines
- Classes < 300 lines

**Documentation:**
- 100% public API documented
- Docstring coverage ≥ 90%

### Test Quality Metrics

**Coverage:**
- Overall: ≥ 80%
- Critical paths: 100%
- Core logic: ≥ 90%

**Test Quality:**
- No flaky tests
- Unit tests < 1 minute total
- Integration tests < 5 minutes total

### Performance Benchmarks

Refer to `performance-benchmarks.md` for detailed criteria

**Response Time:**
- p50: < 50ms
- p95: < 200ms
- p99: < 500ms

**Resource Usage:**
- Memory: < 100MB
- CPU: < 50% single core

---

## Automated Validation Script

The `scripts/run_checks.py` script automates validation:

```bash
# Run all checks
python scripts/run_checks.py --all

# Run specific checks
python scripts/run_checks.py --quality
python scripts/run_checks.py --tests
python scripts/run_checks.py --coverage
python scripts/run_checks.py --security
python scripts/run_checks.py --performance

# Generate report
python scripts/run_checks.py --all --report validation-report.md
```

---

## Supporting Resources

- **quality-checklist.md**: Comprehensive code quality standards
- **performance-benchmarks.md**: Performance criteria and targets
- **scripts/run_checks.py**: Automated validation runner

---

## Integration with Feature Implementation Flow

**Input:** Completed implementation with tests
**Process:** Systematic validation against all criteria
**Output:** Validation report + approval for PR
**Next Step:** Create pull request or deploy

---

## Validation Checklist Summary

### Quality ✓
- [ ] Code formatted (Black)
- [ ] Type checked (mypy)
- [ ] Linted (no errors/warnings)
- [ ] Files < 500 lines
- [ ] Functions documented
- [ ] Quality checklist complete

### Testing ✓
- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] Core logic ≥ 90% coverage
- [ ] No flaky tests
- [ ] Tests run quickly

### Performance ✓
- [ ] Response time < target
- [ ] Throughput meets requirements
- [ ] Memory usage reasonable
- [ ] No performance regressions

### Security ✓
- [ ] Input validation complete
- [ ] No hardcoded secrets
- [ ] Dependencies scanned
- [ ] Security checklist complete

### Requirements ✓
- [ ] Acceptance criteria met
- [ ] User stories fulfilled
- [ ] Edge cases handled
- [ ] No regressions

### Documentation ✓
- [ ] Code documented
- [ ] Technical docs complete
- [ ] User docs (if applicable)
- [ ] CHANGELOG updated

### Integration ✓
- [ ] Integration tests passing
- [ ] No breaking changes
- [ ] Backward compatible

### Final Approval ✓
- [ ] All checklists complete
- [ ] Validation report generated
- [ ] Ready for pull request
- [ ] Stakeholder approval (if required)

---

## Sign-off

**Feature:** [Feature Name]
**Validated By:** [Your Name]
**Date:** [YYYY-MM-DD]

**Status:** ☐ Approved ☐ Needs Work

**Notes:**
[Any additional notes or concerns]

---

## What to Do If Validation Fails

**Quality Issues:**
1. Fix formatting: `black src/ tests/`
2. Fix type errors: Review mypy output
3. Fix lint errors: Review flake8 output
4. Refactor large files/functions

**Coverage Issues:**
1. Identify untested code: `pytest --cov-report=html`
2. Add missing tests
3. Review edge cases
4. Add error condition tests

**Performance Issues:**
1. Profile code: `python -m cProfile`
2. Optimize hot paths
3. Add caching where appropriate
4. Optimize database queries

**Security Issues:**
1. Address vulnerabilities: `pip-audit`
2. Review input validation
3. Check secrets management
4. Run security checklist again

**Requirement Issues:**
1. Review acceptance criteria
2. Implement missing functionality
3. Test edge cases
4. Verify with stakeholders

**After Fixes:**
- Re-run validation
- Update validation report
- Verify all checks pass
- Proceed to PR
