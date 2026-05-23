---
name: bknd-password-reset
description: Use when implementing password reset or change functionality in a Bknd application. Covers server-side password changes, building forgot-password flows with email tokens, and security considerations.
---

# Password Reset Flow

Implement password reset and change functionality in Bknd applications.

## Prerequisites

- Bknd project with auth enabled (`bknd-setup-auth`)
- Password strategy configured
- For email-based reset: email sending capability (external service)

## Important Context

Bknd provides:
- **Server-side `changePassword()`** method for admin/system password changes
- **No built-in forgot-password flow** - you must implement token generation, email sending, and validation

## When to Use UI Mode

- Admin-initiated password resets via admin panel

**UI steps:** Admin Panel > Data > users > Select user > Edit

Note: Direct password editing via UI sets raw value - use server-side method for proper hashing.

## When to Use Code Mode

- Implementing forgot-password flow with email
- Adding change-password functionality for logged-in users
- Admin tools for password resets

## Server-Side Password Change

### Using changePassword() Method

```typescript
import { serve } from "bknd/adapter/node";
import { defineConfig } from "bknd";

export default serve(
  defineConfig({ /* config */ }),
  {
    async seed(ctx) {
      // Change password by user ID
      await ctx.app.module.auth.changePassword(1, "newSecurePassword123");

      // Or find user first
      const { data: user } = await ctx.em.repo("users").findOne({
        email: "user@example.com",
      });
      if (user) {
        await ctx.app.module.auth.changePassword(user.id, "newPassword456");
      }
    },
  }
);
```

**Method signature:**

```typescript
changePassword(userId: number | string, newPassword: string): Promise<boolean>
```

**Constraints:**
- User must exist
- User must use password strategy (not OAuth)
- Password is automatically hashed using configured hashing method

## Building Forgot-Password Flow

Since Bknd doesn't have built-in forgot-password, implement a custom flow:

### Step 1: Create Reset Token Entity

```typescript
import { em, entity, text, date, number } from "bknd";

const schema = em({
  password_resets: entity("password_resets", {
    email: text().required(),
    token: text().required().unique(),
    expires_at: date().required(),
    used: number().default(0), // 0 = unused, 1 = used
  }),
});
```

### Step 2: Request Reset Endpoint

```typescript
import { randomBytes } from "crypto";

async function requestPasswordReset(email: string, ctx: any) {
  const api = ctx.api;

  // Check if user exists (don't reveal in response)
  const { data: user } = await api.data.readOneBy("users", { email });
  if (!user) {
    return { success: true, message: "If email exists, reset link sent" };
  }

  // Generate secure token
  const token = randomBytes(32).toString("hex");
  const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

  // Store reset token
  await api.data.createOne("password_resets", {
    email,
    token,
    expires_at: expiresAt.toISOString(),
    used: 0,
  });

  // Send email (use your email service: SendGrid, Resend, etc.)
  const resetUrl = `https://yourapp.com/reset-password?token=${token}`;
  // await emailService.send({ to: email, subject: "Password Reset", ... });

  return { success: true, message: "If email exists, reset link sent" };
}
```

### Step 3: Validate and Reset Password

```typescript
async function resetPassword(token: string, newPassword: string, ctx: any) {
  const api = ctx.api;
  const auth = ctx.app.module.auth;

  // Find valid token
  const { data: resetRecord } = await api.data.readOneBy("password_resets", {
    token,
    used: 0,
  });

  if (!resetRecord) {
    throw new Error("Invalid or expired reset token");
  }

  // Check expiration
  if (new Date(resetRecord.expires_at) < new Date()) {
    throw new Error("Reset token has expired");
  }

  // Find user
  const { data: user } = await api.data.readOneBy("users", {
    email: resetRecord.email,
  });
  if (!user) {
    throw new Error("User not found");
  }

  // Change password (properly hashed)
  await auth.changePassword(user.id, newPassword);

  // Mark token as used
  await api.data.updateOne("password_resets", resetRecord.id, { used: 1 });

  return { success: true };
}
```

### Step 4: React Frontend

**Request Reset Form:**

```tsx
function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "sent">("idle");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");

    await fetch("/api/password-reset/request", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    setStatus("sent");
  }

  if (status === "sent") {
    return <p>Check your email for reset instructions.</p>;
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
      <button type="submit" disabled={status === "loading"}>
        {status === "loading" ? "Sending..." : "Send Reset Link"}
      </button>
    </form>
  );
}
```

**Reset Password Form:**

```tsx
function ResetPasswordForm() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  if (!token) return <p>Invalid reset link.</p>;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const res = await fetch("/api/password-reset/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, password }),
    });

    if (res.ok) {
      navigate("/login");
    } else {
      const data = await res.json();
      setError(data.message || "Reset failed");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <p className="error">{error}</p>}
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="New Password"
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
      <button type="submit">Reset Password</button>
    </form>
  );
}
```

## Authenticated Password Change

For logged-in users changing their own password:

```typescript
async function changePassword(currentPassword: string, newPassword: string) {
  const api = new Api({ host: "http://localhost:7654", storage: localStorage });

  // Verify current password by re-authenticating
  const { data: userData } = await api.auth.me();
  if (!userData?.user) throw new Error("Not authenticated");

  const { ok } = await api.auth.login("password", {
    email: userData.user.email,
    password: currentPassword,
  });

  if (!ok) throw new Error("Current password is incorrect");

  // Call custom password change endpoint
  const res = await fetch("/api/password-change", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ newPassword }),
  });

  if (!res.ok) throw new Error("Failed to change password");
}
```

## Security Considerations

### Token Security

```typescript
// Good: Cryptographically secure token
import { randomBytes } from "crypto";
const token = randomBytes(32).toString("hex"); // 64 chars

// Bad: Predictable token
const token = Math.random().toString(36); // NOT secure!
```

### Rate Limiting

```typescript
const resetAttempts = new Map<string, { count: number; lastAttempt: Date }>();

function checkRateLimit(email: string): boolean {
  const record = resetAttempts.get(email);
  const now = new Date();

  if (!record || record.lastAttempt < new Date(now.getTime() - 3600000)) {
    resetAttempts.set(email, { count: 1, lastAttempt: now });
    return true;
  }

  if (record.count >= 3) return false; // Max 3 per hour

  record.count++;
  return true;
}
```

## Common Pitfalls

### Not Hashing Password

```typescript
// Wrong - bypasses hashing
await api.data.updateOne("users", userId, {
  strategy_value: "plainPassword123",
});

// Correct - uses configured hashing
await ctx.app.module.auth.changePassword(userId, "plainPassword123");
```

### Email Enumeration

```typescript
// Wrong - reveals email existence
if (!user) return { error: "Email not found" };

// Correct - doesn't reveal
return { success: true, message: "If email exists, reset link sent" };
```

### OAuth User Password Reset

```typescript
const { data: user } = await api.data.readOneBy("users", { email });
if (user?.strategy !== "password") {
  return { error: "This account uses social login" };
}
```

## Verification

```bash
# 1. Request reset
curl -X POST http://localhost:7654/api/password-reset/request \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'

# 2. Reset password (use token from email/DB)
curl -X POST http://localhost:7654/api/password-reset/confirm \
  -H "Content-Type: application/json" \
  -d '{"token": "<token>", "password": "newPassword123"}'

# 3. Login with new password
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "newPassword123"}'
```

## DOs and DON'Ts

**DO:**
- Use `changePassword()` method for proper hashing
- Generate cryptographically secure tokens
- Set short expiration (1 hour max)
- Mark tokens as used immediately
- Return consistent responses (don't reveal email existence)
- Rate limit reset requests

**DON'T:**
- Store/transmit passwords in plain text
- Use predictable tokens (Math.random)
- Allow unlimited reset attempts
- Keep tokens valid indefinitely
- Allow password reset for OAuth users

## Related Skills

- **bknd-setup-auth** - Configure authentication system
- **bknd-login-flow** - Login/logout functionality
- **bknd-registration** - User registration setup
- **bknd-session-handling** - Manage user sessions
- **bknd-custom-endpoint** - Create custom API endpoints
