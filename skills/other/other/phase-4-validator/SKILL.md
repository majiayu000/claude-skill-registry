---
name: phase-4-validator
description: Validates Testing Phase completion before advancing to Finalization Phase. Checks test execution results, coverage targets, test quality, and environment health. Ensures 100% test pass rate required by quality gates.
---

# Phase 4 (Testing) Validation Skill

**Purpose**: Automate validation of Testing Phase before advancing to Finalization Phase.

**When to Use**: When orchestrator needs to verify all tests are passing and ready for deployment.

## Critical Rule: 100% Test Pass Rate Required

**ALL work types (Feature/Bug/Hotfix/Docs/Refactor) require 100% test pass rate.**

No exceptions. One failing test = Phase 4 fails.

## How to Use This Skill

**Executable Script**: `execute.sh`

```bash
# Basic usage (no parameters required)
bash .claude/skills/phase-4-validator/execute.sh

# Show help
bash .claude/skills/phase-4-validator/execute.sh --help
```

**Parameters**:
- No parameters required - validates current Docker environment

**Script validates**:
- Environment health (Docker containers, database, API, web services)
- Test execution results (100% pass rate REQUIRED for all tests)
- Test coverage (API ≥80%, React ≥70%)
- Test quality (no flaky tests, execution time, independence, cleanup)
- Documentation (TEST_CATALOG, test reports, known issues, metrics)

**Exit codes**:
- 0: All tests passing at 100%, ready for Finalization Phase
- 1: Tests failing OR environment unhealthy OR quality gates not met

**CRITICAL**: This validator BLOCKS workflow if ANY test fails. 100% pass rate is mandatory.

## Quality Gate Checklist (100% Test Pass Rate Required)

### Environment Health (15 points)
- [ ] All Docker containers running (5 points)
- [ ] Database healthy and seeded (5 points)
- [ ] API service responding (3 points)
- [ ] Web service responding (2 points)

### Test Execution (40 points - MUST BE 40/40)
- [ ] Unit tests: 100% passing (15 points)
- [ ] Integration tests: 100% passing (15 points)
- [ ] E2E tests: 100% passing (10 points)

### Test Coverage (15 points)
- [ ] API coverage ≥ 80% (5 points)
- [ ] React coverage ≥ 70% (5 points)
- [ ] Critical paths covered (5 points)

### Test Quality (15 points)
- [ ] No flaky tests (5 points)
- [ ] Test execution time acceptable (3 points)
- [ ] Tests are independent (4 points)
- [ ] Test data cleanup working (3 points)

### Documentation (15 points)
- [ ] TEST_CATALOG updated (5 points)
- [ ] Test results documented (5 points)
- [ ] Known issues documented (3 points)
- [ ] Performance metrics recorded (2 points)

## Usage Examples

### From Orchestrator
```
Use the phase-4-validator skill to verify all tests are passing
```

### Manual Validation
```bash
# Run complete validation
bash .claude/skills/phase-4-validator.md
```

## Common Issues

### Issue: Environment Not Healthy
**Solution**: Run environment checks first
```bash
./dev.sh
# Wait for all containers to be healthy
docker ps
```

### Issue: Failing Tests
**Solution**: Phase 4 CANNOT advance with failing tests
- Loop back to react-developer for UI test failures
- Loop back to backend-developer for API test failures
- Loop back to test-developer for test logic issues
- test-executor handles environment issues only

### Issue: Low Coverage
**Warning but not blocker**: Coverage below targets is a warning but doesn't block if all tests pass.

**However**: Should document in testing-notes.md as known limitation.

### Issue: Flaky Tests
**Solution**: Flaky tests = unreliable validation
- Must be fixed before advancing
- Document patterns causing flakiness
- Add to lessons learned

## Zero Tolerance Policy

**Testing Phase has ZERO TOLERANCE for failing tests.**

Even a single failing test means:
- ❌ Phase 4 validation FAILS
- ❌ Cannot advance to Phase 5
- ❌ Must loop back to implementation

**Why**: Deploying with failing tests risks production issues.

## Output Format

```json
{
  "phase": "testing",
  "status": "pass|fail",
  "score": 95,
  "maxScore": 100,
  "percentage": 95,
  "testResults": {
    "unit": {
      "total": 45,
      "passed": 45,
      "failed": 0,
      "passRate": 100
    },
    "integration": {
      "total": 12,
      "passed": 12,
      "failed": 0,
      "passRate": 100
    },
    "e2e": {
      "total": 8,
      "passed": 8,
      "failed": 0,
      "passRate": 100
    }
  },
  "coverage": {
    "api": 85,
    "web": 72
  },
  "environment": {
    "docker": "healthy",
    "database": "healthy",
    "api": "responding",
    "web": "responding"
  },
  "quality": {
    "flakyTests": 0,
    "executionTime": 125.3,
    "independent": true,
    "cleanupWorking": true
  },
  "readyForNextPhase": true
}
```

## Integration with Quality Gates

**ALL work types require 100% test pass rate:**
- **Feature**: 100% pass (40/40 test points) + coverage/quality
- **Bug Fix**: 100% pass (40/40 test points) + coverage/quality
- **Hotfix**: 100% pass (40/40 test points) + minimal other requirements
- **Refactoring**: 100% pass (40/40 test points) + no regressions

## Progressive Disclosure

**Initial Context**: Show pass/fail status only
**On Request**: Show detailed test results and coverage
**On Failure**: Show specific failing tests with logs
**On Pass**: Show concise summary + quality metrics

---

**Remember**: Phase 4 is the quality gate. If tests aren't 100% passing, nothing advances. This protects production from bugs.
