---
name: Quality Assurance
description: Comprehensive quality assurance combining testing strategy, code quality enforcement, and validation gates. Consolidated from testing-strategist, code-quality-enforcer, and validation-gate-checker.
version: 1.0.0
category: quality
triggers:
  - 'quality-assurance'
  - 'quality assurance'
  - 'qa strategy'
  - 'testing strategy'
  - 'code quality'
  - 'validation gates'
dependencies:
  required_mcps: []
  required_tools: []
  required_integrations: []
---

# Quality Assurance

## Overview

Quality Assurance is a consolidated skill that combines three critical quality dimensions: comprehensive testing strategy, code quality enforcement, and phase-gate validation. It ensures your code is tested, maintainable, and ready for production at every stage.

**Consolidated from:**

- **testing-strategist** - Test pyramid and comprehensive testing
- **code-quality-enforcer** - Code standards and best practices
- **validation-gate-checker** - Phase transition validation

## When to Use This Skill

Use Quality Assurance when:

- Setting up testing infrastructure for a project
- Conducting code reviews
- Validating readiness to move between project phases
- Establishing quality standards for a team
- Debugging quality issues in production
- Improving code maintainability
- Ensuring production readiness

## Key Capabilities

### Testing Strategy (from testing-strategist)

- Design test pyramid with optimal coverage
- Define unit, integration, and E2E test strategies
- Set coverage targets and quality metrics
- Choose testing frameworks and tools
- Plan test automation and CI/CD integration

### Code Quality (from code-quality-enforcer)

- Enforce coding standards and best practices
- Review code for readability and maintainability
- Identify security vulnerabilities and anti-patterns
- Ensure type safety and error handling
- Refactor code to improve quality scores

### Validation Gates (from validation-gate-checker)

- Define phase transition criteria
- Validate readiness for next phase
- Ensure deliverables are complete
- Check compliance with standards
- Prevent premature phase transitions

## Workflow

### Part 1: Testing Strategy

#### The Test Pyramid

**Structure:**

```
        /\
       /E2E\      10% - End-to-End (Critical user flows)
      /------\
     /Integr-\   20% - Integration (Components, APIs, DB)
    /----------\
   /   Unit     \ 70% - Unit (Functions, classes, logic)
  /--------------\
```

**Rationale:**

- **Unit tests** are fast, isolated, cheap to maintain
- **Integration tests** catch component interaction issues
- **E2E tests** validate critical user workflows, but are slow and brittle

---

#### Unit Tests (70% of tests)

**Coverage Targets:**

- Critical code (auth, payments, security): 100%
- Business logic: >90%
- Overall codebase: >85%

**What to Test:**

- Pure functions and business logic
- Edge cases and error conditions
- Input validation
- State management
- Utility functions

**Best Practices:**

- One test file per source file
- Fast execution (<1ms per test)
- No external dependencies (mock/stub)
- Descriptive test names
- AAA pattern (Arrange, Act, Assert)

**Example:**

```javascript
// Good: Fast, isolated, clear
describe('calculateDiscount', () => {
  it('applies 10% discount for orders over $100', () => {
    const result = calculateDiscount(150)
    expect(result).toBe(15)
  })

  it('returns 0 for orders under $100', () => {
    const result = calculateDiscount(50)
    expect(result).toBe(0)
  })

  it('throws error for negative amounts', () => {
    expect(() => calculateDiscount(-10)).toThrow()
  })
})
```

---

#### Integration Tests (20% of tests)

**What to Test:**

- API endpoints with real database
- Multiple components working together
- Third-party service integrations (with mocks)
- Database queries and transactions
- File system operations

**Best Practices:**

- Test database setup/teardown
- Use test database or transactions
- Mock external services
- Test happy path + key error scenarios
- <5 seconds per test

**Example:**

```javascript
// Good: Real database, tests integration
describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.users.deleteMany({})
  })

  it('creates user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })

    expect(response.status).toBe(201)
    expect(response.body.email).toBe('test@example.com')

    const user = await db.users.findOne({ email: 'test@example.com' })
    expect(user).toBeDefined()
  })

  it('returns 400 for duplicate email', async () => {
    await db.users.create({ email: 'test@example.com' })

    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })

    expect(response.status).toBe(400)
  })
})
```

---

#### E2E Tests (10% of tests)

**What to Test:**

- Critical user workflows (signup, checkout, etc.)
- Multi-page user journeys
- UI interactions with backend
- Cross-browser compatibility (if needed)

**Best Practices:**

- Only test critical paths
- Use page object pattern
- Run in CI/CD before deployment
- Accept slower execution (30s-2min per test)
- Use headless browsers in CI

**Example:**

```javascript
// Good: Tests complete user flow
describe('User Signup Flow', () => {
  it('allows new user to signup and access dashboard', async () => {
    await page.goto('/signup')

    await page.fill('input[name="email"]', 'newuser@example.com')
    await page.fill('input[name="password"]', 'SecurePass123!')
    await page.click('button[type="submit"]')

    await page.waitForURL('/dashboard')
    expect(await page.textContent('h1')).toContain('Welcome')
  })
})
```

---

#### Testing Tools Recommendations

**JavaScript/TypeScript:**

- Unit: Jest or Vitest
- Integration: Supertest (API) + Jest
- E2E: Playwright or Cypress

**Python:**

- Unit: pytest
- Integration: pytest with fixtures
- E2E: Selenium or Playwright

**General:**

- Coverage: Istanbul (JS), Coverage.py (Python)
- CI/CD: GitHub Actions, CircleCI, GitLab CI
- Mocking: Jest (JS), unittest.mock (Python)

---

### Part 2: Code Quality Enforcement

#### Code Quality Principles

**1. Readability**

- Descriptive variable and function names
- Single Responsibility Principle
- Clear, consistent formatting
- Comments for "why", not "what"

**2. Maintainability**

- DRY (Don't Repeat Yourself)
- SOLID principles
- Type safety (TypeScript, type hints)
- Error handling everywhere

**3. Testing**

- Unit tests for all functions
- Edge cases covered
- Test names describe behavior

**4. Security**

- No hardcoded secrets
- Input validation
- SQL injection prevention
- XSS protection

---

#### Code Quality Checklist

**Before Code Review:**

- [ ] No hardcoded secrets or API keys
- [ ] Functions <50 lines (split if longer)
- [ ] Error handling present (try/catch, null checks)
- [ ] All tests passing
- [ ] Type safety (TypeScript strict mode, Python type hints)
- [ ] No console.log or debugging code
- [ ] Descriptive variable names (no x, tmp, data)
- [ ] Comments explain "why", not "what"
- [ ] DRY - no copy-paste code
- [ ] Security best practices (input validation, sanitization)

---

#### Code Review Guidelines

**What to Look For:**

**Critical Issues (Must Fix):**

- Security vulnerabilities (SQL injection, XSS, secrets)
- Breaking changes without migration
- Missing error handling
- Incorrect logic or algorithm
- Performance bottlenecks

**Important Issues (Should Fix):**

- Code duplication (DRY violations)
- Poor naming or structure
- Missing tests for new code
- Type safety violations
- Inconsistent formatting

**Minor Issues (Nice to Fix):**

- Style inconsistencies
- Over-commenting
- Optimization opportunities
- Documentation improvements

---

#### Code Quality Score

**Scoring System (0-100):**

**Security (30 points):**

- No secrets in code (10 pts)
- Input validation (10 pts)
- Error handling (10 pts)

**Readability (25 points):**

- Descriptive names (10 pts)
- Clear structure (10 pts)
- Appropriate comments (5 pts)

**Testing (25 points):**

- Unit test coverage >85% (15 pts)
- Tests for edge cases (10 pts)

**Maintainability (20 points):**

- DRY compliance (10 pts)
- Function size <50 lines (5 pts)
- Type safety (5 pts)

**Grading:**

- 90-100: Excellent
- 80-89: Good
- 70-79: Acceptable
- <70: Needs improvement

---

### Part 3: Validation Gates

Validation gates ensure each phase is complete before moving to the next.

#### Phase 1 → Phase 2 (Discovery → Design)

**Gate Criteria:**

- [ ] PRP document complete and reviewed
- [ ] Problem statement validated with users
- [ ] Success criteria defined and measurable
- [ ] User stories documented (Jobs-to-be-Done)
- [ ] Stakeholder alignment on scope
- [ ] Open questions documented with owners

**Deliverables:**

- Product Requirements Prompt (PRP)
- User research summary
- Success metrics dashboard

**Review Questions:**

- Do we understand the user problem?
- Can we measure success?
- Is scope clear and agreed upon?

---

#### Phase 2 → Phase 3 (Design → Development)

**Gate Criteria:**

- [ ] Architecture documented (system diagram)
- [ ] Data model designed (ERD or schema)
- [ ] API contracts defined (if applicable)
- [ ] Security threats identified (threat model)
- [ ] Mitigations planned for critical threats
- [ ] Technology stack approved
- [ ] Infrastructure plan documented

**Deliverables:**

- Architecture document
- Data model / ERD
- API specification (OpenAPI/Swagger)
- Threat model with mitigations
- Infrastructure diagram

**Review Questions:**

- Is architecture sound and scalable?
- Are security threats mitigated?
- Do we have required infrastructure access?

---

#### Phase 3 → Phase 4 (Development → Testing)

**Gate Criteria:**

- [ ] All P0 features complete
- [ ] Unit test coverage >80%
- [ ] Code review completed
- [ ] Static analysis (SAST) passed
- [ ] No critical or high severity issues
- [ ] Error handling implemented
- [ ] Logging and monitoring in place

**Deliverables:**

- Working software (all P0 features)
- Test coverage report
- Code review sign-off
- SAST scan results

**Review Questions:**

- Are all MVP features complete?
- Is code quality acceptable?
- Are critical bugs resolved?

---

#### Phase 4 → Phase 5 (Testing → Deployment)

**Gate Criteria:**

- [ ] All tests passing (unit, integration, E2E)
- [ ] Test coverage >90%
- [ ] User acceptance testing (UAT) completed
- [ ] Security testing passed (DAST, penetration test)
- [ ] Performance testing passed (load, stress)
- [ ] Documentation complete (user + dev docs)
- [ ] Rollback plan documented
- [ ] Deployment runbook ready

**Deliverables:**

- Test results (all green)
- UAT sign-off
- Security test report
- Performance test results
- Deployment runbook

**Review Questions:**

- Are we confident in quality?
- Can we roll back if needed?
- Is production infrastructure ready?

---

## Examples

### Example 1: API Testing Strategy

**Project:** REST API for user management

**Test Plan:**

**Unit Tests (70%):**

- Business logic (validation, permissions)
- Data transformations
- Utility functions
- Error handling logic

**Integration Tests (20%):**

- POST /users (creates user in DB)
- GET /users/:id (retrieves from DB)
- PUT /users/:id (updates in DB)
- DELETE /users/:id (removes from DB)
- Authentication middleware
- Error responses (400, 401, 404, 500)

**E2E Tests (10%):**

- Full signup flow (create user → verify email → login)
- Password reset flow
- Profile update flow

**Tools:**

- Jest (unit)
- Supertest (integration)
- Playwright (E2E)

**Coverage Target:** 90% overall

---

### Example 2: Code Quality Review

**Before (Poor Quality - Score: 55/100):**

```javascript
// Bad: Hardcoded secret, no error handling, poor naming
function getData(x) {
  const result = fetch('https://api.example.com/data', {
    headers: { Authorization: 'Bearer sk_live_abc123' }
  })
  return result.json()
}
```

**Issues:**

- Security: Hardcoded API key (-10 pts)
- Error handling: None (-10 pts)
- Naming: Poor variable names (-10 pts)
- Testing: No tests (-15 pts)

**After (Good Quality - Score: 95/100):**

```javascript
// Good: Secure, robust, clear
async function fetchUserData(userId: string): Promise<UserData> {
  try {
    const apiKey = process.env.API_KEY;
    if (!apiKey) {
      throw new Error('API_KEY environment variable not set');
    }

    const response = await fetch(`https://api.example.com/users/${userId}`, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    logger.error('Failed to fetch user data', { userId, error });
    throw new Error(`Failed to fetch user ${userId}`);
  }
}

// Tests
describe('fetchUserData', () => {
  it('fetches user successfully', async () => {
    // Test implementation
  });

  it('throws error if API_KEY not set', async () => {
    // Test implementation
  });
});
```

---

### Example 3: Phase Gate Validation

**Project:** Customer Support Chatbot (Phase 3 → Phase 4)

**Validation Check:**

**Requirements:**

- ✅ All P0 features complete (chat UI, AI responses, escalation)
- ✅ Unit test coverage: 87%
- ✅ Code review: Approved (2 reviewers)
- ❌ SAST scan: 3 medium severity issues (FAIL)
- ✅ Error handling: Implemented
- ✅ Logging: Datadog integration complete

**Decision:** GATE FAILED - Must fix SAST issues before proceeding

**Action Items:**

1. Fix 3 medium severity issues (input validation)
2. Re-run SAST scan
3. Re-review gate criteria

**Estimated Time to Pass:** 2 days

---

## Best Practices

### Testing

1. **Write tests first (TDD)** - Clarifies requirements
2. **Keep tests independent** - No shared state
3. **Test behavior, not implementation** - Refactor-safe tests
4. **Use descriptive test names** - Tests are documentation
5. **Fail fast** - Run fast tests first

### Code Quality

1. **Automate quality checks** - ESLint, Prettier, type checking
2. **Review your own code first** - Catch obvious issues
3. **Small, focused PRs** - Easier to review thoroughly
4. **Fix root causes** - Don't just patch symptoms
5. **Refactor continuously** - Don't accumulate tech debt

### Validation Gates

1. **Document criteria upfront** - No surprises
2. **Be strict on critical gates** - Security, production readiness
3. **Flexible on nice-to-haves** - Don't block progress
4. **Track gate passage** - Identify bottlenecks
5. **Automate checks** - CI/CD enforcement

---

## Common Pitfalls

### 1. Testing the Wrong Things

**Antipattern:** Test implementation details (private methods)
**Better:** Test public API and behavior

### 2. Insufficient Coverage of Edge Cases

**Antipattern:** Only test happy path
**Better:** Test nulls, empty arrays, errors, boundaries

### 3. Skipping Phase Gates

**Antipattern:** "We'll fix it after shipping"
**Result:** Production bugs, security issues

**Better:** Enforce gates, delay if needed

### 4. Over-Engineering Quality

**Antipattern:** 100% coverage on everything, perfection paralysis
**Better:** Pragmatic quality aligned with risk

### 5. Manual Quality Checks

**Antipattern:** Remember to run linter before commit
**Better:** Automate in pre-commit hooks + CI/CD

---

## Related Skills

- **testing-strategist** - Original testing skill (now consolidated)
- **security-architect** - Security testing and threat validation
- **deployment-advisor** - Production readiness validation
- **performance-optimizer** - Performance testing and optimization
- **framework-orchestrator** - Uses validation gates for phase transitions

---

## Deliverables

When using Quality Assurance, produce:

1. **Test Strategy Document**
   - Test pyramid breakdown
   - Coverage targets
   - Tools and frameworks
   - CI/CD integration plan

2. **Code Quality Standards**
   - Style guide
   - Linting rules
   - Review checklist
   - Quality score rubric

3. **Phase Gate Criteria**
   - Entry/exit criteria for each phase
   - Required deliverables
   - Review process
   - Sign-off authority

4. **Quality Dashboard**
   - Test coverage metrics
   - Code quality scores
   - Gate passage tracking
   - Trend analysis

---

## Success Metrics

Quality Assurance is working when:

- Test coverage consistently >85%
- Production bugs <1% of releases
- Code reviews catch issues before merge
- Phase gates prevent premature transitions
- Quality improves over time (not degrades)
- Team follows standards without enforcement
- CI/CD pipeline enforces quality automatically

---

**Remember:** Quality is not optional. It's the difference between sustainable software and technical bankruptcy.
