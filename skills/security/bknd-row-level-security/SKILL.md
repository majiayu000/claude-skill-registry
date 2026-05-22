---
name: bknd-row-level-security
description: Use when implementing row-level security (RLS) in Bknd. Covers filter policies, user ownership patterns, public/private records, entity-specific RLS, multi-tenant isolation, and data-level access control.
---

# Row-Level Security (RLS)

Implement data-level access control using filter policies to restrict which records users can access.

## Prerequisites

- Bknd project with code-first configuration
- Auth enabled (`auth: { enabled: true }`)
- Guard enabled (`guard: { enabled: true }`)
- At least one role defined (see **bknd-create-role**)
- Entity with ownership field (e.g., `user_id`)

## When to Use UI Mode

- Viewing current role policies
- Quick policy inspection

**UI steps:** Admin Panel > Auth > Roles > Select role

**Note:** RLS configuration requires code mode. UI is read-only.

## When to Use Code Mode

- Implementing row-level security
- Creating filter policies
- Entity-specific data isolation
- Multi-tenant patterns

## Code Approach

### Step 1: Add Ownership Field to Entity

Ensure entity has a field to track ownership:

```typescript
import { serve } from "bknd/adapter/bun";
import { em, entity, text, number } from "bknd";

const schema = em({
  posts: entity("posts", {
    title: text().required(),
    content: text(),
    user_id: number().required(),  // Ownership field
  }),
});
```

### Step 2: Basic RLS - Own Records Only

Users can only read their own records:

```typescript
serve({
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
    auth: {
      enabled: true,
      guard: { enabled: true },
      roles: {
        user: {
          implicit_allow: false,
          permissions: [
            {
              permission: "data.entity.read",
              effect: "allow",
              policies: [
                {
                  description: "Users read own records only",
                  effect: "filter",
                  filter: { user_id: "@user.id" },
                },
              ],
            },
          ],
        },
      },
    },
  },
});
```

### How Filter Policies Work

| Component | Purpose |
|-----------|---------|
| `effect: "filter"` | Apply row-level filtering (not allow/deny) |
| `filter` | Query conditions added to every request |
| `@user.id` | Variable replaced with current user's ID |

When user with ID 5 queries posts, the filter transforms:
```typescript
// User's query
api.data.readMany("posts", { where: { status: "published" } });

// Becomes (with RLS filter applied)
api.data.readMany("posts", { where: { status: "published", user_id: 5 } });
```

### Step 3: Full CRUD with RLS

Apply RLS to all operations:

```typescript
{
  roles: {
    user: {
      implicit_allow: false,
      permissions: [
        // Read: own records
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { user_id: "@user.id" },
          }],
        },
        // Create: allowed (user_id set via hook/plugin)
        { permission: "data.entity.create", effect: "allow" },
        // Update: own records
        {
          permission: "data.entity.update",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { user_id: "@user.id" },
          }],
        },
        // Delete: own records
        {
          permission: "data.entity.delete",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { user_id: "@user.id" },
          }],
        },
      ],
    },
  },
}
```

### Step 4: Entity-Specific RLS

Different RLS rules per entity:

```typescript
{
  roles: {
    user: {
      implicit_allow: false,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [
            // Posts: filter by author
            {
              condition: { entity: "posts" },
              effect: "filter",
              filter: { author_id: "@user.id" },
            },
            // Comments: filter by user
            {
              condition: { entity: "comments" },
              effect: "filter",
              filter: { user_id: "@user.id" },
            },
            // Categories: no filter (public)
            {
              condition: { entity: "categories" },
              effect: "allow",
            },
          ],
        },
      ],
    },
  },
}
```

### Step 5: Public + Private Records

Users see public records AND their own private records:

```typescript
{
  permissions: [
    {
      permission: "data.entity.read",
      effect: "allow",
      policies: [
        {
          condition: { entity: "posts" },
          effect: "filter",
          filter: {
            $or: [
              { is_public: true },      // Public posts
              { user_id: "@user.id" },  // Own posts
            ],
          },
        },
      ],
    },
  ],
}
```

### Step 6: Draft/Published Pattern

Authors see their drafts, everyone sees published:

```typescript
{
  roles: {
    author: {
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [
            {
              condition: { entity: "posts" },
              effect: "filter",
              filter: {
                $or: [
                  { status: "published" },  // Anyone can read published
                  { author_id: "@user.id" }, // Author reads own drafts
                ],
              },
            },
          ],
        },
      ],
    },
    viewer: {
      is_default: true,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [
            {
              condition: { entity: "posts" },
              effect: "filter",
              filter: { status: "published" },  // Only published
            },
          ],
        },
      ],
    },
  },
}
```

## Common RLS Patterns

### Multi-Tenant Isolation

Isolate data by organization/tenant:

```typescript
const schema = em({
  organizations: entity("organizations", {
    name: text().required(),
  }),
  projects: entity("projects", {
    name: text().required(),
    org_id: number().required(),
  }),
  tasks: entity("tasks", {
    title: text().required(),
    org_id: number().required(),
  }),
});

// Assuming user has org_id field
{
  roles: {
    member: {
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [
            {
              condition: { entity: { $in: ["projects", "tasks"] } },
              effect: "filter",
              filter: { org_id: "@user.org_id" },
            },
          ],
        },
        {
          permission: "data.entity.create",
          effect: "allow",
          policies: [
            {
              condition: { entity: { $in: ["projects", "tasks"] } },
              effect: "allow",
            },
          ],
        },
      ],
    },
  },
}
```

### Team-Based Access

Users access records belonging to their team:

```typescript
// Assuming user has team_id field
{
  roles: {
    team_member: {
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { team_id: "@user.team_id" },
          }],
        },
        {
          permission: "data.entity.update",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { team_id: "@user.team_id" },
          }],
        },
      ],
    },
  },
}
```

### Hierarchical Access (Manager Pattern)

Manager sees their reports' data:

```typescript
// Manager sees records where:
// - They own the record, OR
// - Record belongs to someone they manage
// Note: This pattern may require custom logic via hooks
{
  roles: {
    manager: {
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: {
              $or: [
                { user_id: "@user.id" },
                { manager_id: "@user.id" },
              ],
            },
          }],
        },
      ],
    },
  },
}
```

### Anonymous Read, Authenticated Write

```typescript
{
  roles: {
    anonymous: {
      is_default: true,
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            condition: { entity: "posts" },
            effect: "filter",
            filter: { is_public: true },
          }],
        },
      ],
    },
    user: {
      permissions: [
        // Read: public + own
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            condition: { entity: "posts" },
            effect: "filter",
            filter: {
              $or: [
                { is_public: true },
                { user_id: "@user.id" },
              ],
            },
          }],
        },
        // Create/Update/Delete: own only
        { permission: "data.entity.create", effect: "allow" },
        {
          permission: "data.entity.update",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { user_id: "@user.id" },
          }],
        },
        {
          permission: "data.entity.delete",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { user_id: "@user.id" },
          }],
        },
      ],
    },
  },
}
```

### Admin Bypass

Admin sees everything, users see own:

```typescript
{
  roles: {
    admin: {
      implicit_allow: true,  // No RLS filters applied
    },
    user: {
      permissions: [
        {
          permission: "data.entity.read",
          effect: "allow",
          policies: [{
            effect: "filter",
            filter: { user_id: "@user.id" },
          }],
        },
      ],
    },
  },
}
```

## Setting User Ownership on Create

RLS filters query results but you also need to set ownership on creation.

### Option 1: Client Sets user_id

```typescript
// Frontend code
const api = new Api({ baseUrl: "http://localhost:7654/api" });
const user = await api.auth.me();

await api.data.createOne("posts", {
  title: "My Post",
  user_id: user.id,  // Client sets ownership
});
```

### Option 2: Server Hook (Recommended)

Use Bknd events to auto-set ownership:

```typescript
import { serve } from "bknd/adapter/bun";
import { DataRecordMutatingEvent } from "bknd";

serve({
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
    auth: { /* ... */ },
  },
  options: {
    onBuild: async (app) => {
      const events = app.modules.get("events");

      events.on(DataRecordMutatingEvent, async (event) => {
        if (event.data.action === "create") {
          const authModule = app.modules.get("auth");
          const user = await authModule.resolveAuthFromRequest(event.data.ctx?.request);

          if (user && !event.data.record.user_id) {
            event.data.record.user_id = user.id;
          }
        }
      });
    },
  },
});
```

## Verification

### 1. Create Test Users

```bash
# User 1
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@test.com", "password": "pass123"}'

# User 2
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user2@test.com", "password": "pass123"}'
```

### 2. Create Records as User 1

```bash
# Login as user1
TOKEN1=$(curl -s -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@test.com", "password": "pass123"}' | jq -r '.token')

# Create post
curl -X POST http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer $TOKEN1" \
  -H "Content-Type: application/json" \
  -d '{"title": "User1 Post", "user_id": 1}'
```

### 3. Verify RLS as User 2

```bash
# Login as user2
TOKEN2=$(curl -s -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user2@test.com", "password": "pass123"}' | jq -r '.token')

# Query posts - should NOT see user1's posts
curl http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer $TOKEN2"
# Expected: empty array or only user2's posts
```

### 4. Verify Update RLS

```bash
# User2 try to update user1's post - should fail or affect 0 rows
curl -X PATCH http://localhost:7654/api/data/posts/1 \
  -H "Authorization: Bearer $TOKEN2" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hacked!"}'
# Expected: 404 or 0 affected (record filtered out)
```

## Common Pitfalls

### Filter Not Applied

**Problem:** RLS filter not restricting data

**Fix:** Ensure guard is enabled:

```typescript
{
  auth: {
    enabled: true,
    guard: { enabled: true },  // Required!
  },
}
```

### Wrong Variable Placeholder

**Problem:** Using `@id` instead of `@user.id`

**Fix:** Use correct placeholders:

| Placeholder | Meaning |
|-------------|---------|
| `@user.id` | Current user's ID |
| `@user.email` | Current user's email |
| `@id` | Current record ID (not user) |

```typescript
// WRONG - @id is record ID, not user ID
filter: { user_id: "@id" }

// CORRECT
filter: { user_id: "@user.id" }
```

### Missing Entity Condition

**Problem:** RLS applies to wrong entities

**Fix:** Add entity condition for entity-specific RLS:

```typescript
// WRONG - applies to ALL entities
policies: [{
  effect: "filter",
  filter: { user_id: "@user.id" },
}]

// CORRECT - only posts entity
policies: [{
  condition: { entity: "posts" },
  effect: "filter",
  filter: { user_id: "@user.id" },
}]
```

### Filter vs Allow/Deny Confusion

**Problem:** Using `effect: "allow"` when you need filtering

**Fix:** Understand the difference:

| Effect | Purpose |
|--------|---------|
| `allow` | Grant permission (no data filtering) |
| `deny` | Block permission entirely |
| `filter` | Allow but filter results |

```typescript
// WRONG - allows all, no filtering
{ effect: "allow", filter: { user_id: "@user.id" } }

// CORRECT - filters results
{ effect: "filter", filter: { user_id: "@user.id" } }
```

### Ownership Not Set on Create

**Problem:** New records have null user_id

**Fix:** Either set in client or use server hook (see "Setting User Ownership" section above)

### Complex $or Filter Not Working

**Problem:** `$or` filter returning wrong results

**Fix:** Verify syntax:

```typescript
// CORRECT $or syntax
filter: {
  $or: [
    { is_public: true },
    { user_id: "@user.id" },
  ],
}
```

## DOs and DON'Ts

**DO:**
- Add ownership field (`user_id`) to entities needing RLS
- Use `effect: "filter"` for row-level restrictions
- Add entity conditions for entity-specific rules
- Test with multiple users to verify isolation
- Combine RLS with ownership assignment hooks

**DON'T:**
- Confuse `@id` (record) with `@user.id` (user)
- Forget `guard: { enabled: true }`
- Mix `effect: "allow"` with `filter` field (use `effect: "filter"`)
- Apply same filter to entities with different ownership fields
- Trust client to set ownership without validation

## Related Skills

- **bknd-create-role** - Define roles for RLS
- **bknd-assign-permissions** - Configure role permissions
- **bknd-protect-endpoint** - Secure specific endpoints
- **bknd-public-vs-auth** - Public vs authenticated access
- **bknd-crud-read** - Query data with filters
