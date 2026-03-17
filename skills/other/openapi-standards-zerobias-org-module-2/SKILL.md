---
name: openapi-standards
description: OpenAPI standards and guidelines for professional API specifications
---

# API Specification - Standards & Guidelines

**Standard conventions, guidelines, and best practices for API specifications**

## 🟡 STANDARD RULES

### Operation Naming Conventions

Use ONLY these prefixes:

| Operation Type | Name | HTTP Method | Example |
|---------------|------|-------------|---------|
| Get single | `get{Resource}` | GET | `getUser` |
| List multiple | `list{Resources}` | GET | `listUsers` |
| Search with filters | `search{Resources}` | POST | `searchUsers` |
| Create new | `create{Resource}` | POST | `createUser` |
| Update existing | `update{Resource}` | PUT/PATCH | `updateUser` |
| Delete resource | `delete{Resource}` | DELETE | `deleteUser` |

**Forbidden prefixes**: describe, fetch, retrieve, find, query, add, remove, modify, patch

### Descriptions - Always From Documentation

**MANDATORY**: When creating/updating specs:
1. Check vendor documentation for operation descriptions
2. Include descriptions when available
3. Copy accurately from official documentation

```yaml
paths:
  /users/{userId}:
    get:
      operationId: getUser
      summary: Retrieve a user
      description: |
        Returns detailed information about a specific user including
        their profile, permissions, and account status.
      parameters:
        - name: userId
          description: The unique identifier of the user
          required: true
```

When descriptions are not available:
- Create minimal factual description
- Document the gap

### Schema Organization

**Model Definition Source Priority**:
1. **Official Documentation** - Definitive source, include ALL documented fields
2. **API Responses** - Only when significantly mismatches docs
3. **Field Inclusion** - Include ALL documented fields (may be optional)

**Schema Naming Patterns**:
```yaml
User              # Main resource
UserInfo          # Extended version
UserBase          # Minimal version
UserCreateInput   # Create request
UserUpdateInput   # Update request
UserSummary       # Abbreviated (for nested usage)
```

### Parameter Naming - Avoid Conflicts

**Shared parameters MUST include operation name to avoid conflicts:**

```yaml
# ❌ WRONG - Generic name, could conflict
components:
  parameters:
    withPictureParam:  # Used by multiple operations
      name: withPicture
      in: query

# ✅ CORRECT - Operation-specific name
components:
  parameters:
    withPictureListUsersParam:  # Specific to listUsers
      name: withPicture
      in: query
    withPictureGetUserParam:    # Specific to getUser
      name: withPicture
      in: query
```

**Rule**: Parameter component name = `{paramName}{OperationName}Param`

### Enum Descriptions - x-enum-descriptions

**ALL enum values MUST have x-enum-descriptions:**

```yaml
# ❌ WRONG - Enums without x-enum-descriptions
status:
  type: string
  enum: [A, I, S]
  description: User status

# ❌ WRONG - Even clear enums need descriptions
type:
  type: string
  enum: [active, inactive, pending]
  description: Account type

# ✅ CORRECT - x-enum-descriptions for all enums
status:
  type: string
  description: Current status of the user account
  enum: [A, I, S]
  x-enum-descriptions:
    - Active - user can access the system
    - Inactive - user account is deactivated
    - Suspended - user access is temporarily disabled
  example: A

# ✅ CORRECT - Even for clear values
type:
  type: string
  description: Type of the account
  enum: [active, inactive, pending]
  x-enum-descriptions:
    - Account is active and can be used
    - Account is deactivated and cannot be used
    - Account is awaiting activation
  example: active
```

**WHY**: x-enum-descriptions provide context and clarity for ALL enum values, not just abbreviated ones. They help users understand the exact meaning and implications of each value.

## 🟢 GUIDELINES

### Security Schemes
- ALWAYS use OAuth2 type with scopes
- Even for API Key/PAT/Basic Auth, define as OAuth2
- Scopes define required permissions per operation

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: oauth2
      flows:
        authorizationCode:
          scopes:
            user:read: Read user information
            user:write: Modify user information
```

### API Metadata Configuration

**x-impl-name Format:**
- MUST be single PascalCase identifier (no spaces)
- Use service brand name as-is (preserve capitalization)
- For multi-word names: combine using PascalCase

```yaml
# ✅ CORRECT
x-impl-name: GitHub
x-impl-name: AccessManagement      # Multi-word: "Access Management" → AccessManagement
x-impl-name: AmazonS3

# ❌ WRONG
x-impl-name: Access Management     # Has space (should be AccessManagement)
x-impl-name: github                # Not PascalCase
x-impl-name: GitHub API            # Multiple words with space
```

**WHY**: Combine multi-word names into single PascalCase identifier while preserving brand capitalization.

**Other Metadata:**
- Do NOT set title, description, or version (sync-meta script handles)
- Configure server base URL from service configuration

### Schema Validation
- Run `npx swagger-cli validate api.yml` after any changes
- Specification must validate without errors
- Fix all validation errors before proceeding

## Validation Quick Reference

| Rule | Check Command |
|------|--------------|
| No root servers/security | `yq eval '.servers, .security' api.yml` |
| camelCase only | `grep -r '_' api.yml` in properties |
| No 'describe' | `grep -E "describe[A-Z]" api.yml` |
| 200 only | `yq eval '.paths.*.*.responses \| keys' api.yml` |
| No InlineResponse | `grep -r "InlineResponse" generated/` |
| No nullable | `grep "nullable:" api.yml` |
| IDs are strings | `yq eval '.. \| select(has("id")) \| .id.type' api.yml` |

## Failure Recovery

If ANY rule is violated:

1. **STOP all work immediately**
2. **Document the violation**
3. **Fix the violation**
4. **Re-validate ALL rules**
5. **Only proceed when 100% compliant**

### Resource Scope - Check Product Documentation

**ALWAYS check if resources belong to a parent entity (organization, workspace, project):**

```yaml
# ❌ WRONG - Missing parent scope
/users:
  get:
    operationId: listUsers

# ✅ CORRECT - Scoped to organization
/organizations/{organizationId}/users:
  get:
    operationId: listUsers
    parameters:
      - name: organizationId
        in: path
        required: true
```

**How to determine scope:**
1. Check product documentation for resource hierarchy
2. Look for mentions of "organization", "workspace", "project", "team"
3. If resources belong to parent entity → include in path
4. If resources are truly global → root path is OK

**Common parent scopes:**
- `/organizations/{organizationId}/...`
- `/workspaces/{workspaceId}/...`
- `/projects/{projectId}/...`
- `/teams/{teamId}/...`

## Best Practices

### Documentation Quality
- Include operation summaries
- Add parameter descriptions
- Document ALL enum values with x-enum-descriptions
- Explain complex schemas
- Link to vendor documentation

### Maintainability
- Use $ref for reusable components
- Keep schemas focused (single responsibility)
- Separate read/write schemas when needed
- Version schemas carefully
- Document breaking changes

### Type Safety
- Use specific types (not just "object")
- Define formats (date-time, email, uri)
- Set minimum/maximum constraints
- Use enums for fixed values
- Mark required fields explicitly

## Remember

These standards ensure:
- Consistent API design across all modules
- Clean code generation
- Type-safe implementations
- Maintainable specifications
- Framework compatibility

---

**Follow these standards for professional, maintainable API specifications.**
