---
name: connection-schema-design
description: Connection profile and state schema design rules and core profile selection
---

# Connection Profile & State Design Rules

**Rules for designing connectionProfile.yml and connectionState.yml schemas**

## 🚨 CRITICAL RULES

### Rule 1: Always Extend Core Profiles

**NEVER create custom profiles from scratch - ALWAYS extend core profiles**

```yaml
# ❌ WRONG - Custom profile
type: object
properties:
  apiKey:
    type: string

# ✅ CORRECT - Extend core profile
$ref: './node_modules/@auditmation/types-core/schema/tokenProfile.yml'
```

### Rule 2: connectionState MUST Extend baseConnectionState

**🚨 MANDATORY**: connectionState.yml MUST extend baseConnectionState.yml for expiresIn

```yaml
# ✅ CORRECT - Extends base with expiresIn
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/baseConnectionState.yml'
  - type: object
    properties:
      accessToken:
        type: string

# ❌ WRONG - Missing baseConnectionState
type: object
properties:
  accessToken:
    type: string
  # Missing expiresIn!
```

**WHY**: Server uses expiresIn to schedule automatic token refresh cronjobs

### Rule 3: expiresIn Must Be in Seconds

```yaml
# ✅ CORRECT
expiresIn:
  type: integer
  description: Token expiry time in SECONDS from now

# ❌ WRONG
expiresAt:
  type: string  # Don't use expiresAt, convert to expiresIn
```

**Calculation**: `expiresIn = Math.floor((expiresAt - now) / 1000)`

## Core Profile Selection

### Available Core Profiles

| Profile | When to Use | Contains |
|---------|-------------|----------|
| **tokenProfile.yml** | API Key, Bearer Token, PAT | token |
| **oauthClientProfile.yml** | OAuth2 Client Credentials | clientId, clientSecret |
| **oauthTokenProfile.yml** | OAuth2 with Refresh | clientId, clientSecret |
| **basicConnection.yml** | Username/Password, Email/Password | username, password |

**Path**: `./node_modules/@auditmation/types-core/schema/{profileName}.yml`

### Selection Decision Tree

```
@credential-manager provides authMethodType:

IF authMethodType == "bearer-token" OR "api-key"
  → EXTEND tokenProfile.yml

IF authMethodType == "oauth2-client-credentials"
  → EXTEND oauthClientProfile.yml

IF authMethodType == "oauth2-authorization-code"
  → EXTEND oauthTokenProfile.yml

IF authMethodType == "basic-auth"
  → EXTEND basicConnection.yml
```

## Available Core States

| State | When to Use | Contains |
|-------|-------------|----------|
| **tokenConnectionState.yml** | Simple token auth | accessToken + expiresIn |
| **oauthTokenState.yml** | OAuth with refresh | accessToken + refreshToken + expiresIn |

### State Selection

```
IF requiresRefresh == false
  → EXTEND tokenConnectionState.yml

IF requiresRefresh == true
  → EXTEND oauthTokenState.yml
```

## Common Patterns

### Pattern 1: Simple API Token

```yaml
# connectionProfile.yml
$ref: './node_modules/@auditmation/types-core/schema/tokenProfile.yml'

# connectionState.yml
$ref: './node_modules/@auditmation/types-core/schema/tokenConnectionState.yml'
```

### Pattern 2: OAuth Client Credentials

```yaml
# connectionProfile.yml
$ref: './node_modules/@auditmation/types-core/schema/oauthClientProfile.yml'

# connectionState.yml (no refresh)
$ref: './node_modules/@auditmation/types-core/schema/tokenConnectionState.yml'
```

### Pattern 3: OAuth with Refresh Token

```yaml
# connectionProfile.yml
$ref: './node_modules/@auditmation/types-core/schema/oauthTokenProfile.yml'

# connectionState.yml
$ref: './node_modules/@auditmation/types-core/schema/oauthTokenState.yml'
```

### Pattern 4: Custom Fields (Extend Core)

```yaml
# connectionProfile.yml - Add organizationId
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/tokenProfile.yml'
  - type: object
    required: [organizationId]
    properties:
      organizationId:
        type: string
        description: Organization identifier for API access

# connectionState.yml - Add extra state
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/tokenConnectionState.yml'
  - type: object
    properties:
      organizationName:
        type: string
        description: Cached organization name
```

## Connection Profile Scope

### What Belongs in connectionProfile

**ONLY connection parameters - minimal set needed to CONNECT**

```yaml
# ✅ GOOD - Connection parameters
- token / apiKey / clientId / clientSecret
- baseUrl (if API has multiple environments)
- organizationId (if required to authenticate)

# ❌ BAD - Operation parameters
- limit (pagination parameter)
- projectId (operation scope, not connection scope)
- fields (query parameter)
```

**Rule**: If you can connect WITHOUT it, it's an operation parameter (not profile)

### Check for Additional Optional Parameters

**Always review API docs for environment-specific optional parameters:**

```yaml
# Example: Service has optional region parameter
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/tokenProfile.yml'
  - type: object
    properties:
      region:
        type: string
        description: Optional region for multi-region deployments
        enum: [us-east-1, eu-west-1, ap-southeast-1]
    # region is optional, but include it if API docs mention it
```

**Don't omit parameters that some environments might need!**

## 🚨 CRITICAL: Check Parent Schema First

**Before adding ANY property, check what the parent schema provides:**

```bash
# Check what tokenProfile.yml provides
cat node_modules/@auditmation/types-core/schema/tokenProfile.yml

# Check what basicConnection.yml provides
cat node_modules/@auditmation/types-core/schema/basicConnection.yml

# Check what baseConnectionState.yml provides
cat node_modules/@auditmation/types-core/schema/baseConnectionState.yml
```

### Avoid Semantic Duplication

```yaml
# ❌ WRONG - basicConnection already has uri
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/basicConnection.yml'
  - type: object
    properties:
      url:    # Duplicate! basicConnection has uri
        type: string

# ✅ CORRECT - Use parent's uri, or extend if truly different
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/basicConnection.yml'
  # uri is already provided by basicConnection
```

**Semantic duplicates to avoid:**
- url / uri / baseUrl
- token / accessToken
- username / user / userName
- password / pass / pwd

## 🚨 CRITICAL: ALWAYS Check Product Documentation

**Before finalizing connectionProfile, check product docs for ALL auth parameters:**

```yaml
# Example: Missing mfaCode from product docs
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/basicConnection.yml'
  - type: object
    properties:
      mfaCode:    # Found in product docs!
        type: string
        description: Multi-factor authentication code (optional)
```

**Don't assume - verify:**
1. Read product documentation authentication section
2. Look for optional parameters (region, environment, mfaCode, etc.)
3. Include ALL mentioned parameters (even if optional)
4. Don't omit parameters some environments might need

## 🚨 CRITICAL: Connection Scope MUST NOT Limit Operations

**NEVER add organization/project/workspace IDs to connection:**

```yaml
# ❌ WRONG - Limits connection to single organization
connectionState:
  allOf:
    - $ref: './node_modules/@auditmation/types-core/schema/baseConnectionState.yml'
    - type: object
      properties:
        accessToken:
          type: string
        organizationId:    # NO! Limits scope
          type: string

# ✅ CORRECT - Connection works across all organizations
connectionState:
  allOf:
    - $ref: './node_modules/@auditmation/types-core/schema/baseConnectionState.yml'
    - type: object
      properties:
        accessToken:
          type: string
  # organizationId is operation parameter, NOT connection parameter
```

**WHY**: Connection should be reusable across all scopes. Use operation parameters for scope.

**Scope identifiers belong in operation parameters, NOT connection:**
- ❌ organizationId in connection
- ❌ workspaceId in connection
- ❌ projectId in connection
- ❌ teamId in connection
- ✅ These are operation parameters (use in API paths)

## 🚨 CRITICAL: Only Add Used Fields (for connectionState)

**For connectionState - don't add fields "just in case" - only add what's actually USED:**

```yaml
# ❌ WRONG - identityId not used anywhere
connectionState:
  properties:
    accessToken: string
    identityId: string    # Where is this used? Nowhere!

# ✅ CORRECT - Only fields that are actually used
connectionState:
  properties:
    accessToken: string
  # If connect() doesn't return identityId, don't add it
```

**Ask:**
1. Does connect() method return this field?
2. Do operations use this field?
3. Is it needed for refresh/reconnect?
If NO to all → don't add it

**For connectionProfile - include environment-optional fields:**

```yaml
# ✅ CORRECT - Include optional fields that some environments need
allOf:
  - $ref: './node_modules/@auditmation/types-core/schema/tokenProfile.yml'
  - type: object
    properties:
      region:
        type: string
        description: Optional region (needed in some deployments)
      mfaCode:
        type: string
        description: Multi-factor authentication code (optional)
    # These aren't required, but include them if product docs mention them
```

**connectionProfile vs connectionState:**
- **connectionProfile**: Include optional fields that might be needed in some environments (region, mfaCode, etc.)
- **connectionState**: Only fields actually used by connect() or operations

## Validation Checklist

Before finalizing connection schemas:

- [ ] **Checked parent schema** - no semantic duplicates (url/uri, token/accessToken)
- [ ] **Checked product docs thoroughly** - all auth parameters included (mfaCode, region, etc.)
- [ ] connectionProfile extends a core profile (NOT custom)
- [ ] connectionState extends baseConnectionState (includes expiresIn)
- [ ] expiresIn is in seconds (integer), not expiresAt timestamp
- [ ] If refresh capability: state extends oauthTokenState
- [ ] If simple token: state extends tokenConnectionState
- [ ] Custom fields use allOf to extend core
- [ ] All required fields marked as required
- [ ] Checked API docs for optional connection parameters (region, environment, etc.)
- [ ] Profile contains ONLY connection parameters (not operation parameters)
- [ ] **NO scope limitation** - no organizationId/projectId/workspaceId in connection
- [ ] **Only used fields** - every state field is actually used by connect() or operations
- [ ] Minimal set needed to connect (don't add operation scope parameters)

## Common Mistakes

### ❌ Creating Custom Profile
```yaml
# DON'T DO THIS
type: object
properties:
  apiKey: string
  baseUrl: string
```
**Fix**: Extend tokenProfile.yml

### ❌ Missing baseConnectionState
```yaml
# DON'T DO THIS
type: object
properties:
  accessToken: string
```
**Fix**: Extend baseConnectionState or tokenConnectionState

### ❌ Using expiresAt Instead of expiresIn
```yaml
# DON'T DO THIS
expiresAt:
  type: string
  format: date-time
```
**Fix**: Convert to expiresIn (seconds) in connect() method

### ❌ No expiresIn for Refresh Tokens
```yaml
# DON'T DO THIS
properties:
  accessToken: string
  refreshToken: string
  # Missing expiresIn!
```
**Fix**: MUST extend baseConnectionState for expiresIn

## Remember

1. **Always extend core profiles** - Never create custom from scratch
2. **Always extend baseConnectionState** - Server needs expiresIn for cronjobs
3. **expiresIn in seconds** - Not timestamps, not milliseconds
4. **Use allOf for extensions** - Add custom fields via composition
5. **Receive data from @credential-manager** - Don't guess auth method

---

**Connection schemas are YAML schemas - design them like api.yml schemas!**
