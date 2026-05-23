---
name: validation-coordinator
description: Auto-activates when coordinating sequential validation specialists with
  workflow management, dependency tracking, and overall validation status monitoring.
allowed-tools: Read, Bash
---

## Purpose

The **validation-coordinator** skill provides structured methods for managing sequential validation specialist invocation, tracking validation workflow progress, and ensuring all quality gates are satisfied before deployment. It handles specialist dependencies, failure tracking, and overall validation status reporting.

## When to Use

This skill auto-activates when you:
- Coordinate sequential validation specialists (5-6 specialists)
- Manage validation workflow across test writing, test execution, quality checks, and security scans
- Track validation progress and status
- Ensure specialist dependencies are satisfied (e.g., tests written before execution)
- Monitor validation failures and re-validation cycles
- Generate comprehensive validation status reports
- Prepare validation results for deployment phase

## Provided Capabilities

### 1. Sequential Specialist Invocation
- **Specialist Ordering**: Invoke specialists in correct sequence with dependencies
- **Prerequisite Validation**: Ensure each specialist's inputs are ready before invocation
- **Invocation Tracking**: Log each specialist invocation with timestamp
- **Status Monitoring**: Track specialist status (pending, in-progress, completed, failed)

### 2. Validation Workflow Management
- **Phase Tracking**: Monitor validation phases (test writing, test execution, quality, security)
- **Dependency Resolution**: Ensure specialists run in order (unit tests → integration tests → test execution)
- **Workflow Visualization**: Provide clear view of validation progress
- **Completion Detection**: Identify when all validations complete

### 3. Failure Tracking
- **Failure Logging**: Record all validation failures with details
- **Iteration Tracking**: Count re-validation attempts per specialist
- **Failure Analysis**: Identify patterns in validation failures
- **Escalation Detection**: Flag specialists exceeding max iterations

### 4. Overall Validation Status
- **Aggregate Status**: Compute overall validation status (in-progress, passed, failed)
- **Quality Gate Tracking**: Monitor each quality gate (tests, coverage, quality, security)
- **Pass/Fail Reporting**: Report which validations passed/failed
- **Readiness Assessment**: Determine if feature is ready for deployment

### 5. Validation Documentation
- **Status Reports**: Generate validation status snapshots
- **Progress Logs**: Maintain detailed validation history
- **Summary Generation**: Create concise validation summaries
- **Metrics Collection**: Track validation time, iterations, and success rates

## Usage Guide

### Step 1: Initialize Validation Workflow

Load implementation artifacts and initialize validation state:

```bash
# Load PRP to understand what was implemented
/docs/implementation/prp/feature-{issue-number}-prp.md

# Identify implementation files
[Files listed in PRP or passed by orchestrator]
```

**Initialization**:
```markdown
### Validation Workflow Initialized

**Issue**: #{issue-number}
**Feature**: [Feature Name]
**Technology Stack**: [Python, TypeScript, Swift, etc.]
**Frontend**: [Yes/No - determines if E2E specialist needed]

**Validation Phases**:
1. Test Writing (Unit + Integration)
2. Test Execution (Test Runner)
3. Code Quality (Linting, Typing, Formatting)
4. Security (Security Scan, OWASP)
5. E2E & Accessibility (Frontend only)

**Specialist Status**:
- [ ] Unit Test Specialist: Pending
- [ ] Integration Test Specialist: Pending
- [ ] Test Runner Specialist: Pending
- [ ] Code Quality Specialist: Pending
- [ ] Security Specialist: Pending
- [ ] E2E & Accessibility Specialist: [Pending/N/A]

**Overall Status**: Pending
```

### Step 2: Invoke Specialists Sequentially

Use validation-workflow.md for detailed specialist invocation procedures.

**Sequential Invocation Pattern**:
```markdown
FOR EACH specialist IN validation_sequence:
  1. Check Prerequisites:
     - Are required inputs ready?
     - Did previous specialists complete successfully?

  2. Update Status:
     - Mark specialist as "In Progress"
     - Log invocation timestamp

  3. Invoke Specialist:
     - Call specialist with required inputs
     - Pass context (PRP, implementation files, previous outputs)

  4. Wait for Completion:
     - Monitor specialist progress
     - Capture specialist output

  5. Check Specialist Result:
     - IF specialist passes:
         a. Mark specialist as "Completed"
         b. Log success with timestamp
         c. Proceed to next specialist
     - IF specialist fails:
         a. Mark specialist as "Failed (iteration X)"
         b. Log failure details
         c. Trigger recursive communication (handled by recursive-communicator skill)
         d. Wait for main agent to fix
         e. Re-invoke specialist (increment iteration)
         f. Repeat until success OR max iterations (5)

  6. Update Overall Status:
     - Recalculate validation progress
     - Update quality gate checklist
```

**Specialist Dependencies**:
```markdown
### Dependency Chain

Unit Test Specialist
  ↓ (requires unit tests written)
Integration Test Specialist
  ↓ (requires integration tests written)
Test Runner Specialist
  ↓ (requires all tests pass + coverage ≥80%)
Code Quality Specialist
  ↓ (requires quality checks pass)
Security Specialist
  ↓ (requires security scan pass)
E2E & Accessibility Specialist (Frontend only)
  ↓ (requires E2E tests pass + WCAG compliant)
Deployment Ready
```

### Step 3: Track Validation Progress

Use validation-checklist.md for comprehensive quality gate tracking.

**Validation Checklist**:
```markdown
## Validation Progress

### Phase 1: Test Writing
- [✅] Unit tests written (Specialist: unit-test-specialist, Iteration: 1/1)
- [✅] Integration tests written (Specialist: integration-test-specialist, Iteration: 1/1)

### Phase 2: Test Execution
- [⚠️] All tests pass (Specialist: test-runner-specialist, Iteration: 2/5, Status: Failed)
  - Failure: 3 unit tests failing in test_feature_47.py
  - Action: Recursive communication triggered, awaiting main agent fix
- [ ] Code coverage ≥80% (Pending test success)

### Phase 3: Code Quality
- [ ] Linting pass (Pending: awaiting test success)
- [ ] Type checking pass (Pending: awaiting test success)
- [ ] Formatting compliant (Pending: awaiting test success)

### Phase 4: Security
- [ ] Security scan clean (Pending: awaiting quality pass)
- [ ] OWASP Top 10 compliant (Pending: awaiting quality pass)

### Phase 5: E2E & Accessibility [FRONTEND ONLY]
- [N/A] E2E tests pass (Backend feature - specialist not invoked)
- [N/A] WCAG 2.1 AA compliant (Backend feature - specialist not invoked)

**Overall Status**: In Progress (Phase 2, Iteration 2)
**Blocking Issue**: Test failures in unit tests
**Next Action**: Awaiting main agent fix → re-run tests
```

**Progress Metrics**:
```markdown
### Validation Metrics

**Specialists Completed**: 2/5 (40%)
**Specialists In Progress**: 1/5 (Test Runner - Iteration 2)
**Specialists Pending**: 2/5 (Code Quality, Security)
**Total Iterations**: 3 (Unit Test: 1, Integration Test: 1, Test Runner: 1 initial + 1 retry)
**Elapsed Time**: 00:15:32
**Estimated Remaining**: ~00:10:00 (based on remaining specialists)
```

### Step 4: Monitor Quality Gates

Track each quality gate individually:

**Quality Gate Tracking**:
```markdown
### Quality Gate Status

| Gate | Status | Details | Iterations | Last Updated |
|------|--------|---------|------------|--------------|
| Unit Tests Written | ✅ PASS | 45 tests created | 1 | 2025-10-29 14:23:15 |
| Integration Tests Written | ✅ PASS | 12 tests created | 1 | 2025-10-29 14:28:42 |
| All Tests Pass | ⚠️ FAIL | 3 failures remaining | 2 | 2025-10-29 14:35:18 |
| Coverage ≥80% | ⏸️ PENDING | Awaiting test pass | - | - |
| Linting | ⏸️ PENDING | Awaiting test pass | - | - |
| Type Checking | ⏸️ PENDING | Awaiting test pass | - | - |
| Formatting | ⏸️ PENDING | Awaiting test pass | - | - |
| Security Scan | ⏸️ PENDING | Awaiting quality pass | - | - |
| OWASP Compliance | ⏸️ PENDING | Awaiting quality pass | - | - |

**Gates Passed**: 2/9 (22%)
**Gates Failed**: 1/9 (11%)
**Gates Pending**: 6/9 (67%)
```

### Step 5: Handle Specialist Failures

When specialist fails, coordinate with recursive-communicator:

**Failure Handling**:
```markdown
### Specialist Failure: test-runner-specialist (Iteration 2/5)

**Failures Detected**:
1. test_validation_coordinator.py::test_sequential_invocation - AssertionError
2. test_validation_coordinator.py::test_failure_tracking - KeyError
3. test_validation_coordinator.py::test_workflow_completion - AttributeError

**Failure Analysis**:
- **Pattern**: All failures in validation-coordinator tests
- **Root Cause**: Implementation logic errors in specialist invocation
- **Impact**: Blocks validation workflow progression

**Action Taken**:
1. Logged failure details
2. Triggered recursive-communicator skill
3. Formatted failure report for main agent
4. Awaiting main agent fix

**Re-validation Plan**:
1. Main agent fixes implementation logic
2. Main agent signals completion
3. Re-invoke test-runner-specialist (Iteration 3/5)
4. If pass: Proceed to code quality
5. If fail: Repeat (max 5 iterations total)

**Status**: Awaiting Fix
```

### Step 6: Generate Validation Status Reports

Create status snapshots for orchestrator and main agent:

**Status Report Format**:
```markdown
## Validation Status Report

**Generated**: 2025-10-29 14:40:22
**Issue**: #47 - Validation Orchestrator Agent
**Overall Status**: ⚠️ IN PROGRESS

### Summary
Validation in progress. Unit and integration tests written successfully. Test execution encountered 3 failures (iteration 2/5). Recursive communication with main agent active for fixes.

### Specialist Status
| Specialist | Status | Iteration | Result |
|------------|--------|-----------|--------|
| Unit Test Specialist | ✅ Completed | 1/1 | 45 unit tests created |
| Integration Test Specialist | ✅ Completed | 1/1 | 12 integration tests created |
| Test Runner Specialist | ⚠️ In Progress | 2/5 | 3 test failures |
| Code Quality Specialist | ⏸️ Pending | - | Awaiting test pass |
| Security Specialist | ⏸️ Pending | - | Awaiting quality pass |
| E2E Specialist | N/A | - | Backend only |

### Quality Gates
- ✅ Unit tests written (45 tests)
- ✅ Integration tests written (12 tests)
- ⚠️ All tests pass (3 failures)
- ⏸️ Coverage ≥80% (pending)
- ⏸️ Code quality (pending)
- ⏸️ Security scan (pending)

### Current Blocking Issue
**Test Failures** (3):
- test_validation_coordinator.py::test_sequential_invocation
- test_validation_coordinator.py::test_failure_tracking
- test_validation_coordinator.py::test_workflow_completion

**Action**: Recursive communication with main agent for fixes

### Progress
- **Specialists Completed**: 2/5 (40%)
- **Validation Time**: 00:15:32
- **Estimated Remaining**: ~00:15:00 (including fix time)

### Next Steps
1. Await main agent fixes for test failures
2. Re-run test-runner-specialist (iteration 3/5)
3. If pass: Proceed to code-quality-specialist
4. Continue sequential validation workflow
```

### Step 7: Detect Validation Completion

Identify when all validations pass:

**Completion Detection**:
```markdown
### Validation Complete Check

**All Specialists Complete?**
- [✅] Unit Test Specialist: Completed
- [✅] Integration Test Specialist: Completed
- [✅] Test Runner Specialist: Completed (iteration 3)
- [✅] Code Quality Specialist: Completed (iteration 1)
- [✅] Security Specialist: Completed (iteration 2)
- [N/A] E2E Specialist: Not applicable (backend only)

**All Quality Gates Passed?**
- [✅] Unit tests written: 45 tests
- [✅] Integration tests written: 12 tests
- [✅] All tests pass: 57/57
- [✅] Coverage ≥80%: 87.3%
- [✅] Linting: No errors
- [✅] Type checking: No errors
- [✅] Formatting: Compliant
- [✅] Security scan: Clean
- [✅] OWASP Top 10: Compliant

**Result**: ✅ ALL VALIDATIONS PASSED

**Total Validation Time**: 00:42:15
**Total Iterations**: 6 (across all specialists)

**Ready for Phase 6**: Deployment
```

### Step 8: Generate Final Validation Summary

Create comprehensive summary for validation report:

**Final Summary Format**:
```markdown
## Validation Summary: Feature #47

**Overall Status**: ✅ ALL VALIDATIONS PASSED

### Execution Summary
- **Total Specialists Invoked**: 5 (E2E not needed - backend only)
- **Total Iterations**: 6
  - Unit Test Specialist: 1
  - Integration Test Specialist: 1
  - Test Runner Specialist: 3 (2 re-runs after fixes)
  - Code Quality Specialist: 1
  - Security Specialist: 2 (1 re-run after fix)
- **Total Validation Time**: 00:42:15
- **Recursive Fix Cycles**: 2 (test failures, security vulnerability)

### Quality Gates Achieved
- ✅ 45 unit tests written and passing
- ✅ 12 integration tests written and passing
- ✅ 87.3% code coverage (target: ≥80%)
- ✅ Zero linting errors
- ✅ Zero type errors
- ✅ Code formatting compliant
- ✅ Zero security vulnerabilities
- ✅ OWASP Top 10 compliant

### Validation Documentation
- Test Report: /docs/implementation/tests/feature-47-tests.md
- Quality Report: /docs/implementation/quality/feature-47-quality.md
- Security Report: /docs/implementation/security/feature-47-security.md

### Issues Resolved
1. **Test Failures (Iteration 2-3)**: 3 unit test failures resolved via main agent fix
2. **Security Vulnerability (Iteration 1-2)**: Input validation issue resolved via main agent fix

**Validation Complete**: 2025-10-29 15:18:33
**Deployment Readiness**: ✅ READY
```

## Best Practices

### 1. Strict Sequential Execution
- Always invoke specialists in correct order
- Never skip prerequisite checks
- Ensure dependencies are satisfied before invocation

### 2. Comprehensive Status Tracking
- Log every specialist invocation with timestamp
- Track iterations for each specialist
- Maintain detailed failure history
- Update status after every specialist completion

### 3. Clear Progress Visualization
- Provide real-time validation progress
- Show which phase is active
- Highlight blocking issues
- Estimate remaining time

### 4. Proactive Failure Management
- Detect failures immediately
- Trigger recursive communication promptly
- Track iteration counts
- Escalate after max iterations (5)

### 5. Quality Gate Enforcement
- Do not proceed to next specialist if current fails
- Ensure all quality gates pass before completion
- Validate final status before reporting to orchestrator

### 6. Detailed Documentation
- Maintain validation history
- Document all failures and resolutions
- Generate comprehensive final summary
- Provide traceability for validation decisions

## Resources

### validation-workflow.md
Comprehensive guide for validation workflow management including:
- Specialist invocation procedures
- Dependency resolution logic
- Sequential execution patterns
- Failure handling workflows
- Status tracking mechanisms

### validation-checklist.md
Quality gate checklist including:
- Test writing checkpoints
- Test execution requirements
- Code quality standards
- Security compliance criteria
- E2E and accessibility standards
- Deployment readiness criteria

## Example Usage

### Input (Validation Initialization)

```markdown
**Issue**: #47
**PRP**: /docs/implementation/prp/feature-47-prp.md
**Implementation Files**:
- .claude/agents/validation-orchestrator.md
- .claude/skills/validation-coordinator/
- .claude/skills/recursive-communicator/
**Technology Stack**: Markdown (Agent/Skill configs)
**Frontend**: No (backend agent/skill configuration)
```

### Output (Validation Progress)

```markdown
## Validation Workflow: Feature #47

**Status**: In Progress (Phase 2: Test Execution)

### Specialist Status
- ✅ Unit Test Specialist: Completed (1/1) - 45 tests created
- ✅ Integration Test Specialist: Completed (1/1) - 12 tests created
- ⚠️ Test Runner Specialist: In Progress (2/5) - 3 failures, recursive communication active
- ⏸️ Code Quality Specialist: Pending
- ⏸️ Security Specialist: Pending
- N/A E2E Specialist: Not applicable (backend only)

### Quality Gates
- ✅ Unit tests written
- ✅ Integration tests written
- ⚠️ All tests pass (3 failures)
- ⏸️ Coverage ≥80%
- ⏸️ Code quality
- ⏸️ Security scan

**Current Issue**: Test failures - recursive communication with main agent for fixes
**Progress**: 2/5 specialists completed (40%)
**Time Elapsed**: 00:15:32
```

## Integration

This skill is used by:
- **validation-orchestrator** agent during Phase 5: Validation
- Activates automatically when orchestrator coordinates validation specialists
- Works in conjunction with **recursive-communicator** skill for failure handling
- Provides validation status for main orchestrator and deployment phase

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when coordinating validation workflow)
**Phase**: 5 (Validation)
**Created**: 2025-10-29