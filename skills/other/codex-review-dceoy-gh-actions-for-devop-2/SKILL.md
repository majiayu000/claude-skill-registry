---
name: codex-review
description: Perform code reviews using OpenAI Codex CLI to identify bugs, security vulnerabilities, performance issues, and code quality problems. Use when the user asks to review code, check for issues, security audit, or before committing. Requires Codex CLI installed.
allowed-tools: Bash, Read, Grep, Glob
---

# Codex Review Skill

Use OpenAI Codex CLI to perform automated code reviews that identify issues and suggest improvements. This is a **read-only** analysis skill.

## When to Use

- User asks to "review" code
- User wants to check for bugs or issues
- User mentions "security", "performance", or "quality"
- Before committing code
- During pull request review
- User asks "what's wrong with this code?"

## Prerequisites

Verify Codex CLI is available:

```bash
codex --version  # Should display installed version
```

## Basic Usage

### Step 1: Determine Scope

What to review:

- Uncommitted changes (default)
- Specific file(s)
- Last commit
- Pull request
- Entire codebase

### Step 2: Check Current State

```bash
git status          # See what's changed
git diff --stat     # Summary of changes
git diff            # Detailed changes
```

### Step 3: Execute Codex Review

Run Codex with review-focused prompt:

```bash
codex --sandbox=read-only exec "Perform comprehensive code review of [SCOPE].

Check for:
1. CRITICAL ISSUES (must fix):
   - Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
   - Potential runtime errors
   - Data loss risks
   - Breaking changes

2. IMPORTANT ISSUES (should fix):
   - Logic bugs
   - Performance problems
   - Type safety gaps
   - Error handling issues

3. SUGGESTIONS (consider):
   - Code quality improvements
   - Refactoring opportunities
   - Better patterns
   - Documentation needs

4. POSITIVE OBSERVATIONS:
   - Best practices followed
   - Good patterns used

For each issue:
- Severity level (Critical/Important/Suggestion)
- File path and line number
- Clear description of the problem
- Why it's a problem
- How to fix it

Do NOT make any changes - this is review only."
```

### Step 4: Present Findings

Organize results by severity:

- 🔴 Critical Issues
- 🟡 Important Issues
- 🟢 Suggestions
- ✅ Positive Observations

## Example Reviews

### Review Uncommitted Changes

```bash
codex --sandbox=read-only exec "Review all uncommitted changes for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code quality problems
- Missing error handling
Do NOT modify code."
```

### Security-Focused Review

```bash
codex --sandbox=read-only exec "Security review of src/auth/*.ts:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication bypass
- Authorization flaws
- Secrets in code
- Input validation gaps
Provide severity level and fix suggestions. Do NOT modify code."
```

### Performance Review

```bash
codex --sandbox=read-only exec "Performance review of src/components/*.tsx:
- Unnecessary re-renders
- Missing React.memo, useMemo, useCallback
- Inefficient algorithms
- Memory leaks
- Large bundle impacts
Provide specific optimization suggestions. Do NOT modify code."
```

### Pre-Commit Review

```bash
codex --sandbox=read-only exec "Quick review of staged changes for:
- console.log statements
- Commented-out code
- Unused imports
- TODO comments
- Missing error handling
- Type errors
Exit with error if critical issues found. Do NOT modify code."
```

## Review Focus Areas

### General Review

```bash
# Comprehensive review of all aspects
codex --sandbox=read-only exec "Comprehensive review covering: security, performance, code quality, architecture, testing, accessibility. Do NOT modify code."
```

### Security Audit

```bash
# OWASP Top 10 and security best practices
codex --sandbox=read-only exec "Security audit focusing on: SQL injection, XSS, CSRF, authentication, authorization, secrets, input validation. Do NOT modify code."
```

### Architecture Review

```bash
# SOLID principles and design patterns
codex --sandbox=read-only exec "Architecture review: SOLID principles, separation of concerns, dependency management, code organization, design patterns. Do NOT modify code."
```

### Accessibility Review

```bash
# WCAG compliance
codex --sandbox=read-only exec "Accessibility review: ARIA labels, keyboard navigation, screen reader support, color contrast, semantic HTML. Do NOT modify code."
```

## Output Format

Structure review results:

````markdown
# Code Review: [Scope]

## Summary

- Files reviewed: 3
- Issues found: 5 (Critical: 1, Important: 2, Suggestions: 2)
- Estimated fix time: 2 hours

## 🔴 Critical Issues (Fix Immediately)

### src/auth/login.ts:45 - SQL Injection Vulnerability

**Severity:** Critical
**Category:** Security

**Problem:**
Direct string interpolation in SQL query allows SQL injection.

**Why it matters:**
Attacker can execute arbitrary SQL commands, steal data, or drop tables.

**How to fix:**
Use parameterized queries:

```typescript
// Before (vulnerable)
db.query(`SELECT * FROM users WHERE email = '${email}'`);

// After (safe)
db.query("SELECT * FROM users WHERE email = ?", [email]);
```
````

---

## 🟡 Important Issues (Should Fix)

[Same format as critical]

---

## 🟢 Suggestions (Consider Improving)

[Same format]

---

## ✅ Positive Observations

- src/utils/validation.ts:23 - Excellent input sanitization
- src/hooks/useAuth.ts:67 - Proper cleanup in useEffect

---

## Recommended Actions

1. **Immediate:** Fix SQL injection in auth/login.ts:45
2. **Soon:** Address performance issue in components/UserList.tsx
3. **Consider:** Refactor large function at utils/helpers.ts:120

```

## Best Practices

✅ **DO:**
- Categorize by severity (Critical/Important/Suggestion)
- Include specific file paths and line numbers
- Explain WHY something is a problem
- Provide clear fix suggestions
- Note positive observations too

❌ **DON'T:**
- Make code modifications (use codex-exec for that)
- Skip verification of findings
- Report false positives without investigation
- Be purely negative without noting good practices

## Verification

After getting Codex's review:
1. Verify file paths and line numbers are correct
2. Check if issues are real (not false positives)
3. Assess severity appropriately
4. Add context from your knowledge of the code

## Error Handling

**If Codex not found:**
```

Codex CLI is not available. Ensure it's installed and in your PATH.

````

**If too many issues:**
- Focus on critical issues first
- Group related issues
- Break into multiple focused reviews

**If false positives:**
- Manually verify each issue
- Filter out non-issues
- Clarify with more specific review scope

## Integration Patterns

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
codex --sandbox=read-only exec "Quick review of staged changes for critical issues" --yes
exit $?
````

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Codex Review
  run: |
    codex --sandbox=read-only exec "Review PR changes for security and quality" > review.md
```

## Review Checklist Templates

### General Checklist

```
- [ ] No console.log or debug statements
- [ ] No commented-out code
- [ ] All imports are used
- [ ] No TODO comments (or tracked in issues)
- [ ] Error handling present
- [ ] TypeScript types complete
- [ ] No security vulnerabilities
- [ ] Tests pass
```

### Security Checklist

```
- [ ] No SQL injection risks
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] No secrets in code
- [ ] Authentication/authorization correct
- [ ] HTTPS enforced
- [ ] CSRF protection enabled
```

## Related Skills

- **codex-ask**: For understanding code before reviewing
- **codex-exec**: For fixing issues found in review

## Tips for Better Reviews

1. **Be specific**: "Review src/auth.ts for security" vs "Review code"
2. **Define scope**: Specific files > entire codebase
3. **Choose focus**: Security audit vs general review
4. **Iterate**: Review → Fix → Re-review
5. **Combine skills**: codex-ask → codex-review → codex-exec

## Limitations

- Static analysis only (cannot run code)
- May generate false positives
- Cannot understand business logic
- Cannot test runtime behavior
- Limited by context window size

---

**Remember**: This skill is READ-ONLY. To fix issues found, use the `codex-exec` skill.
