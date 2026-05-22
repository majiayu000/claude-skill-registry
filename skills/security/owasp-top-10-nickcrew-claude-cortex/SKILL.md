---
name: owasp-top-10
description: OWASP Top 10 security vulnerabilities with detection and remediation patterns. Use when conducting security audits, implementing secure coding practices, or reviewing code for common security vulnerabilities.
---

# OWASP Top 10 Security Vulnerabilities

Expert guidance for identifying, preventing, and remediating the most critical web application security risks based on OWASP Top 10 2021.

## When to Use This Skill

- Conducting security audits and code reviews
- Implementing secure coding practices in new features
- Reviewing authentication and authorization systems
- Assessing input validation and sanitization
- Evaluating third-party dependencies for vulnerabilities
- Designing security controls and defense-in-depth strategies
- Preparing for security certifications or compliance audits
- Investigating security incidents or suspicious behavior

## OWASP Top 10 2021 Overview

**Ranked by Risk Severity:**

1. **A01** - Broken Access Control (↑ from #5)
2. **A02** - Cryptographic Failures (formerly Sensitive Data Exposure)
3. **A03** - Injection (↓ from #1)
4. **A04** - Insecure Design (NEW)
5. **A05** - Security Misconfiguration
6. **A06** - Vulnerable and Outdated Components
7. **A07** - Identification and Authentication Failures
8. **A08** - Software and Data Integrity Failures (NEW)
9. **A09** - Security Logging and Monitoring Failures
10. **A10** - Server-Side Request Forgery (SSRF) (NEW)

## Quick Reference

Load detailed guidance for each vulnerability:

| Vulnerability | Reference File |
|---|---|
| **Broken Access Control** | `skills/owasp-top-10/references/broken-access-control.md` |
| **Cryptographic Failures** | `skills/owasp-top-10/references/cryptographic-failures.md` |
| **Injection** | `skills/owasp-top-10/references/injection.md` |
| **Insecure Design** | `skills/owasp-top-10/references/insecure-design.md` |
| **Security Misconfiguration** | `skills/owasp-top-10/references/security-misconfiguration.md` |
| **Vulnerable Components** | `skills/owasp-top-10/references/vulnerable-components.md` |
| **Authentication Failures** | `skills/owasp-top-10/references/authentication-failures.md` |
| **Integrity Failures** | `skills/owasp-top-10/references/integrity-failures.md` |
| **Logging & Monitoring** | `skills/owasp-top-10/references/logging-monitoring.md` |
| **SSRF** | `skills/owasp-top-10/references/ssrf.md` |
| **Prevention Strategies** | `skills/owasp-top-10/references/prevention-strategies.md` |

## Security Audit Workflow

1. **Identify Scope**: Determine application components and attack surface
2. **Select Vulnerabilities**: Choose relevant OWASP categories based on features
3. **Load Reference**: Read appropriate reference file(s) for detailed patterns
4. **Analyze Code**: Review code against vulnerable and secure patterns
5. **Document Findings**: Record vulnerabilities with severity and remediation
6. **Verify Fixes**: Test that remediations properly address issues
7. **Test Security**: Run automated security testing (SAST, DAST, SCA)

## Core Security Principles

### Defense in Depth
- Layer security controls at network, application, data, and monitoring levels
- Ensure failure of one control doesn't compromise entire system

### Secure by Default
- Deny all access by default, explicitly grant permissions
- Fail securely (errors don't expose sensitive information)
- Minimize attack surface (disable unused features)
- Apply least privilege to all accounts and services

### Input Validation
- Validate type, length, format, and allowed values
- Use allow-lists over deny-lists
- Sanitize for specific context (SQL, HTML, shell, etc.)
- Never trust client input

## Common Mistakes

1. **Trusting User Input**: Always validate and sanitize all user-supplied data
2. **Rolling Your Own Crypto**: Use established libraries (bcrypt, AES-256)
3. **Exposing Errors**: Log detailed errors internally, show generic messages to users
4. **Missing Authorization**: Check permissions on every request, not just UI
5. **Weak Session Management**: Use secure, httpOnly, sameSite cookies with HTTPS
6. **Ignoring Dependencies**: Regularly audit and update third-party libraries
7. **No Logging**: Log security events for detection and incident response
8. **Default Configurations**: Harden all systems, disable defaults

## Security Testing Tools

**SAST (Static)**: SonarQube, Semgrep, ESLint security plugins
**DAST (Dynamic)**: OWASP ZAP, Burp Suite
**SCA (Dependencies)**: npm audit, Snyk, Dependabot
**Secrets Scanning**: GitGuardian, TruffleHog
**Penetration Testing**: Metasploit, Kali Linux tools

## Resources

- **OWASP Top 10 2021**: https://owasp.org/Top10/
- **OWASP Cheat Sheets**: https://cheatsheetseries.owasp.org/
- **OWASP ASVS**: Application Security Verification Standard
- **CWE Top 25**: Common Weakness Enumeration
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **CVE Database**: https://cve.mitre.org/
- **Snyk Vulnerability DB**: https://snyk.io/vuln/
