---
name: vibe-security
description: "Security intelligence for code analysis. Detects SQL injection, XSS, CSRF, authentication issues, crypto failures, and more. Actions: scan, analyze, fix, audit, check, review, secure, validate, sanitize, protect. Languages: JavaScript, TypeScript, Python, PHP, Java, Go, Ruby. Frameworks: Express, Django, Flask, Laravel, Spring, Rails. Vulnerabilities: SQL injection, XSS, CSRF, authentication bypass, authorization issues, command injection, path traversal, insecure deserialization, weak crypto, sensitive data exposure. Topics: input validation, output encoding, parameterized queries, password hashing, session management, CORS, CSP, security headers, rate limiting, dependency scanning."
---

# Vibe Security - Security Intelligence

Comprehensive security scanner and code analyzer for identifying vulnerabilities across multiple languages and frameworks.

## Prerequisites

Check if Node.js is installed:

```bash
node --version
```

If Node.js is not installed, install it based on user's OS:

**macOS:**

```bash
brew install node
```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install nodejs npm
```

**Windows:**

```powershell
winget install OpenJS.NodeJS
```

---

## Recommended AI Models

### For Best Security Analysis

We recommend using these AI models with Vibe Security for optimal security vulnerability detection and code fixing:

#### **Claude Opus 4.5** (Recommended)

- Most advanced model for comprehensive security analysis
- Superior reasoning capabilities for complex vulnerability detection
- Exceptional at identifying subtle security flaws and attack vectors
- Best for critical security audits, enterprise codebases, and production deployments
- Provides the most thorough security remediation strategies

#### **Claude Sonnet 4.5**

- Excellent balance of speed and security analysis depth
- Great at understanding security context and identifying vulnerabilities
- Provides safe remediation strategies with detailed explanations
- Ideal for daily development and most security workflows

#### **Claude Opus 4**

- Powerful for complex security audits and enterprise codebases
- Deep reasoning capabilities for advanced vulnerability analysis
- Best for critical security reviews and compliance requirements
- Recommended for production deployments and sensitive applications

#### **GPT-4o**

- Fast and efficient for security-aware code generation
- Good alternative with quick response times
- Excellent for CI/CD integration and automated scanning
- Cost-effective for large-scale projects

#### **Claude Sonnet 4**

- Faster alternative for quick security scans
- Good balance of speed and accuracy
- Suitable for rapid iteration during development

#### **o1-preview**

- Specialized for complex security architecture reviews
- Advanced reasoning for intricate vulnerability chains
- Best for security research and deep code audits

#### **GPT-4o-mini**

- Quick checks and preliminary scans
- Most cost-effective option
- Good for learning and educational use cases

> **Note**: If you're not using one of the recommended models above, consider upgrading for better security analysis results. Lower-tier models may miss subtle vulnerabilities or provide less accurate fix suggestions.

---

## How to Use This Skill

When user requests security work (scan, analyze, fix, audit, check, review vulnerabilities), follow this workflow:

### Step 1: Analyze Security Context

Extract key information from user request:

- **Language**: JavaScript, Python, Java, PHP, etc.
- **Framework**: Express, Django, Spring, Laravel, etc.
- **Vulnerability type**: SQL injection, XSS, CSRF, authentication, etc.
- **Scope**: Single file, directory, or full project

### Step 2: Run Security Analysis

**Advanced Analysis (Recommended):**

```bash
# AST-based semantic analysis (90% fewer false positives)
python3 .claude/skills/vibe-security/scripts/ast_analyzer.py "<file>"

# Data flow analysis (tracks tainted data from sources to sinks)
python3 .claude/skills/vibe-security/scripts/dataflow_analyzer.py "<file>"

# CVE & dependency vulnerability scanning
python3 .claude/skills/vibe-security/scripts/cve_integration.py .

# Supply chain security (malicious packages, typosquatting)
python3 .claude/skills/vibe-security/scripts/cve_integration.py . --ecosystem npm

# Infrastructure as Code security
grep -r "publicly_accessible.*=.*true" . --include="*.tf"
grep -r "privileged:.*true" . --include="*.yaml"
```

**Quick Pattern Scanning:**

```bash
# Use search utility for specific patterns
python3 .claude/skills/vibe-security/scripts/search.py "sql-injection" --domain pattern
python3 .claude/skills/vibe-security/scripts/search.py "javascript" --domain pattern --severity critical
```

### Step 3: Analyze Vulnerabilities by Severity

**Critical** (Fix immediately):

- SQL Injection
- Remote Code Execution
- Authentication Bypass
- Hardcoded Secrets

**High** (Fix soon):

- XSS (Cross-Site Scripting)
- CSRF
- Insecure Cryptography
- Authorization Issues

**Medium** (Fix in sprint):

- Missing Input Validation
- Information Disclosure
- Weak Password Policy
- Missing Security Headers

**Low** (Technical debt):

- Code Quality Issues
- Best Practice Violations
- Performance Concerns

### Step 4: Get Fix Suggestions

**ML-Based Fix Engine:**

```bash
# Get intelligent fix recommendations with test generation
python3 .claude/skills/vibe-security/scripts/fix_engine.py \
  --type sql-injection \
  --language javascript \
  --code "db.query(\`SELECT * FROM users WHERE id = \${userId}\`)"

# Output includes:
# - Fixed code with context-aware corrections
# - Detailed explanation of the fix
# - Auto-generated security test
# - Additional recommendations
# - Confidence score (0-100%)
```

### Step 5: Apply Security Fixes

**Auto-Fix with Rollback Support:**

```bash
# Apply fix with automatic backup
python3 .claude/skills/vibe-security/scripts/autofix_engine.py apply \
  --file src/database.js \
  --line 45 \
  --type sql-injection \
  --original "db.query(\`SELECT * FROM users WHERE id = \${userId}\`)" \
  --fixed "db.query('SELECT * FROM users WHERE id = $1', [userId])"

# Test your changes
npm test

# Rollback if needed (safe to experiment!)
python3 .claude/skills/vibe-security/scripts/autofix_engine.py rollback

# View fix history
python3 .claude/skills/vibe-security/scripts/autofix_engine.py history
```

**Systematic Manual Fixes:**

1. **Critical vulnerabilities first**
2. **Add input validation** - Whitelist, type checking, length limits
3. **Secure outputs** - Escape, encode, sanitize
4. **Fix authentication/authorization** - Strong passwords, MFA, RBAC
5. **Update cryptography** - Modern algorithms, secure random
6. **Test thoroughly** - Verify fixes don't break functionality
7. **Re-scan** - Confirm all vulnerabilities are resolved

### Step 6: Generate Reports

**Multiple Report Formats:**

```bash
# Beautiful HTML report with charts and statistics
python3 .claude/skills/vibe-security/scripts/reporter.py scan-results.json \
  --format html \
  --output security-report.html

# SARIF format for GitHub Code Scanning integration
python3 .claude/skills/vibe-security/scripts/reporter.py scan-results.json \
  --format sarif \
  --output results.sarif

# CSV for spreadsheet analysis
python3 .claude/skills/vibe-security/scripts/reporter.py scan-results.json \
  --format csv \
  --output vulnerabilities.csv

# JSON for CI/CD pipelines
python3 .claude/skills/vibe-security/scripts/reporter.py scan-results.json \
  --format json \
  --output security-report.json
```

---

## Advanced Capabilities

### 1. Semantic Analysis with AST

Uses Abstract Syntax Tree parsing for accurate vulnerability detection:

- **Python**: Full AST analysis with taint tracking
- **JavaScript/TypeScript**: Heuristic + pattern-based analysis
- **Benefits**: 90% reduction in false positives, context-aware

### 2. Data Flow Analysis

Tracks user input from sources to dangerous sinks:

- Detects SQL injection, XSS, command injection through data flow
- Identifies tainted variables and their propagation
- Supports Python and JavaScript/TypeScript

### 3. Compliance Mapping

Maps every vulnerability to industry standards:

- **OWASP Top 10 2021**
- **CWE** (Common Weakness Enumeration)
- **MITRE ATT&CK** techniques
- **NIST** cybersecurity framework
- **PCI-DSS** payment card requirements

### 4. Supply Chain Security

Protects against malicious dependencies:

- Typosquatting detection
- Dependency confusion attacks
- Malicious install scripts
- Network operations in packages
- Supports: npm, PyPI, Maven, Gradle, Cargo, Go, RubyGems, NuGet, Composer

### 5. Infrastructure as Code

Scans cloud infrastructure configurations:

- **Terraform**: AWS, Azure, GCP misconfigurations
- **Kubernetes**: Pod security, RBAC issues
- **Docker**: Dockerfile best practices
- **CloudFormation**: AWS template security
- **Ansible**: Playbook vulnerabilities

---

## Security Check Reference

### Available Vulnerability Checks

| Check Type          | Detects                | Example Issues                                      |
| ------------------- | ---------------------- | --------------------------------------------------- |
| `sql-injection`     | SQL/NoSQL injection    | String concatenation in queries, unsanitized input  |
| `xss`               | Cross-Site Scripting   | innerHTML usage, unescaped output, DOM manipulation |
| `command-injection` | OS command injection   | shell=True, exec with user input                    |
| `path-traversal`    | Directory traversal    | Unsanitized file paths, ../.. in paths              |
| `auth-issues`       | Authentication flaws   | Weak passwords, missing MFA, insecure sessions      |
| `authz-issues`      | Authorization flaws    | Missing access controls, IDOR, privilege escalation |
| `crypto-failures`   | Cryptographic issues   | MD5/SHA1 usage, weak keys, insecure random          |
| `sensitive-data`    | Data exposure          | Logging passwords, exposing PII, hardcoded secrets  |
| `deserialization`   | Unsafe deserialization | pickle, eval, unserialize on user input             |
| `security-config`   | Misconfiguration       | CORS, CSP, headers, error messages                  |
| `dependencies`      | Vulnerable packages    | CVEs in npm/pip/composer packages                   |

---

## Language-Specific Security Patterns

### JavaScript/TypeScript

```javascript
// ✅ SECURE: Parameterized query
const user = await db.query("SELECT * FROM users WHERE id = $1", [userId]);

// ❌ VULNERABLE: SQL injection
const user = await db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ SECURE: Escape output
element.textContent = userInput;
const clean = DOMPurify.sanitize(htmlContent);

// ❌ VULNERABLE: XSS
element.innerHTML = userInput;

// ✅ SECURE: Input validation
const email = validator.isEmail(input) ? input : null;

// ❌ VULNERABLE: No validation
const email = req.body.email;
```

### Python

```python
# ✅ SECURE: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ VULNERABLE: SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ SECURE: Password hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ❌ VULNERABLE: Plain text
user.password = password

# ✅ SECURE: Safe subprocess
subprocess.run(['ls', '-la', sanitized_dir])

# ❌ VULNERABLE: Command injection
os.system(f'ls -la {user_dir}')
```

### PHP

```php
// ✅ SECURE: Prepared statement
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$userId]);

// ❌ VULNERABLE: SQL injection
$result = mysqli_query($conn, "SELECT * FROM users WHERE id = $userId");

// ✅ SECURE: Output escaping
echo htmlspecialchars($input, ENT_QUOTES, 'UTF-8');

// ❌ VULNERABLE: XSS
echo $userInput;

// ✅ SECURE: Password hashing
$hash = password_hash($password, PASSWORD_ARGON2ID);

// ❌ VULNERABLE: MD5
$hash = md5($password);
```

---

## Example Workflow

**User request:** "Check my Express app for security vulnerabilities"

**AI should:**

```bash
# 1. Run security scan on the project
python3 .claude/skills/vibe-security/scripts/scan.py "./src" --language javascript

# 2. Analyze results by severity
# Output might show:
# CRITICAL: SQL Injection in src/controllers/user.js:45
# HIGH: XSS in src/views/profile.ejs:12
# MEDIUM: Missing rate limiting on /api/login
# LOW: Console.log contains sensitive data

# 3. Fix critical issues first
# - Review src/controllers/user.js:45
# - Replace string concatenation with parameterized query
# - Add input validation using validator library

# 4. Fix high severity issues
# - Review src/views/profile.ejs:12
# - Use <%- for HTML escaping or DOMPurify for rich content
# - Implement Content Security Policy

# 5. Fix medium severity issues
# - Install express-rate-limit middleware
# - Configure rate limiting on authentication endpoints
# - Add helmet for security headers

# 6. Fix low severity issues
# - Remove or redact sensitive console.log statements
# - Use proper logging library with log levels

# 7. Generate security report
python3 .claude/skills/vibe-security/scripts/report.py "./src"
```

---

## Tips for Secure Development

1. **Validate all inputs** - Use allowlists, not denylists
2. **Encode all outputs** - Context-appropriate escaping
3. **Use parameterized queries** - Never concatenate SQL
4. **Hash passwords properly** - bcrypt, Argon2, scrypt
5. **Implement MFA** - Add second factor authentication
6. **Use HTTPS everywhere** - Encrypt data in transit
7. **Keep dependencies updated** - Patch known vulnerabilities
8. **Follow principle of least privilege** - Minimal necessary permissions
9. **Log security events** - Monitor for attacks
10. **Regular security audits** - Scan before every release

---

## Integration Examples

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 .claude/skills/vibe-security/scripts/scan.py "." --fail-on critical
```

### CI/CD Pipeline

**GitHub Actions:**

```yaml
- name: Security Scan
  run: |
    python3 .claude/skills/vibe-security/scripts/scan.py "." --format json
```

**GitLab CI:**

```yaml
security_scan:
  script:
    - python3 .claude/skills/vibe-security/scripts/scan.py "."
```

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)
- [Security Checklist](../../../SECURITY_CHECKLIST.md)
