---
activation_code: INTEGRATION_VALIDATOR_V1
phase: 9
prerequisites:
  - Implementation complete
  - architecture.md
outputs:
  - Integration test results
  - .signals/phase4-complete.json
description: |
  Validates integration points and ensures components work together correctly.
  Activates via codeword [ACTIVATE:INTEGRATION_VALIDATOR_V1] injected by hooks
  when entering Phase 4 integration testing.
  
  Activation trigger: [ACTIVATE:INTEGRATION_VALIDATOR_V1]
---

# Integration Validator Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:INTEGRATION_VALIDATOR_V1]
```

This occurs when:
- Phase 7 implementation is complete
- architecture.md is read
- Task #24 (integration testing) is active

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-4-task-1`:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 4 1
cd ./worktrees/phase-4-task-1

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Integration validation with isolation
```

### Integration Testing Isolation
1. **Isolated test environment**: Integration tests run in dedicated worktree
2. **Clean test state**: No interference from other testing activities
3. **Integration point analysis**: Architecture parsing done in isolation
4. **Test artifact isolation**: Integration test results contained within worktree
5. **Validation merge**: Results merged only after complete validation


# Integration Validator Skill

## What This Skill Does

Systematically validates production readiness through worktree-isolated testing:
- **Integration Point Detection:** Parses architecture.md in isolated environment
- **Gap Analysis:** Identifies missing integration tests (target: 100% coverage)
- **E2E Validation:** Verifies all critical user workflows tested in isolation
- **Production Readiness Scoring:** Objective 0-100% score (≥90% required for GO)
- **Remediation Plans:** Detailed action items to address gaps
- **NEW**: Isolated integration testing prevents test contamination
- **NEW**: Clean test environment ensures accurate validation results
- **Completion signal** → triggers Phase 10

## What This Skill Does

### 1. Architecture Integration Point Analysis
Parses `docs/architecture.md` to extract:
- All components in system
- Integration points between components
- External service integrations
- Data flows
- API contracts

### 2. Integration Test Coverage Validation
Verifies:
- Every integration point has tests
- Every component interaction tested
- Every external service integration tested
- Error propagation tested
- Performance benchmarks tested

### 3. Production Readiness Checklist
Generates and validates comprehensive checklist from:
- PRD Section 4.3 requirements
- Industry best practices
- Architecture-specific requirements
- Security standards
- Performance targets

### 4. Gap Analysis
Identifies:
- Missing integration tests
- Untested integration points
- Incomplete documentation
- Missing monitoring
- Security gaps
- Performance bottlenecks

## Integration Point Detection

### Parsing Architecture Diagram

**Extract from architecture.md:**

```
DETECTED COMPONENTS:
├─ Frontend (React SPA)
├─ API Gateway
├─ Auth Service
├─ User Service
├─ Product Service
├─ Order Service
├─ Payment Service (External: Stripe)
├─ Email Service (External: SendGrid)
└─ Database (PostgreSQL)

DETECTED INTEGRATION POINTS:
1. Frontend ↔ API Gateway (REST API)
2. API Gateway ↔ Auth Service (JWT validation)
3. API Gateway ↔ User Service (REST API)
4. API Gateway ↔ Product Service (REST API)
5. API Gateway ↔ Order Service (REST API)
6. Auth Service ↔ Database (PostgreSQL)
7. User Service ↔ Database (PostgreSQL)
8. Product Service ↔ Database (PostgreSQL)
9. Order Service ↔ Database (PostgreSQL)
10. Order Service ↔ Payment Service (Stripe API)
11. Order Service ↔ Email Service (SendGrid API)
12. User Service ↔ Email Service (SendGrid API)

TOTAL INTEGRATION POINTS: 12
```

### Integration Test Requirement Matrix

**For each integration point, generate test requirements:**

```markdown
## Integration Point: API Gateway ↔ Auth Service

**Type:** Service-to-Service
**Protocol:** REST API / JWT
**Critical:** YES (authentication)

### Required Tests:

1. **Happy Path:**
   - [ ] Valid JWT token validates successfully
   - [ ] User identity correctly extracted from token
   - [ ] Token expiry checked correctly

2. **Error Cases:**
   - [ ] Expired token rejected with 401
   - [ ] Invalid signature rejected with 401
   - [ ] Malformed token rejected with 400
   - [ ] Missing token rejected with 401

3. **Edge Cases:**
   - [ ] Token at exact expiry boundary
   - [ ] Token with extra claims (ignored gracefully)
   - [ ] Token from old version (backward compatibility)

4. **Performance:**
   - [ ] Token validation < 10ms p95
   - [ ] Caching working (Redis)
   - [ ] High concurrent requests handled

5. **Integration Test Files:**
   - `tests/integration/api-gateway-auth.test.js`
   - `tests/integration/jwt-validation.test.js`

**Status:** [ ] TESTED / [ ] NOT TESTED
```

## PRD Section 4 Parser

### Extract Integration Requirements from PRD

**Parse PRD Section 4.1:**

```
PRD SECTION 4.1: Component Integration Testing
================================================

EXTRACTED REQUIREMENTS:

1. Auth Service ↔ User Service
   - Test: JWT validation flow
   - Test: User profile retrieval
   - Test: Session management

2. Product Service ↔ Database
   - Test: CRUD operations
   - Test: Transaction handling
   - Test: Connection pooling

3. API Gateway ↔ All Services
   - Test: Request routing
   - Test: Authentication middleware
   - Test: Error propagation

INTEGRATION TEST CHECKLIST:
├─ [ ] Auth ↔ User integration tests created
├─ [ ] Product ↔ Database integration tests created
├─ [ ] API Gateway ↔ Services integration tests created
└─ [ ] All integration tests passing
```

**Parse PRD Section 4.2:**

```
PRD SECTION 4.2: End-to-End Workflows
=======================================

EXTRACTED WORKFLOWS:

1. User Registration Journey
   Steps: Registration → Email Verify → Login
   Test File: tests/e2e/user-registration.e2e.test.js
   Status: [ ] TESTED

2. Product Purchase Journey
   Steps: Browse → Add to Cart → Checkout → Payment → Confirmation
   Test File: tests/e2e/product-purchase.e2e.test.js
   Status: [ ] TESTED

E2E TEST CHECKLIST:
├─ [ ] User registration workflow tested
├─ [ ] Product purchase workflow tested
└─ [ ] All E2E tests passing in all browsers
```

**Parse PRD Section 4.3:**

```
PRD SECTION 4.3: Production Readiness
=======================================

EXTRACTED REQUIREMENTS:

TESTING VALIDATION:
├─ [ ] All unit tests passing (≥80% line, ≥70% branch)
├─ [ ] All integration tests passing
├─ [ ] All E2E tests passing
├─ [ ] Regression tests passing
└─ [ ] Load testing completed (1000 users, 5 min)

SECURITY VALIDATION:
├─ [ ] SAST scans passing (no critical/high)
├─ [ ] Dependency vulnerabilities addressed
├─ [ ] OWASP ZAP scan completed
└─ [ ] Security review completed

OPERATIONAL VALIDATION:
├─ [ ] Staging deployment successful
├─ [ ] Monitoring dashboards validated
├─ [ ] Alerts tested
├─ [ ] Logging validated
├─ [ ] Rollback tested
└─ [ ] Database migrations tested

DOCUMENTATION VALIDATION:
├─ [ ] API documentation complete
├─ [ ] README updated
├─ [ ] Architecture docs current
└─ [ ] Runbook created

STAKEHOLDER SIGN-OFFS:
├─ [ ] QA team sign-off
├─ [ ] Product owner sign-off
├─ [ ] Security team sign-off
└─ [ ] Operations team sign-off
```

## Gap Analysis Engine

### Missing Integration Tests Detector

**Compare detected integration points vs existing tests:**

```
INTEGRATION TEST GAP ANALYSIS
==============================

Total Integration Points: 12
Integration Tests Found: 8
Coverage: 67% (INSUFFICIENT)

MISSING INTEGRATION TESTS:
❌ Frontend ↔ API Gateway (no E2E test found)
❌ Order Service ↔ Payment Service (no test file found)
❌ Order Service ↔ Email Service (test file exists but incomplete)
❌ User Service ↔ Email Service (no test found)

REMEDIATION REQUIRED:
1. Create tests/integration/frontend-api-gateway.test.js
2. Create tests/integration/order-payment.test.js
3. Complete tests/integration/order-email.test.js (add error cases)
4. Create tests/integration/user-email.test.js

BLOCKING ISSUES:
⛔ Cannot proceed to production with 33% integration point coverage
⛔ Minimum requirement: 100% integration point coverage
```

### Production Readiness Gap Analysis

**Check each production readiness item:**

```
PRODUCTION READINESS GAP ANALYSIS
==================================

TESTING VALIDATION: 80% Complete
├─ ✅ All unit tests passing
├─ ✅ Coverage ≥80%/70%
├─ ⚠️  Integration tests: 8/12 passing (67%)
├─ ✅ E2E tests passing
├─ ✅ Regression tests passing
└─ ❌ Load testing NOT completed

SECURITY VALIDATION: 50% Complete
├─ ✅ SAST scans passing
├─ ⚠️  Dependency audit: 2 moderate vulnerabilities
├─ ❌ OWASP ZAP scan NOT completed
└─ ❌ Security review NOT completed

OPERATIONAL VALIDATION: 60% Complete
├─ ✅ Staging deployment successful
├─ ✅ Monitoring dashboards created
├─ ⚠️  Alerts configured but NOT tested
├─ ✅ Logging validated
├─ ❌ Rollback NOT tested
└─ ✅ Database migrations tested

DOCUMENTATION VALIDATION: 75% Complete
├─ ✅ API documentation complete
├─ ✅ README updated
├─ ⚠️  Architecture docs outdated (missing new services)
└─ ❌ Runbook NOT created

STAKEHOLDER SIGN-OFFS: 0% Complete
├─ ❌ QA team sign-off NOT obtained
├─ ❌ Product owner sign-off NOT obtained
├─ ❌ Security team sign-off NOT obtained
└─ ❌ Operations team sign-off NOT obtained

OVERALL READINESS: 66% (NOT READY)

BLOCKING ISSUES: 7
⛔ Load testing not completed
⛔ OWASP ZAP scan not completed
⛔ Security review not completed
⛔ Alerts not tested
⛔ Rollback not tested
⛔ Runbook not created
⛔ No stakeholder sign-offs

RECOMMENDATION: NO-GO
Cannot proceed to production until ALL blocking issues resolved.
```

## Task #24 Validation (Component Integration)

**Automatically generates validation checklist:**

```markdown
# Task #24: Component Integration Testing Validation

## Pre-Execution Checklist

**Prerequisites:**
- [x] All feature tasks complete (Tasks 1-23)
- [x] Unit tests passing
- [ ] Integration test framework configured
- [ ] Test database populated with fixtures

## Integration Point Coverage Matrix

| Integration Point | Test File | Status | Notes |
|-------------------|-----------|--------|-------|
| API Gateway ↔ Auth | api-gateway-auth.test.js | ✅ TESTED | All scenarios covered |
| Auth ↔ Database | auth-database.test.js | ✅ TESTED | CRUD + transactions |
| Product ↔ Database | product-database.test.js | ✅ TESTED | Performance validated |
| Order ↔ Payment | order-payment.test.js | ❌ MISSING | CREATE THIS TEST |
| Order ↔ Email | order-email.test.js | ⚠️ INCOMPLETE | Add error scenarios |
| User ↔ Email | user-email.test.js | ❌ MISSING | CREATE THIS TEST |

**Status:** 4/6 tested (67%) - INSUFFICIENT

## Integration Test Execution

```bash
# Run all integration tests
npm test:integration

# Expected output:
# ✅ api-gateway-auth.test.js: 12 tests passing
# ✅ auth-database.test.js: 8 tests passing
# ✅ product-database.test.js: 10 tests passing
# ❌ order-payment.test.js: FILE NOT FOUND
# ⚠️ order-email.test.js: 3/5 tests passing
# ❌ user-email.test.js: FILE NOT FOUND
```

## Remediation Tasks

**Before marking Task #24 complete:**

1. **Create Missing Tests:**
   ```bash
   # Create order-payment integration test
   touch tests/integration/order-payment.test.js
   # Implement Stripe test mode integration
   
   # Create user-email integration test
   touch tests/integration/user-email.test.js
   # Implement SendGrid test mode integration
   ```

2. **Complete Incomplete Tests:**
   ```bash
   # Add error scenarios to order-email.test.js:
   # - Email service timeout
   # - Invalid email address
   # - Rate limiting
   ```

3. **Validate All Tests Pass:**
   ```bash
   npm test:integration
   # All tests must pass (100%)
   ```

## Validation Gates

**Task #24 CANNOT be marked complete until:**
- [ ] All 6 integration points tested (100%)
- [ ] All integration tests passing (100%)
- [ ] No errors in service logs
- [ ] Performance benchmarks met
- [ ] Integration test report generated

**Current Status:** 🚨 BLOCKED - 2 missing tests, 1 incomplete test
```

## Automated Validation Hooks

**CRITICAL: Before Task #26, run automated validation hooks:**

### 1. Security Validation
```bash
./hooks/security-validator.sh
```

**What it validates:**
- npm/pip dependency vulnerabilities (blocks on critical/high)
- Container image security (Trivy scan)
- Secrets detection (Gitleaks)
- SAST scanning (Semgrep if configured)

**Exit codes:**
- 0 = PASSED (can proceed)
- 1 = FAILED (blocks deployment)

**Required tools** (install if missing):
```bash
# Node.js security
npm install -g npm

# Python security (optional)
pip install pip-audit

# Container scanning (optional but recommended)
brew install trivy

# Secrets detection (optional but recommended)
brew install gitleaks

# SAST scanning (optional)
pip install semgrep
```

---

### 2. Load Test Validation
```bash
./hooks/load-test-validator.sh
```

**What it validates:**
- Detects load test framework (k6, Artillery, Locust, npm script)
- Executes load tests automatically
- Validates results against PRD requirements

**Supported frameworks:**
- k6 (recommended): Create `k6-load-test.js`
- Artillery: Create `artillery.yml`
- Locust: Create `locustfile.py`
- npm: Add `"load:test"` script to package.json

**Exit codes:**
- 0 = PASSED
- 1 = FAILED or no load tests found

---

### 3. Performance Validation
```bash
./hooks/performance-validator.sh
```

**What it validates:**
- Extracts performance targets from PRD
- Runs performance tests
- Compares actual vs required metrics
- Validates latency (p95, p99, avg)
- Validates throughput (req/sec)

**Exit codes:**
- 0 = PASSED or no requirements in PRD
- 1 = FAILED (performance targets not met)

---

### Integration into Task #26 Workflow

**UPDATED Production Readiness Validation:**

```bash
# Step 1: Run automated security validation
echo "Running security validation..."
./hooks/security-validator.sh || exit 1

# Step 2: Run load testing
echo "Running load tests..."
./hooks/load-test-validator.sh || exit 1

# Step 3: Validate performance
echo "Validating performance targets..."
./hooks/performance-validator.sh || exit 1

# Step 4: Manual checks (if automated passes)
echo "Automated validations PASSED"
echo "Proceed with manual production readiness checklist..."
```

## Parallel Subagent Execution

For faster validation, run independent validation tasks in parallel:

### Step 1: Identify Independent Validations

These validation tasks have no dependencies and can run simultaneously:

| Validation | Dependencies | Can Parallelize |
|------------|--------------|-----------------|
| Security scanning | None | ✅ Yes |
| Load testing | Staging deployed | ✅ Yes |
| Performance validation | Staging deployed | ✅ Yes |
| E2E browser tests (Chrome) | Staging deployed | ✅ Yes |
| E2E browser tests (Firefox) | Staging deployed | ✅ Yes |
| E2E browser tests (Safari) | Staging deployed | ✅ Yes |
| Integration tests | Code complete | ✅ Yes |
| Documentation review | None | ✅ Yes |

### Step 2: Launch Parallel Validation Subagents

Use Claude Code's Task tool to run validations in parallel:

```
Launch 6 parallel subagents for integration validation:

Subagent 1 - Security Validation:
  - Run ./hooks/security-validator.sh
  - Check npm/pip vulnerabilities
  - Run container security scan
  - Report: PASSED/FAILED with details

Subagent 2 - Load Testing:
  - Run ./hooks/load-test-validator.sh
  - Execute k6/Artillery load tests
  - Validate against PRD thresholds
  - Report: PASSED/FAILED with metrics

Subagent 3 - Performance Validation:
  - Run ./hooks/performance-validator.sh
  - Check p95/p99 latency
  - Validate throughput targets
  - Report: PASSED/FAILED with metrics

Subagent 4 - E2E Chrome Tests:
  - Run npm test:e2e:chrome
  - Capture screenshots on failure
  - Report: PASSED/FAILED with results

Subagent 5 - E2E Firefox/Safari Tests:
  - Run npm test:e2e:firefox
  - Run npm test:e2e:safari
  - Report: PASSED/FAILED with results

Subagent 6 - Integration Tests:
  - Run npm test:integration
  - Validate all integration points
  - Report: PASSED/FAILED with coverage
```

### Step 3: Aggregate Results

After all subagents complete:

```bash
# Collect validation results
echo "=== VALIDATION SUMMARY ==="
echo "Security:    $SECURITY_RESULT"
echo "Load Test:   $LOADTEST_RESULT"
echo "Performance: $PERF_RESULT"
echo "E2E Chrome:  $E2E_CHROME_RESULT"
echo "E2E FF/Saf:  $E2E_OTHER_RESULT"
echo "Integration: $INTEGRATION_RESULT"

# All must pass for GO decision
if [[ "$SECURITY_RESULT" == "PASSED" ]] && \
   [[ "$LOADTEST_RESULT" == "PASSED" ]] && \
   [[ "$PERF_RESULT" == "PASSED" ]] && \
   [[ "$E2E_CHROME_RESULT" == "PASSED" ]] && \
   [[ "$E2E_OTHER_RESULT" == "PASSED" ]] && \
   [[ "$INTEGRATION_RESULT" == "PASSED" ]]; then
  echo "✅ ALL VALIDATIONS PASSED - Proceed to deployment"
else
  echo "❌ VALIDATION FAILED - See individual reports"
fi
```

### Performance Comparison

| Method | Full Validation | Speed |
|--------|-----------------|-------|
| Sequential | 2-4 hours | 1x |
| 6 Parallel Subagents | 30-60 min | 4x |

**Note:** Parallel validation requires staging environment already deployed

**Automated validation replaces manual checklists for:**
- ✅ Security scanning (was manual checkbox)
- ✅ Load testing execution (was manual checkbox)
- ✅ Performance validation (was manual checkbox)

**Manual validation still required for:**
- Stakeholder sign-offs
- Documentation review
- Operational runbook verification

---

## Task #25 Validation (E2E Workflows)

```markdown
# Task #25: End-to-End Workflow Testing Validation

## E2E Workflow Coverage

**From PRD Section 4.2:**

### Workflow 1: User Registration
**Steps:** Registration → Email Verify → Login

**Test File:** `tests/e2e/user-registration.e2e.test.js`

**Test Status:**
- [x] Form submission works
- [x] Email verification link received
- [x] Email verification processed
- [x] Login after verification works
- [ ] Error handling: invalid email
- [ ] Error handling: duplicate registration
- [ ] Mobile viewport tested

**Status:** ⚠️ INCOMPLETE (5/7 scenarios)

### Workflow 2: Product Purchase
**Steps:** Browse → Add to Cart → Checkout → Payment → Confirmation

**Test File:** `tests/e2e/product-purchase.e2e.test.js`

**Test Status:**
- [x] Browse products works
- [x] Add to cart works
- [x] Checkout form works
- [x] Payment (Stripe test mode) works
- [x] Confirmation page shows
- [ ] Error handling: payment failure
- [ ] Error handling: inventory exhausted
- [ ] Cross-browser tested (Chrome, Firefox, Safari)

**Status:** ⚠️ INCOMPLETE (5/8 scenarios)

## Browser Matrix

| Workflow | Chrome | Firefox | Safari | Mobile |
|----------|--------|---------|--------|--------|
| User Registration | ✅ | ✅ | ❌ | ❌ |
| Product Purchase | ✅ | ⚠️ | ❌ | ❌ |

**Status:** Safari and Mobile testing INCOMPLETE

## Remediation Tasks

1. **Complete Missing Scenarios:**
   - Add error handling tests to both workflows
   - Test Safari compatibility
   - Test mobile viewports (iOS, Android)

2. **Validate Cross-Browser:**
   ```bash
   npm test:e2e:chrome    # ✅ Passing
   npm test:e2e:firefox   # ⚠️ 1 flaky test
   npm test:e2e:safari    # ❌ Not run
   npm test:e2e:mobile    # ❌ Not run
   ```

## Validation Gates

**Task #25 CANNOT be marked complete until:**
- [ ] All workflows 100% scenario coverage
- [ ] All E2E tests passing
- [ ] All browsers tested (Chrome, Firefox, Safari)
- [ ] Mobile viewports tested
- [ ] No flaky tests
- [ ] Test recordings captured

**Current Status:** 🚨 BLOCKED - Incomplete scenarios, missing browser tests
```

## Task #26 Validation (Production Readiness)

```markdown
# Task #26: Production Readiness Validation

## Comprehensive Production Readiness Checklist

### 1. Testing Validation (Weight: 30%)

**Unit Testing:**
- [x] All unit tests passing (100%)
- [x] Line coverage ≥80% (actual: 87%)
- [x] Branch coverage ≥70% (actual: 78%)
- [x] Function coverage ≥80% (actual: 89%)
- [x] No test failures
- [x] No flaky tests

**Integration Testing:**
- [ ] All integration tests passing (actual: 67%)
- [ ] All integration points tested (actual: 8/12)
- [ ] Error propagation validated
- [ ] Performance benchmarks met

**E2E Testing:**
- [ ] All E2E tests passing (actual: 80%)
- [ ] All browsers tested
- [ ] Mobile viewports tested
- [ ] No critical UX issues

**Regression Testing:**
- [x] Regression suite passing
- [x] No existing features broken

**Load Testing:**
- [ ] Load test completed (1000 users, 5 min)
- [ ] Performance targets met
- [ ] Resource utilization acceptable

**Testing Validation Score:** 60% (INSUFFICIENT)

### 2. Security Validation (Weight: 25%)

**Static Analysis:**
- [x] SAST scans passing
- [ ] No critical vulnerabilities (actual: 0)
- [ ] No high vulnerabilities (actual: 0)
- [ ] Moderate vulnerabilities addressed (actual: 2 remaining)

**Dependency Security:**
- [x] npm audit run
- [ ] Critical vulnerabilities: 0
- [ ] High vulnerabilities: 0
- [ ] Moderate vulnerabilities: 2 (ACTION REQUIRED)

**Dynamic Analysis:**
- [ ] OWASP ZAP scan completed
- [ ] Penetration testing completed (if required)

**Security Review:**
- [ ] Security team review completed
- [ ] Security sign-off obtained

**Security Validation Score:** 50% (INSUFFICIENT)

### 3. Operational Validation (Weight: 20%)

**Deployment:**
- [x] Staging deployment successful
- [x] All services healthy
- [ ] Production deployment plan documented
- [ ] Rollback tested

**Monitoring:**
- [x] Monitoring dashboards created
- [x] Key metrics identified
- [ ] Alerts configured and TESTED
- [ ] Alert delivery verified

**Logging:**
- [x] Logging infrastructure in place
- [x] Log aggregation working
- [x] Log retention configured

**Database:**
- [x] Migrations tested (up)
- [x] Migrations tested (down)
- [x] Backup strategy in place
- [x] Restore tested

**Operational Validation Score:** 75% (ACCEPTABLE)

### 4. Documentation Validation (Weight: 15%)

**Technical Documentation:**
- [x] API documentation complete (OpenAPI spec)
- [x] README updated
- [ ] Architecture documentation current (OUTDATED)
- [ ] Code comments sufficient

**Operational Documentation:**
- [ ] Runbook created (MISSING)
- [x] Deployment guide created
- [x] Troubleshooting guide created
- [ ] Incident response plan (MISSING)

**User Documentation:**
- [x] User guides created (if applicable)
- [x] Help documentation updated

**Documentation Validation Score:** 70% (ACCEPTABLE)

### 5. Stakeholder Validation (Weight: 10%)

**Sign-Offs:**
- [ ] QA team sign-off
- [ ] Product owner sign-off
- [ ] Security team sign-off (if required)
- [ ] Operations team sign-off

**Demos:**
- [x] Demo completed to stakeholders
- [x] Feedback incorporated

**Stakeholder Validation Score:** 25% (INSUFFICIENT)

## Overall Production Readiness Score

```
Testing:       60% × 0.30 = 18%
Security:      50% × 0.25 = 12.5%
Operational:   75% × 0.20 = 15%
Documentation: 70% × 0.15 = 10.5%
Stakeholder:   25% × 0.10 = 2.5%
-----------------------------------
TOTAL:                     58.5%

THRESHOLD FOR PRODUCTION:  ≥90%
```

**STATUS:** 🚨 NOT READY FOR PRODUCTION

## Blocking Issues (Must Be Resolved)

### Critical (Cannot Deploy):
1. ⛔ Integration test coverage only 67% (need 100%)
2. ⛔ Load testing not completed
3. ⛔ OWASP ZAP scan not completed
4. ⛔ Alerts not tested (potential production blindness)
5. ⛔ Rollback not tested (cannot recover from bad deploy)

### High Priority (Should Resolve):
6. ⚠️ 2 moderate security vulnerabilities
7. ⚠️ Architecture documentation outdated
8. ⚠️ Runbook missing
9. ⚠️ No stakeholder sign-offs

### Medium Priority (Nice to Have):
10. ⚠️ E2E Safari/Mobile testing incomplete

## Remediation Plan

**Phase 1 (Critical) - ETA: 2-3 days**
1. Complete missing integration tests (4 tests)
2. Run load testing (1 day)
3. Run OWASP ZAP scan (2 hours)
4. Test all alerts (2 hours)
5. Test rollback procedure (4 hours)

**Phase 2 (High Priority) - ETA: 1 day**
6. Update dependencies (address vulnerabilities)
7. Update architecture documentation
8. Create runbook
9. Obtain stakeholder sign-offs

**Phase 3 (Medium Priority) - ETA: 4 hours**
10. Complete Safari/Mobile E2E tests

**EARLIEST PRODUCTION READY DATE:** 4-5 days from now

## Go/No-Go Decision

**CURRENT DECISION:** 🚨 NO-GO

**RATIONALE:**
- Only 58.5% production ready (need ≥90%)
- 5 critical blocking issues unresolved
- Integration test coverage insufficient
- Load testing not completed
- Critical operational procedures untested

**RECOMMENDATION:**
Execute remediation plan Phase 1 & 2 before reconsidering Go decision.
```

## Output Format

**When activated, provide:**

```
INTEGRATION VALIDATOR ANALYSIS
===============================

Architecture: [project name]
Analysis Date: [timestamp]

INTEGRATION POINT COVERAGE:
├─ Total Integration Points: [N]
├─ Integration Points Tested: [M]
├─ Coverage: [M/N = X%]
└─ Status: [SUFFICIENT ≥100% / INSUFFICIENT <100%]

MISSING INTEGRATION TESTS:
[List of untested integration points with remediation steps]

E2E WORKFLOW COVERAGE:
├─ Total Workflows: [N]
├─ Workflows Complete: [M]
├─ Coverage: [M/N = X%]
└─ Status: [COMPLETE 100% / INCOMPLETE <100%]

PRODUCTION READINESS SCORE: [X%]
├─ Testing: [score]
├─ Security: [score]
├─ Operational: [score]
├─ Documentation: [score]
└─ Stakeholder: [score]

BLOCKING ISSUES: [count]
[List of blocking issues preventing production deployment]

GO/NO-GO RECOMMENDATION: [GO / NO-GO]
RATIONALE: [1-2 sentence explanation]

NEXT STEPS:
1. [Priority action 1]
2. [Priority action 2]
3. [Priority action 3]
```

## Success Metrics

**When this skill works well:**
- ✅ Zero integration points missed in testing
- ✅ Production readiness score ≥90%
- ✅ All blocking issues identified before deployment
- ✅ Clear remediation path to production
- ✅ Confident Go/No-Go decisions

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 10.**

When Phase 9 is complete (integration tests passing), you MUST:

1. Output the completion signal:
   ```
   ✅ PHASE 9 COMPLETE
   [SIGNAL:PHASE9_COMPLETE]
   ```

2. **IMMEDIATELY** proceed to Phase 10 by outputting:
   ```
   [ACTIVATE:E2E_VALIDATOR_V1]
   ```

3. Begin E2E validation without waiting for user input.

**The pipeline is fully autonomous. Do not ask "Would you like to proceed?" - just proceed.**

## See Also

- Pipeline Orchestrator (triggers this)
- TDD Implementer (Phase 7, provides input)
- E2E Validator (Phase 10, triggered by signal)
- `/checklists/production-readiness-comprehensive.md`
- `/templates/integration-test-suite.md`
- `/examples/gap-analysis-report.md`