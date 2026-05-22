---
name: when-reviewing-code-comprehensively-use-code-review-assistant
description: Comprehensive PR review with multi-agent swarm specialization for security, performance, style, tests, and documentation
version: 1.0.0
category: testing-quality
agents:
  - code-review-swarm
  - security-manager
  - performance-analyzer
  - tester
topology: hierarchical
coordination: claude-flow
evidence_based: true
validation_gates: true
---

# Comprehensive Code Review Assistant

## Purpose

Orchestrate multi-agent swarm review of pull requests with specialized reviewers for security, performance, style, test coverage, and documentation. Provides detailed feedback with auto-fix suggestions and merge readiness assessment.

## Core Principles

- **Multi-Agent Specialization**: Dedicated agents for each review dimension
- **Parallel Analysis**: Concurrent review across all quality vectors
- **Evidence-Based**: Measurable quality metrics and validation gates
- **Auto-Fix Capability**: Automated corrections where possible
- **Merge Readiness**: Clear approval/rejection criteria

## Phase 1: Security Review

### Objective
Identify and report security vulnerabilities, OWASP violations, and authentication/authorization issues.

### Agent Configuration
```yaml
agent: security-manager
specialization: security-audit
validation: OWASP-Top-10
```

### Execution Steps

**1. Initialize Security Scan**
```bash
# Pre-task setup
npx claude-flow@alpha hooks pre-task \
  --agent-id "security-manager" \
  --description "Security vulnerability scanning" \
  --task-type "security-audit"

# Restore session context
npx claude-flow@alpha hooks session-restore \
  --session-id "code-review-swarm-${PR_ID}" \
  --agent-id "security-manager"
```

**2. OWASP Top 10 Scan**
```bash
# Scan for OWASP vulnerabilities
npx eslint . --format json --config .eslintrc-security.json > security-report.json

# Check for dependency vulnerabilities
npm audit --json > npm-audit.json

# Scan for secrets and credentials
npx gitleaks detect --source . --report-path gitleaks-report.json
```

**3. Authentication/Authorization Review**
```javascript
// Analyze authentication patterns
const authPatterns = {
  jwt_validation: /jwt\.verify\(/g,
  password_hashing: /bcrypt|argon2|scrypt/g,
  sql_injection: /\$\{.*\}/g,
  xss_prevention: /sanitize|escape|DOMPurify/g,
  csrf_protection: /csrf|csurf/g
};

// Validate security controls
const securityChecks = {
  has_jwt_validation: false,
  has_password_hashing: false,
  has_sql_parameterization: false,
  has_xss_prevention: false,
  has_csrf_protection: false
};
```

**4. Store Security Findings**
```bash
# Store results in memory
npx claude-flow@alpha hooks post-edit \
  --file "security-report.json" \
  --memory-key "swarm/security-manager/findings" \
  --metadata "{\"critical\": ${CRITICAL_COUNT}, \"high\": ${HIGH_COUNT}}"
```

**5. Generate Security Report**
```markdown
## Security Review Results

### Critical Issues (Blocking)
- [ ] SQL injection vulnerability in user.controller.js:45
- [ ] Hardcoded API key in config/production.js:12

### High Priority Issues
- [ ] Missing JWT expiration validation
- [ ] Weak password hashing (MD5 detected)

### Recommendations
1. Implement parameterized queries for all database operations
2. Move credentials to environment variables
3. Add JWT expiration checks (max 1 hour)
4. Upgrade to bcrypt with work factor 12+
```

**6. Post-Task Cleanup**
```bash
npx claude-flow@alpha hooks post-task \
  --task-id "security-review-${PR_ID}" \
  --status "complete" \
  --metrics "{\"issues_found\": ${TOTAL_ISSUES}, \"critical\": ${CRITICAL_COUNT}}"
```

### Validation Gates
- ✅ No critical security issues
- ✅ All OWASP Top 10 checks pass
- ✅ No hardcoded secrets detected
- ✅ Authentication properly implemented

### Expected Outputs
- `security-report.json` - Detailed security findings
- `security-score.json` - Security quality metrics (0-100)
- `auto-fix-suggestions.json` - Automated fix recommendations

---

## Phase 2: Performance Review

### Objective
Analyze code efficiency, detect bottlenecks, and recommend performance optimizations.

### Agent Configuration
```yaml
agent: performance-analyzer
specialization: performance-audit
metrics: latency, memory, cpu
```

### Execution Steps

**1. Initialize Performance Analysis**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "performance-analyzer" \
  --description "Performance bottleneck analysis" \
  --task-type "performance-audit"
```

**2. Static Performance Analysis**
```javascript
// Detect anti-patterns
const performanceAntiPatterns = {
  nested_loops: /for.*for.*for/gs,
  blocking_operations: /fs\.readFileSync|execSync/g,
  memory_leaks: /global\.|window\./g,
  inefficient_queries: /SELECT \*/gi,
  n_plus_one: /\.map\(.*await/gs
};

// Analyze complexity
const complexityMetrics = {
  cyclomatic_complexity: [], // McCabe complexity
  cognitive_complexity: [],   // Sonar cognitive
  nesting_depth: [],          // Max nesting level
  function_length: []         // Lines per function
};
```

**3. Runtime Performance Profiling**
```bash
# Run performance benchmarks
npm run test:perf -- --profile

# Analyze bundle size
npx webpack-bundle-analyzer stats.json --mode static -r bundle-analysis.html

# Check memory usage
node --inspect --expose-gc performance-test.js
```

**4. Bottleneck Detection**
```javascript
// Identify slow operations
const bottlenecks = [
  {
    file: "api/users.controller.js",
    function: "getUsersList",
    issue: "N+1 query pattern",
    current_latency: "1250ms",
    optimized_latency: "45ms",
    fix: "Use JOIN or eager loading"
  },
  {
    file: "utils/processor.js",
    function: "processData",
    issue: "Synchronous file operations",
    current_latency: "800ms",
    optimized_latency: "120ms",
    fix: "Use fs.promises.readFile"
  }
];
```

**5. Generate Performance Report**
```markdown
## Performance Review Results

### Critical Bottlenecks (P0)
- **N+1 Query Pattern** (api/users.controller.js:67)
  - Impact: 1250ms → 45ms (27.7x improvement)
  - Fix: Replace `.map(await)` with single JOIN query

### Performance Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| API Response Time | 850ms | <200ms | ⚠️ FAIL |
| Memory Usage | 512MB | <256MB | ⚠️ FAIL |
| Bundle Size | 2.4MB | <1MB | ⚠️ FAIL |
| Lighthouse Score | 62 | >90 | ⚠️ FAIL |

### Optimization Recommendations
1. Implement query result caching (Redis)
2. Use async/await for file operations
3. Code splitting for bundle size reduction
4. Lazy load non-critical components
```

**6. Store Performance Data**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "performance-report.json" \
  --memory-key "swarm/performance-analyzer/metrics" \
  --metadata "{\"bottlenecks\": ${BOTTLENECK_COUNT}, \"avg_latency\": ${AVG_LATENCY}}"
```

### Validation Gates
- ✅ API response time <200ms
- ✅ Memory usage <256MB
- ✅ No O(n²) or worse algorithms
- ✅ Bundle size <1MB

### Expected Outputs
- `performance-report.json` - Performance analysis
- `bottlenecks.json` - Identified slow operations
- `optimization-plan.json` - Recommended fixes

---

## Phase 3: Style Review

### Objective
Verify code conventions, linting rules, and consistent formatting across the codebase.

### Agent Configuration
```yaml
agent: code-review-swarm
specialization: style-audit
standards: ESLint, Prettier, TypeScript
```

### Execution Steps

**1. Initialize Style Check**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-review-swarm" \
  --description "Code style and conventions audit" \
  --task-type "style-audit"
```

**2. Run Linting Tools**
```bash
# ESLint for JavaScript/TypeScript
npx eslint . --ext .js,.jsx,.ts,.tsx --format json > eslint-report.json

# Prettier for formatting
npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,md}" --list-different > prettier-report.txt

# TypeScript compiler for type checks
npx tsc --noEmit --pretty false 2> typescript-errors.txt
```

**3. Analyze Naming Conventions**
```javascript
// Check naming patterns
const namingConventions = {
  classes: /^[A-Z][a-zA-Z0-9]*$/,        // PascalCase
  functions: /^[a-z][a-zA-Z0-9]*$/,      // camelCase
  constants: /^[A-Z][A-Z0-9_]*$/,        // UPPER_SNAKE_CASE
  components: /^[A-Z][a-zA-Z0-9]*$/,     // PascalCase (React)
  files: /^[a-z][a-z0-9-]*\.(js|ts)$/   // kebab-case
};

// Validate naming compliance
const namingViolations = [];
```

**4. Check Code Organization**
```javascript
// Verify file structure
const organizationRules = {
  max_file_length: 500,        // Lines per file
  max_function_length: 50,     // Lines per function
  max_function_params: 4,      // Parameters per function
  max_nesting_depth: 4,        // Nested blocks
  imports_organized: true      // Sorted imports
};
```

**5. Generate Style Report**
```markdown
## Style Review Results

### ESLint Violations
- **69 errors, 23 warnings**
  - 12x `no-unused-vars`
  - 8x `no-console`
  - 15x `prefer-const`
  - 34x `indent` (2 spaces expected)

### Prettier Formatting Issues
- 47 files need formatting
- Inconsistent quote style (mix of single/double)
- Missing trailing commas

### Naming Convention Violations
| File | Line | Issue | Expected |
|------|------|-------|----------|
| user.js | 45 | `UserID` constant | `USER_ID` |
| api-helper.js | 12 | `APIHelper` class | `ApiHelper` |

### Auto-Fix Available
```bash
# Fix all auto-fixable issues
npx eslint . --fix
npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}"
```
```

**6. Store Style Findings**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "style-report.json" \
  --memory-key "swarm/code-review-swarm/style" \
  --metadata "{\"violations\": ${VIOLATION_COUNT}, \"auto_fixable\": ${AUTO_FIX_COUNT}}"
```

### Validation Gates
- ✅ No ESLint errors
- ✅ All files formatted with Prettier
- ✅ Naming conventions followed
- ✅ TypeScript types validated

### Expected Outputs
- `eslint-report.json` - Linting violations
- `prettier-report.txt` - Formatting issues
- `style-fixes.sh` - Auto-fix script

---

## Phase 4: Test Coverage Review

### Objective
Validate unit and integration test coverage, test quality, and edge case handling.

### Agent Configuration
```yaml
agent: tester
specialization: test-coverage-audit
coverage_target: 90%
```

### Execution Steps

**1. Initialize Test Analysis**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "tester" \
  --description "Test coverage and quality validation" \
  --task-type "test-audit"
```

**2. Run Test Coverage Analysis**
```bash
# Run Jest with coverage
npm run test:coverage -- --json --outputFile=coverage-summary.json

# Generate detailed coverage report
npx jest --coverage --coverageReporters=html --coverageReporters=json-summary

# Check for missing test files
find src -name "*.js" ! -path "*/node_modules/*" | while read file; do
  test_file="${file%.js}.test.js"
  if [ ! -f "$test_file" ]; then
    echo "$file" >> missing-tests.txt
  fi
done
```

**3. Analyze Test Quality**
```javascript
// Test quality metrics
const testQualityMetrics = {
  total_tests: 0,
  passing_tests: 0,
  failing_tests: 0,
  skipped_tests: 0,
  test_execution_time: 0,

  assertions_per_test: 0,      // Avg assertions
  edge_cases_covered: false,   // Null, undefined, empty checks
  error_handling_tested: false, // Try-catch scenarios
  async_tested: false,         // Async/await coverage
  mocks_used_properly: false   // Mock verification
};
```

**4. Check Coverage Thresholds**
```javascript
// Coverage requirements
const coverageThresholds = {
  statements: 90,
  branches: 85,
  functions: 90,
  lines: 90
};

// Current coverage
const currentCoverage = {
  statements: 73.5,  // ⚠️ Below threshold
  branches: 68.2,    // ⚠️ Below threshold
  functions: 81.0,   // ⚠️ Below threshold
  lines: 74.8        // ⚠️ Below threshold
};
```

**5. Generate Test Coverage Report**
```markdown
## Test Coverage Review Results

### Coverage Summary
| Category | Current | Target | Status |
|----------|---------|--------|--------|
| Statements | 73.5% | 90% | ⚠️ FAIL (-16.5%) |
| Branches | 68.2% | 85% | ⚠️ FAIL (-16.8%) |
| Functions | 81.0% | 90% | ⚠️ FAIL (-9.0%) |
| Lines | 74.8% | 90% | ⚠️ FAIL (-15.2%) |

### Untested Files (Critical)
- `src/auth/jwt-validator.js` (0% coverage)
- `src/api/payment-processor.js` (0% coverage)
- `src/utils/encryption.js` (15% coverage)

### Missing Test Types
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical user flows
- [ ] Load tests for performance validation
- [ ] Security tests for auth flows

### Test Quality Issues
1. **Insufficient assertions**: 12 tests with 0 assertions
2. **No error handling tests**: Exception paths not covered
3. **Missing edge cases**: Null/undefined checks absent
4. **Async tests not awaited**: 8 tests missing await

### Recommendations
```javascript
// Add missing tests
describe('JWT Validator', () => {
  it('should validate valid JWT tokens', async () => {
    const token = generateValidToken();
    const result = await jwtValidator.validate(token);
    expect(result.valid).toBe(true);
  });

  it('should reject expired tokens', async () => {
    const expiredToken = generateExpiredToken();
    await expect(jwtValidator.validate(expiredToken))
      .rejects.toThrow('Token expired');
  });

  it('should handle malformed tokens', async () => {
    await expect(jwtValidator.validate('invalid'))
      .rejects.toThrow('Malformed token');
  });
});
```
```

**6. Store Test Data**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "coverage-summary.json" \
  --memory-key "swarm/tester/coverage" \
  --metadata "{\"coverage_pct\": ${COVERAGE_PCT}, \"missing_tests\": ${MISSING_COUNT}}"
```

### Validation Gates
- ✅ Statement coverage ≥90%
- ✅ Branch coverage ≥85%
- ✅ Function coverage ≥90%
- ✅ All critical paths tested

### Expected Outputs
- `coverage-summary.json` - Detailed coverage metrics
- `missing-tests.txt` - Untested files list
- `test-quality-report.md` - Test quality analysis

---

## Phase 5: Documentation Review

### Objective
Validate API documentation, inline comments, README completeness, and code maintainability.

### Agent Configuration
```yaml
agent: code-review-swarm
specialization: documentation-audit
standards: JSDoc, OpenAPI, Markdown
```

### Execution Steps

**1. Initialize Documentation Check**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-review-swarm" \
  --description "Documentation completeness audit" \
  --task-type "documentation-audit"
```

**2. Analyze JSDoc/TypeDoc Coverage**
```bash
# Check JSDoc coverage
npx jsdoc-coverage-checker src/**/*.js --threshold 80 > jsdoc-report.json

# Generate TypeDoc for TypeScript
npx typedoc --json typedoc-output.json

# Check for missing function documentation
grep -r "^function\|^const.*=.*=>" src/ | grep -v "\/\*\*" > undocumented-functions.txt
```

**3. Validate API Documentation**
```javascript
// Check OpenAPI/Swagger completeness
const apiDocRequirements = {
  has_openapi_spec: false,
  all_endpoints_documented: false,
  request_schemas_defined: false,
  response_schemas_defined: false,
  error_responses_documented: false,
  authentication_documented: false,
  examples_provided: false
};

// Validate endpoint documentation
const endpointDocs = {
  total_endpoints: 47,
  documented_endpoints: 31,
  missing_documentation: 16,  // ⚠️ 34% undocumented
  incomplete_schemas: 12
};
```

**4. Check README and Setup Docs**
```javascript
// README completeness checklist
const readmeRequirements = {
  project_description: true,
  installation_steps: true,
  usage_examples: true,
  api_reference: false,        // ⚠️ Missing
  environment_variables: false, // ⚠️ Missing
  testing_instructions: true,
  contributing_guide: false,   // ⚠️ Missing
  license_info: true,
  changelog: false             // ⚠️ Missing
};
```

**5. Analyze Inline Comments Quality**
```javascript
// Comment quality metrics
const commentMetrics = {
  total_comments: 342,
  useful_comments: 198,        // Explain "why", not "what"
  redundant_comments: 89,      // Obvious comments
  outdated_comments: 55,       // Don't match code

  comment_to_code_ratio: 0.12, // 12% (target: 10-20%)
  complex_code_commented: 0.67  // 67% of complex functions
};
```

**6. Generate Documentation Report**
```markdown
## Documentation Review Results

### API Documentation
- **OpenAPI Spec**: ⚠️ Missing
- **Endpoint Documentation**: 31/47 (66%)
- **Schema Definitions**: Incomplete

### Undocumented API Endpoints
- `POST /api/v1/users/:id/roles`
- `DELETE /api/v1/sessions/:id`
- `PATCH /api/v1/settings`
- ...12 more endpoints

### JSDoc/TypeDoc Coverage
- **Overall Coverage**: 62% (target: 80%)
- **Public Functions**: 78% documented
- **Private Functions**: 41% documented

### Missing Documentation
1. **Setup Guide**: Environment variable configuration
2. **API Reference**: Complete endpoint documentation
3. **Architecture Docs**: System design overview
4. **Troubleshooting Guide**: Common issues and solutions

### README Improvements Needed
```markdown
## Environment Variables

Required environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `JWT_SECRET` | Secret key for JWT signing | - | Yes |
| `REDIS_URL` | Redis connection string | localhost:6379 | No |
| `LOG_LEVEL` | Logging verbosity | info | No |

## API Reference

See [API.md](./docs/API.md) for complete endpoint documentation.
```

### Inline Comment Issues
- 89 redundant comments (explain obvious code)
- 55 outdated comments (don't match current implementation)

### Recommendations
1. Generate OpenAPI spec from code annotations
2. Add JSDoc to all public functions
3. Document environment variables in README
4. Create architecture diagram
5. Remove redundant/outdated comments
```

**7. Store Documentation Findings**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "documentation-report.json" \
  --memory-key "swarm/code-review-swarm/documentation" \
  --metadata "{\"coverage_pct\": ${DOC_COVERAGE}, \"missing_docs\": ${MISSING_DOCS}}"
```

### Validation Gates
- ✅ JSDoc coverage ≥80%
- ✅ All public APIs documented
- ✅ README complete with setup instructions
- ✅ OpenAPI/Swagger spec exists

### Expected Outputs
- `documentation-report.json` - Documentation audit
- `undocumented-functions.txt` - Missing JSDoc
- `readme-improvements.md` - README enhancement suggestions

---

## Final Integration: Merge Readiness Assessment

### Comprehensive Review Summary

**Aggregate Results from All Phases:**

```javascript
// Merge readiness calculation
const mergeReadiness = {
  security_score: 65,      // Phase 1 (Critical: 2, High: 5)
  performance_score: 58,   // Phase 2 (P0 bottlenecks: 3)
  style_score: 74,         // Phase 3 (Violations: 92)
  test_coverage_score: 73, // Phase 4 (Coverage: 73.5%)
  documentation_score: 62, // Phase 5 (Coverage: 62%)

  overall_score: 66.4,     // Weighted average
  merge_approved: false    // Requires score ≥80
};
```

### Decision Matrix

```markdown
## Merge Readiness Report

### Overall Score: 66.4/100 ⚠️ CHANGES REQUIRED

| Dimension | Score | Status | Blocking Issues |
|-----------|-------|--------|-----------------|
| Security | 65/100 | ⚠️ FAIL | 2 critical, 5 high |
| Performance | 58/100 | ⚠️ FAIL | 3 P0 bottlenecks |
| Style | 74/100 | ⚠️ WARN | 92 violations |
| Test Coverage | 73/100 | ⚠️ FAIL | 16.5% below target |
| Documentation | 62/100 | ⚠️ WARN | 38% undocumented |

### Blocking Issues (Must Fix Before Merge)
1. **[SECURITY]** SQL injection vulnerability (user.controller.js:45)
2. **[SECURITY]** Hardcoded API key (config/production.js:12)
3. **[PERFORMANCE]** N+1 query pattern (api/users.controller.js:67)
4. **[TESTING]** Critical files untested (auth/jwt-validator.js: 0%)

### Recommended Actions
1. Fix all critical security issues
2. Optimize N+1 query patterns
3. Add tests for untested critical paths
4. Run auto-fix for style violations: `npm run lint:fix`

### Estimated Time to Merge-Ready: 4-6 hours
```

### Auto-Fix Script Generation

```bash
#!/bin/bash
# auto-fix-review-issues.sh

echo "Applying automated fixes..."

# Fix style violations
npx eslint . --fix
npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}"

# Fix simple security issues
sed -i 's/API_KEY = ".*"/API_KEY = process.env.API_KEY/g' config/production.js

# Add missing test files
for file in $(cat missing-tests.txt); do
  test_file="${file%.js}.test.js"
  cat > "$test_file" << 'EOF'
describe('${file}', () => {
  it('should be implemented', () => {
    // TODO: Add tests
    expect(true).toBe(true);
  });
});
EOF
done

echo "Automated fixes complete. Manual review required for:"
echo "- SQL injection fixes"
echo "- Performance optimizations"
echo "- Test implementation"
```

### Session Cleanup

```bash
# Export complete review session
npx claude-flow@alpha hooks session-end \
  --session-id "code-review-swarm-${PR_ID}" \
  --export-metrics true \
  --export-path "./code-review-summary.json"

# Notify completion
npx claude-flow@alpha hooks notify \
  --message "Code review complete: Score ${OVERALL_SCORE}/100" \
  --level "info" \
  --metadata "{\"merge_approved\": ${MERGE_APPROVED}}"
```

---

## Memory Patterns

### Storage Keys
```yaml
swarm/security-manager/findings:
  critical_issues: []
  high_priority_issues: []
  owasp_violations: []
  auto_fix_available: boolean

swarm/performance-analyzer/metrics:
  bottlenecks: []
  latency_p95: number
  memory_usage_mb: number
  optimization_recommendations: []

swarm/code-review-swarm/style:
  eslint_errors: number
  prettier_violations: number
  naming_issues: []
  auto_fixable: number

swarm/tester/coverage:
  statements_pct: number
  branches_pct: number
  functions_pct: number
  untested_files: []

swarm/code-review-swarm/documentation:
  jsdoc_coverage_pct: number
  api_docs_complete: boolean
  readme_complete: boolean
  missing_docs: []

swarm/review-summary:
  overall_score: number
  merge_approved: boolean
  blocking_issues: []
  estimated_fix_time_hours: number
```

---

## Evidence-Based Validation

### Success Criteria
- ✅ All 5 specialized reviews complete
- ✅ Overall score ≥80/100
- ✅ Zero critical security issues
- ✅ Zero P0 performance bottlenecks
- ✅ Test coverage ≥90%
- ✅ No blocking style violations

### Metrics Tracking
```javascript
{
  "review_duration_minutes": 12,
  "agents_used": 4,
  "total_issues_found": 187,
  "auto_fixable_issues": 92,
  "blocking_issues": 4,
  "merge_approved": false,
  "estimated_fix_time_hours": 5
}
```

### Quality Gates
1. **Security Gate**: No critical/high vulnerabilities
2. **Performance Gate**: All APIs <200ms, no O(n²) patterns
3. **Style Gate**: Zero ESLint errors, Prettier formatted
4. **Testing Gate**: Coverage ≥90%, all critical paths tested
5. **Documentation Gate**: JSDoc ≥80%, API docs complete

---

## Usage Examples

### Basic PR Review
```bash
# Initialize review swarm
npx claude-flow@alpha swarm init \
  --topology hierarchical \
  --agents "security-manager,performance-analyzer,code-review-swarm,tester"

# Run comprehensive review
npm run review:pr -- --pr-number 123
```

### CI/CD Integration
```yaml
# .github/workflows/code-review.yml
name: Automated Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Review Swarm
        run: |
          npx claude-flow@alpha swarm init --topology hierarchical
          npm run review:comprehensive
      - name: Post Review Results
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body-file ./code-review-summary.md
```

### Custom Review Configuration
```javascript
// code-review.config.js
module.exports = {
  security: {
    owasp_check: true,
    dependency_audit: true,
    secret_scan: true
  },
  performance: {
    latency_threshold_ms: 200,
    memory_threshold_mb: 256,
    bundle_size_mb: 1
  },
  testing: {
    coverage_threshold: 90,
    require_integration_tests: true
  },
  merge_gate: {
    minimum_score: 80,
    allow_warnings: false
  }
};
```

---

## Troubleshooting

### Issue: Review Times Out
```bash
# Increase timeout for large PRs
export REVIEW_TIMEOUT=1800  # 30 minutes

# Review specific files only
npm run review:pr -- --files "src/critical/**"
```

### Issue: False Positive Security Warnings
```javascript
// Add to .eslintrc-security.json
{
  "rules": {
    "security/detect-object-injection": "off",  // If intentional
    "security/detect-non-literal-fs-filename": "warn"
  }
}
```

### Issue: Coverage Calculation Incorrect
```bash
# Clear coverage cache
rm -rf coverage/ .nyc_output/

# Regenerate coverage
npm run test:coverage -- --clearCache
```

---

## Best Practices

1. **Run Reviews Early**: Integrate in PR workflow, not at merge time
2. **Auto-Fix First**: Apply automated fixes before manual review
3. **Prioritize Blocking Issues**: Focus on critical/high security and P0 performance
4. **Incremental Reviews**: Review commits incrementally, not entire PR at once
5. **Custom Thresholds**: Adjust scoring based on project criticality
6. **Review Automation**: Integrate with CI/CD for every PR
7. **Track Metrics**: Monitor review scores over time for quality trends

---

## Integration with SPARC

- **Specification Phase**: Review requirements documentation
- **Refinement Phase**: Code review during TDD cycles
- **Completion Phase**: Final merge readiness check

---

## Related Skills

- `when-ensuring-production-ready-use-production-readiness`
- `when-verifying-quality-use-verification-quality`
- `when-auditing-code-style-use-style-audit`
- `when-debugging-complex-issues-use-smart-bug-fix`
