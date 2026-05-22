---
name: code-security-review
description: Conducts comprehensive security code reviews including vulnerability detection (OWASP Top 10, CWE), authentication/authorization flaws, injection attacks, cryptography issues, sensitive data exposure, API security, dependency vulnerabilities, security misconfigurations, and compliance validation (PCI-DSS, GDPR, HIPAA). Produces detailed security assessment reports with CVE references, CVSS scores, exploit scenarios, and remediation guidance. Use when reviewing code security, performing security audits, checking for vulnerabilities, validating security controls, assessing security risks, or when users mention "security review", "vulnerability scan", "security audit", "penetration test", "OWASP", "security assessment", "secure coding", or "security compliance".
---

# Code Security Review

## Overview

Performs comprehensive security code reviews to identify vulnerabilities, assess security risks, and provide actionable remediation guidance. Covers OWASP Top 10, CWE classifications, compliance requirements, and security best practices.

## Security Review Workflow

## 1. Initial Assessment

Gather context about the application:

- **Application type**: Web app, API, mobile, desktop, embedded
- **Data sensitivity**: PII, financial data, healthcare records, proprietary information
- **Compliance requirements**: PCI-DSS, GDPR, HIPAA, SOC 2, ISO 27001
- **Authentication mechanisms**: OAuth, JWT, session-based, API keys
- **Technology stack**: Languages, frameworks, libraries, databases
- **External integrations**: Third-party APIs, cloud services, payment processors

Perform threat modeling:

- Identify critical assets (data, functions, resources)
- Map attack surfaces (user inputs, APIs, file uploads, network interfaces)
- Determine threat actors (external attackers, malicious insiders, automated bots)
- Assess existing security controls

### 2. Code Analysis

Systematically review code for security vulnerabilities:

**Priority Areas:**

1. **Authentication & Authorization** - Login flows, session management, access controls
2. **Input Validation** - All user inputs, API parameters, file uploads
3. **Data Protection** - Encryption at rest and in transit, sensitive data handling
4. **API Security** - Rate limiting, authentication, input validation
5. **Dependency Security** - Third-party libraries, outdated packages, known CVEs
6. **Configuration** - Security headers, CORS, environment variables, secrets management
7. **Error Handling** - Information disclosure, stack traces, error messages
8. **Business Logic** - Race conditions, workflow bypasses, state manipulation

### 3. Vulnerability Classification

Classify each finding:

- **Severity**: Critical, High, Medium, Low, Informational
- **CWE ID**: Common Weakness Enumeration identifier
- **OWASP Category**: Map to OWASP Top 10 if applicable
- **CVSS Score**: Calculate if applicable (use CVSS 3.1)
- **Exploitability**: How easy to exploit
- **Impact**: Data loss, privilege escalation, DoS, data breach

### 4. Documentation

Produce comprehensive security report:

- **Executive Summary** - High-level findings and risk overview
- **Detailed Findings** - Each vulnerability with code examples and exploit scenarios
- **Remediation Guidance** - Specific fixes with secure code examples
- **Compliance Assessment** - Status against required standards
- **Remediation Timeline** - Prioritized action plan
- **Security Metrics** - Vulnerability counts by severity and category

## Severity Classification

**Critical (CVSS 9.0-10.0):**

- Remote code execution
- Authentication bypass
- SQL injection with data access
- Hardcoded credentials for production systems
- Complete access control bypass

**High (CVSS 7.0-8.9):**

- Privilege escalation
- Sensitive data exposure (PII, financial)
- Cross-site scripting (XSS) with session theft
- Insecure deserialization
- XML external entity (XXE) injection

**Medium (CVSS 4.0-6.9):**

- Information disclosure
- Cross-site request forgery (CSRF)
- Weak cryptography
- Security misconfiguration
- Missing security headers

**Low (CVSS 0.1-3.9):**

- Version disclosure
- Verbose error messages
- Missing best practices
- Security through obscurity

**Informational:**

- Recommendations for defense in depth
- Future-proofing suggestions
- Security hygiene improvements

## Report Structure

Generate security reports in this format:

### Executive Summary

- Total vulnerabilities by severity
- Critical risk areas
- Compliance status summary
- Overall security posture rating
- Recommended immediate actions

### Detailed Findings

For each vulnerability:

```
## [SEVERITY] Finding Title (CWE-XXX)

**Severity**: Critical/High/Medium/Low
**CWE ID**: CWE-XXX
**OWASP**: A0X:YYYY
**CVSS Score**: X.X (if applicable)

**Description**:
[Clear explanation of the vulnerability]

**Location**:
- File: path/to/file.ext
- Lines: XX-XX
- Function/Class: function_name()

**Vulnerable Code**:
```language
[Actual vulnerable code snippet]
```

**Exploit Scenario**:
[Step-by-step demonstration of how an attacker could exploit this]

**Impact**:
[What could happen if exploited - data breach, privilege escalation, etc.]

**Remediation**:
[Specific steps to fix the vulnerability]

**Secure Code Example**:

```language
[Working secure implementation]
```

**References**:

- [Relevant CWE, CVE, or documentation links]

```

### Remediation Timeline
- **Phase 1 (Critical - Week 1)**: List of critical issues
- **Phase 2 (High - Weeks 2-3)**: List of high severity issues
- **Phase 3 (Medium - Month 2)**: List of medium severity issues
- **Phase 4 (Low - Month 3)**: List of low severity issues

### Compliance Assessment
For each applicable standard, document:
- Requirements checked
- Compliance status (Compliant/Non-Compliant/Partially Compliant)
- Specific gaps identified
- Remediation needed for compliance

## Detailed References

For comprehensive vulnerability patterns, testing procedures, and compliance details:

- **OWASP Top 10 & CWE Patterns**: See [security-review-workflow.md](references/security-review-workflow.md) for:
  - Detailed vulnerability patterns for each OWASP Top 10 category
  - Code examples of vulnerable and secure implementations
  - Testing procedures and detection methods
  - Complete CWE mappings and classifications

- **Security Testing Procedures**: See [security-testing-checklist.md](references/security-testing-checklist.md) for:
  - Comprehensive testing checklist by category
  - Manual and automated testing techniques
  - Security testing tools and configurations
  - API security testing procedures

- **Compliance Requirements**: See [compliance-requirements.md](references/compliance-requirements.md) for:
  - PCI-DSS requirements and validation
  - GDPR data protection requirements
  - HIPAA security and privacy rules
  - SOC 2 security controls

- **Report Examples**: See [report-example.md](references/report-example.md) for:
  - Complete security report template
  - Example findings with remediation guidance
  - Executive summary examples
  - Remediation timeline structures

## Best Practices

**Be Thorough:**
- Review ALL user input points
- Check ALL database queries
- Verify ALL authentication and authorization checks
- Test ALL file operations and uploads
- Examine ALL external integrations

**Be Practical:**
- Prioritize by risk (likelihood × impact)
- Consider exploitability and business context
- Account for compensating controls
- Balance security with usability

**Be Clear:**
- Provide step-by-step exploit scenarios
- Show exact vulnerable code locations
- Give specific, actionable remediation steps
- Include working secure code examples

**Be Professional:**
- Focus on code issues, not developers
- Use industry-standard classifications (CWE, OWASP, CVSS)
- Provide credible references (NIST, OWASP, vendor documentation)
- Document assumptions and testing limitations

