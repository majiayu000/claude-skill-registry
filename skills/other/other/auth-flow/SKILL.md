---
name: auth-flow
description: IntelliFill authentication flow patterns using Supabase Auth, JWT tokens, and backend auth mode
version: 1.0.0
author: IntelliFill Team
lastUpdated: 2025-12-12
---

# IntelliFill Authentication Flow Skill

This skill provides comprehensive guidance for working with authentication in the IntelliFill project, covering Supabase integration, JWT token handling, protected routes, and backend auth mode.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Backend Auth Routes](#backend-auth-routes)
4. [Frontend Auth Store](#frontend-auth-store)
5. [Protected Routes](#protected-routes)
6. [Token Management](#token-management)
7. [Password Reset Flow](#password-reset-flow)
8. [Backend Auth Mode](#backend-auth-mode)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)
11. [Troubleshooting](#troubleshooting)

---

## Overview

IntelliFill uses a **dual-auth architecture** that combines:
- **Supabase Auth** - Handles user authentication, password hashing, and session management
- **Prisma Database** - Stores user profiles, roles, and business logic
- **Backend API** - Centralized auth routing at `/api/auth/v2/*`
- **Frontend Store** - Zustand-based state management with persistence

### Key Features

- Server-side JWT verification using Supabase
- Automatic token refresh with retry logic
- Protected route components with loading states
- Backend auth mode (no direct Supabase dependency in frontend)
- Rate limiting on auth endpoints
- Account lockout after failed attempts
- Password reset with email verification

---

## Architecture

### Authentication Flow Diagram

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Frontend  │────────▶│   Backend   │────────▶│   Supabase   │
│  (React)    │  POST   │   (Express) │  Auth   │   Auth API   │
│             │  /login │             │  Verify │              │
└─────────────┘         └─────────────┘         └──────────────┘
       │                       │                        │
       │                       │                        │
       ▼                       ▼                        ▼
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Zustand   │         │   Prisma    │         │  Supabase    │
│   Store     │         │   Database  │         │  User Table  │
│ (Persisted) │         │ User Profile│         │  (Auth)      │
└─────────────┘         └─────────────┘         └──────────────┘
```

### Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **Auth Routes** | `quikadmin/src/api/supabase-auth.routes.ts` | Backend API endpoints |
| **Auth Middleware** | `quikadmin/src/middleware/supabaseAuth.ts` | JWT verification |
| **Auth Store** | `quikadmin-web/src/stores/backendAuthStore.ts` | Frontend state |
| **Auth Service** | `quikadmin-web/src/services/authService.ts` | API calls |
| **Protected Route** | `quikadmin-web/src/components/ProtectedRoute.tsx` | Route guard |
| **API Client** | `quikadmin-web/src/services/api.ts` | Axios with interceptors |

---

## Backend Auth Routes

### Available Endpoints

All auth routes are under `/api/auth/v2/*`:

```typescript
POST   /api/auth/v2/register          # Create new user account
POST   /api/auth/v2/login             # Authenticate user
POST   /api/auth/v2/logout            # Invalidate session
POST   /api/auth/v2/refresh           # Refresh access token
GET    /api/auth/v2/me                # Get current user profile
POST   /api/auth/v2/forgot-password   # Request password reset
POST   /api/auth/v2/verify-reset-token # Verify reset token
POST   /api/auth/v2/reset-password    # Reset password with token
POST   /api/auth/v2/change-password   # Change password (authenticated)
```

### Register Endpoint

**Request:**
```typescript
POST /api/auth/v2/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "fullName": "John Doe",
  "role": "user" // Optional: "user" | "admin"
}
```

**Response:**
```typescript
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user",
      "emailVerified": true // Auto-verified in dev mode
    },
    "tokens": {
      "accessToken": "eyJhbGc...",
      "refreshToken": "eyJhbGc...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    }
  }
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

**Rate Limiting:**
- Max 3 registrations per hour per IP
- Returns 429 if exceeded

### Login Endpoint

**Request:**
```typescript
POST /api/auth/v2/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```typescript
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user",
      "emailVerified": true,
      "lastLogin": "2025-12-12T10:00:00Z",
      "createdAt": "2025-12-01T10:00:00Z"
    },
    "tokens": {
      "accessToken": "eyJhbGc...",
      "refreshToken": "eyJhbGc...",
      "expiresIn": 3600,
      "tokenType": "Bearer"
    }
  }
}
```

**Error Codes:**
- `401` - Invalid credentials
- `403` - Account deactivated
- `429` - Rate limit exceeded (5 attempts per 15 minutes)

### Refresh Token Endpoint

**Request:**
```typescript
POST /api/auth/v2/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGc..."
}
```

**Response:**
```typescript
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "tokens": {
      "accessToken": "eyJhbGc...", // New access token
      "refreshToken": "eyJhbGc...", // New refresh token
      "expiresIn": 3600,
      "tokenType": "Bearer"
    }
  }
}
```

---

## Frontend Auth Store

### Store Structure

The auth store is located at `quikadmin-web/src/stores/backendAuthStore.ts`.

**State Interface:**
```typescript
interface AuthState {
  user: AuthUser | null;
  tokens: AuthTokens | null;
  company: { id: string } | null;
  isAuthenticated: boolean;
  isInitialized: boolean;
  isLoading: boolean;
  error: AppError | null;
  loginAttempts: number;
  isLocked: boolean;
  lockExpiry: number | null;
  lastActivity: number;
  rememberMe: boolean;
}
```

### Usage in Components

**Basic Usage:**
```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useBackendAuthStore();

  if (!isAuthenticated) {
    return <LoginForm onSubmit={login} />;
  }

  return (
    <div>
      <p>Welcome, {user?.firstName}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

**Selective State Subscription:**
```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function Header() {
  // Only re-renders when user changes
  const user = useBackendAuthStore(state => state.user);
  const logout = useBackendAuthStore(state => state.logout);

  return (
    <header>
      <span>{user?.email}</span>
      <button onClick={logout}>Logout</button>
    </header>
  );
}
```

### Auth Actions

**Login:**
```typescript
const login = useBackendAuthStore(state => state.login);

try {
  await login({
    email: 'user@example.com',
    password: 'SecurePass123',
    rememberMe: true
  });
  // User is now authenticated
} catch (error) {
  console.error('Login failed:', error.message);
}
```

**Register:**
```typescript
const register = useBackendAuthStore(state => state.register);

try {
  await register({
    email: 'user@example.com',
    password: 'SecurePass123',
    fullName: 'John Doe'
  });
  // User is registered and authenticated
} catch (error) {
  console.error('Registration failed:', error.message);
}
```

**Logout:**
```typescript
const logout = useBackendAuthStore(state => state.logout);

await logout();
// User is logged out, tokens cleared, redirected to login
```

**Check Session:**
```typescript
const checkSession = useBackendAuthStore(state => state.checkSession);

if (checkSession()) {
  // Session is valid
} else {
  // Session expired, redirect to login
}
```

### Error Handling

The store provides structured error handling:

```typescript
const { error, clearError } = useBackendAuthStore();

useEffect(() => {
  if (error) {
    toast.error(error.message);
    clearError();
  }
}, [error]);
```

**Error Structure:**
```typescript
interface AppError {
  id: string;
  code: string; // e.g., 'INVALID_CREDENTIALS', 'ACCOUNT_DEACTIVATED'
  message: string;
  details?: unknown;
  timestamp: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  component: string;
  resolved: boolean;
}
```

### Account Lockout

The store tracks failed login attempts:

```typescript
const { loginAttempts, isLocked, lockExpiry } = useBackendAuthStore();

if (isLocked) {
  const timeLeft = Math.ceil((lockExpiry! - Date.now()) / 1000 / 60);
  console.log(`Account locked for ${timeLeft} minutes`);
}

// After 5 failed attempts, account is locked for 15 minutes
```

---

## Protected Routes

### ProtectedRoute Component

Located at `quikadmin-web/src/components/ProtectedRoute.tsx`.

**Usage:**
```typescript
import { ProtectedRoute } from '@/components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected routes */}
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/documents" element={<DocumentLibrary />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
```

### How It Works

1. **Initialization Check:**
   - On mount, calls `initialize()` if not already initialized
   - Shows loading spinner during initialization

2. **Session Validation:**
   - Calls `checkSession()` to validate tokens
   - Checks token expiration synchronously

3. **Redirect Logic:**
   - If session invalid → redirect to `/login`
   - Preserves current location in state for return redirect

4. **Loading State:**
```typescript
if (!isInitialized || isLoading) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 className="h-8 w-8 animate-spin" />
      <p>Loading...</p>
    </div>
  );
}
```

### Return URL After Login

The ProtectedRoute preserves the original location:

```typescript
// In ProtectedRoute
<Navigate to="/login" state={{ from: location }} replace />

// In Login component
import { useLocation, useNavigate } from 'react-router-dom';

function Login() {
  const location = useLocation();
  const navigate = useNavigate();
  const login = useBackendAuthStore(state => state.login);

  async function handleLogin(credentials) {
    await login(credentials);
    const from = location.state?.from?.pathname || '/';
    navigate(from, { replace: true });
  }
}
```

---

## Token Management

### Automatic Token Refresh

The API client (`quikadmin-web/src/services/api.ts`) automatically refreshes tokens:

```typescript
// Axios response interceptor
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Shared refresh promise prevents multiple simultaneous refreshes
      if (!refreshPromise) {
        refreshPromise = refreshToken();
      }

      const newToken = await refreshPromise;

      if (newToken) {
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      }

      // Refresh failed, logout user
      await logout();
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);
```

### Token Storage

Tokens are persisted in localStorage:

```typescript
// In backendAuthStore.ts
persist(
  immer((set, get) => ({ /* store logic */ })),
  {
    name: 'intellifill-backend-auth',
    storage: createJSONStorage(() => localStorage),
    partialize: (state) => ({
      user: state.user,
      tokens: state.tokens,
      company: state.company,
      isAuthenticated: state.isAuthenticated,
      rememberMe: state.rememberMe,
      lastActivity: state.lastActivity,
    }),
    version: 1,
  }
)
```

### Token Expiration Handling

**Frontend:**
- Access token expires in 3600 seconds (1 hour)
- Refresh token used to get new access token
- If refresh fails, user is logged out

**Backend:**
- Uses Supabase `getUser()` for server-side validation
- Never uses `getSession()` (client-side only)

---

## Password Reset Flow

### Request Password Reset

**Frontend:**
```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function ForgotPassword() {
  const requestPasswordReset = useBackendAuthStore(
    state => state.requestPasswordReset
  );

  async function handleSubmit(email: string) {
    try {
      await requestPasswordReset(email);
      toast.success('Password reset email sent (if account exists)');
    } catch (error) {
      toast.error('Failed to send reset email');
    }
  }
}
```

**Backend Endpoint:**
```typescript
POST /api/auth/v2/forgot-password
Content-Type: application/json

{
  "email": "user@example.com",
  "redirectUrl": "https://app.example.com/reset-password" // Optional
}
```

**Response (Always Success):**
```typescript
{
  "success": true,
  "message": "If an account exists for this email, you will receive a password reset link shortly."
}
```

**Security Note:** Always returns success to prevent email enumeration.

### Verify Reset Token

**Frontend:**
```typescript
const verifyResetToken = useBackendAuthStore(
  state => state.verifyResetToken
);

useEffect(() => {
  const token = new URLSearchParams(location.search).get('token');
  if (token) {
    verifyResetToken(token)
      .then(() => setTokenValid(true))
      .catch(() => setTokenValid(false));
  }
}, []);
```

### Reset Password

**Frontend:**
```typescript
const resetPassword = useBackendAuthStore(state => state.resetPassword);

async function handleReset(token: string, newPassword: string) {
  try {
    await resetPassword(token, newPassword);
    toast.success('Password reset successfully. Please login.');
    navigate('/login');
  } catch (error) {
    toast.error('Failed to reset password');
  }
}
```

**Backend Endpoint:**
```typescript
POST /api/auth/v2/reset-password
Content-Type: application/json

{
  "token": "reset-token-from-email",
  "newPassword": "NewSecurePass123"
}
```

**Flow:**
1. User requests reset → email sent
2. User clicks link in email → redirected with token
3. Frontend verifies token validity
4. User enters new password
5. Backend updates password in Supabase
6. All sessions invalidated
7. User redirected to login

---

## Backend Auth Mode

### Configuration

Set in `quikadmin-web/.env`:

```env
# Enable backend auth mode (recommended for local dev)
VITE_USE_BACKEND_AUTH=true
VITE_API_URL=http://localhost:3002/api

# Supabase vars NOT required when using backend auth mode
# VITE_SUPABASE_URL=...
# VITE_SUPABASE_ANON_KEY=...
```

### Benefits

1. **No Supabase SDK in Frontend** - Smaller bundle size
2. **Centralized Auth** - All auth goes through backend API
3. **Simpler Configuration** - Only need backend API URL
4. **No CORS Issues** - Backend handles Supabase communication
5. **Better Security** - Supabase credentials not exposed to frontend

### How It Works

**Without Backend Auth Mode:**
```
Frontend ──▶ Supabase Auth API (direct)
Frontend ──▶ Backend API (for data)
```

**With Backend Auth Mode:**
```
Frontend ──▶ Backend API ──▶ Supabase Auth API
Frontend ──▶ Backend API ──▶ Database
```

### Implementation

**Unified Auth Export:**
```typescript
// quikadmin-web/src/stores/auth.ts
export { useBackendAuthStore as useAuthStore } from './backendAuthStore';
```

**All Components Use:**
```typescript
import { useAuthStore } from '@/stores/auth';
// Works with backend auth mode automatically
```

---

## Best Practices

### 1. Always Use Middleware for Protected Routes

**Backend:**
```typescript
import { authenticateSupabase } from '@/middleware/supabaseAuth';

router.get('/protected', authenticateSupabase, async (req, res) => {
  // req.user is available and verified
  const userId = req.user.id;
});
```

### 2. Validate User Status

**Backend Middleware:**
```typescript
// Check if account is active
if (!user.isActive) {
  return res.status(403).json({
    error: 'Account is deactivated',
    code: 'ACCOUNT_DEACTIVATED'
  });
}
```

### 3. Handle Token Refresh Gracefully

**Frontend:**
```typescript
// Use shared refresh promise to prevent stampede
let refreshPromise: Promise<string | null> | null = null;

if (!refreshPromise) {
  refreshPromise = refreshToken();
}

const newToken = await refreshPromise;
```

### 4. Implement Rate Limiting

**Backend:**
```typescript
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many authentication attempts'
});

router.post('/login', authLimiter, loginHandler);
```

### 5. Use Server-Side Token Verification

**Backend:**
```typescript
// ALWAYS use getUser() for server-side auth
const supabaseUser = await verifySupabaseToken(token);

// NEVER use getSession() (client-side only)
```

### 6. Clear Sessions on Password Change

**Backend:**
```typescript
// After password change, invalidate all sessions
await supabaseAdmin.auth.admin.signOut(userId, 'global');
```

### 7. Implement Account Lockout

**Frontend Store:**
```typescript
if (state.loginAttempts >= 5) {
  state.isLocked = true;
  state.lockExpiry = Date.now() + (15 * 60 * 1000); // 15 minutes
}
```

### 8. Persist Minimal State

**Store Configuration:**
```typescript
partialize: (state) => ({
  user: state.user,
  tokens: state.tokens,
  // Don't persist: error, isLoading, loginAttempts
})
```

---

## Common Patterns

### Login Form with Error Handling

```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function LoginForm() {
  const login = useBackendAuthStore(state => state.login);
  const error = useBackendAuthStore(state => state.error);
  const isLoading = useBackendAuthStore(state => state.isLoading);
  const clearError = useBackendAuthStore(state => state.clearError);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    clearError();

    try {
      await login({ email, password, rememberMe });
      // Redirect handled by ProtectedRoute
    } catch (err) {
      // Error is already in store
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error.message}</AlertDescription>
        </Alert>
      )}

      <Input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={isLoading}
      />

      <Input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        disabled={isLoading}
      />

      <Button type="submit" disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Login'}
      </Button>
    </form>
  );
}
```

### Role-Based Access Control

```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function AdminPanel() {
  const user = useBackendAuthStore(state => state.user);

  if (user?.role !== 'admin') {
    return <Navigate to="/" replace />;
  }

  return <div>Admin Panel</div>;
}
```

### Auth Status Indicator

```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function AuthStatus() {
  const { user, isAuthenticated, isLoading } = useBackendAuthStore();

  if (isLoading) {
    return <Skeleton className="h-8 w-32" />;
  }

  if (!isAuthenticated) {
    return <Link to="/login">Login</Link>;
  }

  return (
    <div>
      <Avatar>
        <AvatarFallback>
          {user?.firstName?.[0]}{user?.lastName?.[0]}
        </AvatarFallback>
      </Avatar>
      <span>{user?.email}</span>
    </div>
  );
}
```

### Session Timeout Warning

```typescript
import { useBackendAuthStore } from '@/stores/backendAuthStore';

function SessionTimeout() {
  const lastActivity = useBackendAuthStore(state => state.lastActivity);
  const logout = useBackendAuthStore(state => state.logout);

  useEffect(() => {
    const TIMEOUT = 30 * 60 * 1000; // 30 minutes

    const interval = setInterval(() => {
      if (Date.now() - lastActivity > TIMEOUT) {
        logout();
        toast.warning('Session expired due to inactivity');
      }
    }, 60 * 1000); // Check every minute

    return () => clearInterval(interval);
  }, [lastActivity, logout]);

  return null;
}
```

---

## Troubleshooting

### Issue: "Invalid or expired token"

**Cause:** Token expired and refresh failed

**Solution:**
```typescript
// Check token expiration
const tokens = useBackendAuthStore.getState().tokens;
if (tokens) {
  const expiresAt = Date.now() + (tokens.expiresIn * 1000);
  console.log('Token expires in:', expiresAt - Date.now(), 'ms');
}

// Force logout and re-login
const logout = useBackendAuthStore.getState().logout;
await logout();
```

### Issue: "Account is deactivated"

**Cause:** User account `isActive` is false in database

**Solution:**
```sql
-- Reactivate user in database
UPDATE "User" SET "isActive" = true WHERE email = 'user@example.com';
```

### Issue: Infinite redirect loop

**Cause:** ProtectedRoute redirects to login, login redirects to protected route

**Solution:**
```typescript
// In Login component, check if already authenticated
const isAuthenticated = useBackendAuthStore(state => state.isAuthenticated);

useEffect(() => {
  if (isAuthenticated) {
    navigate('/');
  }
}, [isAuthenticated]);
```

### Issue: Token refresh stampede

**Cause:** Multiple API calls trigger refresh simultaneously

**Solution:** Already implemented in `api.ts`:
```typescript
// Shared refresh promise
let refreshPromise: Promise<string | null> | null = null;

if (!refreshPromise) {
  refreshPromise = refreshToken();
}
```

### Issue: "User not found in database"

**Cause:** User exists in Supabase but not in Prisma

**Solution:**
```typescript
// Check Supabase user
const { data } = await supabaseAdmin.auth.admin.listUsers();
console.log('Supabase users:', data.users);

// Check Prisma user
const user = await prisma.user.findUnique({
  where: { id: 'supabase-user-id' }
});

// Create missing Prisma user
if (!user) {
  await prisma.user.create({
    data: {
      id: supabaseUser.id,
      email: supabaseUser.email,
      // ... other fields
    }
  });
}
```

### Issue: CORS errors

**Cause:** Frontend making direct Supabase calls

**Solution:** Enable backend auth mode:
```env
VITE_USE_BACKEND_AUTH=true
```

---

## Related Documentation

- **Backend Auth Routes:** `N:\IntelliFill\quikadmin\src\api\supabase-auth.routes.ts`
- **Backend Middleware:** `N:\IntelliFill\quikadmin\src\middleware\supabaseAuth.ts`
- **Frontend Store:** `N:\IntelliFill\quikadmin-web\src\stores\backendAuthStore.ts`
- **Frontend Service:** `N:\IntelliFill\quikadmin-web\src\services\authService.ts`
- **Protected Route:** `N:\IntelliFill\quikadmin-web\src\components\ProtectedRoute.tsx`
- **API Client:** `N:\IntelliFill\quikadmin-web\src\services\api.ts`
- **CLAUDE.local.md:** `N:\IntelliFill\CLAUDE.local.md`

---

**Last Updated:** 2025-12-12
**Maintained By:** IntelliFill Team
