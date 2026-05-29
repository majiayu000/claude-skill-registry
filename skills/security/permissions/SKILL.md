---
name: bknd-assign-permissions
description: Use when assigning permissions to roles in Bknd. Covers permission syntax (simple strings, extended format), permission effects (allow/deny), policies with conditions, entity-specific permissions, and fine-grained access control patterns.
---

# Assign Permissions

Configure detailed permissions for roles using simple strings, extended format with effects, and conditional policies.

## Prerequisites

- Bknd project with code-first configuration
- Auth enabled (`auth: { enabled: true }`)
- Guard enabled (`guard: { enabled: true }`)
- At least one role defined (see **bknd-create-role**)

## When to Use UI Mode

- Viewing current role permissions
- Quick permission checks

**UI steps:** Admin Panel > Auth > Roles > Select role

**Note:** Permission assignment requires code mode. UI is read-only.

## When to Use Code Mode

- Assigning permissions to roles
- Adding permission effects (allow/deny)
- Creating conditional policies
- Entity-specific permission rules

## Code Approach

### Step 1: Simple Permission Strings

Assign basic permissions as string array:

```typescript
import { serve } from "bknd/adapter/bun";
import { em, entity, text } from "bknd";

const schema = em({
  posts: entity("posts", { title: text().required() }),
});

serve({
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      guard: { enabled: true },
      roles: {
        editor: {
          implicit_allow: false,
          permissions: [
            "data.entity.read",    // Read any entity
            "data.entity.create",  // Create in any entity
            "data.entity.update",  // Update any entity
            // No delete permission
          ],
        },
      },
    },
  },
});
```

### Available Permissions

| Permission | Filterable | Description |
|------------|------------|-------------|
| `data.entity.read` | Yes | Read entity records |
| `data.entity.create` | Yes | Create new records |
| `data.entity.update` | Yes | Update existing records |
| `data.entity.delete` | Yes | Delete records |
| `data.database.sync` | No | Sync database schema |
| `data.raw.query` | No | Execute raw SELECT |
| `data.raw.mutate` | No | Execute raw INSERT/UPDATE/DELETE |

**Filterable** means you can add conditions/filters via policies.

### Step 2: Extended Permission Format

Use objects for explicit allow/deny effects:

```typescript
{
  roles: {
    moderator: {
      implicit_allow: false,
      permissions: [
        { permission: "data.entity.read", effect: "allow" },
        { permission: "data.entity.update", effect: "allow" },
        { permission: "data.entity.delete", effect: "deny" },  // Explicit deny
      ],
    },
  },
}
```

### Permission Effects

| Effect | Description |
|--------|-------------|
| `allow` | Grant the permission (default) |
| `deny` | Explicitly block the permission |

**Deny overrides allow** - useful when `implicit_allow: true` but you want to block specific actions.

### Step 3: Conditional Policies

Add policies for fine-grained control:

```typescript
{
  roles: {
    content_editor: {
      implicit_allow: false,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [
            {
              description: "Only read posts and comments",
              condition: { entity: { $in: ["posts", "comments"] } },
              effect: "allow",
            },
          ],
        },
        {
          permission: "data.entity.create",
          effect: "allow",
          policies: [
            {
              condition: { entity: { $in: ["posts", "comments"] } },
              effect: "allow",
            },
          ],
        },
      ],
    },
  },
}
```

### Policy Structure

```typescript
{
  description?: string,      // Human-readable (optional)
  condition?: ObjectQuery,   // When policy applies
  effect: "allow" | "deny" | "filter",
  filter?: ObjectQuery,      // Row filter (for effect: "filter")
}
```

### Policy Effects

| Effect | Purpose |
|--------|---------|
| `allow` | Grant when condition met |
| `deny` | Block when condition met |
| `filter` | Apply row-level filter to results |

### Condition Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$eq` | Equal | `{ entity: { $eq: "posts" } }` |
| `$ne` | Not equal | `{ entity: { $ne: "users" } }` |
| `$in` | In array | `{ entity: { $in: ["posts", "comments"] } }` |
| `$nin` | Not in array | `{ entity: { $nin: ["users", "secrets"] } }` |
| `$gt` | Greater than | `{ age: { $gt: 18 } }` |
| `$gte` | Greater or equal | `{ level: { $gte: 5 } }` |
| `$lt` | Less than | `{ count: { $lt: 100 } }` |
| `$lte` | Less or equal | `{ priority: { $lte: 3 } }` |

### Step 4: Variable Placeholders

Reference runtime context with `@variable`:

| Placeholder | Description |
|-------------|-------------|
| `@user.id` | Current user's ID |
| `@user.email` | Current user's email |
| `@user.role` | Current user's role |
| `@entity` | Current entity name |
| `@id` | Current record ID |

Example - user can only update their own profile:

```typescript
{
  permissions: [
    {
      permission: "data.entity.update",
      effect: "allow",
      policies: [
        {
          condition: { entity: "users", "@id": "@user.id" },
          effect: "allow",
        },
      ],
    },
  ],
}
```

### Step 5: Entity-Specific Permissions

Grant different permissions per entity:

```typescript
{
  roles: {
    blog_author: {
      implicit_allow: false,
      permissions: [
        // Full CRUD on posts
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{ condition: { entity: "posts" }, effect: "allow" }],
        },
        {
          permission: "data.entity.create",
          effect: "allow",
          policies: [{ condition: { entity: "posts" }, effect: "allow" }],
        },
        {
          permission: "data.entity.update",
          effect: "allow",
          policies: [{ condition: { entity: "posts" }, effect: "allow" }],
        },
        {
          permission: "data.entity.delete",
          effect: "allow",
          policies: [{ condition: { entity: "posts" }, effect: "allow" }],
        },

        // Read-only on categories
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{ condition: { entity: "categories" }, effect: "allow" }],
        },
      ],
    },
  },
}
```

## Common Patterns

### Read-Only Role

```typescript
{
  roles: {
    viewer: {
      implicit_allow: false,
      permissions: ["data.entity.read"],
    },
  },
}
```

### CRUD Without Delete

```typescript
{
  roles: {
    contributor: {
      implicit_allow: false,
      permissions: [
        "data.entity.read",
        "data.entity.create",
        "data.entity.update",
        { permission: "data.entity.delete", effect: "deny" },
      ],
    },
  },
}
```

### Admin with Restricted Raw Access

```typescript
{
  roles: {
    admin: {
      implicit_allow: true,  // Allow all by default
      permissions: [
        // But deny raw database access
        { permission: "data.raw.query", effect: "deny" },
        { permission: "data.raw.mutate", effect: "deny" },
      ],
    },
  },
}
```

### Multi-Entity Role

```typescript
{
  roles: {
    content_manager: {
      implicit_allow: false,
      permissions: [
        // Content entities: full CRUD
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            condition: { entity: { $in: ["posts", "pages", "comments", "media"] } },
            effect: "allow",
          }],
        },
        {
          permission: "data.entity.create",
          effect: "allow",
          policies: [{
            condition: { entity: { $in: ["posts", "pages", "comments", "media"] } },
            effect: "allow",
          }],
        },
        {
          permission: "data.entity.update",
          effect: "allow",
          policies: [{
            condition: { entity: { $in: ["posts", "pages", "comments", "media"] } },
            effect: "allow",
          }],
        },
        {
          permission: "data.entity.delete",
          effect: "allow",
          policies: [{
            condition: { entity: { $in: ["posts", "pages", "comments"] } },  // No media delete
            effect: "allow",
          }],
        },
      ],
    },
  },
}
```

### Deny Specific Entity

```typescript
{
  roles: {
    user: {
      implicit_allow: false,
      permissions: [
        // Can read most entities
        "data.entity.read",
        // But never access secrets entity
        {
          permission: "data.entity.read",
          effect: "deny",
          policies: [{
            condition: { entity: "secrets" },
            effect: "deny",
          }],
        },
      ],
    },
  },
}
```

### Create Helper Function

For complex role definitions:

```typescript
// helpers/permissions.ts
type EntityPermission = "read" | "create" | "update" | "delete";

function entityPermissions(
  entities: string[],
  actions: EntityPermission[]
) {
  const permMap: Record<EntityPermission, string> = {
    read: "data.entity.read",
    create: "data.entity.create",
    update: "data.entity.update",
    delete: "data.entity.delete",
  };

  return actions.map((action) => ({
    permission: permMap[action],
    effect: "allow" as const,
    policies: [{
      condition: { entity: { $in: entities } },
      effect: "allow" as const,
    }],
  }));
}

// Usage
{
  roles: {
    blog_author: {
      implicit_allow: false,
      permissions: [
        ...entityPermissions(["posts", "comments"], ["read", "create", "update"]),
        ...entityPermissions(["categories", "tags"], ["read"]),
      ],
    },
  },
}
```

## Verification

Test permission assignments:

**1. Login as user with role:**

```bash
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "editor@example.com", "password": "password123"}'
```

**2. Test allowed permission:**

```bash
curl http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer <token>"
# Should return 200 with data
```

**3. Test denied permission:**

```bash
curl -X DELETE http://localhost:7654/api/data/posts/1 \
  -H "Authorization: Bearer <token>"
# Should return 403 Forbidden
```

**4. Test entity-specific permission:**

```bash
# If only posts/comments allowed:
curl http://localhost:7654/api/data/users \
  -H "Authorization: Bearer <token>"
# Should return 403 if users entity not in allowed list
```

## Common Pitfalls

### Permission Not Taking Effect

**Problem:** Changed permissions but old behavior persists

**Fix:** Restart server - role config is loaded at startup:

```bash
# Stop and restart
bknd run
```

### Deny Not Overriding

**Problem:** Deny effect not blocking access

**Fix:** Check policy condition - deny only applies when condition matches:

```typescript
// WRONG - no condition, may not match
{ permission: "data.entity.delete", effect: "deny" }

// CORRECT - simple deny at permission level
{
  permissions: [
    "data.entity.read",
    "data.entity.create",
    // Don't include delete at all
  ],
}
```

### Entity Condition Not Matching

**Problem:** Entity-specific permission not working

**Fix:** Verify entity name matches exactly:

```typescript
// WRONG - entity name case matters
{ condition: { entity: "Posts" } }

// CORRECT - use exact entity name
{ condition: { entity: "posts" } }
```

### Multiple Policies Conflict

**Problem:** Confusing behavior with multiple policies

**Fix:** Understand evaluation order - first matching policy wins:

```typescript
{
  policies: [
    // More specific first
    { condition: { entity: "secrets" }, effect: "deny" },
    // General fallback last
    { effect: "allow" },
  ],
}
```

### Variable Placeholder Not Resolving

**Problem:** `@user.id` appearing literally in filter

**Fix:** Variables only work in `filter` and `condition` fields:

```typescript
// CORRECT usage
{
  condition: { "@id": "@user.id" },  // Works
  filter: { user_id: "@user.id" },   // Works
}
```

## DOs and DON'Ts

**DO:**
- Start with minimal permissions, add as needed
- Use `$in` operator for multiple entities
- Test each permission after adding
- Use descriptive policy descriptions
- Prefer explicit permissions over `implicit_allow`

**DON'T:**
- Grant `data.raw.*` to non-admin roles (SQL injection risk)
- Use `implicit_allow: true` with deny policies (confusing)
- Forget to restart server after config changes
- Mix simple strings and extended format unnecessarily
- Over-complicate with too many nested policies

## Related Skills

- **bknd-create-role** - Define new roles
- **bknd-row-level-security** - Filter data by user ownership
- **bknd-protect-endpoint** - Secure specific endpoints
- **bknd-public-vs-auth** - Configure public vs authenticated access
- **bknd-setup-auth** - Initialize authentication system
