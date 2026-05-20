---
name: security-auditor
description: Security vulnerability scanner and OWASP compliance auditor for codebases. Dependency scanning (npm audit, pip-audit), secret detection (high-entropy strings, API keys), SAST for injection/XSS vulnerabilities, and security posture reports. Activate on 'security audit', 'vulnerability scan', 'OWASP', 'secret detection', 'dependency check', 'CVE', 'security review', 'penetration testing prep'. NOT for runtime WAF configuration (use infrastructure tools), network security/firewalls, or compliance certifications like SOC2/HIPAA (legal/organizational).
allowed-tools: Read,Write,Edit,Bash(npm audit:*,pip-audit:*,grep:*,find:*),Grep,Glob
category: Code Quality & Testing
tags:
  - security
  - owasp
  - vulnerabilities
  - sast
  - dependencies
pairs-with:
  - skill: devops-automator
    reason: Secure deployment pipelines
  - skill: mcp-creator
    reason: Secure MCP server development
---

# Security Auditor

Comprehensive security scanning for codebases. Identifies vulnerabilities before they become incidents. Focuses on actionable findings with remediation guidance.

## When to Use

**Use for:**
- Pre-deployment security audits
- Dependency vulnerability scanning
- Secret/credential leak detection
- Code-level SAST (Static Application Security Testing)
- Security posture reports for stakeholders
- OWASP Top 10 compliance checking
- Pre-PR security reviews

**Do NOT use for:**
- Runtime security (WAF, rate limiting) - use infrastructure tools
- Network security/firewall rules - use cloud/DevOps skills
- SOC2/HIPAA/PCI compliance - requires legal/organizational process
- Penetration testing execution - this is detection, not exploitation

## Quick Start

### Full Security Audit
```bash
# Run comprehensive scan
./scripts/full-audit.sh /path/to/project

# Output: security-report.json + summary
```

### Quick Checks
```bash
# Dependency vulnerabilities only
npm audit --json > deps-audit.json

# Secret detection only
./scripts/detect-secrets.sh /path/to/project

# OWASP check specific file
./scripts/owasp-check.py /path/to/file.js
```

## Core Scanning Capabilities

### 1. Dependency Scanning

| Package Manager | Command | Severity Levels |
|-----------------|---------|-----------------|
| npm | `npm audit --json` | critical, high, moderate, low |
| yarn | `yarn audit --json` | same as npm |
| pip | `pip-audit --format json` | critical, high, medium, low |
| cargo | `cargo audit --json` | same |

**Decision Tree:**
```
Critical severity found?
├── YES → Block deployment, immediate fix required
│   └── Check if patch available → npm audit fix --force
├── NO → High severity?
    ├── YES → Fix within sprint, document if deferred
    └── NO → Low/Moderate → Track, fix during maintenance
```

### 2. Secret Detection

**High-Risk Patterns:**
- API keys: `/[A-Za-z0-9_]{20,}/` near "key", "api", "secret"
- AWS credentials: `AKIA[0-9A-Z]{16}`
- Private keys: `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`
- JWT tokens: `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
- Connection strings: `://[^:]+:[^@]+@`

**Entropy Analysis:**
- Shannon entropy > 4.5 on strings > 20 chars = suspicious
- Base64-encoded blobs in source = investigate

**False Positive Handling:**
```
Secret-like pattern found?
├── In test file? → Lower severity, document
├── In example/docs? → Check if placeholder
├── High entropy + near "password"/"secret" → High confidence
└── In .env.example? → Acceptable if placeholder values
```

### 3. OWASP Top 10 Static Analysis

| # | Vulnerability | Detection Pattern |
|---|---------------|-------------------|
| A01 | Broken Access Control | Missing auth checks on routes |
| A02 | Cryptographic Failures | Weak algorithms (MD5, SHA1 for passwords) |
| A03 | Injection | Unparameterized queries, eval(), innerHTML |
| A04 | Insecure Design | Hardcoded credentials, missing rate limits |
| A05 | Security Misconfiguration | Debug mode in prod, default credentials |
| A06 | Vulnerable Components | Known CVEs in dependencies |
| A07 | Auth Failures | Weak password policies, session issues |
| A08 | Integrity Failures | Unsigned updates, untrusted deserialization |
| A09 | Logging Failures | Sensitive data in logs, missing audit trails |
| A10 | SSRF | Unvalidated URL inputs to fetch/request |

### 4. Language-Specific Checks

**JavaScript/TypeScript:**
- `eval()`, `new Function()` - code injection
- `innerHTML`, `outerHTML` - XSS vectors
- `document.write()` - DOM-based XSS
- `child_process.exec()` with user input - command injection
- Regex without timeout - ReDoS vulnerability

**Python:**
- `pickle.loads()` with untrusted data - arbitrary code execution
- `yaml.load()` without `Loader=SafeLoader` - code injection
- `subprocess.shell=True` - command injection
- `eval()`, `exec()` - code injection
- SQL string concatenation - SQL injection

**SQL:**
- String concatenation in queries - SQL injection
- `LIKE '%' + input + '%'` - injection via wildcards
- Missing parameterization - critical vulnerability

## Anti-Patterns

### Anti-Pattern: Security by Obscurity
**What it looks like**: "Nobody will find this hardcoded password"
**Why wrong**: Secrets in source always leak eventually
**Instead**: Environment variables, secret managers, zero hardcoded secrets

### Anti-Pattern: Audit Fatigue
**What it looks like**: 500 findings, all "medium", team ignores
**Why wrong**: Critical issues buried in noise
**Instead**: Prioritize by exploitability, start with critical/high only

### Anti-Pattern: Fix Without Understanding
**What it looks like**: `npm audit fix --force` without review
**Why wrong**: May introduce breaking changes, doesn't address root cause
**Instead**: Review each fix, understand the vulnerability, test after

### Anti-Pattern: One-Time Audit
**What it looks like**: "We did a security audit last year"
**Why wrong**: New CVEs daily, code changes constantly
**Instead**: CI/CD integration, weekly automated scans minimum

## Security Report Format

```json
{
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 12,
    "informational": 8
  },
  "findings": [
    {
      "id": "SEC-001",
      "severity": "high",
      "category": "A03:Injection",
      "title": "SQL Injection in user search",
      "location": "src/api/users.js:45",
      "description": "User input concatenated directly into SQL query",
      "evidence": "const query = `SELECT * FROM users WHERE name = '${input}'`",
      "remediation": "Use parameterized queries: db.query('SELECT * FROM users WHERE name = $1', [input])",
      "references": ["https://owasp.org/www-community/attacks/SQL_Injection"]
    }
  ],
  "recommendations": [
    "Implement parameterized queries across all database access",
    "Add input validation layer",
    "Enable SQL query logging for monitoring"
  ]
}
```

## CI/CD Integration

### GitHub Actions Example
```yaml
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run security audit
      run: |
        npm audit --json > audit.json
        ./scripts/detect-secrets.sh . > secrets.json
        ./scripts/generate-report.py
    - name: Fail on critical
      run: |
        if jq '.summary.critical > 0' report.json; then
          echo "Critical vulnerabilities found!"
          exit 1
        fi
```

## Scripts (in `scripts/` folder)

| Script | Purpose |
|--------|---------|
| `full-audit.sh` | Comprehensive security scan |
| `detect-secrets.sh` | High-entropy string and pattern detection |
| `owasp-check.py` | OWASP Top 10 static analysis |
| `generate-report.py` | Combine findings into unified report |

## Expert vs Novice Approach

| Novice | Expert |
|--------|--------|
| Runs audit once before release | CI/CD integration, every commit |
| Focuses on tool output only | Understands vulnerability context |
| Fixes everything or nothing | Triages by exploitability |
| Uses one scanner | Layers multiple tools |
| Ignores false positives | Tunes detection rules |

## Success Metrics

| Metric | Target |
|--------|--------|
| Critical/High pre-production | 0 |
| Mean time to remediate critical | &lt; 24 hours |
| False positive rate | &lt; 10% |
| Scan coverage | 100% of deployable code |

## Reference Files

- `references/owasp-top-10-2024.md` - Detailed OWASP guidance
- `references/secret-patterns.md` - Comprehensive regex patterns
- `references/remediation-playbook.md` - Fix guidance by vulnerability type
- `references/ci-cd-templates.md` - Integration examples
- `scripts/` - Working security scanning scripts

---

**Detects**: Dependency CVEs | Secret leaks | Injection vulnerabilities | OWASP violations | Security misconfigurations

**Use with**: site-reliability-engineer (deployment gates) | code-review (PR security checks)
