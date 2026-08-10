---
name: oauth-2-0-setup
description: Implement OAuth 2.0 authentication flows including authorization code with PKCE, client credentials, and device code for secure API integration. Use when the user requests oauth 2 0 setup or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# OAuth 2.0 Setup

This skill enables an AI agent to implement OAuth 2.0 authentication for API integrations. The agent selects the appropriate grant type for the use case—authorization code with PKCE for user-facing apps, client credentials for machine-to-machine auth, and device code for input-limited devices. It handles token storage, refresh token rotation, CSRF protection via the state parameter, and secure credential management throughout the flow.

## Workflow

1. **Select the appropriate grant type:** Choose the OAuth 2.0 flow based on the client type. Use authorization code with PKCE for web and mobile apps where a user is present—PKCE replaces the client secret and prevents authorization code interception attacks. Use client credentials for server-to-server communication with no user context. Use device code flow for CLI tools or smart TVs where browser-based login isn't possible. Implicit flow is deprecated and should not be used.

2. **Register the application with the provider:** Create an OAuth application in the provider's developer console (Google, GitHub, Auth0, etc.). Configure the redirect URI precisely—mismatched URIs are the most common setup error. For PKCE flows, mark the application as a public client. Record the client ID, client secret (if applicable), authorization endpoint, token endpoint, and scopes.

3. **Implement the authorization request:** Construct the authorization URL with the required parameters: `client_id`, `redirect_uri`, `response_type=code`, `scope`, and a cryptographically random `state` parameter for CSRF protection. For PKCE, generate a random `code_verifier` (43-128 characters), derive the `code_challenge` using SHA-256, and include both `code_challenge` and `code_challenge_method=S256` in the request. Store the state and code_verifier in the session.

4. **Handle the callback and exchange tokens:** When the provider redirects back with the authorization code, first verify the `state` parameter matches what was stored in the session. Then exchange the code for tokens by POSTing to the token endpoint with `grant_type=authorization_code`, the authorization code, `redirect_uri`, `client_id`, and the `code_verifier` (for PKCE). Parse the response for `access_token`, `refresh_token`, `expires_in`, and `token_type`.

5. **Store tokens securely:** Never store tokens in localStorage (XSS vulnerable) or URL parameters (logged in server access logs). Use HTTP-only secure cookies for web apps, the system keychain for desktop apps, and encrypted storage for mobile apps. Store refresh tokens server-side when possible. Record token expiration timestamps so you can proactively refresh before expiry.

6. **Implement token refresh and rotation:** Before each API call, check if the access token is expired or about to expire (within a 60-second window). If so, use the refresh token to get a new access token. Handle refresh token rotation—when the provider issues a new refresh token alongside the new access token, store the new refresh token and invalidate the old one. If refresh fails with an invalid_grant error, the user must re-authenticate.

## Supported Technologies

- **Providers:** Auth0, Google, GitHub, Microsoft Entra ID, Okta, AWS Cognito, Keycloak
- **Server frameworks:** Express.js, FastAPI, Django, Spring Security, ASP.NET Core
- **Libraries:** passport.js (Node.js), authlib (Python), oauthlib (Python), Spring Security OAuth
- **Token formats:** JWT (self-contained), opaque tokens (require introspection)
- **Standards:** RFC 6749 (OAuth 2.0), RFC 7636 (PKCE), RFC 8628 (Device Code), RFC 9449 (DPoP)

## Usage

Provide the agent with the OAuth provider, the type of application (web app, SPA, CLI, server-to-server), and the required scopes. The agent will select the correct grant type and produce a complete implementation including the authorization flow, token exchange, secure storage, and refresh logic.

## Examples

### Example 1: Authorization Code Flow with PKCE (Node.js/Express)

```javascript
const express = require("express");
const crypto = require("crypto");
const session = require("express-session");

const app = express();
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true, httpOnly: true, sameSite: "lax", maxAge: 3600000 },
}));

const OAUTH_CONFIG = {
  clientId: process.env.OAUTH_CLIENT_ID,
  authorizationEndpoint: "https://accounts.google.com/o/oauth2/v2/auth",
  tokenEndpoint: "https://oauth2.googleapis.com/token",
  redirectUri: "https://myapp.com/auth/callback",
  scopes: ["openid", "email", "profile"],
};

// Generate PKCE code verifier and challenge
function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString("base64url");
  const challenge = crypto
    .createHash("sha256")
    .update(verifier)
    .digest("base64url");
  return { verifier, challenge };
}

// Step 1: Start authorization — redirect user to provider
app.get("/auth/login", (req, res) => {
  const state = crypto.randomBytes(16).toString("hex");
  const { verifier, challenge } = generatePKCE();

  // Store in session for verification on callback
  req.session.oauthState = state;
  req.session.codeVerifier = verifier;

  const params = new URLSearchParams({
    client_id: OAUTH_CONFIG.clientId,
    redirect_uri: OAUTH_CONFIG.redirectUri,
    response_type: "code",
    scope: OAUTH_CONFIG.scopes.join(" "),
    state: state,
    code_challenge: challenge,
    code_challenge_method: "S256",
    access_type: "offline",  // Request refresh token
    prompt: "consent",
  });

  res.redirect(`${OAUTH_CONFIG.authorizationEndpoint}?${params}`);
});

// Step 2: Handle callback — verify state and exchange code for tokens
app.get("/auth/callback", async (req, res) => {
  const { code, state, error } = req.query;

  if (error) {
    console.error(`OAuth error: ${error}`);
    return res.redirect("/auth/error");
  }

  // CSRF protection: verify state matches
  if (state !== req.session.oauthState) {
    console.error("State mismatch — possible CSRF attack");
    return res.status(403).send("Invalid state parameter");
  }

  try {
    const tokenResponse = await fetch(OAUTH_CONFIG.tokenEndpoint, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "authorization_code",
        code: code,
        redirect_uri: OAUTH_CONFIG.redirectUri,
        client_id: OAUTH_CONFIG.clientId,
        code_verifier: req.session.codeVerifier,
      }),
    });

    if (!tokenResponse.ok) {
      const err = await tokenResponse.json();
      throw new Error(`Token exchange failed: ${err.error_description || err.error}`);
    }

    const tokens = await tokenResponse.json();

    // Store tokens securely in session (server-side)
    req.session.accessToken = tokens.access_token;
    req.session.refreshToken = tokens.refresh_token;
    req.session.tokenExpiry = Date.now() + tokens.expires_in * 1000;

    // Clean up PKCE and state from session
    delete req.session.oauthState;
    delete req.session.codeVerifier;

    res.redirect("/dashboard");
  } catch (err) {
    console.error("Token exchange error:", err.message);
    res.redirect("/auth/error");
  }
});

// Token refresh middleware
async function ensureValidToken(req, res, next) {
  if (!req.session.accessToken) {
    return res.redirect("/auth/login");
  }

  // Refresh if token expires within 60 seconds
  if (Date.now() > req.session.tokenExpiry - 60000) {
    try {
      const refreshResponse = await fetch(OAUTH_CONFIG.tokenEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          grant_type: "refresh_token",
          refresh_token: req.session.refreshToken,
          client_id: OAUTH_CONFIG.clientId,
        }),
      });

      if (!refreshResponse.ok) throw new Error("Refresh failed");

      const tokens = await refreshResponse.json();
      req.session.accessToken = tokens.access_token;
      req.session.tokenExpiry = Date.now() + tokens.expires_in * 1000;
      // Handle refresh token rotation
      if (tokens.refresh_token) {
        req.session.refreshToken = tokens.refresh_token;
      }
    } catch {
      // Refresh token is invalid — user must re-authenticate
      req.session.destroy();
      return res.redirect("/auth/login");
    }
  }
  next();
}

app.get("/dashboard", ensureValidToken, async (req, res) => {
  const profile = await fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
    headers: { Authorization: `Bearer ${req.session.accessToken}` },
  });
  const user = await profile.json();
  res.json({ message: `Welcome, ${user.name}` });
});

app.listen(3000);
```

### Example 2: Client Credentials Flow (Machine-to-Machine)

```python
import os
import time
import threading
import requests

class ClientCredentialsAuth:
    """OAuth 2.0 client credentials flow for server-to-server auth.

    Manages token lifecycle with thread-safe caching and automatic refresh.
    """

    def __init__(self, token_endpoint: str, client_id: str, client_secret: str,
                 scopes: list[str] | None = None):
        self.token_endpoint = token_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes or []
        self._access_token: str | None = None
        self._token_expiry: float = 0
        self._lock = threading.Lock()

    def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        with self._lock:
            if self._access_token and time.time() < self._token_expiry - 60:
                return self._access_token
            return self._fetch_new_token()

    def _fetch_new_token(self) -> str:
        response = requests.post(
            self.token_endpoint,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": " ".join(self.scopes),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )
        response.raise_for_status()
        token_data = response.json()

        self._access_token = token_data["access_token"]
        self._token_expiry = time.time() + token_data.get("expires_in", 3600)
        return self._access_token

    def authorized_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an HTTP request with automatic bearer token injection."""
        token = self.get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        return requests.request(method, url, headers=headers, **kwargs)


# Usage
auth = ClientCredentialsAuth(
    token_endpoint="https://auth.example.com/oauth/token",
    client_id=os.environ["M2M_CLIENT_ID"],
    client_secret=os.environ["M2M_CLIENT_SECRET"],
    scopes=["read:data", "write:data"],
)

# Token is fetched automatically and cached
response = auth.authorized_request("GET", "https://api.example.com/v1/reports")
print(response.json())

# Subsequent calls reuse the cached token until it nears expiry
response = auth.authorized_request("POST", "https://api.example.com/v1/exports", json={
    "format": "csv",
    "date_range": "2024-01-01/2024-12-31",
})
print(f"Export started: {response.json()['export_id']}")
```

## Best Practices

- **Always use PKCE** for authorization code flows, even for confidential clients. It adds defense in depth against code interception at zero cost. The implicit flow is deprecated—do not use it.
- **Validate the state parameter** on every callback before processing the authorization code. This is your primary defense against CSRF attacks. Use a cryptographically random value of at least 128 bits.
- **Store tokens server-side** whenever possible. For web apps, keep tokens in the server session and use HTTP-only, secure, SameSite cookies for the session ID. Never expose access tokens to client-side JavaScript.
- **Implement refresh token rotation** so that each refresh token can only be used once. When you receive a new refresh token in a token response, immediately replace the old one. If a rotated token is reused, treat it as a compromise and revoke all tokens for that session.
- **Request minimum scopes** and use incremental authorization when available. Start with the least privilege and request additional scopes only when the user performs an action that needs them.
- **Set short access token lifetimes** (5-15 minutes for sensitive APIs) and rely on refresh tokens for longevity. This limits the damage window if an access token is leaked.

## Edge Cases

- **Refresh token expiry:** Refresh tokens can expire or be revoked. When a refresh attempt returns `invalid_grant`, destroy the session and redirect the user to re-authenticate. Do not retry indefinitely.
- **Concurrent refresh requests:** If multiple threads try to refresh the token simultaneously, only one should perform the refresh while others wait. Use a mutex or single-flight pattern to prevent multiple refresh requests racing and invalidating each other's tokens.
- **Provider outages:** If the token endpoint is unreachable, continue using the current access token if it hasn't expired yet. Queue retries for token refresh with exponential backoff rather than failing immediately.
- **Clock skew:** Token expiration checks depend on accurate clocks. Add a buffer (30-60 seconds) when checking expiry to account for clock differences between your server and the OAuth provider.
- **Redirect URI mismatch:** OAuth providers require exact redirect URI matching. Ensure your registered URI matches exactly, including the protocol, port, and trailing slash. Mismatches cause silent failures that are hard to debug.
- **Token leakage in logs:** Access tokens appearing in logs, error messages, or URLs are a common vulnerability. Redact tokens in all logging middleware. Never pass tokens as URL query parameters—use Authorization headers exclusively.
