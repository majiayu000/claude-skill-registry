---
description: Review code for issues, improvements, and best practices.
---

# Code Review

Review code for issues, improvements, and best practices.

## Instructions

When asked to review code, perform a thorough analysis looking for:

### 1. Security Issues (Critical) - OWASP Top 10

- [ ] **Injection**: SQL, command, LDAP injection via string concatenation
- [ ] **XSS**: innerHTML, dangerouslySetInnerHTML, v-html with user data
- [ ] **Broken Auth**: Hardcoded credentials, weak passwords, missing rate limiting
- [ ] **Sensitive Data Exposure**: Secrets in code, sensitive data in logs/URLs
- [ ] **Broken Access Control**: Missing auth checks, IDOR, privilege escalation
- [ ] **Security Misconfiguration**: Debug mode, default credentials, verbose errors
- [ ] **Insecure Deserialization**: pickle, eval() with user input
- [ ] **Vulnerable Dependencies**: Outdated packages with known CVEs

```typescript
// VULNERABLE - SQL injection
const query = `SELECT * FROM users WHERE name = '${userInput}'`;

// SAFE - parameterized query
const query = "SELECT * FROM users WHERE name = ?";
db.execute(query, [userInput]);
```

```typescript
// VULNERABLE - XSS
element.innerHTML = userInput;

// SAFE
element.textContent = userInput;
// or with sanitization
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 2. Error Handling (High)

- [ ] Empty catch blocks
- [ ] Missing error boundaries
- [ ] Unhandled promise rejections
- [ ] Missing null/undefined checks
- [ ] Silent failures

### 3. Type Safety (High for TypeScript)

- [ ] Usage of `any` type
- [ ] Missing type annotations
- [ ] Type assertions that could fail
- [ ] Inconsistent types

### 4. Code Quality (Medium)

- [ ] Functions over 50 lines
- [ ] Deep nesting (4+ levels)
- [ ] Code duplication
- [ ] Magic numbers
- [ ] Unclear variable names
- [ ] Missing or outdated comments

### 5. Performance (Medium)

- [ ] N+1 query patterns
- [ ] Missing memoization for expensive operations
- [ ] Unnecessary re-renders (React)
- [ ] Large bundle imports
- [ ] Missing pagination

### 6. Maintainability (Low)

- [ ] Dead code
- [ ] Commented-out code
- [ ] TODOs that should be addressed
- [ ] Inconsistent patterns
- [ ] Missing tests

## Output Format

Structure your review like this:

```markdown
## Code Review: [filename or description]

### Summary
[1-2 sentence overview of the code quality]

### Critical Issues
These must be fixed before merging:

1. **[Issue Title]** (Line X)
   - Problem: [What's wrong]
   - Risk: [What could happen]
   - Fix: [How to fix it]
   ```
   [Code suggestion if applicable]
   ```

### Improvements
These should be addressed:

1. **[Issue Title]** (Line X)
   - Current: [What it does now]
   - Better: [What it should do]
   - Why: [Benefit of changing]

### Minor Suggestions
Nice to have, low priority:

1. **[Suggestion]** (Line X)
   - [Brief explanation]

### What's Good
[Acknowledge good patterns and practices in the code]

### Verdict
[ ] Ready to merge
[ ] Needs minor changes
[ ] Needs significant changes
[ ] Needs rewrite
```

## Severity Guide

| Severity | Block Merge? | Examples |
|----------|--------------|----------|
| Critical | Yes | Security vulnerabilities, data loss risks |
| High | Yes | Missing error handling, type safety issues |
| Medium | Review | Performance issues, code quality |
| Low | No | Style preferences, minor improvements |

## Review Modes

### Quick Review
Focus only on critical and high-severity issues:
> "Quick review of this code"

### Full Review
Check everything:
> "Full review of src/api/users.ts"

### Security Review (OWASP Top 10)
Deep dive on security - injection, XSS, auth, access control, secrets:
> "Security review of the authentication flow"
> "Check for SQL injection vulnerabilities"
> "Full security audit of the API endpoints"

### Performance Review
Focus on performance:
> "Performance review of the dashboard page"

### Dependency Audit
Check for vulnerable dependencies:
> "Check our dependencies for known vulnerabilities"

## Be Constructive

- Explain **why** something is an issue, not just that it is
- Provide **specific** suggestions for fixes
- Acknowledge what's **done well**
- Be **respectful** - we all make mistakes
- Focus on the **code**, not the coder
