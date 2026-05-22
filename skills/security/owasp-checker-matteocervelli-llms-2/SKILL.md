---
name: owasp-checker
description: Verify compliance with OWASP Top 10 2021 security standards. Use when
  performing OWASP compliance checks and security certification.
allowed-tools: Read, Grep, Glob, Bash
---

# OWASP Top 10 Checker Skill

## Purpose

This skill provides systematic verification of application compliance with the OWASP Top 10 2021 security standards, ensuring comprehensive security coverage across all critical categories.

## When to Use

- Final security validation before deployment
- Security certification and compliance
- Security audit preparation
- Post-remediation verification
- Quarterly security reviews
- Pre-release security checklist

## OWASP Top 10 2021 Compliance Workflow

### A01:2021 - Broken Access Control

**Risk**: Users can act outside of their intended permissions

**Compliance Checks:**

**1. Authorization Enforcement:**
```bash
# Check for authorization decorators/middleware
grep -r "@requires_auth\|@login_required\|@permission_required" src/
grep -r "auth_required\|check_permission" src/

# Find routes without authorization
grep -r "@app.route\|@router.get\|@router.post" src/ --include="*.py" -A 5
```

**Checklist:**
- [ ] Authorization enforced on every endpoint
- [ ] Default deny access control
- [ ] Server-side authorization (not client-side only)
- [ ] Authorization checked on every request
- [ ] Role-based access control (RBAC) implemented
- [ ] Ownership verified for object access

**2. Insecure Direct Object References (IDOR):**
```bash
# Look for direct ID usage from requests
grep -r "request.*\['id'\]\|request.*\.id\|params\['id'\]" src/
```

**Checklist:**
- [ ] No direct object references without validation
- [ ] Ownership verified before access
- [ ] Indirect references used (e.g., session-based)
- [ ] UUID instead of sequential IDs where applicable

**3. CORS Configuration:**
```bash
# Check CORS settings
grep -r "Access-Control-Allow-Origin" src/ config/
grep -r "CORS.*origin" src/ --include="*.py" --include="*.js"
```

**Checklist:**
- [ ] No wildcard (*) CORS unless absolutely necessary
- [ ] Specific origin whitelist configured
- [ ] Credentials mode properly configured
- [ ] Preflight requests handled correctly

**4. Disable Directory Listing:**
```bash
# Check web server config
grep -r "autoindex\|directory.*listing" config/
```

**Checklist:**
- [ ] Directory listing disabled
- [ ] .git directory not accessible
- [ ] Backup files not accessible

**Status**: ☐ Pass ☐ Fail

---

### A02:2021 - Cryptographic Failures

**Risk**: Sensitive data exposed due to weak or missing encryption

**Compliance Checks:**

**1. Data in Transit:**
```bash
# Check TLS enforcement
grep -r "SECURE_SSL_REDIRECT\|HTTPS_ONLY\|ssl.*required" config/ src/
grep -r "tls.*version\|ssl.*version" config/

# Check for HTTP usage
grep -r "http://\|ws://" src/ | grep -v "localhost\|127.0.0.1"
```

**Checklist:**
- [ ] TLS 1.2+ enforced
- [ ] TLS 1.0/1.1 disabled
- [ ] HTTPS redirect configured
- [ ] HSTS header set (max-age >= 31536000)
- [ ] Secure WebSocket (wss://) for real-time
- [ ] Certificate validation enabled

**2. Data at Rest:**
```bash
# Check for encryption of sensitive data
grep -r "encrypt\|cipher\|AES" src/
grep -r "password.*plain\|password.*clear" src/
```

**Checklist:**
- [ ] Passwords hashed (bcrypt/argon2/scrypt)
- [ ] PII encrypted at rest
- [ ] Database encryption enabled for sensitive columns
- [ ] Backups encrypted
- [ ] Key management system used

**3. Weak Cryptography:**
```bash
# Find weak algorithms
grep -r "md5\|sha1\|DES\|RC4" src/ --include="*.py" --include="*.js"
grep -r "ECB.*mode" src/
```

**Checklist:**
- [ ] No MD5/SHA1 for security (only for checksums)
- [ ] AES-256-GCM or ChaCha20-Poly1305 for encryption
- [ ] Argon2id or bcrypt for passwords
- [ ] SHA-256/SHA-3 for hashing
- [ ] Proper IV/nonce generation
- [ ] No ECB mode

**4. Random Number Generation:**
```bash
# Check RNG usage
grep -r "random\.random\|Math\.random" src/
grep -r "secrets\|os\.urandom\|crypto\.randomBytes" src/
```

**Checklist:**
- [ ] Cryptographically secure RNG (secrets, os.urandom)
- [ ] No Math.random() or random.random() for security
- [ ] Sufficient entropy for keys/tokens

**Status**: ☐ Pass ☐ Fail

---

### A03:2021 - Injection

**Risk**: Untrusted data sent to interpreter as command/query

**Compliance Checks:**

**1. SQL Injection Prevention:**
```bash
# Find string concatenation in SQL
grep -r "execute.*%\|execute.*\+\|execute.*format\|execute.*f\"" src/ --include="*.py"
grep -r "SELECT.*\+\|INSERT.*\+\|UPDATE.*\+\|DELETE.*\+" src/
```

**Checklist:**
- [ ] Parameterized queries/prepared statements
- [ ] ORM used correctly (no raw SQL with user input)
- [ ] No string concatenation in SQL
- [ ] Input validation on all parameters
- [ ] Least privilege database accounts

**2. Command Injection Prevention:**
```bash
# Find shell command execution
grep -r "subprocess.*shell=True\|os\.system\|os\.popen" src/ --include="*.py"
grep -r "exec\|eval\|child_process" src/ --include="*.js"
```

**Checklist:**
- [ ] No shell=True with user input
- [ ] Command arguments as list, not string
- [ ] Input validation/sanitization
- [ ] Whitelist allowed commands
- [ ] No eval() or exec() with user input

**3. LDAP Injection:**
```bash
grep -r "ldap.*search\|ldap.*filter" src/
```

**Checklist:**
- [ ] LDAP queries parameterized
- [ ] Special characters escaped
- [ ] Input validation

**4. NoSQL Injection:**
```bash
grep -r "find.*\$where\|\.exec(" src/ --include="*.js"
```

**Checklist:**
- [ ] MongoDB operators sanitized
- [ ] $where clauses avoided or validated
- [ ] Input type validation

**5. Template Injection:**
```bash
grep -r "render_template_string\|Jinja2.*from_string" src/
grep -r "autoescape.*False" src/
```

**Checklist:**
- [ ] No user input in template compilation
- [ ] Auto-escaping enabled
- [ ] Safe template rendering

**Status**: ☐ Pass ☐ Fail

---

### A04:2021 - Insecure Design

**Risk**: Missing or ineffective security controls in design

**Compliance Checks:**

**1. Threat Modeling:**

**Checklist:**
- [ ] Threat model documented
- [ ] Attack surface analyzed
- [ ] Trust boundaries identified
- [ ] Data flow diagrams created
- [ ] Security requirements defined

**2. Security Design Patterns:**

**Checklist:**
- [ ] Defense in depth implemented
- [ ] Fail securely (errors don't expose data)
- [ ] Least privilege principle
- [ ] Separation of duties
- [ ] Complete mediation (check every access)

**3. Rate Limiting:**
```bash
grep -r "rate.*limit\|throttle" src/ config/
```

**Checklist:**
- [ ] Rate limiting on authentication endpoints
- [ ] Rate limiting on API endpoints
- [ ] Account lockout after failed attempts
- [ ] CAPTCHA for public forms

**4. Business Logic:**

**Checklist:**
- [ ] Transaction integrity enforced
- [ ] Workflow state validated
- [ ] Resource limits defined
- [ ] Input bounds checked
- [ ] Edge cases handled

**Status**: ☐ Pass ☐ Fail

---

### A05:2021 - Security Misconfiguration

**Risk**: Insecure default configurations, incomplete setups

**Compliance Checks:**

**1. Security Headers:**
```bash
# Check for security headers
grep -r "X-Frame-Options\|X-Content-Type-Options\|Content-Security-Policy" src/ config/
grep -r "Strict-Transport-Security\|X-XSS-Protection" src/ config/
```

**Checklist:**
- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] X-Content-Type-Options: nosniff
- [ ] Content-Security-Policy configured
- [ ] Strict-Transport-Security: max-age=31536000
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Referrer-Policy: strict-origin-when-cross-origin

**2. Error Handling:**
```bash
# Check debug mode
grep -r "DEBUG.*True\|development.*mode" config/ src/
grep -r "traceback\|stack.*trace" src/
```

**Checklist:**
- [ ] Debug mode disabled in production
- [ ] Generic error messages to users
- [ ] Detailed errors logged, not displayed
- [ ] No stack traces exposed
- [ ] Custom error pages configured

**3. Default Credentials:**
```bash
# Find hardcoded credentials
grep -r "password.*=.*admin\|password.*=.*password" src/ config/
```

**Checklist:**
- [ ] All default credentials changed
- [ ] No hardcoded passwords
- [ ] Credentials in environment variables
- [ ] Secrets management system used

**4. Unnecessary Features:**
```bash
# Check for sample/test code
find . -name "*sample*" -o -name "*test*" -o -name "*demo*" | grep -v node_modules
```

**Checklist:**
- [ ] Sample code removed
- [ ] Unused endpoints disabled
- [ ] Test accounts removed
- [ ] Development tools disabled in production
- [ ] Unnecessary services stopped

**5. Missing Patches:**
```bash
# Check dependency status
pip list --outdated 2>/dev/null || npm outdated 2>/dev/null
```

**Checklist:**
- [ ] Dependencies up to date
- [ ] Security patches applied
- [ ] Regular update schedule
- [ ] Vulnerability monitoring enabled

**Status**: ☐ Pass ☐ Fail

---

### A06:2021 - Vulnerable and Outdated Components

**Risk**: Using components with known vulnerabilities

**Compliance Checks:**

**1. Dependency Inventory:**
```bash
# List all dependencies
pip list --format=json > dependencies.json 2>/dev/null || npm list --json > dependencies.json 2>/dev/null
```

**Checklist:**
- [ ] Complete dependency inventory (SBOM)
- [ ] Direct and transitive dependencies tracked
- [ ] License compliance verified
- [ ] Dependency sources trusted

**2. Vulnerability Scanning:**
```bash
# Scan for vulnerabilities
pip-audit --format json 2>/dev/null || npm audit --json 2>/dev/null
safety check --json 2>/dev/null
```

**Checklist:**
- [ ] Regular vulnerability scans (weekly minimum)
- [ ] No critical vulnerabilities
- [ ] High vulnerabilities remediated
- [ ] Vulnerability remediation SLA defined

**3. Version Management:**
```bash
# Check for version pinning
cat requirements.txt setup.py package.json 2>/dev/null
```

**Checklist:**
- [ ] Versions pinned in lockfiles
- [ ] Compatible version ranges defined
- [ ] Regular updates scheduled
- [ ] Breaking changes reviewed before update

**4. Component Retirement:**

**Checklist:**
- [ ] No unmaintained dependencies
- [ ] EOL software replaced
- [ ] Deprecated features not used
- [ ] Migration plan for aging components

**Status**: ☐ Pass ☐ Fail

---

### A07:2021 - Identification and Authentication Failures

**Risk**: Weak authentication allows impersonation

**Compliance Checks:**

**1. Password Policy:**
```bash
# Check password requirements
grep -r "password.*length\|password.*complexity" src/
grep -r "MIN_PASSWORD_LENGTH\|PASSWORD_VALIDATORS" config/ src/
```

**Checklist:**
- [ ] Minimum 8 characters (12+ recommended)
- [ ] Complexity requirements enforced
- [ ] Common passwords blocked
- [ ] Password strength meter implemented
- [ ] Password history (no reuse)

**2. Multi-Factor Authentication:**
```bash
grep -r "mfa\|2fa\|totp\|two.*factor" src/
```

**Checklist:**
- [ ] MFA available for sensitive operations
- [ ] MFA enforced for admin accounts
- [ ] TOTP/hardware token support
- [ ] Backup codes provided

**3. Session Management:**
```bash
# Check session configuration
grep -r "SESSION.*TIMEOUT\|session.*expir" config/ src/
grep -r "SESSION_COOKIE_SECURE\|SESSION_COOKIE_HTTPONLY" config/ src/
```

**Checklist:**
- [ ] Session timeout configured (15-30 min idle)
- [ ] Absolute session timeout (e.g., 8 hours)
- [ ] Session invalidated on logout
- [ ] Secure session cookies (Secure, HttpOnly, SameSite)
- [ ] Session fixation prevented (regenerate on login)
- [ ] Concurrent session limits

**4. Credential Storage:**
```bash
# Check password hashing
grep -r "bcrypt\|argon2\|scrypt\|pbkdf2" src/
grep -r "hashlib\.md5.*password\|hashlib\.sha1.*password" src/
```

**Checklist:**
- [ ] Passwords hashed with bcrypt/argon2/scrypt
- [ ] Salt unique per password
- [ ] Work factor appropriate (bcrypt: 12+, argon2: per OWASP)
- [ ] No reversible encryption for passwords

**5. Account Enumeration:**
```bash
# Check error messages
grep -r "user.*not.*found\|invalid.*username" src/
```

**Checklist:**
- [ ] Generic authentication errors ("Invalid credentials")
- [ ] Same response time for valid/invalid users
- [ ] Password reset doesn't confirm email existence
- [ ] Registration doesn't confirm email existence

**6. Brute Force Protection:**
```bash
grep -r "login.*attempt\|failed.*attempt\|account.*lock" src/
```

**Checklist:**
- [ ] Account lockout after N failed attempts (5-10)
- [ ] Temporary lockout (not permanent)
- [ ] Rate limiting on login endpoint
- [ ] CAPTCHA after failed attempts
- [ ] Login attempt logging

**Status**: ☐ Pass ☐ Fail

---

### A08:2021 - Software and Data Integrity Failures

**Risk**: Code and infrastructure not protected from integrity violations

**Compliance Checks:**

**1. Insecure Deserialization:**
```bash
# Check for unsafe deserialization
grep -r "pickle\.loads\|yaml\.load\(" src/ --include="*.py"
grep -r "eval\|unserialize" src/
```

**Checklist:**
- [ ] No pickle with untrusted data
- [ ] yaml.safe_load() used (not yaml.load())
- [ ] JSON preferred over pickle
- [ ] Deserialization input validated
- [ ] No eval() with untrusted data

**2. CI/CD Pipeline Security:**

**Checklist:**
- [ ] Pipeline configuration in version control
- [ ] Code signing for releases
- [ ] Secret scanning in CI/CD
- [ ] Dependency verification
- [ ] Build reproducibility
- [ ] Artifact signing
- [ ] Deployment approval process

**3. Update Mechanism:**

**Checklist:**
- [ ] Updates delivered over HTTPS
- [ ] Update signatures verified
- [ ] Automatic updates signed
- [ ] Rollback mechanism available
- [ ] Update integrity checked

**4. Supply Chain Security:**

**Checklist:**
- [ ] Dependencies from trusted sources
- [ ] Dependency hash verification
- [ ] Software Bill of Materials (SBOM)
- [ ] Third-party code reviewed
- [ ] Vendor security assessment

**Status**: ☐ Pass ☐ Fail

---

### A09:2021 - Security Logging and Monitoring Failures

**Risk**: Breaches not detected, incidents not responded to

**Compliance Checks:**

**1. Security Event Logging:**
```bash
# Check logging implementation
grep -r "logging\|logger\|log\." src/ --include="*.py" --include="*.js"
grep -r "audit.*log\|security.*log" src/
```

**Checklist:**
- [ ] Authentication events logged (success/failure)
- [ ] Authorization failures logged
- [ ] Input validation failures logged
- [ ] Sensitive operations logged
- [ ] Administrative actions logged
- [ ] Access to sensitive data logged

**2. Log Content:**

**Checklist:**
- [ ] Timestamp (UTC)
- [ ] User/session identifier
- [ ] Action performed
- [ ] Resource accessed
- [ ] Source IP address
- [ ] Outcome (success/failure)
- [ ] No sensitive data in logs (passwords, tokens, PII)

**3. Log Protection:**
```bash
# Check log file permissions
find . -name "*.log" -ls 2>/dev/null
```

**Checklist:**
- [ ] Log files write-only for application
- [ ] Logs protected from tampering
- [ ] Logs rotated regularly
- [ ] Log retention policy defined
- [ ] Logs backed up
- [ ] Centralized logging implemented

**4. Monitoring and Alerting:**

**Checklist:**
- [ ] Real-time security monitoring
- [ ] Automated alerting configured
- [ ] Failed login threshold alerts
- [ ] Unusual activity detection
- [ ] Anomaly detection
- [ ] Security dashboard available

**5. Incident Response:**

**Checklist:**
- [ ] Incident response plan documented
- [ ] Response team identified
- [ ] Alert escalation procedures
- [ ] Incident logging and tracking
- [ ] Post-incident review process

**Status**: ☐ Pass ☐ Fail

---

### A10:2021 - Server-Side Request Forgery (SSRF)

**Risk**: Application fetches remote resources without validating user-supplied URL

**Compliance Checks:**

**1. URL Validation:**
```bash
# Find URL fetching code
grep -r "requests\.get\|urllib\.request\|fetch\|axios\.get" src/
grep -r "url.*request\|user.*url" src/
```

**Checklist:**
- [ ] User-supplied URLs validated
- [ ] URL whitelist implemented
- [ ] Protocol whitelist (HTTP/HTTPS only)
- [ ] Private IP ranges blocked
- [ ] DNS rebinding protection
- [ ] URL redirection limited

**2. Network Segmentation:**

**Checklist:**
- [ ] Application in DMZ
- [ ] Internal services not accessible from app
- [ ] Firewall rules deny by default
- [ ] Outbound traffic restricted
- [ ] Service mesh/network policies configured

**3. Input Validation:**
```bash
# Check for URL sanitization
grep -r "validate.*url\|sanitize.*url\|parse.*url" src/
```

**Checklist:**
- [ ] URL parsing and validation
- [ ] Hostname validation
- [ ] Port restrictions
- [ ] Path normalization
- [ ] No file:// protocol
- [ ] No access to metadata services (169.254.169.254)

**Status**: ☐ Pass ☐ Fail

---

## Overall Compliance Report Format

```markdown
# OWASP Top 10 2021 Compliance Report

**Date**: [YYYY-MM-DD]
**Application**: [name]
**Assessed By**: OWASP Checker

## Compliance Summary

| Category | Status | Critical Issues | Notes |
|----------|--------|-----------------|-------|
| A01 - Broken Access Control | ✅/⚠️/❌ | [count] | [summary] |
| A02 - Cryptographic Failures | ✅/⚠️/❌ | [count] | [summary] |
| A03 - Injection | ✅/⚠️/❌ | [count] | [summary] |
| A04 - Insecure Design | ✅/⚠️/❌ | [count] | [summary] |
| A05 - Security Misconfiguration | ✅/⚠️/❌ | [count] | [summary] |
| A06 - Vulnerable Components | ✅/⚠️/❌ | [count] | [summary] |
| A07 - Auth Failures | ✅/⚠️/❌ | [count] | [summary] |
| A08 - Integrity Failures | ✅/⚠️/❌ | [count] | [summary] |
| A09 - Logging Failures | ✅/⚠️/❌ | [count] | [summary] |
| A10 - SSRF | ✅/⚠️/❌ | [count] | [summary] |

**Legend**:
- ✅ Pass: Fully compliant
- ⚠️ Partial: Some issues, not critical
- ❌ Fail: Critical issues found

**Overall Compliance**: [XX]% ([X]/10 categories passed)

## Critical Findings

[List all critical non-compliance items that must be fixed]

## Recommendations

### Immediate (Critical)
1. [Item]

### Short-term (High)
1. [Item]

### Long-term (Medium)
1. [Item]

## Certification

This application [IS / IS NOT] compliant with OWASP Top 10 2021 standards.

**Assessor**: [name]
**Date**: [YYYY-MM-DD]
**Next Assessment**: [YYYY-MM-DD]
```

---

## Best Practices

**Assessment Process:**
- Complete all categories
- Document evidence for each check
- Retest after remediation
- Keep assessment current (quarterly)

**Compliance Tracking:**
- Track compliance over time
- Maintain compliance dashboard
- Regular reassessment (quarterly)
- Update after major changes

**Remediation:**
- Fix critical items immediately
- Schedule high/medium items
- Document compensating controls
- Verify fixes effectiveness

**Documentation:**
- Keep detailed compliance records
- Document exceptions with justification
- Track remediation progress
- Maintain audit trail

---

## Integration with Security Workflow

**Input**: Implemented and tested application
**Process**: Systematic OWASP Top 10 compliance verification
**Output**: Compliance report with certification status
**Next Step**: Security certification or deployment approval

---

## Remember

- **Compliance is not security**: OWASP Top 10 is baseline, not complete security
- **Context matters**: Adapt checks to your application type
- **Defense in depth**: Multiple layers of controls
- **Continuous compliance**: Not a one-time check
- **Document everything**: Maintain audit trail
- **Stay current**: OWASP Top 10 updates periodically

Your goal is to ensure applications meet OWASP Top 10 security standards and maintain compliance over time.