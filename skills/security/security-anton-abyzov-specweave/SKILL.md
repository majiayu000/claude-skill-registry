---
description: Security engineer for vulnerability assessment, penetration testing guidance, and secure code review. Use for OWASP Top 10 checks, threat modeling, or security architecture review. Covers authentication flaws, injection vulnerabilities, access control, and compliance requirements.
---

# Security Review

## Project Overrides

!`s="security"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

## Security Assessment

Perform security assessment:

1. **OWASP Top 10** — Check for injection, XSS, CSRF, broken auth, etc.
2. **Threat modeling** — Identify attack surfaces and data flow risks
3. **Auth review** — Authentication and authorization design
4. **Dependency audit** — Check for known CVEs

For real-time pattern detection during coding, use `/sw:security-patterns` instead.
