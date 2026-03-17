---
name: bknd-public-vs-auth
description: Use when configuring public vs authenticated access in Bknd. Covers anonymous role setup, unauthenticated data access, public/private entity patterns, mixed access modes, and protecting sensitive entities while exposing public ones.
---

# Public vs Authenticated Access

Configure which data and endpoints are publicly accessible vs require authentication.

## Prerequisites

- Bknd project with code-first configuration
- Auth enabled (`auth: { enabled: true }`)
- Guard enabled (`guard: { enabled: true }`)
- Basic understanding of roles (see **bknd-create-role**)

## When to Use UI Mode

- Viewing current role configurations
- Inspecting permission assignments

**UI steps:** Admin Panel > Auth > Roles

**Note:** Access configuration requires code mode.

## When to Use Code Mode

- Setting up anonymous/default role for public access
- Configuring entity-specific access rules
- Creating mixed public/private data patterns
- Building closed (auth-required) systems

## Core Concept: Default Role

Bknd uses the **default role** to determine what unauthenticated users can access:

```
User makes request → Has token? → Yes → Use user's role
                              → No  → Use default role (is_default: true)
                                    → No default? → ACCESS DENIED
```

## Code Approach

### Step 1: Fully Public (Read-Only)

Allow unauthenticated users to read all data:

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
        // Public role - anyone can read
        anonymous: {
          is_default: true,
          implicit_allow: false,
          permissions: ["data.entity.read"],
        },
        // Authenticated users can create/update
        user: {
          implicit_allow: false,
          permissions: [
            "data.entity.read",
            "data.entity.create",
            "data.entity.update",
          ],
        },
      },
    },
  },
});
```

**Result:**
- `GET /api/data/posts` - Works without auth
- `POST /api/data/posts` - Requires auth
- `PATCH /api/data/posts/1` - Requires auth

### Step 2: Fully Private (Auth Required)

Require authentication for all access:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    allow_register: true,
    default_role_register: "user",
    roles: {
      admin: { implicit_allow: true },
      user: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          "data.entity.create",
          "data.entity.update",
        ],
      },
      // NO default role - unauthenticated users get nothing
    },
  },
}
```

**Result:** All `/api/data/*` endpoints return 403 without authentication.

### Step 3: Entity-Specific Public Access

Make some entities public, others private:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    roles: {
      anonymous: {
        is_default: true,
        implicit_allow: false,
        permissions: [
          // Only posts are public
          {
            permission: "data.entity.read",
            effect: "allow",
            policies: [{
              condition: { entity: "posts" },
              effect: "allow",
            }],
          },
        ],
      },
      user: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",   // Read all entities
          "data.entity.create",
          "data.entity.update",
        ],
      },
    },
  },
}
```

**Result:**
- `GET /api/data/posts` - Public
- `GET /api/data/users` - Requires auth
- `GET /api/data/comments` - Requires auth

### Step 4: Multiple Public Entities

Expose several entities publicly:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,
      implicit_allow: false,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            condition: { entity: { $in: ["posts", "categories", "tags"] } },
            effect: "allow",
          }],
        },
      ],
    },
  },
}
```

### Step 5: Public Records with Filter

Make only published/public records accessible:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,
      implicit_allow: false,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [
            // Posts: only published
            {
              condition: { entity: "posts" },
              effect: "filter",
              filter: { status: "published" },
            },
            // Products: only visible
            {
              condition: { entity: "products" },
              effect: "filter",
              filter: { visible: true },
            },
          ],
        },
      ],
    },
  },
}
```

**Result:** Anonymous users only see filtered records; authenticated users see all.

### Step 6: Mixed Public/Owner Access

Public can read published; owners can read their own drafts:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,
      implicit_allow: false,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            condition: { entity: "posts" },
            effect: "filter",
            filter: { status: "published" },
          }],
        },
      ],
    },
    user: {
      implicit_allow: false,
      permissions: [
        // Read: published OR own posts
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            condition: { entity: "posts" },
            effect: "filter",
            filter: {
              $or: [
                { status: "published" },
                { author_id: "@user.id" },
              ],
            },
          }],
        },
        // Create allowed
        "data.entity.create",
        // Update own only
        {
          permission: "data.entity.update",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { author_id: "@user.id" },
          }],
        },
      ],
    },
  },
}
```

### Step 7: Invite-Only System

No public access, no self-registration:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    allow_register: false,  // Disable self-registration
    roles: {
      admin: { implicit_allow: true },
      member: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          "data.entity.create",
          "data.entity.update",
        ],
      },
      // No default role
    },
  },
  options: {
    seed: async (ctx) => {
      // Admin creates users manually
      await ctx.app.module.auth.createUser({
        email: "admin@company.com",
        password: "admin-password",
        role: "admin",
      });
    },
  },
}
```

### Step 8: API with Public Read, Auth Write

Common REST API pattern:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,
      implicit_allow: false,
      permissions: ["data.entity.read"],  // Read anything
    },
    api_user: {
      implicit_allow: false,
      permissions: [
        "data.entity.read",
        "data.entity.create",
        "data.entity.update",
        "data.entity.delete",
      ],
    },
  },
}
```

## Complete Configuration Examples

### Blog Platform

```typescript
import { serve } from "bknd/adapter/bun";
import { em, entity, text, boolean, relation } from "bknd";

const schema = em(
  {
    posts: entity("posts", {
      title: text().required(),
      content: text(),
      published: boolean().default(false),
    }),
    comments: entity("comments", {
      body: text().required(),
      approved: boolean().default(false),
    }),
    users: entity("users", {}),
  },
  ({ posts, comments, users }) => [
    relation(posts, "author").manyToOne(users),
    relation(comments, "post").manyToOne(posts),
    relation(comments, "user").manyToOne(users),
  ]
);

serve({
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      guard: { enabled: true },
      allow_register: true,
      default_role_register: "commenter",
      roles: {
        // Public: read published posts + approved comments
        anonymous: {
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
                {
                  condition: { entity: "comments" },
                  effect: "filter",
                  filter: { approved: true },
                },
              ],
            },
          ],
        },
        // Registered users: read all, create comments
        commenter: {
          implicit_allow: false,
          permissions: [
            "data.entity.read",
            {
              permission: "data.entity.create",
              effect: "allow",
              policies: [{
                condition: { entity: "comments" },
                effect: "allow",
              }],
            },
          ],
        },
        // Authors: full post access, manage own comments
        author: {
          implicit_allow: false,
          permissions: [
            "data.entity.read",
            {
              permission: "data.entity.create",
              effect: "allow",
              policies: [{
                condition: { entity: { $in: ["posts", "comments"] } },
                effect: "allow",
              }],
            },
            {
              permission: "data.entity.update",
              effect: "allow",
              policies: [{
                condition: { entity: "posts" },
                effect: "filter",
                filter: { author_id: "@user.id" },
              }],
            },
          ],
        },
        // Admin: everything
        admin: { implicit_allow: true },
      },
    },
  },
});
```

### SaaS Application

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },
    allow_register: true,
    default_role_register: "free_user",
    roles: {
      // Landing page data only
      anonymous: {
        is_default: true,
        implicit_allow: false,
        permissions: [
          {
            permission: "data.entity.read",
            effect: "allow",
            policies: [{
              condition: { entity: { $in: ["plans", "features"] } },
              effect: "allow",
            }],
          },
        ],
      },
      // Free tier: limited access
      free_user: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          {
            permission: "data.entity.create",
            effect: "allow",
            policies: [{
              condition: { entity: "projects" },
              effect: "allow",
            }],
          },
        ],
      },
      // Paid tier: full access to own data
      pro_user: {
        implicit_allow: false,
        permissions: [
          "data.entity.read",
          "data.entity.create",
          {
            permission: "data.entity.update",
            effect: "allow",
            policies: [{
              effect: "filter",
              filter: { owner_id: "@user.id" },
            }],
          },
          {
            permission: "data.entity.delete",
            effect: "allow",
            policies: [{
              effect: "filter",
              filter: { owner_id: "@user.id" },
            }],
          },
        ],
      },
      admin: { implicit_allow: true },
    },
  },
}
```

## Testing Access Levels

### Test Public Access

```bash
# Should succeed (anonymous read)
curl http://localhost:7654/api/data/posts

# Should fail (anonymous create)
curl -X POST http://localhost:7654/api/data/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
# Returns 403
```

### Test Authenticated Access

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "pass123"}' | jq -r '.token')

# Should succeed (authenticated create)
curl -X POST http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
```

### Test Entity-Specific Access

```bash
# Public entity - should succeed
curl http://localhost:7654/api/data/posts

# Private entity - should fail
curl http://localhost:7654/api/data/users
# Returns 403
```

### Test Filtered Access

```bash
# Anonymous: only sees published
curl http://localhost:7654/api/data/posts
# Returns: [{ status: "published" }, ...]

# Authenticated: sees all including drafts
curl http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer $TOKEN"
# Returns: [{ status: "draft" }, { status: "published" }, ...]
```

## Frontend Integration

### React: Check Auth State

```typescript
import { useApp, useAuth } from "bknd/react";

function DataDisplay() {
  const { api } = useApp();
  const { user } = useAuth();
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Works for both anonymous and authenticated
    api.data.readMany("posts").then((res) => {
      if (res.ok) setPosts(res.data);
    });
  }, []);

  return (
    <div>
      {posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          {/* Show edit only for authenticated users */}
          {user && <button>Edit</button>}
        </article>
      ))}

      {/* Show create only for authenticated */}
      {user ? (
        <button>New Post</button>
      ) : (
        <a href="/login">Login to create posts</a>
      )}
    </div>
  );
}
```

### Conditional Fetch

```typescript
function useProtectedData(entity: string) {
  const { api } = useApp();
  const { user, isLoading } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isLoading) return;

    api.data.readMany(entity).then((res) => {
      if (res.ok) {
        setData(res.data);
      } else {
        setError(res.error);
      }
    });
  }, [entity, user, isLoading]);

  return { data, error, isAuthenticated: !!user };
}

// Usage
function ProtectedPage() {
  const { data, error, isAuthenticated } = useProtectedData("projects");

  if (error?.status === 403 && !isAuthenticated) {
    return <LoginPrompt />;
  }

  return <DataList items={data} />;
}
```

## Common Pitfalls

### No Default Role = No Public Access

**Problem:** `Permission not granted` for unauthenticated requests

**Fix:** Add a default role:

```typescript
{
  roles: {
    anonymous: {
      is_default: true,  // Required for public access!
      permissions: ["data.entity.read"],
    },
  },
}
```

### Guard Disabled

**Problem:** Everyone can access everything

**Fix:** Enable the guard:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },  // Required!
  },
}
```

### Filter Not Applied

**Problem:** Anonymous users see all records, not just filtered

**Fix:** Use `effect: "filter"` not `effect: "allow"`:

```typescript
// WRONG - allows all
{
  condition: { entity: "posts" },
  effect: "allow",
  filter: { published: true },  // Ignored!
}

// CORRECT - applies filter
{
  condition: { entity: "posts" },
  effect: "filter",
  filter: { published: true },
}
```

### Sensitive Entity Exposed

**Problem:** Users entity publicly readable

**Fix:** Use entity conditions:

```typescript
{
  permissions: [
    {
      permission: "data.entity.read",
      effect: "allow",
      policies: [{
        // Only allow specific entities
        condition: { entity: { $in: ["posts", "comments"] } },
        effect: "allow",
      }],
    },
  ],
}
```

### Auth Header Not Sent

**Problem:** User authenticated but still gets public data

**Fix:** Include credentials in fetch:

```typescript
// Browser with cookies
fetch("/api/data/posts", { credentials: "include" });

// Token-based
fetch("/api/data/posts", {
  headers: { Authorization: `Bearer ${token}` },
});
```

## Access Matrix Reference

| Scenario | Anonymous Role | User Role | Result |
|----------|----------------|-----------|--------|
| Public Read | `data.entity.read` | All CRUD | Anon: read; User: CRUD |
| Private Only | None/No default | All CRUD | Anon: 403; User: CRUD |
| Entity-Specific | Read posts only | Read all | Anon: posts; User: all |
| Filtered | Filter published | Read all | Anon: published; User: all |

## DOs and DON'Ts

**DO:**
- Set `is_default: true` on exactly one role for public access
- Use entity conditions to limit which entities are public
- Use filter policies to expose only appropriate records
- Test access as both anonymous and authenticated users
- Keep sensitive entities (users, settings) protected

**DON'T:**
- Forget to enable guard (`guard: { enabled: true }`)
- Use `implicit_allow: true` on anonymous/default role
- Expose user data publicly without filters
- Assume auth header is always sent (check frontend code)
- Mix up `effect: "allow"` and `effect: "filter"`

## Related Skills

- **bknd-create-role** - Define roles for authorization
- **bknd-assign-permissions** - Configure detailed permissions
- **bknd-row-level-security** - Data-level access control
- **bknd-protect-endpoint** - Secure custom endpoints
- **bknd-setup-auth** - Initialize authentication system
