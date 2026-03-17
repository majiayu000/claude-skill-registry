---
name: quality-security-scan
description: Scan code for security vulnerabilities and unsafe patterns. Use before committing sensitive code or in security reviews.
mcp_fallback: none
category: quality
agent: test-engineer
user-invocable: false
---

# Security Scan Skill

Scan code for security vulnerabilities and unsafe patterns.

## When to Use

- Before committing code with secrets
- Security review process
- Handling sensitive data
- Pre-release security audit

## Quick Reference

```bash
# Check for committed secrets
./scripts/scan_for_secrets.sh

# Check Python dependencies
pip-audit

# Check unsafe patterns
./scripts/check_unsafe_patterns.sh
```

## Security Checks

### 1. Secrets Detection

```bash
./scripts/scan_for_secrets.sh
```

Detects:

- API keys and tokens
- Passwords and credentials
- Private keys (.key, .pem)
- AWS credentials
- Database credentials

### 2. Dependency Vulnerabilities

```bash
pip-audit              # Python packages
safety check          # Alternative scanner
```

### 3. Unsafe Code Patterns

```bash
./scripts/check_unsafe_patterns.sh
```

Looks for:

- Hardcoded credentials
- SQL injection vectors
- Unsafe file operations
- Unvalidated input

## Prevention

### .gitignore

Ensure sensitive files ignored:

```text
.env
.env.local
*.key
*.pem
credentials.json
secrets/
aws/
google/
api-keys.txt
```

### Pre-commit Hook

```yaml
- id: detect-private-key
  name: Detect Private Key
- id: detect-aws-credentials
  name: Detect AWS Credentials
```

## Common Vulnerabilities

### Hardcoded Secrets

```python
# ❌ Wrong
API_KEY = "sk_live_1234567890"
PASSWORD = "admin123"

# ✅ Correct
import os
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("DB_PASSWORD")
```

### Unsafe File Operations

```mojo
# ❌ Potential path traversal
fn load_file(path: String):
    var data = open(path).read()
    return data

# ✅ Validate path
fn load_file(path: String) -> String:
    if not is_safe_path(path):
        return error("Invalid path")
    return open(path).read()
```

### SQL Injection

```python
# ❌ Unsafe - string concatenation
query = "SELECT * FROM users WHERE id = " + user_id

# ✅ Safe - parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

## Workflow

```bash
# 1. Before committing
./scripts/scan_for_secrets.sh

# 2. Check dependencies
pip-audit

# 3. Check unsafe patterns
./scripts/check_unsafe_patterns.sh

# 4. If no issues, commit
git add .
git commit -m "feat: new feature"

# 5. If issues found, fix before committing
# ... move secrets to .env ...
# ... update dependencies ...
# ... fix unsafe patterns ...
```

## Error Handling

| Issue | Fix |
|-------|-----|
| "Secret detected" | Move to .env, add to .gitignore |
| "Unsafe dependency" | Update to patched version |
| "Unsafe pattern" | Refactor code to use safe approach |

## Best Practices

1. **Never commit secrets** - Use environment variables
2. **Keep dependencies updated** - Run pip-audit regularly
3. **Validate input** - Always validate user input
4. **Use safe libraries** - Prefer parameterized queries, etc.
5. **Review PRs** - Include security review in PR process

## Scripts Available

- `scripts/scan_for_secrets.sh` - Detect committed secrets
- `scripts/check_unsafe_patterns.sh` - Check code patterns
- `pip-audit` - Check Python vulnerabilities
- `safety check` - Alternative vulnerability scanner

## References

- OWASP Top 10: <https://owasp.org/www-project-top-ten/>
- Security best practices: See security documentation
- Related skill: `quality-run-linters` for complete quality check
