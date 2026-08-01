---
name: security-williaby-image-preprocessing-d
description: Security validation, vulnerability scanning, and compliance checking.
---

# Security Skill

Security validation, vulnerability scanning, and compliance checking.

## Activation

Auto-activates on keywords: security, vulnerability, audit, OWASP, encryption, GPG, SSH, signing, secrets, scan, bandit

## Workflows

### Environment Validation
- **validate-env.md**: GPG/SSH key validation

### Scanning
- **scan.md**: Security vulnerability scanning

### Encryption
- **encrypt.md**: Secret encryption and management

## Commands

```bash
# Validate GPG key
gpg --list-secret-keys

# Validate SSH key
ssh-add -l

# Check git signing configuration
git config --get user.signingkey

# Run Bandit security scanner
uv run bandit -r src/ -c pyproject.toml

# Check dependencies for vulnerabilities
uv run pip-audit
uv run safety check

# Run Semgrep security rules
uv run semgrep scan --config auto src/
```

## Security Checklist

### Pre-Commit
- [ ] No secrets in code (checked by gitleaks)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Bandit security scan passes

### Pre-Release
- [ ] All known vulnerabilities addressed
- [ ] Security advisory published (if applicable)
- [ ] Dependencies updated to secure versions

## OWASP Top 10 Considerations

1. **Injection**: Use parameterized queries, validate input
2. **Broken Authentication**: Use secure session management
3. **Sensitive Data Exposure**: Encrypt sensitive data at rest and in transit
4. **XML External Entities**: Disable external entity processing
5. **Broken Access Control**: Implement proper authorization checks
6. **Security Misconfiguration**: Use secure defaults
7. **XSS**: Escape output, use Content Security Policy
8. **Insecure Deserialization**: Validate and sanitize serialized data
9. **Using Components with Known Vulnerabilities**: Keep dependencies updated
10. **Insufficient Logging**: Log security events, monitor for anomalies
