---
name: bknd-create-role
description: Use when defining a new role in Bknd authorization system. Covers role properties (implicit_allow, is_default, permissions), permission assignment, role hierarchies, and common role patterns (admin, editor, viewer, anonymous).
---

# Create Role

Define a new role in Bknd's authorization system to control user access.

## Prerequisites

- Bknd project initialized with code-first configuration
- Auth enabled (`auth: { enabled: true }`)
- Guard enabled for authorization (`guard: { enabled: true }`)

## When to Use UI Mode

- Viewing existing roles
- Quick toggle of role settings

**UI steps:** Admin Panel > Auth > Roles

**Note:** Role creation requires code mode. UI only shows existing roles.

## When to Use Code Mode

- Creating new roles
- Setting role permissions
- Configuring default roles
- Setting up role hierarchies

## Code Approach

### Step 1: Enable Guard

Roles require the guard system to be enabled:

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
      guard: { enabled: true },  // Required for roles
      roles: {
        // Roles defined here
      },
    },
  },
});
```

### Step 2: Define a Basic Role

Create a role with explicit permissions:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    roles: {
      viewer: {
        implicit_allow: false,  // Deny by default
        permissions: [
          "data.entity.read",   // Grant read access only
        ],
      },
    },
  },
}
```

### Role Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `implicit_allow` | boolean | `false` | Allow all unless denied |
| `is_default` | boolean | `false` | Use when user has no role |
| `permissions` | array | `[]` | Permissions granted to role |

### Step 3: Create Admin Role (Full Access)

Grant full access with `implicit_allow`:

```typescript
{
  roles: {
    admin: {
      implicit_allow: true,  // Can do everything
    },
  },
}
```

**Warning:** `implicit_allow: true` grants ALL permissions. Use only for admin roles.

### Step 4: Create Editor Role (Partial Access)

Grant specific CRUD permissions:

```typescript
{
  roles: {
    editor: {
      implicit_allow: false,
      permissions: [
        "data.entity.read",
        "data.entity.create",
        "data.entity.update",
        // No delete permission
      ],
    },
  },
}
```

### Step 5: Create Default Role

Set a role for users without assigned role:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,       // Applied when no role
      implicit_allow: false,
      permissions: [
        "data.entity.read",   // Read-only access
      ],
    },
  },
}
```

**Note:** Only ONE role can have `is_default: true`.

### Step 6: Set Registration Role

Assign role to newly registered users:

```typescript
{
  auth: {
    enabled: true,
    default_role_register: "user",  // Role for new registrations
    roles: {
      user: {
        implicit_allow: false,
        permissions: ["data.entity.read"],
      },
    },
  },
}
```

## Available Permissions

| Permission | Description |
|------------|-------------|
| `data.entity.read` | Read any entity records |
| `data.entity.create` | Create records in any entity |
| `data.entity.update` | Update records in any entity |
| `data.entity.delete` | Delete records from any entity |
| `data.database.sync` | Sync database schema |
| `data.raw.query` | Execute raw SELECT queries |
| `data.raw.mutate` | Execute raw INSERT/UPDATE/DELETE |

## Common Role Patterns

### Multi-Tier Access System

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    default_role_register: "user",
    roles: {
      // Full access
      admin: {
        implicit_allow: true,
      },

      // Content management
      editor: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          "data.entity.create",
          "data.entity.update",
          "data.entity.delete",
        ],
      },

      // Create and read
      contributor: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          "data.entity.create",
        ],
      },

      // Authenticated read-only
      user: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
        ],
      },

      // Unauthenticated/guest
      anonymous: {
        is_default: true,
        implicit_allow: false,
        permissions: [
          "data.entity.read",
        ],
      },
    },
  },
}
```

### Closed System (No Public Access)

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    allow_register: false,  // Disable self-registration
    roles: {
      admin: {
        implicit_allow: true,
      },
      member: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          "data.entity.create",
          "data.entity.update",
        ],
      },
      // No default role - unauthenticated users get NO access
    },
  },
}
```

### API Consumer Role

```typescript
{
  roles: {
    api_client: {
      implicit_allow: false,
      permissions: [
        "data.entity.read",
        "data.entity.create",
        // No update/delete - API clients create data only
      ],
    },
  },
}
```

## Permission Effects

Use extended format for allow/deny effects:

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

## Role Assignment

### Assign During User Creation (Seed)

```typescript
{
  options: {
    seed: async (ctx) => {
      await ctx.app.module.auth.createUser({
        email: "admin@example.com",
        password: "secure-password",
        role: "admin",  // Assign admin role
      });
    },
  },
}
```

### Assign During Registration

```typescript
{
  auth: {
    default_role_register: "user",  // All registrations get "user" role
  },
}
```

### Update User Role (API)

```typescript
const api = getApi(app);

// Update user's role
await api.data.updateOne("users", userId, {
  role: "editor",
});
```

## Verification

Test role permissions:

**1. Create user with role:**

```bash
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

**2. Login and get token:**

```bash
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

**3. Test permission (should succeed for read):**

```bash
curl http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer <token>"
```

**4. Test denied permission (should fail for delete if not allowed):**

```bash
curl -X DELETE http://localhost:7654/api/data/posts/1 \
  -H "Authorization: Bearer <token>"
# Returns 403 if delete not in permissions
```

## Common Pitfalls

### No Default Role

**Problem:** `User has no role` error for unauthenticated users

**Fix:** Set a default role:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,
      permissions: ["data.entity.read"],
    },
  },
}
```

### Multiple Default Roles

**Problem:** Unpredictable behavior with multiple `is_default: true`

**Fix:** Only ONE role should be default:

```typescript
{
  roles: {
    user: { is_default: true },    // Only one!
    guest: { /* no is_default */ },
  },
}
```

### Role Not Found

**Problem:** `Role "admin" not found` when assigning

**Fix:** Define role before referencing:

```typescript
{
  auth: {
    roles: {
      admin: { implicit_allow: true },  // Define first
    },
    default_role_register: "admin",     // Then reference
  },
}
```

### Guard Not Enabled

**Problem:** Roles defined but permissions not enforced

**Fix:** Enable the guard:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },  // Required!
    roles: { /* ... */ },
  },
}
```

### Implicit Allow Overuse

**Problem:** Using `implicit_allow: true` on non-admin roles

**Fix:** Be explicit about permissions:

```typescript
// WRONG - too permissive
{
  roles: {
    editor: { implicit_allow: true },
  },
}

// CORRECT - explicit permissions
{
  roles: {
    editor: {
      implicit_allow: false,
      permissions: [
        "data.entity.read",
        "data.entity.create",
        "data.entity.update",
      ],
    },
  },
}
```

## DOs and DON'Ts

**DO:**
- Enable guard when using roles
- Use `implicit_allow: false` for non-admin roles
- Set one default role for unauthenticated access
- Define roles before referencing them
- Test each role's permissions after creation

**DON'T:**
- Use `implicit_allow: true` for non-admin roles
- Set multiple roles as default
- Forget to enable guard
- Grant `data.raw.*` permissions to untrusted roles
- Assume roles work without guard enabled

## Related Skills

- **bknd-setup-auth** - Initialize authentication system
- **bknd-assign-permissions** - Configure detailed permissions with policies
- **bknd-row-level-security** - Implement row-level access control
- **bknd-protect-endpoint** - Secure specific endpoints
- **bknd-public-vs-auth** - Configure public vs authenticated access
