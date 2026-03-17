---
name: gate-3-implementation
description: Gate 3 validation: Implementation quality and type safety
---

### Gate 3: Implementation

**STOP AND CHECK:**
```bash
# No 'any' types in signatures
grep "Promise<any>" src/*.ts
# Must return nothing

# Using generated types
grep "import.*generated" src/*.ts
# Must show imports

# ConnectorImpl extends only generated interface
grep "extends.*Connector" src/*ConnectorImpl.ts
# Should show: extends {Service}Connector (not AbstractConnector or other classes)

# Metadata uses boilerplate (ConnectionStatus.Down)
grep "ConnectionStatus.Down" src/*ConnectorImpl.ts
# MUST return match - this is the required boilerplate

# Metadata is async returning Promise
grep "async metadata(): Promise<ConnectionMetadata>" src/*ConnectorImpl.ts
# MUST return match - correct signature

# isSupported uses boilerplate (OperationSupportStatus.Maybe)
grep "OperationSupportStatus.Maybe" src/*ConnectorImpl.ts
# MUST return match - this is the required boilerplate

# isSupported parameter named correctly (_operationId with underscore)
grep "isSupported(_operationId:" src/*ConnectorImpl.ts
# MUST return match - underscore indicates unused parameter

# No customized metadata logic
grep -E "ConnectionStatus\.(Up|Connected|Ready)" src/*ConnectorImpl.ts
# Should return nothing - only Down allowed

# No customized isSupported logic
grep -E "OperationSupportStatus\.(Yes|No)" src/*ConnectorImpl.ts
# Should return nothing - only Maybe allowed

# No connection context in producer method parameters
grep -E "(apiKey|token|baseUrl|organizationId):" src/*Producer.ts
# Should return nothing - these come from client

# Mappers should prefer map() function over constructors
if [ -f "src/Mappers.ts" ]; then
  if grep -E "new (UUID|Email|URL|DateTime)\(" src/Mappers.ts > /dev/null; then
    echo "⚠️  WARNING: Mappers.ts using constructors directly"
    echo "   PREFER map() from @zerobias-org/util-hub-module-utils"
    echo "   Example: map(UUID, value) instead of new UUID(value)"
    echo "   Only use constructors if map() doesn't meet requirements"
  fi

  # Check for map() import
  if ! grep -q "import.*map.*from.*@zerobias-org/util-hub-module-utils" src/Mappers.ts; then
    echo "⚠️  WARNING: Mappers.ts missing map() import"
    echo "   Add: import { map } from '@zerobias-org/util-hub-module-utils';"
    echo "   map() handles optional values automatically and is preferred"
  fi
fi

# Check if using core profiles when applicable
# If connectionProfile.yml exists and is custom
if [ -f "connectionProfile.yml" ] && ! grep -q "\$ref.*types-core/schema" connectionProfile.yml; then
  echo "⚠️  WARNING: Custom connectionProfile.yml - verify core profile not applicable"
  echo "   Available core profiles:"
  echo "   - tokenProfile.yml (API token/key auth)"
  echo "   - oauthClientProfile.yml (OAuth client credentials)"
  echo "   - oauthTokenProfile.yml (OAuth token)"
  echo "   - basicConnection.yml (username/password or email/password)"
  echo "   For email/password auth, consider extending basicConnection.yml"
fi

# If connectionState.yml exists, validate it
if [ -f "connectionState.yml" ]; then
  # Check if using core state (recommended)
  if ! grep -q "\$ref.*types-core/schema" connectionState.yml; then
    echo "⚠️  WARNING: Custom connectionState.yml - verify core state not applicable"
    echo "   Available core states:"
    echo "   - tokenConnectionState.yml (access token + expiresIn)"
    echo "   - oauthTokenState.yml (OAuth with refresh capability)"
    echo "   All states MUST extend baseConnectionState.yml for expiresIn"
  fi

  # CRITICAL: Validate expiresIn field (required for server cronjobs)
  if ! grep -q "\$ref.*baseConnectionState\|expiresIn:" connectionState.yml; then
    echo "❌  CRITICAL ERROR: connectionState.yml missing expiresIn field"
    echo "   WHY: Server sets cronjobs based on expiresIn for automatic token refresh"
    echo "   FIX: Must extend baseConnectionState.yml OR include expiresIn property"
    echo "   UNIT: expiresIn must be in SECONDS (integer) until token expires"
  fi

  # Check for expiresAt (should be converted to expiresIn)
  if grep -q "expiresAt:" connectionState.yml; then
    echo "⚠️  WARNING: connectionState.yml has expiresAt field"
    echo "   REQUIRED: Calculate expiresIn (seconds) from expiresAt and DROP expiresAt"
    echo "   WHY: Server needs expiresIn (seconds) for cronjobs, not timestamps"
    echo "   FIX: In connect(), calculate: expiresIn = Math.floor((expiresAt - now) / 1000)"
  fi

  # If has refreshToken, MUST have expiresIn
  if grep -q "refreshToken:" connectionState.yml && ! grep -q "\$ref.*baseConnectionState\|expiresIn:" connectionState.yml; then
    echo "❌  CRITICAL ERROR: Has refreshToken but missing expiresIn"
    echo "   WHY: Cannot schedule token refresh without knowing when it expires"
    echo "   FIX: Must extend baseConnectionState.yml to include expiresIn"
  fi
fi
```

**PROCEED ONLY IF:**
- ✅ NO `any` types in method signatures
- ✅ Using generated types from generated/api/
- ✅ ConnectorImpl extends ONLY generated interface (read from generated/api/index.ts)
- ✅ metadata() exact boilerplate: `async metadata(): Promise<ConnectionMetadata> { return { status: ConnectionStatus.Down } satisfies ConnectionMetadata; }`
- ✅ isSupported() exact boilerplate: `async isSupported(_operationId: string) { return OperationSupportStatus.Maybe; }`
- ❌ NO customization of metadata() or isSupported() methods
- ✅ Mappers implemented for field conversions (const output pattern)
- ✅ Mappers use `map()` from `@zerobias-org/util-hub-module-utils` (NOT constructors directly)
- ✅ **Mapper runtime validation completed** - ZERO missing fields confirmed (see validation section below)
- ✅ Error handling uses core error types
- ✅ NO connection context parameters (apiKey, token, baseUrl, organizationId) in producer methods
- ✅ Using core connectionProfile/connectionState when applicable (or justified custom)
- ✅ If custom connectionState: includes expiresIn (extends baseConnectionState.yml)
- ✅ If refresh capability: connectionState has refreshToken + all refresh-relevant data
- ✅ No TypeScript compilation errors

**IF FAILED:** Fix implementation before writing tests.

## Mapper Runtime Validation (CRITICAL)

**MANDATORY validation step** after mapper implementation to detect missing fields.

### Why Runtime Validation is Required

Static validation (counting interface fields) does NOT catch:
- ❌ Field name mismatches (API `mobilePhone` vs mapper `phoneNumber`)
- ❌ Fields in API but not in spec
- ❌ Incorrect field lookups in mapper

**Real example:** User producer had 14 missing fields that passed TypeScript compilation and all tests.

### Validation Process

1. **Add temporary debug logs** in producer implementations BEFORE mapping:
   ```typescript
   this.logger.debug('[TEMP-RAW-API] operationName:', JSON.stringify(response.data, null, 2));
   ```

2. **Run integration tests** with debug logging:
   ```bash
   env LOG_LEVEL=debug npm run test:integration > /tmp/debug.log 2>&1
   ```

3. **Compare raw API vs mapped** fields:
   ```bash
   # Extract raw API response
   grep -A 100 "\[TEMP-RAW-API\]" /tmp/debug.log

   # Compare with mapped result
   grep "Api\." /tmp/debug.log
   ```

4. **Fix missing fields** if any found

5. **Remove temp debug logs** after validation passes

### Automated Validation (RECOMMENDED)

Use parallel mapping-engineer agents (one per producer):

```bash
# For each producer, launch agent to:
# 1. Read debug log
# 2. Extract raw API responses
# 3. Compare with mapper
# 4. Fix any missing fields
# 5. Report results
```

### Success Criteria

- ✅ All [TEMP-RAW-API] logs added
- ✅ Integration tests run with LOG_LEVEL=debug
- ✅ Raw API responses extracted
- ✅ Field-by-field comparison completed
- ✅ **ZERO missing fields** confirmed
- ✅ All field name mismatches fixed
- ✅ API-spec gaps documented
- ✅ Temp debug logs removed

**RULE:** Gate 3 does NOT pass until mapper runtime validation shows ZERO missing fields.

**Complete process:** mapper-runtime-validation skill
