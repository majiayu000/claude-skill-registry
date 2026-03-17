---
name: openapi-schemas
description: OpenAPI schema rules 14-24 for response models, nullable handling, and data modeling
---

# API Specification - Schemas (Rules 14-24)

**Schema design, response patterns, and data modeling**

## Rule 14: Response Schema - Main Business Object Only

**Response schemas MUST map directly to the main business object, NOT envelope/wrapper objects**

```yaml
# ❌ WRONG - Includes envelope (status, data, meta)
responses:
  '200':
    schema:
      type: object
      properties:
        status: { type: string }
        data: { $ref: '#/components/schemas/User' }
        meta: { type: object }

# ✅ CORRECT - Direct reference to main business object
responses:
  '200':
    schema:
      $ref: '#/components/schemas/User'

# ✅ CORRECT - Array of main business objects
responses:
  '200':
    schema:
      type: array
      items:
        $ref: '#/components/schemas/User'
```

**WHY**: Framework handles status/metadata separately. Mappers extract main object from API envelope.

## Rule 15: No nullable in API Specification

**🚨 CRITICAL: NEVER use nullable in api.yml**

```yaml
# ❌ FORBIDDEN
properties:
  name:
    type: string
    nullable: true       # NO! Never use nullable

# ✅ CORRECT - Optional without nullable
properties:
  name:
    type: string         # Optional = not in required array
```

**WHY**: TypeScript uses `| undefined` for optional fields. Mappers convert null → undefined.

## Rule 16: ID Fields - String Type Only

**ALL ID fields MUST use `type: string`** even if external API uses numbers

```yaml
# ✅ CORRECT
properties:
  id: { type: string }
  userId: { type: string }
  organizationId: { type: string }

# ❌ WRONG
properties:
  id: { type: integer }    # NO! Always use string
```

**Rationale**: IDs are identifiers not quantities - prevents precision/overflow issues.

## Rule 17: Path Plurality Matches Operation Type

```yaml
# ✅ CORRECT - List operation uses plural path
/resources:
  get:
    operationId: listResources

# ✅ CORRECT - Get operation uses singular path
/resources/{resourceId}:
  get:
    operationId: getResource

# ❌ WRONG - Mismatch
/resource:
  get:
    operationId: listResources    # List but singular path!
```

## Rule 18: Clean Path Structure - Resource-Based Only

```yaml
# ✅ CORRECT - Clean resource paths
/users
/users/{userId}
/users/{userId}/repositories
/users/{userId}/repositories/{repositoryId}

# ❌ WRONG - External API style paths
/api/v1/users                    # NO! No /api/v1 prefix
/{owner}/{repo}/issues           # NO! Use /repositories/{repositoryId}/issues
/users/{username}/repos          # NO! Use userId not username in path
```

**Rationale**: Module creates clean, consistent resource-based paths regardless of external API structure.

## Rule 19: Nested Objects Must Use $ref

```yaml
# ✅ CORRECT - Nested object uses $ref
properties:
  owner:
    $ref: '#/components/schemas/User'
  repository:
    $ref: '#/components/schemas/Repository'

# ❌ WRONG - Inline nested object
properties:
  owner:
    type: object
    properties:
      id: { type: string }
      name: { type: string }
```

**WHY**: Reusability, maintainability, and type safety.

## Rule 20: Schema Name Conflict Check When Adding Operations

When adding new operations, check if response schemas already exist in the spec. If YES and schemas differ:

```yaml
# Scenario: Adding "getAccessToken" but "AccessToken" schema exists
# with different structure than new operation needs

# Option 1: Use existing if compatible
responses:
  '200':
    schema:
      $ref: '#/components/schemas/AccessToken'

# Option 2: Create operation-specific schema if incompatible
components:
  schemas:
    AccessTokenDetails:    # New schema for this specific operation
      properties:
        token: { type: string }
        expiresIn: { type: integer }
        # ... different from existing AccessToken
```

**WHY**: Prevents breaking existing operations when adding new ones.

## Rule 21: Never Update Connection Profile During Operation Implementation

**🚨 CRITICAL**: When implementing operations, NEVER modify connectionProfile.yml or connectionState.yml

```
# ❌ WRONG Flow
1. Implementing getAccessToken operation
2. Notice we need to store refreshToken
3. Add refreshToken to connectionState.yml    # NO! STOP!

# ✅ CORRECT Flow
1. Implementing getAccessToken operation
2. Notice we need refreshToken
3. STOP and report: "connectionState needs refreshToken field"
4. User reviews and updates connection schemas
5. Resume operation implementation
```

**WHY**: Connection profile changes affect ALL operations. Must be reviewed separately.

## Rule 22: Enum Fields - Keep Original API Values (Case Normalization Allowed)

**CRITICAL**: Enum values MUST preserve the semantic meaning from the external API. Case normalization to snake_case is allowed, but semantic transformation is forbidden.

```yaml
# ✅ CORRECT - Case normalization (ActiveUser → active_user)
status:
  type: string
  enum: [active_user, suspended_user, inactive_user]  # snake_case normalized
  x-enum-descriptions:
    active_user: User account is active and can be used
    suspended_user: User account has been suspended
    inactive_user: User account is inactive

# ✅ CORRECT - Original values when already simple
status:
  type: string
  enum: [A, S, I]  # Keep as-is when API uses codes
  x-enum-descriptions:
    A: Active - Account is active and can be used
    S: Suspended - Account has been suspended
    I: Inactive - Account is inactive

# ✅ CORRECT - Already snake_case from API
status:
  type: string
  enum: [active, pending, suspended]  # Already snake_case
  x-enum-descriptions:
    active: Account is active and can be used
    pending: Account is awaiting activation
    suspended: Account has been suspended

# ❌ WRONG - Semantic transformation (changing meaning)
status:
  type: string
  enum: [active, suspended, inactive]  # NO! API returns A/S/I - semantic change!
  description: Status values

# ❌ WRONG - Adding prefixes/suffixes not in API
type:
  type: string
  enum: [user_admin, user_member]  # NO! If API returns admin/member, don't add user_ prefix
```

**Allowed transformations:**
- ✅ Case normalization: `ActiveUser` → `active_user`
- ✅ Case normalization: `PENDING` → `pending`
- ✅ Case normalization: `Suspended-User` → `suspended_user`

**Forbidden transformations:**
- ❌ Semantic changes: `A` → `active` (code to word)
- ❌ Value expansion: `admin` → `user_admin` (adding prefix)
- ❌ Value contraction: `active_user` → `active` (removing suffix)
- ❌ Synonym replacement: `inactive` → `disabled` (different word)

**WHY**:
- **Predictable mapping** - Case normalization is mechanical and reversible
- **No semantic loss** - Value meaning preserved, just normalized format
- **Simpler mappers** - `toEnum()` default snake_case transformation handles it
- **x-enum-descriptions** - Provides documentation without changing values

**Mapper behavior**:
```typescript
// ✅ GOOD - Case normalization (toEnum default behavior)
// API returns: "ActiveUser"
// Schema has: "active_user"
status: toEnum(UserInfo.StatusEnum, raw.status)  // toEnum converts to snake_case

// ✅ GOOD - No transformation needed
// API returns: "active"
// Schema has: "active"
status: toEnum(UserInfo.StatusEnum, raw.status)  // Direct match

// ❌ BAD - Semantic transformation required
// API returns: "A"
// Schema has: "active"
status: toEnum(UserInfo.StatusEnum, raw.status, (apiValue: string) => {
  const statusMap = { A: 'active', S: 'suspended', I: 'inactive' };  // NO!
  return statusMap[apiValue] || 'active';
})
```

## Rule 23: Complete Response Model Mapping

Every response schema property must map to external API field:

```yaml
# ✅ COMPLETE - All fields documented
User:
  properties:
    id:
      type: string          # Maps to: id
    name:
      type: string          # Maps to: display_name
    email:
      type: string          # Maps to: email_address
    createdAt:
      type: string          # Maps to: created_at
```

## Rule 24: Schema Context Separation - Summary vs Full

When a schema is used in BOTH nested contexts AND as direct response, consider separating:

```yaml
# ✅ GOOD - Separate Summary and Full schemas
components:
  schemas:
    UserSummary:        # For nested usage (10+ properties)
      properties:
        id: { type: string }
        name: { type: string }
        email: { type: string }

    User:               # For direct response (full details)
      allOf:
        - $ref: '#/components/schemas/UserSummary'
        - properties:
            bio: { type: string }
            location: { type: string }
            # ... 20+ more properties

# Usage:
/users/{userId}:
  get:
    responses:
      '200':
        schema:
          $ref: '#/components/schemas/User'    # Full details

/organizations/{orgId}:
  get:
    responses:
      '200':
        schema:
          properties:
            owner:
              $ref: '#/components/schemas/UserSummary'  # Nested = summary
```

**WHEN**: Schema used in BOTH contexts AND has 10+ properties
**WHY**: Avoids circular references, reduces payload size for nested usage

---

## Schema Design Checklist

Before finalizing schemas:

- [ ] Responses reference main business object (NOT envelope)
- [ ] NO `nullable` anywhere in api.yml
- [ ] ALL IDs use `type: string`
- [ ] Path plurality matches operation type
- [ ] Paths are clean resource-based (no /api/v1, no external patterns)
- [ ] Nested objects use $ref (NOT inline)
- [ ] Checked for schema name conflicts with existing schemas
- [ ] NOT modifying connectionProfile/connectionState during operation work
- [ ] Enums preserve semantic meaning (snake_case normalization OK, semantic changes forbidden) with x-enum-descriptions
- [ ] All schema properties documented with external API mapping
- [ ] Large schemas (10+ props) separated into Summary/Full when used in both contexts

---

**These schema rules ensure clean, reusable, and maintainable data models.**

## Schema Naming Conventions

**Resource schema naming must be consistent and make sense for the resource.**

### Valid Naming Suffixes

- **Base** - Common properties shared between Resource and ResourceInfo/ResourceSummary (NOT returned by APIs)
- **Info** - Extended version with additional context/metadata
- **Summary** - Lightweight version for nested usage
- **Ref** - Reference with minimal fields (usually id + name)
- **No suffix** - The main resource schema

```yaml
# ✅ CORRECT - Consistent with resource name
Configuration:           # Main resource
  properties:
    id: { type: string }
    name: { type: string }
    settings: { type: object }

ConfigurationBase:       # Common properties (not returned by API)
  properties:
    id: { type: string }
    name: { type: string }

ConfigurationInfo:       # Extended with org context
  allOf:
    - $ref: '#/components/schemas/Configuration'
    - properties:
        org: { $ref: '#/components/schemas/OrganizationRef' }

ConfigurationSummary:    # Lightweight for nested usage
  properties:
    id: { type: string }
    name: { type: string }

# ❌ WRONG - Non-standard suffixes
ConfigurationDetails:    # Invalid - use Configuration or ConfigurationInfo
ConfigurationSettings:   # Invalid - 'Settings' not a standard suffix
ConfigurationData:       # Invalid - 'Data' not a standard suffix
```

**Rule**: If your resource is named `Configuration`, then `ConfigurationInfo`, `ConfigurationSummary`, `ConfigurationBase` are valid. Stay consistent across the entire API.

### Base Schema Usage

**Base schemas:**
- Contain common properties between Resource and ResourceInfo/ResourceSummary
- Should NEVER be returned by any API operation
- Used only for composition with `allOf`

```yaml
# ✅ CORRECT - Base for composition only
UserBase:
  properties:
    id: { type: string }
    status: { type: string }

User:
  allOf:
    - $ref: '#/components/schemas/UserBase'
    - properties:
        email: { type: string }

UserInfo:
  allOf:
    - $ref: '#/components/schemas/UserBase'
    - properties:
        org: { $ref: '#/components/schemas/OrganizationRef' }

# ❌ WRONG - Base returned by API
/users/{userId}:
  get:
    responses:
      '200':
        schema:
          $ref: '#/components/schemas/UserBase'  # NO! Use User or UserInfo
```

## Schema Design Patterns

### Pattern 1: Base + Extension (Composition)

```yaml
components:
  schemas:
    ResourceBase:
      type: object
      properties:
        id:
          type: string
          format: uuid
        createdAt:
          type: string
          format: date-time

    Resource:
      allOf:
        - $ref: '#/components/schemas/ResourceBase'
        - type: object
          properties:
            name:
              type: string
            description:
              type: string
```

**When to use:** Common properties shared across multiple schemas

### Pattern 2: Context Separation (Summary vs Full)

```yaml
# For nested usage (lightweight)
WebhookSummary:
  type: object
  required: [id, name, active]
  properties:
    id:
      type: string
    name:
      type: string
    active:
      type: boolean

# For direct endpoint responses (full details)
Webhook:
  allOf:
    - $ref: '#/components/schemas/WebhookSummary'
    - type: object
      properties:
        config:
          $ref: '#/components/schemas/WebhookConfig'
        events:
          type: array
          items:
            type: string
        createdAt:
          type: string
          format: date-time
```

**When to use:** Schema used in BOTH nested and direct contexts, 10+ properties

### Pattern 3: Nested Object $ref (REQUIRED)

```yaml
# ❌ WRONG - Inline nested object
Webhook:
  type: object
  properties:
    config:
      type: object  # NO!
      properties:
        url: { type: string }

# ✅ CORRECT - Use $ref
Webhook:
  type: object
  properties:
    config:
      $ref: '#/components/schemas/WebhookConfig'

WebhookConfig:
  type: object
  properties:
    url:
      type: string
      format: uri
```

**Always required:** ALL nested objects MUST use $ref

### Pattern 4: Format Application

```yaml
properties:
  id:
    type: string
    format: uuid        # ✅ For UUIDs
  createdAt:
    type: string
    format: date-time   # ✅ For timestamps
  website:
    type: string
    format: uri         # ✅ For URLs
  email:
    type: string
    format: email       # ✅ For emails
```

See type-mapping skill for complete format reference.

## Schema Validation Scripts

### Check for Inline Schemas in Responses

```bash
# No inline schemas in responses
yq eval '.paths.*.*.responses.*.content.*.schema | select(has("properties"))' api.yml
# Should only return $ref or array items
```

### Check All Nested Objects Use $ref

```bash
# All nested objects use $ref
grep -A 5 "type: object" api.yml | grep -B 2 "properties:" | grep -v "\$ref"
# Should return minimal matches (only root schemas)
```

### Check for Nullable Usage (FORBIDDEN)

```bash
# No nullable usage (CRITICAL)
grep "nullable:" api.yml
# Must return nothing
# WHY: We transform null values to undefined in mappers, not via nullable in schema
```

### Check Format Application

```bash
# Formats applied
yq eval '.. | select(has("format")) | .format' api.yml
# Should show: uuid, date-time, uri, email
```

### Check Schema Context Separation

```bash
# Check if any schema used in BOTH nested and direct contexts
# Manual review required - look for schemas referenced in multiple places
grep -r "ref.*schemas/User" api.yml
```

## Schema Design Workflow

1. **Identify unique objects** in API responses
2. **Create base schemas** for common properties
3. **Use allOf** for composition
4. **Never duplicate properties** across schemas
5. **Apply formats consistently** (uuid, date-time, uri, email)
6. **Separate schemas by context** (Summary vs Full when needed)
7. **Validate no inline schemas** remain
8. **Document external API mapping** for each property

## Validation Checklist

Run these checks before finalizing schemas:

```bash
cd package/{vendor}/{service}

# 1. No inline schemas
yq eval '.paths.*.*.responses.*.content.*.schema | select(has("properties"))' api.yml

# 2. No nullable (CRITICAL)
grep "nullable:" api.yml
# Must be empty

# 3. All IDs are strings
yq eval '..| select(.properties.id) | .properties.id.type' api.yml
# All should be "string"

# 4. Nested objects use $ref
grep -A 5 "type: object" api.yml | grep -B 2 "properties:" | grep -v "\$ref"
# Minimal results

# 5. Formats applied
yq eval '.. | select(has("format")) | .format' api.yml | sort | uniq
# Should show format types used
```

## Success Metrics

Schema design is complete when:

- ✅ Zero inline schemas in responses
- ✅ No duplicate schema definitions
- ✅ Proper format application (uuid, date-time, uri, email)
- ✅ Clean composition with allOf
- ✅ Context-appropriate schemas (Summary vs Full where needed)
- ✅ All nested objects use $ref
- ✅ **No nullable in spec** (null → undefined happens in mappers)
- ✅ All IDs use type: string
- ✅ Clean resource-based paths
- ✅ External API mapping documented
