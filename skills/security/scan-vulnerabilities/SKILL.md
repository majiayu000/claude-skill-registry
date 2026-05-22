---
name: scan-vulnerabilities
description: "Detect security vulnerabilities in code and dependencies. Use when auditing security."
mcp_fallback: none
category: security
tier: 2
user-invocable: false
---

# Scan Vulnerabilities

Systematically scan code for security vulnerabilities including unsafe patterns, known CVEs, and potential exploits.

## When to Use

- Regular security audits
- Before releasing code to production
- When updating dependencies
- In CI/CD security checks

## Quick Reference

```bash
# Python security scanning
pip install bandit safety

# Scan code for security issues
bandit -r . -ll

# Check for known vulnerabilities in dependencies
safety check

# Advanced: SAST scanning
python3 -m pip install semgrep
semgrep --config=p/security-audit --json .
```

## Workflow

1. **Scan code for issues**: Identify unsafe patterns (SQL injection, exec, hardcoded secrets)
2. **Check dependencies**: Scan for known vulnerabilities (CVEs)
3. **Review findings**: Analyze severity and exploitability
4. **Prioritize fixes**: Address critical/high severity issues first
5. **Document fixes**: Record how vulnerabilities were resolved

## Output Format

Security scan report:

- Vulnerability type (SQL injection, hardcoded secret, etc.)
- Location (file, line number)
- Severity (critical/high/medium/low)
- CVSS score (if applicable)
- Vulnerable dependency version (if applicable)
- Recommended fix
- Fixed version (if dependency)

## References

- See CLAUDE.md > Security standards for security guidelines
- See `quality-security-scan` skill for automated CI scanning
- OWASP Top 10 for common vulnerability categories
