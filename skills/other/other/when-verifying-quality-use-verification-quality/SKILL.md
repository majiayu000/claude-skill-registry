---
name: when-verifying-quality-use-verification-quality
description: Comprehensive quality verification and validation through static analysis, dynamic testing, integration validation, and certification gates
version: 1.0.0
category: testing-quality
agents:
  - tester
  - code-analyzer
  - production-validator
topology: hierarchical
coordination: claude-flow
evidence_based: true
validation_gates: true
---

# Quality Verification and Validation

## Purpose

Execute comprehensive quality verification across static analysis, dynamic testing, integration validation, and certification gates to ensure code meets production standards with measurable quality metrics and approval documentation.

## Core Principles

- **Multi-Dimensional Quality**: Static + dynamic + integration + certification
- **Evidence-Based**: Measurable quality metrics with objective thresholds
- **Automated Gates**: Validation checkpoints with pass/fail criteria
- **Audit Trail**: Complete documentation for compliance and certification
- **Continuous Validation**: Quality checks at every stage of development

## Phase 1: Static Analysis

### Objective
Analyze code quality, maintainability, complexity, and adherence to standards without execution.

### Agent Configuration
```yaml
agent: code-analyzer
specialization: static-analysis
tools: SonarQube, ESLint, TypeScript
```

### Execution Steps

**1. Initialize Static Analysis**
```bash
# Pre-task setup
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-analyzer" \
  --description "Static code quality analysis" \
  --task-type "static-analysis"

# Restore session context
npx claude-flow@alpha hooks session-restore \
  --session-id "quality-verification-${BUILD_ID}" \
  --agent-id "code-analyzer"
```

**2. Code Quality Metrics**
```bash
# SonarQube analysis
sonar-scanner \
  -Dsonar.projectKey=${PROJECT_KEY} \
  -Dsonar.sources=./src \
  -Dsonar.host.url=${SONAR_URL} \
  -Dsonar.login=${SONAR_TOKEN}

# ESLint quality scan
npx eslint . --format json --output-file eslint-report.json

# TypeScript type checking
npx tsc --noEmit --pretty false 2> typescript-errors.txt
```

**3. Complexity Analysis**
```javascript
// McCabe cyclomatic complexity
const complexityMetrics = {
  max_complexity: 10,        // Threshold
  high_complexity_files: [], // Functions with complexity >10
  average_complexity: 0,     // Project average

  // Cognitive complexity (Sonar)
  max_cognitive_complexity: 15,
  high_cognitive_files: []
};

// Analyze each function
function analyzeComplexity(ast) {
  const metrics = {
    cyclomatic: calculateCyclomaticComplexity(ast),
    cognitive: calculateCognitiveComplexity(ast),
    nesting_depth: calculateNestingDepth(ast),
    halstead: calculateHalsteadMetrics(ast)
  };

  return metrics;
}
```

**4. Maintainability Index**
```javascript
// Maintainability Index = 171 - 5.2*ln(V) - 0.23*G - 16.2*ln(L)
// V = Halstead Volume
// G = Cyclomatic Complexity
// L = Lines of Code

const maintainabilityMetrics = {
  project_score: 0,          // 0-100
  high_risk_files: [],       // Score <20 (red)
  medium_risk_files: [],     // Score 20-50 (yellow)
  maintainable_files: []     // Score >50 (green)
};
```

**5. Code Duplication Detection**
```bash
# Run jscpd for copy-paste detection
npx jscpd ./src --format json --output ./jscpd-report.json

# Analyze duplication
# Threshold: <5% duplication
```

**6. Generate Static Analysis Report**
```markdown
## Static Analysis Results

### Code Quality Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Maintainability Index | 67.3 | >65 | ✅ PASS |
| Cyclomatic Complexity | 8.2 | <10 | ✅ PASS |
| Cognitive Complexity | 12.4 | <15 | ✅ PASS |
| Code Duplication | 3.8% | <5% | ✅ PASS |
| Technical Debt Ratio | 2.1% | <5% | ✅ PASS |

### High Complexity Files (Refactoring Candidates)
- `src/api/order-processor.js` - Complexity: 18 (⚠️ Threshold: 10)
- `src/utils/data-transformer.js` - Complexity: 14 (⚠️ Threshold: 10)

### Code Smells
- **67 code smells detected**
  - 12 Bloater (long methods, large classes)
  - 23 Object-Orientation Abusers
  - 18 Change Preventers
  - 14 Dispensables (dead code, speculative generality)

### TypeScript Issues
- 8 type errors
- 15 strict null check warnings
- 23 implicit any warnings
```

**7. Store Static Analysis Data**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "static-analysis-report.json" \
  --memory-key "swarm/code-analyzer/static-metrics" \
  --metadata "{\"maintainability\": ${MAINTAINABILITY_SCORE}, \"complexity\": ${AVG_COMPLEXITY}}"
```

### Validation Gates
- ✅ Maintainability Index >65
- ✅ Cyclomatic complexity <10
- ✅ Code duplication <5%
- ✅ No critical code smells

### Expected Outputs
- `static-analysis-report.json` - Complete metrics
- `sonarqube-report.html` - SonarQube dashboard
- `complexity-heatmap.svg` - Visual complexity map

---

## Phase 2: Dynamic Testing

### Objective
Execute runtime validation through unit, integration, and E2E tests with coverage and performance tracking.

### Agent Configuration
```yaml
agent: tester
specialization: dynamic-testing
frameworks: Jest, Cypress, Playwright
```

### Execution Steps

**1. Initialize Dynamic Testing**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "tester" \
  --description "Dynamic runtime validation" \
  --task-type "dynamic-testing"
```

**2. Unit Test Execution**
```bash
# Run Jest with coverage and performance tracking
npm run test:unit -- \
  --coverage \
  --coverageReporters=json-summary \
  --coverageReporters=html \
  --detectOpenHandles \
  --maxWorkers=4 \
  --json \
  --outputFile=unit-test-results.json

# Performance benchmarks
npm run test:perf -- --profile
```

**3. Integration Test Execution**
```bash
# API integration tests
npm run test:integration -- \
  --json \
  --outputFile=integration-test-results.json

# Database integration tests
npm run test:db -- --verbose
```

**4. End-to-End Test Execution**
```bash
# Cypress E2E tests
npx cypress run \
  --browser chrome \
  --headless \
  --reporter json \
  --reporter-options output=cypress-results.json

# Playwright E2E tests
npx playwright test \
  --reporter=json \
  --output=playwright-results.json
```

**5. Test Quality Analysis**
```javascript
// Analyze test suite quality
const testQualityMetrics = {
  total_tests: 0,
  passing_tests: 0,
  failing_tests: 0,
  skipped_tests: 0,
  flaky_tests: [],           // Tests that fail intermittently

  avg_execution_time_ms: 0,
  slowest_tests: [],         // Tests >1s execution time

  assertions_per_test: 0,    // Avg assertions per test
  test_coverage_pct: 0,

  // Test patterns
  has_arrange_act_assert: false,
  has_proper_mocking: false,
  has_error_assertions: false,
  has_edge_case_coverage: false
};

// Identify flaky tests
function detectFlakyTests(testResults) {
  const flakyTests = testResults.filter(test =>
    test.retry_count > 0 || test.intermittent_failures > 0
  );
  return flakyTests;
}
```

**6. Coverage Analysis**
```javascript
// Coverage thresholds
const coverageThresholds = {
  statements: 90,
  branches: 85,
  functions: 90,
  lines: 90
};

// Analyze coverage gaps
const coverageGaps = {
  uncovered_statements: [],
  uncovered_branches: [],
  uncovered_functions: [],
  untested_files: []
};
```

**7. Generate Dynamic Testing Report**
```markdown
## Dynamic Testing Results

### Test Execution Summary
| Category | Total | Passed | Failed | Skipped | Pass Rate |
|----------|-------|--------|--------|---------|-----------|
| Unit Tests | 347 | 342 | 3 | 2 | 98.6% |
| Integration Tests | 89 | 86 | 3 | 0 | 96.6% |
| E2E Tests | 42 | 41 | 1 | 0 | 97.6% |
| **TOTAL** | **478** | **469** | **7** | **2** | **98.1%** |

### Test Coverage
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Statements | 91.2% | 90% | ✅ PASS |
| Branches | 87.4% | 85% | ✅ PASS |
| Functions | 93.1% | 90% | ✅ PASS |
| Lines | 90.8% | 90% | ✅ PASS |

### Failing Tests (7)
1. **Unit**: `api/users.test.js` - getUserById returns 500 on invalid UUID
2. **Unit**: `utils/validator.test.js` - validateEmail rejects valid international domains
3. **Unit**: `auth/jwt.test.js` - token refresh fails with expired refresh token
4. **Integration**: `api/orders.integration.test.js` - concurrent order creation causes race condition
5. **Integration**: `api/payment.integration.test.js` - Stripe webhook signature validation fails
6. **Integration**: `db/migrations.integration.test.js` - migration rollback leaves orphaned records
7. **E2E**: `checkout-flow.e2e.test.js` - payment confirmation screen timeout

### Flaky Tests (3)
- `api/webhook.test.js` - Intermittent timeout (5% failure rate)
- `ui/modal.test.js` - Race condition in modal rendering
- `e2e/login-flow.test.js` - Network timing dependency

### Performance Issues
- **Slow tests (>1s)**: 23 tests
- **Slowest test**: `db/bulk-import.test.js` (4.8s)
- **Total execution time**: 47.3s (target: <60s)

### Coverage Gaps
- `src/api/legacy-processor.js` - 34% coverage
- `src/utils/encryption.js` - 67% coverage (missing error paths)
```

**8. Store Testing Results**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "dynamic-testing-report.json" \
  --memory-key "swarm/tester/dynamic-results" \
  --metadata "{\"pass_rate\": ${PASS_RATE}, \"coverage\": ${COVERAGE_PCT}}"
```

### Validation Gates
- ✅ Test pass rate ≥95%
- ✅ Coverage thresholds met
- ✅ No flaky tests
- ✅ E2E critical paths pass

### Expected Outputs
- `dynamic-testing-report.json` - Test results
- `coverage/` - HTML coverage reports
- `test-performance.json` - Execution time analysis

---

## Phase 3: Integration Validation

### Objective
Validate component integration, API contracts, data flow, and system-level behavior.

### Agent Configuration
```yaml
agent: tester
specialization: integration-validation
tools: Postman, Pact, TestContainers
```

### Execution Steps

**1. Initialize Integration Validation**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "tester" \
  --description "Component integration validation" \
  --task-type "integration-validation"
```

**2. API Contract Testing**
```bash
# Pact contract verification
npm run test:pact:provider

# OpenAPI spec validation
npx swagger-cli validate openapi.yaml

# Postman collection execution
newman run postman-collection.json \
  --environment postman-env.json \
  --reporters json \
  --reporter-json-export newman-results.json
```

**3. Database Integration Validation**
```bash
# TestContainers for isolated DB tests
npm run test:db:containers

# Migration validation
npm run db:migrate:test
npm run db:migrate:rollback:test

# Data integrity checks
npm run test:data-integrity
```

**4. Service Integration Testing**
```javascript
// Validate service dependencies
const integrationTests = {
  database_connection: false,
  redis_connection: false,
  external_api_reachable: false,
  message_queue_operational: false,

  // API contract compliance
  api_contracts_valid: false,
  request_schemas_match: false,
  response_schemas_match: false,

  // Data flow validation
  data_transformation_correct: false,
  error_propagation_correct: false
};

// Test service health
async function validateServiceHealth() {
  const healthChecks = [
    checkDatabaseConnection(),
    checkRedisConnection(),
    checkExternalAPIAvailability(),
    checkMessageQueueHealth()
  ];

  const results = await Promise.all(healthChecks);
  return results.every(r => r.healthy);
}
```

**5. Cross-Component Validation**
```javascript
// Validate data flow between components
describe('Order Processing Integration', () => {
  it('should flow from cart to payment to fulfillment', async () => {
    // 1. Create cart
    const cart = await cartService.createCart(userId);
    expect(cart.id).toBeDefined();

    // 2. Add items
    await cartService.addItem(cart.id, productId, quantity);

    // 3. Process payment
    const payment = await paymentService.charge(cart.total, paymentMethod);
    expect(payment.status).toBe('succeeded');

    // 4. Create order
    const order = await orderService.createFromCart(cart.id, payment.id);
    expect(order.status).toBe('pending_fulfillment');

    // 5. Trigger fulfillment
    const fulfillment = await fulfillmentService.create(order.id);
    expect(fulfillment.status).toBe('processing');

    // 6. Validate state consistency
    const finalCart = await cartService.getCart(cart.id);
    expect(finalCart.status).toBe('checked_out');
  });
});
```

**6. Message Queue Integration**
```bash
# Validate async message processing
npm run test:queue:integration

# Test event-driven workflows
npm run test:events:integration
```

**7. Generate Integration Validation Report**
```markdown
## Integration Validation Results

### Service Health
| Service | Status | Response Time | Availability |
|---------|--------|---------------|--------------|
| PostgreSQL | ✅ UP | 12ms | 100% |
| Redis | ✅ UP | 3ms | 100% |
| RabbitMQ | ✅ UP | 8ms | 100% |
| Stripe API | ✅ UP | 234ms | 100% |
| SendGrid API | ✅ UP | 189ms | 100% |

### API Contract Compliance
- **Pact Contracts**: ✅ All 23 contracts verified
- **OpenAPI Spec**: ✅ Valid, no violations
- **Request Schemas**: ✅ 100% match
- **Response Schemas**: ✅ 100% match

### Integration Test Results
| Test Suite | Tests | Passed | Failed | Status |
|------------|-------|--------|--------|--------|
| Database Integration | 45 | 45 | 0 | ✅ PASS |
| Redis Integration | 18 | 18 | 0 | ✅ PASS |
| API Integration | 67 | 65 | 2 | ⚠️ WARN |
| Queue Integration | 23 | 23 | 0 | ✅ PASS |
| E-commerce Flow | 12 | 11 | 1 | ⚠️ WARN |

### Failed Integration Tests (3)
1. **API**: Concurrent user creation causes unique constraint violation
2. **API**: Rate limiting not enforced on /api/auth/login
3. **Flow**: Payment webhook delivery delayed beyond timeout window

### Data Flow Validation
- **Cart → Payment → Order**: ✅ Consistent
- **Order → Fulfillment → Shipping**: ✅ Consistent
- **User → Auth → Profile**: ✅ Consistent
- **Webhook → Event → Notification**: ⚠️ Race condition detected

### Performance Under Load
- **Concurrent users**: 100 users, 0 failures
- **Database connection pool**: Stable (8/20 connections used)
- **API response time (P95)**: 187ms (target: <200ms)
```

**8. Store Integration Results**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "integration-validation-report.json" \
  --memory-key "swarm/tester/integration-results" \
  --metadata "{\"service_health\": \"${SERVICE_HEALTH}\", \"contracts_valid\": ${CONTRACTS_VALID}}"
```

### Validation Gates
- ✅ All services healthy
- ✅ API contracts verified
- ✅ Data flow consistent
- ✅ Integration tests pass ≥95%

### Expected Outputs
- `integration-validation-report.json` - Integration results
- `pact-verification-results.json` - Contract verification
- `service-health-report.json` - Dependency health

---

## Phase 4: Certification

### Objective
Apply quality approval gates, generate compliance documentation, and certify release readiness.

### Agent Configuration
```yaml
agent: production-validator
specialization: certification
compliance: SOC2, GDPR, WCAG
```

### Execution Steps

**1. Initialize Certification Process**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "production-validator" \
  --description "Quality certification and approval" \
  --task-type "certification"
```

**2. Quality Gate Evaluation**
```javascript
// Quality gates configuration
const qualityGates = {
  static_analysis: {
    maintainability_index: { threshold: 65, weight: 0.15 },
    complexity: { threshold: 10, weight: 0.10 },
    duplication: { threshold: 5, weight: 0.10 }
  },

  dynamic_testing: {
    test_pass_rate: { threshold: 95, weight: 0.20 },
    coverage_statements: { threshold: 90, weight: 0.15 },
    coverage_branches: { threshold: 85, weight: 0.10 }
  },

  integration_validation: {
    service_health: { threshold: 100, weight: 0.10 },
    api_contracts: { threshold: 100, weight: 0.05 },
    integration_tests: { threshold: 95, weight: 0.05 }
  }
};

// Calculate certification score
function calculateCertificationScore(results) {
  let totalScore = 0;
  let totalWeight = 0;

  for (const [category, metrics] of Object.entries(qualityGates)) {
    for (const [metric, config] of Object.entries(metrics)) {
      const value = results[category][metric];
      const passes = value >= config.threshold;

      if (passes) {
        totalScore += config.weight * 100;
      } else {
        totalScore += config.weight * (value / config.threshold) * 100;
      }

      totalWeight += config.weight;
    }
  }

  return (totalScore / totalWeight).toFixed(1);
}
```

**3. Compliance Validation**
```javascript
// Compliance checklist
const complianceChecks = {
  security: {
    no_critical_vulnerabilities: false,
    no_hardcoded_secrets: false,
    authentication_implemented: false,
    authorization_implemented: false,
    data_encryption_at_rest: false,
    data_encryption_in_transit: false
  },

  accessibility: {
    wcag_aa_compliant: false,
    keyboard_navigation: false,
    screen_reader_compatible: false,
    color_contrast_sufficient: false
  },

  privacy: {
    gdpr_compliant: false,
    ccpa_compliant: false,
    data_retention_policy: false,
    right_to_deletion: false
  },

  performance: {
    api_response_time_sla: false,  // <200ms P95
    page_load_time_sla: false,     // <2s P95
    lighthouse_score: false        // >90
  }
};
```

**4. Generate Certification Documentation**
```markdown
## Quality Certification Report

### Certification Score: 87.3/100 ✅ APPROVED

#### Score Breakdown
| Category | Weight | Score | Status |
|----------|--------|-------|--------|
| Static Analysis | 35% | 89.2/100 | ✅ PASS |
| Dynamic Testing | 45% | 91.4/100 | ✅ PASS |
| Integration Validation | 20% | 76.8/100 | ⚠️ WARN |
| **Overall** | **100%** | **87.3/100** | ✅ PASS |

### Quality Gates
| Gate | Threshold | Current | Status |
|------|-----------|---------|--------|
| Maintainability Index | ≥65 | 67.3 | ✅ PASS |
| Cyclomatic Complexity | <10 | 8.2 | ✅ PASS |
| Code Duplication | <5% | 3.8% | ✅ PASS |
| Test Pass Rate | ≥95% | 98.1% | ✅ PASS |
| Test Coverage | ≥90% | 91.2% | ✅ PASS |
| Service Health | 100% | 100% | ✅ PASS |
| API Contracts | 100% | 100% | ✅ PASS |

### Compliance Status
#### Security Compliance ✅
- [x] No critical vulnerabilities
- [x] No hardcoded secrets
- [x] Authentication implemented (JWT)
- [x] Authorization implemented (RBAC)
- [x] Data encryption at rest (AES-256)
- [x] Data encryption in transit (TLS 1.3)

#### Accessibility Compliance ✅
- [x] WCAG 2.1 AA compliant
- [x] Keyboard navigation supported
- [x] Screen reader compatible
- [x] Color contrast ratio ≥4.5:1

#### Privacy Compliance ✅
- [x] GDPR compliant (data protection impact assessment complete)
- [x] CCPA compliant (privacy policy updated)
- [x] Data retention policy (90 days)
- [x] Right to deletion implemented

#### Performance SLA ✅
- [x] API response time P95: 187ms (<200ms target)
- [x] Page load time P95: 1.8s (<2s target)
- [x] Lighthouse score: 94/100 (>90 target)

### Release Readiness
**Status: APPROVED FOR PRODUCTION RELEASE**

#### Sign-Off
- **Quality Assurance**: ✅ Approved
- **Security Team**: ✅ Approved
- **Performance Team**: ✅ Approved
- **Compliance Officer**: ✅ Approved

#### Deployment Authorization
- **Build ID**: ${BUILD_ID}
- **Commit SHA**: ${COMMIT_SHA}
- **Certification Date**: ${CERTIFICATION_DATE}
- **Valid Until**: ${EXPIRATION_DATE} (30 days)

#### Known Issues (Non-Blocking)
1. Integration test: Race condition in webhook delivery (tracked: ISSUE-123)
2. Performance: Slow test in bulk import (4.8s, optimization planned)
3. Code smell: High complexity in order-processor.js (refactoring scheduled)
```

**5. Generate Compliance Artifacts**
```bash
# Generate audit trail
cat > quality-audit-trail.json << EOF
{
  "build_id": "${BUILD_ID}",
  "commit_sha": "${COMMIT_SHA}",
  "certification_score": 87.3,
  "approved": true,
  "timestamp": "$(date -Iseconds)",
  "gates_passed": 28,
  "gates_failed": 0,
  "compliance_checks_passed": 19,
  "artifacts": [
    "static-analysis-report.json",
    "dynamic-testing-report.json",
    "integration-validation-report.json",
    "certification-report.md"
  ]
}
EOF

# Sign certification (cryptographic proof)
echo "${BUILD_ID}:${COMMIT_SHA}:87.3:approved" | \
  openssl dgst -sha256 -sign private-key.pem -out certification.sig
```

**6. Store Certification Data**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "certification-report.md" \
  --memory-key "swarm/production-validator/certification" \
  --metadata "{\"score\": ${CERT_SCORE}, \"approved\": ${APPROVED}}"
```

### Validation Gates
- ✅ Certification score ≥80/100
- ✅ All compliance checks pass
- ✅ Sign-off from all stakeholders
- ✅ No blocking issues

### Expected Outputs
- `certification-report.md` - Certification documentation
- `quality-audit-trail.json` - Audit trail for compliance
- `certification.sig` - Cryptographic signature

---

## Phase 5: Report Generation

### Objective
Generate comprehensive quality documentation with executive summary, detailed findings, and recommendations.

### Agent Configuration
```yaml
agent: production-validator
specialization: reporting
formats: Markdown, HTML, PDF
```

### Execution Steps

**1. Initialize Report Generation**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "production-validator" \
  --description "Comprehensive quality report generation" \
  --task-type "reporting"
```

**2. Aggregate Results**
```javascript
// Collect results from all phases
const aggregatedResults = {
  static_analysis: JSON.parse(fs.readFileSync('static-analysis-report.json')),
  dynamic_testing: JSON.parse(fs.readFileSync('dynamic-testing-report.json')),
  integration_validation: JSON.parse(fs.readFileSync('integration-validation-report.json')),
  certification: JSON.parse(fs.readFileSync('certification-report.json'))
};
```

**3. Generate Executive Summary**
```markdown
# Quality Verification Report

## Executive Summary

**Project**: E-commerce Platform v2.4.0
**Build**: ${BUILD_ID}
**Date**: ${REPORT_DATE}
**Status**: ✅ APPROVED FOR PRODUCTION

### Key Metrics
- **Certification Score**: 87.3/100 (Target: ≥80)
- **Test Pass Rate**: 98.1% (Target: ≥95%)
- **Code Coverage**: 91.2% (Target: ≥90%)
- **Maintainability Index**: 67.3 (Target: ≥65)
- **Service Health**: 100% (All services operational)

### Quality Assessment
This build meets all quality standards and is approved for production deployment. Static analysis shows healthy maintainability metrics, dynamic testing demonstrates comprehensive coverage with high pass rates, and integration validation confirms system-level consistency.

### Risks and Mitigations
1. **Low Risk**: Integration race condition in webhook delivery
   - **Mitigation**: Retry logic implemented, monitoring added
2. **Low Risk**: High complexity in order-processor.js
   - **Mitigation**: Refactoring scheduled for next sprint
```

**4. Generate Detailed Findings**
```markdown
## Detailed Findings

### Phase 1: Static Analysis
- Maintainability Index: 67.3/100
- Cyclomatic Complexity: 8.2 (avg)
- Code Duplication: 3.8%
- Code Smells: 67 (12 bloaters, 23 OO abusers)

**Recommendations**:
- Refactor `order-processor.js` (complexity: 18)
- Extract duplicated validation logic
- Address 12 bloater code smells

### Phase 2: Dynamic Testing
- Total Tests: 478 (342 unit, 89 integration, 42 E2E)
- Pass Rate: 98.1%
- Coverage: 91.2% statements, 87.4% branches
- Execution Time: 47.3s

**Recommendations**:
- Fix 7 failing tests
- Stabilize 3 flaky tests
- Optimize 23 slow tests (>1s)

### Phase 3: Integration Validation
- Service Health: 100% (all dependencies operational)
- API Contracts: 100% verified
- Integration Tests: 96.6% pass rate

**Recommendations**:
- Fix concurrent user creation race condition
- Add rate limiting enforcement
- Improve webhook delivery reliability

### Phase 4: Certification
- Certification Score: 87.3/100
- Compliance: All checks passed
- Sign-off: All stakeholders approved

**Recommendations**:
- Address 3 non-blocking known issues
- Schedule quarterly recertification
```

**5. Generate Visualizations**
```bash
# Generate quality trend chart
node scripts/generate-quality-trends.js > quality-trends.svg

# Generate coverage heatmap
npm run coverage:heatmap -- --output coverage-heatmap.svg

# Generate complexity distribution
node scripts/complexity-distribution.js > complexity-chart.svg
```

**6. Export Multi-Format Reports**
```bash
# Markdown (default)
cat comprehensive-quality-report.md

# HTML
npx marked comprehensive-quality-report.md > quality-report.html

# PDF (via Puppeteer)
node scripts/generate-pdf-report.js \
  --input quality-report.html \
  --output quality-report.pdf
```

**7. Store Final Report**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "comprehensive-quality-report.md" \
  --memory-key "swarm/production-validator/final-report" \
  --metadata "{\"certification_score\": ${CERT_SCORE}, \"approved\": true}"
```

### Validation Gates
- ✅ All phase reports generated
- ✅ Executive summary complete
- ✅ Recommendations documented
- ✅ Visualizations included

### Expected Outputs
- `comprehensive-quality-report.md` - Full report
- `quality-report.html` - HTML version
- `quality-report.pdf` - PDF version
- `quality-trends.svg` - Trend visualization

---

## Final Session Cleanup

```bash
# Export complete verification session
npx claude-flow@alpha hooks session-end \
  --session-id "quality-verification-${BUILD_ID}" \
  --export-metrics true \
  --export-path "./quality-verification-summary.json"

# Notify completion
npx claude-flow@alpha hooks notify \
  --message "Quality verification complete: Score ${CERT_SCORE}/100" \
  --level "info" \
  --metadata "{\"approved\": ${APPROVED}, \"build_id\": \"${BUILD_ID}\"}"
```

---

## Memory Patterns

### Storage Keys
```yaml
swarm/code-analyzer/static-metrics:
  maintainability_index: number
  cyclomatic_complexity: number
  code_duplication_pct: number
  code_smells: array

swarm/tester/dynamic-results:
  total_tests: number
  pass_rate: number
  coverage_pct: number
  failing_tests: array

swarm/tester/integration-results:
  service_health: string
  api_contracts_valid: boolean
  integration_pass_rate: number
  data_flow_consistent: boolean

swarm/production-validator/certification:
  certification_score: number
  approved: boolean
  compliance_checks_passed: number
  sign_off_complete: boolean

swarm/production-validator/final-report:
  report_generated: boolean
  formats: array
  artifacts: array
```

---

## Evidence-Based Validation

### Success Criteria
- ✅ Certification score ≥80/100
- ✅ All quality gates pass
- ✅ Compliance checks complete
- ✅ Stakeholder sign-off obtained
- ✅ Comprehensive documentation generated

### Metrics Tracking
```javascript
{
  "verification_duration_minutes": 35,
  "agents_used": 3,
  "quality_gates_evaluated": 28,
  "quality_gates_passed": 28,
  "certification_score": 87.3,
  "approved_for_production": true
}
```

---

## Usage Examples

### Basic Quality Verification
```bash
# Run complete verification
npm run verify:quality

# Generate report
npm run verify:report
```

### CI/CD Integration
```yaml
# .github/workflows/quality-verification.yml
name: Quality Verification
on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Quality Verification
        run: npm run verify:quality
      - name: Check Certification
        run: |
          SCORE=$(jq '.certification_score' quality-verification-summary.json)
          if [ "$SCORE" -lt 80 ]; then exit 1; fi
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.pdf
```

---

## Related Skills

- `when-reviewing-code-comprehensively-use-code-review-assistant`
- `when-ensuring-production-ready-use-production-readiness`
- `when-auditing-code-style-use-style-audit`
