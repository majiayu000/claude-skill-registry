---
name: security-analysis
description: Perform static security review of modified code, identifying vulnerabilities and recommending mitigations
category: security
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Security Analysis

Inspect the repository for code changes and recommend changes specializing in secure software design and vulnerability mitigations. Perform a static security review.

## Procedure

### Phase 1 - Get the Changes
1. Get all changes in this branch compared to the default branch since it diverged
2. Scoped from those changes, analyze code from modified and added code (functions, configuration, etc.)
3. Identify vulnerabilities or risky patterns:
   - Reentrancy
   - Unchecked inputs
   - Unsafe deserialization
   - Race conditions
   - Privilege escalation
   - Misuse of cryptography
   - Injection vulnerabilities (SQL, command, etc.)
   - Path traversal
   - XSS/CSRF potential
4. Detect non-compliance with internal security policies or coding standards
5. Highlight dependency or permission risks introduced by new imports or external calls
6. Suggest minimal, safe code-level remediations that preserve logic

### Phase 2 - Return Recommendations

Return Markdown structured as follows:

```markdown
# Recommendations

High-level explanation of risk and next steps

## Risk Level Critical
**functionName**
location: src/path/to/file.ts `functionName`
type: Type of issue (e.g., injection, privilege escalation)
description: Detailed explanation of the issue
recommendation: Specific mitigation with code-level detail

## Risk Level High
...

## Risk Level Medium
...

## Risk Level Low
...
```

## Constraints
- Never invent context or external data
- Assume principle of least privilege and functional immutability
- Focus on verifiable, code-level evidence
- Prioritize actionable recommendations over theoretical concerns