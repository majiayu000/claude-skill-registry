---
name: check-security
description: Perform a security code review on pending changes or specified files
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Bash(git diff*), Bash(git show*), Bash(git log*), Read, Grep, Glob
---

# Security Code Review

Perform a comprehensive security audit of the code changes.

## Scope

Review changes from: `!git diff --name-only HEAD~1` or files specified in $ARGUMENTS

## Security Checklist

### 1. Injection Vulnerabilities
- [ ] **SQL Injection**: Verify all database queries use parameterized queries (`sql` template literal)
- [ ] **Command Injection**: Check for unsanitized input in shell commands or child processes
- [ ] **XSS**: Validate output encoding in API responses and templates
- [ ] **NoSQL Injection**: Check Redis and other NoSQL operations

### 2. Authentication & Authorization
- [ ] **Authentication bypass**: Verify auth middleware is applied to protected routes
- [ ] **Authorization checks**: Confirm permission checks match the action's sensitivity
- [ ] **Session management**: Check for session fixation, timeout issues
- [ ] **JWT handling**: Verify token validation, expiration, and signature checks

### 3. Data Exposure
- [ ] **Sensitive data in logs**: Check for PII, tokens, or credentials in log statements
- [ ] **Error messages**: Ensure errors don't leak internal details
- [ ] **API responses**: Verify only necessary fields are returned
- [ ] **File paths**: Check for path traversal vulnerabilities

### 4. Input Validation
- [ ] **Schema validation**: Verify AJV validators cover all inputs
- [ ] **Type coercion**: Check for unexpected type conversions
- [ ] **Size limits**: Verify file upload and request body limits
- [ ] **Rate limiting**: Confirm rate limits on sensitive endpoints

### 5. Dependencies
- [ ] **New dependencies**: Review any new npm/deno packages for known vulnerabilities
- [ ] **Outdated packages**: Flag significantly outdated security-critical packages

### 6. Secrets Management
- [ ] **Hardcoded secrets**: Check for API keys, passwords, tokens in code
- [ ] **Environment variables**: Verify secrets are loaded from environment
- [ ] **Talisman compliance**: Ensure changes won't trigger secret detection

### 7. Deno-Specific
- [ ] **Permissions**: Check `--allow-*` flags aren't overly permissive
- [ ] **Import sources**: Verify external imports are from trusted sources (jsr, npm)

## Output Format

Provide a structured report:

```markdown
## Security Review Summary

**Risk Level**: [LOW | MEDIUM | HIGH | CRITICAL]
**Files Reviewed**: X files

### Findings

#### [SEVERITY] Finding Title
- **File**: path/to/file.ts:line
- **Issue**: Description of the vulnerability
- **Impact**: What could happen if exploited
- **Recommendation**: How to fix it

### Approved Changes
- List of changes that passed security review

### Action Required
- [ ] Fix critical/high issues before merge
- [ ] Address medium issues in follow-up
- [ ] Low issues can be tracked as tech debt
```

## Invocation

```
/check-security                    # Review uncommitted changes
/check-security src/pdc/services/  # Review specific directory
/check-security HEAD~3..HEAD       # Review last 3 commits
```
