---
name: bknd-oauth-setup
description: Use when configuring OAuth or social login providers in a Bknd application. Covers Google OAuth, GitHub OAuth, custom OAuth providers, callback URLs, environment variables, and frontend OAuth integration.
---

# OAuth/Social Login Setup

Configure OAuth authentication providers (Google, GitHub, or custom) in Bknd.

## Prerequisites

- Bknd project with auth enabled (`bknd-setup-auth`)
- OAuth app credentials from provider (client_id, client_secret)
- For Google: Google Cloud Console project with OAuth 2.0 credentials
- For GitHub: GitHub OAuth App in Developer Settings
- For custom: Provider's authorization server endpoints

## When to Use UI Mode

- Testing OAuth login flow via admin panel
- Viewing enabled OAuth strategies
- Checking callback URL configuration

**UI steps:** Admin Panel > Auth > Strategies

## When to Use Code Mode

- Configuring OAuth providers in `bknd.config.ts`
- Setting up multiple OAuth providers
- Implementing frontend OAuth buttons
- Configuring custom OAuth providers (Slack, Discord, etc.)

## Built-in OAuth Providers

Bknd has pre-configured support for:

| Provider | Type | Scopes |
|----------|------|--------|
| `google` | OIDC | openid, email, profile |
| `github` | OAuth2 | read:user, user:email |

## Google OAuth Setup

### 1. Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project or select existing
3. Navigate: **APIs & Services > Credentials**
4. Click **Create Credentials > OAuth client ID**
5. Application type: **Web application**
6. Add authorized redirect URI:
   ```
   http://localhost:7654/api/auth/google/callback
   ```
   (Replace with your production URL)
7. Copy **Client ID** and **Client Secret**

### 2. Configure Bknd

```typescript
// bknd.config.ts
import { defineConfig } from "bknd";

export default defineConfig({
  auth: {
    enabled: true,
    jwt: {
      secret: process.env.JWT_SECRET!,
      expires: 604800,
    },
    strategies: {
      google: {
        type: "oauth",
        enabled: true,
        config: {
          name: "google",
          client: {
            client_id: process.env.GOOGLE_CLIENT_ID!,
            client_secret: process.env.GOOGLE_CLIENT_SECRET!,
          },
        },
      },
    },
  },
});
```

### 3. Environment Variables

```bash
# .env
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
JWT_SECRET=your-256-bit-secret
```

## GitHub OAuth Setup

### 1. Create GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Fill in:
   - **Application name**: Your app name
   - **Homepage URL**: `http://localhost:7654`
   - **Authorization callback URL**: `http://localhost:7654/api/auth/github/callback`
4. Click **Register application**
5. Copy **Client ID** and generate **Client Secret**

### 2. Configure Bknd

```typescript
// bknd.config.ts
import { defineConfig } from "bknd";

export default defineConfig({
  auth: {
    enabled: true,
    jwt: {
      secret: process.env.JWT_SECRET!,
      expires: 604800,
    },
    strategies: {
      github: {
        type: "oauth",
        enabled: true,
        config: {
          name: "github",
          client: {
            client_id: process.env.GITHUB_CLIENT_ID!,
            client_secret: process.env.GITHUB_CLIENT_SECRET!,
          },
        },
      },
    },
  },
});
```

### 3. Environment Variables

```bash
# .env
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
JWT_SECRET=your-256-bit-secret
```

## Multiple OAuth Providers

Enable multiple providers simultaneously:

```typescript
// bknd.config.ts
import { defineConfig } from "bknd";

export default defineConfig({
  auth: {
    enabled: true,
    jwt: {
      secret: process.env.JWT_SECRET!,
      expires: 604800,
    },
    strategies: {
      password: {
        type: "password",
        enabled: true,
        config: {
          hashing: "bcrypt",
          rounds: 4,
        },
      },
      google: {
        type: "oauth",
        enabled: true,
        config: {
          name: "google",
          client: {
            client_id: process.env.GOOGLE_CLIENT_ID!,
            client_secret: process.env.GOOGLE_CLIENT_SECRET!,
          },
        },
      },
      github: {
        type: "oauth",
        enabled: true,
        config: {
          name: "github",
          client: {
            client_id: process.env.GITHUB_CLIENT_ID!,
            client_secret: process.env.GITHUB_CLIENT_SECRET!,
          },
        },
      },
    },
  },
});
```

## Custom OAuth Provider

For providers not built-in (Slack, Discord, Microsoft, etc.):

```typescript
// bknd.config.ts
import { defineConfig } from "bknd";

export default defineConfig({
  auth: {
    enabled: true,
    strategies: {
      slack: {
        type: "custom_oauth",
        enabled: true,
        config: {
          name: "slack",
          type: "oauth2",  // "oauth2" or "oidc"
          client: {
            client_id: process.env.SLACK_CLIENT_ID!,
            client_secret: process.env.SLACK_CLIENT_SECRET!,
            token_endpoint_auth_method: "client_secret_basic",
          },
          as: {
            issuer: "https://slack.com",
            authorization_endpoint: "https://slack.com/oauth/v2/authorize",
            token_endpoint: "https://slack.com/api/oauth.v2.access",
            userinfo_endpoint: "https://slack.com/api/users.identity",
            scopes_supported: ["openid", "profile", "email"],
          },
        },
      },
    },
  },
});
```

**Custom OAuth config options:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Strategy identifier |
| `type` | `"oauth2"` \| `"oidc"` | Yes | Protocol type |
| `client.client_id` | string | Yes | OAuth client ID |
| `client.client_secret` | string | Yes | OAuth client secret |
| `client.token_endpoint_auth_method` | string | Yes | Auth method (`client_secret_basic`) |
| `as.issuer` | string | Yes | Authorization server issuer URL |
| `as.authorization_endpoint` | string | Yes | OAuth authorize URL |
| `as.token_endpoint` | string | Yes | Token exchange URL |
| `as.userinfo_endpoint` | string | No | User info URL |
| `as.scopes_supported` | string[] | No | Available scopes |

## OAuth Endpoints

Once configured, Bknd exposes these endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/{provider}/login` | Start OAuth login (cookie mode) |
| POST | `/api/auth/{provider}/register` | Start OAuth registration (cookie mode) |
| GET | `/api/auth/{provider}/login` | Get OAuth URL (token mode) |
| GET | `/api/auth/{provider}/callback` | OAuth callback handler |

## Frontend Integration

### Cookie-Based Flow (Recommended for SSR)

```typescript
// Redirect user to OAuth provider
function loginWithGoogle() {
  // POST redirects to Google, callback sets cookie, redirects to pathSuccess
  const form = document.createElement("form");
  form.method = "POST";
  form.action = "http://localhost:7654/api/auth/google/login";
  document.body.appendChild(form);
  form.submit();
}
```

### Token-Based Flow (SPA)

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "http://localhost:7654",
  storage: localStorage,
});

async function loginWithGoogle() {
  // Get OAuth URL
  const { data } = await api.auth.login("google");

  if (data?.url) {
    // Store challenge for callback verification
    sessionStorage.setItem("oauth_challenge", data.challenge);

    // Redirect to Google
    window.location.href = data.url;
  }
}

// On callback page, complete the flow
async function handleOAuthCallback() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");
  const challenge = sessionStorage.getItem("oauth_challenge");

  if (code && challenge) {
    // Complete OAuth flow
    const response = await fetch(
      `http://localhost:7654/api/auth/google/callback?code=${code}`,
      {
        headers: {
          "X-State-Challenge": challenge,
          "X-State-Action": "login",
        },
      }
    );

    const { user, token } = await response.json();
    api.setToken(token);
    sessionStorage.removeItem("oauth_challenge");
  }
}
```

### React OAuth Buttons

```tsx
import { useAuth } from "@bknd/react";

function OAuthButtons() {
  const { login } = useAuth();

  async function handleGoogleLogin() {
    const result = await login("google");
    if (result.data?.url) {
      window.location.href = result.data.url;
    }
  }

  async function handleGitHubLogin() {
    const result = await login("github");
    if (result.data?.url) {
      window.location.href = result.data.url;
    }
  }

  return (
    <div>
      <button onClick={handleGoogleLogin}>
        Continue with Google
      </button>
      <button onClick={handleGitHubLogin}>
        Continue with GitHub
      </button>
    </div>
  );
}
```

### OAuth Callback Page (React)

```tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Api } from "bknd";

const api = new Api({
  host: import.meta.env.VITE_API_URL,
  storage: localStorage,
});

function OAuthCallback() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const challenge = sessionStorage.getItem("oauth_challenge");

    if (!code) {
      setError("No authorization code received");
      return;
    }

    if (!challenge) {
      setError("OAuth session expired. Please try again.");
      return;
    }

    fetch(`${import.meta.env.VITE_API_URL}/api/auth/google/callback?code=${code}`, {
      headers: {
        "X-State-Challenge": challenge,
        "X-State-Action": "login",
      },
    })
      .then((res) => res.json())
      .then(({ user, token }) => {
        api.setToken(token);
        sessionStorage.removeItem("oauth_challenge");
        navigate("/dashboard");
      })
      .catch((err) => {
        setError("Authentication failed. Please try again.");
      });
  }, [navigate]);

  if (error) {
    return (
      <div>
        <p>{error}</p>
        <a href="/login">Back to login</a>
      </div>
    );
  }

  return <div>Completing sign in...</div>;
}
```

## Callback URL Configuration

**Development:**
```
http://localhost:7654/api/auth/{provider}/callback
```

**Production:**
```
https://api.yourapp.com/api/auth/{provider}/callback
```

Update redirect URIs in provider dashboard when deploying.

## Cookie Settings for OAuth

Configure cookie behavior for OAuth flow:

```typescript
{
  auth: {
    cookie: {
      secure: process.env.NODE_ENV === "production",  // HTTPS only in prod
      httpOnly: true,
      sameSite: "lax",  // Required for OAuth redirects
      pathSuccess: "/dashboard",  // Redirect after login
      pathLoggedOut: "/login",    // Redirect after logout
    },
  },
}
```

## Common Pitfalls

### Callback URL Mismatch

**Problem:** `redirect_uri_mismatch` error from provider

**Fix:** Ensure callback URL exactly matches provider dashboard:

```
# Provider dashboard (Google/GitHub)
http://localhost:7654/api/auth/google/callback

# Must match Bknd host configuration
host: "http://localhost:7654"
```

### Missing Environment Variables

**Problem:** OAuth login fails silently

**Fix:** Verify all required env vars are set:

```bash
# Required for Google OAuth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# Required for GitHub OAuth
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# Always required
JWT_SECRET=...
```

### CORS Issues (SPA)

**Problem:** CORS error when calling OAuth endpoints

**Fix:** Configure CORS on backend:

```typescript
{
  server: {
    cors: {
      origin: ["http://localhost:3000"],  // Your frontend URL
      credentials: true,
    },
  },
}
```

### Strategy Conflict

**Problem:** "User signed up with different strategy"

**Cause:** User has existing account with different auth method

**Solution:** Users can only have ONE strategy. Guide them to use their original login method or implement account linking (requires custom code).

### OAuth Cookie Not Set

**Problem:** Cookie not received after OAuth callback

**Fix:** Ensure secure cookie settings:

```typescript
{
  auth: {
    cookie: {
      secure: false,  // Set false for localhost (no HTTPS)
      sameSite: "lax",  // Required for OAuth redirects
    },
  },
}
```

### Invalid Scopes

**Problem:** Provider rejects scope request

**Fix:** Use only scopes from `scopes_supported`:

```typescript
// Google OIDC defaults
scopes_supported: ["openid", "email", "profile"]

// GitHub OAuth2 defaults
scopes_supported: ["read:user", "user:email"]
```

## Verification

Test OAuth setup:

**1. Check available strategies:**

```bash
curl http://localhost:7654/api/auth/strategies
```

Response should include your OAuth providers:

```json
{
  "strategies": ["password", "google", "github"],
  "basepath": "/api/auth"
}
```

**2. Test OAuth URL generation:**

```bash
curl http://localhost:7654/api/auth/google/login
```

Response:

```json
{
  "url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "challenge": "...",
  "action": "login"
}
```

**3. Complete full OAuth flow:**

- Visit the OAuth URL in browser
- Complete provider login
- Verify redirect to `pathSuccess`
- Check `api/auth/me` returns user

## DOs and DON'Ts

**DO:**

- Store client secrets in environment variables
- Use HTTPS in production
- Set `sameSite: "lax"` for cookie (required for OAuth redirects)
- Match callback URLs exactly in provider dashboard
- Test OAuth flow in incognito (avoid cached sessions)
- Set appropriate JWT expiration

**DON'T:**

- Hardcode client secrets in code
- Use `secure: true` cookie on localhost (no HTTPS)
- Mix up client_id and client_secret
- Forget to update callback URLs for production
- Expect users to have multiple strategies (one per user)
- Skip the challenge verification in token flow

## Related Skills

- **bknd-setup-auth** - Initialize authentication system
- **bknd-login-flow** - Login/logout functionality
- **bknd-registration** - User registration setup
- **bknd-session-handling** - Manage user sessions
- **bknd-create-role** - Define user roles for OAuth users
