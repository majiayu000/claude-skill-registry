---
activation_code: TEST_STRATEGY_V1
phase: 6.1
prerequisites:
  - OpenSpec proposals created
outputs:
  - Test strategy documentation
  - .signals/test-strategy-complete.json
description: |
  Generates comprehensive test strategies (60/30/10 distribution) from OpenSpec proposals.
  Activates via codeword [ACTIVATE:TEST_STRATEGY_V1] injected by hooks after
  OpenSpec proposal creation.
  
  Activation trigger: [ACTIVATE:TEST_STRATEGY_V1]
---

# Test Strategy Generator Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:TEST_STRATEGY_V1]
```

This occurs when:
- OpenSpec proposals are created
- User requests test strategy
- Preparing for Phase 7 implementation

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-2-task-strategy`:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 2 strategy
cd ./worktrees/phase-2-task-strategy

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Test strategy generation with isolation
```

### Test Strategy Isolation
1. **Isolated analysis**: OpenSpec proposals analyzed in dedicated workspace
2. **Strategy generation**: Test templates created without cross-contamination
3. **Template validation**: Test strategies validated before merge
4. **Clean merge**: Strategy artifacts merged atomically to main branch

# Test Strategy Generator Skill

## What This Skill Does

Automatically generates comprehensive test strategies from OpenSpec scenarios in isolated worktree:
- **Test Distribution:** 60% unit, 30% integration, 10% E2E tests
- **Test Templates:** Ready-to-use code in Arrange-Act-Assert format
- **Coverage Projection:** Estimates if 80% line / 70% branch achievable
- **TDD Enforcement:** RED-GREEN-REFACTOR cycle with failing tests first
- **Edge Cases:** Automatically suggests boundary conditions and error scenarios
- **NEW**: Worktree isolation for test strategy development
- **NEW**: Contamination-free strategy template generation

## When This Skill Activates

**Phase 6 & 7:** Creating OpenSpec proposals or starting implementation

**Trigger Patterns:**
- Creating OpenSpec proposal (`/openspec:proposal <n>`)
- Viewing OpenSpec proposal (`openspec show <n>`)
- Starting implementation (`/openspec:apply <n>`)
- User asks "what tests should I write?"


## What This Skill Does

### 1. Analyzes OpenSpec Scenarios
Extracts test cases from:
- Requirements (SHALL statements)
- Scenarios (GIVEN-WHEN-THEN)
- Edge cases mentioned
- Error conditions
- Acceptance criteria from TaskMaster

### 2. Generates Test Categories

**Unit Tests (60% of total tests):**
- One test per function/method
- Edge case tests
- Error handling tests
- Input validation tests

**Integration Tests (30% of total tests):**
- Component interaction tests
- Database integration tests
- API endpoint tests
- External service tests

**E2E Tests (10% of total tests):**
- Complete user workflow tests
- Critical path tests
- Multi-step scenario tests

### 3. Creates Test Templates

**Provides ready-to-use test skeletons:**
- Test file structure
- Test case names
- Arrange-Act-Assert sections
- Mock/stub suggestions
- Fixture requirements

### 4. Estimates Coverage

**Projects test coverage:**
- Expected line coverage
- Expected branch coverage
- Critical path coverage (must be 100%)
- Risk areas requiring extra tests

## Test Strategy Format

```markdown
## Test Strategy

### Overview
[1-2 sentence summary of testing approach]

### Test-Driven Development (TDD) Approach

**MANDATORY: Write tests FIRST before any implementation code**

1. **RED Phase:** Write failing tests
   - Create test file(s)
   - Write test cases for all scenarios
   - Run tests: MUST fail (proves tests are valid)
   - Commit failing tests

2. **GREEN Phase:** Implement minimum code
   - Write code to pass tests
   - Run tests continuously
   - Stop when all tests pass
   - Commit implementation

3. **REFACTOR Phase:** Improve code quality
   - Clean up code
   - Remove duplication
   - Run tests after EVERY change
   - Tests must stay GREEN

### Test Distribution (60/30/10 Rule)

**Unit Tests (60%):** [X] test cases
├─ [Test category 1]: [count] tests
├─ [Test category 2]: [count] tests
└─ [Test category 3]: [count] tests

**Integration Tests (30%):** [Y] test cases
├─ [Integration point 1]: [count] tests
└─ [Integration point 2]: [count] tests

**E2E Tests (10%):** [Z] test cases
└─ [Critical workflow]: [count] tests

**Total Test Cases:** [X+Y+Z] tests

### Coverage Requirements (BLOCKING)

**Minimum Thresholds:**
├─ Line coverage: ≥80%
├─ Branch coverage: ≥70%
├─ Function coverage: ≥80%
└─ Statement coverage: ≥80%

**Critical Paths (100% Required):**
├─ [Critical path 1]
├─ [Critical path 2]
└─ [Critical path 3]

### Test Files

```
tests/
├── unit/
│   ├── [component].test.js (main unit tests)
│   ├── [component].edge-cases.test.js (edge cases)
│   └── [component].errors.test.js (error handling)
├── integration/
│   ├── [component]-integration.test.js
│   └── [component]-[external-service].test.js
└── e2e/
    └── [workflow].e2e.test.js
```

### Validation Commands

```bash
# Run tests during development
npm test -- [component]           # Run specific tests
npm test -- --watch              # Watch mode for TDD

# Validate before marking complete
npm test                         # All unit tests
npm test:integration            # Integration tests
npm test:e2e                    # E2E tests (if applicable)
npm run coverage                # Coverage report (MUST meet thresholds)
npm test:regression             # Verify no regressions
```

### Test Fixtures & Mocks

**Required Fixtures:**
├─ [Fixture 1]: [Description]
├─ [Fixture 2]: [Description]
└─ [Fixture 3]: [Description]

**Mock Dependencies:**
├─ [Dependency 1]: Mock [reason]
├─ [Dependency 2]: Mock [reason]
└─ [Dependency 3]: Mock [reason]
```

## Test Template Generation

### Unit Test Template

**For each requirement, generate:**

```javascript
describe('[Component/Function Name]', () => {
  // Arrange: Setup
  beforeEach(() => {
    // Initialize mocks
    // Create test fixtures
  });

  afterEach(() => {
    // Cleanup
  });

  // Requirement 1: [OpenSpec Requirement Title]
  describe('[Requirement description]', () => {
    // Happy path from OpenSpec scenario
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = [test data];
      const expected = [expected result];
      
      // Act
      const actual = functionUnderTest(input);
      
      // Assert
      expect(actual).toEqual(expected);
    });

    // Edge case 1
    it('should [behavior] when [edge condition]', () => {
      // Test edge case
    });

    // Edge case 2
    it('should [behavior] when [another edge condition]', () => {
      // Test edge case
    });

    // Error case
    it('should throw [error type] when [invalid condition]', () => {
      // Test error handling
      expect(() => {
        functionUnderTest(invalidInput);
      }).toThrow(ExpectedError);
    });
  });

  // Repeat for each requirement...
});
```

### Integration Test Template

```javascript
describe('[Component] Integration', () => {
  let testDatabase;
  let testServer;

  beforeAll(async () => {
    // Setup test database
    testDatabase = await setupTestDB();
    // Start test server
    testServer = await startTestServer();
  });

  afterAll(async () => {
    // Cleanup
    await testDatabase.close();
    await testServer.close();
  });

  describe('[Integration Point]', () => {
    it('should [behavior] through full stack', async () => {
      // Arrange: Setup test data
      await testDatabase.seed([test data]);
      
      // Act: Make API request
      const response = await request(testServer)
        .post('/api/endpoint')
        .send([request body]);
      
      // Assert: Verify response
      expect(response.status).toBe(200);
      expect(response.body).toMatchObject([expected]);
      
      // Assert: Verify database state
      const dbRecord = await testDatabase.query([query]);
      expect(dbRecord).toMatchObject([expected state]);
    });
  });
});
```

### E2E Test Template

```javascript
describe('[User Workflow] E2E', () => {
  let page;

  beforeAll(async () => {
    page = await browser.newPage();
  });

  afterAll(async () => {
    await page.close();
  });

  it('should complete [workflow description]', async () => {
    // Step 1: [User action]
    await page.goto('/start-page');
    await page.fill('#input-field', 'test data');
    await page.click('#submit-button');
    
    // Step 2: [Expected result]
    await page.waitForSelector('.success-message');
    const message = await page.textContent('.success-message');
    expect(message).toContain('Success');
    
    // Step 3: [Next action]
    await page.click('#next-step');
    
    // Step 4: [Final verification]
    const finalState = await page.textContent('.final-state');
    expect(finalState).toBe('Expected final state');
  });
});
```

## Scenario-to-Test Mapping

**For each OpenSpec scenario:**

```markdown
**Scenario: User Registration**
GIVEN a new user with valid email and password
WHEN they submit the registration form
THEN account is created with pending status
AND verification email is sent
```

**Generates tests:**

```javascript
// Unit Tests
it('should create user account when valid data provided', () => {
  // Test user creation logic
});

it('should hash password before storing', () => {
  // Test password hashing
});

it('should set status to pending for new users', () => {
  // Test status initialization
});

it('should trigger email verification', () => {
  // Test email service call
});

// Integration Tests
it('should create user and send email through full registration flow', async () => {
  // Test API → Service → Database → Email service
});

// E2E Tests
it('should complete user registration from form to email', async () => {
  // Test full UI workflow
});
```

## Coverage Analysis

### Automatic Coverage Estimation

**Based on requirements count and complexity:**

```
Requirements: [N]
Expected Functions: [N * 3] (average 3 functions per requirement)
Expected Branches: [N * 5] (average 5 branches per requirement)

Estimated Tests Needed:
├─ Unit Tests: [N * 3 * 2] = [X] tests (2 tests per function: happy + edge)
├─ Integration Tests: [N * 1] = [Y] tests (1 per requirement)
└─ E2E Tests: [workflows] = [Z] tests

Total: [X + Y + Z] tests

With this test count:
├─ Expected Line Coverage: 85-90%
├─ Expected Branch Coverage: 75-80%
└─ Risk: [LOW / MEDIUM / HIGH]
```

### Critical Path Identification

**Automatically flags critical paths:**

```
CRITICAL PATHS (100% Coverage Required):
├─ Authentication flow
├─ Payment processing
├─ Data persistence
└─ Security-sensitive operations

These paths MUST have:
├─ All happy paths tested
├─ All error paths tested
├─ All edge cases tested
└─ Integration tests covering full flow
```

## Test Quality Checklist

**Generated for each requirement:**

```markdown
### Testing Checklist for [Requirement]

**Test Independence:**
- [ ] Tests can run in any order
- [ ] Tests don't depend on each other
- [ ] Tests clean up after themselves

**Test Completeness:**
- [ ] Happy path tested
- [ ] Edge cases tested (empty, null, max, min)
- [ ] Error cases tested
- [ ] Boundary conditions tested

**Test Quality:**
- [ ] Test names are descriptive
- [ ] Arrange-Act-Assert pattern used
- [ ] No magic numbers (use constants)
- [ ] Minimal mocking (only external dependencies)

**Test Performance:**
- [ ] Unit tests < 100ms each
- [ ] Integration tests < 1s each
- [ ] No flaky tests (deterministic)

**Coverage Validation:**
- [ ] Line coverage ≥80%
- [ ] Branch coverage ≥70%
- [ ] Critical paths 100%
```

## Edge Case Generator

**Automatically suggests edge cases:**

### For String Inputs:
- Empty string ("")
- Very long string (>1000 chars)
- Special characters
- Unicode characters
- Null/undefined

### For Numbers:
- Zero
- Negative numbers
- Very large numbers
- Decimal vs integer
- NaN, Infinity

### For Arrays:
- Empty array
- Single element
- Very large array
- Duplicate elements
- Null elements

### For Objects:
- Empty object
- Missing required fields
- Extra unexpected fields
- Nested objects
- Circular references

### For Dates:
- Past dates
- Future dates
- Leap years
- Time zones
- Invalid dates

## Error Scenario Generator

**Automatically generates error tests:**

```javascript
// Database errors
it('should handle database connection failure', async () => {
  mockDB.connect.mockRejectedValue(new Error('Connection failed'));
  await expect(service.method()).rejects.toThrow('Connection failed');
});

// Network errors
it('should handle network timeout', async () => {
  mockAPI.call.mockRejectedValue(new Error('Timeout'));
  await expect(service.method()).rejects.toThrow('Timeout');
});

// Validation errors
it('should reject invalid input', () => {
  const invalidInput = { /* bad data */ };
  expect(() => service.method(invalidInput)).toThrow(ValidationError);
});

// Authorization errors
it('should reject unauthorized access', async () => {
  const unauthenticatedUser = null;
  await expect(service.method(unauthenticatedUser)).rejects.toThrow(UnauthorizedError);
});

// Rate limiting
it('should enforce rate limits', async () => {
  // Make N requests
  for (let i = 0; i < rateLimitThreshold + 1; i++) {
    if (i < rateLimitThreshold) {
      await expect(service.method()).resolves.toBeDefined();
    } else {
      await expect(service.method()).rejects.toThrow(RateLimitError);
    }
  }
});
```

## Mock Strategy Suggestions

**Analyzes dependencies and suggests mocking approach:**

```markdown
### Dependency: Database
**Strategy:** Mock with in-memory implementation
**Reason:** Fast, deterministic, no external dependency
**Implementation:** Use test fixtures with jest.mock()

### Dependency: External API (Stripe)
**Strategy:** Use Stripe test mode + mock responses
**Reason:** Avoid real charges, control responses
**Implementation:** Nock or MSW for HTTP mocking

### Dependency: Email Service
**Strategy:** Mock email sending
**Reason:** Don't send real emails in tests
**Implementation:** Capture calls, verify parameters

### Dependency: File System
**Strategy:** Use in-memory file system
**Reason:** Fast, isolated, no cleanup needed
**Implementation:** memfs or mock-fs
```

## Integration with OpenSpec Proposal

**Automatically adds test strategy section:**

```markdown
## Requirements

### Requirement 1: User Registration
The system SHALL create user accounts with email verification.

**Scenarios:**
- GIVEN valid email and password
  WHEN user submits registration
  THEN account created with pending status
  AND verification email sent

**TEST STRATEGY GENERATED:**

#### Unit Tests (5 tests)
1. Test user account creation logic
2. Test password hashing (bcrypt)
3. Test email validation
4. Test status initialization (pending)
5. Test email service trigger

#### Integration Tests (2 tests)
1. Full registration flow: API → Service → DB → Email
2. Duplicate email rejection flow

#### E2E Test (1 test)
1. Complete registration: Form → Submit → Email → Verify

#### Test Files
- `tests/unit/auth.service.test.js`
- `tests/integration/auth-integration.test.js`
- `tests/e2e/registration.e2e.test.js`

#### Expected Coverage
- Line: 90% (registration is critical path)
- Branch: 85% (multiple validation paths)
- Critical: 100% (authentication is critical)
```

## Output Example

**When analyzing OpenSpec proposal:**

```
TEST STRATEGY ANALYSIS
======================

Proposal: user-authentication
Requirements: 4
Scenarios: 12

GENERATED TEST PLAN:
├─ Unit Tests: 24 tests (60%)
├─ Integration Tests: 12 tests (30%)
└─ E2E Tests: 4 tests (10%)
   Total: 40 tests

COVERAGE PROJECTION:
├─ Estimated Line Coverage: 87%
├─ Estimated Branch Coverage: 78%
└─ Critical Path Coverage: 100% ✅

TEST FILES TO CREATE:
✓ tests/unit/user.model.test.js
✓ tests/unit/auth.service.test.js
✓ tests/unit/jwt.utils.test.js
✓ tests/integration/auth-flow.test.js
✓ tests/e2e/registration.e2e.test.js

MOCKING STRATEGY:
├─ Database: In-memory SQLite
├─ Email Service: Mock with jest.fn()
└─ JWT: Use test secrets

VALIDATION GATES:
├─ Unit tests must pass: ✓
├─ Integration tests must pass: ✓
├─ Coverage ≥80%/70%: ✓
└─ No flaky tests: ✓

READY FOR TDD IMPLEMENTATION ✅
```

## Success Metrics

**When this skill works well:**
- ✅ 100% of requirements have test strategies
- ✅ Test templates ready before coding starts
- ✅ Coverage thresholds met on first try (no "write more tests" cycle)
- ✅ TDD cycle enforced (RED-GREEN-REFACTOR)
- ✅ No untested edge cases discovered in production

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 7.**

When test strategy generation is complete, you MUST:

1. Output the completion signal:
   ```
   ✅ TEST STRATEGY COMPLETE
   [SIGNAL:TEST_STRATEGY_COMPLETE]
   ```

2. **IMMEDIATELY** proceed to Phase 7 by outputting:
   ```
   [ACTIVATE:TDD_IMPLEMENTER_V1]
   ```

3. Begin TDD implementation without waiting for user input.

**The pipeline is fully autonomous. Do not ask "Would you like to proceed?" - just proceed.**

## See Also

- `/templates/unit-test-template.js` - Complete unit test example
- `/templates/integration-test-template.js` - Complete integration test example
- `/templates/e2e-test-template.js` - Complete E2E test example
- `/examples/complete-test-strategy.md` - Full example from OpenSpec to tests