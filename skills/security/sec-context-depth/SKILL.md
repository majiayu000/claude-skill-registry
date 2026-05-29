---
# VERSION: 2.90.1
name: sec-context-depth
description: Comprehensive AI code security review using 27 sec-context anti-patterns. Use for code review when security vulnerabilities are suspected, especially for AI-generated code.
allowed-tools: Read,Glob,Grep,Bash
---

# Sec-Context Depth: AI Code Security Anti-Patterns Review

## v2.90.1 Changes

- **References-driven**: Uses LOCAL reference files with full BAD/GOOD examples
- **Model-agnostic**: Works with any configured model
- **No flags required**: Works with the configured default model

Perform comprehensive security reviews on AI-generated code, detecting **27 security anti-patterns** from the sec-context framework.

> Based on: [Arcanum-Sec/sec-context](https://github.com/Arcanum-Sec/sec-context)
> Source: 150+ security research sources, OWASP, CWE

## MANDATORY: Load Reference Files First

**Before analyzing any code, you MUST read the local reference files** that contain the full detection patterns with BAD/GOOD examples:

1. **BREADTH reference** (comprehensive coverage of all 27 patterns):
   ```
   Read: .claude/skills/sec-context-depth/references/ANTI_PATTERNS_BREADTH.md
   ```

2. **DEPTH reference** (deep-dive into 7 most critical patterns):
   ```
   Read: .claude/skills/sec-context-depth/references/ANTI_PATTERNS_DEPTH.md
   ```

These files contain:
- Pseudocode BAD examples (what to detect)
- Pseudocode GOOD examples (secure alternatives)
- CWE identifiers and severity scores
- Attack scenarios and exploitation techniques
- Edge cases frequently overlooked by AI models

**Do NOT rely only on this SKILL.md** — the pattern titles below are an index only. The actual detection logic is in the reference files.

---

## Execution Steps

1. **Read** both reference files above
2. **Glob** target files: `Glob pattern="src/**/*.{ts,js,py,java,go}"` (adjust to target)
3. **Grep** for each anti-pattern using the BAD examples from references
4. **Report** findings organized by Priority (P0 → P2)

---

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

## Pattern Index (details in reference files)

### P0: CRITICAL (13)

| # | Pattern | CWE | Score |
|---|---------|-----|-------|
| 1 | Hardcoded Secrets | CWE-798 | 23 |
| 2 | API Key Prefixes | CWE-798 | 23 |
| 3 | Private Keys | CWE-321 | 23 |
| 4 | SQL Injection - String Concat | CWE-89 | 22 |
| 5 | SQL Injection - f-string | CWE-89 | 22 |
| 6 | Command Injection | CWE-78 | 21 |
| 7 | Command Injection - Concat | CWE-78 | 21 |
| 8 | XSS - innerHTML | CWE-79 | 23 |
| 9 | XSS - document.write | CWE-79 | 23 |
| 10 | XSS - React Unsafe | CWE-79 | 23 |
| 11 | NoSQL Injection | CWE-943 | 22 |
| 12 | Template Injection SSTI | CWE-1336 | 22 |
| 13 | Hardcoded Encryption Key | CWE-798 | 22 |

### P1: HIGH (8)

| # | Pattern | CWE | Score |
|---|---------|-----|-------|
| 14 | JWT None Algorithm | CWE-287 | 22 |
| 15 | Weak Hash MD5/SHA1 | CWE-327 | 20 |
| 16 | ECB Mode | CWE-327 | 20 |
| 17 | DES/RC4 | CWE-327 | 20 |
| 18 | Insecure Random | CWE-330 | 18 |
| 19 | Path Traversal | CWE-22 | 20 |
| 20 | LDAP Injection | CWE-90 | 20 |
| 21 | XPath Injection | CWE-643 | 20 |

### P2: MEDIUM (6)

| # | Pattern | CWE | Score |
|---|---------|-----|-------|
| 22 | Open CORS | CWE-346 | 17 |
| 23 | Verbose Errors | CWE-209 | 16 |
| 24 | Insecure Temp Files | CWE-377 | 16 |
| 25 | Unvalidated Redirect | CWE-601 | 16 |
| 26 | Insecure Deserialization | CWE-502 | 18 |
| 27 | Debug Mode | CWE-489 | 15 |

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

## Output Format

```markdown
# Sec-Context Depth Audit Report

## Summary
- Files scanned: N
- Findings: X (P0: N, P1: N, P2: N)

## P0 Critical Findings
### [Pattern Name] (CWE-XXX) - file:line
- **BAD**: [code snippet]
- **GOOD**: [secure alternative from reference]
- **Impact**: [description]

## P1 High Findings
...

## P2 Medium Findings
...

## Recommendations
1. ...
```

---

## Integration with Hook

The `sec-context-validate.sh` hook automatically checks these 27 patterns on every Edit/Write operation via PostToolUse.

---

## Related Skills

- /adversarial - Adversarial spec refinement
- /security - Security audit
- /gates - Quality gates validation
