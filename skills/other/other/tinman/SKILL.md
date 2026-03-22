---
name: tinman
version: 1.0.0
description: Security auditing and hardening for OpenClaw and system infrastructure.
metadata:
  openclaw:
    emoji: 🛡️
    category: security
---

# Tinman

Security auditing and hardening for OpenClaw and system infrastructure.

## Security Levels

| Level | Description | Response |
|-------|-------------|----------|
| **S0** | Info | Log only |
| **S1** | Low | Notify user |
| **S2** | Medium | Alert + recommend fix |
| **S3** | High | Immediate action required |
| **S4** | Critical | Stop + notify immediately |

## Checks

### OpenClaw Security

| Check | Risk | Action |
|-------|------|--------|
| Credentials in git | S3 | Add to .gitignore, rotate |
| Token expiration | S2 | Refresh tokens |
| Exposed secrets | S4 | Rotate immediately |
| Uncommitted changes | S1 | Review + commit |

### System Security

| Check | Risk | Action |
|-------|------|--------|
| SSH password auth | S2 | Disable, use keys only |
| Open ports | S1 | Review with `ss -tlnp` |
| Unattended upgrades | S2 | Enable automatic updates |
| Firewall status | S2 | Verify ufw/iptables |

## Workflow

### 1. Security Scan

```bash
# Check for credentials in git
git log --all --full-history -- .credentials/

# Check file permissions
ls -la ~/.credentials/

# Check SSH config
cat /etc/ssh/sshd_config | grep -E "PasswordAuthentication|PermitRootLogin"
```

### 2. Report Generation

```markdown
## Security Audit Report
**Date:** 2026-02-20
**Scope:** OpenClaw + System

### Findings
| Level | Issue | Recommendation |
|-------|-------|----------------|
| S2 | Token expires in 3 days | Refresh Google OAuth |

### Actions Taken
- [x] Verified .credentials/ permissions (600)
- [ ] Refresh expiring tokens
```

### 3. Automated Monitoring

```json
{
  "name": "daily-security-check",
  "schedule": {"kind": "cron", "expr": "0 6 * * *"},
  "payload": {
    "kind": "agentTurn",
    "message": "Run tinman security scan. Check: credential perms, token expiration, git secrets. Report S2+ issues."
  },
  "sessionTarget": "isolated",
  "notify": true
}
```

## Best Practices

1. **Credential hygiene** — 600 permissions, never in git
2. **Token rotation** — Before expiration
3. **Regular audits** — Weekly automated scans
4. **Principle of least privilege** — Minimal permissions
5. **Audit logging** — Track all changes

## Emergency Response

If S4 (Critical) detected:

1. **Stop** — Halt related operations
2. **Assess** — Scope of exposure
3. **Rotate** — Change all affected credentials
4. **Review** — How did it happen
5. **Prevent** — Update processes
