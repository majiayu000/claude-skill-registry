---
name: validator-role-skill
version: 1.0.0
category: quality-assurance
complexity: moderate
status: active
created: 2025-12-12
author: claude-command-and-control

description: |
  Professional software QA and code review skill for ensuring code quality,
  comprehensive test coverage, standards compliance, and security through
  rigorous testing and validation workflows.

triggers:
  - "validate code"
  - "review pull request"
  - "create tests"
  - "run quality checks"
  - "security review"

dependencies: []

tags:
  - testing
  - code-review
  - quality-assurance
  - security
  - tdd
---

# Validator Role Skill

## Description

Ensure code quality, comprehensive test coverage, standards compliance, and security through rigorous testing and review workflows. This skill implements professional QA practices including test creation, test execution, code review, coverage analysis, security assessment, and performance validation.

## When to Use This Skill

- Validating pull requests before merge
- Creating comprehensive test suites (TDD support)
- Performing security assessments
- Analyzing test coverage and quality
- Executing regression testing after changes
- Reviewing code for quality and standards compliance
- Performance validation and benchmarking

## When NOT to Use This Skill

- For production code implementation (use builder-role-skill)
- For infrastructure deployment (use devops-role-skill)
- For system design decisions (use architect-role-skill)
- For documentation generation (use scribe-role-skill)

## Prerequisites

- Test framework configured (Jest, pytest, JUnit, etc.)
- Linting tools installed (ESLint, flake8, Clippy, etc.)
- Security scanning tools available (npm audit, safety, snyk)
- Coverage tools configured
- Git repository with pull request workflow

---

## Workflow

### Phase 1: Pre-Implementation Test Creation (TDD Support)

Support test-driven development by creating tests before implementation.

**Step 1.1: Review Feature Specification**

```
Load context files:
- DEVELOPMENT_PLAN.md (overall plan)
- ARCHITECTURE.md (design specs)
- IMPLEMENTATION_PLAN.md (implementation details)
```

**Step 1.2: Create Test Specification**

Generate `TEST_PLAN.md` with comprehensive test strategy:

```markdown
# Test Plan: [Feature Name]

## Test Strategy
- Unit Test Coverage Target: 95%
- Integration Test Coverage: All public APIs
- E2E Test Coverage: Critical user paths
- Performance Benchmarks: [Specific targets]

## Test Categories

### Unit Tests
**Component**: [Name]
- Test 1: [Scenario] - Expected: [Result]
- Test 2: [Scenario] - Expected: [Result]
- Test 3: [Edge case] - Expected: [Error handling]

### Integration Tests
**Integration Point**: [Name]
- Test 1: [Interaction scenario]
- Test 2: [Data flow validation]
- Test 3: [Error propagation]

### End-to-End Tests
**User Journey**: [Name]
- Test 1: [Happy path]
- Test 2: [Alternate path]
- Test 3: [Error scenarios]

## Test Data Requirements
[Fixtures, mocks, test databases needed]

## Performance Criteria
- Response time: < [X]ms
- Throughput: > [Y] requests/sec
- Memory usage: < [Z]MB

## Security Test Cases
- [ ] Input validation
- [ ] SQL injection protection
- [ ] XSS prevention
- [ ] Authentication bypass attempts
- [ ] Authorization boundary tests
```

**Step 1.3: Write Failing Tests First**

```javascript
// Example: Jest/JavaScript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        password: 'SecurePass123!'
      };

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toHaveProperty('id');
      expect(result.email).toBe(userData.email);
      expect(result.password).not.toBe(userData.password); // hashed
    });

    it('should reject invalid email format', async () => {
      // Arrange
      const userData = {
        email: 'invalid-email',
        password: 'SecurePass123!'
      };

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow('Invalid email format');
    });

    it('should reject weak password', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        password: '123'
      };

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow('Password does not meet security requirements');
    });
  });
});
```

**Step 1.4: Handoff to Builder**

```markdown
---
TO: Builder (or use builder-role-skill)
FEATURE: [Feature Name]
TEST_SPEC: TEST_PLAN.md
TESTS_WRITTEN: [List of test files]
STATUS: Failing (as expected - TDD)

IMPLEMENTATION_REQUIRED:
Builder should implement code to make these tests pass.

VALIDATION_CRITERIA:
- All unit tests passing
- Coverage >= 95%
- No security warnings
---
```

---

### Phase 2: Post-Implementation Validation

Validate code after implementation is complete.

**Step 2.1: Receive Implementation Handoff**

```
Load context files:
- IMPLEMENTATION_PLAN.md (what was built)
- PR description (change summary)
- Modified files list (scope of changes)
```

**Step 2.2: Execute Comprehensive Test Suite**

```bash
# Run all tests
npm test || pytest || mvn test || cargo test

# Generate coverage report
npm run coverage || pytest --cov --cov-report=html || mvn jacoco:report

# Run linter
npm run lint || flake8 || mvn checkstyle:check || cargo clippy

# Run security scan
npm audit || safety check || mvn dependency-check:check || cargo audit
```

**Step 2.3: Analyze Results**

Create `VALIDATION_REPORT.md`:

```markdown
# Validation Report: [Feature/PR Name]

## Test Execution Results
- Total Tests: [N]
- Passing: [N]
- Failing: [N]
- Skipped: [N]
- Duration: [X]s

## Coverage Analysis
- Overall Coverage: [X]%
- Line Coverage: [X]%
- Branch Coverage: [X]%
- Function Coverage: [X]%

**Coverage by Component**:
| Component | Coverage | Status |
|-----------|----------|--------|
| [Name] | [X]% | ✅ / ⚠️ / ❌ |

**Uncovered Areas**:
- File: [name], Lines: [X-Y] - Reason: [Why not covered]

## Code Quality
- Linting Issues: [N]
- Code Smells: [N]
- Complexity Warnings: [N]
- Duplication: [X]%

## Security Assessment
- Vulnerabilities Found: [N]
- Severity: [Critical/High/Medium/Low]
- Affected Packages: [List]

## Performance Validation
- Response Time: [X]ms (Target: <[Y]ms) ✅ / ❌
- Memory Usage: [X]MB (Target: <[Y]MB) ✅ / ❌
- Throughput: [X] req/s (Target: >[Y]) ✅ / ❌

## Overall Assessment
**Status**: ✅ APPROVED / ⚠️ APPROVED WITH CONCERNS / ❌ REJECTED

**Justification**:
[Detailed reasoning for decision]
```

**Step 2.4: Code Review**

Add inline review comments to PR:

```markdown
## Code Review Comments

### Critical Issues (Must Fix)
1. **File: [name], Line: [X]**
   - Issue: [Description]
   - Impact: [Security/Functionality/Performance]
   - Recommendation: [How to fix]

### Suggestions (Should Consider)
1. **File: [name], Line: [X]**
   - Observation: [What could be improved]
   - Recommendation: [Alternative approach]
   - Benefit: [Why it's better]

### Positive Highlights
1. **File: [name]**
   - Excellent: [What was done well]

### Questions
1. **File: [name], Line: [X]**
   - Question: [What's unclear]
   - Context: [Why asking]
```

**Step 2.5: Decision and Handoff**

**If APPROVED**:
```bash
# Add approval comment to PR
gh pr review [PR-number] --approve --body "$(cat VALIDATION_REPORT.md)"

# Update status
echo "✅ Validation complete - APPROVED" >> MULTI_AGENT_PLAN.md
```

**If REJECTED**:
```bash
# Request changes
gh pr review [PR-number] --request-changes --body "$(cat VALIDATION_REPORT.md)"
```

Handoff back to Builder:
```markdown
---
TO: Builder (or use builder-role-skill)
PR: #[number]
STATUS: Changes Requested
VALIDATION_REPORT: VALIDATION_REPORT.md
PRIORITY_FIXES: [List critical issues]
REVALIDATION_REQUIRED: After fixes applied
---
```

---

### Phase 3: Regression Testing

Validate that changes don't break existing functionality.

**Step 3.1: Identify Affected Areas**

```bash
# Find changed files
git diff --name-only main..HEAD

# Find tests related to changed files
grep -r "import.*[changed-file]" test/
```

**Step 3.2: Execute Regression Suite**

```bash
# Run full test suite
npm test

# Run affected component tests specifically
npm test -- --testPathPattern=[component]

# Compare with baseline performance
npm run benchmark
```

**Step 3.3: Document Regression Results**

```markdown
# Regression Test Report: [Date]

## Changes Analyzed
- [File 1]: [Type of change]
- [File 2]: [Type of change]

## Tests Executed
- Total regression tests: [N]
- New failures: [N]
- Fixed issues: [N]

## Regression Detected
**None** / **Issues Found**:

1. **Test**: [Name]
   - Previous: PASS
   - Current: FAIL
   - Root Cause: [Analysis]
   - Action: [Revert / Fix / Accept]

## Recommendation
✅ Safe to proceed / ❌ Revert changes / ⚠️ Proceed with caution
```

---

### Phase 4: Security-Focused Validation

Perform comprehensive security assessment.

**Step 4.1: Security Checklist Review**

```markdown
# Security Validation Checklist: [Feature]

## Input Validation
- [ ] All user inputs validated
- [ ] Type checking implemented
- [ ] Length/size limits enforced
- [ ] Special characters sanitized
- [ ] SQL injection protected
- [ ] XSS prevention in place

## Authentication & Authorization
- [ ] Authentication required on protected routes
- [ ] Authorization verified for each action
- [ ] Session management secure
- [ ] Token expiration handled
- [ ] Password storage uses strong hashing

## Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS for data in transit
- [ ] No secrets in code or logs
- [ ] PII handling compliant
- [ ] Data access properly logged

## API Security
- [ ] Rate limiting implemented
- [ ] CORS configured correctly
- [ ] API keys secured
- [ ] Error messages don't leak info
- [ ] No verbose errors in production

## Dependencies
- [ ] No known vulnerable packages
- [ ] Dependencies up to date
- [ ] License compliance verified
```

**Step 4.2: Penetration Testing**

```bash
# Run security scanner
npm audit --audit-level=moderate
safety check
snyk test

# SQL injection test cases
npm test -- --testNamePattern="SQL injection"

# XSS test cases
npm test -- --testNamePattern="XSS"
```

**Step 4.3: Security Report**

```markdown
# Security Assessment: [Feature]

## Vulnerabilities Found: [N]

### Critical
- None / [List with CVE numbers]

### High
- None / [List with CVE numbers]

### Medium
- None / [List with CVE numbers]

### Low
- None / [List with CVE numbers]

## Remediation Plan
| Vulnerability | Severity | Fix | Timeline |
|---------------|----------|-----|----------|
| [Name] | [Level] | [Action] | [Date] |

## Security Test Coverage
- Input validation tests: [N] scenarios
- Authentication tests: [N] scenarios
- Authorization tests: [N] scenarios
- Encryption validation: [N] scenarios

## Sign-off
**Security Approved**: ✅ YES / ❌ NO / ⚠️ CONDITIONAL

**Conditions**:
[Any requirements for approval]
```

---

## Test Quality Standards

### Every Test Must Have

- **Descriptive name**: Clearly states what is being tested
- **Arrange-Act-Assert structure**: Organized setup, execution, verification
- **Single responsibility**: Tests one thing
- **Deterministic**: Same input always produces same output
- **Independent**: Can run in any order
- **Fast**: Executes quickly

### Test Coverage Requirements

- **Critical Paths**: 100% coverage
- **Business Logic**: 95% coverage minimum
- **Utility Functions**: 90% coverage minimum
- **Integration Points**: All scenarios tested
- **Error Handling**: All error paths tested

### Test Documentation

```javascript
/**
 * Test Suite: UserAuthentication
 * Purpose: Validates user authentication workflows including login,
 *          logout, token refresh, and session management.
 * Dependencies: Database test fixtures, mock email service
 * Cleanup: Resets database after each test
 */
describe('UserAuthentication', () => {
  // Tests...
});
```

---

## Code Review Standards

### Review Focus Areas

**1. Correctness**
- Does the code do what it's supposed to?
- Are edge cases handled?
- Is error handling appropriate?

**2. Security**
- Any injection vulnerabilities?
- Proper authentication/authorization?
- Sensitive data protected?

**3. Performance**
- Any obvious bottlenecks?
- Appropriate data structures?
- Unnecessary loops or queries?

**4. Maintainability**
- Is code readable and clear?
- Appropriate comments and documentation?
- Follows project conventions?

**5. Testability**
- Can this code be easily tested?
- Are dependencies injectable?
- Is complexity manageable?

### Review Comment Guidelines

- Be specific and actionable
- Provide reasoning and context
- Suggest concrete improvements
- Highlight positives as well as issues
- Ask questions when unclear
- Use appropriate severity levels

---

## Quality Gates

### Cannot Approve PR Unless

- [ ] All tests passing
- [ ] Coverage >= threshold (typically 80-95%)
- [ ] Zero critical security vulnerabilities
- [ ] Zero high-priority linter errors
- [ ] Performance benchmarks met
- [ ] No regression in existing functionality
- [ ] Documentation updated
- [ ] Breaking changes clearly documented

---

## Collaboration Patterns

### With Builder (or builder-role-skill)

```markdown
Feedback Loop:
1. Validator identifies issues
2. Builder fixes issues
3. Validator re-validates
4. Repeat until quality gates met

Communication:
- Use PR comments for code-specific feedback
- Use validation report for overall assessment
- Be specific about what needs to change
```

### With Architect (or architect-role-skill)

- Escalate architectural concerns
- Report patterns of technical debt
- Suggest refactoring opportunities
- Validate architectural constraints enforced

### With DevOps (or devops-role-skill)

- Share performance test results
- Report environment-specific issues
- Validate deployment readiness
- Coordinate load testing

---

## Examples

### Example 1: TDD Test Creation

**Task**: Create tests for user registration endpoint

```markdown
## Test Plan

### Unit Tests (UserService)
1. Test valid user registration
2. Test duplicate email rejection
3. Test weak password rejection
4. Test email format validation
5. Test password hashing

### Integration Tests (API)
1. Test POST /register endpoint success
2. Test validation error responses
3. Test database transaction rollback
4. Test email notification trigger

### Security Tests
1. Test SQL injection attempts
2. Test XSS in username field
3. Test password strength requirements
4. Test rate limiting on registration

Result: 13 failing tests created, ready for builder implementation
```

### Example 2: PR Validation

**Task**: Validate authentication feature PR

```markdown
## Validation Results

### Test Execution
- Total tests: 87
- Passing: 87
- Coverage: 94%

### Code Quality
- Linting: 0 errors
- Complexity: Acceptable
- Duplication: 2% (within limits)

### Security
- Vulnerabilities: 0 critical
- Password hashing: ✅ bcrypt with salt
- Token management: ✅ JWT with expiration

### Performance
- Login response: 45ms (target: <100ms) ✅
- Token validation: 2ms ✅

**Decision**: ✅ APPROVED - Ready to merge
```

### Example 3: Regression Detection

**Task**: Validate refactoring PR for regressions

```markdown
## Regression Analysis

### Tests Executed
- Full suite: 234 tests
- Previous failures: 0
- New failures: 2

### Regression Found
1. **Test**: User profile update
   - Previous: PASS
   - Current: FAIL
   - Root Cause: Missing field in refactored model
   - Action: Request fix

**Decision**: ❌ REJECTED - Regression detected, changes requested
```

---

## Resources

### Templates

- `resources/TEST_PLAN_template.md` - Test plan template
- `resources/VALIDATION_REPORT_template.md` - Validation report template
- `resources/security_checklist.md` - Security review checklist

### Scripts

- `scripts/run_tests.sh` - Comprehensive test execution
- `scripts/coverage_report.sh` - Coverage analysis
- `scripts/security_scan.sh` - Security vulnerability scanning

---

## References

- [Agent Skills vs. Multi-Agent](../../docs/best-practices/09-Agent-Skills-vs-Multi-Agent.md)
- [Testing Anti-Patterns Skill](../testing-anti-patterns/) (if available)
- [Test-Driven Development Skill](../test-driven-development/) (if available)

---

**Version**: 1.0.0
**Last Updated**: December 12, 2025
**Status**: ✅ Active
**Maintained By**: Claude Command and Control Project
