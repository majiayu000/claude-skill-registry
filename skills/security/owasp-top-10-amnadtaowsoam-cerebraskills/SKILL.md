---
name: OWASP Top 10
description: Understanding and mitigating the top 10 most critical security risks to web applications as defined by OWASP, including broken access control, cryptographic failures, injection, and insecure design.
---

# OWASP Top 10

> **Current Level:** Intermediate  
> **Domain:** Security / Application Security

---

## Overview

The OWASP (Open Web Application Security Project) Top 10 is a standard awareness document representing a broad consensus about the most critical security risks to web applications. Updated every 3-4 years (2021 is the latest version), it provides a prioritized list of security risks and mitigation strategies.

## What is OWASP Top 10

### Why OWASP Top 10 Matters

| Benefit | Impact |
|---------|---------|
| **Industry Standard** | Widely recognized security framework |
| **Prioritization** | Focus on most critical risks |
| **Compliance** | Required by many security standards |
| **Education** | Learn common vulnerabilities |
| **Testing** | Guide for security testing |

## A01: Broken Access Control

### Description

Users can access resources or perform actions they shouldn't be able to, due to missing or ineffective access controls.

### Examples

| Scenario | Description |
|-----------|-------------|
| **View other users' data** | Access `/user/123` when logged in as user 456 |
| **Access admin functions** | Access `/admin` without admin role |
| **Modify others' data** | Update `/user/123/profile` as user 456 |
| **Bypass authorization** | Access API endpoints without proper auth |

### Prevention

```javascript
// Bad: No authorization check
app.get('/user/:id', (req, res) => {
    const user = getUser(req.params.id);
    res.json(user); // Anyone can view any user!
});

// Good: Check authorization
app.get('/user/:id', (req, res) => {
    if (req.params.id !== req.user.id && !req.user.isAdmin) {
        return res.status(403).json({ error: 'Forbidden' });
    }
    const user = getUser(req.params.id);
    res.json(user);
});
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Deny by default** | Explicitly allow, deny everything else |
| **Check server-side** | Never trust client-side checks |
| **Principle of least privilege** | Grant minimum necessary access |
| **Log access** | Track who accesses what |
| **Regular audit** | Review access controls regularly |

## A02: Cryptographic Failures

### Description

Sensitive data is exposed due to weak or missing encryption, or improper cryptographic practices.

### Examples

| Scenario | Description |
|-----------|-------------|
| **Passwords in plaintext** | Stored without hashing |
| **Weak hashing** | Using MD5, SHA1 for passwords |
| **Unencrypted transmission** | HTTP instead of HTTPS |
| **Hardcoded keys** | Encryption keys in source code |
| **Weak algorithms** | Using DES, RC4 |

### Prevention

```javascript
// Bad: Weak password hashing
const hash = md5(password); // MD5 is broken

// Good: Strong password hashing
const hash = await bcrypt.hash(password, 10);

// Bad: Hardcoded key
const apiKey = 'sk_live_1234567890';

// Good: Environment variable
const apiKey = process.env.API_KEY;

// Bad: No encryption in transit
http.createServer((req, res) => { ... }); // HTTP

// Good: Use HTTPS
https.createServer(options, (req, res) => { ... });
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Encrypt at rest** | Use AES-256 for sensitive data |
| **Encrypt in transit** | Use TLS (HTTPS) |
| **Strong password hashing** | Use bcrypt, Argon2, scrypt |
| **Never store plaintext passwords** | Always hash passwords |
| **Key management** | Use secure key management service |
| **Update algorithms** | Use current, strong algorithms |

## A03: Injection

### Description

Malicious data is sent to an interpreter as part of a command or query, allowing attackers to execute unintended commands.

### SQL Injection

**Example Attack**:
```sql
-- Vulnerable query
SELECT * FROM users WHERE username = '$username' AND password = '$password';

-- Attack payload
username: ' OR '1'='1
password: anything

-- Resulting query (always true)
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything'
```

### Prevention

```javascript
// Bad: String concatenation
const query = `SELECT * FROM users WHERE username = '${username}'`;

// Good: Parameterized query
const query = 'SELECT * FROM users WHERE username = $1';
await db.query(query, [username]);

// Good: Using ORM
const user = await User.findOne({ where: { username } });
```

### Other Injection Types

| Type | Example | Prevention |
|-------|----------|-------------|
| **NoSQL Injection** | MongoDB query injection | Use parameterized queries |
| **OS Command Injection** | `; rm -rf /` | Use parameterized APIs |
| **LDAP Injection** | `*)(&` | Use parameterized queries |
| **XPath Injection** | `1' or '1'='1` | Use parameterized queries |

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Parameterized queries** | Never concatenate user input |
| **Use ORM** | Let ORM handle escaping |
| **Input validation** | Validate and sanitize input |
| **Least privilege** | Use least-privileged DB user |
| **Stored procedures** | Use when appropriate |

## A04: Insecure Design

### Description

Missing or ineffective security controls by design, not implementation.

### Examples

| Scenario | Description |
|-----------|-------------|
| **No rate limiting** | Brute force attacks possible |
| **Weak password policy** | Users can set weak passwords |
| **No MFA** | Single-factor authentication |
| **Insecure defaults** | Default admin/admin passwords |
| **No security headers** | Missing CSP, HSTS |

### Prevention

```javascript
// Bad: No rate limiting
app.post('/login', (req, res) => {
    // No rate limit, brute force possible
});

// Good: Rate limiting
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5 // limit each IP to 5 requests per windowMs
});

app.post('/login', limiter, (req, res) => {
    // Rate limited
});

// Good: Security headers
app.use(helmet());
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Threat modeling** | Identify threats during design |
| **Secure design patterns** | Use proven patterns |
| **Defense in depth** | Multiple security layers |
| **Security by design** | Build security from start |
| **Regular reviews** | Review design for security issues |

## A05: Security Misconfiguration

### Description

Insecure default configurations, incomplete setups, open cloud storage, verbose error messages, etc.

### Examples

| Scenario | Description |
|-----------|-------------|
| **Default credentials** | admin/admin, root/password |
| **Directory listing** | Files visible at `/files/` |
| **Verbose errors** | Stack traces exposed to users |
| **Unnecessary services** | Debug mode enabled in production |
| **Open cloud storage** | S3 bucket publicly accessible |

### Prevention

```javascript
// Bad: Verbose error messages
app.use((err, req, res, next) => {
    res.status(500).json({
        error: err.message,
        stack: err.stack // Exposes internal details
    });
});

// Good: Generic error messages
app.use((err, req, res, next) => {
    console.error(err); // Log full error
    res.status(500).json({
        error: 'Internal server error'
    });
});

// Good: Disable directory listing
app.use(express.static('public', {
    index: false,
    showDir: false
}));
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Hardening guides** | Follow vendor hardening guides |
| **Remove defaults** | Change default credentials |
| **Minimal install** | Install only what's needed |
| **Disable debug** | Never run debug in production |
| **Automated scanning** | Use config scanning tools |
| **Cloud security** | Review cloud configurations |

## A06: Vulnerable and Outdated Components

### Description

Using libraries, frameworks, or other software modules with known vulnerabilities.

### Examples

| Scenario | Description |
|-----------|-------------|
| **Old React version** | Known XSS vulnerability |
| **Outdated OpenSSL** | Heartbleed vulnerability |
| **Vulnerable npm package** | Malicious code in dependency |
| **Unpatched server** | Known exploit available |

### Prevention

```bash
# Check for vulnerabilities
npm audit

# Update dependencies
npm update

# Use Snyk
snyk test

# Use Dependabot (GitHub)
# Automatically creates PRs for vulnerable dependencies
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Dependency scanning** | Regularly scan for vulnerabilities |
| **Keep updated** | Update dependencies regularly |
| **Remove unused** | Delete unused dependencies |
| **Use lockfiles** | Pin dependency versions |
| **Monitor CVEs** | Watch for new vulnerabilities |
| **Automated updates** | Use Dependabot, Renovate |

## A07: Identification and Authentication Failures

### Description

Broken authentication mechanisms allowing attackers to compromise user identities.

### Examples

| Scenario | Description |
|-----------|-------------|
| **Weak passwords allowed** | No password complexity requirements |
| **No MFA** | Only password required |
| **Session fixation** | Attacker sets session ID |
| **Credential stuffing** | Reuse of compromised credentials |
| **Password reset flaws** | Weak reset tokens |

### Prevention

```javascript
// Bad: Weak password validation
if (password.length < 6) {
    return 'Password too short';
}

// Good: Strong password validation
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
if (!passwordRegex.test(password)) {
    return 'Password must be 8+ chars with uppercase, lowercase, and number';
}

// Good: MFA
app.post('/login', async (req, res) => {
    const { username, password, totpCode } = req.body;

    // Verify password
    const user = await verifyPassword(username, password);
    if (!user) return res.status(401).json({ error: 'Invalid credentials' });

    // Verify MFA
    if (!verifyTOTP(user.totpSecret, totpCode)) {
        return res.status(401).json({ error: 'Invalid MFA code' });
    }

    // Create session
    req.session.userId = user.id;
    res.json({ success: true });
});
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Strong password policy** | Enforce complexity |
| **MFA required** | Require 2FA for sensitive actions |
| **Secure session management** | Use secure session tokens |
| **Rate limiting** | Limit login attempts |
| **Secure password reset** | Use time-limited, single-use tokens |
| **Credential stuffing protection** | Detect and block reused credentials |

## A08: Software and Data Integrity Failures

### Description

Code or infrastructure without integrity verification, allowing supply chain attacks or unauthorized modifications.

### Examples

| Scenario | Description |
|-----------|-------------|
| **Supply chain attack** | Malicious npm package |
| **Unsigned updates** | No verification of updates |
| **Insecure CI/CD** | Unauthorized code changes |
| **Missing code signing** | Executables not signed |
| **Subresource integrity** | CDN resources not verified |

### Prevention

```bash
# Verify package integrity
npm install --package-lock-only

# Use npm audit
npm audit

# Use SRI (Subresource Integrity)
<script src="https://cdn.example.com/script.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Code signing** | Sign executables and packages |
| **Verify dependencies** | Check lockfiles |
| **Secure CI/CD** | Require approvals, sign artifacts |
| **Supply chain security** | Vet dependencies |
| **SRI** | Use subresource integrity for CDN resources |
| **Immutable infrastructure** | Don't modify running systems |

## A09: Security Logging and Monitoring Failures

### Description

Insufficient logging, lack of alerting on suspicious activity, or missing audit trails.

### Examples

| Scenario | Description |
|-----------|-------------|
| **No login logging** | Can't detect unauthorized access |
| **No error logging** | Can't diagnose issues |
| **No alerting** | Attacks go unnoticed |
| **Insufficient logs** | Missing critical events |
| **Logs not reviewed** | Attacks detected but ignored |

### Prevention

```javascript
// Good: Comprehensive logging
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

// Log security events
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const ip = req.ip;

    try {
        const user = await verifyPassword(username, password);
        if (user) {
            logger.info('Login successful', { username, ip, userId: user.id });
            req.session.userId = user.id;
            res.json({ success: true });
        } else {
            logger.warn('Login failed', { username, ip });
            res.status(401).json({ error: 'Invalid credentials' });
        }
    } catch (error) {
        logger.error('Login error', { username, ip, error: error.message });
        res.status(500).json({ error: 'Internal error' });
    }
});
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **Log security events** | Logins, failures, privilege changes |
| **SIEM integration** | Centralize logs |
| **Real-time alerting** | Alert on suspicious activity |
| **Log retention** | Keep logs for investigation |
| **Log review** | Regularly review logs |
| **Audit trails** | Track who did what |

## A10: Server-Side Request Forgery (SSRF)

### Description

Application fetches remote resource without validating user-supplied URL, allowing attackers to access internal resources.

### Examples

| Scenario | Description |
|-----------|-------------|
| **Internal network access** | Access internal APIs |
| **Cloud metadata** | Read cloud instance metadata |
| **Port scanning** | Scan internal network |
| **File access** | Access internal files |

### Prevention

```javascript
// Bad: No URL validation
app.get('/fetch', async (req, res) => {
    const url = req.query.url;
    const response = await axios.get(url); // Fetches any URL!
    res.json(response.data);
});

// Good: URL whitelist
const ALLOWED_HOSTS = ['api.example.com', 'cdn.example.com'];

app.get('/fetch', async (req, res) => {
    const url = req.query.url;
    const parsed = new URL(url);

    if (!ALLOWED_HOSTS.includes(parsed.hostname)) {
        return res.status(400).json({ error: 'Invalid URL' });
    }

    const response = await axios.get(url);
    res.json(response.data);
});

// Good: Use URL library for validation
const { URL } = require('url');

app.get('/fetch', async (req, res) => {
    const url = req.query.url;
    const parsed = new URL(url);

    // Block private IPs
    if (parsed.hostname.startsWith('192.168.') ||
        parsed.hostname.startsWith('10.') ||
        parsed.hostname.startsWith('127.')) {
        return res.status(400).json({ error: 'Invalid URL' });
    }

    const response = await axios.get(url);
    res.json(response.data);
});
```

### Best Practices

| Practice | Description |
|-----------|-------------|
| **URL whitelist** | Only allow specific hosts |
| **Validate URLs** | Parse and validate URLs |
| **Network segmentation** | Restrict outbound access |
| **Disable unnecessary protocols** | Block file://, ftp:// |
| **Use allowlist** | Allow only what's needed |
| **Cloud metadata protection** | Block metadata endpoints |

## Testing for OWASP Top 10

### Manual Testing

| Test Type | What to Check |
|------------|----------------|
| **Access control** | Try accessing others' data |
| **Injection** | Try SQL injection payloads |
| **Authentication** | Test weak passwords, no MFA |
| **SSRF** | Try internal URLs |
| **Misconfiguration** | Check for default credentials |

### Automated Scanning

| Tool | Type | What It Finds |
|-------|-------|----------------|
| **OWASP ZAP** | DAST | Web vulnerabilities |
| **Burp Suite** | DAST | Web vulnerabilities |
| **Nessus** | Vulnerability scanner | Known vulnerabilities |
| **SonarQube** | SAST | Code vulnerabilities |
| **Snyk** | Dependency scanner | Vulnerable dependencies |

### Code Review

**What to Look For**:
- User input handling
- Authentication/authorization checks
- Cryptographic usage
- Error handling
- Logging

## Prevention Checklist

### Input Validation

| Practice | Status |
|-----------|--------|
| [ ] Validate all user input |
| [ ] Use allowlists (not blocklists) |
| [ ] Sanitize input for context |
| [ ] Validate data types |
| [ ] Check input length |

### Output Encoding

| Practice | Status |
|-----------|--------|
| [ ] Encode HTML output (prevent XSS) |
| [ ] Encode URL parameters |
| [ ] Encode JSON output |
| [ ] Use template engines with auto-escaping |

### Parameterized Queries

| Practice | Status |
|-----------|--------|
| [ ] Never concatenate SQL |
| [ ] Use parameterized queries |
| [ ] Use ORM when possible |
| [ ] Use least-privileged DB user |

### Authentication and Authorization

| Practice | Status |
|-----------|--------|
| [ ] Check auth on every request |
| [ ] Implement authorization checks |
| [ ] Use strong password hashing |
| [ ] Require MFA for sensitive actions |
| [ ] Implement rate limiting |

### HTTPS Everywhere

| Practice | Status |
|-----------|--------|
| [ ] Use HTTPS everywhere |
| [ ] Redirect HTTP to HTTPS |
| [ ] Use HSTS |
| [ ] Use strong TLS configuration |

### Security Headers

| Header | Purpose |
|---------|---------|
| **Content-Security-Policy** | Prevent XSS |
| **Strict-Transport-Security** | Force HTTPS |
| **X-Content-Type-Options** | Prevent MIME sniffing |
| **X-Frame-Options** | Prevent clickjacking |
| **X-XSS-Protection** | XSS protection |

```javascript
// Using Helmet.js
const helmet = require('helmet');

app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
        },
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    }
}));
```

## Secure Coding Practices

### Principles

| Principle | Description |
|-----------|-------------|
| **Principle of least privilege** | Grant minimum necessary access |
| **Defense in depth** | Multiple security layers |
| **Fail securely** | Errors don't expose info |
| **Keep it simple** | Complexity = bugs |
| **Don't trust input** | Validate and sanitize |

### Secure Coding Examples

```javascript
// Bad: Trust user input
const filename = req.params.filename;
fs.readFile(`/uploads/${filename}`, (err, data) => {
    // Path traversal vulnerability!
});

// Good: Validate and sanitize
const filename = req.params.filename;
const safeFilename = path.basename(filename); // Remove path traversal
const safePath = path.join('/uploads', safeFilename);
fs.readFile(safePath, (err, data) => {
    // Safe!
});
```

## Developer Security Training

### Training Topics

| Topic | Description |
|--------|-------------|
| **OWASP Top 10** | Understand common vulnerabilities |
| **Secure coding** | Learn secure coding practices |
| **Common patterns** | Recognize vulnerability patterns |
| **Tools** | Learn to use security tools |
| **Updates** | Stay current on threats |

### Training Methods

| Method | Frequency |
|---------|-----------|
| **Workshops** | Quarterly |
| **Online courses** | Ongoing |
| **Code reviews** | Continuous |
| **Security newsletters** | Weekly |
| **Conferences** | Annually |

## Tools for OWASP Top 10

### SAST (Static Application Security Testing)

| Tool | Description | Pricing |
|-------|-------------|---------|
| **SonarQube** | Code quality + security | Free/$ |
| **Checkmarx** | Enterprise SAST | $$$ |
| **Fortify** | Enterprise SAST | $$$ |
| **Semgrep** | Open-source SAST | Free |

### DAST (Dynamic Application Security Testing)

| Tool | Description | Pricing |
|-------|-------------|---------|
| **OWASP ZAP** | Free DAST tool | Free |
| **Burp Suite** | Professional DAST | $$$ |
| **Acunetix** | Web vulnerability scanner | $$$ |
| **Netsparker** | Web vulnerability scanner | $$$ |

### Dependency Scanning

| Tool | Description | Pricing |
|-------|-------------|---------|
| **Snyk** | Dependency vulnerability scanner | Free/$ |
| **Dependabot** | GitHub dependency scanning | Free |
| **WhiteSource** | Dependency scanning | $$ |
| **npm audit** | Node.js dependency scanning | Free |

## Real Vulnerability Examples

### Example 1: SQL Injection in Login Form

**Vulnerable Code**:
```javascript
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    const user = await db.query(query);
    // SQL injection possible!
});
```

**Attack**:
```
username: ' OR '1'='1
password: anything
```

**Fix**:
```javascript
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const query = 'SELECT * FROM users WHERE username = $1 AND password = $2';
    const user = await db.query(query, [username, password]);
    // Safe!
});
```

### Example 2: XSS in Comment Section

**Vulnerable Code**:
```javascript
app.get('/comments', async (req, res) => {
    const comments = await db.query('SELECT * FROM comments');
    res.render('comments', { comments }); // No escaping!
});
```

**Attack**:
```
<script>alert('XSS')</script>
```

**Fix**:
```javascript
app.get('/comments', async (req, res) => {
    const comments = await db.query('SELECT * FROM comments');
    res.render('comments', { comments }); // Template engine auto-escapes
});
```

### Example 3: Broken Access Control in API

**Vulnerable Code**:
```javascript
app.get('/api/user/:id', async (req, res) => {
    const user = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
    res.json(user); // No authorization check!
});
```

**Attack**:
```
GET /api/user/123  // Access user 123's data as user 456
```

**Fix**:
```javascript
app.get('/api/user/:id', async (req, res) => {
    if (req.params.id !== req.user.id && !req.user.isAdmin) {
        return res.status(403).json({ error: 'Forbidden' });
    }
    const user = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
    res.json(user);
});
```

## Summary Checklist

### Before Development

- [ ] Understand OWASP Top 10
- [ ] Learn secure coding practices
- [ ] Set up security tools
- [ ] Review threat model

### During Development

- [ ] Validate all input
- [ ] Use parameterized queries
- [ ] Implement auth/authz
- [ ] Add logging
- [ ] Use security headers

### Before Deployment

- [ ] Run SAST scan
- [ ] Run DAST scan
- [ ] Check dependencies
- [ ] Review configuration
- [ ] Test security
```

---

## Quick Start

### OWASP Top 10 (2021) Overview

1. **A01: Broken Access Control** - Validate authorization
2. **A02: Cryptographic Failures** - Use strong encryption
3. **A03: Injection** - Use parameterized queries
4. **A04: Insecure Design** - Security by design
5. **A05: Security Misconfiguration** - Secure defaults
6. **A06: Vulnerable Components** - Update dependencies
7. **A07: Authentication Failures** - Strong authentication
8. **A08: Software and Data Integrity** - Verify integrity
9. **A09: Security Logging Failures** - Comprehensive logging
10. **A10: SSRF** - Validate server requests

### Prevent Injection

```javascript
// ❌ Bad - SQL injection
const query = `SELECT * FROM users WHERE id = ${userId}`

// ✅ Good - Parameterized query
const query = 'SELECT * FROM users WHERE id = ?'
db.query(query, [userId])
```

---

## Production Checklist

- [ ] **Access Control**: Validate all authorization checks
- [ ] **Encryption**: Use strong encryption for sensitive data
- [ ] **Parameterized Queries**: Prevent injection attacks
- [ ] **Security Design**: Security by design principles
- [ ] **Configuration**: Secure default configurations
- [ ] **Dependencies**: Keep dependencies updated
- [ ] **Authentication**: Strong authentication mechanisms
- [ ] **Integrity**: Verify software and data integrity
- [ ] **Logging**: Comprehensive security logging
- [ ] **SSRF Protection**: Validate server-side requests
- [ ] **Security Testing**: Regular security scans
- [ ] **Training**: Team security training

---

## Anti-patterns

### ❌ Don't: Broken Access Control

```javascript
// ❌ Bad - No authorization check
app.get('/api/users/:id', (req, res) => {
  const user = db.getUser(req.params.id)  // Anyone can access!
  res.json(user)
})
```

```javascript
// ✅ Good - Authorization check
app.get('/api/users/:id', authenticate, (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' })
  }
  const user = db.getUser(req.params.id)
  res.json(user)
})
```

### ❌ Don't: SQL Injection

```javascript
// ❌ Bad - String concatenation
const query = `SELECT * FROM users WHERE email = '${email}'`
```

```javascript
// ✅ Good - Parameterized query
const query = 'SELECT * FROM users WHERE email = ?'
db.query(query, [email])
```

---

## Integration Points

- **Secure Coding** (`24-security-practices/secure-coding/`) - Secure coding practices
- **Security Audit** (`24-security-practices/security-audit/`) - Security reviews
- **Vulnerability Management** (`24-security-practices/vulnerability-management/`) - Vulnerability handling

---

## Further Reading

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### After Deployment

- [ ] Monitor logs
- [ ] Set up alerts
- [ ] Regular security scans
- [ ] Stay updated on vulnerabilities
- [ ] Incident response plan ready
