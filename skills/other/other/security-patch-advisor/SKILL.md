---
name: security-patch-advisor
description: Proposes secure remediation strategies for detected security vulnerabilities including buffer overflows, injection risks, insecure deserialization, improper authentication, and unsafe cryptographic usage. Provides recommended security checks, safer API alternatives, design-level changes, code examples, trade-off analysis, and prioritized remediation plans. Does NOT automatically modify code unless explicitly requested.
---

# Security Patch Advisor

## Overview

This skill analyzes security vulnerabilities and provides comprehensive remediation strategies without automatically modifying code. It offers multiple remediation approaches with detailed trade-off analysis, code examples, and implementation guidance for vulnerabilities categorized by CWE (Common Weakness Enumeration) and severity.

## When to Use This Skill

Use this skill when you need:
- Remediation strategies for detected security vulnerabilities
- Safer API alternatives for insecure code patterns
- Design-level security improvements
- Multiple remediation approaches with trade-offs
- Code examples showing before/after fixes
- Prioritized remediation plans based on severity and impact
- Security best practices for specific vulnerability types

**Trigger scenarios:**
- After running static analysis tools (SAST)
- After security audits or penetration testing
- When reviewing code for security issues
- When planning security improvements
- After vulnerability disclosure or CVE reports

## Core Workflow

### 1. Vulnerability Analysis

When presented with a security vulnerability, analyze:

**Context Gathering:**
- Vulnerability type and CWE classification
- Severity level (Critical, High, Medium, Low)
- Affected code location and scope
- Current implementation details
- Attack vectors and exploitation scenarios
- Business impact and data sensitivity

**Questions to Consider:**
- What is the root cause of the vulnerability?
- What data or systems are at risk?
- What are the prerequisites for exploitation?
- Are there existing security controls?
- What is the attack surface?

### 2. Remediation Strategy Development

Provide multiple remediation approaches:

**Strategy Components:**
1. **Primary Remediation** (recommended approach)
   - Specific code changes required
   - Safer API alternatives
   - Security controls to implement
   - Validation and sanitization logic

2. **Alternative Approaches**
   - Different implementation strategies
   - Framework-specific solutions
   - Defense-in-depth measures
   - Compensating controls

3. **Design-Level Changes**
   - Architectural improvements
   - Security patterns to adopt
   - System-level mitigations
   - Infrastructure changes

**For Each Strategy, Include:**
- ✅ Benefits and security improvements
- ⚠️ Trade-offs and limitations
- 📊 Implementation complexity
- ⚡ Performance impact
- 🔧 Required dependencies or tools
- 📚 Relevant security standards (OWASP, CWE, NIST)

### 3. Code Examples

Provide concrete before/after examples:

**Example Structure:**
```
### Vulnerable Code
[Show the insecure code with clear vulnerability markers]

**Vulnerability:** CWE-XXX (Name)
**Risk:** [Explain the security risk]
**Attack Example:** [Show how it could be exploited]

### Remediated Code (Approach 1)
[Show the fixed code with security improvements]

**Changes:**
- [List specific changes made]
- [Explain security mechanisms added]

**Trade-offs:**
- ✅ [Benefits]
- ⚠️ [Limitations or considerations]

### Alternative Remediation (Approach 2)
[Show alternative fix if applicable]

**Trade-offs:**
- ✅ [Benefits]
- ⚠️ [Limitations or considerations]
```

### 4. Implementation Guidance

Provide step-by-step implementation instructions:

**Guidance Should Include:**
1. **Prerequisites**
   - Required libraries or dependencies
   - Configuration changes needed
   - Environment setup

2. **Implementation Steps**
   - Ordered list of changes
   - Code modifications required
   - Testing procedures

3. **Verification**
   - How to verify the fix works
   - Security testing recommendations
   - Regression testing considerations

4. **Deployment Considerations**
   - Backward compatibility
   - Migration strategy
   - Rollback plan

### 5. Prioritization and Risk Assessment

Help prioritize remediation efforts:

**Prioritization Factors:**
- **Severity:** CVSS score, exploitability, impact
- **Exposure:** Public-facing vs internal, attack surface
- **Data Sensitivity:** PII, credentials, financial data
- **Ease of Exploitation:** Skill level required, available exploits
- **Business Impact:** System criticality, user impact
- **Remediation Effort:** Development time, testing requirements

**Priority Levels:**
- **P0 (Critical):** Immediate action required (active exploitation, critical systems)
- **P1 (High):** Fix within days (high severity, exposed systems)
- **P2 (Medium):** Fix within weeks (moderate risk, mitigating controls exist)
- **P3 (Low):** Fix in next release cycle (low risk, defense in depth)

## Vulnerability Categories

### Buffer Overflow Vulnerabilities
- CWE-120: Buffer Copy without Checking Size
- CWE-121: Stack-based Buffer Overflow
- CWE-122: Heap-based Buffer Overflow
- CWE-787: Out-of-bounds Write

**Common Remediations:**
- Use safe string functions (`strncpy`, `snprintf`)
- Implement bounds checking
- Use memory-safe languages or libraries
- Enable compiler protections (stack canaries, ASLR)

### Injection Vulnerabilities
- CWE-89: SQL Injection
- CWE-78: OS Command Injection
- CWE-79: Cross-Site Scripting (XSS)
- CWE-91: XML Injection
- CWE-94: Code Injection

**Common Remediations:**
- Use parameterized queries/prepared statements
- Implement input validation and output encoding
- Use safe APIs instead of shell execution
- Apply Content Security Policy (CSP)
- Use ORM frameworks with built-in protections

### Insecure Deserialization
- CWE-502: Deserialization of Untrusted Data

**Common Remediations:**
- Use data-only formats (JSON, XML)
- Implement integrity checks (HMAC signatures)
- Whitelist allowed classes
- Avoid deserializing untrusted data

### Authentication & Authorization
- CWE-287: Improper Authentication
- CWE-306: Missing Authentication
- CWE-862: Missing Authorization
- CWE-798: Hard-coded Credentials
- CWE-522: Insufficiently Protected Credentials

**Common Remediations:**
- Implement multi-factor authentication
- Use secure session management
- Implement proper authorization checks
- Use environment variables or secret management
- Hash passwords with bcrypt/Argon2

### Cryptographic Issues
- CWE-327: Use of Broken Cryptography
- CWE-328: Weak Hash
- CWE-330: Insufficient Randomness
- CWE-326: Inadequate Encryption Strength

**Common Remediations:**
- Use modern algorithms (AES-256, SHA-256, RSA-2048+)
- Use cryptographically secure random number generators
- Implement proper key management
- Use authenticated encryption (GCM, CCM)

### Memory Safety
- CWE-416: Use After Free
- CWE-476: NULL Pointer Dereference
- CWE-415: Double Free
- CWE-401: Memory Leak

**Common Remediations:**
- Use smart pointers (C++)
- Nullify pointers after free
- Use memory-safe languages
- Enable AddressSanitizer for testing

### Path Traversal & File Handling
- CWE-22: Path Traversal
- CWE-73: External Control of File Name
- CWE-434: Unrestricted Upload of Dangerous File Type

**Common Remediations:**
- Validate and sanitize file paths
- Use whitelists for allowed paths/extensions
- Implement proper access controls
- Store uploads outside web root

## Output Format

Structure your remediation advice as follows:

```markdown
## Vulnerability Summary
- **Type:** [CWE-XXX: Name]
- **Severity:** [Critical/High/Medium/Low]
- **Location:** [File:Line or Component]
- **Impact:** [Brief description of security impact]

## Risk Analysis
[Explain the security risk, attack vectors, and potential impact]

## Recommended Remediation (Primary)
[Detailed description of the recommended fix]

### Code Example
[Before/after code showing the fix]

### Implementation Steps
1. [Step 1]
2. [Step 2]
...

### Trade-offs
- ✅ [Benefits]
- ⚠️ [Considerations]

## Alternative Approaches

### Alternative 1: [Name]
[Description and code example]

**Trade-offs:**
- ✅ [Benefits]
- ⚠️ [Considerations]

### Alternative 2: [Name]
[Description and code example]

**Trade-offs:**
- ✅ [Benefits]
- ⚠️ [Considerations]

## Design-Level Improvements
[Architectural or system-level changes to consider]

## Verification & Testing
[How to verify the fix and test for regressions]

## Priority Recommendation
**Priority Level:** [P0/P1/P2/P3]
**Rationale:** [Why this priority level]
**Timeline:** [Suggested remediation timeline]

## Additional Resources
[Links to relevant security standards, documentation, or tools]
```

## Important Guidelines

### DO:
- ✅ Provide multiple remediation approaches when applicable
- ✅ Include concrete code examples with explanations
- ✅ Explain trade-offs honestly (security vs performance, complexity, etc.)
- ✅ Reference relevant CWE classifications and security standards
- ✅ Consider the specific technology stack and constraints
- ✅ Provide implementation guidance and verification steps
- ✅ Prioritize based on risk and business impact
- ✅ Explain the "why" behind recommendations

### DON'T:
- ❌ Automatically modify code without explicit user request
- ❌ Provide only one solution without discussing alternatives
- ❌ Ignore performance or compatibility trade-offs
- ❌ Recommend overly complex solutions for simple problems
- ❌ Suggest security theater (ineffective controls)
- ❌ Provide generic advice without code-specific context
- ❌ Overlook defense-in-depth opportunities

## Example Interaction

**User:** "I found a SQL injection vulnerability in our login function. Here's the code: `query = "SELECT * FROM users WHERE username = '" + username + "'"`"

**Response:**

```markdown
## Vulnerability Summary
- **Type:** CWE-89: SQL Injection
- **Severity:** Critical
- **Location:** Login function
- **Impact:** Attackers can bypass authentication, extract database contents, or modify data

## Risk Analysis
The login function constructs SQL queries using string concatenation with user-supplied input. An attacker can inject SQL commands by providing specially crafted input like `' OR '1'='1` to bypass authentication or `'; DROP TABLE users; --` to execute destructive commands.

## Recommended Remediation (Parameterized Queries)

Use parameterized queries (prepared statements) to separate SQL logic from data:

### Code Example

**Vulnerable Code:**
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)
```

**Remediated Code:**
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### Implementation Steps
1. Replace string concatenation with parameterized query syntax
2. Pass user input as tuple parameter to `execute()`
3. Test with various inputs including SQL injection attempts
4. Verify query logs show parameterized queries

### Trade-offs
- ✅ Complete protection against SQL injection
- ✅ No performance impact
- ✅ Minimal code changes
- ✅ Database driver handles escaping automatically
- ⚠️ Requires understanding of parameterized query syntax

## Alternative Approaches

### Alternative 1: ORM Framework
Use an Object-Relational Mapping framework:

```python
user = User.query.filter_by(username=username).first()
```

**Trade-offs:**
- ✅ Even simpler code
- ✅ Built-in injection protection
- ✅ Abstraction from SQL details
- ⚠️ Requires ORM framework (SQLAlchemy, Django ORM)
- ⚠️ May have performance overhead for complex queries
- ⚠️ Learning curve for ORM concepts

### Alternative 2: Stored Procedures
Encapsulate SQL logic in stored procedures:

```python
cursor.callproc('sp_authenticate_user', (username,))
```

**Trade-offs:**
- ✅ Centralized SQL logic
- ✅ Parameterized by default
- ✅ Can enforce additional security policies
- ⚠️ Requires database-side development
- ⚠️ Less flexible for dynamic queries
- ⚠️ Harder to version control

## Design-Level Improvements

1. **Input Validation:** Implement whitelist validation for usernames (alphanumeric only)
2. **Rate Limiting:** Add rate limiting to prevent brute force attacks
3. **Logging:** Log all authentication attempts for security monitoring
4. **MFA:** Consider implementing multi-factor authentication

## Verification & Testing

1. **Positive Test:** Verify legitimate logins still work
2. **Injection Test:** Try inputs like `' OR '1'='1`, `'; DROP TABLE users; --`
3. **Query Inspection:** Check database logs to confirm parameterized queries
4. **Automated Testing:** Add security test cases to test suite

## Priority Recommendation
**Priority Level:** P0 (Critical)
**Rationale:** SQL injection in authentication is critical severity, allows complete system compromise
**Timeline:** Fix immediately (within 24 hours)

## Additional Resources
- OWASP SQL Injection Prevention Cheat Sheet
- CWE-89: SQL Injection
- Database-specific parameterized query documentation
```

## Resources

### references/remediation_strategies.md
Comprehensive remediation patterns organized by vulnerability category, including:
- Buffer overflow mitigations
- Injection prevention techniques
- Secure deserialization approaches
- Authentication and authorization best practices
- Cryptographic recommendations
- Memory safety strategies
- Configuration security

### references/examples.md
Complete before/after remediation examples with detailed explanations:
- SQL injection fixes (parameterized queries, ORMs)
- Command injection prevention (subprocess, library alternatives)
- Buffer overflow mitigations (bounds checking, safe functions)
- XSS prevention (output encoding, CSP, templates)
- Insecure deserialization fixes (JSON, signed data)
- Weak cryptography upgrades (bcrypt, Argon2)
- Authentication improvements (rate limiting, session management)
- Authorization enforcement (ownership checks, RBAC)
- Hard-coded credential removal (environment variables, secret management)
- Path traversal prevention (validation, whitelisting)
