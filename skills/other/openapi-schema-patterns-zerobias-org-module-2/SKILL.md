---
name: openapi-schema-patterns
description: Advanced OpenAPI schema patterns including allOf, naming hierarchies, and context separation
---

# API Specification - Schema Patterns

**Rules for schema design patterns and naming conventions**

## Pattern 1: allOf with Single $ref for Description Override

### The Problem

OpenAPI ignores sibling properties when using `$ref`:

```yaml
# ❌ WRONG - Description is LOST by OpenAPI
items:
  $ref: '#/components/schemas/UserGroup'
  description: Groups the user belongs to  # OpenAPI IGNORES THIS!
```

### The Solution

Use `allOf` wrapper to preserve description:

```yaml
# ✅ CORRECT - Description is preserved
items:
  allOf:
    - $ref: '#/components/schemas/UserGroup'
  description: Groups the user belongs to  # This WORKS!
```

### When to Use

Use `allOf` with single `$ref` when you need to:
1. Add or override `description` on a referenced schema
2. Add additional metadata (example, deprecated, etc.)
3. Change any property that would be lost as sibling to `$ref`

### When NOT to Use

Do NOT use `allOf` for actual schema composition - that's a different pattern:

```yaml
# This is COMPOSITION (combining schemas) - different use case
UserInfo:
  allOf:
    - $ref: '#/components/schemas/User'
    - type: object
      properties:
        additionalField: string
```

---

## Pattern 2: Schema Naming Hierarchy

### Naming Convention

Schemas follow this hierarchy based on usage context:

| Pattern | When to Use | Contains | Example |
|---------|-------------|----------|---------|
| `<Resource>` | List operation results | Core fields for list view | `User`, `Group`, `Acu` |
| `<Resource>Info` | Get operation results (if different) | Full details, more than list | `UserInfo`, `AcuInfo` |
| `<Resource>Summary` | Nested references (detailed) | More than Ref, less than full | `UserSummary` |
| `<Resource>Ref` | Nested references (minimal) | Just id + name | `OrganizationRef`, `ZoneSiteRef` |
| `<Context><Resource>` | Resource within specific context | The **Resource** (2nd word) as viewed from **Context** (1st word) | `GroupUser` (User from Group), `ZoneEntry` (Entry from Zone) |

### Examples

```yaml
# List result - core fields
User:
  properties:
    id: string
    status: string
    email: string
    # 10-15 fields

# Get result - full details
UserInfo:
  allOf:
    - $ref: '#/components/schemas/User'
    - type: object
      properties:
        organizationId: string
        lastLoginAt: string
        customFields: object
        # Additional 5-10 fields

# Minimal reference - nested in other schemas
OrganizationRef:
  properties:
    id: string
    name: string

# Context-specific - User (resource type) as seen from Group (context)
# Read as: "A User, from the Group's perspective"
# Used when: /groups/{groupId}/users returns this
GroupUser:
  properties:
    id: string
    name: string
    email: string
    role: string  # Group-specific field (context-specific!)

# The SECOND word (User) tells you what type of resource this is
# The FIRST word (Group) tells you from which context you're viewing it
```

### Naming Rules

1. **Base Resource** (`User`, `Group`): Singular, PascalCase, used in list operations
2. **Info Variant** (`UserInfo`): Add `Info` suffix when get returns more fields than list
3. **Ref Variant** (`OrganizationRef`): Add `Ref` suffix for minimal nested references
4. **Summary Variant** (`UserSummary`): Add `Summary` for medium-detail nested references
5. **Context Prefix** (`GroupUser`): `<Context><Resource>` where **Resource (2nd word)** is what's returned, **Context (1st word)** is the perspective. So `GroupUser` returns a `User` as seen from `Group` context (NOT `UserGroup` which would return a Group!)

---

## Pattern 3: Follow Original API Naming (After camelCase)

**CRITICAL**: We wrap external APIs - we don't design from scratch. Follow vendor API naming after normalizing to camelCase.

### Field Names

```yaml
# If vendor API has: user_profile_picture
# ✅ CORRECT - Convert to camelCase
userProfilePicture:
  type: string

# ❌ WRONG - Don't rename semantically
avatarUrl:  # Don't change user_profile_picture to avatarUrl
  type: string
```

**Rule**: Convert snake_case/kebab-case to camelCase, but keep the semantic name from vendor API.

### Boolean Fields

```yaml
# If vendor API has: is_active, has_access, can_override
# ✅ CORRECT - Keep vendor prefixes
isActive: boolean
hasAccess: boolean
canOverride: boolean

# ❌ WRONG - Don't standardize prefixes if vendor doesn't
active: boolean  # Don't remove 'is' if vendor has it
```

**Rule**: Keep vendor's boolean naming convention (is/has/can/supports) exactly as they define it.

### Timestamp Fields

```yaml
# If vendor API has: created_at, last_login_time, status_updated
# ✅ CORRECT - Keep vendor naming
createdAt: string
lastLoginTime: string
statusUpdated: string

# ❌ WRONG - Don't standardize suffixes
createdAt: string
lastLoginAt: string  # Don't add 'At' if vendor uses 'time'
statusUpdatedAt: string  # Don't add 'At' if vendor omits it
```

**Rule**: Keep vendor's timestamp naming pattern. If they use `*_at`, use `*At`. If they use `*_time`, use `*Time`.

### Count Fields

```yaml
# If vendor API has: user_count, total_entries, num_zones
# ✅ CORRECT - Keep vendor naming
userCount: integer
totalEntries: integer
numZones: integer

# ❌ WRONG - Don't standardize to *Count
userCount: integer
entryCount: integer  # Don't change totalEntries
zoneCount: integer   # Don't change numZones
```

**Rule**: Keep vendor's count field naming (count/total/num) as they define it.

### Path Parameters

```yaml
# If vendor API uses: /users/{user_id}
# ✅ CORRECT
paths:
  /users/{userId}:
    parameters:
      - name: userId

# If vendor API uses: /templates/{template_name}
# ✅ CORRECT
paths:
  /templates/{templateName}:
    parameters:
      - name: templateName

# If vendor API uses: /roles/{role_arn}
# ✅ CORRECT
paths:
  /roles/{roleArn}:
    parameters:
      - name: roleArn
```

**Rule**: Use whatever identifier type the vendor API uses (id/name/arn/key). Convert to camelCase but keep semantic meaning.

### Security Scopes

```yaml
# If vendor API defines scopes as: user:read, group:write, admin-access
# ✅ CORRECT - Match exactly (or as close as possible)
securitySchemes:
  oauth:
    flows:
      authorizationCode:
        scopes:
          user:read: Read user information
          group:write: Write group information
          admin-access: Administrative access

# ❌ WRONG - Don't normalize scope format
securitySchemes:
  oauth:
    flows:
      authorizationCode:
        scopes:
          read:users: Read user information    # Changed format!
          write:groups: Write group information # Changed format!
          access:admin: Administrative access   # Changed format!
```

**Rule**: Security scopes must match vendor API exactly so users know what to request. Don't normalize format.

---

## Pattern 4: Free-Form Objects

When vendor API has truly dynamic/unknown structure objects:

```yaml
# If vendor API documents a field as "dynamic configuration object"
# ✅ CORRECT - Empty object
badgeConfig:
  type: object
  description: Badge configuration for the group

# ❌ WRONG - Don't add fake structure if vendor doesn't define it
badgeConfig:
  type: object
  properties:
    color: string  # Don't make this up!
  description: Badge configuration for the group
```

**Rule**: Use empty `type: object` for truly dynamic fields from vendor API. Don't invent structure.

---

## Summary Table

| Aspect | Rule | Example |
|--------|------|---------|
| allOf single ref | Use for description override | `allOf: [- $ref: Schema]` + description |
| Schema hierarchy | Resource/Info/Summary/Ref/ContextResource | UserInfo, OrganizationRef, GroupUser |
| Field names | Follow vendor (camelCase) | `userProfilePicture` not `avatarUrl` |
| Booleans | Follow vendor prefixes | Keep `is*/has*/can*` as vendor defines |
| Timestamps | Follow vendor suffixes | Keep `*At/*Time/*ed` as vendor defines |
| Counts | Follow vendor naming | Keep `*Count/total*/num*` as vendor defines |
| Path params | Follow vendor identifier type | Use `userId/userName/userArn` per vendor |
| Security scopes | Match vendor exactly | Don't normalize scope format |
| Free objects | Use `type: object` only | When vendor docs say "dynamic" |

---

## Validation Questions

Before finalizing schemas, ask:

1. **allOf usage**: Am I using `allOf` with single ref just to add description? (✅) Or for actual composition? (Different pattern)
2. **Schema naming**: Does this follow Resource/Info/Summary/Ref/ContextResource hierarchy?
3. **Field naming**: Did I check the vendor API docs for the exact field name?
4. **Prefixes/suffixes**: Am I keeping vendor's boolean/timestamp/count conventions?
5. **Path parameters**: Am I using the identifier type (id/name/arn) that vendor uses?
6. **Security scopes**: Do these match vendor docs exactly?
7. **Free objects**: Did vendor docs actually say this is dynamic, or should I define structure?

---

## Common Mistakes

### ❌ Mistake 1: Removing allOf "to simplify"
```yaml
# WRONG - Loses description
items:
  $ref: '#/components/schemas/User'
  description: Active users  # OpenAPI ignores this!
```

### ❌ Mistake 2: Wrong context order
```yaml
# WRONG - Should be GroupUser not UserGroup
UserGroup:  # This returns a GROUP (from user context)
  properties:
    groupId: string
    groupName: string

# CORRECT - Returns a USER (from group context)
GroupUser:  # This returns a USER (from group context)
  properties:
    userId: string
    userName: string
    role: string  # Group-specific
```

**Remember**: The **SECOND word** is the resource type being returned!

### ❌ Mistake 3: Normalizing vendor naming
```yaml
# If vendor API has: last_login_time
# WRONG
lastLoginAt: string  # Changed 'time' to 'At'
```

### ❌ Mistake 4: Inventing object structure
```yaml
# If vendor docs say "configuration object (dynamic)"
# WRONG
config:
  type: object
  properties:
    setting1: string  # Don't invent structure!
```

---

## References

- Core Rules: api-spec-core-rules skill
- Critical 12 Rules: @.claude/rules/api-specification-critical-12-rules.md
- Schema Rules: api-spec-schemas skill
