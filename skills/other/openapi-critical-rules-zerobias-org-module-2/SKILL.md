---
name: openapi-critical-rules
description: The 12 critical OpenAPI rules that cause immediate task failure if violated
---

# 12 Critical API Specification Rules

These 12 rules cause IMMEDIATE TASK FAILURE if violated.

## Rule 1: Root Level Restrictions

**FORBIDDEN** at root level in api.yml:
- `servers:` - NO server configuration at root
- `security:` - NO security at root
- `securitySchemes:` - Belongs in components only

```yaml
# ❌ WRONG
servers:
  - url: https://api.example.com

security:
  - bearerAuth: []

# ✅ CORRECT - Clean root, security in components
openapi: 3.0.0
info:
  title: Service API
paths:
  ...
components:
  securitySchemes:
    ...
```

**WHY**: Root-level servers and security conflict with hub's connection management.

## Rule 2: Resource Naming Consistency

**MANDATORY**: Singular nouns for tags and schemas

```yaml
# ✅ CORRECT
tags:
  - name: user
  - name: organization
  - name: webhook

components:
  schemas:
    User:
      ...
    Organization:
      ...

# ❌ WRONG
tags:
  - name: users    # NO - use singular
  - name: orgs     # NO - use full word
```

**WHY**: Consistent naming convention across all modules.

## Rule 3: Operation Coverage

**MANDATORY**: ALL operations from product analysis MUST be in API spec

**Process**:
1. Product specialist identifies N operations
2. API architect MUST include all N operations
3. Zero operations may be skipped

**Validation**:
```bash
# Count operations in api.yml
yq eval '.paths.*.* | select(has("operationId")) | .operationId' api.yml | wc -l

# Compare with product analysis count
```

**IF MISMATCH**: Add missing operations or document why excluded.

## Rule 4: Parameter Reuse

**RULE**: If 2+ operations use same parameter → Move to components

```yaml
# ✅ CORRECT - Reusable parameter
components:
  parameters:
    userId:
      name: userId
      in: path
      required: true
      schema:
        type: string

paths:
  /users/{userId}:
    get:
      parameters:
        - $ref: '#/components/parameters/userId'
  /users/{userId}/profile:
    get:
      parameters:
        - $ref: '#/components/parameters/userId'

# ❌ WRONG - Duplicate definition
paths:
  /users/{userId}:
    get:
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
  /users/{userId}/profile:
    get:
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
```

**WHY**: DRY principle, consistency, easier updates.

## Rule 5: Property Naming - camelCase ONLY

**MANDATORY**: ALL properties in camelCase

```yaml
# ✅ CORRECT
User:
  properties:
    userId:
      type: string
    firstName:
      type: string
    createdAt:
      type: string
      format: date-time

# ❌ WRONG
User:
  properties:
    user_id:        # NO - snake_case
      type: string
    first_name:     # NO - snake_case
      type: string
    created-at:     # NO - kebab-case
      type: string
```

**Validation**:
```bash
# Check for snake_case (should return nothing)
grep "_" api.yml | grep -v "x-" | grep -v "#"
```

**WHY**: TypeScript/JavaScript convention, generated code uses camelCase.

## Rule 6: Parameter Naming - orderBy/orderDir

**MANDATORY**: Sorting parameters use these exact names

```yaml
# ✅ CORRECT
parameters:
  - name: orderBy
    in: query
    schema:
      type: string
      enum: [name, createdAt, updatedAt]
  - name: orderDir
    in: query
    schema:
      type: string
      enum: [asc, desc]
      default: asc

# ❌ WRONG
parameters:
  - name: sortBy        # NO - use orderBy
  - name: sortField     # NO - use orderBy
  - name: direction     # NO - use orderDir
  - name: order         # NO - use orderDir
```

**WHY**: Framework expects these exact parameter names.

## Rule 7: Path Parameters - Descriptive Types

**MANDATORY**: Path parameters use descriptive names

```yaml
# ✅ CORRECT
/users/{userId}
/organizations/{organizationId}
/webhooks/{webhookId}

# ❌ WRONG
/users/{id}           # NO - not descriptive enough
/organizations/{org}  # NO - use full word
/webhooks/{wid}       # NO - no abbreviations
```

**WHY**: Clear, self-documenting paths. Prevents parameter conflicts.

## Rule 8: Resource Identifier Priority

**MANDATORY**: Use this order for resource identification:

1. `id` (UUID, integer, string ID)
2. `name` (if unique identifier)
3. Other unique fields

```yaml
# ✅ CORRECT - Using id (preferred)
/users/{userId}

# ✅ ACCEPTABLE - Using name (if no id)
/templates/{templateName}

# ❌ WRONG - Using non-unique field
/users/{email}  # Email can change, not stable ID
```

**WHY**: Stable identifiers for API operations.

## Rule 9: Tags - Singular Nouns

**MANDATORY**: Tags are singular nouns matching resource name

```yaml
# ✅ CORRECT
paths:
  /users:
    get:
      tags:
        - user    # Singular
  /users/{userId}:
    get:
      tags:
        - user    # Singular

# ❌ WRONG
paths:
  /users:
    get:
      tags:
        - users   # NO - use singular
        - Users   # NO - lowercase
```

**WHY**: Consistent tag naming, generates clean Producer class names.

## Rule 10: Method Naming - operationId vs x-method-name

**PATTERN**:
- `operationId`: Full descriptive ID (getUser, listUsers, createUser)
- `x-method-name`: Actual TypeScript method name (must match operationId pattern)

```yaml
# ✅ CORRECT
paths:
  /users/{userId}:
    get:
      operationId: getUser
      x-method-name: getUser
      summary: Retrieve user by ID

  /users:
    get:
      operationId: listUsers
      x-method-name: listUsers
      summary: Retrieve list of users

# ❌ WRONG
paths:
  /users/{userId}:
    get:
      operationId: describeUser    # NO - use 'get'
      x-method-name: get_user      # NO - camelCase
```

**VERBS**:
- `get` - Retrieve single resource
- `list` - Retrieve collection
- `search` - Query with filters
- `create` - Create new resource
- `update` - Modify existing resource
- `delete` - Remove resource

**WHY**: Consistent method naming, proper TypeScript generation.

## Rule 11: Pagination - pageTokenParam from Core

**MANDATORY**: Use core pagination parameter for token-based paging

```yaml
# ✅ CORRECT
paths:
  /users:
    get:
      parameters:
        - $ref: './node_modules/@zerobias-org/types-core/schema/pageTokenParam.yml'
        - name: pageSize
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20

# ❌ WRONG
parameters:
  - name: nextToken      # NO - use pageTokenParam
  - name: cursor         # NO - use pageTokenParam
  - name: continuationToken  # NO - use pageTokenParam
```

**WHY**: Framework expects standard pageToken parameter name.

## Rule 12: Response Codes - 200/201 ONLY

**MANDATORY**: ONLY success responses in API specification

```yaml
# ✅ CORRECT
responses:
  '200':
    description: User retrieved successfully
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'

# ❌ WRONG
responses:
  '200':
    description: Success
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  '401':    # NO - remove all error responses
    description: Unauthorized
  '404':    # NO - remove all error responses
    description: Not found
  '500':    # NO - remove all error responses
    description: Server error
```

**Validation**:
```bash
# Should return nothing
grep -E "'40[0-9]'|'50[0-9]'" api.yml
```

**WHY**: Framework handles errors automatically. Error responses in spec cause generation issues.

## Summary Table

| Rule # | Topic | Violation = Immediate Failure |
|--------|-------|------------------------------|
| 1 | Root Level Restrictions | ✅ Yes |
| 2 | Resource Naming | ✅ Yes |
| 3 | Operation Coverage | ✅ Yes |
| 4 | Parameter Reuse | ✅ Yes |
| 5 | Property Naming (camelCase) | ✅ Yes |
| 6 | Parameter Naming (orderBy/orderDir) | ✅ Yes |
| 7 | Path Parameters (descriptive) | ✅ Yes |
| 8 | Resource Identifier Priority | ✅ Yes |
| 9 | Tags (singular) | ✅ Yes |
| 10 | Method Naming (operationId) | ✅ Yes |
| 11 | Pagination (pageTokenParam) | ✅ Yes |
| 12 | Response Codes (200/201 only) | ✅ Yes |

## Validation Checklist

Before proceeding past Gate 1, verify ALL 12 rules:

- [ ] Rule 1: No servers/security at root
- [ ] Rule 2: Tags and schemas are singular nouns
- [ ] Rule 3: All product operations included
- [ ] Rule 4: Duplicate parameters moved to components
- [ ] Rule 5: All properties are camelCase
- [ ] Rule 6: Sorting uses orderBy/orderDir
- [ ] Rule 7: Path parameters are descriptive (userId not id)
- [ ] Rule 8: Using id > name > other for identification
- [ ] Rule 9: Tags are singular nouns
- [ ] Rule 10: operationId uses get/list/search/create/update/delete
- [ ] Rule 11: Pagination uses pageTokenParam from core
- [ ] Rule 12: ONLY 200/201 responses (no 4xx/5xx)

## Quick Validation Script

```bash
#!/bin/bash
# validate-12-rules.sh

FAILED=0

# Rule 5: Check camelCase
if grep "_" api.yml | grep -v "x-" | grep -v "#" > /dev/null 2>&1; then
  echo "❌ Rule 5 FAILED: snake_case found in properties"
  FAILED=1
fi

# Rule 10: Check for 'describe'
if grep -E "describe[A-Z]" api.yml > /dev/null 2>&1; then
  echo "❌ Rule 10 FAILED: 'describe' prefix found"
  FAILED=1
fi

# Rule 12: Check for error responses
if grep -E "'40[0-9]'|'50[0-9]'" api.yml > /dev/null 2>&1; then
  echo "❌ Rule 12 FAILED: Error responses found"
  FAILED=1
fi

if [ $FAILED -eq 0 ]; then
  echo "✅ Critical rules validation passed"
else
  echo "🚨 FIX ISSUES BEFORE PROCEEDING"
  exit 1
fi
```

## References

- Full API specification rules: @.claude/rules/api-spec-*.md
- Gate 1 validation: @.claude/rules/gate-1-api-spec.md
- API Architect agent: @.claude/agents/api-architect.md
