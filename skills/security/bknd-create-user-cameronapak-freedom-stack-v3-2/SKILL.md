---
name: bknd-create-user
description: Use when creating a new user account in Bknd programmatically. Covers auth.createUser() in seed functions, registration via SDK/REST API, creating users via data API, admin panel user creation, and role assignment.
---

# Create User

Create new user accounts in Bknd via seed functions, SDK, REST API, or admin panel.

## Prerequisites

- Bknd project running (local or deployed)
- Auth module enabled (`auth.enabled: true`)
- Password strategy configured (enabled by default)
- For role assignment: roles defined in auth config

## When to Use UI Mode

- Creating admin/test users during development
- Manual user management by non-technical admins
- One-off user creation

**UI steps:** Admin Panel > Auth > Users > Click "+" > Fill email/password > Select role > Save

## When to Use Code Mode

- Seeding initial admin users on first deploy
- Programmatic user creation in server code
- User registration flows in your frontend
- Automated user provisioning

## Code Approach

### Method 1: Seed Function (Recommended for Initial Users)

Create users on first app startup via seed function:

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
      jwt: { secret: process.env.JWT_SECRET || "dev-secret" },
      roles: {
        admin: { implicit_allow: true },
        user: { implicit_allow: false },
      },
    },
  },
  options: {
    seed: async (ctx) => {
      // Create admin user on first run
      await ctx.app.module.auth.createUser({
        email: "admin@example.com",
        password: "securepassword123",
        role: "admin",
      });
      console.log("Admin user created");
    },
  },
});
```

**Seed function notes:**
- Runs only on first startup when database is empty
- Has full access to `ctx.app.module.auth`
- Ideal for creating initial admin accounts

### Method 2: Server-Side createUser()

Create users programmatically in server code (plugins, flows, custom endpoints):

```typescript
import { getApi } from "bknd";

// In a plugin, flow, or custom endpoint handler
async function createAdminUser(app) {
  const user = await app.module.auth.createUser({
    email: "newadmin@example.com",
    password: "securepassword123",
    role: "admin",
  });

  console.log("Created user:", user.id, user.email);
  return user;
}

// With additional fields (if users entity has custom fields)
async function createUserWithProfile(app) {
  const user = await app.module.auth.createUser({
    email: "user@example.com",
    password: "password123",
    role: "user",
    name: "John Doe",        // Custom field
    avatar: "https://...",   // Custom field
  });
  return user;
}
```

**createUser() signature:**
```typescript
type CreateUserPayload = {
  email: string;      // Required: user email
  password: string;   // Required: plain text (will be hashed)
  role?: string;      // Optional: must exist in auth.roles
  [key: string]: any; // Additional fields for users entity
};

// Returns the created user record
async createUser(payload: CreateUserPayload): Promise<User>
```

### Method 3: SDK Registration (Client-Side)

For user self-registration via your frontend:

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,  // For token persistence
});

// Register new user
const { ok, data, error } = await api.auth.register("password", {
  email: "newuser@example.com",
  password: "securepassword123",
});

if (ok) {
  console.log("Registered:", data.user);
  console.log("Token:", data.token);
  // User is now logged in, token stored in localStorage
} else {
  console.error("Registration failed:", error);
}
```

**Registration notes:**
- Requires `auth.allow_register: true` (default)
- Assigns `auth.default_role_register` role automatically
- Returns JWT token (user is logged in after registration)
- Only accepts email/password; additional fields need separate update

### Method 4: REST API Registration

```bash
# Register via REST API
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Method 5: Data API (Admin Creating Users)

Admins can create users directly via data API (requires auth + admin role):

```typescript
// As authenticated admin
const { ok, data } = await api.data.createOne("users", {
  email: "managed@example.com",
  strategy: "password",
  strategy_value: "HASHED_PASSWORD",  // Must be pre-hashed!
  role: "user",
});
```

**Warning:** Data API requires pre-hashed password. Use `createUser()` or registration instead for proper password handling.

## React Integration

### Registration Form

```tsx
import { useApp } from "bknd/react";
import { useState } from "react";

function RegisterForm() {
  const { api } = useApp();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { ok, data, error: apiError } = await api.auth.register("password", {
      email,
      password,
    });

    setLoading(false);

    if (ok) {
      console.log("Registered:", data.user);
      // Redirect to dashboard or show success
    } else {
      setError(apiError?.message || "Registration failed");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        minLength={8}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Creating account..." : "Register"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
```

### Using useAuth Hook

```tsx
import { useAuth } from "@bknd/react";

function AuthStatus() {
  const { user, isLoading, register, logout } = useAuth();

  if (isLoading) return <div>Loading...</div>;

  if (!user) {
    return (
      <button onClick={() => register("password", {
        email: "new@example.com",
        password: "password123"
      })}>
        Create Account
      </button>
    );
  }

  return (
    <div>
      <p>Welcome, {user.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## Configuration Options

### Enable/Disable Registration

```typescript
{
  auth: {
    enabled: true,
    allow_register: true,  // Set to false to disable self-registration
    default_role_register: "user",  // Role assigned on registration
  },
}
```

### Password Requirements

```typescript
{
  auth: {
    strategies: {
      password: {
        type: "password",
        enabled: true,
        config: {
          hashing: "bcrypt",   // "plain" | "sha256" | "bcrypt"
          rounds: 4,           // bcrypt rounds (1-10)
          minLength: 8,        // Minimum password length
        },
      },
    },
  },
}
```

### Define Roles for Assignment

```typescript
{
  auth: {
    roles: {
      admin: {
        implicit_allow: true,  // Can do everything
      },
      editor: {
        implicit_allow: false,
        permissions: [
          { permission: "data.posts.read", effect: "allow" },
          { permission: "data.posts.create", effect: "allow" },
          { permission: "data.posts.update", effect: "allow" },
        ],
      },
      user: {
        implicit_allow: false,
        permissions: [
          { permission: "data.posts.read", effect: "allow" },
        ],
      },
    },
    default_role_register: "user",  // New registrations get this role
  },
}
```

## Extending Users Entity

Add custom fields to users:

```typescript
import { em, entity, text, date } from "bknd";

const schema = em({
  users: entity("users", {
    email: text().required().unique(),
    name: text(),
    avatar: text(),
    bio: text(),
    created_at: date({ default_value: "now" }),
  }),
});

// In config
{
  config: {
    data: schema.toJSON(),
    auth: { enabled: true, /* ... */ },
  },
}
```

**Note:** `strategy` and `strategy_value` fields are managed by auth system - don't modify directly.

## Common Pitfalls

### Registration Disabled

**Problem:** `Registration not allowed` error

**Fix:** Enable registration:
```typescript
{ auth: { allow_register: true } }
```

### Role Not Found

**Problem:** `Role "admin" not found` error

**Fix:** Define role in config before assigning:
```typescript
{
  auth: {
    roles: {
      admin: { implicit_allow: true },
    },
  },
}
```

### User Already Exists

**Problem:** `User already exists` or `UNIQUE constraint failed`

**Fix:** Check before creating or handle error:
```typescript
// SDK registration handles this automatically
const { ok, error } = await api.auth.register("password", { email, password });
if (!ok && error?.message?.includes("exists")) {
  console.log("Email already registered");
}

// Server-side: check first
const { data: exists } = await api.data.exists("users", {
  email: { $eq: email },
});
if (!exists.exists) {
  await app.module.auth.createUser({ email, password });
}
```

### Weak JWT Secret

**Problem:** `Cannot sign JWT without secret` or security warnings

**Fix:** Set strong JWT secret:
```typescript
{
  auth: {
    jwt: {
      secret: process.env.JWT_SECRET,  // Use env var, 256-bit minimum
    },
  },
}
```

### Password Not Hashed (Data API)

**Problem:** User can't login after creating via data API

**Cause:** Data API doesn't hash passwords automatically

**Fix:** Use `createUser()` or registration instead:
```typescript
// Wrong - password not hashed
await api.data.createOne("users", { email, password: "plain" });

// Correct - use auth module
await app.module.auth.createUser({ email, password: "plain" });
```

### Additional Fields Not Saved

**Problem:** Custom fields not included after registration

**Cause:** Registration only accepts email/password

**Fix:** Update user after registration:
```typescript
const { data } = await api.auth.register("password", { email, password });

// Update with additional fields
await api.data.updateOne("users", data.user.id, {
  name: "John Doe",
  avatar: "https://...",
});
```

## Verification

After creating a user, verify:

```typescript
// SDK - check current user after registration
const { data } = await api.auth.me();
console.log("Current user:", data?.user);

// Server-side - read back
const { data: user } = await api.data.readOneBy("users", {
  where: { email: { $eq: "user@example.com" } },
});
console.log("Created user:", user);
```

Or via admin panel: Admin Panel > Auth > Users > Find new user in list.

## DOs and DON'Ts

**DO:**
- Use `createUser()` or registration for proper password hashing
- Use seed function for initial admin users
- Set strong JWT secrets in production
- Define roles before assigning them
- Use bcrypt hashing in production

**DON'T:**
- Create users via data API (passwords won't be hashed correctly)
- Store plain text passwords
- Use weak JWT secrets in production
- Assign roles that don't exist
- Modify `strategy` or `strategy_value` fields directly

## Related Skills

- **bknd-setup-auth** - Initialize authentication system
- **bknd-login-flow** - Implement login/logout functionality
- **bknd-registration** - Set up user registration flows
- **bknd-create-role** - Define roles for user assignment
- **bknd-assign-permissions** - Configure role permissions
