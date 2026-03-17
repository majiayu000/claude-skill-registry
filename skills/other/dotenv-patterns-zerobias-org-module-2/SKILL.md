---
name: dotenv-patterns
description: Environment file (.env) patterns, test data, and credential loading
---

# Environment File Patterns (.env)

## 🚨 CRITICAL RULES

### Rule #1: NEVER Commit .env Files

- .env files contain secrets
- ALWAYS in .gitignore
- Use .env.example as template
- Each developer has their own .env

```bash
# .gitignore MUST contain:
.env
.env.local
.env.*.local
```

### Rule #2: ONLY test/integration/Common.ts Reads .env

- **FORBIDDEN**: `process.env` in `src/` directory (production code)
- **ONLY EXCEPTION**: `test/integration/Common.ts` may read env vars
- **MANDATORY**: All credentials loaded via Common.ts
- Test files import from Common.ts, NEVER access process.env directly

```typescript
// ✅ CORRECT: test/integration/Common.ts ONLY
import { config } from 'dotenv';

config(); // Load .env explicitly

export const SERVICE_API_KEY = process.env.SERVICE_API_KEY || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

// ✅ CORRECT: test/integration/ServiceProducerTest.ts
import { SERVICE_API_KEY } from './Common';

// ❌ FORBIDDEN: Any src/ file
const apiKey = process.env.API_KEY; // NEVER!

// ❌ FORBIDDEN: Direct access in test files
const apiKey = process.env.SERVICE_API_KEY; // Use Common.ts instead!

// ❌ FORBIDDEN: Unit test Common.ts - NO env vars at all
// test/unit/Common.ts should NEVER use process.env
```

### Rule #3: ALL Test Values Must Be in .env

**🚨 CRITICAL: NO hardcoded test values in integration tests**

```bash
# ✅ CORRECT - Test values in .env
SERVICE_API_KEY=your-api-key
SERVICE_TEST_USER_ID=12345
SERVICE_TEST_ORGANIZATION_ID=1067
SERVICE_TEST_RESOURCE_NAME=test-resource

# ❌ WRONG - Hardcoding in test files
const userId = '12345';  // NO!
const orgId = '1067';    // NO!
```

**RULE**:
1. User gives you test values → Add to `.env` immediately
2. Export from `test/integration/Common.ts`
3. Import and use in integration tests
4. NEVER hardcode any test data values

## .env File Structure

### Location

**Create .env in module root** (same directory as package.json):

```
package/vendor/service/product/
├── .env                    ← HERE (module root)
├── package.json
├── api.yml
├── src/
└── test/
```

### Naming Conventions

**Pattern**: `{VENDOR}_{SERVICE}_{PRODUCT}_{VARIABLE_NAME}`

```bash
# Examples
GITHUB_API_TOKEN=ghp_abc123...
GITHUB_BASE_URL=https://api.github.com

AVIGILON_ALTA_ACCESS_API_KEY=your-api-key
AVIGILON_ALTA_ACCESS_EMAIL=user@example.com
AVIGILON_ALTA_ACCESS_PASSWORD=your-password

READYPLAYERME_API_TOKEN=rpm_xyz789...
READYPLAYERME_APP_ID=your-app-id
```

**Format**:
- UPPERCASE with underscores
- Vendor/service name prefix prevents conflicts
- Descriptive variable names

## Authentication Patterns

### Simple Token Authentication

```bash
# Single API token/key
SERVICE_API_TOKEN=your_token_here
SERVICE_BASE_URL=https://api.example.com
```

**Use case**: API key, bearer token, personal access token

**Example test/integration/Common.ts**:
```typescript
import { config } from 'dotenv';

config();

export const SERVICE_API_TOKEN = process.env.SERVICE_API_TOKEN || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

export function hasCredentials(): boolean {
  return !!SERVICE_API_TOKEN;
}
```

### OAuth Client Credentials

```bash
# OAuth client credentials flow
SERVICE_CLIENT_ID=your_client_id
SERVICE_CLIENT_SECRET=your_client_secret
SERVICE_BASE_URL=https://api.example.com
SERVICE_TOKEN_URL=https://api.example.com/oauth/token
```

**Use case**: OAuth 2.0 client credentials grant

**Example test/integration/Common.ts**:
```typescript
import { config } from 'dotenv';

config();

export const SERVICE_CLIENT_ID = process.env.SERVICE_CLIENT_ID || '';
export const SERVICE_CLIENT_SECRET = process.env.SERVICE_CLIENT_SECRET || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';
export const SERVICE_TOKEN_URL = process.env.SERVICE_TOKEN_URL || 'https://api.example.com/oauth/token';

export function hasCredentials(): boolean {
  return !!SERVICE_CLIENT_ID && !!SERVICE_CLIENT_SECRET;
}
```

### Basic Authentication (Email/Password)

```bash
# Email and password authentication
SERVICE_EMAIL=user@example.com
SERVICE_PASSWORD=your_password
SERVICE_BASE_URL=https://api.example.com
```

**Use case**: Email/password login, basic auth

**Example test/integration/Common.ts**:
```typescript
import { config } from 'dotenv';

config();

export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

export function hasCredentials(): boolean {
  return !!SERVICE_EMAIL && !!SERVICE_PASSWORD;
}
```

### API Key + Secret

```bash
# API key and secret pair
SERVICE_API_KEY=your_api_key
SERVICE_API_SECRET=your_api_secret
SERVICE_BASE_URL=https://api.example.com
```

**Use case**: Services requiring both key and secret (like AWS-style signing)

### Multiple Auth Methods

```bash
# Service supporting multiple auth methods
SERVICE_API_TOKEN=your_token           # Preferred method
SERVICE_EMAIL=user@example.com         # Alternative method
SERVICE_PASSWORD=your_password
SERVICE_BASE_URL=https://api.example.com
```

**Example test/integration/Common.ts**:
```typescript
import { config } from 'dotenv';

config();

// Primary auth method
export const SERVICE_API_TOKEN = process.env.SERVICE_API_TOKEN || '';

// Alternative auth method
export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';

export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

export function hasCredentials(): boolean {
  // Check if EITHER auth method is available
  return (
    !!SERVICE_API_TOKEN ||
    (!!SERVICE_EMAIL && !!SERVICE_PASSWORD)
  );
}
```

## Test Data Values Pattern

**🚨 CRITICAL: All integration test IDs/values MUST be in .env**

```bash
# Credentials
SERVICE_API_KEY=your-api-key
SERVICE_BASE_URL=https://api.example.com

# Test Data Values (MANDATORY for integration tests)
SERVICE_TEST_USER_ID=12345
SERVICE_TEST_ORGANIZATION_ID=1067
SERVICE_TEST_RESOURCE_NAME=test-resource
SERVICE_TEST_WORKSPACE_ID=ws_abc123
SERVICE_TEST_PROJECT_ID=proj_xyz789

# Optional: Test data for specific scenarios
SERVICE_TEST_ADMIN_USER_ID=admin_123
SERVICE_TEST_READONLY_USER_ID=readonly_456
```

**Example test/integration/Common.ts**:
```typescript
import { config } from 'dotenv';

config();

// Credentials
export const SERVICE_API_KEY = process.env.SERVICE_API_KEY || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

// Test Data Values
export const SERVICE_TEST_USER_ID = process.env.SERVICE_TEST_USER_ID || '';
export const SERVICE_TEST_ORGANIZATION_ID = process.env.SERVICE_TEST_ORGANIZATION_ID || '';
export const SERVICE_TEST_RESOURCE_NAME = process.env.SERVICE_TEST_RESOURCE_NAME || '';

export function hasCredentials(): boolean {
  return !!SERVICE_API_KEY;
}
```

**Example usage in integration test**:
```typescript
import { SERVICE_TEST_USER_ID, SERVICE_TEST_ORGANIZATION_ID } from './Common';

it('should retrieve user', async () => {
  const userId = SERVICE_TEST_USER_ID;  // ✅ From .env
  // NOT: const userId = '12345';  // ❌ Hardcoded

  const user = await api.getUser(userId);
  expect(user.id).to.equal(userId);
});
```

## test/integration/Common.ts Pattern

**MANDATORY structure for integration test credentials:**

```typescript
// test/integration/Common.ts - ONLY file allowed to access process.env
import { config } from 'dotenv';
import { Email } from '@zerobias-org/types-core-js';
import { LoggerEngine } from '@zerobias-org/logger';
import { newService } from '../../src';
import type { ServiceConnector } from '../../src';

// Load .env file explicitly to ensure credentials are available
config();

// Credentials
export const SERVICE_API_KEY = process.env.SERVICE_API_KEY || '';
export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

// Test Data Values - export any test IDs, names, or other values from .env
export const SERVICE_TEST_USER_ID = process.env.SERVICE_TEST_USER_ID || '';
export const SERVICE_TEST_ORGANIZATION_ID = process.env.SERVICE_TEST_ORGANIZATION_ID || '';

/**
 * Get a logger with configurable level from LOG_LEVEL env var.
 * Usage: LOG_LEVEL=debug npm run test:integration
 */
export function getLogger(name: string) {
  return LoggerEngine.root().get(name);
}

if (process.env.LOG_LEVEL) {
  switch (process.env.LOG_LEVEL) {
    case 'trace': {
      getLogger().setLevel(LogLevel.TRACE);
      break;
    }
    case 'debug': {
      getLogger().setLevel(LogLevel.DEBUG);
      break;
    }
    case 'verbose': {
      getLogger().setLevel(LogLevel.VERBOSE);
      break;
    }
    case 'info': {
      getLogger().setLevel(LogLevel.INFO);
      break;
    }
    case 'warn': {
      getLogger().setLevel(LogLevel.WARN);
      break;
    }
    case 'error': {
      getLogger().setLevel(LogLevel.ERROR);
      break;
    }
    case 'crit': {
      getLogger().setLevel(LogLevel.CRIT);
      break;
    }
    default: {
      getLogger().setLevel(LogLevel.INFO);
      break;
    }
  }
}

export function hasCredentials(): boolean {
  return !!SERVICE_API_KEY; // Or check EMAIL && PASSWORD
}

// Cached connector instance - connect once, reuse many times
let cachedConnector: ServiceConnector | null = null;

/**
 * Get a connected instance for integration testing.
 * Connects once on first call, then returns cached instance on subsequent calls.
 * Uses real credentials from .env file.
 */
export async function getConnectedInstance(): Promise<ServiceConnector> {
  if (cachedConnector) {
    return cachedConnector;
  }

  const connector = newService();

  await connector.connect({
    apiKey: SERVICE_API_KEY,
    baseUrl: SERVICE_BASE_URL,
  });

  cachedConnector = connector;
  return connector;
}
```

**Why explicit config()?**
- .mocharc.json `"require": ["dotenv/config"]` loads dotenv, BUT
- Environment variables in Common.ts are evaluated at module load time
- Explicit `config()` ensures .env is loaded BEFORE env vars are accessed
- This guarantees integration tests can detect credentials properly

## Local vs CI Environment Variables

### Local Development (.env file)

```bash
# .env - Local developer credentials
SERVICE_API_KEY=your-local-api-key
SERVICE_EMAIL=developer@example.com
SERVICE_PASSWORD=local-dev-password
```

### CI/CD Environment (GitHub Actions, etc.)

```yaml
# .github/workflows/test.yml
env:
  SERVICE_API_KEY: ${{ secrets.SERVICE_API_KEY }}
  SERVICE_EMAIL: ${{ secrets.SERVICE_EMAIL }}
  SERVICE_PASSWORD: ${{ secrets.SERVICE_PASSWORD }}
```

**Benefits**:
- Local: .env file for developers
- CI: GitHub Secrets or environment variables
- Same variable names work in both environments
- test/integration/Common.ts works identically

## .env.example Template

**ALWAYS provide .env.example for documentation:**

```bash
# .env.example - Template for setting up credentials

# Authentication credentials
SERVICE_API_KEY=your-api-key-here
SERVICE_BASE_URL=https://api.example.com

# Test Data Values (for integration tests)
SERVICE_TEST_USER_ID=your-test-user-id
SERVICE_TEST_ORGANIZATION_ID=your-test-org-id
SERVICE_TEST_RESOURCE_NAME=test-resource-name

# Optional: Debugging
LOG_LEVEL=info  # Set to 'debug' for verbose test output
```

**Developer setup**:
```bash
# Copy template and fill in real values
cp .env.example .env
vim .env  # Add your credentials
```

## dotenv Setup for Integration Tests

**Step 1: Install dotenv**

```bash
npm install --save-dev dotenv
```

**Step 2: Configure .mocharc.json**

```json
{
  "extension": ["ts"],
  "require": ["ts-node/register", "dotenv/config"]
}
```

**Step 3: Load dotenv explicitly in test/integration/Common.ts**

```typescript
import { config } from 'dotenv';

// Load .env file explicitly
config();

export const SERVICE_API_KEY = process.env.SERVICE_API_KEY || '';
```

**Step 4: Use in integration tests**

```typescript
import { hasCredentials, SERVICE_API_KEY } from './Common';

describe('Service Integration Tests', function () {
  before(function () {
    if (!hasCredentials()) {
      this.skip(); // Skip entire suite if no credentials
    }
  });

  it('should connect with real API', async function () {
    // Test with real credentials from .env
  });
});
```

## Validation

### Check .env Configuration

```bash
# Verify .env exists
[ -f .env ] && echo "✅ .env exists" || echo "❌ Missing .env - create it!"

# Check .env is in .gitignore
grep -q "^\.env$" .gitignore && echo "✅ .env in .gitignore" || echo "❌ Add .env to .gitignore!"

# Verify required variables are set (example)
grep -q "SERVICE_API_KEY" .env && echo "✅ SERVICE_API_KEY present" || echo "❌ Missing SERVICE_API_KEY"
```

### Validate test/integration/Common.ts Pattern

```bash
# Check dotenv is imported and configured
grep -E "import.*config.*from ['\"]dotenv['\"]" test/integration/Common.ts && echo "✅ dotenv imported" || echo "❌ Missing dotenv import"

grep -E "^config\(\)" test/integration/Common.ts && echo "✅ config() called" || echo "❌ Missing config() call"

# Check credentials are exported
grep -E "export const.*=.*process\.env\." test/integration/Common.ts && echo "✅ Exports env vars" || echo "❌ No env var exports"

# Check hasCredentials() function exists
grep -E "export function hasCredentials" test/integration/Common.ts && echo "✅ hasCredentials() present" || echo "❌ Missing hasCredentials()"
```

### Check NO process.env in src/ (Security Rule #2)

```bash
# Verify no environment variables in production code
grep -r "process\.env" src/ && echo "❌ Found process.env in src/! FORBIDDEN!" || echo "✅ No process.env in src/"

# Verify no environment variables in unit test Common.ts
grep "process\.env" test/unit/Common.ts 2>/dev/null && echo "❌ Found process.env in unit test Common.ts! FORBIDDEN!" || echo "✅ No process.env in unit tests"
```

### Check NO hardcoded test values

```bash
# Check for common hardcoded ID patterns in integration tests
if grep -E "(const|let|var) [a-zA-Z]*[Ii]d = ['\"][0-9]+['\"]" test/integration/*.ts 2>/dev/null | grep -v Common.ts; then
  echo "❌ Found hardcoded test values in integration tests!"
  echo "   ALL test values must be in .env and imported from Common.ts"
else
  echo "✅ No hardcoded test values found"
fi

# Verify test data constants exported from Common.ts if integration tests exist
if [ -d "test/integration" ] && [ -f "test/integration/Common.ts" ]; then
  if grep -E "api\.(get|list|update|delete)\(" test/integration/*.ts 2>/dev/null | grep -v "Common.ts" > /dev/null; then
    if ! grep -E "export const.*TEST.*=" test/integration/Common.ts > /dev/null 2>&1; then
      echo "⚠️  WARNING: Integration tests may need test data constants exported from Common.ts"
    else
      echo "✅ Test data constants exported from Common.ts"
    fi
  fi
fi
```

## Security Checklist

Before committing:

- [ ] .env is in .gitignore
- [ ] No .env files committed to git
- [ ] .env.example created (no real credentials)
- [ ] No process.env in src/ directory
- [ ] ONLY test/integration/Common.ts reads process.env
- [ ] No credentials hardcoded in code
- [ ] No credentials in error messages or logs
- [ ] All test values in .env (no hardcoded IDs in tests)

## Documentation in USERGUIDE.md

**Include this section in every module's USERGUIDE.md:**

```markdown
## Setting Up Credentials for Testing

### Local Development

Create a `.env` file in the module root:

\`\`\`bash
# Copy the template
cp .env.example .env

# Edit with your credentials
SERVICE_API_KEY=your-api-key
SERVICE_BASE_URL=https://api.example.com

# Add test data values for integration tests
SERVICE_TEST_USER_ID=your-test-user-id
SERVICE_TEST_ORGANIZATION_ID=your-test-org-id
\`\`\`

### Running Tests

The test suite automatically loads credentials using `dotenv`:

\`\`\`bash
# Run all tests (integration tests skip if no credentials)
npm test

# Run integration tests with debug logging
LOG_LEVEL=debug npm run test:integration
\`\`\`

### CI/CD Setup

Set environment variables in your CI system (GitHub Actions secrets, etc.):

- `SERVICE_API_KEY` - API authentication key
- `SERVICE_TEST_USER_ID` - Test user ID for integration tests
- `SERVICE_TEST_ORGANIZATION_ID` - Test organization ID
```

## Common Patterns

### Multiple Environments

```bash
# .env.development
SERVICE_BASE_URL=https://dev-api.example.com
SERVICE_API_KEY=dev-key

# .env.staging
SERVICE_BASE_URL=https://staging-api.example.com
SERVICE_API_KEY=staging-key

# .env.production (NEVER commit!)
SERVICE_BASE_URL=https://api.example.com
SERVICE_API_KEY=prod-key
```

**Load specific environment**:
```typescript
import { config } from 'dotenv';

const environment = process.env.NODE_ENV || 'development';
config({ path: `.env.${environment}` });
```

### Debug Logging Control

```bash
# .env
LOG_LEVEL=info  # Default: only info/warn/error
# LOG_LEVEL=debug  # Uncomment for verbose output
```

**Usage**:
```bash
# Run integration tests with debug logging
LOG_LEVEL=debug npm run test:integration
```

## Success Criteria

Environment file setup MUST meet all criteria:

- ✅ .env file created in module root
- ✅ .env is in .gitignore
- ✅ .env.example template provided
- ✅ Credentials use consistent naming convention (VENDOR_SERVICE_VARIABLE)
- ✅ test/integration/Common.ts is ONLY file accessing process.env
- ✅ Explicit config() call in Common.ts
- ✅ hasCredentials() function implemented
- ✅ All test data values in .env (no hardcoded test IDs)
- ✅ Integration tests export test values from Common.ts
- ✅ dotenv installed and configured in .mocharc.json
- ✅ No process.env in src/ directory (CRITICAL)
- ✅ No process.env in test/unit/Common.ts (unit tests don't use env vars)
- ✅ Documentation in USERGUIDE.md
