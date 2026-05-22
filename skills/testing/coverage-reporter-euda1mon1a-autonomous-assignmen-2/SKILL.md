---
name: coverage-reporter
description: Generate and analyze test coverage reports. Use to identify coverage gaps, track coverage trends, and ensure quality thresholds are met.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [test-writer, code-review, lint-monorepo]
  must_serialize_with: []
  preferred_batch_size: 5
context_hints:
  max_file_context: 100
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "coverage.*below.*threshold"
    reason: "Coverage below minimum requires human decision"
  - keyword: ["critical", "untested"]
    reason: "Untested critical code needs attention"
---

# Coverage Reporter Skill

Comprehensive test coverage analysis and reporting for Python and TypeScript code.

## When This Skill Activates

- After running test suite
- Before committing changes
- Tracking coverage over time
- Investigating coverage gaps
- Reporting on coverage metrics

## Coverage Analysis Methodology

### Phase 1: Coverage Collection

**Python Coverage**
```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term-missing
```

**TypeScript Coverage**
```bash
cd frontend
npm run test:coverage
```

### Phase 2: Gap Analysis

**Step 2.1: Identify Untested Code**
```
For each file:
1. Count lines not covered
2. Identify untested functions
3. Identify untested branches
4. Calculate coverage percentage
```

**Step 2.2: Prioritize by Risk**
| Risk Level | Type | Priority |
|-----------|------|----------|
| Critical | Auth, crypto, data access | Fix immediately |
| High | Business logic, validation | Fix within 48h |
| Medium | Utils, helpers | Fix within 1 week |
| Low | Formatting, display | Nice to have |

### Phase 3: Coverage Report Generation

```markdown
## Test Coverage Report

**Date:** [DATE]
**Overall Coverage:** [X]%

### Summary
- Backend: [X]%
- Frontend: [Y]%
- Target: 80%

### Critical Gaps
- [File]: [X]% - [reason]
- [File]: [Y]% - [reason]

### Trends
- Week 1: 75%
- Week 2: 77%
- Week 3: 79%
- Trend: Improving

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

### Phase 4: Trend Analysis

```
1. Historical coverage
   - Track weekly/monthly trends
   - Identify degradation
   - Project future coverage

2. Coverage velocity
   - How fast is coverage improving?
   - Estimate time to target

3. Coverage stability
   - Which areas consistently low?
   - Which areas consistently high?
```

## Coverage Requirements by Layer

| Layer | Target | Minimum |
|-------|--------|---------|
| Services | 90% | 80% |
| Controllers | 85% | 75% |
| Models | 80% | 70% |
| Utils | 90% | 85% |
| Routes | 75% | 65% |
| Components (Frontend) | 80% | 70% |

## Quick Coverage Commands

```bash
# Python coverage with details
cd backend
pytest --cov=app --cov-report=html --cov-report=term-missing -v

# Frontend coverage
cd frontend
npm run test:coverage

# Coverage diff against main
# (Identify what new code is untested)
git diff main...HEAD | grep "^+" | wc -l
```

## Gap Remediation Workflow

### For Each Untested Component:

```
1. Understand the code
   - What does it do?
   - When is it called?
   - Why isn't it tested?

2. Determine test strategy
   - Unit test?
   - Integration test?
   - E2E test?

3. Write tests
   - Happy path
   - Error cases
   - Edge cases

4. Verify coverage
   - Re-run coverage
   - Confirm improved
```

## Integration with test-writer

When coverage gaps identified:
1. Report findings to test-writer skill
2. Request test generation for gaps
3. Re-run coverage after tests added
4. Track improvement

## Validation Checklist

- [ ] Coverage >= target percentage
- [ ] No untested critical code
- [ ] All public APIs covered
- [ ] Error paths tested
- [ ] Edge cases covered
- [ ] Coverage trend is improving
- [ ] No artificial coverage inflation

## References

- Coverage requirements in CLAUDE.md
- See test-writer skill for test generation
- Testing patterns in python-testing-patterns skill

