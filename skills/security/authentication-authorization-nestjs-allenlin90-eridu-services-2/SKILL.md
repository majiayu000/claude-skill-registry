---
name: authentication-authorization-nestjs
description: Comprehensive authentication and authorization patterns for Eridu Services. This skill should be used when implementing login flows, protecting endpoints, enforcing permissions, or designing API security for both backend and frontend.
metadata:
  priority: 2
  applies_to: [backend, frontend, authentication, authorization]
  supersedes: [eridu-authentication-authorization, authentication-authorization-backend, authentication-authorization-frontend]
---

# Authentication & Authorization (Comprehensive)

Complete guide for authentication and authorization across Eridu Services monorepo (backend and frontend).

## Table of Contents

1. [General Principles](#general-principles)
2. [Authorization Levels](#authorization-levels)
3. [Backend Implementation](#backend-implementation)
4. [Frontend Implementation](#frontend-implementation)
5. [Common Mistakes](#common-mistakes)

---

## General Principles

### Always Protect Sensitive Operations

🔴 **Critical**: Require authentication for any operation that:
- Modifies user data
- Accesses user-specific resources
- Changes permissions or roles
- Accesses client/studio-specific data

**Examples**:
- ✅ Public: `/health`, `/api/reference`, login page
- ✅ Authenticated: `/me/*`, dashboard, user profile updates
- ✅ Authorized: `/admin/*`, moderation tools, financial reports

### Validate on Every Access

🔴 **Critical**: Don't trust client-sent identifiers

- Backend validates credentials/tokens on every request
- User ID comes from validated credentials, never from URL/body
- Permissions are fetched from authoritative source (database)
- Frontend checks auth status before rendering sensitive content

### Clear Error Messages (For Users)

**Authentication Failures** (401):
- User message: "Invalid credentials"
- Don't reveal: Whether username exists, password requirements

**Authorization Failures** (403):
- User message: "Access denied"
- Don't reveal: What resources exist, which permissions are missing

### Token Security Standards

🔴 **Critical Best Practices**:
- ✅ Use industry-standard formats (JWT with RS256/EdDSA)
- ✅ Include token expiration times
- ✅ Implement refresh mechanisms
- ✅ Validate signatures using public keys
- ✅ Use HTTPS/TLS for transmission
- ✅ Store securely (HTTP-only cookies preferred)
- ❌ Never log tokens
- ❌ Never expose in URLs
- ❌ Never hardcode secrets

---

## Authorization Levels

### Public Access (No Authentication)

**Use when**: Information is freely available to everyone
- Health checks
- API documentation
- Login/registration pages
- Public blog posts

### User Authentication (Logged In)

**Use when**: User must be logged in, but any logged-in user can access
- User profile (`/me`)
- Personal dashboard
- User-specific settings
- History/preferences

### Role-Based Authorization (Admin/Special Role)

**Use when**: Only specific roles can access
- Admin panels (`/admin/*`)
- Moderation tools
- Financial reports
- User management

### Resource-Level Authorization

**Use when**: User owns the resource or has explicit permission
- Edit own comments (not others')
- View client-specific data
- Manage team members
- Update project settings

---

## Backend Implementation

### Token Validation

🔴 **Critical**: Use `@eridu/auth-sdk` for JWT validation.

```typescript
import { JwtAuthGuard } from '@/lib/auth/jwt-auth.guard';
import { CurrentUser } from '@eridu/auth-sdk/adapters/nestjs/current-user.decorator';

@Controller('me/profile')
@UseGuards(JwtAuthGuard)
export class ProfileController {
  @Get()
  async getProfile(@CurrentUser() user: AuthenticatedUser) {
    // user.id is validated from JWT
    return this.userService.getUserById(user.id);
  }
}
```

### Role-Based Authorization

🟡 **Recommended**: Use guards for role enforcement.

```typescript
import { AdminGuard } from '@/lib/auth/admin.guard';

@Controller('admin/users')
@UseGuards(JwtAuthGuard, AdminGuard)
export class AdminUserController {
  // Only system admins can access
}
```

### Studio-Scoped Authorization

🔴 **Critical**: Use `@StudioProtected()` for studio-scoped resources.

```typescript
import { StudioProtected } from '@/lib/decorators/studio-protected.decorator';
import { STUDIO_ROLE } from '@eridu/api-types/memberships';

@Controller('studios/:studioId/tasks')
@StudioProtected([STUDIO_ROLE.ADMIN, STUDIO_ROLE.MEMBER])
export class StudioTaskController {
  // Only studio members can access
}
```

### Service-to-Service Authentication

🔴 **Critical**: Use API keys for service-to-service calls.

```typescript
import { ApiKeyGuard } from '@/lib/auth/api-key.guard';

@Controller('backdoor/users')
@UseGuards(ApiKeyGuard)
export class BackdoorUserController {
  // Only services with valid API key can access
}
```

---

## Frontend Implementation

### Token Storage

🔴 **Critical**: Store tokens securely.

**Preferred**: HTTP-only cookies (set by backend)
```typescript
// Backend sets cookie
res.cookie('access_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});
```

**Alternative**: localStorage (if cookies not feasible)
```typescript
// Only if HTTP-only cookies can't be used
localStorage.setItem('access_token', token);
```

### Protected Routes

🟡 **Recommended**: Protect routes requiring authentication.

```typescript
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return <>{children}</>;
}
```

### User Context

🟡 **Recommended**: Provide user context globally.

```typescript
import { createContext, useContext, useState, useEffect } from 'react';

interface AuthContext {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContext | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch current user on mount
    fetchCurrentUser().then(setUser).finally(() => setIsLoading(false));
  }, []);

  const login = async (credentials: Credentials) => {
    const user = await apiClient.login(credentials);
    setUser(user);
  };

  const logout = () => {
    apiClient.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

### Token Refresh

🟡 **Recommended**: Implement automatic token refresh.

```typescript
import axios from 'axios';

const apiClient = axios.create({ baseURL: '/api' });

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        // Attempt to refresh token
        await apiClient.post('/auth/refresh');
        // Retry original request
        return apiClient(error.config);
      } catch {
        // Refresh failed, redirect to login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

### API Interceptors

🟡 **Recommended**: Attach tokens to requests automatically.

```typescript
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

---

## Common Mistakes

### ❌ Mistake 1: Trusting user ID from request body

**Problem:**
```typescript
// ❌ Wrong: User ID from body
@Post('update-profile')
async updateProfile(@Body() body: { userId: string; name: string }) {
  return this.userService.updateUser(body.userId, { name: body.name });
}
```

**Why it's wrong:** Users can modify other users' profiles.

**✅ Correct Approach:**
```typescript
// ✅ Right: User ID from validated token
@Post('me/profile')
async updateProfile(
  @CurrentUser() user: AuthenticatedUser,
  @Body() body: { name: string }
) {
  return this.userService.updateUser(user.id, { name: body.name });
}
```

---

### ❌ Mistake 2: Storing tokens in localStorage without consideration

**Problem:**
```typescript
// ❌ Potentially risky: Vulnerable to XSS
localStorage.setItem('access_token', token);
```

**Why it's wrong:** XSS attacks can steal tokens from localStorage.

**✅ Correct Approach:**
```typescript
// ✅ Preferred: HTTP-only cookies (set by backend)
// Backend:
res.cookie('access_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});

// Frontend: Cookie sent automatically, no JS access
```

---

### ❌ Mistake 3: Not checking authorization on backend

**Problem:**
```typescript
// ❌ Wrong: Frontend-only protection
// Frontend protects route, but backend doesn't check
@Get('admin/users')
async listUsers() {
  return this.userService.listUsers();
}
```

**Why it's wrong:** Attackers can bypass frontend and call API directly.

**✅ Correct Approach:**
```typescript
// ✅ Right: Backend enforces authorization
@Get('admin/users')
@UseGuards(JwtAuthGuard, AdminGuard)
async listUsers() {
  return this.userService.listUsers();
}
```

---

### ❌ Mistake 4: Not handling token expiration

**Problem:**
```typescript
// ❌ Wrong: No token refresh logic
// User gets logged out abruptly when token expires
```

**Why it's wrong:** Poor user experience.

**✅ Correct Approach:**
```typescript
// ✅ Right: Implement token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await refreshToken();
      return apiClient(error.config);
    }
    return Promise.reject(error);
  }
);
```

---

### ❌ Mistake 5: Exposing sensitive information in error messages

**Problem:**
```typescript
// ❌ Wrong: Revealing user existence
throw new UnauthorizedException('User user@example.com not found');
```

**Why it's wrong:** Helps attackers enumerate valid users.

**✅ Correct Approach:**
```typescript
// ✅ Right: Generic error message
throw new UnauthorizedException('Invalid credentials');
```

---

## Best Practices Checklist

### Backend
- [ ] 🔴 **Critical**: Use `@eridu/auth-sdk` for JWT validation
- [ ] 🔴 **Critical**: Validate tokens on every protected endpoint
- [ ] 🔴 **Critical**: User ID from token, never from request body/params
- [ ] 🔴 **Critical**: Use guards for role-based authorization
- [ ] 🟡 **Recommended**: Use `@StudioProtected()` for studio-scoped resources
- [ ] 🟡 **Recommended**: Use API keys for service-to-service auth
- [ ] 🟡 **Recommended**: Log authentication failures for security monitoring
- [ ] Generic error messages (don't reveal user existence)

### Frontend
- [ ] 🔴 **Critical**: Store tokens securely (prefer HTTP-only cookies)
- [ ] 🔴 **Critical**: Protect sensitive routes with auth checks
- [ ] 🟡 **Recommended**: Provide global user context via React Context
- [ ] 🟡 **Recommended**: Implement automatic token refresh
- [ ] 🟡 **Recommended**: Use API interceptors to attach tokens
- [ ] 🟡 **Recommended**: Handle token expiration gracefully
- [ ] Redirect to login on 401 errors
- [ ] Clear user state on logout

---

## Related Skills

- **[Backend Controller Pattern NestJS](backend-controller-pattern-nestjs/SKILL.md)** - Controller patterns for protected endpoints
- **[Service Pattern NestJS](service-pattern-nestjs/SKILL.md)** - Services receive authenticated user context
- **[Data Validation](data-validation/SKILL.md)** - Input validation (complement to auth)
- **[Erify Authorization](erify-authorization/SKILL.md)** - Role-based authorization in erify_api
