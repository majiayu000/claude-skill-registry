---
name: quality-gate
description: Complete quality validation workflow combining TypeScript checking, linting, tests, coverage, and build validation. Works with any TypeScript/JavaScript project. Returns structured pass/fail with detailed results for each check. Used in conductor workflows and quality assurance phases.
---

# Quality Gate

## Purpose

Execute comprehensive quality validation before code can proceed to PR creation, ensuring all quality standards are met through automated checks and minimum thresholds.

## When to Use

- Conductor workflow Phase 3 (Quality Assurance)
- Before creating any pull request
- After refactoring changes
- As part of CI/CD pipeline
- Before merging to development branch

## Quality Standards

All checks must pass:
- ✅ All tests passing (unit, integration, E2E)
- ✅ Audit score ≥ 8.0/10
- ✅ Production build successful
- ✅ Test coverage ≥ 80% (configurable)
- ✅ No TypeScript errors
- ✅ No linting errors

## Instructions

### Step 1: Run Comprehensive Tests

Use the `run-comprehensive-tests` skill:

```bash
npm run test
```

**Validation:**
- Exit code 0 (all tests passed)
- No failing test cases
- Coverage data available

**If tests fail:**
- BLOCK - Do not proceed
- Delegate to debugger agent for investigation
- Fix failures and re-run quality gate

### Step 2: Execute Code Quality Audit

Use the `audit-code` skill or delegate to audit agent:

```markdown
Audit all changed files from this implementation:
- Architecture patterns
- Code complexity
- SOLID principles
- DRY violations
- Type safety
- Error handling
```

**Validation:**
- Audit score ≥ 8.0/10
- No CRITICAL findings
- No HIGH priority blocking issues

**If audit score < 8.0:**
- BLOCK - Do not proceed
- Delegate to refactor agent
- Address critical/high findings
- Re-run audit
- Must achieve ≥ 8.0 before continuing

### Step 3: Validate Production Build

```bash
npm run build
```

**Validation:**
- Build completes successfully
- No compilation errors
- No build warnings (or acceptable count)
- All packages build successfully

**If build fails:**
- BLOCK - Do not proceed
- Investigate build errors
- Fix compilation issues
- Re-run quality gate

### Step 4: Check Test Coverage

Parse coverage report from test results:

```bash
# Coverage should be included in test output
npm run test -- --coverage
```

**Validation:**
- Overall coverage ≥ 80%
- Statement coverage ≥ 80%
- Branch coverage ≥ 75%
- Function coverage ≥ 80%

**If coverage below threshold:**
- WARNING (not blocking for MVP)
- Log coverage gap
- Create GitHub issue for coverage improvement
- Proceed with quality gate

### Step 5: TypeScript Type Checking

```bash
npm run type-check
# Or: npx tsc --noEmit
```

**Validation:**
- No TypeScript errors
- All types resolve correctly
- No implicit any types (if strict)

**If type errors:**
- BLOCK - Do not proceed
- Fix type errors
- Re-run quality gate

### Step 6: Linting Validation

```bash
npm run lint
# Or: npx eslint .
```

**Validation:**
- No linting errors
- Warnings acceptable (log count)
- Code style consistent

**If linting errors:**
- Try auto-fix: `npm run lint -- --fix`
- Manual fix if auto-fix doesn't resolve
- Re-run quality gate

## Result Aggregation

Return structured results:

```json
{
  "qualityGate": "pass" | "fail",
  "timestamp": "2025-10-21T...",
  "checks": {
    "tests": {
      "status": "pass",
      "total": 45,
      "passed": 45,
      "failed": 0,
      "coverage": 87.5
    },
    "audit": {
      "status": "pass",
      "score": 8.5,
      "critical": 0,
      "high": 0,
      "medium": 2,
      "low": 3
    },
    "build": {
      "status": "pass",
      "duration": "12.3s",
      "warnings": 0
    },
    "typeCheck": {
      "status": "pass",
      "errors": 0
    },
    "lint": {
      "status": "pass",
      "errors": 0,
      "warnings": 2
    }
  },
  "blockers": [],
  "warnings": [
    "Coverage below target: 87.5% (target: 90%)",
    "2 lint warnings present"
  ]
}
```

## Failure Handling

### Retry Logic

If quality gate fails:
1. Identify failing check
2. Route to appropriate fix:
   - **Tests fail** → debugger agent
   - **Audit < 8.0** → refactor agent
   - **Build fails** → investigate build errors
   - **Type errors** → fix type issues
   - **Lint errors** → auto-fix or manual
3. Re-run quality gate after fixes
4. Maximum 3 retries before escalating to human

### Escalation Criteria

Escalate to human if:
- Quality gate fails after 3 retry attempts
- Audit score consistently < 7.0
- Build failures persist after investigation
- Tests fail with unclear error messages

## Integration with Conductor

Used in Conductor Phase 3:

```markdown
**Phase 3: Quality Assurance**

Use the `quality-gate` skill to validate all quality standards:

1. Execute quality gate
2. If pass: Proceed to Phase 4 (PR Creation)
3. If fail:
   - Identify failing check
   - Route to appropriate agent for fixes
   - Re-run quality gate
   - Repeat until pass or escalate

Quality gate must pass before creating PR.
```

## Performance Optimization

Run checks in optimal order:
1. **TypeScript check** (fastest, catches syntax errors early)
2. **Lint** (fast, catches code style issues)
3. **Tests** (slower, but comprehensive)
4. **Audit** (slowest, deep analysis)
5. **Build** (final validation)

This order allows fast-failing for quick feedback.

## Configuration

Quality gate thresholds can be adjusted:

```json
// .claude/quality-gate-config.json
{
  "minimumAuditScore": 8.0,
  "minimumCoverage": 80,
  "blockOnCoverage": false,
  "blockOnLintWarnings": false,
  "maxRetries": 3
}
```

## Related Skills

- `run-comprehensive-tests` - Test execution
- `audit-code` - Code quality audit
- `validate-coverage` - Coverage analysis
- `check-lint` - Linting validation
- `validate-build` - Build validation

## Examples

See `examples.md` for:
- Complete quality gate execution flow
- Failure handling scenarios
- Integration with Conductor workflow
- Custom threshold configuration
