---
name: Security Architect
description: Comprehensive security architecture combining threat modeling, security-first design, secure coding review, and compliance validation. Consolidated from threat-modeling, security-first-design, secure-coding-review, and compliance-validator.
version: 1.0.0
category: security
triggers:
  - 'security-architect'
  - 'security architect'
  - 'threat modeling'
  - 'security design'
  - 'secure coding'
  - 'compliance validation'
dependencies:
  required_mcps: []
  required_tools: []
  required_integrations: []
---

# Security Architect

## Overview

Security Architect is a consolidated skill that covers the complete security lifecycle: threat modeling, secure design principles, secure coding practices, and regulatory compliance. It ensures security is integrated from the start, not bolted on at the end.

**Consolidated from:**

- **threat-modeling** - STRIDE threat analysis and risk assessment
- **security-first-design** - Security principles and secure design patterns
- **secure-coding-review** - OWASP Top 10 and vulnerability detection
- **compliance-validator** - GDPR, HIPAA, SOC2, PCI-DSS compliance

## When to Use This Skill

Use Security Architect when:

- Starting a new project (design phase)
- Conducting security architecture review
- Reviewing code for security vulnerabilities
- Ensuring regulatory compliance
- Responding to security incidents
- Planning for security certifications (SOC2, ISO 27001)
- Designing authentication and authorization systems

## Key Capabilities

### Threat Modeling (from threat-modeling)

- Apply STRIDE methodology for threat identification
- Assess risk levels (Likelihood × Impact)
- Create threat models and mitigation plans
- Identify attack surfaces and trust boundaries

### Security Design (from security-first-design)

- Apply security principles (Defense in Depth, Least Privilege, Zero Trust)
- Design secure authentication and authorization
- Implement encryption and key management
- Design secure APIs and data protection

### Secure Coding (from secure-coding-review)

- Review code against OWASP Top 10
- Detect injection vulnerabilities (SQL, XSS, command)
- Identify broken authentication and access control
- Ensure secure data handling and validation

### Compliance (from compliance-validator)

- Ensure GDPR, HIPAA, CCPA, SOC2, PCI-DSS compliance
- Implement data subject rights (access, erasure, portability)
- Design audit logging and retention policies
- Configure encryption and access controls

## Workflow

### Part 1: Threat Modeling (STRIDE)

#### STRIDE Framework

**S - Spoofing (Authentication)**

- **Threat:** Attacker impersonates a user or system
- **Examples:**
  - Stolen credentials
  - Session hijacking
  - Weak or no authentication
- **Mitigations:**
  - Multi-factor authentication (MFA)
  - Strong password policies
  - JWT with short expiration
  - Secure session management

**T - Tampering (Integrity)**

- **Threat:** Attacker modifies data or code
- **Examples:**
  - SQL injection
  - Man-in-the-middle attacks
  - Parameter manipulation
  - Code injection
- **Mitigations:**
  - Input validation and sanitization
  - HTTPS/TLS everywhere
  - Signed tokens (JWT)
  - Integrity checks (hashing)

**R - Repudiation (Accountability)**

- **Threat:** User denies performing an action
- **Examples:**
  - No audit logs
  - Unsigned transactions
  - Anonymous actions
- **Mitigations:**
  - Comprehensive audit logging
  - Digital signatures for transactions
  - Immutable log storage
  - User action tracking

**I - Information Disclosure (Confidentiality)**

- **Threat:** Sensitive data exposed to unauthorized parties
- **Examples:**
  - Exposed API keys
  - Database dumps
  - Verbose error messages
  - Insufficient access controls
- **Mitigations:**
  - Encryption at rest and in transit
  - Principle of least privilege
  - Secure secret management (AWS Secrets Manager, Vault)
  - Role-based access control (RBAC)

**D - Denial of Service (Availability)**

- **Threat:** System becomes unavailable to legitimate users
- **Examples:**
  - DDoS attacks
  - Resource exhaustion
  - Unhandled exceptions
- **Mitigations:**
  - Rate limiting and throttling
  - Input validation (reject massive payloads)
  - Auto-scaling infrastructure
  - CDN and DDoS protection (Cloudflare)

**E - Elevation of Privilege (Authorization)**

- **Threat:** User gains unauthorized access to higher privileges
- **Examples:**
  - Broken access control
  - Insecure direct object references (IDOR)
  - Missing authorization checks
- **Mitigations:**
  - Authorization checks on every request
  - Principle of least privilege
  - Attribute-based access control (ABAC)
  - Regular permission audits

---

#### Threat Modeling Process

**Step 1: Identify Assets**

- User data (PII, passwords, financial info)
- Business data (IP, customer lists, transactions)
- System credentials (API keys, certificates)
- Infrastructure (servers, databases, APIs)

**Step 2: Identify Trust Boundaries**

- User ↔ Web App
- Web App ↔ API
- API ↔ Database
- Internal services ↔ External APIs
- Admin ↔ Production systems

**Step 3: Apply STRIDE to Each Boundary**
For each boundary, ask:

- **S:** Can an attacker spoof identity?
- **T:** Can data be tampered with?
- **R:** Can actions be repudiated?
- **I:** Can information be disclosed?
- **D:** Can service be denied?
- **E:** Can privileges be elevated?

**Step 4: Assess Risk**

```
Risk = Likelihood × Impact

Likelihood:
- High (likely to occur)
- Medium (may occur)
- Low (unlikely to occur)

Impact:
- Critical (data breach, financial loss, legal liability)
- High (significant damage, downtime)
- Medium (limited damage, temporary disruption)
- Low (minimal impact)

Risk Level:
- Critical: Immediate action required
- High: Address before launch
- Medium: Address post-launch
- Low: Monitor, may accept risk
```

**Step 5: Define Mitigations**
For each threat, document:

- Mitigation strategy
- Implementation effort (low, medium, high)
- Residual risk after mitigation
- Owner and timeline

---

### Part 2: Security-First Design

#### Security Principles

**1. Defense in Depth**
Multiple layers of security controls. If one fails, others still protect.

**Example:**

- Layer 1: Firewall
- Layer 2: Authentication
- Layer 3: Authorization
- Layer 4: Encryption
- Layer 5: Audit logs

**2. Least Privilege**
Users/systems only have minimum permissions needed.

**Example:**

- Read-only database credentials for reporting service
- User can only see their own data
- Admin access requires MFA + time-limited token

**3. Zero Trust**
Never trust, always verify. Even internal networks are untrusted.

**Example:**

- Every request authenticated and authorized
- No "trusted" internal network
- Encrypt internal traffic
- Assume breach mentality

**4. Secure by Default**
Default configuration is secure. Users must opt-in to less secure options.

**Example:**

- HTTPS enforced by default
- Strict password policy by default
- MFA recommended on signup
- Secure cookies (HttpOnly, Secure, SameSite)

**5. Fail Securely**
When errors occur, fail in a way that doesn't compromise security.

**Example:**

- Access denied on error (not granted)
- Log error but don't expose details to user
- Graceful degradation without exposing internals

---

#### Secure Design Patterns

**Authentication:**

- **Pattern:** OAuth 2.0 + OpenID Connect (OIDC)
- **Implementation:**
  - Use Auth0, AWS Cognito, or Okta (don't build your own)
  - JWT tokens with short expiration (15 min access, 7 day refresh)
  - Secure token storage (HttpOnly cookies or secure local storage)
  - MFA for sensitive operations

**Authorization:**

- **Pattern:** Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC)
- **Implementation:**
  - Define roles: admin, user, viewer
  - Check authorization on every API request
  - Use middleware: `@requireRole('admin')`
  - Implement IDOR protection (verify ownership)

**Data Protection:**

- **Pattern:** Encryption at rest and in transit
- **Implementation:**
  - TLS 1.3 for all external traffic
  - AES-256 for data at rest
  - Key management service (AWS KMS, Google Cloud KMS)
  - Encrypt PII fields (email, SSN, credit cards)

**API Security:**

- **Pattern:** Rate limiting + authentication + input validation
- **Implementation:**
  - Rate limit: 100 requests/minute per user
  - API keys for server-to-server
  - OAuth tokens for user-to-server
  - Validate all inputs (type, length, format)
  - Whitelist allowed values

**Secrets Management:**

- **Pattern:** Never commit secrets, use secret managers
- **Implementation:**
  - AWS Secrets Manager or HashiCorp Vault
  - Environment variables for config (never in code)
  - Rotate secrets regularly (90 days)
  - Use IAM roles (not long-lived credentials)

---

### Part 3: Secure Coding Review (OWASP Top 10)

#### OWASP Top 10 (2021)

**A01: Broken Access Control**

- **Risk:** Users access data/functions they shouldn't
- **Examples:**
  - URL tampering: `/user/123` → `/user/456`
  - Missing authorization checks
  - Insecure Direct Object References (IDOR)

**How to Detect:**

```javascript
// BAD: No authorization check
app.get('/api/users/:id', (req, res) => {
  const user = db.users.findById(req.params.id)
  res.json(user) // Anyone can see any user!
})

// GOOD: Check ownership
app.get('/api/users/:id', authMiddleware, (req, res) => {
  const requestedId = req.params.id
  const currentUserId = req.user.id

  if (requestedId !== currentUserId && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' })
  }

  const user = db.users.findById(requestedId)
  res.json(user)
})
```

---

**A02: Cryptographic Failures**

- **Risk:** Sensitive data exposed due to weak or missing encryption
- **Examples:**
  - Plaintext passwords in database
  - HTTP instead of HTTPS
  - Weak hashing (MD5, SHA1)

**How to Detect:**

```javascript
// BAD: Plaintext password
const user = { email, password: req.body.password }
db.users.create(user)

// GOOD: Hash with bcrypt
const bcrypt = require('bcrypt')
const hashedPassword = await bcrypt.hash(req.body.password, 10)
const user = { email, password: hashedPassword }
db.users.create(user)
```

---

**A03: Injection**

- **Risk:** Attacker injects malicious code (SQL, XSS, command)
- **Examples:**
  - SQL injection
  - Cross-site scripting (XSS)
  - Command injection

**How to Detect:**

```javascript
// BAD: SQL Injection
const query = `SELECT * FROM users WHERE email = '${req.body.email}'`
db.query(query) // Attacker can send: ' OR '1'='1

// GOOD: Parameterized query
const query = 'SELECT * FROM users WHERE email = ?'
db.query(query, [req.body.email])

// BAD: XSS
;<div dangerouslySetInnerHTML={{ __html: userInput }} />

// GOOD: Escape user input
import DOMPurify from 'dompurify'
const sanitized = DOMPurify.sanitize(userInput)
;<div dangerouslySetInnerHTML={{ __html: sanitized }} />
```

---

**A04: Insecure Design**

- **Risk:** Flawed architecture or missing security controls
- **Examples:**
  - No rate limiting
  - Lack of threat modeling
  - No security requirements

**How to Detect:**

- Review architecture diagram
- Check for rate limiting, authentication, authorization
- Validate threat model exists

---

**A05: Security Misconfiguration**

- **Risk:** Default configs, verbose errors, unnecessary features enabled
- **Examples:**
  - Default admin password
  - Directory listing enabled
  - Stack traces in production

**How to Detect:**

```javascript
// BAD: Exposes stack trace
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack })
})

// GOOD: Generic error message
app.use((err, req, res, next) => {
  logger.error(err)
  res.status(500).json({ error: 'Internal server error' })
})
```

---

**A06-A10: Other Critical Issues**

- **A06:** Vulnerable and Outdated Components (use `npm audit`, Dependabot)
- **A07:** Identification and Authentication Failures (weak passwords, no MFA)
- **A08:** Software and Data Integrity Failures (supply chain attacks)
- **A09:** Security Logging and Monitoring Failures (no audit logs)
- **A10:** Server-Side Request Forgery (SSRF) (validate URLs)

---

### Part 4: Compliance Validation

#### Regulatory Frameworks

**GDPR (General Data Protection Regulation)**

- **Scope:** EU data subjects
- **Key Requirements:**
  - Lawful basis for processing (consent, contract, legitimate interest)
  - Data subject rights (access, rectification, erasure, portability)
  - Privacy by design and default
  - Data breach notification (72 hours)
  - Data Protection Impact Assessment (DPIA) for high-risk processing

**Implementation Checklist:**

- [ ] Consent mechanism for data collection
- [ ] Data subject access request (DSAR) process
- [ ] Right to erasure ("right to be forgotten") implementation
- [ ] Data portability export (JSON/CSV)
- [ ] Privacy policy and cookie banner
- [ ] Data Processing Agreement (DPA) with vendors
- [ ] Breach notification process

---

**HIPAA (Health Insurance Portability and Accountability Act)**

- **Scope:** Healthcare data in the US
- **Key Requirements:**
  - Protected Health Information (PHI) must be encrypted
  - Access controls and audit logs
  - Business Associate Agreements (BAA)
  - Breach notification

**Implementation Checklist:**

- [ ] Encrypt PHI at rest (AES-256) and in transit (TLS 1.3)
- [ ] Role-based access control to PHI
- [ ] Audit logs for all PHI access
- [ ] BAA with cloud providers (AWS, Azure)
- [ ] Breach notification process
- [ ] Regular security risk assessments

---

**SOC 2 (Service Organization Control 2)**

- **Scope:** SaaS companies handling customer data
- **Key Requirements:**
  - Trust Service Criteria (Security, Availability, Confidentiality)
  - Access controls and monitoring
  - Change management
  - Incident response

**Implementation Checklist:**

- [ ] Security policies documented
- [ ] Background checks for employees
- [ ] Multi-factor authentication (MFA) enforced
- [ ] Encryption at rest and in transit
- [ ] Audit logging and monitoring
- [ ] Incident response plan
- [ ] Vendor management program
- [ ] Regular security training

---

**PCI-DSS (Payment Card Industry Data Security Standard)**

- **Scope:** Organizations handling credit card data
- **Key Requirements:**
  - Never store CVV/CVC codes
  - Encrypt cardholder data
  - Regularly update and patch systems
  - Restrict access to cardholder data

**Implementation Checklist:**

- [ ] Use payment processor (Stripe, Braintree) - DON'T store cards yourself
- [ ] If storing cards, use tokenization
- [ ] PCI-compliant hosting (Level 1 certified)
- [ ] Network segmentation (isolate cardholder data)
- [ ] Vulnerability scanning and penetration testing
- [ ] Strong access controls

---

## Examples

### Example 1: Threat Model for SaaS Application

**Application:** Project Management SaaS

**Assets:**

- User credentials (email, password)
- Project data (documents, tasks, comments)
- Payment information (via Stripe)
- API keys for integrations

**Trust Boundaries:**

1. User Browser ↔ Web App (HTTPS)
2. Web App ↔ API Server (internal TLS)
3. API Server ↔ Database (encrypted connection)
4. API Server ↔ Stripe API (HTTPS)

**STRIDE Analysis for Boundary 1 (User ↔ Web App):**

| Threat                       | Risk   | Mitigation                                  |
| ---------------------------- | ------ | ------------------------------------------- |
| **S:** Credential theft      | High   | MFA, password hashing (bcrypt)              |
| **T:** Session hijacking     | Medium | HttpOnly cookies, SameSite, CSRF tokens     |
| **R:** Denied action         | Low    | Audit logs for all user actions             |
| **I:** Data exposure via XSS | High   | Content Security Policy, input sanitization |
| **D:** Brute force login     | Medium | Rate limiting (5 attempts/min)              |
| **E:** Account takeover      | High   | Email verification, MFA                     |

**Priority Mitigations:**

1. Implement MFA (High risk, high impact)
2. Add rate limiting (Medium risk, easy fix)
3. Enable CSP headers (High risk, easy fix)

---

### Example 2: Secure Code Review Findings

**Code Review:** User authentication endpoint

**Findings:**

**CRITICAL: SQL Injection (A03)**

```javascript
// Current code (VULNERABLE):
const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`

// Recommended fix:
const query = 'SELECT * FROM users WHERE email = ? AND password_hash = ?'
const hashedPassword = bcrypt.hashSync(password, user.salt)
db.query(query, [email, hashedPassword])
```

**HIGH: Plaintext Passwords (A02)**

```javascript
// Current code (VULNERABLE):
db.users.create({ email, password })

// Recommended fix:
const hashedPassword = await bcrypt.hash(password, 10)
db.users.create({ email, password: hashedPassword })
```

**MEDIUM: No Rate Limiting (A04)**

```javascript
// Recommended fix:
const rateLimit = require('express-rate-limit')
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // 5 attempts
})
app.post('/login', loginLimiter, loginHandler)
```

**Action:** Fix CRITICAL and HIGH before deployment. Add MEDIUM post-launch.

---

### Example 3: GDPR Compliance Implementation

**Requirement:** Implement data subject rights

**Implementation:**

**1. Right to Access (DSAR)**

```javascript
app.get('/api/user/data-export', authMiddleware, async (req, res) => {
  const userId = req.user.id

  const userData = {
    profile: await db.users.findById(userId),
    projects: await db.projects.findByUser(userId),
    comments: await db.comments.findByUser(userId),
    activity: await db.activityLog.findByUser(userId)
  }

  res.setHeader('Content-Type', 'application/json')
  res.setHeader('Content-Disposition', 'attachment; filename=my-data.json')
  res.json(userData)
})
```

**2. Right to Erasure**

```javascript
app.delete('/api/user/account', authMiddleware, async (req, res) => {
  const userId = req.user.id

  // Anonymize instead of delete (retain for legal compliance)
  await db.users.update(userId, {
    email: `deleted-${userId}@example.com`,
    name: 'Deleted User',
    deleted_at: new Date()
  })

  // Delete PII
  await db.sessions.deleteByUser(userId)
  await db.notifications.deleteByUser(userId)

  res.json({ message: 'Account deleted successfully' })
})
```

**3. Consent Management**

```javascript
const user = {
  email,
  marketing_consent: req.body.marketingConsent || false,
  analytics_consent: req.body.analyticsConsent || false,
  consent_date: new Date()
}
```

---

## Best Practices

### Threat Modeling

1. **Model early** - Design phase, not after development
2. **Update regularly** - When architecture changes
3. **Focus on high-risk threats** - Don't aim for 100% coverage
4. **Document mitigations** - Not just threats

### Security Design

1. **Use proven solutions** - Don't roll your own crypto
2. **Defense in depth** - Multiple layers of security
3. **Secure by default** - Opt-in to less secure, not opt-out
4. **Assume breach** - Design with "when" not "if" mindset

### Secure Coding

1. **Automate security scanning** - SAST, DAST, SCA in CI/CD
2. **Validate all inputs** - Trust nothing from users
3. **Use security libraries** - OWASP, helmet.js, DOMPurify
4. **Keep dependencies updated** - Monitor with Dependabot

### Compliance

1. **Understand scope** - Which regulations apply to you
2. **Document everything** - Policies, procedures, decisions
3. **Regular audits** - Internal + external reviews
4. **Work with legal** - Don't interpret regulations alone

---

## Common Pitfalls

### 1. Security as an Afterthought

**Antipattern:** Build first, secure later
**Result:** Expensive retrofitting, vulnerabilities in production

**Better:** Integrate security from design phase

### 2. Trusting Client-Side Validation

**Antipattern:** Only validate on frontend
**Result:** Attacker bypasses with curl

**Better:** Always validate on backend

### 3. Rolling Your Own Crypto

**Antipattern:** Custom encryption or hashing
**Result:** Weak crypto, vulnerabilities

**Better:** Use proven libraries (bcrypt, libsodium)

### 4. Over-Reliance on Compliance

**Antipattern:** "We're compliant, so we're secure"
**Result:** Compliant but insecure

**Better:** Compliance is minimum; security is ongoing

### 5. Ignoring Low-Risk Threats

**Antipattern:** Only fix CRITICAL issues
**Result:** Death by a thousand cuts

**Better:** Systematically address all severity levels

---

## Related Skills

- **quality-assurance** - Security testing and validation gates
- **api-designer** - API security patterns
- **deployment-advisor** - Infrastructure security
- **framework-orchestrator** - Security in phase gates
- **data-engineer** - Data security and privacy

---

## Deliverables

When using Security Architect, produce:

1. **Threat Model**
   - Asset inventory
   - Trust boundaries
   - STRIDE analysis
   - Risk assessment
   - Mitigation plan

2. **Security Architecture Document**
   - Authentication/authorization design
   - Encryption strategy
   - Secrets management
   - Network diagram with security controls

3. **Secure Code Review Report**
   - OWASP Top 10 findings
   - Severity ratings
   - Remediation recommendations
   - Re-test results

4. **Compliance Checklist**
   - Applicable regulations
   - Implementation status
   - Gap analysis
   - Remediation plan

---

## Success Metrics

Security Architect is effective when:

- Threat models completed before development
- Zero CRITICAL vulnerabilities in production
- Security incidents <1 per year
- Compliance audits passed
- Security gates enforced in CI/CD
- Team follows secure coding practices
- Regular security training completed

---

**Remember:** Security is not a feature, it's a foundation. Build it in from the start.
