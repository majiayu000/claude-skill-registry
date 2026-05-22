---
name: dashboard-api-authentication
description: Proper authentication patterns for dashboard frontend API calls. Use when adding new API endpoints, creating components that fetch data, or debugging 401 Unauthorized errors. Covers JWT token handling, the apiRequest helper, and common pitfalls.
---

# Dashboard API Authentication

## Quick Reference

```typescript
// ALWAYS use api.ts functions for authenticated requests
import { getFeatureFlags, setFeatureFlagOverride } from '../api';

// NEVER use raw fetch for authenticated endpoints
// BAD: fetch('/api/feature-flags', { credentials: 'include' })
// GOOD: getFeatureFlags()
```

## The Golden Rule

**All authenticated API calls MUST use the `apiRequest` helper from `api.ts`** or one of the exported API functions that use it internally.

The dashboard uses JWT-based authentication. The token is stored in localStorage and sent via the `Authorization: Bearer <token>` header. Raw `fetch()` calls with `credentials: 'include'` will NOT include this header.

## Authentication Architecture

### Token Storage

```typescript
// Token is stored in multiple places for different purposes:
localStorage.setItem('dashboard_token', token); // Primary storage
setCookie('auth_token', token, 1); // For nginx auth (production)
```

### The apiRequest Helper

Located in `packages/dashboard-frontend/src/api.ts`:

```typescript
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken(); // Gets from localStorage or cookie

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    // THIS IS THE KEY - adds Authorization header
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  // Handles 401 by clearing token and reloading
  if (response.status === 401) {
    clearAuthToken();
    window.location.reload();
    throw new Error('Authentication expired');
  }

  // ... rest of response handling
}
```

## Common Patterns

### Adding a New API Function

```typescript
// In packages/dashboard-frontend/src/api.ts

// For GET requests
export async function getMyData(): Promise<MyDataResponse> {
  return apiRequest('/my-endpoint');
}

// For POST/PUT/DELETE requests
export async function updateMyData(id: string, data: UpdateInput): Promise<MyDataResponse> {
  return apiRequest(`/my-endpoint/${encodeURIComponent(id)}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}
```

### Using API Functions in Components

```typescript
// In a component or hook
import { getMyData, updateMyData } from '../api';

// In useEffect or event handler
const loadData = async () => {
  try {
    const data = await getMyData(); // Automatically authenticated
    setData(data);
  } catch (error) {
    // Handle error - may be auth error, network error, etc.
  }
};
```

### Using API Functions in Custom Hooks

```typescript
// In packages/dashboard-frontend/src/hooks/useMyFeature.ts
import { useCallback, useEffect, useState } from 'react';
import { getMyData, type MyDataResponse } from '../api';

export function useMyFeature() {
  const [data, setData] = useState<MyDataResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const result = await getMyData(); // Uses apiRequest internally
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return { data, loading, error, refresh: loadData };
}
```

## Common Mistakes

### Mistake 1: Using Raw Fetch

```typescript
// BAD - Will get 401 Unauthorized
const response = await fetch('/api/feature-flags', {
  credentials: 'include', // This sends cookies, NOT the JWT header
});

// GOOD - Uses apiRequest which adds Authorization header
import { getFeatureFlags } from '../api';
const data = await getFeatureFlags();
```

### Mistake 2: Forgetting to Export from api.ts

If you add a new endpoint, you must:

1. Add the function to `api.ts`
2. Export it
3. Import it where needed

```typescript
// In api.ts - add AND export
export async function getNewEndpoint(): Promise<Response> {
  return apiRequest('/new-endpoint');
}

// In component - import from api.ts
import { getNewEndpoint } from '../api';
```

### Mistake 3: Not Handling 401 in Custom Fetch

If you absolutely must use raw fetch (rare), handle 401:

```typescript
// Only if apiRequest can't be used (e.g., file uploads with progress)
const response = await fetch(url, {
  headers: {
    Authorization: `Bearer ${getAuthToken()}`,
  },
});

if (response.status === 401) {
  clearAuthToken();
  window.location.reload();
  throw new Error('Authentication expired');
}
```

## Debugging 401 Errors

### Symptoms

- API calls return 401 Unauthorized
- Server logs show "No authorization header"
- Feature works initially but fails after page components load

### Diagnostic Steps

1. **Check if using apiRequest**:

   ```bash
   grep -r "fetch('/api" packages/dashboard-frontend/src/
   ```

   Any raw fetch to `/api/*` is suspicious.

2. **Check Network tab**:
   - Look for `Authorization` header in request
   - If missing, the call isn't using apiRequest

3. **Verify token exists**:
   ```javascript
   // In browser console
   localStorage.getItem('dashboard_token');
   ```

### Fix Pattern

Replace raw fetch with api.ts function:

```typescript
// Before (broken)
const response = await fetch(`/api/feature-flags/${id}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({ enabled }),
});

// After (working)
import { setFeatureFlagOverride } from '../api';
await setFeatureFlagOverride(id, enabled);
```

## Server-Side Authentication

The server expects JWT in the Authorization header:

```typescript
// In packages/dashboard/src/auth.ts
authMiddleware = async (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    res.status(401).json({ error: 'No authorization header' });
    return;
  }

  const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : authHeader;

  const payload = this.verifyToken(token);
  // ... rest of verification
};
```

## Checklist for New API Endpoints

When adding a new authenticated endpoint:

- [ ] Create the route in `packages/dashboard/src/server/routes/`
- [ ] Apply `requireAuth` middleware to the route
- [ ] Add API function in `packages/dashboard-frontend/src/api.ts`
- [ ] Export the function from `api.ts`
- [ ] Use the exported function in components/hooks (never raw fetch)
- [ ] Test that 401 is properly handled if token expires

## Testing Authentication

To verify authentication is working:

```typescript
// In a test or console
import { getAuthToken } from '../api';

// Check token exists
const token = getAuthToken();
console.log('Token present:', !!token);

// Make authenticated request
try {
  const data = await getFeatureFlags();
  console.log('Auth working:', data);
} catch (e) {
  console.error('Auth failed:', e);
}
```
