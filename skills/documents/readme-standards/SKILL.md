---
name: readme-standards
description: README template structure and required sections
---

# README Template Rules

## 🚨 CRITICAL RULES

### 1. Required Sections
Every module README/USERGUIDE.md MUST include these sections in this order:
- Installation
- Usage
- Authentication
- Operations
- Examples
- Testing

**Missing any section = FAIL**

### 2. Code Example Quality
- ALL code examples MUST be working, tested TypeScript code
- Type-safe imports from the module
- Clear, explanatory comments
- Realistic but sanitized data (NO real credentials)
- Include error handling in examples

### 3. Never Include Real Credentials
- ALWAYS use placeholder/example values
- Mark clearly as examples: `your-email@example.com`, `your-password-here`
- Link to credential acquisition guide
- Use .env file pattern for credential management

## 🟡 STANDARD RULES

### Installation Section

**Must include:**
```markdown
## Installation

\`\`\`bash
npm install @auditmation/connector-[vendor]-[service]
\`\`\`

### Prerequisites
- Node.js 14.x or higher
- npm or yarn
- Valid [Service Name] account with API access
\`\`\`

**Key elements:**
- Exact npm package name
- Node version requirements
- Any peer dependencies
- Account/permission requirements

### Usage Section

**Must include:**
1. Factory function import
2. Creating connector instance
3. Basic connection example
4. Simple operation example

**Template:**
```markdown
## Usage

### Basic Setup

\`\`\`typescript
import { newServiceName } from '@auditmation/connector-vendor-service';

// Create connector instance
const connector = newServiceName();
\`\`\`

### Connecting

\`\`\`typescript
import { ConnectionProfile } from '@auditmation/connector-vendor-service';

const profile: ConnectionProfile = {
  email: process.env.SERVICE_EMAIL!,
  password: process.env.SERVICE_PASSWORD!
  // Add other required credentials
};

const connectionState = await connector.connect(profile);
console.log('Connected! Token expires in:', connectionState.expiresIn, 'seconds');
\`\`\`

### Basic Operation

\`\`\`typescript
// Get API for specific resource
const userApi = connector.getUserApi();

// List resources
const users = await userApi.listUsers();
console.log('Found', users.length, 'users');
\`\`\`
\`\`\`

### Authentication Section

**Must include:**
1. Supported authentication methods
2. How to obtain credentials
3. .env file setup
4. Link to credential guide (USERGUIDE.md or external docs)

**Template:**
```markdown
## Authentication

### Supported Methods
- **Username/Password** - Basic authentication with email and password
- **TOTP (Optional)** - Time-based One-Time Password if MFA is enabled

### Obtaining Credentials

See [USERGUIDE.md](./USERGUIDE.md) for detailed instructions on obtaining credentials.

Quick summary:
1. Log into [Service Dashboard](https://service.example.com)
2. Navigate to Settings > API
3. Create API credentials or use your login credentials

### Environment Variables

Create a `.env` file in your project root:

\`\`\`env
SERVICE_EMAIL=your-email@example.com
SERVICE_PASSWORD=your-password-here
SERVICE_TOTP_SECRET=your-totp-secret  # Optional, if MFA enabled
\`\`\`

**Security Note:** Never commit `.env` files to version control. Add `.env` to your `.gitignore`.
\`\`\`

### Operations Section

**Must include:**
1. List of ALL available operations
2. Brief description of each
3. Grouped by resource type (Producer API)
4. Links to examples or code

**Template:**
```markdown
## Operations

This connector supports the following operations:

### User Management (UserApi)
- `listUsers()` - Retrieve all users
- `getUser(id)` - Get specific user by ID
- `createUser(data)` - Create new user
- `updateUser(id, data)` - Update existing user
- `deleteUser(id)` - Delete user

### Access Control (AcuApi)
- `listAcus()` - List all access control units
- `getAcu(id)` - Get specific ACU by ID
- `unlockAcu(id)` - Remotely unlock ACU

### Groups (GroupApi)
- `listGroups()` - List all groups
- `getGroup(id)` - Get specific group
- `addUserToGroup(groupId, userId)` - Add user to group

See the [Examples](#examples) section for usage examples.
\`\`\`

### Examples Section

**Must include:**
1. Complete, runnable examples
2. Error handling examples
3. Common use cases
4. Multiple examples showing different operations

**Template:**
```markdown
## Examples

### List All Users

\`\`\`typescript
import { newServiceName } from '@auditmation/connector-vendor-service';

async function listAllUsers() {
  const connector = newServiceName();

  try {
    // Connect
    await connector.connect({
      email: process.env.SERVICE_EMAIL!,
      password: process.env.SERVICE_PASSWORD!
    });

    // Get User API
    const userApi = connector.getUserApi();

    // List users
    const users = await userApi.listUsers();

    console.log('Users:');
    users.forEach(user => {
      console.log(`- ${user.name} (${user.email})`);
    });

    // Always disconnect when done
    await connector.disconnect();
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

listAllUsers();
\`\`\`

### Create and Update User

\`\`\`typescript
async function createAndUpdateUser() {
  const connector = newServiceName();

  try {
    await connector.connect({
      email: process.env.SERVICE_EMAIL!,
      password: process.env.SERVICE_PASSWORD!
    });

    const userApi = connector.getUserApi();

    // Create user
    const newUser = await userApi.createUser({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com'
    });
    console.log('Created user:', newUser.id);

    // Update user
    const updated = await userApi.updateUser(newUser.id, {
      firstName: 'Jane'
    });
    console.log('Updated user:', updated.firstName);

    await connector.disconnect();
  } catch (error) {
    console.error('Error:', error.message);
  }
}
\`\`\`

### Error Handling

\`\`\`typescript
import {
  InvalidCredentialsError,
  NoSuchObjectError,
  RateLimitExceededError
} from '@auditmation/types-core-js';

async function handleErrors() {
  const connector = newServiceName();

  try {
    await connector.connect({ /* credentials */ });
    const userApi = connector.getUserApi();

    const user = await userApi.getUser('non-existent-id');
  } catch (error) {
    if (error instanceof InvalidCredentialsError) {
      console.error('Invalid credentials provided');
    } else if (error instanceof NoSuchObjectError) {
      console.error('User not found');
    } else if (error instanceof RateLimitExceededError) {
      console.error('Rate limit exceeded, please wait');
    } else {
      console.error('Unexpected error:', error);
    }
  } finally {
    await connector.disconnect();
  }
}
\`\`\`
\`\`\`

### Testing Section

**Must include:**
1. How to run tests
2. Environment setup for tests
3. Required test credentials
4. What tests cover

**Template:**
```markdown
## Testing

### Running Tests

\`\`\`bash
# Run all tests
npm test

# Run specific test suite
npm test -- --testPathPattern=User

# Run with coverage
npm test -- --coverage
\`\`\`

### Test Environment Setup

Tests require valid credentials. Create a `.env.test` file:

\`\`\`env
SERVICE_EMAIL=your-test-account@example.com
SERVICE_PASSWORD=your-test-password
SERVICE_TOTP_SECRET=your-test-totp-secret  # Optional
\`\`\`

**Important:** Use a dedicated test account, NOT production credentials.

### Test Coverage

Tests cover:
- ✅ Connection and authentication
- ✅ All CRUD operations for each resource type
- ✅ Error handling (401, 403, 404, 429, etc.)
- ✅ Data mapping between API and Core types
- ✅ Edge cases and validation

### Integration Tests

Integration tests run against the live API. To skip them:

\`\`\`bash
npm test -- --testPathPattern="unit"
\`\`\`
\`\`\`

## 🟢 GUIDELINES

### Code Examples Best Practices

**Do:**
- ✅ Use TypeScript syntax highlighting
- ✅ Show all necessary imports
- ✅ Include try/catch/finally blocks
- ✅ Use environment variables for credentials
- ✅ Add descriptive console.log statements
- ✅ Show complete, runnable code
- ✅ Use realistic but fake data

**Don't:**
- ❌ Include real credentials
- ❌ Show incomplete code snippets without imports
- ❌ Omit error handling
- ❌ Use hardcoded credentials
- ❌ Show code that won't actually run

### Credential Instructions

**Do:**
- ✅ Link to detailed credential acquisition guide
- ✅ Show .env file examples
- ✅ Explain security considerations
- ✅ Provide step-by-step instructions
- ✅ Include screenshots suggestions in USERGUIDE.md

**Don't:**
- ❌ Include real API keys or tokens
- ❌ Encourage hardcoding credentials
- ❌ Skip security warnings

### Markdown Formatting

**Structure:**
```markdown
# Module Name

> Brief 1-2 sentence description

## Installation
...

## Usage
...

## Authentication
...

## Operations
...

## Examples
...

## Testing
...

## License
MIT

## Support
For issues, contact support@auditmation.com
```

**Styling:**
- Use code fences with language: \`\`\`typescript
- Use tables for mapping credentials
- Use bullet points for lists
- Use **bold** for important terms
- Use > for callouts/notes

## Validation

### Check Required Sections
```bash
# Check all required sections exist
REQUIRED_SECTIONS=("Installation" "Usage" "Authentication" "Operations" "Examples" "Testing")
MISSING=0

for section in "${REQUIRED_SECTIONS[@]}"; do
  if ! grep -q "## $section" README.md 2>/dev/null && ! grep -q "## $section" USERGUIDE.md 2>/dev/null; then
    echo "❌ FAIL: Missing section: $section"
    MISSING=1
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "✅ PASS: All required sections present"
fi
```

### Check Code Examples
```bash
# Check for TypeScript code examples
if [ -f README.md ]; then
  COUNT=$(grep -c '```typescript' README.md)
  if [ $COUNT -ge 3 ]; then
    echo "✅ PASS: Found $COUNT TypeScript code examples"
  else
    echo "❌ FAIL: Only $COUNT TypeScript examples (need at least 3)"
  fi
fi
```

### Check No Real Credentials
```bash
# Check for suspicious patterns that might be real credentials
if [ -f README.md ]; then
  # Check for long alphanumeric strings that look like tokens
  if grep -E '(password|token|key|secret).*[:=].*[A-Za-z0-9]{32,}' README.md; then
    echo "❌ FAIL: Possible real credentials found in README"
  else
    echo "✅ PASS: No obvious credentials in README"
  fi
fi

if [ -f USERGUIDE.md ]; then
  if grep -E '(password|token|key|secret).*[:=].*[A-Za-z0-9]{32,}' USERGUIDE.md; then
    echo "❌ FAIL: Possible real credentials found in USERGUIDE"
  else
    echo "✅ PASS: No obvious credentials in USERGUIDE"
  fi
fi
```

### Check Factory Function Documentation
```bash
# Check factory function is documented
if [ -f README.md ]; then
  if grep -q "newServiceName\|new[A-Z][a-zA-Z]*(" README.md; then
    echo "✅ PASS: Factory function documented"
  else
    echo "❌ FAIL: Factory function not documented"
  fi
fi
```

### Check Error Handling Examples
```bash
# Check for error handling in examples
if [ -f README.md ]; then
  if grep -q "try\|catch\|Error" README.md; then
    echo "✅ PASS: Error handling shown in examples"
  else
    echo "⚠️ WARN: No error handling examples found"
  fi
fi
```

### Complete Validation Script
```bash
#!/bin/bash
# validate-readme.sh - Complete README validation

echo "=== README Validation ==="
echo ""

# Find README or USERGUIDE
if [ -f README.md ]; then
  DOC="README.md"
elif [ -f USERGUIDE.md ]; then
  DOC="USERGUIDE.md"
else
  echo "❌ FAIL: No README.md or USERGUIDE.md found"
  exit 1
fi

echo "Checking: $DOC"
echo ""

# 1. Required sections
echo "1. Required Sections:"
SECTIONS=("Installation" "Usage" "Authentication" "Operations" "Examples" "Testing")
ALL_PRESENT=1
for section in "${SECTIONS[@]}"; do
  if grep -q "## $section" "$DOC"; then
    echo "  ✅ $section"
  else
    echo "  ❌ $section (MISSING)"
    ALL_PRESENT=0
  fi
done
echo ""

# 2. Code examples
echo "2. Code Examples:"
TS_COUNT=$(grep -c '```typescript' "$DOC" 2>/dev/null || echo "0")
if [ "$TS_COUNT" -ge 3 ]; then
  echo "  ✅ Found $TS_COUNT TypeScript examples"
else
  echo "  ❌ Only $TS_COUNT TypeScript examples (need ≥3)"
fi
echo ""

# 3. Factory function
echo "3. Factory Function:"
if grep -q "new[A-Z][a-zA-Z]*(" "$DOC"; then
  echo "  ✅ Factory function documented"
else
  echo "  ❌ Factory function not documented"
fi
echo ""

# 4. Error handling
echo "4. Error Handling:"
if grep -q "try\|catch\|Error" "$DOC"; then
  echo "  ✅ Error handling examples present"
else
  echo "  ⚠️  No error handling examples"
fi
echo ""

# 5. Credentials safety
echo "5. Credentials Safety:"
if grep -E '(password|token|key|secret).*[:=].*[A-Za-z0-9]{32,}' "$DOC" > /dev/null; then
  echo "  ❌ Possible real credentials detected!"
  grep -n -E '(password|token|key|secret).*[:=].*[A-Za-z0-9]{32,}' "$DOC"
else
  echo "  ✅ No obvious real credentials"
fi
echo ""

# Summary
if [ $ALL_PRESENT -eq 1 ] && [ "$TS_COUNT" -ge 3 ]; then
  echo "=== ✅ VALIDATION PASSED ==="
else
  echo "=== ❌ VALIDATION FAILED ==="
  exit 1
fi
```

## Common Patterns

### Service Name Placeholders
When writing template, use these placeholders:
- `ServiceName` - PascalCase service name (e.g., `AvigilonAltaAccess`)
- `service-name` - kebab-case for package names (e.g., `avigilon-alta-access`)
- `SERVICE` - UPPERCASE for environment variables (e.g., `AVIGILON_ALTA_ACCESS`)

### Connection Profile Mapping Table
Always include a table mapping service credentials to ConnectionProfile fields:

```markdown
| Service Credential | Connection Profile Field | Description |
|-------------------|-------------------------|-------------|
| API Key | `apiKey` | Your service API key |
| Account Email | `email` | Your account email address |
| Password | `password` | Your account password |
```

### Link to USERGUIDE.md
If USERGUIDE.md exists with detailed credential instructions:

```markdown
For detailed instructions on obtaining credentials, see [USERGUIDE.md](./USERGUIDE.md).
```

### Multiple Auth Methods
If service supports multiple authentication methods:

```markdown
## Authentication

This connector supports two authentication methods:

### Method 1: API Key (Recommended)
\`\`\`typescript
const profile = {
  apiKey: process.env.SERVICE_API_KEY!
};
\`\`\`

### Method 2: Username/Password
\`\`\`typescript
const profile = {
  email: process.env.SERVICE_EMAIL!,
  password: process.env.SERVICE_PASSWORD!
};
\`\`\`
```

## Anti-Patterns

### ❌ BAD: Missing imports
```typescript
// Bad - where does newServiceName come from?
const connector = newServiceName();
```

### ✅ GOOD: Complete imports
```typescript
import { newServiceName } from '@auditmation/connector-vendor-service';

const connector = newServiceName();
```

### ❌ BAD: Hardcoded credentials
```typescript
const profile = {
  apiKey: 'sk-1234567890abcdef'  // NEVER do this!
};
```

### ✅ GOOD: Environment variables
```typescript
const profile = {
  apiKey: process.env.SERVICE_API_KEY!
};
```

### ❌ BAD: No error handling
```typescript
const users = await userApi.listUsers();
```

### ✅ GOOD: Proper error handling
```typescript
try {
  const users = await userApi.listUsers();
  console.log('Users:', users);
} catch (error) {
  console.error('Failed to list users:', error.message);
}
```

### ❌ BAD: Incomplete example
```typescript
// Get users
const users = await userApi.listUsers();
```

### ✅ GOOD: Complete, runnable example
```typescript
import { newServiceName } from '@auditmation/connector-vendor-service';

async function main() {
  const connector = newServiceName();

  try {
    await connector.connect({
      apiKey: process.env.SERVICE_API_KEY!
    });

    const userApi = connector.getUserApi();
    const users = await userApi.listUsers();

    console.log('Found', users.length, 'users');
  } finally {
    await connector.disconnect();
  }
}

main();
```
