---
name: oneauth-oauth2
description: Integrate client applications with OneAuth for OAuth2/OIDC authentication. Use when implementing user login/logout, token management, or identity integration via OneAuth (based on Ory Kratos + Ory Hydra). Covers Web OAuth2 Authorization Code + PKCE flow, token refresh/verify/revoke, UI customization, and multi-platform support (Web, mini-program, CLI). Trigger when user mentions OneAuth login, OAuth2 integration, SSO, or authentication with OneAuth.
---

# OneAuth OAuth2 Integration

OneAuth is an identity authentication system based on Ory Kratos and Ory Hydra, providing OAuth2/OIDC standard authentication.

## Architecture

```
Client App → OneAuth Proxy (Gateway) → Hydra (OAuth2) → OneAuth Login UI → Kratos (Identity)
                                      ↓
                                   Kratos (Identity)
```

- **OneAuth Proxy**: Unified entry point for all authentication services (OAuth2, OIDC, Identity)
- **Kratos**: Identity management (internal, accessed via proxy)
- **Hydra**: OAuth2/OIDC server (internal, accessed via proxy)
- **OneAuth UI**: Frontend login/register pages

## Service Endpoints

| Service | Port | Description |
|---------|------|-------------|
| OneAuth Proxy | `:8080` (Default) | **Unified Entry Point** for API, OAuth2, and Identity |
| OneAuth Web | `:8081` | Frontend static resources (Login UI) |
| Hydra/Kratos | Internal Only | Not exposed directly |

## OIDC Discovery

```
GET {ONEAUTH_PROXY_URL}/.well-known/openid-configuration
```

Standard OIDC libraries can auto-configure from this endpoint.

## Web OAuth2 Login Flow (Authorization Code + PKCE)

### Step 1: Generate PKCE parameters and redirect

```javascript
const codeVerifier = generateRandomString(64);
const codeChallenge = await sha256Base64Url(codeVerifier);
const state = generateRandomString(32);

sessionStorage.setItem('oauth_code_verifier', codeVerifier);
sessionStorage.setItem('oauth_state', state);

const params = new URLSearchParams({
  client_id: 'your-client-id',
  redirect_uri: 'http://your-app.com/callback',
  response_type: 'code',
  scope: 'openid profile email offline',
  state: state,
  code_challenge: codeChallenge,
  code_challenge_method: 'S256'
});

// Redirect to OneAuth Proxy instead of direct Hydra URL
window.location.href = `${ONEAUTH_PROXY_URL}/oauth2/auth?${params}`;
```

### Step 2: Hydra redirects to OneAuth login page

```
{ONEAUTH_WEB_URL}/login?login_challenge=abc123...
```

User completes login (password/SMS/email/social) on OneAuth UI.

### Step 3: OneAuth accepts login challenge and consent

OneAuth frontend automatically calls:
- `PUT /api/hydra/login/accept` (with Kratos session cookie)
- Hydra auto-skips consent (if `skip_consent: true`)

### Step 4: Handle callback with authorization code

```javascript
// On your /callback page
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
const state = urlParams.get('state');

// Verify state
if (state !== sessionStorage.getItem('oauth_state')) throw new Error('Invalid state');

const codeVerifier = sessionStorage.getItem('oauth_code_verifier');
```

### Step 5: Exchange code for tokens

**Option A: Via OneAuth proxy (recommended)**

```
POST {ONEAUTH_API_URL}/api/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code={code}&
redirect_uri={redirect_uri}&
client_id={client_id}&
code_verifier={code_verifier}
```

**Option B: Via backend API**

Frontend sends code + code_verifier to your backend, backend exchanges with Hydra.

**Token response**:
```json
{
  "access_token": "ory_at_...",
  "refresh_token": "ory_rt_...",
  "id_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3599,
  "scope": "openid profile email offline"
}
```

### Step 6: Store tokens and redirect

```javascript
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('refresh_token', data.refresh_token);
sessionStorage.removeItem('oauth_code_verifier');
sessionStorage.removeItem('oauth_state');
```

## Silent Token Exchange (Alternative)

Skip the redirect-based callback with `POST /api/oauth/web/exchange`:

```json
POST {ONEAUTH_API_URL}/api/oauth/web/exchange
Cookie: ory_kratos_session=...

{
  "client_id": "your-client-id",
  "redirect_uri": "http://your-app.com/callback",
  "scope": "openid profile email offline",
  "code_verifier": "your-pkce-verifier"
}
```

Returns tokens directly. Requires same-origin Kratos session cookie.

## Token Management

### Refresh Token

```
POST {ONEAUTH_API_URL}/api/oauth/refresh
{ "refresh_token": "ory_rt_..." }
```

### Verify Token

```
POST {ONEAUTH_API_URL}/oauth/token/verify
{ "token": "ory_at_..." }
```

Returns `{ "active": true, "sub": "...", "exp": ..., ... }`.

### Logout (Two-Step, Recommended)

```javascript
async function logout() {
  // 1. Revoke OAuth2 tokens
  await fetch(`${ONEAUTH_API_URL}/api/oauth/logout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      access_token: localStorage.getItem('access_token'),
      refresh_token: localStorage.getItem('refresh_token')
    })
  });

  // 2. Clear local storage
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');

  // 3. Redirect to revoke Kratos session
  window.location.href = `${ONEAUTH_API_URL}/api/auth/logout?post_logout_redirect_uri=${encodeURIComponent(window.location.origin)}`;
}
```

## Using Standard OIDC Libraries

```javascript
import { UserManager } from 'oidc-client-ts';

const settings = {
  authority: ONEAUTH_API_URL,          // e.g. 'https://auth.example.com'
  client_id: 'your-client-id',
  redirect_uri: 'http://your-app.com/callback',
  response_type: 'code',
  scope: 'openid profile email offline',
};

const userManager = new UserManager(settings);
```

## Login/Register UI Customization

### Login page parameters

```
{ONEAUTH_WEB_URL}/login?
  login_challenge={challenge}&        // OAuth2 flow (required for OAuth2)
  return_to={url}&                    // Post-login redirect (non-OAuth2)
  login_methods=password,phone,email& // Enabled methods
  enable_social=true&                 // Show social login buttons
  default_method=password&            // Default selected tab
  mode=normal                         // normal | popup
```

### Register page parameters

```
{ONEAUTH_WEB_URL}/register?
  return_to={url}&
  verify_method=email&          // email | phone | both
  confirm_password=true&
  require_username=false&
  require_name=false&
  email={prefill}&
  phone={prefill}
```

Parameters auto-transfer between login and register pages.

### return_to vs redirect_uri

- **`redirect_uri`**: OAuth2 standard callback URL for receiving authorization code
- **`return_to`**: OneAuth custom param for post-login redirect (non-OAuth2 or after OAuth2 completes)

## PKCE Helper

```javascript
function generateCodeVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64URLEncode(array);
}

async function generateCodeChallenge(verifier) {
  const data = new TextEncoder().encode(verifier);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return base64URLEncode(new Uint8Array(hash));
}

function base64URLEncode(buffer) {
  return btoa(String.fromCharCode(...buffer))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
```

## Hydra Client Registration

Register a new OAuth2 client for your app:

```bash
hydra create client \
  --id your-app-id \
  --name "Your App" \
  --grant-type authorization_code,refresh_token \
  --response-type code \
  --scope openid,profile,email,offline \
  --redirect-uri http://your-app.com/callback \
  --token-endpoint-auth-method none \
  --skip-consent
```

## CLI Login

For headless/CLI tools, use the native CLI endpoint:

```
POST {ONEAUTH_API_URL}/oauth/native/cli
{
  "client_id": "cli-tool",
  "username": "user@example.com",
  "password": "password",
  "code_verifier": "pkce-verifier",
  "scope": "openid profile offline"
}
```

## Error Handling

| HTTP Status | Error Code Range | Description |
|-------------|-----------------|-------------|
| 400 | 4001-4999 | Client request error |
| 401 | 2001-2999 | Authentication failed |
| 403 | 3001-3999 | Permission denied |
| 429 | - | Rate limited |
| 500 | 5001-5999 | Server error |

## Security Checklist

- Always use PKCE for authorization code flow
- Use HTTPS in production
- Store tokens securely (prefer httpOnly cookies over localStorage)
- Implement automatic token refresh (refresh 1 min before expiry)
- Revoke all tokens on logout
- Validate `state` parameter to prevent CSRF
- Never expose tokens in URLs or logs
