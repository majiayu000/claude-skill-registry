---
name: testing-strategy
description: |
  Test planning and coverage strategy workflow. Use when designing test suites,
  establishing coverage targets, planning TDD approaches, or assessing
  testing gaps in existing codebases.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Testing Strategy

Systematic test planning and coverage improvement workflow.

## When to Use

| Trigger | Description |
|---------|-------------|
| **Post-COMPLEX Feature** | After implementing major features |
| **Coverage Drop** | When coverage falls below thresholds |
| **Test Debt Sprint** | Dedicated testing improvement effort |
| **New Project** | Establishing testing foundation |
| **Pre-Release** | Ensuring quality before deployment |

---

## Coverage Targets

| Category | Target | Warning | Critical |
|----------|--------|---------|----------|
| Business Logic | >80% | 70-80% | <70% |
| Overall | >60% | 50-60% | <50% |
| Critical Paths | >90% | 80-90% | <80% |

---

## Prerequisites

Before starting:

- [ ] Test framework configured
- [ ] Coverage tool available
- [ ] CI/CD running tests
- [ ] Access to current coverage report
- [ ] Understanding of business-critical features

---

## Strategy Process

```
Phase 1: Coverage Analysis
    ↓
Phase 2: Critical Path Identification
    ↓
Phase 3: Test Pyramid Planning
    ↓
Phase 4: Test Prioritization
    ↓
Phase 5: Edge Case Planning
    ↓
Phase 6: Flaky Test Remediation
    ↓
Phase 7: Implementation Roadmap
```

---

## Phase 1: Coverage Analysis

### 1.1 Generate Coverage Report

**Node.js (Jest/Vitest)**:
```bash
npm test -- --coverage
# or
npx vitest run --coverage
```

**Python (pytest)**:
```bash
pytest --cov=src --cov-report=html
```

**Go**:
```bash
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

**Rust**:
```bash
cargo tarpaulin --out Html
```

### 1.2 Analyze Coverage Gaps

Review coverage report for:

| Area | Target | Current | Gap |
|------|--------|---------|-----|
| `src/auth/` | 90% | 45% | -45% |
| `src/api/` | 80% | 62% | -18% |
| `src/utils/` | 60% | 78% | +18% |
| **Overall** | 60% | 55% | -5% |

### 1.3 Identify Uncovered Files

List files with lowest coverage:

```
Lowest Coverage Files:
1. src/auth/oauth.ts - 12% (critical!)
2. src/api/payments.ts - 28% (critical!)
3. src/services/email.ts - 35%
4. src/utils/validation.ts - 42%
5. src/api/users.ts - 48%
```

---

## Phase 2: Critical Path Identification

### 2.1 Define Critical Paths

Critical paths are user journeys that MUST work:

| Path | Description | Files | Priority |
|------|-------------|-------|----------|
| Authentication | Login, logout, session | auth/* | P0 |
| Checkout | Cart → Payment → Confirm | payments/*, cart/* | P0 |
| Registration | Signup → Verify → Profile | users/*, email/* | P1 |
| Search | Query → Results → Filter | search/*, api/* | P1 |

### 2.2 Map Critical Files

For each critical path, list involved files:

**Authentication Path**:
```
src/auth/login.ts        - 45% coverage
src/auth/session.ts      - 52% coverage
src/auth/middleware.ts   - 88% coverage
src/models/user.ts       - 72% coverage
```

### 2.3 Calculate Critical Path Coverage

```
Authentication Path:
- Total lines: 450
- Covered lines: 267
- Coverage: 59% (target: 90%)
- Gap: 183 lines to cover
```

---

## Phase 3: Test Pyramid Planning

### 3.1 Ideal Test Pyramid

```
         /\
        /  \
       / E2E \         10% - Slow, expensive, covers user flows
      /______\
     /        \
    /Integration\      20% - Medium speed, covers integrations
   /______________\
  /                \
 /    Unit Tests    \  70% - Fast, cheap, covers logic
/____________________\
```

### 3.2 Current Distribution

Analyze current test distribution:

```
Current State:
- Unit tests: 45 (60%)
- Integration: 25 (33%)
- E2E: 5 (7%)

Ideal State:
- Unit tests: 70 (70%)
- Integration: 20 (20%)
- E2E: 10 (10%)

Gap:
- Need +25 unit tests
- Need -5 integration tests (or OK)
- Need +5 E2E tests
```

### 3.3 Test Type Guidelines

**Unit Tests** (70%):
- Pure functions
- Business logic
- Utility functions
- Model methods
- State transitions

**Integration Tests** (20%):
- API endpoints
- Database operations
- Service interactions
- Authentication flows
- External service mocks

**E2E Tests** (10%):
- Critical user journeys
- Happy path scenarios
- Cross-system flows
- Smoke tests

---

## Phase 4: Test Prioritization

### 4.1 Priority Matrix

| Priority | Criteria | Example |
|----------|----------|---------|
| P0 | Critical path, no tests | Payment processing |
| P1 | Critical path, low coverage | Authentication |
| P2 | High risk, medium coverage | Data validation |
| P3 | Medium risk, any coverage | Utility functions |
| P4 | Low risk, nice to have | Formatting helpers |

### 4.2 Effort Estimation

| Test Type | Effort | Coverage Impact |
|-----------|--------|-----------------|
| Unit (simple) | 15 min | High |
| Unit (complex) | 1 hour | High |
| Integration | 2 hours | Medium |
| E2E | 4 hours | Low (but valuable) |

### 4.3 Prioritized Test Backlog

```markdown
## Test Backlog

### P0 - Immediate (This Sprint)
- [ ] Unit: payment.processPayment()
- [ ] Unit: auth.validateToken()
- [ ] Integration: POST /api/payments
- [ ] E2E: Complete checkout flow

### P1 - High (Next Sprint)
- [ ] Unit: auth.refreshToken()
- [ ] Unit: user.validateEmail()
- [ ] Integration: GET /api/users/:id
- [ ] E2E: Registration flow

### P2 - Medium (Backlog)
- [ ] Unit: validation helpers
- [ ] Unit: formatting utilities
- [ ] Integration: Search API

### P3 - Low (Nice to Have)
- [ ] Unit: logging utilities
- [ ] Unit: config loaders
```

---

## Phase 5: Edge Case Planning

### 5.1 Required Edge Cases

Every function should test:

| Category | Cases | Example |
|----------|-------|---------|
| Null/Undefined | null, undefined input | `validateUser(null)` |
| Empty | "", [], {} | `searchUsers("")` |
| Boundary | 0, -1, MAX_INT | `setQuantity(0)` |
| Invalid Type | Wrong type input | `calculatePrice("abc")` |
| Concurrent | Race conditions | Parallel updates |

### 5.2 Edge Case Checklist

For each function:

- [ ] Happy path tested
- [ ] Null input tested
- [ ] Undefined input tested
- [ ] Empty input tested
- [ ] Minimum boundary tested
- [ ] Maximum boundary tested
- [ ] Invalid type tested
- [ ] Error conditions tested

---

## Phase 6: Flaky Test Remediation

### 6.1 Identify Flaky Tests

Signs of flaky tests:
- Intermittent failures in CI
- Tests that pass locally but fail in CI
- Tests that depend on execution order
- Tests with timing-dependent assertions

### 6.2 Common Causes & Fixes

| Cause | Symptom | Fix |
|-------|---------|-----|
| Timing | Random timeouts | Use proper async/await |
| Order dependency | Fails when run alone | Reset state in beforeEach |
| Shared state | Random failures | Isolate test data |
| External services | Network failures | Mock external calls |
| Date/time | Fails at midnight | Mock dates |

---

## Phase 7: Implementation Roadmap

### 7.1 Sprint Planning Template

```markdown
## Sprint 1: Critical Path (2 weeks)

### Goals
- Achieve 90% coverage on authentication
- Achieve 90% coverage on payments
- Add 5 E2E tests for critical paths

### Tasks
1. Unit tests for auth module (20 tests)
2. Unit tests for payment module (15 tests)
3. Integration tests for auth API (5 tests)
4. E2E test: Complete checkout (1 test)
5. E2E test: Login flow (1 test)

### Expected Outcome
- Overall coverage: 55% → 65%
- Critical path coverage: 59% → 90%
```

### 7.2 Test Writing Guidelines

**Test Structure**:
```typescript
describe('Module or Function', () => {
  // Setup
  beforeEach(() => {
    // Reset state
  });

  describe('method or scenario', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = createTestInput();

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });
  });
});
```

**Naming Convention**:
```
should [expected behavior] when [condition]

Examples:
- should return user when valid ID provided
- should throw error when user not found
- should update timestamp when saving
```

### 7.3 Coverage Tracking

Track coverage weekly:

| Week | Overall | Business | Critical | Tests Added |
|------|---------|----------|----------|-------------|
| 1 | 55% | 62% | 59% | +15 |
| 2 | 62% | 75% | 78% | +22 |
| 3 | 68% | 82% | 88% | +18 |
| 4 | 72% | 85% | 92% | +12 |

---

## Quick Reference

### Coverage Commands

```bash
# Node.js
npm test -- --coverage --coverageReporters=text-summary

# Python
pytest --cov=src --cov-report=term-missing

# Go
go test -cover ./... | grep -E "coverage:"

# Rust
cargo tarpaulin --out Stdout
```

### Test Templates

**Unit Test**:
```typescript
describe('functionName', () => {
  it('should [behavior] when [condition]', () => {
    const result = functionName(input);
    expect(result).toEqual(expected);
  });
});
```

**Integration Test**:
```typescript
describe('POST /api/resource', () => {
  it('should create resource when valid data', async () => {
    const response = await request(app)
      .post('/api/resource')
      .send(validData);
    expect(response.status).toBe(201);
  });
});
```

---

## Checklist

### Analysis
- [ ] Coverage report generated
- [ ] Gaps identified
- [ ] Critical paths mapped
- [ ] Current pyramid analyzed

### Planning
- [ ] Tests prioritized
- [ ] Edge cases documented
- [ ] Flaky tests identified
- [ ] Sprint plan created

### Implementation
- [ ] P0 tests written
- [ ] P1 tests written
- [ ] Edge cases covered
- [ ] Flaky tests fixed

### Validation
- [ ] Coverage targets met
- [ ] All tests passing
- [ ] No flaky tests
- [ ] CI/CD updated

---

## Extended Resources

For detailed examples, patterns, and in-depth guidance, see:
- `references/process.md` - Comprehensive testing patterns and examples

## Related Resources

- `code-review` - Includes test validation
- `refactoring` - Tests enable safe refactoring
- `troubleshooting` - When tests fail unexpectedly
