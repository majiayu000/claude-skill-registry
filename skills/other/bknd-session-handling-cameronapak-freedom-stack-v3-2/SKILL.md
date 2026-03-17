---
name: bknd-session-handling
description: Use when managing user sessions in a Bknd application. Covers JWT token lifecycle, session persistence, automatic renewal, checking auth state, invalidating sessions, and handling expiration.
---

# Session Handling

Manage user sessions in Bknd: token persistence, session checking, auto-renewal, and invalidation.

## Prerequisites

- Bknd project with auth enabled (`bknd-setup-auth`)
- Auth strategy configured and working (`bknd-login-flow`)
- For SDK: `bknd` package installed
- For React: `@bknd/react` package installed

## When to Use UI Mode

- Viewing JWT configuration in admin panel
- Checking cookie settings
- Testing session expiration

**UI steps:** Admin Panel > Auth > Configuration > JWT/Cookie settings

## When to Use Code Mode

- Implementing session persistence in frontend
- Checking authentication state on page load
- Handling token expiration gracefully
- Implementing auto-refresh patterns
- Server-side session validation

## How Sessions Work in Bknd

Bknd uses **stateless JWT-based sessions**:

1. **Login** - Server creates signed JWT with user data, returns token
2. **Storage** - Token stored in cookie (automatic) or localStorage/header (manual)
3. **Requests** - Token sent with each request for authentication
4. **Validation** - Server validates signature and expiration
5. **Renewal** - Cookie can auto-renew; header tokens require manual refresh

**Key Concept:** No server-side session storage. Token itself is the session.

## Session Configuration

### JWT Settings

```typescript
import { defineConfig } from "bknd";

export default defineConfig({
  auth: {
    enabled: true,
    jwt: {
      secret: process.env.JWT_SECRET!,  // Required for production
      alg: "HS256",                       // Algorithm: HS256 | HS384 | HS512
      expires: 604800,                    // 7 days in seconds
      issuer: "my-app",                   // Token issuer claim
      fields: ["id", "email", "role"],    // User fields in token payload
    },
  },
});
```

**JWT options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `secret` | string | `""` | Signing secret (256-bit min for production) |
| `alg` | string | `"HS256"` | HMAC algorithm |
| `expires` | number | - | Token lifetime in seconds |
| `issuer` | string | - | Issuer claim (iss) |
| `fields` | string[] | `["id","email","role"]` | User fields encoded in token |

### Cookie Settings

```typescript
{
  auth: {
    cookie: {
      secure: process.env.NODE_ENV === "production",  // HTTPS only
      httpOnly: true,                                  // No JS access
      sameSite: "lax",                                 // CSRF protection
      expires: 604800,                                 // Match JWT expiry
      renew: true,                                     // Auto-extend on activity
      path: "/",                                       // Cookie scope
      pathSuccess: "/dashboard",                       // Redirect after login
      pathLoggedOut: "/login",                         // Redirect after logout
    },
  },
}
```

**Cookie options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `secure` | boolean | `true` | Require HTTPS |
| `httpOnly` | boolean | `true` | Block JavaScript access |
| `sameSite` | string | `"lax"` | `"strict"` \| `"lax"` \| `"none"` |
| `expires` | number | `604800` | Cookie lifetime (seconds) |
| `renew` | boolean | `true` | Auto-renew on requests |
| `pathSuccess` | string | `"/"` | Post-login redirect |
| `pathLoggedOut` | string | `"/"` | Post-logout redirect |

## SDK Approach

### Session Persistence with Storage

```typescript
import { Api } from "bknd";

// Persistent sessions (survives page refresh/browser restart)
const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,  // Token persisted
});

// Session-only (cleared when tab closes)
const api = new Api({
  host: "http://localhost:7654",
  storage: sessionStorage,  // Token cleared on tab close
});

// No persistence (token in memory only)
const api = new Api({
  host: "http://localhost:7654",
  // No storage = token lost on page refresh
});
```

### Check Session on App Start

```typescript
async function initializeAuth() {
  const api = new Api({
    host: "http://localhost:7654",
    storage: localStorage,
  });

  // Check if existing token is still valid
  const { ok, data } = await api.auth.me();

  if (ok && data?.user) {
    console.log("Session valid:", data.user.email);
    return { api, user: data.user };
  }

  console.log("No valid session");
  return { api, user: null };
}

// On app mount
const { api, user } = await initializeAuth();
```

### Session State Management

```typescript
import { Api } from "bknd";

class SessionManager {
  private api: Api;
  private user: User | null = null;
  private listeners: Set<(user: User | null) => void> = new Set();

  constructor(host: string) {
    this.api = new Api({ host, storage: localStorage });
  }

  // Initialize - call on app start
  async init() {
    const { ok, data } = await this.api.auth.me();
    this.user = ok ? data?.user ?? null : null;
    this.notifyListeners();
    return this.user;
  }

  // Get current session
  getUser() {
    return this.user;
  }

  isAuthenticated() {
    return this.user !== null;
  }

  // Login - creates new session
  async login(email: string, password: string) {
    const { ok, data, error } = await this.api.auth.login("password", {
      email,
      password,
    });

    if (!ok) throw new Error(error?.message || "Login failed");

    this.user = data!.user;
    this.notifyListeners();
    return this.user;
  }

  // Logout - destroys session
  async logout() {
    await this.api.auth.logout();
    this.user = null;
    this.notifyListeners();
  }

  // Refresh session (re-validate token)
  async refresh() {
    const { ok, data } = await this.api.auth.me();
    this.user = ok ? data?.user ?? null : null;
    this.notifyListeners();
    return this.user;
  }

  // Subscribe to session changes
  subscribe(callback: (user: User | null) => void) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  private notifyListeners() {
    this.listeners.forEach((cb) => cb(this.user));
  }
}

type User = { id: number; email: string; role?: string };

// Usage
const session = new SessionManager("http://localhost:7654");
await session.init();

session.subscribe((user) => {
  console.log("Session changed:", user?.email || "logged out");
});
```

### Cookie-Based Sessions (Automatic)

```typescript
const api = new Api({
  host: "http://localhost:7654",
  tokenTransport: "cookie",  // Use httpOnly cookies
});

// Login sets cookie automatically
await api.auth.login("password", { email, password });

// All requests include cookie automatically
await api.data.readMany("posts");

// Logout clears cookie
await api.auth.logout();
```

**Cookie mode advantages:**

- HttpOnly = XSS protection (JavaScript can't access token)
- Auto-renewal on every request (if `cookie.renew: true`)
- No manual token management
- Automatic CSRF protection with `sameSite`

### Header-Based Sessions (Manual)

```typescript
const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,
  tokenTransport: "header",  // Default
});

// Token stored in localStorage, sent via Authorization header
await api.auth.login("password", { email, password });

// Token automatically included:
// Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Handling Session Expiration

### Detect Expired Token

```typescript
async function makeAuthenticatedRequest<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    // Check if error is due to expired session
    if (isAuthError(error)) {
      // Session expired - redirect to login or refresh
      await handleExpiredSession();
    }
    throw error;
  }
}

function isAuthError(error: unknown): boolean {
  if (error instanceof Error) {
    return error.message.includes("401") || error.message.includes("Unauthorized");
  }
  return false;
}

async function handleExpiredSession() {
  // Option 1: Redirect to login
  window.location.href = "/login?expired=true";

  // Option 2: Show re-authentication modal
  // showReauthModal();

  // Option 3: Try to refresh (if using refresh tokens)
  // await refreshToken();
}
```

### Auto-Refresh Pattern

Since Bknd uses stateless JWT, there's no built-in refresh token. Instead, use `api.auth.me()` to re-validate and extend cookie-based sessions:

```typescript
class SessionWithAutoRefresh {
  private api: Api;
  private refreshInterval: number | null = null;

  constructor(host: string) {
    this.api = new Api({
      host,
      tokenTransport: "cookie",  // Cookie auto-renews on requests
    });
  }

  // Start periodic session check
  startAutoRefresh(intervalMs = 5 * 60 * 1000) {
    // Every 5 minutes
    this.refreshInterval = window.setInterval(async () => {
      const { ok } = await this.api.auth.me();
      if (!ok) {
        this.stopAutoRefresh();
        this.onSessionExpired();
      }
    }, intervalMs);
  }

  stopAutoRefresh() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
      this.refreshInterval = null;
    }
  }

  private onSessionExpired() {
    // Handle expired session
    window.location.href = "/login?session=expired";
  }
}
```

### Proactive Token Refresh

For header-based auth, re-login before token expires:

```typescript
import { jwtDecode } from "jwt-decode";  // npm install jwt-decode

class TokenManager {
  private api: Api;
  private refreshTimer: number | null = null;

  constructor(host: string) {
    this.api = new Api({ host, storage: localStorage });
  }

  // Schedule refresh before expiry
  scheduleRefresh(token: string) {
    const decoded = jwtDecode<{ exp: number }>(token);
    const expiresAt = decoded.exp * 1000;  // Convert to ms
    const refreshAt = expiresAt - 5 * 60 * 1000;  // 5 min before expiry
    const delay = refreshAt - Date.now();

    if (delay > 0) {
      this.refreshTimer = window.setTimeout(() => {
        this.promptRelogin();
      }, delay);
    }
  }

  private promptRelogin() {
    // Show modal asking user to re-authenticate
    // Or redirect to login with return URL
  }

  cleanup() {
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
    }
  }
}
```

## React Integration

### Session Provider

```tsx
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { Api } from "bknd";

type User = { id: number; email: string; role?: string };

type SessionContextType = {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  checkSession: () => Promise<User | null>;
  clearSession: () => void;
};

const SessionContext = createContext<SessionContextType | null>(null);

const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,
});

export function SessionProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check session on mount
  useEffect(() => {
    checkSession().finally(() => setIsLoading(false));
  }, []);

  async function checkSession() {
    const { ok, data } = await api.auth.me();
    const user = ok ? data?.user ?? null : null;
    setUser(user);
    return user;
  }

  function clearSession() {
    setUser(null);
    api.auth.logout();
  }

  return (
    <SessionContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: user !== null,
        checkSession,
        clearSession,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (!context) throw new Error("useSession must be used within SessionProvider");
  return context;
}
```

### Session-Aware Components

```tsx
import { useSession } from "./SessionProvider";

function Header() {
  const { user, isAuthenticated, clearSession } = useSession();

  if (!isAuthenticated) {
    return <a href="/login">Login</a>;
  }

  return (
    <div>
      <span>Welcome, {user!.email}</span>
      <button onClick={clearSession}>Logout</button>
    </div>
  );
}

function ProtectedPage() {
  const { isLoading, isAuthenticated } = useSession();

  if (isLoading) return <div>Checking session...</div>;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return <div>Protected content</div>;
}
```

### Session Expiration Handler

```tsx
import { useEffect } from "react";
import { useSession } from "./SessionProvider";

function SessionExpirationHandler() {
  const { checkSession, clearSession } = useSession();

  useEffect(() => {
    // Check session periodically
    const interval = setInterval(async () => {
      const user = await checkSession();
      if (!user) {
        // Session expired
        alert("Your session has expired. Please log in again.");
        clearSession();
        window.location.href = "/login";
      }
    }, 5 * 60 * 1000);  // Every 5 minutes

    // Check on window focus (user returns to tab)
    const handleFocus = () => checkSession();
    window.addEventListener("focus", handleFocus);

    return () => {
      clearInterval(interval);
      window.removeEventListener("focus", handleFocus);
    };
  }, [checkSession, clearSession]);

  return null;  // Invisible component
}

// Add to app root
function App() {
  return (
    <SessionProvider>
      <SessionExpirationHandler />
      <Routes />
    </SessionProvider>
  );
}
```

## Server-Side Session Validation

### Validate Session in API Routes

```typescript
import { getApi } from "bknd";

export async function GET(request: Request, app: BkndApp) {
  const api = getApi(app);
  const user = await api.auth.resolveAuthFromRequest(request);

  if (!user) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Session valid - user data available
  console.log("User ID:", user.id);
  console.log("Email:", user.email);
  console.log("Role:", user.role);

  return new Response(JSON.stringify({ user }));
}
```

### Server-Side Session Check (Next.js)

```typescript
// app/api/me/route.ts
import { getApp, getApi } from "bknd/adapter/nextjs";

export async function GET(request: Request) {
  const app = await getApp();
  const api = getApi(app);
  const user = await api.auth.resolveAuthFromRequest(request);

  if (!user) {
    return Response.json({ user: null }, { status: 401 });
  }

  return Response.json({ user });
}
```

## Common Patterns

### Remember Last Activity

```typescript
// Track user activity for session timeout warnings
let lastActivity = Date.now();

// Update on user interaction
document.addEventListener("click", () => (lastActivity = Date.now()));
document.addEventListener("keypress", () => (lastActivity = Date.now()));

// Check for inactivity
setInterval(() => {
  const inactiveMinutes = (Date.now() - lastActivity) / 1000 / 60;

  if (inactiveMinutes > 25) {
    // Warn user session will expire soon
    showSessionWarning();
  }

  if (inactiveMinutes > 30) {
    // Force logout
    api.auth.logout();
    window.location.href = "/login?reason=inactive";
  }
}, 60000);  // Check every minute
```

### Multi-Tab Session Sync

```typescript
// Sync session state across browser tabs
window.addEventListener("storage", async (event) => {
  if (event.key === "auth") {
    if (event.newValue === null) {
      // Logged out in another tab
      window.location.href = "/login";
    } else {
      // Logged in in another tab - refresh session
      await api.auth.me();
      window.location.reload();
    }
  }
});
```

### Secure Session Storage

```typescript
// For sensitive apps, use sessionStorage + warn on tab close
const api = new Api({
  host: "http://localhost:7654",
  storage: sessionStorage,
});

window.addEventListener("beforeunload", (e) => {
  if (api.auth.me()) {
    e.preventDefault();
    e.returnValue = "You will be logged out if you leave.";
  }
});
```

## Common Pitfalls

### Session Lost on Refresh

**Problem:** User logged out after page refresh

**Fix:** Provide storage adapter:

```typescript
// Wrong - no persistence
const api = new Api({ host: "http://localhost:7654" });

// Correct
const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,
});
```

### Cookie Not Working Locally

**Problem:** Cookie not set in development

**Fix:** Disable secure flag for localhost:

```typescript
{
  auth: {
    cookie: {
      secure: process.env.NODE_ENV === "production",  // false in dev
    },
  },
}
```

### Session Check Blocking UI

**Problem:** App shows blank while checking session

**Fix:** Show loading state:

```tsx
function App() {
  const { isLoading } = useSession();

  if (isLoading) {
    return <LoadingSpinner />;  // Don't leave blank
  }

  return <Routes />;
}
```

### Expired Token Still in Storage

**Problem:** Old token causes continuous 401 errors

**Fix:** Clear storage on auth failure:

```typescript
async function checkSession() {
  const { ok } = await api.auth.me();

  if (!ok) {
    // Clear stale token
    localStorage.removeItem("auth");
    return null;
  }

  return user;
}
```

## Verification

Test session handling:

**1. Session persists across refresh:**

```typescript
// Login
await api.auth.login("password", { email: "test@example.com", password: "pass" });

// Refresh page, then:
const { ok, data } = await api.auth.me();
console.log("Session persists:", ok && data?.user);  // Should be true
```

**2. Session expires correctly:**

```typescript
// Set short expiry in config (for testing)
jwt: { expires: 10 }  // 10 seconds

// Login, wait 15 seconds
await api.auth.login("password", { email, password });
await new Promise(r => setTimeout(r, 15000));

const { ok } = await api.auth.me();
console.log("Session expired:", !ok);  // Should be true
```

**3. Logout clears session:**

```typescript
await api.auth.logout();
const { ok } = await api.auth.me();
console.log("Session cleared:", !ok);  // Should be true
```

## DOs and DON'Ts

**DO:**

- Configure appropriate JWT expiry for your use case
- Use httpOnly cookies when possible (XSS protection)
- Check session validity on app initialization
- Handle session expiration gracefully with UI feedback
- Match cookie expiry with JWT expiry
- Use `secure: true` in production

**DON'T:**

- Store tokens in memory only (lost on refresh)
- Use long expiry times without renewal mechanism
- Ignore session expiration errors
- Mix cookie and header auth without clear reason
- Disable httpOnly unless absolutely necessary
- Forget to clear storage on logout

## Related Skills

- **bknd-setup-auth** - Configure authentication system
- **bknd-login-flow** - Login/logout functionality
- **bknd-oauth-setup** - OAuth/social login providers
- **bknd-protect-endpoint** - Secure specific endpoints
- **bknd-public-vs-auth** - Configure public vs authenticated access
