---
name: sast-patterns
description: Static Application Security Testing patterns, OWASP Top 10 checklist, language-specific vulnerability patterns, Semgrep rule writing guide, and CI/CD integration. Use when scanning code for security vulnerabilities or writing custom SAST rules.
---

# SAST Patterns Skill

Comprehensive vulnerability pattern library for static application security testing. Covers OWASP Top 10, language-specific patterns, Semgrep custom rules, and CI/CD pipeline integration.

## When to Activate

- Running security scans on code
- Writing custom Semgrep rules
- Setting up CI/CD security gates
- Reviewing code for security vulnerabilities
- After sast-on-edit hook triggers
- Before production deployment

---

## OWASP Top 10 (2021) Checklist

### A01: Broken Access Control

**What to Look For:**
- Missing authorization checks on endpoints
- Direct object reference without ownership validation
- CORS misconfiguration allowing wildcard origins
- Missing function-level access control
- Metadata manipulation (JWT, cookies, hidden fields)

**Detection Patterns:**

```javascript
// VULNERABLE: No authorization check
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id)
  res.json(user)  // Anyone can access any user
})

// SECURE: Authorization verified
app.get('/api/users/:id', authenticate, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' })
  }
  const user = await db.users.findById(req.params.id)
  res.json(user)
})
```

```python
# VULNERABLE: No permission check
@app.route('/admin/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.session.delete(User.query.get(user_id))
    db.session.commit()

# SECURE: Permission verified
@app.route('/admin/delete/<user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    db.session.delete(User.query.get(user_id))
    db.session.commit()
```

**Semgrep Rules:**
```yaml
rules:
  - id: missing-auth-check
    patterns:
      - pattern: |
          app.$METHOD($PATH, async (req, res) => {
            ...
            $DB.$QUERY(...)
            ...
          })
      - pattern-not: |
          app.$METHOD($PATH, authenticate, ...)
    message: "Endpoint missing authentication middleware"
    severity: ERROR
```

---

### A02: Cryptographic Failures

**What to Look For:**
- Hardcoded secrets in source code
- Weak hashing (MD5, SHA1) for passwords
- Missing encryption for sensitive data at rest
- HTTP instead of HTTPS
- Weak TLS configuration

**Detection Patterns:**

```javascript
// VULNERABLE: Weak password hashing
const hash = crypto.createHash('md5').update(password).digest('hex')

// SECURE: Strong password hashing
const hash = await bcrypt.hash(password, 12)
```

```python
# VULNERABLE: Hardcoded secret
SECRET_KEY = "my-super-secret-key-123"

# SECURE: Environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable required")
```

**Regex Patterns for Detection:**
```
# API Keys
(?:api[_-]?key|apikey)\s*[:=]\s*['"][A-Za-z0-9_\-]{20,}['"]

# AWS Keys
(?:AKIA|ASIA)[A-Z0-9]{16}

# Generic Secrets
(?:password|passwd|pwd|secret|token)\s*[:=]\s*['"][^'"]{8,}['"]

# Private Keys
-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----

# JWT Tokens
eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+
```

---

### A03: Injection

**What to Look For:**
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell execution)
- NoSQL injection (MongoDB query operators in user input)
- LDAP injection
- Expression Language injection

**Detection Patterns:**

```javascript
// SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`  // VULNERABLE
const query = 'SELECT * FROM users WHERE id = $1'         // SECURE

// Command Injection
exec(`ping ${hostname}`)           // VULNERABLE
execFile('ping', [hostname])        // SECURE

// NoSQL Injection (MongoDB)
db.users.find({ email: req.body.email })        // VULNERABLE if email = {"$gt": ""}
db.users.find({ email: String(req.body.email) }) // SECURE: type coercion
```

```python
# SQL Injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # VULNERABLE
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))  # SECURE

# Command Injection
os.system(f"convert {filename} output.png")                # VULNERABLE
subprocess.run(['convert', filename, 'output.png'], check=True)  # SECURE
```

```go
// SQL Injection
db.Query("SELECT * FROM users WHERE id = " + userID)     // VULNERABLE
db.Query("SELECT * FROM users WHERE id = $1", userID)     // SECURE

// Command Injection
exec.Command("sh", "-c", userInput)                       // VULNERABLE
exec.Command("ping", "-c", "1", hostname)                 // SECURE
```

```java
// SQL Injection
stmt.executeQuery("SELECT * FROM users WHERE id = " + id);          // VULNERABLE
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setString(1, id);                                                // SECURE
```

---

### A04: Insecure Design

**What to Look For:**
- Missing rate limiting on critical operations
- No account lockout after failed attempts
- Missing CAPTCHA on public forms
- Business logic flaws
- Missing transaction atomicity

**Detection Patterns:**

```javascript
// VULNERABLE: No rate limiting on login
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body)
  res.json({ token: generateToken(user) })
})

// SECURE: Rate limited login
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts'
})
app.post('/login', loginLimiter, async (req, res) => {
  const user = await authenticate(req.body)
  res.json({ token: generateToken(user) })
})
```

```python
# VULNERABLE: Race condition in balance check
balance = get_balance(user_id)
if balance >= amount:
    withdraw(user_id, amount)  # Another request could drain first

# SECURE: Atomic transaction
with db.transaction():
    balance = db.query("SELECT balance FROM accounts WHERE id = %s FOR UPDATE", user_id)
    if balance >= amount:
        db.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", amount, user_id)
```

---

### A05: Security Misconfiguration

**What to Look For:**
- Debug mode in production
- Default credentials
- Unnecessary features enabled
- Missing security headers
- Verbose error messages
- Directory listing enabled

**Detection Patterns:**

```javascript
// VULNERABLE: Debug mode
app.set('env', 'development')  // In production config

// VULNERABLE: Missing security headers
// No helmet or manual headers

// SECURE: Security headers
import helmet from 'helmet'
app.use(helmet())
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
  }
}))
```

```python
# VULNERABLE: Debug in production
DEBUG = True  # In production settings

# VULNERABLE: Default secret key
SECRET_KEY = 'django-insecure-change-me'

# SECURE
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```

**Security Headers Checklist:**
```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

### A06: Vulnerable and Outdated Components

**Detection Commands:**

```bash
# Node.js
npm audit
npm audit --json
npm outdated

# Python
pip-audit
safety check
pip list --outdated

# Go
go list -m -u all
govulncheck ./...

# Java
mvn dependency-check:check
gradle dependencyCheckAnalyze

# Ruby
bundle audit check
```

---

### A07: Identification and Authentication Failures

**What to Look For:**
- Weak password policies
- Missing MFA
- Session fixation
- Credential stuffing vulnerability
- Plaintext password storage/comparison

**Detection Patterns:**

```javascript
// VULNERABLE: Plaintext password comparison
if (password === user.password) { /* login */ }

// SECURE: Hashed comparison
const isValid = await bcrypt.compare(password, user.passwordHash)

// VULNERABLE: Weak session management
app.use(session({ secret: 'secret' }))

// SECURE: Strong session
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 3600000
  }
}))
```

---

### A08: Software and Data Integrity Failures

**What to Look For:**
- Missing Subresource Integrity (SRI) on CDN scripts
- Insecure deserialization
- Missing code signing
- Auto-update without integrity verification
- CI/CD pipeline without integrity checks

**Detection Patterns:**

```html
<!-- VULNERABLE: No SRI -->
<script src="https://cdn.example.com/lib.js"></script>

<!-- SECURE: With SRI -->
<script src="https://cdn.example.com/lib.js"
  integrity="sha384-abc123..."
  crossorigin="anonymous"></script>
```

```python
# VULNERABLE: Insecure deserialization
import pickle
data = pickle.loads(user_input)

# SECURE: Use JSON
import json
data = json.loads(user_input)
```

---

### A09: Security Logging and Monitoring Failures

**What to Look For:**
- Missing audit logs for auth events
- Sensitive data in logs
- No log integrity protection
- Missing alerting for suspicious activity

**Detection Patterns:**

```javascript
// VULNERABLE: No logging
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body)
  if (!user) return res.status(401).json({ error: 'Invalid' })
  res.json({ token: generateToken(user) })
})

// SECURE: Audit logging
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body)
  if (!user) {
    logger.warn('Failed login attempt', {
      email: req.body.email,
      ip: req.ip,
      timestamp: new Date().toISOString()
    })
    return res.status(401).json({ error: 'Invalid credentials' })
  }
  logger.info('Successful login', { userId: user.id, ip: req.ip })
  res.json({ token: generateToken(user) })
})

// VULNERABLE: Sensitive data in logs
console.log('Login:', { email, password, token })

// SECURE: Redacted logs
console.log('Login:', { email, passwordProvided: !!password })
```

---

### A10: Server-Side Request Forgery (SSRF)

**What to Look For:**
- User-controlled URLs in server-side requests
- Missing URL validation/whitelist
- Internal service access via SSRF
- Cloud metadata endpoint access

**Detection Patterns:**

```javascript
// VULNERABLE: SSRF
const response = await fetch(req.query.url)

// SECURE: URL whitelist
const ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']
const url = new URL(req.query.url)
if (!ALLOWED_DOMAINS.includes(url.hostname)) {
  throw new Error('Domain not allowed')
}
// Also block internal IPs
const ip = await dns.resolve(url.hostname)
if (isPrivateIP(ip)) {
  throw new Error('Internal addresses not allowed')
}
const response = await fetch(url.toString())
```

```python
# VULNERABLE: SSRF
response = requests.get(user_url)

# SECURE: URL validation
from urllib.parse import urlparse
parsed = urlparse(user_url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("Domain not allowed")
if is_private_ip(socket.gethostbyname(parsed.hostname)):
    raise ValueError("Internal addresses blocked")
response = requests.get(user_url, allow_redirects=False)
```

---

## Semgrep Custom Rule Writing Guide

### Basic Rule Structure

```yaml
rules:
  - id: rule-unique-id
    pattern: |
      eval($USER_INPUT)
    message: "eval() with dynamic input detected - potential RCE"
    languages: [javascript, typescript]
    severity: ERROR
    metadata:
      cwe:
        - CWE-94
      owasp:
        - A03:2021
      category: security
      confidence: HIGH
```

### Pattern Operators

```yaml
# pattern: match exactly
- pattern: eval($X)

# pattern-not: exclude matches
- pattern-not: eval("static-string")

# patterns: AND (all must match)
- patterns:
    - pattern: $DB.query($SQL)
    - pattern-not: $DB.query($SQL, $PARAMS)

# pattern-either: OR (any can match)
- pattern-either:
    - pattern: eval($X)
    - pattern: new Function($X)

# pattern-inside: match within a context
- pattern-inside: |
    app.$METHOD($PATH, (req, res) => {
      ...
    })

# pattern-not-inside: exclude context
- pattern-not-inside: |
    app.$METHOD($PATH, authenticate, ...)

# pattern-regex: regex in code
- pattern-regex: "password\s*=\s*['\"][^'\"]{3,}['\"]"
```

### Metavariable Constraints

```yaml
rules:
  - id: weak-hash-for-passwords
    patterns:
      - pattern: crypto.createHash($ALG).update($INPUT)
      - metavariable-regex:
          metavariable: $ALG
          regex: "('md5'|'sha1')"
      - metavariable-regex:
          metavariable: $INPUT
          regex: ".*password.*"
    message: "Weak hash algorithm used for password: $ALG"
    languages: [javascript, typescript]
    severity: ERROR
```

### Taint Analysis (Pro)

```yaml
rules:
  - id: sql-injection-taint
    mode: taint
    pattern-sources:
      - pattern: req.body.$PARAM
      - pattern: req.query.$PARAM
      - pattern: req.params.$PARAM
    pattern-sinks:
      - pattern: $DB.query($SQL)
    pattern-sanitizers:
      - pattern: $DB.escape($X)
      - pattern: sanitize($X)
    message: "User input flows to SQL query without sanitization"
    languages: [javascript]
    severity: ERROR
```

### Project .semgrep.yml Example

```yaml
rules:
  - id: no-hardcoded-secrets
    pattern-regex: |
      (?:api[_-]?key|secret|password|token)\s*[:=]\s*['"][A-Za-z0-9+/=_\-]{16,}['"]
    paths:
      exclude:
        - "*.test.*"
        - "*.spec.*"
        - "__tests__/*"
        - "*.example"
    message: "Potential hardcoded secret detected"
    languages: [generic]
    severity: ERROR

  - id: no-console-log-sensitive
    patterns:
      - pattern: console.log(..., $DATA, ...)
      - metavariable-regex:
          metavariable: $DATA
          regex: ".*(?:password|secret|token|key|credential).*"
    message: "Sensitive data in console.log"
    languages: [javascript, typescript]
    severity: WARNING

  - id: require-input-validation
    patterns:
      - pattern: |
          app.post($PATH, async (req, res) => {
            ...
            $DB.$METHOD(req.body)
            ...
          })
      - pattern-not: |
          app.post($PATH, async (req, res) => {
            ...
            $SCHEMA.parse(...)
            ...
          })
    message: "POST endpoint without input validation"
    languages: [javascript, typescript]
    severity: WARNING
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: SAST Security Scan

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Semgrep Scan
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/secrets
            p/typescript
          generateSarif: "1"
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
        if: always()

      - name: Dependency Audit
        run: npm audit --audit-level=high

      - name: Check for Secrets
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/semgrep/semgrep
    rev: 'v1.60.0'
    hooks:
      - id: semgrep
        args: ['--config', 'auto', '--error', '--severity', 'ERROR']
```

### GitLab CI

```yaml
sast:
  stage: test
  image: semgrep/semgrep
  script:
    - semgrep --config auto --config "p/secrets" --json --output gl-sast-report.json .
  artifacts:
    reports:
      sast: gl-sast-report.json
  rules:
    - if: $CI_MERGE_REQUEST_ID
```

### CLI Commands Quick Reference

```bash
# Full scan with auto rules
semgrep --config auto .

# OWASP + Secrets
semgrep --config "p/owasp-top-ten" --config "p/secrets" .

# Only errors (for CI gates)
semgrep --config auto --error --severity ERROR .

# JSON output for processing
semgrep --config auto --json --output report.json .

# Scan specific files
semgrep --config auto src/api/ src/auth/

# Diff-aware (only changed code)
semgrep --config auto --baseline-commit origin/main

# Custom rules
semgrep --config .semgrep.yml .

# Exclude test files
semgrep --config auto --exclude="*test*" --exclude="*spec*" .

# With metrics disabled (privacy)
semgrep --config auto --metrics=off .
```

---

## Severity Classification Guide

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| CRITICAL | Exploitable RCE, SQLi, auth bypass, data breach | Fix IMMEDIATELY, block deploy | < 1 hour |
| HIGH | XSS, SSRF, IDOR, missing auth, weak crypto | Fix before production | < 24 hours |
| MEDIUM | Missing validation, verbose errors, weak headers | Fix in current sprint | < 1 week |
| LOW | Debug mode, outdated lib (no known CVE), info leak | Fix in backlog | < 1 month |

## Quick Decision Tree

```
Is user input involved?
  YES -> Does it reach a dangerous sink (DB, exec, DOM)?
    YES -> Is it sanitized/validated?
      NO  -> CRITICAL (injection)
      YES -> Check sanitizer adequacy -> MEDIUM if weak
    NO  -> MEDIUM (missing validation)
  NO  -> Is it a configuration issue?
    YES -> Affects security posture?
      YES -> HIGH (misconfiguration)
      NO  -> LOW (best practice)
    NO  -> Is it a dependency issue?
      YES -> Known CVE?
        YES -> Match CVE severity
        NO  -> LOW (outdated)
      NO  -> Informational
```

---

## Resources

- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [Semgrep Registry](https://semgrep.dev/explore)
- [Semgrep Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax/)
- [CWE Database](https://cwe.mitre.org/)
- [NIST NVD](https://nvd.nist.gov/)
- [Snyk Vulnerability DB](https://security.snyk.io/)

---

**Remember**: SAST catches patterns, not intent. Always verify findings with manual review. A finding is only a vulnerability if it can be exploited in the application's specific context.
