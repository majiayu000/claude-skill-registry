---
name: sec-context-depth
description: Comprehensive AI code security review using 27 sec-context anti-patterns. Use for code review when security vulnerabilities are suspected, especially for AI-generated code.
allowed-tools: Read,Glob,mcp__ast-grep__*,Bash
---

# Sec-Context Depth: AI Code Security Anti-Patterns Review (v2.68)

Use this skill to perform comprehensive security reviews on AI-generated code, detecting **27 security anti-patterns** from the sec-context framework.

> Based on: [Arcanum-Sec/sec-context](https://github.com/Arcanum-Sec/sec-context)
> Source: 150+ security research sources, OWASP, CWE

## Statistics (Why This Matters)

- **86% XSS failure rate** in AI-generated code
- **72% of Java AI code** contains vulnerabilities
- AI code is **2.74x more likely** to have XSS vulnerabilities
- **81% of organizations** have shipped vulnerable AI-generated code
- **5-21% of AI-suggested packages don't exist** (slopsquatting)

---

## Priority Classification

| Priority | Score | Action | Count |
|----------|-------|--------|-------|
| **P0 Critical** | 21-24 | BLOCKING - Must fix before merge | 13 patterns |
| **P1 High** | 18-20 | BLOCKING - Should fix before merge | 8 patterns |
| **P2 Medium** | 15-17 | ADVISORY - Review and fix if feasible | 6 patterns |

---

## P0: CRITICAL PATTERNS (13)

### 1. Hardcoded Secrets (CWE-798) - Priority 23
### 2. API Key Prefixes (CWE-798) - Priority 23
### 3. Private Keys (CWE-321) - Priority 23
### 4. SQL Injection - String Concat (CWE-89) - Priority 22
### 5. SQL Injection - f-string (CWE-89) - Priority 22
### 6. Command Injection (CWE-78) - Priority 21
### 7. Command Injection - Concat (CWE-78) - Priority 21
### 8. XSS - innerHTML (CWE-79) - Priority 23
### 9. XSS - document.write (CWE-79) - Priority 23
### 10. XSS - React Unsafe (CWE-79) - Priority 23
### 11. NoSQL Injection (CWE-943) - Priority 22
### 12. Template Injection SSTI (CWE-1336) - Priority 22
### 13. Hardcoded Encryption Key (CWE-798) - Priority 22

## P1: HIGH PRIORITY PATTERNS (8)

### 14. JWT None Algorithm (CWE-287) - Priority 22
### 15. Weak Hash MD5/SHA1 (CWE-327) - Priority 20
### 16. ECB Mode (CWE-327) - Priority 20
### 17. DES/RC4 (CWE-327) - Priority 20
### 18. Insecure Random (CWE-330) - Priority 18
### 19. Path Traversal (CWE-22) - Priority 20
### 20. LDAP Injection (CWE-90) - Priority 20
### 21. XPath Injection (CWE-643) - Priority 20

## P2: MEDIUM PRIORITY PATTERNS (6)

### 22. Open CORS (CWE-346) - Priority 17
### 23. Verbose Errors (CWE-209) - Priority 16
### 24. Insecure Temp Files (CWE-377) - Priority 16
### 25. Unvalidated Redirect (CWE-601) - Priority 16
### 26. Insecure Deserialization (CWE-502) - Priority 18
### 27. Debug Mode (CWE-489) - Priority 15

---

## Detection Checklist

When reviewing code, systematically check:

- [ ] **Secrets**: Environment variables, not hardcoded
- [ ] **Queries**: Parameterized, not concatenated
- [ ] **Commands**: Array arguments, shell=False
- [ ] **HTML**: textContent/sanitized, not innerHTML
- [ ] **Crypto**: Modern algorithms (AES-GCM, bcrypt)
- [ ] **Random**: Cryptographic sources
- [ ] **Files**: Path validation, secure temp
- [ ] **Errors**: Generic messages in production
- [ ] **Auth**: Session regeneration, rate limiting

---

## Integration with Hook

The sec-context-validate.sh hook automatically checks these 27 patterns on every Edit/Write operation.

---

## Related Skills

- @security-auditor - Deep security analysis
- @code-reviewer - General code quality
- /adversarial - Adversarial spec refinement
