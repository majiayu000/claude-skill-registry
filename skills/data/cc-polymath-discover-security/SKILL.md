---
name: discover-security
description: Automatically discover security skills when working with authentication, authorization, input validation, security headers, vulnerability assessment, or secrets management. Activates for application security, OWASP, and security hardening tasks.
---

# Security Skills Discovery

Provides automatic access to comprehensive application security, vulnerability assessment, and security best practices skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- Authentication and authorization systems
- Input validation and sanitization
- Security headers (CSP, HSTS, CORS)
- Vulnerability scanning and penetration testing
- OWASP Top 10 vulnerabilities
- Secrets management (Vault, AWS Secrets Manager)
- SQL injection, XSS, or other attack prevention
- Security hardening and compliance
- Password hashing and credential management
- API security and access control

## Available Skills

### Quick Reference

The Security category contains 6 specialized skills:

1. **authentication** - Authentication patterns (JWT, OAuth2, sessions, MFA, password security)
2. **authorization** - Access control (RBAC, ABAC, policy engines, permissions)
3. **input-validation** - Input validation and sanitization (SQL injection, XSS, command injection)
4. **security-headers** - HTTP security headers (CSP, HSTS, X-Frame-Options, CORS)
5. **vulnerability-assessment** - Security testing (OWASP Top 10, scanning tools, pentesting)
6. **secrets-management** - Secrets handling (Vault, AWS Secrets Manager, key rotation)

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/security/INDEX.md
```

This loads the full Security category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
# Identity and access
cat ~/.claude/skills/security/authentication.md
cat ~/.claude/skills/security/authorization.md

# Input security
cat ~/.claude/skills/security/input-validation.md
cat ~/.claude/skills/security/security-headers.md

# Security operations
cat ~/.claude/skills/security/vulnerability-assessment.md
cat ~/.claude/skills/security/secrets-management.md
```

## Common Workflows

### Secure Web Application
**Sequence**: Authentication → Authorization → Input validation → Security headers

```bash
cat ~/.claude/skills/security/authentication.md        # User login
cat ~/.claude/skills/security/authorization.md         # Access control
cat ~/.claude/skills/security/input-validation.md      # XSS/SQL injection prevention
cat ~/.claude/skills/security/security-headers.md      # Browser protection
```

### Security Audit
**Sequence**: Vulnerability assessment → Input validation → Headers → Secrets

```bash
cat ~/.claude/skills/security/vulnerability-assessment.md  # OWASP Top 10 testing
cat ~/.claude/skills/security/input-validation.md          # Injection testing
cat ~/.claude/skills/security/security-headers.md          # Header configuration
cat ~/.claude/skills/security/secrets-management.md        # Credential security
```

### API Security
**Sequence**: Authentication → Authorization → Input validation → Secrets

```bash
cat ~/.claude/skills/security/authentication.md        # JWT/OAuth2
cat ~/.claude/skills/security/authorization.md         # API access control
cat ~/.claude/skills/security/input-validation.md      # Request validation
cat ~/.claude/skills/security/secrets-management.md    # API key management
```

### DevSecOps Pipeline
**Sequence**: Vulnerability assessment → Secrets → Input validation

```bash
cat ~/.claude/skills/security/vulnerability-assessment.md  # Security scanning
cat ~/.claude/skills/security/secrets-management.md        # CI/CD secrets
cat ~/.claude/skills/security/input-validation.md          # SAST validation
```

### Secure New Application
**Full security implementation from scratch**:

```bash
# 1. Identity and access
cat ~/.claude/skills/security/authentication.md
cat ~/.claude/skills/security/authorization.md

# 2. Input protection
cat ~/.claude/skills/security/input-validation.md
cat ~/.claude/skills/security/security-headers.md

# 3. Operations
cat ~/.claude/skills/security/secrets-management.md
cat ~/.claude/skills/security/vulnerability-assessment.md
```

## Skill Selection Guide

**Choose Authentication when:**
- Implementing user login systems
- Working with JWT, OAuth2, or sessions
- Adding multi-factor authentication
- Managing passwords and credentials

**Choose Authorization when:**
- Implementing access control
- Building role-based permissions (RBAC)
- Working with policy engines (OPA, Casbin)
- Preventing privilege escalation

**Choose Input Validation when:**
- Processing user input
- Preventing SQL injection
- Protecting against XSS attacks
- Validating file uploads
- Preventing command injection

**Choose Security Headers when:**
- Configuring Content Security Policy (CSP)
- Implementing HTTPS enforcement (HSTS)
- Setting up CORS for APIs
- Preventing clickjacking
- Hardening web applications

**Choose Vulnerability Assessment when:**
- Testing for OWASP Top 10
- Running security scans (SAST/DAST)
- Performing penetration tests
- Auditing application security
- Setting up security CI/CD

**Choose Secrets Management when:**
- Storing API keys or credentials
- Integrating with HashiCorp Vault
- Using AWS Secrets Manager or GCP Secret Manager
- Rotating encryption keys
- Managing CI/CD secrets

## Integration with Other Skills

Security skills commonly combine with:

**API skills** (`discover-api`):
- API authentication and authorization
- API input validation
- API rate limiting (abuse prevention)
- Securing REST and GraphQL endpoints

**Database skills** (`discover-database`):
- SQL injection prevention
- Database connection security
- Credential management
- Row-level security

**Frontend skills** (`discover-frontend`):
- XSS prevention in React/Vue
- Content Security Policy
- Secure cookie handling
- Client-side validation

**Infrastructure skills** (`discover-infrastructure`, `discover-cloud`):
- Secrets management in deployments
- Network security
- Container security scanning
- TLS/SSL configuration

**Testing skills** (`discover-testing`):
- Security integration tests
- Penetration testing
- Automated security scans
- Vulnerability regression tests

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects security-related work
2. **Browse skills**: Run `cat ~/.claude/skills/security/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills
4. **Follow workflows**: Use recommended sequences for common security patterns
5. **Combine skills**: Load multiple skills for comprehensive security coverage

## Progressive Loading

This gateway skill (~200 lines, ~2K tokens) enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md (~3K tokens) for full overview
- **Level 3**: Load specific skills (~2-4K tokens each) as needed

Total context: 2K + 3K + skill(s) = 5-12K tokens vs 30K+ for entire index.

## Quick Start Examples

**"Implement user authentication"**:
```bash
cat ~/.claude/skills/security/authentication.md
```

**"Add role-based access control"**:
```bash
cat ~/.claude/skills/security/authorization.md
```

**"Prevent SQL injection"**:
```bash
cat ~/.claude/skills/security/input-validation.md
```

**"Configure Content Security Policy"**:
```bash
cat ~/.claude/skills/security/security-headers.md
```

**"Test for OWASP vulnerabilities"**:
```bash
cat ~/.claude/skills/security/vulnerability-assessment.md
```

**"Integrate HashiCorp Vault"**:
```bash
cat ~/.claude/skills/security/secrets-management.md
```

**"Secure API with JWT"**:
```bash
cat ~/.claude/skills/security/authentication.md
cat ~/.claude/skills/security/authorization.md
```

---

**Next Steps**: Run `cat ~/.claude/skills/security/INDEX.md` to see full category details, or load specific skills using the bash commands above.
