---
name: system-architect
description: "Use when performing security audits or system hardening. Teaches security assessment principles and prioritization."
---

# System Architect

Principles for security auditing and system hardening. Platform-specific commands in `docs/security-audit/`.

## When to Use

- Setting up a new server
- Security audit before deployment
- After major configuration changes
- Periodic security checkups
- Investigating a breach

## Core Principles

### 1. Defense in Depth
No single security measure is sufficient. Layer multiple controls.

```
Network → Firewall → Service → Application → Data
   ↓          ↓         ↓           ↓          ↓
 Block    Filter    Harden      Validate   Encrypt
```

### 2. Least Privilege
Grant minimum access required. Remove what's not needed.

### 3. Fail Secure
When things break, they should fail closed, not open.

### 4. Audit Everything
If you can't see it, you can't secure it. Log all access.

## Priority Levels

All findings must be rated by severity:

| Level | Meaning | Action |
|-------|---------|--------|
| **CRITICAL** | Active exploitation possible | Fix NOW |
| **HIGH** | Significant risk | Fix within 24h |
| **MEDIUM** | Best practice violation | Fix within 1 week |
| **LOW** | Minor improvement | Fix when convenient |

## Audit Phases

### Phase 1: Network Exposure
What can attackers reach?

- List all listening ports
- Check for services bound to 0.0.0.0
- Verify firewall is enabled and configured
- Identify unnecessary exposed services

### Phase 2: Authentication
How do users and services authenticate?

- SSH: Key-based only, no root login
- Passwords: Strong policy, no empty passwords
- Services: No default credentials
- 2FA: Enabled where possible

### Phase 3: Authorization
What can authenticated users do?

- Principle of least privilege
- No unnecessary sudo access
- Service accounts restricted
- File permissions reviewed

### Phase 4: Data Protection
How is sensitive data protected?

- Encryption at rest
- Encryption in transit (TLS)
- Secrets management (not in code)
- Backup encryption

### Phase 5: Monitoring
Can you detect attacks?

- Logging enabled
- Log aggregation
- Alerting configured
- Intrusion detection

## Quick Audit Checklist

### Network
- [ ] Firewall enabled
- [ ] Only necessary ports exposed
- [ ] Services bound to localhost where possible
- [ ] SSL/TLS properly configured

### Authentication
- [ ] SSH key-based auth only
- [ ] Root login disabled
- [ ] Strong password policy
- [ ] fail2ban or similar installed

### Services
- [ ] Running as non-root users
- [ ] Unnecessary services disabled
- [ ] Configurations hardened
- [ ] Auto-updates enabled

### Docker (if applicable)
- [ ] Containers not privileged
- [ ] Ports bound to localhost
- [ ] No secrets in environment
- [ ] Images from trusted sources

## Security Scanning

### Public Tools (No Setup Required)

| Tool | Purpose | Usage |
|------|---------|-------|
| `composer audit` | PHP vulnerabilities | `composer audit` |
| `npm audit` | Node vulnerabilities | `npm audit` |
| `pip-audit` | Python vulnerabilities | `pip-audit -r requirements.txt` |
| Trivy | Multi-language scanner | `docker run aquasec/trivy fs .` |
| Gitleaks | Secrets in code | `docker run zricethezav/gitleaks detect` |

### CI Integration

Add to your pipeline:

**GitLab CI:**
```yaml
security:
  image: aquasec/trivy:latest
  script: trivy fs --exit-code 0 --severity HIGH,CRITICAL .
  allow_failure: true
```

**GitHub Actions:**
```yaml
- name: Security scan
  run: |
    docker run aquasec/trivy:latest fs --severity HIGH,CRITICAL .
  continue-on-error: true
```

## Output Format

```
================================================================================
SECURITY AUDIT REPORT
Date: YYYY-MM-DD
Host: hostname
================================================================================

CRITICAL (0)
------------
None found.

HIGH (2)
--------
[HIGH] Issue description
       Location: where
       Fix: how to fix

MEDIUM (1)
----------
[MEDIUM] Issue description
         Fix: how to fix

================================================================================
SUMMARY: 0 Critical | 2 High | 1 Medium | 0 Low
================================================================================
```

## Documentation Integration

After completing an audit:

```bash
# Log summary
docchange "Security audit completed - X critical, Y high, Z medium issues"

# Log fixes
docchange "FIXED: Disabled SSH root login"
```

## Reference Commands

Platform-specific audit commands:

| Platform | Location |
|----------|----------|
| Linux | `docs/security-audit/linux.md` |
| Windows | `docs/security-audit/windows.md` |
| Docker | `docs/security-audit/docker.md` |

## Common Fixes

| Issue | Fix |
|-------|-----|
| SSH root login | `PermitRootLogin no` in sshd_config |
| SSH password auth | `PasswordAuthentication no` in sshd_config |
| No firewall | Enable ufw/firewalld/Windows Firewall |
| Database exposed | Bind to 127.0.0.1 |
| No fail2ban | Install and enable fail2ban |
| Docker privileged | Remove `--privileged` flag |
| Ports on 0.0.0.0 | Bind to `127.0.0.1:port:port` |

## Integration

Works with:
- `server-documentation` skill for logging
- `defense-in-depth` skill for layered security
- `ci-templates` skill for security scanning in CI
