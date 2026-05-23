---
name: bknd-login-flow
description: Use when implementing login and logout functionality in a Bknd application. Covers SDK authentication methods, REST API endpoints, React integration, session checking, and error handling.
---

# Login/Logout Flow

Implement user authentication flow with login, logout, and session checking in Bknd.

## Prerequisites

- Bknd project with auth enabled (`bknd-setup-auth`)
- At least one auth strategy configured (password, OAuth)
- For SDK: `bknd` package installed
- For React: `@bknd/react` package installed

## When to Use UI Mode

- Testing login/logout endpoints via admin panel
- Viewing active sessions
- Checking user authentication status

**UI steps:** Admin Panel > Auth > Test endpoints

## When to Use Code Mode

- Implementing login forms in your frontend
- Adding logout functionality
- Checking authentication state
- Building protected routes
- Handling authentication errors

## SDK Approach

### Initialize API Client

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,  // Persist token between sessions
});
```

**SDK options:**

| Option | Type | Description |
|--------|------|-------------|
| `host` | string | Backend URL |
| `storage` | Storage | Token persistence (localStorage, sessionStorage) |
| `token` | string | Pre-set auth token |
| `tokenTransport` | `"header"` \| `"cookie"` | How token is sent (default: header) |

### Login with Password Strategy

```typescript
async function login(email: string, password: string) {
  const { ok, data, error, status } = await api.auth.login("password", {
    email,
    password,
  });

  if (ok) {
    // Token automatically stored in localStorage
    console.log("Logged in as:", data.user.email);
    console.log("User ID:", data.user.id);
    console.log("Role:", data.user.role);
    return data.user;
  }

  // Handle errors
  if (status === 401) {
    throw new Error("Invalid email or password");
  }
  if (status === 403) {
    throw new Error("Account uses different login method");
  }
  throw new Error(error?.message || "Login failed");
}
```

**Login response:**

```typescript
type LoginResponse = {
  ok: boolean;
  status: number;
  data?: {
    user: {
      id: number | string;
      email: string;
      role?: string;
      // Custom fields...
    };
    token: string;
  };
  error?: { message: string };
};
```

### Check Current User

```typescript
async function getCurrentUser() {
  const { ok, data } = await api.auth.me();

  if (ok && data?.user) {
    return data.user;  // User is authenticated
  }
  return null;  // Not authenticated
}
```

### Logout

```typescript
async function logout() {
  await api.auth.logout();
  // Token removed from storage
  // User is now logged out
}
```

### Check If Authenticated

```typescript
async function isAuthenticated(): Promise<boolean> {
  const { ok, data } = await api.auth.me();
  return ok && data?.user !== null;
}
```

### Complete Login Flow Example

```typescript
import { Api } from "bknd";

class AuthService {
  private api: Api;

  constructor() {
    this.api = new Api({
      host: import.meta.env.VITE_API_URL || "http://localhost:7654",
      storage: localStorage,
    });
  }

  async login(email: string, password: string) {
    const result = await this.api.auth.login("password", { email, password });

    if (!result.ok) {
      throw new AuthError(result.status, result.error?.message);
    }

    return result.data!.user;
  }

  async logout() {
    await this.api.auth.logout();
  }

  async getUser() {
    const { ok, data } = await this.api.auth.me();
    return ok ? data?.user : null;
  }

  async isAuthenticated() {
    const user = await this.getUser();
    return user !== null;
  }
}

class AuthError extends Error {
  constructor(public status: number, message?: string) {
    super(message || "Authentication failed");
    this.name = "AuthError";
  }
}

// Usage
const auth = new AuthService();

try {
  const user = await auth.login("user@example.com", "password123");
  console.log("Welcome,", user.email);
} catch (e) {
  if (e instanceof AuthError && e.status === 401) {
    console.error("Wrong credentials");
  }
}
```

## REST API Approach

### Login via REST

```bash
# Login
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
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

### Use Token in Requests

```bash
# Get current user
curl http://localhost:7654/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

# Access protected data
curl http://localhost:7654/api/data/posts \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Logout via REST

```bash
curl -X POST http://localhost:7654/api/auth/logout \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Note:** Logout clears server-side cookie. For header-based auth, client must discard token.

### REST Endpoints Reference

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/password/login` | Login with email/password |
| GET | `/api/auth/me` | Get current authenticated user |
| POST | `/api/auth/logout` | Log out (clear session) |
| GET | `/api/auth/strategies` | List available strategies |

## React Integration

### Using useAuth Hook

```tsx
import { BkndProvider, useAuth } from "@bknd/react";

function App() {
  return (
    <BkndProvider config={{ host: "http://localhost:7654" }}>
      <AuthExample />
    </BkndProvider>
  );
}

function AuthExample() {
  const { user, isLoading, login, logout } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <LoginForm onLogin={login} />;
  }

  return (
    <div>
      <p>Welcome, {user.email}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### Login Form Component

```tsx
import { useState } from "react";
import { useAuth } from "@bknd/react";

function LoginForm() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await login("password", { email, password });
      // Redirect or update UI - user state updates automatically
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}

      <label>
        Email:
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </label>

      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </label>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Logging in..." : "Login"}
      </button>
    </form>
  );
}
```

### Protected Route Pattern

```tsx
import { Navigate } from "react-router-dom";
import { useAuth } from "@bknd/react";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

// Usage with React Router
function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
```

### Logout Button Component

```tsx
import { useAuth } from "@bknd/react";
import { useNavigate } from "react-router-dom";

function LogoutButton() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return <button onClick={handleLogout}>Logout</button>;
}
```

### Manual API with React

If not using `@bknd/react`:

```tsx
import { useState, useEffect, createContext, useContext } from "react";
import { Api } from "bknd";

type User = { id: number; email: string; role?: string };

type AuthContextType = {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check auth on mount
  useEffect(() => {
    api.auth.me().then(({ ok, data }) => {
      setUser(ok ? data?.user ?? null : null);
      setIsLoading(false);
    });
  }, []);

  async function login(email: string, password: string) {
    const { ok, data, error } = await api.auth.login("password", {
      email,
      password,
    });

    if (!ok) {
      throw new Error(error?.message || "Login failed");
    }

    setUser(data!.user);
  }

  async function logout() {
    await api.auth.logout();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
```

## Cookie-Based Authentication

For browser apps with cookie transport:

```typescript
const api = new Api({
  host: "http://localhost:7654",
  tokenTransport: "cookie",  // Use cookies instead of header
});

// Login sets httpOnly cookie automatically
await api.auth.login("password", { email, password });

// Subsequent requests include cookie automatically
await api.data.readMany("posts");

// Logout clears cookie
await api.auth.logout();
```

**Cookie mode benefits:**

- HttpOnly cookies not accessible via JavaScript (XSS protection)
- Automatic renewal on requests (if configured)
- No manual token management

## Error Handling

### Error Codes

| Status | Meaning | Common Cause |
|--------|---------|--------------|
| 400 | Bad Request | Missing email/password |
| 401 | Unauthorized | Invalid credentials |
| 403 | Forbidden | Wrong strategy, disabled account |
| 409 | Conflict | Account uses different login method |

### Handling Specific Errors

```typescript
async function handleLogin(email: string, password: string) {
  const { ok, status, error } = await api.auth.login("password", {
    email,
    password,
  });

  if (ok) return;

  switch (status) {
    case 400:
      throw new Error("Please enter email and password");
    case 401:
      throw new Error("Invalid email or password");
    case 403:
      throw new Error("This account uses a different login method");
    case 409:
      throw new Error("Please use social login for this account");
    default:
      throw new Error(error?.message || "Login failed. Try again.");
  }
}
```

## Common Patterns

### Remember Me

Store token in localStorage (persistent) vs sessionStorage (per-session):

```typescript
// Remember me enabled
const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,  // Persists across browser sessions
});

// Remember me disabled
const api = new Api({
  host: "http://localhost:7654",
  storage: sessionStorage,  // Cleared when tab closes
});
```

### Auto-Refresh Token

If using short-lived tokens, refresh before expiry:

```typescript
async function withAuth<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (e) {
    // If 401, attempt refresh and retry
    if (e instanceof Error && e.message.includes("401")) {
      const { ok } = await api.auth.me();  // Refresh token
      if (ok) return await fn();
    }
    throw e;
  }
}
```

### Redirect After Login

```typescript
// Store intended destination
const redirectUrl = new URLSearchParams(window.location.search).get("redirect");

async function login(email: string, password: string) {
  await api.auth.login("password", { email, password });

  // Redirect to original destination or default
  window.location.href = redirectUrl || "/dashboard";
}
```

## Common Pitfalls

### Token Not Persisted

**Problem:** User logged out after page refresh

**Fix:** Provide storage option to API client:

```typescript
// Wrong - token lost on refresh
const api = new Api({ host: "http://localhost:7654" });

// Correct - token persisted
const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,
});
```

### CORS Errors

**Problem:** Login fails with CORS error

**Fix:** Configure CORS on backend or use same origin:

```typescript
// Backend config
{
  server: {
    cors: {
      origin: ["http://localhost:3000"],
      credentials: true,
    },
  },
}
```

### Cookie Not Set (HTTPS)

**Problem:** Cookie not received in browser

**Fix:** Disable `secure` for local development:

```typescript
// Backend config
{
  auth: {
    cookie: {
      secure: process.env.NODE_ENV === "production",
    },
  },
}
```

### Multiple Strategy Conflict

**Problem:** `User signed up with different strategy`

**Solution:** Users can only have one strategy. If they registered with OAuth, they cannot use password login. Check user's strategy first or guide to correct login method.

## Verification

Test login flow:

**1. Login and get token:**

```bash
curl -X POST http://localhost:7654/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

**2. Use token to access protected endpoint:**

```bash
curl http://localhost:7654/api/auth/me \
  -H "Authorization: Bearer <token>"
```

**3. Verify logout clears session:**

```bash
curl -X POST http://localhost:7654/api/auth/logout \
  -H "Authorization: Bearer <token>"

# Should now fail
curl http://localhost:7654/api/auth/me \
  -H "Authorization: Bearer <token>"
```

## DOs and DON'Ts

**DO:**

- Store tokens securely (localStorage or httpOnly cookie)
- Handle all error cases in login flow
- Show loading state during auth operations
- Redirect users after successful login
- Clear auth state fully on logout

**DON'T:**

- Store tokens in memory only (lost on refresh)
- Ignore error handling for login
- Expose tokens in URLs
- Forget to handle expired tokens
- Mix cookie and header auth without reason

## Related Skills

- **bknd-setup-auth** - Configure authentication system
- **bknd-registration** - Set up user registration
- **bknd-session-handling** - Manage user sessions
- **bknd-oauth-setup** - OAuth/social login providers
- **bknd-protect-endpoint** - Secure specific endpoints
