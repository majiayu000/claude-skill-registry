---
name: client-responsibilities
description: Client class responsibilities - connection ONLY, no business operations
---

# Client Implementation Patterns

## 🚨 CRITICAL RULE #1: Client ONLY Handles Connection

- **Client**: ONLY connection management (connect, isConnected, disconnect)
- **Producers**: ALL API operations (list, get, create, update, delete)
- Client provides HTTP client instance to producers, nothing more

**Client MUST NOT implement**: list, get, create, update, delete, or any API operations.

## Client Class - Connection Management Only

```typescript
class ServiceClient {
  // ✅ Client responsibilities ONLY
  async connect(profile: ConnectionProfile): Promise<void> {
    // Setup authentication, HTTP client config
  }

  async isConnected(): Promise<boolean> {
    // Real API call to verify connection
  }

  async disconnect(): Promise<void> {
    // Cleanup
  }
}
```

### Connect Method Return Types
- `Promise<ConnectionState>` - If state needs persistence (tokens, expiration)
- `Promise<void>` - If no state persistence needed

## ConnectionState Pattern

### 🚨 CRITICAL: ConnectionState Design Rules

1. **Include ALL refresh-relevant data** - Store everything needed for token refresh
2. **MANDATORY: expiresIn field** - All states MUST include `expiresIn` (extend baseConnectionState.yml)
   - **WHY**: The server sets cronjobs based on `expiresIn` for automatic token refresh
   - **UNIT**: Must be in **seconds** (integer) until token expires
   - **REQUIRED**: For any token that has an expiration
3. **Store refresh tokens** - If API provides refresh capability, store the refresh token
4. **Refresh method constraint** - `refresh()` can ONLY use ConnectionProfile + ConnectionState data
5. **expiresIn calculation from API responses**:
   - If API returns `expires_in` (seconds) → Use directly as `expiresIn`
   - If API returns `expires_at` (timestamp) → Calculate `expiresIn` as seconds until that time
   - If API returns other expiration format → Convert to `expiresIn` (seconds)
   - **DROP the original field** - Only store `expiresIn`, not `expiresAt` or other formats

### What to Store in ConnectionState

**MANDATORY when provided by API:**
- `accessToken` - Always store the current access token
- `expiresIn` - Token expiration time (seconds or timestamp)
- `refreshToken` - If API supports token refresh
- `scope` - OAuth scope if relevant for refresh
- `tokenType` - Type of token (bearer, etc.)

**OPTIONAL based on API:**
- `url` - If different endpoints for different tokens
- Vendor-specific metadata needed for refresh

```yaml
# ✅ CORRECT - Using core state (recommended)
# connectionState.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'
# Includes: tokenType, accessToken, refreshToken, expiresIn, scope, url
# Already extends baseConnectionState.yml (which provides expiresIn)
```

```yaml
# ✅ CORRECT - Custom state with all refresh data
# connectionState.yml
type: object
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/baseConnectionState.yml'  # Provides expiresIn
  - type: object
    required:
      - accessToken
    properties:
      accessToken:
        type: string
        format: password
        description: Current access token
      refreshToken:
        type: string
        format: password
        description: Token used to obtain new access token
      scope:
        type: string
        description: OAuth scope for this token
# Note: expiresIn comes from baseConnectionState.yml
```

```yaml
# ❌ WRONG - Missing refresh data and not extending baseConnectionState
type: object
properties:
  accessToken:
    type: string
# Missing: expiresIn (MANDATORY - must extend baseConnectionState.yml)
# Missing: refreshToken (needed for refresh capability)
```

### Implementing connect() with State

```typescript
// ✅ CORRECT - Store ALL relevant data from API (expiresIn provided directly)
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  const response = await this.httpClient.post('/auth/login', {
    username: profile.username,
    password: profile.password
  });

  // Store EVERYTHING the API provides that might be needed for refresh
  const state: ConnectionState = {
    accessToken: response.data.access_token,
    refreshToken: response.data.refresh_token,  // Store for refresh()
    expiresIn: response.data.expires_in,         // MANDATORY - seconds until expiration
    tokenType: response.data.token_type,         // Store if needed for headers
    scope: response.data.scope                   // Store if needed for refresh
  };

  this.connectionState = state;
  return state; // Framework persists
}
```

```typescript
// ✅ CORRECT - Calculate expiresIn when API returns expires_at (timestamp)
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  const response = await this.httpClient.post('/auth/login', {
    username: profile.username,
    password: profile.password
  });

  // Calculate expiresIn from expires_at timestamp
  const expiresAtTimestamp = new Date(response.data.expires_at).getTime();
  const nowTimestamp = Date.now();
  const expiresIn = Math.floor((expiresAtTimestamp - nowTimestamp) / 1000); // Convert to seconds

  // CRITICAL: Store ONLY expiresIn, DROP expires_at
  // The server needs expiresIn for cronjobs
  const state: ConnectionState = {
    accessToken: response.data.access_token,
    refreshToken: response.data.refresh_token,
    expiresIn: expiresIn,  // MANDATORY - calculated from expires_at, in SECONDS
    tokenType: response.data.token_type,
    scope: response.data.scope
    // Note: expires_at NOT stored - only expiresIn is needed
  };

  this.connectionState = state;
  return state; // Framework persists
}
```

```typescript
// ❌ WRONG - Storing expiresAt instead of expiresIn
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  const response = await this.httpClient.post('/auth/login', {
    username: profile.username,
    password: profile.password
  });

  const state: ConnectionState = {
    accessToken: response.data.access_token,
    expiresAt: response.data.expires_at,  // ❌ WRONG - should be expiresIn (seconds)
  };

  this.connectionState = state;
  return state;
}
// Problem: Server cannot set cronjob without expiresIn (seconds)
```

### Implementing refresh() Method

**CRITICAL**: `refresh()` can ONLY access:
- `this.connectionProfile` - Original connection credentials
- `this.connectionState` - Current state (with refreshToken, etc.)

```typescript
// ✅ CORRECT - Uses only profile + state
async refresh(): Promise<ConnectionState> {
  // Can use data from connectionState (refreshToken)
  const response = await this.httpClient.post('/auth/refresh', {
    refresh_token: this.connectionState.refreshToken,
    // Can also use profile data if needed
    client_id: this.connectionProfile.client_id
  });

  // Update state with new tokens
  const newState: ConnectionState = {
    accessToken: response.data.access_token,
    refreshToken: response.data.refresh_token || this.connectionState.refreshToken,
    expiresIn: response.data.expires_in,
    tokenType: response.data.token_type,
    scope: response.data.scope
  };

  this.connectionState = newState;
  return newState;
}
```

```typescript
// ❌ WRONG - Requires data not in profile/state
async refresh(): Promise<ConnectionState> {
  const response = await this.httpClient.post('/auth/refresh', {
    refresh_token: this.connectionState.refreshToken,
    device_id: 'hardcoded-value'  // NO! Not in profile/state
  });
  // This will fail - device_id should be in ConnectionProfile or ConnectionState
}
```

### When to use ConnectionState

**Use ConnectionState (return from connect()):**
- OAuth2 flows (access + refresh tokens)
- Session-based authentication
- APIs requiring token refresh
- Token expiration tracking needed

**Use void (return from connect()):**
- API key authentication (static, never expires)
- Basic auth (credentials used each request, no state)
- No refresh capability needed

## Use Core Connection Profiles and States

### 🚨 CRITICAL RULE
- **MANDATORY**: Use existing core schemas from `@zerobias-org/types-core/schema` when they match
- **FORBIDDEN**: Creating custom connectionProfile.yml or connectionState.yml when core schema exists

### Available Core Connection Profiles

```yaml
# ✅ CORRECT - Token/API Key authentication
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/tokenProfile.yml'

# Fields: apiToken (required), url (optional)
# Use when: API uses a single token/key for authentication
```

```yaml
# ✅ CORRECT - OAuth Client Credentials
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthClientProfile.yml'

# Fields: client_id (required), client_secret (required), url (optional)
# Use when: OAuth client credentials grant (RFC 6749 section 4.4)
```

```yaml
# ✅ CORRECT - OAuth Token-based
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenProfile.yml'

# Fields: tokenType (default: bearer), accessToken (required), url (optional)
# Use when: Pre-obtained OAuth token authentication
```

```yaml
# ✅ CORRECT - Username/Password authentication (Basic Auth pattern)
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/basicConnection.yml'

# Fields: uri (required, URL), username (required), password (required)
# Use when: API uses username/password or email/password authentication
# Note: For email specifically, you can extend this and change username to email with format: email
```

```yaml
# ✅ CORRECT - Email/Password authentication (extending basicConnection)
# connectionProfile.yml
type: object
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/basicConnection.yml'
  - type: object
    properties:
      username:
        type: string
        format: email  # Override to require email format
        description: User email for authentication

# Extends basicConnection but enforces email format on username field
# Use when: API requires email specifically (not just any username)
```

### Available Core Connection States

```yaml
# ✅ CORRECT - Simple token state
# connectionState.yml
$ref: './node_modules/@zerobias-org/types-core/schema/tokenConnectionState.yml'

# Fields: accessToken, expiresIn (from baseConnectionState)
# Use when: Only need to persist access token with expiration
# Note: Extends baseConnectionState.yml
```

```yaml
# ✅ CORRECT - Full OAuth state
# connectionState.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'

# Fields: tokenType, accessToken, refreshToken, expiresIn (from base), scope, url
# Use when: OAuth authorization code flow with refresh capability
# Note: Extends baseConnectionState.yml
```

### When to Create Custom Profile/State

Only create custom schemas when:
- Authentication method doesn't match any core profile
- Additional vendor-specific fields required beyond core profile fields
- Specialized authentication flow not covered by core

```yaml
# ⚠️ CONSIDER FIRST - Can this use basicConnection.yml?
# For username/password or email/password auth, prefer extending basicConnection.yml
# See examples above for basicConnection.yml usage

# ✅ ACCEPTABLE - Fully custom (but consider basicConnection first!)
# connectionProfile.yml (custom when core types don't fit)
type: object
required:
  - email
  - password
properties:
  email:
    type: string
    format: email
  password:
    type: string
    format: password
  baseUrl:
    type: string
    format: url
    default: https://api.vendor.com
# Note: Could potentially extend basicConnection.yml instead
```

### Decision Process

1. Check if core profile matches authentication method
   - Token/API Key → `tokenProfile.yml`
   - OAuth client credentials → `oauthClientProfile.yml`
   - OAuth token → `oauthTokenProfile.yml`
   - Username/password or email/password → `basicConnection.yml` (or extend it)
2. If exact match → Use core profile with $ref
3. If partial match → Extend core profile (use allOf)
4. If no match → Create custom profile with full schema (rare)

**WHY**: Core profiles ensure consistency, reduce duplication, and provide standard patterns that the framework expects.

## Validation Scripts

### Validate Client Implementation

```bash
# Check client only has connection methods
grep -E "(async (list|get|create|update|delete|patch))" src/*Client.ts && echo "❌ Client has business logic!" || echo "✅ Client clean"

# Check client implements required methods
grep -E "(async connect|async isConnected|async disconnect)" src/*Client.ts && echo "✅ Client has required methods" || echo "❌ Missing client methods"

# Check ConnectionState extends baseConnectionState or uses core state
grep -E "(baseConnectionState\.yml|tokenConnectionState\.yml|oauthTokenState\.yml)" connectionState.yml && echo "✅ State extends base" || echo "⚠️ Check if expiresIn is defined"
```

### Validate ConnectionState has expiresIn

```bash
# Check expiresIn is in state (either via base or custom)
(grep -q "baseConnectionState.yml" connectionState.yml || grep -q "expiresIn" connectionState.yml) && echo "✅ expiresIn present" || echo "❌ Missing expiresIn!"
```

### Validate Core Profile Usage

```bash
# Check if using core profiles
grep -E "(tokenProfile\.yml|oauthClientProfile\.yml|oauthTokenProfile\.yml|basicConnection\.yml)" connectionProfile.yml && echo "✅ Using core profile" || echo "⚠️ Custom profile - verify it's necessary"
```
