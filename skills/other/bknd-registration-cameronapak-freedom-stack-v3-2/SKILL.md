---
name: bknd-registration
description: Use when setting up user registration flows in a Bknd application. Covers registration configuration, enabling/disabling registration, default roles, password validation, registration forms, and custom fields.
---

# User Registration Setup

Configure and implement user self-registration in Bknd applications.

## Prerequisites

- Bknd project with auth enabled (`bknd-setup-auth`)
- Password strategy configured
- For SDK: `bknd` package installed

## When to Use UI Mode

- Testing registration endpoint via admin panel
- Viewing registered users

**UI steps:** Admin Panel > Auth > Test password/register endpoint

## When to Use Code Mode

- Building registration forms in frontend
- Configuring registration settings
- Adding validation and error handling

## Registration Configuration

### Enable/Disable Registration

```typescript
import { serve } from "bknd/adapter/bun";

serve({
  connection: { url: "file:data.db" },
  config: {
    auth: {
      enabled: true,
      allow_register: true,  // Enable self-registration (default: true)
      default_role_register: "user",  // Role assigned on registration
      strategies: {
        password: {
          type: "password",
          config: {
            hashing: "bcrypt",  // "plain" | "sha256" | "bcrypt"
            minLength: 8,       // Minimum password length
          },
        },
      },
      roles: {
        user: { implicit_allow: false },
      },
    },
  },
});
```

**Config options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `allow_register` | boolean | `true` | Enable self-registration |
| `default_role_register` | string | - | Role for new users |
| `minLength` | number | 8 | Minimum password length |

## SDK Registration

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,  // Persist token
});

async function register(email: string, password: string) {
  const { ok, data, status } = await api.auth.register("password", {
    email,
    password,
  });

  if (ok) {
    // Token stored automatically - user is logged in
    return data.user;
  }

  if (status === 409) throw new Error("Email already registered");
  if (status === 400) throw new Error("Invalid email or password");
  throw new Error("Registration failed");
}
```

**Response:**
```typescript
{
  ok: boolean;
  data?: {
    user: { id: number; email: string; role?: string };
    token: string;
  };
  status: number;
}
```

## REST API Registration

```bash
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'
```

**Responses:**

| Status | Meaning |
|--------|---------|
| 201 | Success - returns user + token |
| 400 | Invalid email/password or too short |
| 403 | Registration disabled |
| 409 | Email already registered |

## React Integration

### Registration Form

```tsx
import { useState } from "react";
import { useApp } from "bknd/react";

function RegisterForm({ onSuccess }: { onSuccess?: () => void }) {
  const { api } = useApp();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setLoading(true);
    const { ok, status } = await api.auth.register("password", {
      email,
      password,
    });
    setLoading(false);

    if (ok) {
      onSuccess?.();
    } else if (status === 409) {
      setError("Email already registered");
    } else {
      setError("Registration failed");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <p className="error">{error}</p>}
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
      <input
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        placeholder="Confirm Password"
        required
      />
      <button disabled={loading}>
        {loading ? "Creating..." : "Create Account"}
      </button>
    </form>
  );
}
```

### Using useAuth Hook

```tsx
import { useAuth } from "@bknd/react";

function RegisterPage() {
  const { user, isLoading, register } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (user) return <Navigate to="/dashboard" />;

  async function handleRegister(email: string, password: string) {
    await register("password", { email, password });
  }

  return <RegisterForm onSuccess={() => navigate("/dashboard")} />;
}
```

## Custom Fields After Registration

Registration only accepts `email` and `password`. Add custom fields after:

```typescript
// 1. Extend users entity
const schema = em({
  users: entity("users", {
    email: text().required().unique(),
    name: text(),
    avatar: text(),
  }),
});

// 2. Update user after registration
const { data } = await api.auth.register("password", { email, password });

await api.data.updateOne("users", data.user.id, {
  name: "John Doe",
  avatar: "https://...",
});
```

## Invite-Only Apps

Disable public registration:

```typescript
{
  auth: {
    allow_register: false,  // Disable self-registration
  },
}

// Admin creates users via seed or plugin
await app.module.auth.createUser({
  email: "invited@example.com",
  password: tempPassword,
  role: "user",
});
```

## Common Pitfalls

### Registration Disabled

**Problem:** `Registration not allowed` (403)

**Fix:** `{ auth: { allow_register: true } }`

### Role Not Found

**Problem:** `Role "user" not found`

**Fix:** Define role before using:
```typescript
{
  auth: {
    roles: { user: { implicit_allow: false } },
    default_role_register: "user",
  },
}
```

### User Already Exists

**Problem:** 409 error

**Fix:** Handle gracefully:
```tsx
if (status === 409) {
  setError("Email already registered. Try logging in instead.");
}
```

### Token Not Stored

**Problem:** User not logged in after registration

**Fix:** Provide storage:
```typescript
const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,  // Required for persistence
});
```

### Custom Fields Ignored

**Problem:** Extra fields passed to registration not saved

**Cause:** Registration only accepts email/password

**Fix:** Update user after registration (see Custom Fields section)

## Verification

```bash
# 1. Test registration
curl -X POST http://localhost:7654/api/auth/password/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# 2. Verify token works
curl http://localhost:7654/api/auth/me \
  -H "Authorization: Bearer <token>"
```

## DOs and DON'Ts

**DO:**
- Use bcrypt hashing in production
- Validate password length client-side to match server config
- Handle 409 error with login suggestion
- Store token with `storage: localStorage`
- Define roles before using `default_role_register`

**DON'T:**
- Use `hashing: "plain"` in production
- Expect custom fields in registration payload
- Forget to handle registration errors
- Disable registration without alternative user creation

## Related Skills

- **bknd-setup-auth** - Configure authentication system
- **bknd-create-user** - Programmatic user creation (admin/seed)
- **bknd-login-flow** - Login/logout functionality
- **bknd-password-reset** - Password reset flow
