---
name: gate-4a-unit-tests
description: Gate 4a validation: Unit test creation and nock-only enforcement
---

### Gate 4a: Unit Test Creation

**Purpose:** Validate unit test quality, mocking strategy, and coverage

**STOP AND CHECK:**
```bash
# 1. Unit test files exist
if ! ls test/unit/*Test.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4a FAILED: No unit test files found"
  echo "   Create test/unit/{Resource}ProducerTest.ts"
  echo "   See unit-test-patterns skill"
  exit 1
fi

TEST_FILE_COUNT=$(ls test/unit/*Test.ts 2>/dev/null | wc -l)
echo "✅ Found $TEST_FILE_COUNT unit test file(s)"

# 2. Test suites exist with proper structure
DESCRIBE_COUNT=$(grep -h "^describe(" test/unit/*.ts 2>/dev/null | wc -l)
if [ "$DESCRIBE_COUNT" -lt 1 ]; then
  echo "❌ Gate 4a FAILED: No describe blocks found"
  echo "   Unit tests must have describe blocks"
  exit 1
fi
echo "✅ Found $DESCRIBE_COUNT describe block(s)"

# 3. Multiple test cases (3+ per operation)
IT_COUNT=$(grep -h "^\s*it(" test/unit/*.ts 2>/dev/null | wc -l)
if [ "$IT_COUNT" -lt 3 ]; then
  echo "❌ Gate 4a FAILED: Insufficient test cases (found $IT_COUNT, need 3+)"
  echo "   Each operation needs multiple test cases including error scenarios"
  exit 1
fi
echo "✅ Found $IT_COUNT test case(s)"

# 4. CRITICAL: ONLY nock used for HTTP mocking
if ! grep -h "from ['\"]nock['\"]" test/unit/*.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4a FAILED: nock not imported in unit tests"
  echo "   Unit tests MUST use nock for HTTP mocking"
  echo ""
  echo "Add to test files:"
  echo "  import * as nock from 'nock';"
  echo ""
  echo "See nock-patterns skill for examples"
  exit 1
fi
echo "✅ nock imported for HTTP mocking"

# 5. CRITICAL: No forbidden mocking libraries
FORBIDDEN_MOCKS=$(grep -h -E "jest\.mock|sinon|fetch-mock|msw" test/unit/*.ts 2>/dev/null || true)
if [ -n "$FORBIDDEN_MOCKS" ]; then
  echo "❌ Gate 4a FAILED: Forbidden mocking library detected"
  echo "   ONLY nock is allowed for HTTP mocking"
  echo ""
  echo "Found forbidden libraries:"
  echo "$FORBIDDEN_MOCKS"
  echo ""
  echo "Fix: Replace with nock HTTP mocking"
  echo "See failure-conditions skill Rule #4"
  exit 1
fi
echo "✅ No forbidden mocking libraries"

# 6. Verify Common.ts exists and is properly structured
if [ ! -f "test/unit/Common.ts" ]; then
  echo "❌ Gate 4a FAILED: test/unit/Common.ts missing"
  echo "   Create Common.ts with getConnectedInstance helper"
  echo "   See unit-test-patterns skill for template"
  exit 1
fi

# Verify Common.ts uses nock (not real credentials)
if ! grep -q "import.*nock" test/unit/Common.ts; then
  echo "⚠️  WARNING: Common.ts should import nock"
  echo "   Unit test Common.ts must use mocked HTTP, not real API"
fi

# Verify Common.ts does NOT use dotenv or process.env
if grep -E "dotenv|process\.env" test/unit/Common.ts > /dev/null 2>&1; then
  echo "❌ Gate 4a FAILED: Common.ts uses environment variables"
  echo "   Unit tests must NOT depend on .env or process.env"
  echo "   Use nock to mock HTTP requests instead"
  echo ""
  echo "Found:"
  grep -n -E "dotenv|process\.env" test/unit/Common.ts
  exit 1
fi
echo "✅ Common.ts properly structured (no env vars)"

# 7. Verify error cases are tested
ERROR_TESTS=$(grep -h -i "error\|fail\|invalid\|unauthorized\|notfound\|404\|401" test/unit/*.ts 2>/dev/null | wc -l)
if [ "$ERROR_TESTS" -lt 1 ]; then
  echo "⚠️  WARNING: No error case tests found"
  echo "   Tests should cover error scenarios:"
  echo "   - 401 → InvalidCredentialsError"
  echo "   - 404 → NoSuchObjectError"
  echo "   - 429 → RateLimitExceededError"
fi

# 8. Verify mocking at HTTP level (not method level)
METHOD_MOCKS=$(grep -h -E "\.mockReturnValue\(|\.mockResolvedValue\(|\.mockImplementation\(" test/unit/*.ts 2>/dev/null || true)
if [ -n "$METHOD_MOCKS" ]; then
  echo "⚠️  WARNING: Method-level mocking detected"
  echo "   Use HTTP-level mocking with nock instead"
  echo ""
  echo "Found:"
  echo "$METHOD_MOCKS"
  echo ""
  echo "Fix: Use nock('https://api.example.com').get('/path').reply(200, data);"
fi

# 9. Verify nock cleanup in tests
if ! grep -h "nock.cleanAll()" test/unit/*.ts > /dev/null 2>&1; then
  echo "⚠️  WARNING: No nock.cleanAll() found"
  echo "   Add afterEach(() => nock.cleanAll()) to clean up mocks"
fi

# 10. Check test file naming convention
for file in test/unit/*Test.ts; do
  if [ -f "$file" ]; then
    basename=$(basename "$file")
    if [[ ! "$basename" =~ ^[A-Z][a-zA-Z]*Test\.ts$ ]] && [[ "$basename" != "Common.ts" ]]; then
      echo "⚠️  WARNING: Incorrect test file naming: $basename"
      echo "   Should be: {Resource}ProducerTest.ts or ConnectionTest.ts"
    fi
  fi
done

echo ""
echo "✅ Gate 4a: Unit Test Creation - PASSED"
```

**PROCEED ONLY IF:**
- ✅ Unit test file(s) exist in test/unit/
- ✅ Test suites have describe blocks
- ✅ At least 3 test cases per operation
- ✅ Error cases are covered
- ✅ **ONLY nock used for HTTP mocking** (CRITICAL)
- ✅ **NO forbidden mocking libraries** (jest.mock, sinon, fetch-mock, msw)
- ✅ Common.ts exists and uses nock (NO env vars)
- ✅ Mocking at HTTP level (not method/function level)
- ✅ nock cleanup present (afterEach)

**IF FAILED:**
- Unit tests are MANDATORY
- Fix mocking violations immediately
- See unit-test-patterns skill for correct patterns
- See nock-patterns skill for HTTP mocking examples

## Common Failures

### 1. Using jest.mock or sinon

```typescript
// ❌ WRONG - forbidden mocking library
import { jest } from '@jest/globals';
jest.mock('./ServiceClient');

const mockClient = {
  getUser: jest.fn().mockResolvedValue({ id: '123' })
};

// ❌ WRONG - sinon stubs
import sinon from 'sinon';
const stub = sinon.stub(client, 'getUser').resolves({ id: '123' });

// ✅ CORRECT - nock HTTP mocking
import * as nock from 'nock';

nock('https://api.service.com')
  .get('/users/123')
  .reply(200, { id: '123', name: 'John' });

const user = await producer.getUser('123');
```

**Why:**
- nock mocks at HTTP network level
- Consistent with existing test infrastructure
- Works with any HTTP client library
- Can record and replay real API interactions

### 2. Method-level mocking

```typescript
// ❌ WRONG - mocking methods
const mockGetUser = jest.fn().mockResolvedValue({ id: '123' });
client.getUser = mockGetUser;

// ❌ WRONG - mocking class instance
jest.spyOn(client, 'getUser').mockReturnValue(Promise.resolve({ id: '123' }));

// ✅ CORRECT - HTTP level with nock
import * as nock from 'nock';

nock('https://api.service.com')
  .get('/users/123')
  .reply(200, { id: '123', name: 'John' });

// Call real implementation - nock intercepts HTTP request
const user = await producer.getUser('123');
expect(user.id).to.be.instanceof(UUID);
```

**Why:**
- Tests real implementation code paths
- Verifies HTTP request formatting
- Ensures proper error handling
- Catches integration issues

### 3. No error case tests

```typescript
// ❌ WRONG - only happy path
describe('UserProducer', () => {
  it('should list users', async () => {
    nock('https://api.service.com')
      .get('/users')
      .reply(200, [{ id: '123' }]);

    const users = await producer.listUsers();
    expect(users).to.have.length(1);
  });
});

// ✅ CORRECT - include error cases
describe('UserProducer', () => {
  it('should list users successfully', async () => {
    nock('https://api.service.com')
      .get('/users')
      .reply(200, [{ id: '123' }]);

    const users = await producer.listUsers();
    expect(users).to.have.length(1);
  });

  it('should throw InvalidCredentialsError on 401', async () => {
    nock('https://api.service.com')
      .get('/users')
      .reply(401, { error: 'Unauthorized' });

    try {
      await producer.listUsers();
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error).to.be.instanceOf(InvalidCredentialsError);
    }
  });

  it('should throw NoSuchObjectError on 404', async () => {
    nock('https://api.service.com')
      .get('/users/999')
      .reply(404, { error: 'Not found' });

    try {
      await producer.getUser('999');
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error).to.be.instanceOf(NoSuchObjectError);
    }
  });

  it('should throw RateLimitExceededError on 429', async () => {
    nock('https://api.service.com')
      .get('/users')
      .reply(429, { error: 'Rate limit exceeded' });

    try {
      await producer.listUsers();
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error).to.be.instanceOf(RateLimitExceededError);
    }
  });
});
```

**Why:**
- Error handling is critical for production code
- Verifies correct error type mapping
- Tests edge cases and failure modes
- Ensures graceful degradation

### 4. Missing nock cleanup

```typescript
// ❌ WRONG - no cleanup
describe('UserProducer', () => {
  it('should get user', async () => {
    nock('https://api.service.com')
      .get('/users/123')
      .reply(200, { id: '123' });

    const user = await producer.getUser('123');
    expect(user.id).to.be.instanceof(UUID);
  });
});

// ✅ CORRECT - cleanup after each test
describe('UserProducer', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it('should get user', async () => {
    nock('https://api.service.com')
      .get('/users/123')
      .reply(200, { id: '123' });

    const user = await producer.getUser('123');
    expect(user.id).to.be.instanceof(UUID);
  });

  it('should get another user', async () => {
    nock('https://api.service.com')
      .get('/users/456')
      .reply(200, { id: '456' });

    const user = await producer.getUser('456');
    expect(user.id).to.be.instanceof(UUID);
  });
});
```

**Why:**
- Prevents test interference
- Ensures clean state between tests
- Avoids "Nock: No match for request" errors
- Makes tests independent and reliable

### 5. Unit test Common.ts using environment variables

```typescript
// ❌ WRONG - unit test Common.ts with env vars
import { config } from 'dotenv';
import { Email } from '@zerobias-org/types-core-js';
import { newService } from '../../src';

config(); // NO! Unit tests don't use .env

export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';

export async function getConnectedInstance() {
  const connector = newService();
  await connector.connect({
    email: new Email(SERVICE_EMAIL),
    password: SERVICE_PASSWORD,
  });
  return connector;
}

// ✅ CORRECT - unit test Common.ts with nock
import * as nock from 'nock';
import { Email } from '@zerobias-org/types-core-js';
import { newService } from '../../src';
import type { ServiceConnector } from '../../src';

/**
 * Get a connected instance for unit testing.
 * Uses mocked HTTP - no real credentials needed.
 * Unit tests should NEVER depend on environment variables.
 */
export async function getConnectedInstance(): Promise<ServiceConnector> {
  nock('https://api.example.com')
    .post('/auth/login')
    .reply(200, {
      accessToken: 'test-token-123',
      expiresAt: '2025-10-02T00:00:00Z',
    });

  const connector = newService();

  await connector.connect({
    email: new Email('test@example.com'),
    password: 'testpass',
  });

  return connector;
}
```

**Why:**
- Unit tests must work without .env file
- Should be deterministic and repeatable
- Credentials belong in integration tests only
- Mocked tests don't need real values

## Validation Scripts

### Check unit test structure

```bash
# Verify unit tests exist
ls -lh test/unit/*Test.ts

# Count test suites and cases
echo "Describe blocks:"
grep -h "^describe(" test/unit/*.ts | wc -l

echo "Test cases:"
grep -h "^\s*it(" test/unit/*.ts | wc -l

echo "Error tests:"
grep -h -i "error\|404\|401\|429" test/unit/*.ts | wc -l
```

### Validate nock usage

```bash
# Check nock imports
echo "Files importing nock:"
grep -l "from ['\"]nock['\"]" test/unit/*.ts

# Check for forbidden libraries
echo "Checking for forbidden mocking libraries:"
grep -n -E "jest\.mock|sinon|fetch-mock|msw" test/unit/*.ts && \
  echo "❌ FAIL: Forbidden mocking library found" || \
  echo "✅ PASS: Only nock used"

# Check nock cleanup
echo "Files with nock.cleanAll():"
grep -l "nock.cleanAll()" test/unit/*.ts
```

### Validate Common.ts

```bash
# Check Common.ts structure
echo "Checking test/unit/Common.ts:"

# Should use nock
grep -q "import.*nock" test/unit/Common.ts && \
  echo "✅ Uses nock" || \
  echo "❌ Should import nock"

# Should NOT use dotenv or process.env
grep -E "dotenv|process\.env" test/unit/Common.ts && \
  echo "❌ FAIL: Uses env vars (forbidden in unit tests)" || \
  echo "✅ No env vars"
```

### Run unit tests

```bash
# Run unit tests (should work without .env file)
npm run test:unit

# Expected: All tests pass, no env file needed
```

## Related Rules

- **unit-test-patterns skill** ⭐ - All unit test patterns and examples
- **nock-patterns skill** ⭐ - HTTP mocking with nock (ONLY allowed library)
- **testing-core-rules skill** - General testing principles
- **failure-conditions skill** - Rule #4: Forbidden mocking libraries
- **test-fixture-patterns skill** - Test data and fixture organization

## Success Criteria

Unit test creation MUST meet ALL criteria:

- ✅ Unit test files exist in test/unit/
- ✅ Each operation has unit tests (ConnectionTest.ts + {Resource}ProducerTest.ts)
- ✅ At least 3 test cases per operation
- ✅ Both success and error cases tested
- ✅ **ONLY nock used for HTTP mocking** (CRITICAL)
- ✅ **NO jest.mock, sinon, fetch-mock, or msw** (CRITICAL)
- ✅ HTTP-level mocking (not method/function level)
- ✅ Common.ts exists with getConnectedInstance helper
- ✅ Common.ts uses nock (NO dotenv or process.env)
- ✅ nock.cleanAll() in afterEach blocks
- ✅ Proper test file naming convention
- ✅ Unit tests pass without .env file
- ✅ 100% unit test pass rate
