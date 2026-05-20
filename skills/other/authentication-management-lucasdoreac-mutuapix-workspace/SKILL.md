---
name: Authentication Management
description: Manages authentication flow for MutuaPIX (Laravel Sanctum + Next.js), handles mock mode security, and validates environment configurations
version: 1.1.0
allowed-tools: [Read, Edit, Grep, Bash, mcp__chrome-devtools__*]
---

# Authentication Management Skill

## Overview

This skill manages the complete authentication system for MutuaPIX, covering:
- Production authentication flow (Laravel Sanctum + JWT)
- Development mock mode (for frontend testing without backend)
- Environment detection and security validation
- CSRF token handling
- Session management

## System Architecture

### Backend: Laravel Sanctum

**Authentication Flow:**
```
1. GET /sanctum/csrf-cookie → Receives XSRF-TOKEN cookie
2. POST /api/v1/login {email, password, X-XSRF-TOKEN header}
3. Backend validates credentials
4. Returns {token, user} (token expires in 24h)
5. All requests include: Authorization: Bearer {token}
```

**Configuration:**
- **Sanctum Expiration:** 1440 minutes (24 hours)
- **Stateful Domain:** `matrix.mutuapix.com`
- **Guard:** `web`
- **Rate Limiting:** 5 requests/minute on login

**Files:**
- `backend/routes/api/auth.php` - Authentication routes
- `backend/app/Http/Controllers/Auth/AuthController.php` - Login/logout logic
- `backend/config/sanctum.php` - Sanctum configuration
- `backend/config/cors.php` - CORS settings

### Frontend: Next.js + Zustand

**State Management:**
- **Store:** `frontend/src/stores/authStore.ts`
- **Persistence:** localStorage['auth-storage']
- **Token Injection:** Axios interceptor adds `Authorization: Bearer {token}`

**Files:**
- `frontend/src/stores/authStore.ts` - Authentication state
- `frontend/src/services/auth.service.ts` - API calls
- `frontend/src/hooks/useAuth.ts` - Authentication hook
- `frontend/src/providers/AuthProvider.tsx` - Auth context provider

## Critical Security Issue: Mock Mode

### Why Mock Mode Exists

**Purpose:** Allow frontend development without running backend API
**Problem:** Implementation has security vulnerabilities if not properly configured

### Mock Components

#### 1. Environment Detection (`src/lib/env.ts`)

```typescript
// ✅ CORRECT: Uses NEXT_PUBLIC_NODE_ENV for client-side detection
export const IS_PRODUCTION = process.env.NEXT_PUBLIC_NODE_ENV === 'production';
export const IS_DEVELOPMENT = !IS_PRODUCTION;
```

**⚠️ WHY THIS IS CRITICAL:**
- `process.env.NODE_ENV` is **undefined** in Next.js client-side code
- Only `NEXT_PUBLIC_*` variables are replaced at build time
- Previous code using `process.env.NODE_ENV` always evaluated to false (insecure!)

#### 2. authStore Default State (CRITICAL VULNERABILITY)

**File:** `frontend/src/stores/authStore.ts:91-96`

**❌ INSECURE (Current State):**
```typescript
user: devLocalUser,        // Mock admin user by default
token: devLocalToken,       // "local-dev-token"
isAuthenticated: true,      // Already authenticated!
```

**✅ SECURE (Required Fix):**
```typescript
user: null,                 // Unauthenticated by default
token: null,
isAuthenticated: false,
```

#### 3. MockLoginButton

**File:** `frontend/src/components/auth/MockLoginButton.tsx`

**Status:** ✅ Secured (renders `null` in production)

```typescript
if (IS_PRODUCTION) {
  return null;  // Button not rendered in production
}
```

## Environment Configuration

### Production VPS (138.199.162.115)

**File:** `/var/www/mutuapix-frontend-production/.env.production`

```bash
# ✅ CORRECT CONFIGURATION
NEXT_PUBLIC_NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.mutuapix.com
NEXT_PUBLIC_API_BASE_URL=https://api.mutuapix.com
NEXT_PUBLIC_USE_AUTH_MOCK=false
NEXT_PUBLIC_AUTH_DISABLED=false
NEXT_PUBLIC_DEBUG=false
```

**Critical:** Must run `npm run build` (NOT just PM2 restart) for changes to take effect!

### Local Development

**File:** `frontend/.env.local`

```bash
# ✅ RECOMMENDED CONFIGURATION
NEXT_PUBLIC_NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:8000    # Local backend!
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_USE_AUTH_MOCK=true              # Enable mock for dev
NEXT_PUBLIC_AUTH_DISABLED=false
NEXT_PUBLIC_DEBUG=true
```

**⚠️ NEVER point local environment to production API!**

## Deployment Checklist

When deploying authentication changes:

### Backend Deployment
- [ ] Verify Sanctum configuration hasn't changed
- [ ] Check CORS allows frontend domain
- [ ] Test CSRF token endpoint: `curl https://api.mutuapix.com/sanctum/csrf-cookie -I`
- [ ] Test login endpoint with invalid credentials (should return 401)
- [ ] Restart PM2: `ssh root@49.13.26.142 'pm2 restart mutuapix-api'`

### Frontend Deployment
- [ ] Verify `.env.production` exists on VPS with correct values
- [ ] Check `NEXT_PUBLIC_NODE_ENV=production` is set
- [ ] Check `NEXT_PUBLIC_USE_AUTH_MOCK=false` is set
- [ ] **CRITICAL:** Delete `.next` cache: `rm -rf .next`
- [ ] Run full build: `npm run build`
- [ ] Restart PM2: `pm2 restart mutuapix-frontend`
- [ ] Verify mock button NOT visible: Use MCP Chrome DevTools
- [ ] Verify console shows `IS_PRODUCTION: true`
- [ ] Test login flow with real credentials

### Post-Deployment Verification (MCP)

```typescript
// 1. Navigate to production login
await mcp__chrome-devtools__navigate_page({
  url: 'https://matrix.mutuapix.com/login'
});

// 2. Check console for mock mode messages
const console = await mcp__chrome-devtools__list_console_messages();
// Should NOT contain: "🔓 Acesso liberado no modo desenvolvimento"

// 3. Take snapshot to verify mock button not rendered
const snapshot = await mcp__chrome-devtools__take_snapshot();
// Should NOT contain: "Login de Desenvolvimento" button

// 4. Monitor network requests after login
const requests = await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ['xhr', 'fetch']
});
// Should call: https://api.mutuapix.com/api/v1/login
// Should NOT call: back-api-mutuapix.test (old dev URL)
```

## Common Issues & Solutions

### Issue 1: Mock Login Button Visible in Production

**Symptoms:**
- Button "🔓 Login de Desenvolvimento" appears on production login page
- Console shows development messages

**Diagnosis:**
```bash
# Check production environment file
ssh root@138.199.162.115 'cat /var/www/mutuapix-frontend-production/.env.production | grep NODE_ENV'
```

**Solution:**
1. Ensure `NEXT_PUBLIC_NODE_ENV=production` in `.env.production`
2. Delete cache: `ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && rm -rf .next'`
3. Rebuild: `ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && npm run build'`
4. Restart: `ssh root@138.199.162.115 'pm2 restart mutuapix-frontend'`

### Issue 2: API Calls Going to Wrong URL

**Symptoms:**
- Network tab shows requests to `back-api-mutuapix.test`
- CORS errors in console

**Diagnosis:**
```bash
# Check if environment variables were embedded in build
ssh root@138.199.162.115 'grep -r "back-api-mutuapix.test" /var/www/mutuapix-frontend-production/.next/static/chunks/ | head -5'
```

**Solution:**
1. Same as Issue 1 - rebuild with correct `.env.production`
2. Verify API URL in build: `grep -r "api.mutuapix.com" .next/static/chunks/ | head -1`

### Issue 3: Login Returns 401 Unauthorized

**Symptoms:**
- Valid credentials rejected
- Backend logs show "CSRF token mismatch"

**Diagnosis:**
```bash
# Test CSRF token endpoint
curl -I https://api.mutuapix.com/sanctum/csrf-cookie

# Check CORS headers
curl -I https://api.mutuapix.com/api/v1/login \
  -H "Origin: https://matrix.mutuapix.com"
```

**Solution:**
1. Verify `backend/config/sanctum.php` has `matrix.mutuapix.com` in stateful domains
2. Verify `backend/config/cors.php` allows frontend origin
3. Check cookies are being set with correct domain (`.mutuapix.com`)

### Issue 4: User Already Authenticated Without Login

**Symptoms:**
- Fresh browser session shows user as logged in
- Mock admin user appears automatically

**Diagnosis:**
```typescript
// Check authStore default state
// File: frontend/src/stores/authStore.ts:91-96
```

**Solution:**
1. Fix authStore default state to:
   ```typescript
   user: null,
   token: null,
   isAuthenticated: false,
   ```
2. Rebuild and deploy frontend

## Testing Procedures

### Manual Testing (Production)

1. **Clear State:**
   ```javascript
   // In browser console
   localStorage.clear();
   sessionStorage.clear();
   location.reload();
   ```

2. **Verify Unauthenticated:**
   - Should redirect to `/login`
   - Cannot access `/user/dashboard` or other protected routes

3. **Test Login:**
   - Enter valid credentials
   - Should see "Login realizado com sucesso" toast
   - Should redirect to dashboard
   - Token should be in `localStorage['auth-storage']`

4. **Test Protected Routes:**
   - Navigate to `/user/dashboard`
   - Should see user data (not mock data)
   - Network tab should show `Authorization: Bearer {token}` in headers

5. **Test Logout:**
   - Click logout
   - Should redirect to `/login`
   - `localStorage['auth-storage']` should be empty

### Automated Testing (MCP)

Use MCP Chrome DevTools for automated verification (see "Post-Deployment Verification" section above).

## Security Best Practices

1. **Never commit `.env` files** (except `.env.example`)
2. **Always verify environment before deployment**
3. **Use MCP Chrome DevTools** to inspect production behavior
4. **Test logout flow** to ensure tokens are invalidated
5. **Monitor failed login attempts** via backend logs
6. **Rotate Sanctum tokens** if compromise suspected

## Related Skills

- **PIX Validation Expert** - Handles PIX key email matching
- **Documentation Updater** - Keeps CLAUDE.md current with auth changes

## Version History

- **1.1.0** (2025-10-16): Added comprehensive security audit
  - Documented mock mode vulnerabilities
  - Added MCP verification procedures
  - Included deployment checklist
  - Added troubleshooting guide

- **1.0.0** (2025-10-10): Initial authentication skill
  - Basic login/logout flow
  - Sanctum integration
  - Environment detection
