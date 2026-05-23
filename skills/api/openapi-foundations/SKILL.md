---
name: openapi-foundations
description: OpenAPI core rules 1-10 covering servers, naming, parameters, and basic patterns
---

# API Specification - Core Rules (Rules 1-10)

**🚨 CRITICAL RULES - Immediate Task Failure if Violated**

These are the foundational rules that EVERY agent working with API specifications must know.

## Rule 1: No Root Level Servers or Security

```yaml
# ❌ WRONG
servers:
  - url: https://api.example.com
security:
  - bearerAuth: []

# ✅ CORRECT - Clean root level
openapi: 3.0.0
info:
  title: Service API
```

**Rationale**: Module determines these dynamically from connection profile.

## Rule 2: Resource Naming Consistency

- Choose ONE term for each resource type
- Use it EVERYWHERE consistently throughout the spec

```yaml
# ✅ CORRECT - Consistent naming
/users
/users/{userId}
/users/{userId}/profile

# ❌ WRONG - Inconsistent
/users
/user/{id}        # Mixed: users vs user
/users/{userId}/userProfile  # Redundant: user appears twice
```

**IMPORTANT**: Use meaningful, standard resource names regardless of vendor API naming.

```yaml
# ✅ CORRECT - Meaningful resource names
/organizations/{organizationId}/users
/organizations/{organizationId}/groups/{groupId}/members

# ❌ WRONG - Don't copy vendor abbreviations
/orgs/{orgId}/users              # NO! Use full word "organizations"
/o/{oid}/u/{uid}                 # NO! Use descriptive names
```

**URL Pattern Standard - Parent Context Rule**:

Use the appropriate path pattern based on whether the resource needs a parent context:

```yaml
# ✅ CORRECT - Resource with NO parent context needed
/accessToken                     # Standalone resource (current user's token)
/profile                         # Standalone resource (current user's profile)
/settings                        # Standalone resource (account settings)

# ✅ CORRECT - Resource WITH parent context that needs ID
/organizations/{organizationId}/users              # Users need organization context
/users/{userId}/repositories/{repositoryId}        # Repository needs user context
/projects/{projectId}/tasks/{taskId}              # Task needs project context

# ❌ WRONG - Unnecessary parent path when no ID needed
/auth/accessToken                # NO! Just use /accessToken
/users/profile                   # NO! Just use /profile (if it's current user)
```

**Decision Rule**:
- **Use `/resource`**: When the resource is standalone OR operates on "current" context (current user, current token, etc.)
- **Use `/parent/{parentId}/resource`**: When the resource exists within a parent that must be identified by an ID parameter

**Pattern**: `/resources/{resourceId}/subResources/{subResourceId}` format with meaningful, descriptive names. The vendor API may use different patterns - we normalize to our standard.

## Rule 3: Complete Operation Coverage

- ALL operations from requirements MUST be implemented as API endpoints
- NO operations can be skipped
- If an operation cannot be implemented, STOP and report

## Rule 4: Parameter Reuse via Components

If a parameter appears in 2+ operations → MUST go in `components/parameters`

```yaml
# ✅ CORRECT
components:
  parameters:
    limitParam:
      name: limit
      in: query
      schema:
        type: integer

paths:
  /users:
    get:
      parameters:
        - $ref: '#/components/parameters/limitParam'
  /groups:
    get:
      parameters:
        - $ref: '#/components/parameters/limitParam'
```

## Rule 5: Property Naming - camelCase ONLY

**NO EXCEPTIONS** - Even if external API uses snake_case

```yaml
# ✅ CORRECT
properties:
  userName:
    type: string
  createdAt:
    type: string
  avatarUrl:
    type: string

# ❌ WRONG - snake_case
properties:
  user_name:     # NO!
    type: string
  created_at:    # NO!
    type: string
```

**Critical**: Convert ALL external API snake_case properties to camelCase in schemas.

## Rule 6: Sorting Parameters Standard Names

NEVER use sortBy, sortDir, sort, or variations - ALWAYS use:

```yaml
# ✅ CORRECT
parameters:
  - name: orderBy
    schema:
      type: string
  - name: orderDir
    schema:
      type: string
      enum: [asc, desc]

# ❌ WRONG
parameters:
  - name: sortBy      # NO! Use orderBy
  - name: sortDir     # NO! Use orderDir
  - name: sort        # NO! Use orderBy
```

## Rule 7: Path Parameters - Descriptive Names

Path parameters MUST indicate resource type

```yaml
# ✅ CORRECT
/resources/{resourceId}
/items/{itemId}/subitems/{subitemId}
/users/{userId}/repositories/{repositoryId}

# ❌ WRONG - Not descriptive
/resources/{id}           # Which ID?
/items/{itemId}/subitems/{id}  # Confusing
```

## Rule 8: Resource Identifier Priority

When choosing the primary identifier:
1. `id` (if exists and unique)
2. `name` (if unique)
3. Other unique field (handle, key, etc.)

Always prefer `id` when available for operations.

## Rule 9: Parameters - No Connection Context

Operations MUST NOT include parameters available from ConnectionProfile or ConnectionState

```yaml
# ❌ FORBIDDEN - These come from connection
parameters:
  - name: apiKey           # NO! In ConnectionProfile
    in: header
  - name: token            # NO! In ConnectionProfile/State
    in: header
  - name: baseUrl          # NO! In ConnectionProfile
    in: query

# ✅ CORRECT - Scope and operation-specific parameters
/organizations/{organizationId}/resources/{resourceId}:
  get:
    parameters:
      - name: organizationId   # YES! Scope parameter (connection must NOT limit scope)
        in: path
      - name: resourceId       # YES! Operation-specific
        in: path
      - name: includeDetails   # YES! Operation option
        in: query
```

**WHY**: Connection context (apiKey, token, baseUrl) is established during connect() and managed by the client. Operations define business parameters AND scope parameters (organizationId, workspaceId, projectId, etc.) because connection must not limit operational scope.

## Rule 10: Tags - Lowercase Singular Nouns Only

```yaml
# ✅ CORRECT
tags:
  - user
  - group
  - account
  - access

# ❌ WRONG - Capitalized or plural
tags:
  - User     # NO! Use lowercase
  - Users    # NO! Use singular
  - Access   # NO! Use lowercase
```

---

## Quick Validation Checklist

Before proceeding with API spec work, verify:

- [ ] No `servers` or `security` at root level
- [ ] ONE consistent term chosen for each resource type
- [ ] ALL required operations are included
- [ ] Reused parameters are in `components/parameters`
- [ ] ALL properties use camelCase
- [ ] Sorting uses `orderBy` and `orderDir`
- [ ] Path parameters are descriptive (`{resourceId}` not `{id}`)
- [ ] Using `id` as primary identifier (when available)
- [ ] NO connection auth parameters (apiKey, token, baseUrl) but YES scope parameters (organizationId, workspaceId)
- [ ] Tags are lowercase singular nouns

---

**These 10 core rules apply to ALL API specification work. Violation of any rule = immediate task failure.**
