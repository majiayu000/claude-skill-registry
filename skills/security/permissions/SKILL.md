---
name: permissions
description: Use when implementing authorization, access control, RBAC, role-based permissions, guards, policies, row-level security, guest access, or protecting API endpoints. Covers Guard system, roles, permissions, policies, and data filtering.
---

# Permissions and Access Control

Bknd provides a comprehensive authorization system built on Guard, roles, permissions, and policies. This system controls who can access what in your application.

## What You'll Learn

- Configure the Guard and roles
- Define permissions with allow, deny, and filter effects
- Use policies for row-level security
- Implement guest access for public endpoints
- Filter data based on user context

## Core Concepts

Bknd's authorization follows this hierarchy:

```
Guard (evaluates)
  └─> Roles (group permissions)
      └─> Permissions (define what's allowed)
          └─> Policies (conditional logic)
```

- **Guard**: Evaluates permissions against user context
- **Roles**: Group permissions and define default behavior
- **Permissions**: Grant access with allow, deny, or filter effects
- **Policies**: Add conditional logic to permissions

## Enabling Authorization

The Guard is automatically enabled when you enable auth:

```typescript
import { em, entity, text, boolean } from "bknd";

const schema = em({
  posts: entity("posts", {
    title: text().required(),
    content: text(),
    published: boolean(),
  }),
});

export default {
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      jwt: {
        issuer: "my-app",
      },
      roles: [
        {
          name: "guest",
          is_default: true,
          implicit_allow: false,
          permissions: [
            {
              permission: "entityRead",
              effect: "allow",
              policies: [
                {
                  condition: { entity: "posts" },
                  effect: "filter",
                  filter: { published: true },
                },
              ],
            },
          ],
        },
      ],
    },
  },
};
```

## Defining Roles

Roles group permissions together and set default behavior:

```typescript
{
  name: "admin",
  is_default: false,
  implicit_allow: true,
  permissions: [],
}
```

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Unique role identifier |
| `is_default` | boolean | Assigned to users without explicit role |
| `implicit_allow` | boolean | Allow all permissions (security risk) |
| `permissions` | array | List of permissions for this role |

## Permission Effects

Permissions define what's allowed with three effects:

### Allow Effect

Grants access when conditions are met:

```typescript
{
  permission: "data.entity.read",
  effect: "allow",
  policies: [
    {
      condition: { entity: "posts" },
      effect: "allow",
    },
  ],
}
```

### Deny Effect

Revokes access (takes precedence over allow):

```typescript
{
  permission: "data.entity.delete",
  effect: "deny",
  policies: [
    {
      condition: { entity: "posts" },
      effect: "deny",
    },
  ],
}
```

### Filter Effect

Filters data based on query criteria (row-level security):

```typescript
{
  permission: "data.entity.read",
  effect: "allow",
  policies: [
    {
      condition: { entity: "posts" },
      effect: "filter",
      filter: { author_id: "@auth.user.id" },
    },
  ],
}
```

## Common Patterns

### Public Read, Authenticated Write

```typescript
{
  auth: {
    enabled: true,
    roles: [
      {
        name: "guest",
        is_default: true,
        implicit_allow: false,
        permissions: [
          {
            permission: "data.entity.read",
            effect: "allow",
            policies: [
              {
                condition: { entity: "posts" },
                effect: "filter",
                filter: { published: true },
              },
            ],
          },
        ],
      },
      {
        name: "user",
        is_default: false,
        implicit_allow: false,
        permissions: [
          {
            permission: "data.entity.create",
            effect: "allow",
            policies: [
              {
                condition: { entity: "posts" },
                effect: "allow",
              },
            ],
          },
          {
            permission: "data.entity.update",
            effect: "allow",
            policies: [
              {
                condition: { entity: "posts" },
                effect: "filter",
                filter: { author_id: "@auth.user.id" },
              },
            ],
          },
        ],
      },
    ],
  },
}
```

### User-Own Data Pattern

Users can only read and modify their own data:

```typescript
{
  name: "user",
  permissions: [
    {
      permission: "data.entity.read",
      effect: "allow",
      policies: [
        {
          condition: { entity: "posts" },
          effect: "filter",
          filter: { author_id: "@auth.user.id" },
        },
      ],
    },
    {
      permission: "data.entity.update",
      effect: "allow",
      policies: [
        {
          condition: { entity: "posts" },
          effect: "filter",
          filter: { author_id: "@auth.user.id" },
        },
      ],
    },
    {
      permission: "data.entity.delete",
      effect: "allow",
      policies: [
        {
          condition: { entity: "posts" },
          effect: "filter",
          filter: { author_id: "@auth.user.id" },
        },
      ],
    },
  ],
}
```

### Multi-Tenant Isolation

Each tenant sees only their data:

```typescript
{
  name: "user",
  permissions: [
    {
      permission: "data.entity.read",
      effect: "allow",
      policies: [
        {
          condition: { entity: "*" },
          effect: "filter",
          filter: { tenant_id: "@auth.user.tenant_id" },
        },
      ],
    },
  ],
}
```

## Policy Variables

Policies support dynamic variable substitution using `@variable` syntax:

### Available Variables

| Variable | Source | Example |
|----------|--------|---------|
| `@auth.user.id` | Authenticated user's ID | `@auth.user.id` |
| `@auth.user.role` | User's role name | `@auth.user.role` |
| `@auth.user.*` | Any user property | `@auth.user.email`, `@auth.user.tenant_id` |
| `@ctx.*` | Guard config context | Custom context variables |

### Example: User-Owned Data

```typescript
filter: {
  author_id: "@auth.user.id",
}
```

### Example: Time-Based Access

```typescript
filter: {
  start_date: { $lte: "@ctx.now" },
  end_date: { $gte: "@ctx.now" },
}
```

### Example: Multi-Tenant with Public Content

```typescript
filter: {
  $or: [
    { published: true },
    { tenant_id: "@auth.user.tenant_id" },
  ],
}
```

## Data Permissions

Bknd provides built-in permissions for data operations:

| Permission | Description | Filterable |
|------------|-------------|------------|
| `data.entity.read` | Read entity data | Yes |
| `data.entity.create` | Create new entity records | Yes |
| `data.entity.update` | Update entity records | Yes |
| `data.entity.delete` | Delete entity records | Yes |

All data permissions support the `filter` effect for row-level security.

## Schema Permissions

Schema operations are protected by system permissions:

```typescript
{
  permission: "system.schema.read",
  effect: "allow",
  policies: [],
}
```

Protects:
- `GET /api/system/schema` - Get current schema
- `GET /api/data/schema` - Get data schema

## Testing Permissions

Create test users to verify access control. Use HTTP API to test with auth context:

```typescript
import { createApp } from "bknd";

const app = createApp({
  connection: { url: "file:test.db" },
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      jwt: {
        secret: "test-secret",
      },
      roles: [
        // Your roles configuration
      ],
    },
  },
});
await app.build();

// Create test data via mutator (bypasses permissions)
await app.em.mutator("posts").insertMany([
  { title: "Public Post", published: true },
  { title: "Private Post", published: false },
]);

// Test as guest (no authentication)
const guestResponse = await app.server.request("/api/data/entity/posts");
const guestPosts = await guestResponse.json();
console.log("Guest sees:", guestPosts.data); // Only published posts

// Create authenticated user and test
const user = await app.createUser({
  email: "user@example.com",
  password: "password123",
});

const token = await app.auth.login(user.email, "password123");

// Test as authenticated user with JWT
const userResponse = await app.server.request("/api/data/entity/posts", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
const userPosts = await userResponse.json();
console.log("User sees:", userPosts.data);
```

## DOs and DON'Ts

**DO:**
- Use `implicit_allow: false` for production roles (require explicit permissions)
- Use `filter` effect for row-level security
- Test with both guest and authenticated contexts
- Define `is_default` role for unauthenticated access
- Use policy filters for complex access rules

**DON'T:**
- Use `implicit_allow: true` unless you truly need all access
- Forget to set `is_default: true` for guest role
- Mix allow and deny in the same permission (deny takes precedence)
- Skip testing edge cases (what happens with null user context?)
- Hardcode user IDs in filters (use `@user.id` instead)

## Common Issues

**Guests can't access anything:**
- Ensure `auth.enabled: true` (required for Guard)
- Check `is_default: true` is set on a role
- Verify `implicit_allow: false` (explicit permissions required)

**Users accessing protected data:**
- Check `filter` conditions match your data structure
- Verify policy variables (`@auth.user.id`) are resolving correctly
- Ensure no `implicit_allow: true` roles are assigned

**Public endpoints returning 403:**
- Verify guest role has the required permission
- Check policy conditions are met
- Debug with `console.log(ctx.get("auth"))` to see user context

## Next Steps

- **[Auth](auth)** - Configure authentication strategies
- **[Data Schema](data-schema)** - Define your data model
- **[Query](query)** - Learn the query system
