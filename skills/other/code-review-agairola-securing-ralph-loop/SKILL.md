---
name: code-review
description: Security-focused code review before committing
allowed-tools: Read, Grep, Glob
---

# Security Code Review

Review code changes for security issues before committing.

## Purpose

This skill performs a security-focused code review to catch common vulnerabilities before they make it into the codebase. Run this before committing to self-check your changes.

## Security Checklist

When reviewing code, check for:

### Secrets & Credentials
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] No AWS credentials in code
- [ ] No private keys or certificates
- [ ] Environment variables used for sensitive config

### Injection Vulnerabilities
- [ ] No SQL injection (use parameterized queries)
- [ ] No command injection (avoid shell=True, sanitize inputs)
- [ ] No LDAP injection
- [ ] No XPath injection

### Input Validation
- [ ] No path traversal (validate file paths)
- [ ] No open redirects
- [ ] User input properly sanitized
- [ ] File uploads validated

### Dependencies
- [ ] Dependencies are from trusted sources
- [ ] No wildcard version specifications
- [ ] Lock files present and updated

### General Security
- [ ] File permissions are appropriate
- [ ] No debug code left in
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't include sensitive data

## Usage

```
/code-review
```

Run this skill before committing to perform a self-check on your changes.

## Output

The skill will:
1. Identify changed files using `git diff`
2. Review each file against the security checklist
3. Report any findings with severity levels
4. Provide remediation suggestions

## Example Findings

```
[HIGH] src/api.py:42 - Hardcoded API key detected
  → Move to environment variable: os.getenv('API_KEY')

[MEDIUM] src/db.py:15 - SQL query uses string formatting
  → Use parameterized query: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

[LOW] src/utils.py:8 - Debug print statement
  → Remove before committing
```
