---
name: security-assessor
description: Auto-activates during requirements analysis to assess security risks
  using OWASP Top 10 framework, identify security requirements, and recommend mitigation
  strategies.
allowed-tools: Read, Grep
---

## Purpose

The **security-assessor** skill provides comprehensive security risk assessment capabilities for feature implementations. It evaluates potential security vulnerabilities using the OWASP Top 10 framework, identifies security requirements, and recommends appropriate mitigation strategies to ensure secure-by-design implementations.

## When to Use

This skill auto-activates when you:
- Assess security risks for new features
- Evaluate OWASP Top 10 compliance
- Identify security requirements
- Review authentication/authorization needs
- Analyze data security implications
- Evaluate input validation requirements
- Check for common security vulnerabilities
- Plan security testing strategies

## Provided Capabilities

### 1. OWASP Top 10 Risk Assessment
Evaluate each of the 10 critical security risks:
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

### 2. Security Requirements Identification
- Authentication requirements
- Authorization and access control
- Data encryption (at rest and in transit)
- Input validation and sanitization
- Output encoding
- Session management
- Password policies
- API security
- Secrets management

### 3. Threat Modeling
- Identify assets to protect
- Identify threat actors
- Map attack vectors
- Assess impact and likelihood
- Prioritize risks

### 4. Security Testing Strategy
- Security test cases
- Penetration testing scope
- Vulnerability scanning approach
- Security code review focus areas

## Usage Guide

### Step 1: Understand Feature Context

Read the requirements to understand:
- What data is being processed?
- Who will access this feature?
- What external systems are involved?
- What sensitive operations are performed?
- What user input is accepted?

### Step 2: OWASP Top 10 Assessment

Use `security-checklist.md` to systematically evaluate each risk:

#### 1. Broken Access Control
**Check for**:
- Are there different user roles?
- Is there privileged functionality?
- Can users access resources they shouldn't?
- Are file paths/URLs user-controllable?

**Assessment Questions**:
- [ ] Does feature involve authorization checks?
- [ ] Are there admin-only operations?
- [ ] Can users modify URLs to access others' data?
- [ ] Are API endpoints properly protected?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Implement role-based access control (RBAC)
- Use permission checks on every request
- Implement resource-level authorization
- Use indirect references (avoid exposing IDs)

#### 2. Cryptographic Failures
**Check for**:
- Is sensitive data transmitted?
- Is sensitive data stored?
- Are passwords handled?
- Are API keys/tokens used?

**Assessment Questions**:
- [ ] Is data encrypted in transit (TLS 1.3+)?
- [ ] Is sensitive data encrypted at rest?
- [ ] Are passwords hashed with strong algorithms (bcrypt, Argon2)?
- [ ] Are API keys/secrets properly secured?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Enforce TLS 1.3+ for all connections
- Use AES-256 for data at rest
- Use bcrypt (cost ≥12) or Argon2 for passwords
- Store secrets in environment variables or vaults
- Never log sensitive data

#### 3. Injection
**Check for**:
- Does feature accept user input?
- Is input used in SQL queries?
- Is input used in shell commands?
- Is input used in dynamic code evaluation?

**Assessment Questions**:
- [ ] Is user input validated and sanitized?
- [ ] Are parameterized queries used for SQL?
- [ ] Are shell commands avoided or properly escaped?
- [ ] Is eval() or similar avoided?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Use parameterized queries (never string concatenation)
- Validate all input (whitelist approach)
- Use ORM/query builders with parameter binding
- Avoid shell commands; use library functions instead
- Never use eval() or exec() with user input

#### 4. Insecure Design
**Check for**:
- Is security considered in design phase?
- Are threat models created?
- Are security patterns used?
- Is defense-in-depth applied?

**Assessment Questions**:
- [ ] Has threat modeling been performed?
- [ ] Are security requirements documented?
- [ ] Are security patterns applied (least privilege, fail-safe defaults)?
- [ ] Is input validation at every layer?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Conduct threat modeling early
- Apply secure design principles
- Use established security patterns
- Implement defense-in-depth
- Plan for failure scenarios

#### 5. Security Misconfiguration
**Check for**:
- Are default configurations used?
- Are unnecessary features enabled?
- Are error messages verbose?
- Are security headers configured?

**Assessment Questions**:
- [ ] Are default passwords changed?
- [ ] Are unnecessary services disabled?
- [ ] Are security headers configured (CSP, HSTS, etc.)?
- [ ] Are error messages generic (not revealing internals)?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Use principle of least functionality
- Implement security headers
- Configure error handling (no stack traces in production)
- Regular security configuration reviews
- Use security scanning tools

#### 6. Vulnerable and Outdated Components
**Check for**:
- What dependencies are used?
- Are dependency versions specified?
- Is there a process for updates?

**Assessment Questions**:
- [ ] Are dependencies up-to-date?
- [ ] Are known vulnerabilities checked?
- [ ] Is dependency scanning automated?
- [ ] Are unmaintained packages avoided?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Use dependency scanning tools (Dependabot, Snyk)
- Keep dependencies updated
- Monitor security advisories
- Remove unused dependencies
- Pin dependency versions

#### 7. Identification and Authentication Failures
**Check for**:
- How are users authenticated?
- Are sessions managed securely?
- Is multi-factor authentication supported?
- Are weak passwords prevented?

**Assessment Questions**:
- [ ] Is password strength enforced?
- [ ] Are sessions properly managed (timeout, invalidation)?
- [ ] Is brute-force protection implemented?
- [ ] Is MFA available for sensitive operations?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Implement strong password policies
- Use secure session management
- Implement rate limiting for login attempts
- Support MFA where appropriate
- Use secure password reset flows

#### 8. Software and Data Integrity Failures
**Check for**:
- Is code from untrusted sources executed?
- Are auto-updates verified?
- Is CI/CD pipeline secured?
- Are deserialization attacks possible?

**Assessment Questions**:
- [ ] Are third-party libraries verified?
- [ ] Is code signing implemented?
- [ ] Are CI/CD pipelines secured?
- [ ] Is deserialization of untrusted data avoided?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Verify integrity of dependencies (checksums, signatures)
- Secure CI/CD pipeline
- Avoid deserializing untrusted data
- Use safe serialization formats (JSON over pickle)
- Implement code signing

#### 9. Security Logging and Monitoring Failures
**Check for**:
- Are security events logged?
- Are logs monitored?
- Are alerts configured?
- Are logs protected?

**Assessment Questions**:
- [ ] Are authentication events logged?
- [ ] Are authorization failures logged?
- [ ] Are anomalies detected and alerted?
- [ ] Are logs tamper-proof?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Log all security-relevant events
- Implement centralized logging
- Set up alerts for suspicious activity
- Protect logs from tampering
- Regular log review

#### 10. Server-Side Request Forgery (SSRF)
**Check for**:
- Does feature make HTTP requests based on user input?
- Can users specify URLs?
- Are webhooks supported?
- Is URL validation implemented?

**Assessment Questions**:
- [ ] Is user-provided URL input validated?
- [ ] Are internal network requests blocked?
- [ ] Is URL allowlisting implemented?
- [ ] Are redirects limited?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigation**:
- Validate and sanitize all URLs
- Use allowlist of permitted domains
- Block requests to private IP ranges
- Disable or limit redirects
- Use network segmentation

### Step 3: Identify Security Requirements

Based on OWASP assessment, document specific security requirements:

```markdown
## Security Requirements

### Authentication
- **SR-AUTH-001**: Implement secure password storage (bcrypt, cost ≥12)
- **SR-AUTH-002**: Enforce password complexity (min 12 chars, mixed case, numbers, symbols)
- **SR-AUTH-003**: Implement account lockout after 5 failed attempts
- **SR-AUTH-004**: Session timeout after 30 minutes of inactivity

### Authorization
- **SR-AUTHZ-001**: Implement role-based access control (RBAC)
- **SR-AUTHZ-002**: Check permissions on every protected resource access
- **SR-AUTHZ-003**: Use indirect references to prevent ID enumeration

### Input Validation
- **SR-INPUT-001**: Validate all user input (whitelist approach)
- **SR-INPUT-002**: Sanitize input before database operations
- **SR-INPUT-003**: Limit input length to prevent DoS
- **SR-INPUT-004**: Validate file uploads (type, size, content)

### Data Protection
- **SR-DATA-001**: Encrypt sensitive data at rest (AES-256)
- **SR-DATA-002**: Use TLS 1.3+ for all data in transit
- **SR-DATA-003**: Never log sensitive data (passwords, tokens, PII)
- **SR-DATA-004**: Implement secure data deletion

### API Security
- **SR-API-001**: Implement rate limiting (100 requests/minute per user)
- **SR-API-002**: Use API keys with proper rotation
- **SR-API-003**: Validate content-type headers
- **SR-API-004**: Implement CORS properly

### Logging and Monitoring
- **SR-LOG-001**: Log all authentication attempts (success and failure)
- **SR-LOG-002**: Log all authorization failures
- **SR-LOG-003**: Implement anomaly detection
- **SR-LOG-004**: Alert on suspicious patterns
```

### Step 4: Threat Modeling

Use `threat-modeling-guide.md` to systematically identify threats:

#### Assets
- User credentials
- Personal data (PII)
- Financial information
- API keys/tokens
- Business logic
- Infrastructure

#### Threat Actors
- External attackers
- Malicious users
- Insider threats
- Automated bots

#### Attack Vectors
- Web application
- API endpoints
- Database
- File system
- Network

#### STRIDE Analysis
- **Spoofing**: Can attacker impersonate users?
- **Tampering**: Can attacker modify data?
- **Repudiation**: Can actions be denied?
- **Information Disclosure**: Can sensitive data leak?
- **Denial of Service**: Can system be made unavailable?
- **Elevation of Privilege**: Can attacker gain higher privileges?

### Step 5: Security Testing Strategy

Define testing approach:

```markdown
## Security Testing Strategy

### Static Analysis
- Run security linters (Bandit for Python, ESLint security plugins)
- Check for hardcoded secrets
- Analyze dependency vulnerabilities

### Dynamic Analysis
- Penetration testing for authentication/authorization
- Input fuzzing for injection vulnerabilities
- Session management testing
- API security testing

### Code Review Focus
- Input validation implementation
- Authentication/authorization logic
- Cryptographic operations
- Error handling
- Logging implementation

### Automated Scanning
- Dependency vulnerability scanning (daily)
- SAST tools in CI/CD
- Container image scanning
```

## Best Practices

### 1. Security-by-Design
- Consider security from the start
- Apply least privilege principle
- Use defense-in-depth
- Fail securely (fail closed, not open)

### 2. Input Validation
- Validate all input (never trust user data)
- Use whitelist approach
- Validate length, format, type, range
- Sanitize before use

### 3. Output Encoding
- Encode output for context (HTML, URL, JavaScript)
- Use framework-provided encoding functions
- Prevent XSS with Content Security Policy

### 4. Authentication Best Practices
- Use strong password hashing (bcrypt, Argon2)
- Implement MFA for sensitive operations
- Use secure session management
- Implement rate limiting

### 5. Authorization Best Practices
- Check permissions on every request
- Use RBAC or ABAC
- Implement resource-level authorization
- Use indirect references

### 6. Cryptography Best Practices
- Use established libraries (don't roll your own crypto)
- Use strong algorithms (AES-256, RSA-2048+)
- Use secure random number generators
- Implement proper key management

### 7. API Security
- Implement authentication for all endpoints
- Use rate limiting
- Validate content-type
- Implement CORS correctly
- Version APIs

### 8. Error Handling
- Use generic error messages externally
- Log detailed errors internally
- Never expose stack traces
- Handle errors gracefully

### 9. Logging
- Log security events (auth, authz, errors)
- Don't log sensitive data
- Use structured logging
- Implement log monitoring

### 10. Dependencies
- Keep dependencies updated
- Monitor for vulnerabilities
- Remove unused dependencies
- Use dependency scanning tools

## Resources

### security-checklist.md
Comprehensive OWASP Top 10 checklist with:
- Detailed assessment questions for each risk
- Python-specific security considerations
- Common vulnerability patterns
- Mitigation strategies

### threat-modeling-guide.md
Guide for conducting threat modeling:
- STRIDE methodology
- Asset identification
- Threat actor profiling
- Attack vector mapping
- Risk prioritization

## Example Usage

### Input (Feature Description)
```
Feature: User login with email and password
- Users enter email and password
- System authenticates and creates session
- Users can reset forgotten passwords
```

### Output (Security Assessment)
```markdown
## Security Assessment

### OWASP Top 10 Risks

1. **Broken Access Control**: LOW
   - Feature implements authentication (positive control)
   - Need to ensure session validation on all protected endpoints

2. **Cryptographic Failures**: MEDIUM
   - Passwords must be hashed with bcrypt (cost ≥12)
   - TLS required for credential transmission
   - Session tokens must be cryptographically secure

3. **Injection**: LOW
   - Email input must be validated
   - Use parameterized queries for database operations

7. **Identification and Authentication Failures**: HIGH
   - Primary authentication feature - critical risk
   - Requires strong password policy
   - Needs brute-force protection
   - Must implement secure password reset

9. **Security Logging and Monitoring Failures**: MEDIUM
   - Must log all authentication attempts
   - Alert on suspicious patterns (multiple failures)

### Security Requirements
- **SR-AUTH-001**: Hash passwords with bcrypt (cost ≥12)
- **SR-AUTH-002**: Enforce strong passwords (min 12 chars)
- **SR-AUTH-003**: Implement rate limiting (5 attempts per 15min)
- **SR-AUTH-004**: Session timeout after 30min inactivity
- **SR-INPUT-001**: Validate email format
- **SR-DATA-001**: Use TLS 1.3+ for credential transmission
- **SR-LOG-001**: Log all authentication attempts
- **SR-LOG-002**: Alert on 10+ failures from same IP

### Recommendations
1. Implement MFA as optional enhancement
2. Consider passwordless authentication for future
3. Implement CAPTCHA after 3 failed attempts
4. Use secure password reset tokens (expiring, one-time use)
```

## Integration

This skill is used by:
- **analysis-specialist** agent during Phase 1: Requirements Analysis
- Activates automatically when agent assesses security risks
- Provides security assessment for analysis document generation

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when assessing security)
**Phase**: 1 (Requirements Analysis)
**Created**: 2025-10-29