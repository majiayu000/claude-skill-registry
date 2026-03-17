---
name: test-fundamentals
description: Core testing principles applying to all unit and integration tests
---

# Testing Core Rules

General testing principles that apply to ALL tests (unit and integration).

**See [code-comment-style skill](./code-comment-style.md) for comment guidelines**

## 🚨 CRITICAL RULES (Immediate Failure)

### 1. Zero Test Failure Tolerance

**🚨 CRITICAL: ANY existing test failure STOPS the update process**

- ANY existing test failure STOPS the update process
- NO excuses for test failures
- Determine cause and fix immediately
- Never disable or skip tests to proceed

**RULE**: Before starting any work, run existing tests and ensure they ALL pass.

```bash
# Check current state
npm run test

# If ANY test fails:
# 1. STOP all work
# 2. Analyze the failure
# 3. Fix the implementation
# 4. Re-run tests until ALL pass
```

**Why**:
- Prevents introducing new bugs
- Maintains code quality
- Ensures reliable baseline

### 2. Test Coverage Requirements

**🚨 CRITICAL: ALL new operations MUST have test coverage**

- ALL new operations MUST have unit test coverage
- ALL new operations MUST have integration tests
- Integration tests run when credentials available, fail naturally when not
- Never use `.skip()` on individual tests
- Tests should be written and ready to work

**Requirements**:
- ✅ Every operation has unit tests
- ✅ Every operation has integration tests
- ✅ Both success and error cases tested
- ✅ 100% pass rate for available tests

**Example**:
```typescript
// ✅ CORRECT: Both unit and integration tests
test/unit/UserProducerTest.ts       // Unit test with nock
test/integration/UserProducerTest.ts // Integration test with real API

// ❌ WRONG: Only one test type
test/unit/UserProducerTest.ts       // Missing integration test
```

### 3. Test Preservation

**🚨 CRITICAL: EXISTING tests must pass throughout entire workflow**

- EXISTING tests must pass throughout entire workflow
- NEVER modify existing tests during updates
- Add new tests separately

**Why**:
- Prevents breaking existing functionality
- Maintains test suite integrity
- Ensures backward compatibility

**Exceptions**: Only in 'fix' workflow when API has breaking changes (see Exceptions section)

### 4. API Validation Before Implementation

**🚨 CRITICAL: Test every operation with curl/Node.js FIRST**

Before implementing any operation:
1. Test with curl or Node.js script
2. Capture real API responses
3. Save as test fixtures
4. Verify credentials work

```bash
# Example: Test API endpoint before implementing
curl -X GET "https://api.example.com/users/123" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json"

# Capture response, sanitize PII, save as fixture
# THEN implement the operation
```

**Why**:
- Verifies API works as documented
- Captures real response structure
- Identifies auth issues early
- Provides fixtures for unit tests

### 5. Test Failure Resolution Protocol

**🚨 CRITICAL: MANDATORY when tests fail**

**When tests fail, follow this protocol:**

1. **ANALYZE** the failure - understand why
2. **FIX THE IMPLEMENTATION** - correct bugs in src/
3. **NEVER SKIP TESTS** - no .skip(), .only(), or comments
4. **NEVER MODIFY GENERATED FILES**
5. **RE-RUN TESTS** - execute until ALL pass
6. **REPEAT UNTIL ZERO FAILURES**

**PROHIBITED**:
- Using `.skip()` on individual tests
- Using `.only()` to run only passing tests
- Commenting out failing tests
- Accepting any failures as "expected"
- Modifying test expectations to match wrong behavior

**Required Pass Rates**:
- **Unit Tests**: 100% pass rate
- **Integration Tests**: 100% when credentials available
- **Lint**: Zero errors, zero warnings
- **Build**: Exit code 0

**Example of CORRECT approach**:
```typescript
// Test fails: expected 'John' but got 'John Doe'

// ❌ WRONG: Skip the test
it.skip('should get user name', async () => { ... });

// ❌ WRONG: Change expectation
expect(user.name).to.equal('John Doe'); // Changed to match wrong output

// ✅ CORRECT: Fix the implementation
// Fix the mapping in src/Mappers.ts to extract first name correctly
// Re-run test until it passes
```

## 🟡 STANDARD RULES

### Test Naming

**Use descriptive test names explaining the scenario:**

```typescript
// ✅ GOOD - Clear, specific
it('should retrieve user by ID with correct type mapping', async () => { ... });
it('should throw NoSuchObjectError when user not found', async () => { ... });
it('should map email string to Email type', async () => { ... });

// ❌ BAD - Vague, unclear
it('should work', async () => { ... });
it('test get user', async () => { ... });
```

**Use 'should' for expected behaviors:**
- ✅ "should retrieve user by ID"
- ✅ "should throw error when invalid ID"
- ✅ "should map API response to core types"

**Include failure cases:**
- ✅ "should throw error when user not found"
- ✅ "should handle authentication failure"
- ✅ "should return empty array when no results"

### Test Execution Order

**Run tests in this order:**

1. **Unit tests first** (fast feedback)
   ```bash
   npm run test:unit
   ```

2. **Integration tests with credentials**
   ```bash
   npm run test:integration
   ```

3. **Lint and build**
   ```bash
   npm run lint
   npm run build
   ```

4. **All must pass for task completion**

**Why this order**:
- Unit tests are fast, catch most issues
- Integration tests verify real API behavior
- Lint catches style issues
- Build verifies TypeScript compilation

### Test Structure

**Standard describe/it structure:**

```typescript
describe('{ClassName}', () => {
  describe('{methodName}', () => {
    it('should {expected behavior}', async () => {
      // Arrange - Set up test data
      // Act - Execute the method
      // Assert - Verify the result
    });

    it('should {handle error case}', async () => {
      // Arrange - Set up error condition
      // Act - Execute the method
      // Assert - Verify error handling
    });
  });
});
```

**Key elements**:
- ✅ Outer describe for class/module
- ✅ Inner describe for method
- ✅ Multiple it() for different scenarios
- ✅ Arrange/Act/Assert pattern

## 🟡 STANDARD RULES

### Debug Logging (MANDATORY for Integration Tests)

**ALL integration tests MUST include debug logging** to enable:
- Runtime mapper validation
- Test failure debugging
- API response verification

**Standard Pattern:**

```typescript
import { LoggerEngine } from '@zerobias-org/logger';

const logger = LoggerEngine.root();

describe('User Producer Tests', function() {
  it('should list users', async function() {
    const result = await userApi.list(organizationId);

    // MANDATORY: Log operation and result
    logger.debug(`userApi.list(${organizationId})`, JSON.stringify(result, null, 2));

    expect(result).to.not.be.null;
    // ... assertions
  });
});
```

**Requirements:**
- ✅ Import logger from `@zerobias-org/logger`
- ✅ Create logger with LOG_LEVEL from environment
- ✅ Log AFTER every API operation call
- ✅ Include operation name and parameters in log
- ✅ Include full result as JSON.stringify

**Visibility:**
```bash
# Normal run - no debug output
npm run test:integration

# Debug run - full logging
env LOG_LEVEL=debug npm run test:integration
```

**Benefits:**
- Enables runtime mapper field validation
- Quick debugging of test failures
- Documents actual API behavior
- Verifies responses match expectations

**RULE:** Integration tests without debug logging are INCOMPLETE.

## 🟢 GUIDELINES

### Documentation

**Document test setup in USERGUIDE.md:**

```markdown
## Testing

### Unit Tests

Unit tests run without credentials and use mocked HTTP interactions:

\`\`\`bash
npm run test:unit
\`\`\`

### Integration Tests

Integration tests require credentials in a `.env` file:

\`\`\`bash
# .env
SERVICE_API_KEY=your-api-key
SERVICE_EMAIL=your-email
SERVICE_PASSWORD=your-password
\`\`\`

Run integration tests:

\`\`\`bash
npm run test:integration

# With debug logging:
LOG_LEVEL=debug npm run test:integration
\`\`\`

### Full Test Suite

Run all tests:

\`\`\`bash
npm test
\`\`\`
```

### Skipped Tests

**When tests can be skipped (ONLY for integration test suites):**

```typescript
// ✅ ALLOWED: Skip entire integration suite if no credentials
describe('Service Integration', function () {
  before(function () {
    if (!hasCredentials()) {
      this.skip(); // Skip whole suite
    }
  });
});

// ❌ FORBIDDEN: Skip individual tests
it.skip('should get user', async () => { ... });
```

**Document skipped tests in output:**
- Integration tests should log when skipped due to missing credentials
- User should see clear message about how to enable tests

## Exceptions

### When Tests Can Be Modified

**Tests can ONLY be modified in these scenarios:**

1. **'fix' workflow** (not 'update')
   - When fixing existing bugs
   - When API has breaking changes
   - When correcting incorrect test logic

2. **API Breaking Changes**
   - When API endpoint changes
   - When response structure changes
   - When authentication method changes

3. **Incorrect Test Logic**
   - When test expectations were wrong
   - When test setup was incorrect
   - When test assertions don't match requirements

**ALWAYS document reason in commit message:**
```
fix: update UserProducer tests for API breaking change

The API changed the user endpoint from /users/:id to /v2/users/:id
and added a required 'version' field in the response.

Updated tests to match new API contract.
```

### Integration Test Exceptions

**Integration tests have special skip rules:**

- Can skip entire suite if no credentials (using `this.skip()` in before hook)
- Must document in test output
- Should provide instructions for enabling

```typescript
before(function () {
  if (!hasCredentials()) {
    console.log('Skipping integration tests: no credentials in .env');
    console.log('Create a .env file with SERVICE_API_KEY to enable');
    this.skip();
  }
});
```

## Validation

**Validate general testing rules:**

```bash
# Check test files exist
ls -lh test/unit/
ls -lh test/integration/

# Run all tests
npm run clean
npm run build
npm run test
npm run test:integration  # If credentials available

# Check for skipped tests (should only be integration suites without creds)
npm test 2>&1 | grep -i "skip"

# Check for test failures (should be none)
npm test 2>&1 | grep -i "fail" && echo "❌ FAIL: Tests failing" || echo "✅ PASS"

# Check build exits with 0
npm run build && echo "✅ PASS: Build successful" || echo "❌ FAIL: Build failed"

# Check lint passes
npm run lint && echo "✅ PASS: Lint successful" || echo "❌ FAIL: Lint failed"
```

**Expected results:**
- ✅ All tests pass
- ✅ Only integration suites skip when no credentials
- ✅ No individual tests skipped
- ✅ Build exits with code 0
- ✅ Lint passes with zero errors/warnings

## Comment Style for Tests

**See [code-comment-style skill](./code-comment-style.md) for complete guidelines**

### Key Rules for Test Code

**NEVER comment obvious assertions:**

```typescript
// ❌ WRONG - Comments restate assertions
// Required fields
expect(entry).to.have.property('id');
expect(entry).to.have.property('name');

// ID should be a string
expect(entry.id).to.be.a('string');

// Validate structure
const groups = groupsResult.items;
expect(groups).to.be.an('array');

// ✅ CORRECT - Assertions are self-documenting
expect(entry).to.have.property('id');
expect(entry).to.have.property('name');
expect(entry.id).to.be.a('string');

const groups = groupsResult.items;
expect(groups).to.be.an('array');
```

**DO comment non-obvious test logic:**

```typescript
// ✅ GOOD - Explains special test case
// Unicode group names require special URL encoding on this endpoint
const result = await groupApi.get(orgId, '测试组');

// ✅ GOOD - Explains API quirk being tested
// API returns 400 for invalid credentials but 404 for missing users
// We normalize both to NotConnectedError for consistent handling
try {
  await userApi.get(invalidUserId);
} catch (error) {
  expect(error).to.be.instanceOf(NotConnectedError);
}
```

**Use Arrange/Act/Assert pattern without comments:**

```typescript
// ❌ WRONG - Structural comments
it('should get user by ID', async () => {
  // Arrange - Set up test data
  const userId = 'test-123';

  // Act - Execute the method
  const result = await userApi.get(orgId, userId);

  // Assert - Verify the result
  expect(result).to.not.be.null;
  expect(result.id).to.equal(userId);
});

// ✅ CORRECT - Blank lines show structure
it('should get user by ID', async () => {
  const userId = 'test-123';

  const result = await userApi.get(orgId, userId);

  expect(result).to.not.be.null;
  expect(result.id).to.equal(userId);
});
```

**Reference**: See [code-comment-style.md](./code-comment-style.md) for full guidelines
