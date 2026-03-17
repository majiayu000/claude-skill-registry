---
name: openapi-operations
description: OpenAPI operation rules 11-13 for naming, pagination, and responses
---

# API Specification - Operations (Rules 11-13)

**Operation naming, pagination, and response patterns**

## Rule 11: Method Naming Pattern - NEVER Use 'describe'

```yaml
# ✅ CORRECT
operationId: getAccessToken   # Full name (globally unique)
x-method-name: getToken       # Method name WITHOUT tag prefix

operationId: listAccessTokens # Full name (globally unique)
x-method-name: listTokens     # Method name WITHOUT tag prefix

# ❌ FORBIDDEN
operationId: describeItem     # NEVER use 'describe'
x-method-name: getAccessToken # NO! Remove tag name from method

# ❌ FORBIDDEN - Tag name in method name
x-method-name: getAccessToken # NO! 'Access' is the tag name
x-method-name: listUserItems  # NO! 'User' is the tag name
```

**Rule**: `x-method-name` must NOT contain the tag name, but `operationId` should be fully descriptive for global uniqueness.

### 🚨 CRITICAL: Parent vs Global List Operations

**When organizing list operations, distinguish between sub-resource lists and global lists:**

#### Sub-Resource Lists → ParentApi.listSubResources

When listing sub-resources of a parent, use the **parent resource tag** with `listSubResources` method name:

```yaml
# ✅ CORRECT - Listing roles for a specific user (sub-resource)
/organizations/{orgId}/users/{userId}/roles:
  get:
    tags:
      - user           # Parent resource tag
    operationId: listUserRoles
    x-method-name: listRoles    # Called as userApi.listRoles(orgId, userId)
```

#### Global Lists → ResourceApi.list

When listing resources globally (not under a parent), use the **resource tag** with `list` method name:

```yaml
# ✅ CORRECT - Listing all roles globally
/organizations/{orgId}/roles:
  get:
    tags:
      - role           # Resource itself
    operationId: listRoles
    x-method-name: list         # Called as roleApi.list(orgId)
```

**Summary**:
- **Sub-resource** (users/{userId}/roles) → `tags: [user]`, `x-method-name: listRoles` → `userApi.listRoles()`
- **Global resource** (/roles) → `tags: [role]`, `x-method-name: list` → `roleApi.list()`

**Why**: This pattern ensures that:
- Sub-resources are accessed through their parent API
- Global resources have clean `list()` methods
- API organization matches resource hierarchy
- Each tag can have one `list` method without conflicts

### 🚨 CRITICAL: Operation ID Consistency for Same Resource

When you have multiple operations for the SAME resource, the operationId must use the SAME resource name consistently:

```yaml
# ✅ CORRECT - Consistent use of "Organization" (full word)
paths:
  /organizations/{organizationId}:
    get:
      operationId: getOrganization
  /organizations:
    get:
      operationId: listOrganizations

# ❌ WRONG - Inconsistent naming (getOrganization vs listOrgs)
paths:
  /organizations/{organizationId}:
    get:
      operationId: getOrganization  # Uses "Organization"
  /organizations:
    get:
      operationId: listOrgs         # Uses "Orgs" - INCONSISTENT!

# ❌ WRONG - Inconsistent naming (getUser vs listAccounts)
paths:
  /users/{userId}:
    get:
      operationId: getUser          # Uses "User"
  /users:
    get:
      operationId: listAccounts     # Uses "Accounts" - INCONSISTENT!
```

**Rationale**: Consistency in naming makes the API predictable and easier to understand. If one operation uses "Organization", ALL operations for that resource must use "Organization" (not "Org", not "Orgs", not "Organisation").

### Summary Text Rules

- `getItem` → Summary: "Retrieve an item"
- `listItems` → Summary: "Retrieve items"
- Use "Retrieve" for get/list operations

## Rule 12: Pagination - MANDATORY for ALL List Operations

**🚨 CRITICAL: ALL `list*` operations MUST be paginated using PagedResults**

### PagedResults Requirements

For TypeScript PagedResults generation, operation MUST have ALL 4 conditions:

1. **pageSize parameter** (core type)
2. **pageNumber OR pageToken parameter** (core type)
3. **links response header** (core type)
4. **Response schema is array**

```yaml
# ✅ CORRECT - Complete pagination with components
components:
  parameters:
    pageSizeParam:
      $ref: './node_modules/@zerobias-org/types-core/schema/params.yml#/pageSizeParam'
    pageNumberParam:
      $ref: './node_modules/@zerobias-org/types-core/schema/params.yml#/pageNumberParam'
  headers:
    linksHeader:
      $ref: './node_modules/@zerobias-org/types-core/schema/headers.yml#/linksHeader'

paths:
  /users:
    get:
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/pageSizeParam'
        - $ref: '#/components/parameters/pageNumberParam'
      responses:
        '200':
          description: Successful response
          headers:
            links:
              $ref: '#/components/headers/linksHeader'
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

# ❌ WRONG - Direct node_modules refs (should use components)
/users:
  get:
    operationId: listUsers
    parameters:
      - $ref: './node_modules/@zerobias-org/types-core/schema/params.yml#/pageSizeParam'  # NO! Use components
    responses:
      '200':
        headers:
          links:
            $ref: './node_modules/@zerobias-org/types-core/schema/headers.yml#/linksHeader'  # NO! Use components

# ❌ WRONG - Missing pagination
/users:
  get:
    operationId: listUsers
    responses:
      '200':
        content:
          application/json:
            schema:
              type: array  # Array without pagination!
              items:
                $ref: '#/components/schemas/User'
```

**IMPORTANT**: NEVER reference node_modules directly in paths. Always define in `components/parameters` and `components/headers` first, then reference the component.

### Pagination Parameter Options

**Define in components first, then reference:**

```yaml
components:
  parameters:
    pageSizeParam:
      $ref: './node_modules/@zerobias-org/types-core/schema/params.yml#/pageSizeParam'
    pageNumberParam:
      $ref: './node_modules/@zerobias-org/types-core/schema/params.yml#/pageNumberParam'
    pageTokenParam:
      $ref: './node_modules/@zerobias-org/types-core/schema/params.yml#/pageTokenParam'
```

**Option A: Page Number (offset-based)**
```yaml
parameters:
  - $ref: '#/components/parameters/pageSizeParam'
  - $ref: '#/components/parameters/pageNumberParam'
```

**Option B: Page Token (cursor-based)**
```yaml
parameters:
  - $ref: '#/components/parameters/pageSizeParam'
  - $ref: '#/components/parameters/pageTokenParam'
```

**Handling API-specific pagination:**
- If API uses `cursor` → Map to pageToken in components
- If API uses `offset` → Calculate pageNumber (`offset / pageSize`)
- If API uses custom params → Map them to standard params

**NEVER use custom pagination parameters directly:**
- ❌ `since`, `offset`, `limit`, `cursor` - Map to core params

### links Response Header (MANDATORY)

**Define in components first:**

```yaml
components:
  headers:
    linksHeader:
      $ref: './node_modules/@zerobias-org/types-core/schema/headers.yml#/linksHeader'
```

**Then reference in operations:**

```yaml
responses:
  '200':
    headers:
      links:
        $ref: '#/components/headers/linksHeader'
```

**WHY**: PagedResults provides type-safe pagination with next/previous links

## Rule 13: Response Codes - 200/201 Only

**NEVER add 40x or 50x error responses** - Framework handles ALL errors

```yaml
# ✅ CORRECT
responses:
  '200':
    description: Successful response
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Resource'

# ❌ WRONG - Error responses included
responses:
  '200':
    description: Success
  '401':
    description: Unauthorized    # NO! Framework handles this
  '404':
    description: Not found       # NO! Framework handles this
  '500':
    description: Server error    # NO! Framework handles this
```

**WHY**: Framework's error handling automatically converts HTTP errors to typed exceptions. Adding error responses to the spec:
1. Creates unnecessary code generation
2. Duplicates framework error handling
3. Makes specs harder to maintain

---

## Operation Naming Quick Reference

| Operation Type | operationId Pattern | x-method-name | Summary |
|---------------|---------------------|---------------|---------|
| Get single | `get{Resource}` | Without tag | "Retrieve a {resource}" |
| List multiple | `list{Resources}` | Without tag | "Retrieve {resources}" |
| Create | `create{Resource}` | Without tag | "Create a {resource}" |
| Update | `update{Resource}` | Without tag | "Update a {resource}" |
| Delete | `delete{Resource}` | Without tag | "Delete a {resource}" |
| Search | `search{Resources}` | Without tag | "Search {resources}" |

**NEVER**: `describe{Resource}` - This is forbidden!

---

## Validation Checklist

Before finalizing operations:

- [ ] No operation uses 'describe' prefix
- [ ] All operationIds for same resource use same resource name
- [ ] x-method-name does NOT include tag name
- [ ] Summaries use "Retrieve" for get/list operations
- [ ] **ALL list operations have complete pagination** (pageSize + pageNumber/pageToken + links header + array response)
- [ ] Pagination uses core params only (NOT custom since/offset/limit)
- [ ] ONLY 200/201 responses (NO 4xx/5xx)

---

**These operation rules ensure consistency and framework compatibility across all modules.**
