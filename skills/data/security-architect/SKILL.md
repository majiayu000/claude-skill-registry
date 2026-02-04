---
name: security-architect
description: Security architecture and threat modeling. OWASP Top 10 analysis, security pattern implementation, vulnerability assessment, and security review for code and infrastructure.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Apply defense in depth
  - Follow principle of least privilege
  - Validate all inputs
  - Encrypt sensitive data at rest and in transit
error_handling: graceful
streaming: supported
---

# Security Architect Skill

<identity>
Security Architect Skill - Performs threat modeling, OWASP Top 10 analysis, security pattern implementation, and vulnerability assessment for code and infrastructure.
</identity>

<capabilities>
- Threat modeling (STRIDE)
- OWASP Top 10 vulnerability analysis
- Security code review
- Authentication/Authorization design
- Encryption and secrets management
- Security architecture patterns
</capabilities>

<instructions>
<execution_process>

### Step 1: Threat Modeling (STRIDE)

Analyze threats using STRIDE:

| Threat                     | Description                 | Example               |
| -------------------------- | --------------------------- | --------------------- |
| **S**poofing               | Impersonating users/systems | Stolen credentials    |
| **T**ampering              | Modifying data              | SQL injection         |
| **R**epudiation            | Denying actions             | Missing audit logs    |
| **I**nformation Disclosure | Data leaks                  | Exposed secrets       |
| **D**enial of Service      | Blocking access             | Resource exhaustion   |
| **E**levation of Privilege | Gaining unauthorized access | Broken access control |

### Step 2: OWASP Top 10 Analysis

Check for common vulnerabilities:

1. **A01: Broken Access Control**
   - Verify authorization on every endpoint
   - Deny by default

2. **A02: Cryptographic Failures**
   - Use strong algorithms (AES-256, SHA-256+)
   - Never store plaintext passwords

3. **A03: Injection**
   - Parameterize all queries
   - Validate/sanitize inputs

4. **A04: Insecure Design**
   - Threat model early
   - Use secure design patterns

5. **A05: Security Misconfiguration**
   - Harden defaults
   - Remove unnecessary features

6. **A06: Vulnerable Components**
   - Keep dependencies updated
   - Monitor CVE databases

7. **A07: Authentication Failures**
   - Implement MFA
   - Use secure session management

8. **A08: Software/Data Integrity**
   - Verify dependencies (SRI, signatures)
   - Protect CI/CD pipelines

9. **A09: Logging Failures**
   - Log security events
   - Protect log integrity

10. **A10: SSRF**
    - Validate/sanitize URLs
    - Use allowlists

### Step 3: Security Code Review

Look for common issues:

```javascript
// BAD: SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: Parameterized query
const query = `SELECT * FROM users WHERE id = $1`;
await db.query(query, [userId]);
```

```javascript
// BAD: Hardcoded secrets
const apiKey = 'sk-abc123...';

// GOOD: Environment variables
const apiKey = process.env.API_KEY;
```

### Step 4: Authentication/Authorization Review

Verify:

- Strong password requirements
- Secure session management
- JWT validation (signature, expiry, audience)
- Role-based access control (RBAC)
- API authentication (OAuth 2.0, API keys)

### Step 5: Generate Security Report

Create findings report:

```markdown
## Security Assessment Report

### Critical Findings

1. SQL injection in /api/users endpoint
   - Risk: Data breach
   - Fix: Use parameterized queries

### High Findings

2. Missing rate limiting on login
   - Risk: Brute force attacks
   - Fix: Implement rate limiting

### Recommendations

- Enable HTTPS everywhere
- Implement CSP headers
- Add security logging
```

</execution_process>

<best_practices>

1. **Defense in Depth**: Layer security controls
2. **Least Privilege**: Minimal permissions
3. **Fail Securely**: Default to deny
4. **Validate Everything**: Never trust input
5. **Keep Secrets Secret**: Use secret managers

</best_practices>
</instructions>

<examples>
<usage_example>
**Security Review Request**:

```
Review the authentication flow in src/auth/ for security issues
```

**Example Response**:

```markdown
## Security Review: src/auth/

### Findings

#### CRITICAL: Weak Password Hashing

- File: src/auth/password.js:23
- Issue: Using MD5 for password hashing
- Fix: Use bcrypt with cost factor >= 12

#### HIGH: No Rate Limiting

- File: src/auth/login.js
- Issue: Login endpoint has no rate limiting
- Fix: Add rate limiting (5 attempts/minute)

#### MEDIUM: Session Not Invalidated

- File: src/auth/logout.js
- Issue: Logout doesn't invalidate server-side session
- Fix: Clear session from store on logout

### Recommendations

1. Implement bcrypt for password hashing
2. Add rate limiting middleware
3. Use secure session configuration
```

</usage_example>
</examples>

## Rules

- Always prioritize findings by severity
- Provide specific remediation steps
- Consider business context when assessing risk

## Related Skills

- [`auth-security-expert`](../auth-security-expert/SKILL.md) - OAuth 2.1, JWT, and authentication-specific security patterns

## Related Workflow

For comprehensive security audits requiring multi-phase threat analysis, vulnerability scanning, and remediation planning, see the corresponding workflow:

- **Workflow File**: `.claude/workflows/security-architect-skill-workflow.md`
- **When to Use**: For structured security audits requiring OWASP Top 10 analysis, dependency CVE checks, penetration testing, and remediation planning
- **Phases**: 5 phases (Threat Modeling, Security Code Review, Dependency Audit, Penetration Testing, Remediation Planning)
- **Coverage**: Full OWASP Top 10, STRIDE threat modeling, CVE database checks, automated and manual penetration testing

**Key Features:**

- Multi-agent orchestration (security-architect, code-reviewer, developer, devops)
- Security gates for pre-release blocking
- Severity classification (CRITICAL/HIGH/MEDIUM/LOW)
- Automated ticket generation
- Compliance-ready reporting (SOC2, GDPR, HIPAA)

See also: [Feature Development Workflow](../../workflows/enterprise/feature-development-workflow.md) for integrating security reviews into the development lifecycle.

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
