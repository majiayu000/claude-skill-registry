---
name: code-quality-monitor
description: Proactive code health monitoring and quality gate enforcement. Use when validating code changes, reviewing PRs, or ensuring code meets quality standards before merging.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [lint-monorepo, test-writer, coverage-reporter]
  must_serialize_with: []
  preferred_batch_size: 5
context_hints:
  max_file_context: 50
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "coverage.*below.*60"
    reason: "Critical coverage drop requires human decision"
  - pattern: "security.*critical"
    reason: "Critical security issues require immediate escalation"
  - keyword: ["architectural", "breaking"]
    reason: "Architectural concerns need human review"
---

# Code Quality Monitor

A proactive health checker that monitors code quality and enforces strict standards.

## When This Skill Activates

- Before committing changes
- During PR reviews
- When validating code health
- After making multiple edits
- When user asks about code quality

## Quality Standards

### Python Backend Standards

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Test Coverage | >= 80% | >= 70% |
| Type Coverage | 100% public APIs | >= 90% |
| Cyclomatic Complexity | <= 10 | <= 15 |
| Function Length | <= 50 lines | <= 100 lines |
| File Length | <= 500 lines | <= 800 lines |

### TypeScript Frontend Standards

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Type Safety | No `any` | < 5 `any` uses |
| Test Coverage | >= 75% | >= 60% |
| Component Size | <= 200 lines | <= 300 lines |
| Hook Complexity | <= 5 dependencies | <= 8 dependencies |

## Health Check Commands

### Quick Health Check
```bash
cd /home/user/Autonomous-Assignment-Program-Manager/backend

# Run all quality checks
pytest --tb=no -q && \
ruff check app/ tests/ && \
black --check app/ tests/ && \
mypy app/ --python-version 3.11 --no-error-summary

echo "Backend health: PASS"
```

### Comprehensive Health Check
```bash
cd /home/user/Autonomous-Assignment-Program-Manager/backend

# Coverage report
pytest --cov=app --cov-report=term-missing --cov-fail-under=70

# Complexity analysis
radon cc app/ -a -s

# Security scan
bandit -r app/ -ll

# Dependency check
pip-audit
```

### Frontend Health Check
```bash
cd /home/user/Autonomous-Assignment-Program-Manager/frontend

npm run type-check && \
npm run lint && \
npm test -- --coverage --watchAll=false

echo "Frontend health: PASS"
```

## Quality Gate Rules

### Gate 1: Must Pass (Blocking)
- [ ] All tests pass
- [ ] No linting errors
- [ ] No type errors
- [ ] No critical security issues

### Gate 2: Should Pass (Warning)
- [ ] Coverage >= 70%
- [ ] No new complexity issues
- [ ] Documentation updated
- [ ] No TODOs without tickets

### Gate 3: Nice to Have (Info)
- [ ] Coverage >= 80%
- [ ] All functions documented
- [ ] No magic numbers
- [ ] Consistent naming

## Monitoring Workflow

### Pre-Commit Check
Before committing, validate:

```bash
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Format
black app/ tests/

# Lint
ruff check app/ tests/ --fix

# Type check
mypy app/ --python-version 3.11

# Quick tests
pytest --tb=no -q --lf

echo "Pre-commit checks: PASS"
```

### PR Validation Check
For pull request reviews:

```bash
#!/bin/bash
set -e

echo "Running PR validation..."

# Full test suite with coverage
pytest --cov=app --cov-report=term-missing

# Security scan
bandit -r app/ -ll

# Check for common issues
ruff check app/ tests/

# Type coverage
mypy app/ --python-version 3.11

echo "PR validation: PASS"
```

## Red Flags to Watch For

### Immediate Action Required
1. Test coverage dropped below 70%
2. New security vulnerability detected
3. Type errors in public APIs
4. Breaking changes without migration

### Needs Attention
1. Coverage trending down
2. Increasing complexity metrics
3. Growing file sizes
4. Missing docstrings on new functions

### Nice to Address
1. Minor style inconsistencies
2. Optimization opportunities
3. Documentation gaps
4. Technical debt

## Integration Points

### With lint-monorepo (Primary Linting)
For all linting operations, delegate to the `lint-monorepo` skill:

```
Quality gate check needed
    → Invoke lint-monorepo skill
    → lint-monorepo runs auto-fix workflow
    → Returns pass/fail with details
```

**Linting workflow:**
```bash
# lint-monorepo handles both Python and TypeScript
# See .claude/skills/lint-monorepo/ for details

# Quick lint check
cd /home/user/Autonomous-Assignment-Program-Manager/backend
ruff check app/ tests/

cd /home/user/Autonomous-Assignment-Program-Manager/frontend
npm run lint
```

**For persistent lint errors:** Use `lint-monorepo` root-cause analysis workflow.

### With automated-code-fixer
When quality issues are detected, the `automated-code-fixer` skill can be triggered to automatically resolve:
- Linting issues (auto-fixable) - coordinates with `lint-monorepo`
- Formatting issues
- Simple type annotation additions
- Import organization

### With Existing Commands
- `/run-tests` - Full test suite
- `/lint-fix` - Auto-fix linting
- `/health-check` - System health
- `/check-compliance` - ACGME validation

## Reporting Format

### Quick Status
```
Code Health: GREEN/YELLOW/RED

Tests: 156 passed, 0 failed
Coverage: 78.2% (target: 80%)
Linting: 0 errors, 3 warnings
Types: 100% coverage
Security: No issues
```

### Detailed Report
```markdown
## Code Quality Report

### Test Results
- Total: 156 tests
- Passed: 156
- Failed: 0
- Skipped: 2

### Coverage Analysis
- Current: 78.2%
- Target: 80.0%
- Delta: -1.8%
- Uncovered: app/services/new_feature.py (lines 45-67)

### Linting
- Errors: 0
- Warnings: 3
  - W291: trailing whitespace (3 occurrences)

### Type Safety
- Checked files: 147
- Errors: 0
- Coverage: 100%

### Security
- Critical: 0
- High: 0
- Medium: 0
- Low: 0

### Recommendations
1. Add tests for app/services/new_feature.py
2. Remove trailing whitespace
3. Consider splitting large function in resilience.py
```

## Escalation Rules

Escalate to human when:
1. Coverage drops below 60%
2. Critical security issue found
3. Multiple interdependent failures
4. Unclear how to improve metrics
5. Architectural concerns detected
