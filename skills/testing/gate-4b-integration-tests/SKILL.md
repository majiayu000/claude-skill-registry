---
name: gate-4b-integration-tests
description: Gate 4b validation: Integration test creation and no-hardcoded-values enforcement
---

### Gate 4b: Integration Test Creation

**Purpose:** Validate integration test quality, test data management, and credential handling

**STOP AND CHECK:**
```bash
# 1. Integration test files exist
if ! ls test/integration/*Test.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4b FAILED: No integration test files found"
  echo "   Create test/integration/{Resource}ProducerTest.ts"
  echo "   See integration-test-patterns skill"
  exit 1
fi

TEST_FILE_COUNT=$(ls test/integration/*Test.ts 2>/dev/null | wc -l)
echo "✅ Found $TEST_FILE_COUNT integration test file(s)"

# 2. Test suites exist with proper structure
DESCRIBE_COUNT=$(grep -h "^describe(" test/integration/*.ts 2>/dev/null | wc -l)
if [ "$DESCRIBE_COUNT" -lt 1 ]; then
  echo "❌ Gate 4b FAILED: No describe blocks found"
  echo "   Integration tests must have describe blocks"
  exit 1
fi
echo "✅ Found $DESCRIBE_COUNT describe block(s)"

# 3. Multiple test cases (3+ per operation)
IT_COUNT=$(grep -h "^\s*it(" test/integration/*.ts 2>/dev/null | wc -l)
if [ "$IT_COUNT" -lt 3 ]; then
  echo "❌ Gate 4b FAILED: Insufficient test cases (found $IT_COUNT, need 3+)"
  echo "   Each operation needs multiple test cases"
  exit 1
fi
echo "✅ Found $IT_COUNT test case(s)"

# 4. CRITICAL: NO hardcoded test values
echo "Checking for hardcoded test values..."
HARDCODED_IDS=$(grep -h -n -E "(const|let|var) [a-zA-Z_][a-zA-Z0-9_]*[Ii]d = ['\"][0-9a-zA-Z_-]+['\"]" test/integration/*.ts 2>/dev/null | grep -v "Common.ts" || true)

if [ -n "$HARDCODED_IDS" ]; then
  echo "❌ Gate 4b FAILED: Hardcoded test values found"
  echo "   ALL test values must be in .env and imported from Common.ts"
  echo ""
  echo "Found hardcoded values:"
  echo "$HARDCODED_IDS"
  echo ""
  echo "Fix:"
  echo "  1. Add to .env file:"
  echo "     SERVICE_TEST_USER_ID=12345"
  echo "     SERVICE_TEST_ORGANIZATION_ID=1067"
  echo ""
  echo "  2. Export from test/integration/Common.ts:"
  echo "     export const SERVICE_TEST_USER_ID = process.env.SERVICE_TEST_USER_ID || '';"
  echo ""
  echo "  3. Import in test files:"
  echo "     import { SERVICE_TEST_USER_ID } from './Common';"
  echo "     const userId = SERVICE_TEST_USER_ID;"
  echo ""
  echo "See env-file-patterns skill Rule #3"
  exit 1
fi
echo "✅ No hardcoded test values"

# 5. CRITICAL: Verify Common.ts exists and exports test data
if [ ! -f "test/integration/Common.ts" ]; then
  echo "❌ Gate 4b FAILED: test/integration/Common.ts missing"
  echo "   Create Common.ts with:"
  echo "   - Credential loading from .env"
  echo "   - Test data exports (TEST_USER_ID, etc.)"
  echo "   - getConnectedInstance() helper"
  echo "   - hasCredentials() check"
  echo ""
  echo "See integration-test-patterns skill for template"
  exit 1
fi

# Check Common.ts has test data exports
if ! grep -E "export const.*TEST.*=" test/integration/Common.ts > /dev/null 2>&1; then
  echo "⚠️  WARNING: Common.ts should export test data constants"
  echo "   Example: export const TEST_USER_ID = process.env.TEST_USER_ID || '';"
  echo "   See env-file-patterns skill"
fi

# Check Common.ts loads credentials
if ! grep -q "process.env" test/integration/Common.ts; then
  echo "⚠️  WARNING: Common.ts should load credentials from process.env"
fi

# Check Common.ts has getConnectedInstance
if ! grep -q "getConnectedInstance" test/integration/Common.ts; then
  echo "❌ Gate 4b FAILED: Common.ts missing getConnectedInstance() helper"
  echo "   Add getConnectedInstance() function that:"
  echo "   - Connects using real credentials"
  echo "   - Caches connection instance"
  echo "   - Returns connected instance for tests"
  exit 1
fi

# Check Common.ts has hasCredentials
if ! grep -q "hasCredentials" test/integration/Common.ts; then
  echo "⚠️  WARNING: Common.ts should have hasCredentials() function"
  echo "   Used to skip tests when credentials unavailable"
fi

echo "✅ Common.ts properly structured"

# 6. Verify .env file exists
if [ ! -f ".env" ]; then
  echo "⚠️  WARNING: .env file missing"
  echo "   Create .env with test credentials and data"
  echo "   See env-file-patterns skill"
  echo ""
  echo "Example .env:"
  echo "  SERVICE_API_KEY=your-api-key"
  echo "  SERVICE_TEST_USER_ID=12345"
  echo "  SERVICE_TEST_ORGANIZATION_ID=1067"
fi

# 7. Verify tests import from Common.ts
TEST_FILES_WITHOUT_COMMON=$(grep -L "from.*['\"]\.\/Common['\"]" test/integration/*Test.ts 2>/dev/null || true)
if [ -n "$TEST_FILES_WITHOUT_COMMON" ]; then
  echo "⚠️  WARNING: Some test files don't import from Common.ts:"
  echo "$TEST_FILES_WITHOUT_COMMON"
  echo "   Tests should import credentials and test data from Common.ts"
fi

# 8. Verify tests check hasCredentials
if ! grep -r "hasCredentials()" test/integration/*.ts > /dev/null 2>&1; then
  echo "⚠️  WARNING: Tests should check hasCredentials() in before() hook"
  echo "   Add:"
  echo "     before(function () {"
  echo "       if (!hasCredentials()) {"
  echo "         this.skip();"
  echo "       }"
  echo "     });"
fi

# 9. Check for debug logging (MANDATORY)
LOGGER_IMPORTS=$(grep -h -c "getLogger" test/integration/*Test.ts 2>/dev/null | awk '{s+=$1} END {print s}')
if [ "$LOGGER_IMPORTS" -lt 1 ]; then
  echo "❌ Gate 4b FAILED: No debug logging found in integration tests"
  echo "   Debug logging is MANDATORY for integration tests"
  echo ""
  echo "Add to each test file:"
  echo "  import { getLogger } from './Common';"
  echo "  const logger = getLogger('{Resource}ProducerTest');"
  echo ""
  echo "Log operations:"
  echo "  logger.debug('api.getUser(id)');"
  echo "  const user = await api.getUser(userId);"
  echo "  logger.debug('→', JSON.stringify(user, null, 2));"
  echo ""
  echo "See integration-test-patterns skill Rule #3"
  exit 1
fi

DEBUG_LOGS=$(grep -h "logger\.debug" test/integration/*Test.ts 2>/dev/null | wc -l)
if [ "$DEBUG_LOGS" -lt 2 ]; then
  echo "⚠️  WARNING: Insufficient debug logging (found $DEBUG_LOGS statements)"
  echo "   Log BEFORE and AFTER each API operation"
fi
echo "✅ Debug logging present ($DEBUG_LOGS statements)"

# 10. Verify NO nock in integration tests (should use real API)
if grep -h "from ['\"]nock['\"]" test/integration/*.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4b FAILED: nock found in integration tests"
  echo "   Integration tests must use REAL API calls, not mocks"
  echo ""
  echo "Found nock imports:"
  grep -n "from ['\"]nock['\"]" test/integration/*.ts
  echo ""
  echo "Fix: Remove nock - integration tests should call real API"
  exit 1
fi
echo "✅ No nock (using real API calls)"

# 11. Check test file naming convention
for file in test/integration/*Test.ts; do
  if [ -f "$file" ]; then
    basename=$(basename "$file")
    if [[ ! "$basename" =~ ^[A-Z][a-zA-Z]*Test\.ts$ ]] && [[ "$basename" != "Common.ts" ]]; then
      echo "⚠️  WARNING: Incorrect test file naming: $basename"
      echo "   Should be: {Resource}ProducerTest.ts or ConnectionTest.ts"
    fi
  fi
done

# 12. Verify dotenv installed and configured
if [ -f "package.json" ]; then
  if ! grep -q "\"dotenv\"" package.json; then
    echo "⚠️  WARNING: dotenv not in package.json dependencies"
    echo "   Run: npm install --save-dev dotenv"
  fi
fi

if [ -f ".mocharc.json" ]; then
  if ! grep -q "dotenv/config" .mocharc.json; then
    echo "⚠️  WARNING: dotenv not configured in .mocharc.json"
    echo "   Add to .mocharc.json:"
    echo "     \"require\": [\"ts-node/register\", \"dotenv/config\"]"
  fi
fi

echo ""
echo "✅ Gate 4b: Integration Test Creation - PASSED"
```

**PROCEED ONLY IF:**
- ✅ Integration test file(s) exist in test/integration/
- ✅ Test suites have describe blocks
- ✅ At least 3 test cases per operation
- ✅ **NO hardcoded test values** (CRITICAL)
- ✅ **ALL test data from .env via Common.ts** (CRITICAL)
- ✅ Common.ts exists with getConnectedInstance, hasCredentials, and test data exports
- ✅ .env file exists with credentials and test data
- ✅ Tests import from Common.ts
- ✅ Tests check hasCredentials() in before() hook
- ✅ **Debug logging present** (MANDATORY)
- ✅ NO nock or mocking (real API calls only)
- ✅ dotenv installed and configured

**IF FAILED:**
- Integration tests are MANDATORY
- Fix hardcoded values immediately
- See integration-test-patterns skill for correct patterns
- See env-file-patterns skill for .env structure

## Common Failures

### 1. Hardcoded test values

```typescript
// ❌ WRONG - hardcoded IDs
describe('UserProducer Integration', function () {
  it('should retrieve user', async () => {
    const userId = '12345';  // HARDCODED - NO!
    const groupId = 'abc-def-ghi';  // HARDCODED - NO!

    const user = await userApi.getUser(userId);
    expect(user.id).to.equal(userId);
  });
});

// ✅ CORRECT - from .env via Common.ts
// .env file:
// SERVICE_TEST_USER_ID=12345
// SERVICE_TEST_GROUP_ID=abc-def-ghi

// test/integration/Common.ts:
export const TEST_USER_ID = process.env.SERVICE_TEST_USER_ID || '';
export const TEST_GROUP_ID = process.env.SERVICE_TEST_GROUP_ID || '';

// test/integration/UserProducerTest.ts:
import { TEST_USER_ID, TEST_GROUP_ID } from './Common';

describe('UserProducer Integration', function () {
  it('should retrieve user', async () => {
    const userId = TEST_USER_ID;  // From .env
    const groupId = TEST_GROUP_ID;  // From .env

    const user = await userApi.getUser(userId);
    expect(user.id).to.equal(userId);
  });
});
```

**Why:**
- Test values are configuration, not code
- Different developers may need different test IDs
- Makes tests portable across environments
- Easy to update without touching code
- Consistent with credential management

### 2. Missing Common.ts exports

```typescript
// ❌ WRONG - Common.ts missing test data exports
import { config } from 'dotenv';
import { Email } from '@auditmation/types-core-js';
import { newService } from '../../src';

config();

export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';

export function hasCredentials(): boolean {
  return !!SERVICE_EMAIL && !!SERVICE_PASSWORD;
}

export async function getConnectedInstance() {
  // ... connection logic
}

// ✅ CORRECT - Common.ts with test data exports
import { config } from 'dotenv';
import { Email } from '@auditmation/types-core-js';
import { getLogger as getLoggerBase } from '@auditmation/util-logger';
import { newService } from '../../src';
import type { ServiceConnector } from '../../src';

config();

// Credentials
export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';

// Test data values - export ANY test IDs, names, or other values
export const TEST_USER_ID = process.env.SERVICE_TEST_USER_ID || '';
export const TEST_ORGANIZATION_ID = process.env.SERVICE_TEST_ORGANIZATION_ID || '';
export const TEST_RESOURCE_NAME = process.env.SERVICE_TEST_RESOURCE_NAME || '';

const LOG_LEVEL = (process.env.LOG_LEVEL || 'info') as string;

export function getLogger(name: string) {
  return getLoggerBase(name, {}, LOG_LEVEL);
}

export function hasCredentials(): boolean {
  return !!SERVICE_EMAIL && !!SERVICE_PASSWORD;
}

let cachedConnector: ServiceConnector | null = null;

export async function getConnectedInstance(): Promise<ServiceConnector> {
  if (cachedConnector) {
    return cachedConnector;
  }

  const connector = newService();

  await connector.connect({
    email: new Email(SERVICE_EMAIL),
    password: SERVICE_PASSWORD,
  });

  cachedConnector = connector;
  return connector;
}
```

**Why:**
- Centralizes all test configuration
- Makes test data visible and manageable
- Ensures consistency across test files
- Easy to add new test data values

### 3. Missing .env file

```bash
# ❌ WRONG - no .env file
# Tests try to run but have no credentials or test data

# ✅ CORRECT - .env file exists in module root
# .env
SERVICE_EMAIL=test@example.com
SERVICE_PASSWORD=test-password
SERVICE_API_KEY=your-api-key

# Test data values
SERVICE_TEST_USER_ID=12345
SERVICE_TEST_ORGANIZATION_ID=1067
SERVICE_TEST_RESOURCE_NAME=test-resource
SERVICE_TEST_WORKSPACE_ID=ws_abc123

# Optional: Debug logging
LOG_LEVEL=info  # Set to 'debug' for verbose output
```

**Usage:**
```bash
# Run integration tests with debug logging
LOG_LEVEL=debug npm run test:integration
```

### 4. No debug logging

```typescript
// ❌ WRONG - no logging
import { expect } from 'chai';
import { getConnectedInstance, hasCredentials, TEST_USER_ID } from './Common';

describe('UserProducer Integration', function () {
  before(function () {
    if (!hasCredentials()) {
      this.skip();
    }
  });

  it('should get user', async () => {
    const connector = await getConnectedInstance();
    const userApi = connector.getUserApi();

    const user = await userApi.getUser(TEST_USER_ID);
    expect(user).toBeDefined();
  });
});

// ✅ CORRECT - debug logging before/after operations
import { expect } from 'chai';
import {
  getConnectedInstance,
  hasCredentials,
  getLogger,
  TEST_USER_ID
} from './Common';

const logger = getLogger('UserProducerTest');

describe('UserProducer Integration', function () {
  this.timeout(30000);

  before(function () {
    if (!hasCredentials()) {
      this.skip();
    }
  });

  it('should get user', async () => {
    logger.debug('getConnectedInstance()');
    const connector = await getConnectedInstance();

    const userApi = connector.getUserApi();

    logger.debug('userApi.getUser(userId)', { userId: TEST_USER_ID });
    const user = await userApi.getUser(TEST_USER_ID);
    logger.debug('→', JSON.stringify(user, null, 2));

    expect(user).toBeDefined();
    expect(user.id).to.equal(TEST_USER_ID);
  });
});
```

**Run with debug output:**
```bash
LOG_LEVEL=debug npm run test:integration
```

**Why:**
- Visible when log level set to debug
- Shows exact operation calls with parameters
- Shows complete API responses for debugging
- Helps diagnose integration issues without re-running tests
- MANDATORY for integration tests

### 5. Using nock in integration tests

```typescript
// ❌ WRONG - mocking in integration tests
import * as nock from 'nock';
import { expect } from 'chai';

describe('UserProducer Integration', function () {
  it('should get user', async () => {
    // NO! Integration tests should NOT mock
    nock('https://api.service.com')
      .get('/users/123')
      .reply(200, { id: '123' });

    const user = await userApi.getUser('123');
    expect(user).toBeDefined();
  });
});

// ✅ CORRECT - real API calls
import { expect } from 'chai';
import {
  getConnectedInstance,
  hasCredentials,
  getLogger,
  TEST_USER_ID
} from './Common';

const logger = getLogger('UserProducerTest');

describe('UserProducer Integration', function () {
  this.timeout(30000);

  before(function () {
    if (!hasCredentials()) {
      this.skip();
    }
  });

  it('should get user', async () => {
    logger.debug('getConnectedInstance()');
    const connector = await getConnectedInstance();

    const userApi = connector.getUserApi();

    logger.debug('userApi.getUser(userId)', { userId: TEST_USER_ID });
    const user = await userApi.getUser(TEST_USER_ID);  // Real API call
    logger.debug('→', JSON.stringify(user, null, 2));

    expect(user).toBeDefined();
    expect(user.id).to.equal(TEST_USER_ID);
  });
});
```

**Why:**
- Integration tests verify real API behavior
- Catches network, authentication, and API-specific issues
- Tests actual response structures
- Validates real-world scenarios

### 6. Missing hasCredentials check

```typescript
// ❌ WRONG - no credential check
describe('UserProducer Integration', function () {
  it('should get user', async () => {
    // Fails if no .env file - no graceful skip
    const connector = await getConnectedInstance();
    const user = await userApi.getUser(TEST_USER_ID);
    expect(user).toBeDefined();
  });
});

// ✅ CORRECT - graceful skip when no credentials
import { hasCredentials, getConnectedInstance, getLogger } from './Common';

const logger = getLogger('UserProducerTest');

describe('UserProducer Integration', function () {
  this.timeout(30000);

  before(function () {
    if (!hasCredentials()) {
      logger.info('Skipping: no credentials in .env');
      this.skip();
    }
  });

  it('should get user', async () => {
    logger.debug('getConnectedInstance()');
    const connector = await getConnectedInstance();

    const userApi = connector.getUserApi();

    logger.debug('userApi.getUser(userId)');
    const user = await userApi.getUser(TEST_USER_ID);
    logger.debug('→', JSON.stringify(user, null, 2));

    expect(user).toBeDefined();
  });
});
```

**Why:**
- Allows tests to run in environments without credentials
- Provides clear message about why tests skipped
- Prevents confusing test failures
- Professional test suite behavior

## Validation Scripts

### Check integration test structure

```bash
# Verify integration tests exist
ls -lh test/integration/*Test.ts

# Count test suites and cases
echo "Describe blocks:"
grep -h "^describe(" test/integration/*.ts | wc -l

echo "Test cases:"
grep -h "^\s*it(" test/integration/*.ts | wc -l

echo "Debug logging statements:"
grep -h "logger.debug" test/integration/*.ts | wc -l
```

### Validate test data management

```bash
# Check for hardcoded test values (should find none)
echo "Checking for hardcoded test values:"
grep -n -E "(const|let|var) [a-zA-Z]*[Ii]d = ['\"][0-9a-zA-Z-]+['\"]" \
  test/integration/*.ts | grep -v "Common.ts" && \
  echo "❌ FAIL: Found hardcoded values" || \
  echo "✅ PASS: No hardcoded values"

# Check Common.ts exports test data
echo "Checking Common.ts test data exports:"
grep -E "export const.*TEST.*=" test/integration/Common.ts && \
  echo "✅ Test data exported" || \
  echo "⚠️  WARNING: No test data exports"

# Check .env file exists
[ -f ".env" ] && \
  echo "✅ .env file exists" || \
  echo "⚠️  WARNING: .env file missing"
```

### Validate credential loading

```bash
# Check Common.ts structure
echo "Checking test/integration/Common.ts:"

# Should load from process.env
grep -q "process.env" test/integration/Common.ts && \
  echo "✅ Loads from process.env" || \
  echo "❌ Should load from process.env"

# Should have getConnectedInstance
grep -q "getConnectedInstance" test/integration/Common.ts && \
  echo "✅ Has getConnectedInstance" || \
  echo "❌ Missing getConnectedInstance"

# Should have hasCredentials
grep -q "hasCredentials" test/integration/Common.ts && \
  echo "✅ Has hasCredentials" || \
  echo "❌ Missing hasCredentials"

# Should have getLogger
grep -q "getLogger" test/integration/Common.ts && \
  echo "✅ Has getLogger" || \
  echo "⚠️  WARNING: Should have getLogger"
```

### Validate no mocking

```bash
# Check for nock (should not be in integration tests)
echo "Checking for nock in integration tests:"
grep -l "from ['\"]nock['\"]" test/integration/*.ts && \
  echo "❌ FAIL: nock found (should use real API)" || \
  echo "✅ PASS: No nock (using real API)"
```

### Run integration tests

```bash
# Run integration tests (requires .env)
npm run test:integration

# Run with debug logging
LOG_LEVEL=debug npm run test:integration

# Expected: Tests pass with real API or skip gracefully if no credentials
```

## Related Rules

- **integration-test-patterns skill** ⭐ - All integration test patterns and examples
- **env-file-patterns skill** ⭐ - .env file structure and test data management
- **testing-core-rules skill** - General testing principles
- **failure-conditions skill** - Rule #11: No hardcoded values in integration tests
- **security skill** - Credential handling best practices

## Success Criteria

Integration test creation MUST meet ALL criteria:

- ✅ Integration test files exist in test/integration/
- ✅ Each operation has integration tests (ConnectionTest.ts + {Resource}ProducerTest.ts)
- ✅ At least 3 test cases per operation
- ✅ Both success and error cases tested
- ✅ **NO hardcoded test values** (CRITICAL)
- ✅ **ALL test data from .env via Common.ts** (CRITICAL)
- ✅ Common.ts exists with:
  - getConnectedInstance() helper with caching
  - hasCredentials() check
  - getLogger() helper
  - Test data constant exports (TEST_USER_ID, etc.)
  - Credential constant exports
- ✅ .env file exists with credentials and test data
- ✅ Tests import from Common.ts
- ✅ Tests check hasCredentials() in before() hook
- ✅ **Debug logging present** (logger.debug before/after operations)
- ✅ NO nock or mocking (real API calls only)
- ✅ dotenv installed and configured in .mocharc.json
- ✅ Proper test file naming convention
- ✅ Tests skip gracefully when no credentials
- ✅ 100% integration test pass rate (when credentials available)
