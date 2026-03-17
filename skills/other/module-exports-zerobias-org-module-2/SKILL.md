---
name: module-exports
description: Module export patterns including factory functions and public API design
---

# Module Exports Patterns

## 🚨 CRITICAL RULES

### 1. Factory Function is Primary Export
Every module's `src/index.ts` MUST export a factory function:

```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

**Rules:**
- ✅ Named export (NOT default export)
- ✅ Function name starts with `new`
- ✅ Returns Impl instance (which implements Connector)
- ✅ No parameters
- ❌ NEVER use default export

### 2. Re-export Generated Types
MUST re-export all generated types:

```typescript
// Re-export all generated API interfaces and wrappers
export * from '../generated/api';

// Re-export all generated models
export * from '../generated/model';
```

**Why:**
- Consumers need access to types
- ConnectionProfile, ConnectionState, etc.
- Resource models (User, Group, etc.)
- Don't pick specific types - export all

### 3. Minimal Public API
ONLY export what consumers actually need:

**Export:**
- ✅ Factory function
- ✅ Generated types (api.ts, model.ts)
- ✅ Custom profile types (if any)
- ✅ Custom error types (if any)

**DO NOT export:**
- ❌ Client class (internal implementation)
- ❌ Producer implementation classes (internal)
- ❌ Mapper functions (internal)
- ❌ Helper/utility functions (internal)
- ❌ HTTP interceptors (internal)

## 🟡 STANDARD RULES

### Standard index.ts Template

**Basic pattern:**

```typescript
// src/index.ts

// Import Impl class
import { ServiceImpl } from './ServiceImpl';

// ========================================
// Factory Function (Primary Export)
// ========================================

/**
 * Creates a new Service connector instance
 * @returns ServiceImpl instance that implements ServiceConnector
 */
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

// ========================================
// Generated Exports
// ========================================

// Re-export all generated API interfaces and wrappers
export * from '../generated/api';

// Re-export all generated models
export * from '../generated/model';

// ========================================
// Custom Type Exports (if needed)
// ========================================

// Export custom profile types if you have them
// export type { CustomProfile } from './ServiceClient';

// Export custom error types if you have them
// export type { CustomError } from './errors';
```

### Factory Function Naming

**Pattern:** `new` + PascalCase service name

**Examples:**
```typescript
// GitHub module
export function newGitHub(): GitHubImpl

// Avigilon Alta Access module
export function newAvigilonAltaAccess(): AccessImpl

// Slack module
export function newSlack(): SlackImpl

// Azure Active Directory module
export function newAzureActiveDirectory(): AzureActiveDirectoryImpl
```

**Rules:**
- ✅ Always starts with `new`
- ✅ Service name in PascalCase
- ✅ Full service name (not abbreviated)
- ✅ Returns Impl class
- ❌ No abbreviations (newAAD ❌, newAzureActiveDirectory ✅)

### What Gets Re-exported from generated/

**From `../generated/api.ts`:**
```typescript
export * from '../generated/api';
```

This exports:
- `ServiceConnector` interface
- `<Resource>Api` interfaces (UserApi, GroupApi, etc.)
- `wrap<Resource>Producer` functions
- Type definitions for all operations

**From `../generated/model.ts`:**
```typescript
export * from '../generated/model';
```

This exports:
- `ConnectionProfile` type
- `ConnectionState` type
- Resource types (User, Group, Acu, etc.)
- Request/Response types
- Enum types

### Optional Exports

**Export Impl class (optional):**
```typescript
// Export implementation class for advanced usage
export { ServiceImpl } from './ServiceImpl';
```

**When to export:**
- ✅ If consumers might need to extend it
- ✅ If consumers need type for instance checks
- ⚠️ Usually not necessary - factory function is enough

**Export Client class (rarely):**
```typescript
// Export client for advanced/testing usage
export { ServiceClient } from './ServiceClient';
```

**When to export:**
- ⚠️ Rarely needed
- ⚠️ Only if consumers need direct access for testing
- ⚠️ Generally keep Client internal

**Export mappers (for testing):**
```typescript
// Export mappers for testing/debugging
export * from './Mappers';
```

**When to export:**
- ✅ If consumers might need to test mappings
- ✅ If mappers are useful utilities
- ⚠️ Consider if mappers should be internal

### Custom Type Exports

**If you have custom ConnectionProfile extensions:**
```typescript
// ServiceClient.ts
export interface ServiceProfile extends ConnectionProfile {
  region?: string;
  customSetting?: boolean;
}

// index.ts
export type { ServiceProfile } from './ServiceClient';
```

**If you have custom error types:**
```typescript
// errors.ts
export class ServiceSpecificError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ServiceSpecificError';
  }
}

// index.ts
export { ServiceSpecificError } from './errors';
```

### Export Organization

**Group exports by purpose with comments:**

```typescript
// src/index.ts

import { ServiceImpl } from './ServiceImpl';

// ========================================
// Factory Function
// ========================================

export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

// ========================================
// Implementation Classes (for advanced usage)
// ========================================

export { ServiceImpl } from './ServiceImpl';
// export { ServiceClient } from './ServiceClient';  // Uncomment if needed

// ========================================
// Generated Types
// ========================================

export * from '../generated/api';
export * from '../generated/model';

// ========================================
// Mappers (for testing)
// ========================================

export * from './Mappers';

// ========================================
// Custom Types
// ========================================

// export type { ServiceProfile } from './ServiceClient';
// export { ServiceSpecificError } from './errors';
```

## 🟢 GUIDELINES

### Type Safety in Exports

**Factory function should have return type:**
```typescript
// ✅ GOOD: Explicit return type
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

// ⚠️ OK but less clear
export function newServiceName() {
  return new ServiceImpl();
}
```

**Why:**
- Explicit type helps consumers
- IDE autocomplete works better
- Catches return type errors

### Default Exports (Don't Use)

**❌ WRONG: Default export**
```typescript
export default function newServiceName() {
  return new ServiceImpl();
}
```

**✅ CORRECT: Named export**
```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

**Why:**
- Named exports are more explicit
- Better for tree-shaking
- Easier to find usages
- Consistent with TypeScript best practices

### Consumer Usage Pattern

**How consumers use your module:**

```typescript
// Consumer code
import {
  newServiceName,
  ConnectionProfile,
  UserApi,
  User
} from '@auditmation/connector-vendor-service';

// Create connector using factory
const connector = newServiceName();

// Use ConnectionProfile type
const profile: ConnectionProfile = {
  apiKey: process.env.API_KEY!
};

// Connect
await connector.connect(profile);

// Get typed API
const userApi: UserApi = connector.getUserApi();

// Get typed resources
const users: User[] = await userApi.listUsers();
```

**What they need:**
1. Factory function - `newServiceName()`
2. Profile type - `ConnectionProfile`
3. API interfaces - `UserApi`
4. Resource types - `User`

All of these come from your exports!

### Documentation Comments

**Add JSDoc to factory function:**

```typescript
/**
 * Creates a new Service connector instance.
 *
 * @returns A new connector instance that implements ServiceConnector
 *
 * @example
 * ```typescript
 * import { newServiceName } from '@auditmation/connector-vendor-service';
 *
 * const connector = newServiceName();
 * await connector.connect({ apiKey: 'your-key' });
 * ```
 */
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

**Benefits:**
- Shows up in IDE tooltips
- Documents usage
- Provides example

### Impl Class Export Pattern

**If exporting Impl, also export it directly:**

```typescript
// Option 1: Export from source
export { ServiceImpl } from './ServiceImpl';

// Option 2: Re-export from factory
import { ServiceImpl } from './ServiceImpl';

export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

export { ServiceImpl };  // Also export class
```

**Enables type checking:**
```typescript
// Consumer code
import { newServiceName, ServiceImpl } from '@auditmation/connector';

const connector = newServiceName();

if (connector instanceof ServiceImpl) {
  // TypeScript knows the type
}
```

## Validation

### Check Factory Function Exists
```bash
# Check factory function exists
if [ -f src/index.ts ]; then
  if grep -q "export function new" src/index.ts; then
    echo "✅ PASS: Factory function exists"
  else
    echo "❌ FAIL: No factory function found"
    exit 1
  fi
else
  echo "❌ FAIL: src/index.ts not found"
  exit 1
fi
```

### Check Factory Function Naming
```bash
# Check factory function follows naming convention
FACTORY_NAME=$(grep "export function new" src/index.ts | sed -E 's/.*function (new[A-Za-z]+).*/\1/')

if [[ "$FACTORY_NAME" =~ ^new[A-Z] ]]; then
  echo "✅ PASS: Factory function named: $FACTORY_NAME"
else
  echo "❌ FAIL: Factory function must start with 'new' + PascalCase"
  exit 1
fi
```

### Check Generated Exports
```bash
# Check re-exports from generated/
if grep -q "export \* from.*generated" src/index.ts; then
  echo "✅ PASS: Re-exports generated types"
else
  echo "❌ FAIL: Must re-export from ../generated/"
  exit 1
fi

# Check both api and model exports
if grep -q "export \* from.*generated/api" src/index.ts; then
  echo "✅ PASS: Exports generated/api"
else
  echo "⚠️ WARN: Should export from ../generated/api"
fi

if grep -q "export \* from.*generated/model" src/index.ts; then
  echo "✅ PASS: Exports generated/model"
else
  echo "⚠️ WARN: Should export from ../generated/model"
fi
```

### Check No Internal Exports
```bash
# Check NOT exporting Client class (usually internal)
if grep -q "export.*Client.*from.*Client" src/index.ts | grep -v "//"; then
  echo "⚠️ WARN: Exporting Client class (usually should be internal)"
else
  echo "✅ PASS: Client class not exported (good - keep internal)"
fi

# Check for default exports (should not use)
if grep -q "export default" src/index.ts; then
  echo "❌ FAIL: Using default export (use named exports)"
  exit 1
else
  echo "✅ PASS: No default exports (good)"
fi
```

### Check Return Type
```bash
# Check factory function has return type
if grep -q "export function new.*().*:" src/index.ts; then
  echo "✅ PASS: Factory function has return type"
else
  echo "⚠️ WARN: Factory function should have explicit return type"
fi
```

### Complete Validation Script
```bash
#!/bin/bash
# validate-exports.sh - Validate index.ts exports

echo "=== Module Exports Validation ==="
echo ""

if [ ! -f src/index.ts ]; then
  echo "❌ FAIL: src/index.ts not found"
  exit 1
fi

echo "Checking: src/index.ts"
echo ""

ERRORS=0

# 1. Factory function
echo "1. Factory Function:"
if grep -q "export function new" src/index.ts; then
  FACTORY=$(grep "export function new" src/index.ts | head -1)
  echo "  ✅ Found: $FACTORY"

  # Check naming
  if echo "$FACTORY" | grep -q "export function new[A-Z]"; then
    echo "  ✅ Correct naming (new + PascalCase)"
  else
    echo "  ❌ Wrong naming (must be new + PascalCase)"
    ERRORS=$((ERRORS + 1))
  fi

  # Check return type
  if echo "$FACTORY" | grep -q "):"; then
    echo "  ✅ Has return type"
  else
    echo "  ⚠️  Should have explicit return type"
  fi
else
  echo "  ❌ Factory function missing"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# 2. Generated exports
echo "2. Generated Exports:"
if grep -q "export \* from.*generated" src/index.ts; then
  echo "  ✅ Re-exports from generated/"

  if grep -q "export \* from.*generated/api" src/index.ts; then
    echo "  ✅ Exports ../generated/api"
  else
    echo "  ⚠️  Should export ../generated/api"
  fi

  if grep -q "export \* from.*generated/model" src/index.ts; then
    echo "  ✅ Exports ../generated/model"
  else
    echo "  ⚠️  Should export ../generated/model"
  fi
else
  echo "  ❌ Must re-export from generated/"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. Export style
echo "3. Export Style:"
if grep -q "export default" src/index.ts; then
  echo "  ❌ Uses default export (should use named exports)"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ No default exports (good)"
fi

# Count named exports
EXPORT_COUNT=$(grep -c "^export" src/index.ts)
echo "  ✅ $EXPORT_COUNT export statements"
echo ""

# 4. Internal exports check
echo "4. Internal Exports (warnings):"
if grep -q "export.*Client" src/index.ts | grep -v "^//"; then
  echo "  ⚠️  Exporting Client (usually internal)"
else
  echo "  ✅ Client not exported"
fi

if grep -q "export.*Mapper" src/index.ts | grep -v "^//"; then
  echo "  ⚠️  Exporting Mappers (check if needed)"
else
  echo "  ✅ Mappers not exported"
fi
echo ""

# 5. File size check (should be small)
LINE_COUNT=$(wc -l < src/index.ts)
if [ "$LINE_COUNT" -lt 50 ]; then
  echo "5. File Size: ✅ $LINE_COUNT lines (good - index.ts should be small)"
else
  echo "5. File Size: ⚠️ $LINE_COUNT lines (large - consider if all exports are needed)"
fi
echo ""

# Summary
if [ $ERRORS -eq 0 ]; then
  echo "=== ✅ VALIDATION PASSED ==="
  exit 0
else
  echo "=== ❌ VALIDATION FAILED ($ERRORS errors) ==="
  exit 1
fi
```

## Common Issues

### Issue: No factory function
**Problem:**
```typescript
// index.ts
export { ServiceImpl } from './ServiceImpl';
```

**Solution:**
```typescript
import { ServiceImpl } from './ServiceImpl';

export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

export * from '../generated/api';
export * from '../generated/model';
```

### Issue: Using default export
**Problem:**
```typescript
export default function newServiceName() {
  return new ServiceImpl();
}
```

**Solution:**
```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

### Issue: Not re-exporting generated types
**Problem:**
```typescript
// Only exports factory
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

**Solution:**
```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

// Add these
export * from '../generated/api';
export * from '../generated/model';
```

### Issue: Exporting too much
**Problem:**
```typescript
// Exporting everything
export * from './ServiceImpl';
export * from './ServiceClient';
export * from './helpers';
export * from './utils';
export * from './mappers';
export * from './errors';
```

**Solution:**
```typescript
// Minimal public API
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

export * from '../generated/api';
export * from '../generated/model';

// Only export what consumers truly need
```

## Anti-Patterns

### ❌ BAD: Complex factory with parameters
```typescript
export function newServiceName(config: ServiceConfig): ServiceImpl {
  return new ServiceImpl(config);
}
```

### ✅ GOOD: Simple factory, no parameters
```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

### ❌ BAD: Multiple factory functions
```typescript
export function newServiceName(): ServiceImpl { ... }
export function createServiceName(): ServiceImpl { ... }
export function makeServiceName(): ServiceImpl { ... }
```

### ✅ GOOD: Single factory function
```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}
```

### ❌ BAD: Selective type exports
```typescript
// Don't cherry-pick types
export { ConnectionProfile, UserApi } from '../generated/api';
export { User, Group } from '../generated/model';
```

### ✅ GOOD: Export all generated types
```typescript
// Export everything
export * from '../generated/api';
export * from '../generated/model';
```

### ❌ BAD: Exporting implementation details
```typescript
export { ServiceClient } from './ServiceClient';
export { httpInterceptor } from './interceptors';
export { mapUser, mapGroup } from './mappers';
export { validateProfile } from './validators';
```

### ✅ GOOD: Minimal public API
```typescript
export function newServiceName(): ServiceImpl {
  return new ServiceImpl();
}

export * from '../generated/api';
export * from '../generated/model';

// Keep internals private
```
