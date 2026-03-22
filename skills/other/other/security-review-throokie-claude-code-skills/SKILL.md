---
name: security-review
description: AI 安全审计，检测 OWASP Top 10 漏洞、注入攻击、认证缺陷。触发词：安全审查、漏洞检测、security review。
allowed-tools: Read, Grep, Glob, Bash
---

# Security Review Skill

Comprehensive security analysis for code changes, detecting vulnerabilities and security anti-patterns.

## Security Categories

### 1. Injection Vulnerabilities (OWASP #1)

Check for:
- SQL injection: Unsanitized user input in queries
- Command injection: `eval()`, `exec()`, shell commands with user input
- XSS: Unescaped output, `innerHTML`, `dangerouslySetInnerHTML`
- LDAP/XPath injection: User input in filter expressions

```bash
# Common dangerous patterns
grep -rn "eval\|exec\|system\|popen\|subprocess.call.*shell=True" --include="*.py" .
grep -rn "innerHTML\|dangerouslySetInnerHTML\|v-html" --include="*.js" --include="*.vue" .
grep -rn "mysqli_query\|pg_query.*\$" --include="*.php" .
```

### 2. Broken Authentication (OWASP #2)

Check for:
- Weak password policies
- Missing/weak session management
- Insecure password storage (plain text, weak hashing)
- Missing MFA for sensitive operations
- Exposed authentication tokens in logs/URLs

### 3. Sensitive Data Exposure (OWASP #3)

Check for:
- Hardcoded secrets, API keys, passwords
- Unencrypted sensitive data at rest
- Sensitive data in logs
- Missing HTTPS enforcement
- Insecure cookie flags

```bash
# Find potential secrets
grep -rn "api_key\|apikey\|secret\|password\|token\|credential" --include="*.py" --include="*.js" --include="*.ts" . | grep -v "\.env\|config\.example"
```

### 4. XML External Entities (XXE) (OWASP #4)

Check for:
- XML parsing without disabling external entities
- SOAP requests with user input
- File upload allowing XML/XLSX

### 5. Broken Access Control (OWASP #5)

Check for:
- Missing authorization checks
- IDOR (Insecure Direct Object References)
- Path traversal vulnerabilities
- Missing CORS configuration

### 6. Security Misconfiguration (OWASP #6)

Check for:
- Default credentials
- Unnecessary features enabled
- Verbose error messages in production
- Missing security headers
- Outdated dependencies with known vulnerabilities

```bash
# Check for outdated packages
npm audit 2>/dev/null || pip-audit 2>/dev/null || yarn audit 2>/dev/null
```

### 7. Cross-Site Scripting (XSS) (OWASP #7)

Already covered in injection section.

### 8. Insecure Deserialization (OWASP #8)

Check for:
- `pickle.loads()` with untrusted data (Python)
- `ObjectInputStream` (Java)
- `JSON.parse()` with prototype pollution risk

### 9. Using Components with Known Vulnerabilities (OWASP #9)

Run dependency audits and check for CVEs.

### 10. Insufficient Logging & Monitoring (OWASP #10)

Check for:
- Missing audit logs for sensitive operations
- Logs without enough context
- No alerting for suspicious activities

## Review Process

1. **Identify attack surface**: Entry points, user inputs, APIs
2. **Check each category**: Systematically review against OWASP Top 10
3. **Analyze data flow**: Trace user input from entry to storage/output
4. **Review dependencies**: Check for known vulnerabilities
5. **Document findings**: Severity, location, remediation

## Output Format

```markdown
## Security Review Report

### Summary
- **Critical**: X issues
- **High**: X issues
- **Medium**: X issues
- **Low**: X issues

### Findings

#### [CRITICAL] Issue Title
- **File**: path/to/file.ext:line
- **Category**: OWASP #X
- **Description**: What's wrong
- **Impact**: What could happen
- **Remediation**: How to fix

### Recommendations
1. ...
```

## Tools

- `npm audit` / `yarn audit` - Node.js vulnerabilities
- `pip-audit` - Python vulnerabilities
- `trivy` - Container vulnerabilities
- `semgrep` - Static analysis
- `snyk` - Dependency scanning