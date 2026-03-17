---
name: IDOR Vulnerability Testing
description: This skill should be used when the user asks to "test for insecure direct object references," "find IDOR vulnerabilities," "exploit broken access control," "enumerate user IDs or object references," or "bypass authorization to access other users' data." It provides comprehensive guidance for detecting, exploiting, and remediating IDOR vulnerabilities in web applications.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# IDOR Vulnerability Testing

## Purpose

Provide systematic methodologies for identifying and exploiting Insecure Direct Object Reference (IDOR) vulnerabilities in web applications. This skill covers both database object references and static file references, detection techniques using parameter manipulation and enumeration, exploitation via Burp Suite, and remediation strategies for securing applications against unauthorized access.

## Inputs / Prerequisites

- **Target Web Application**: URL of application with user-specific resources
- **Multiple User Accounts**: At least two test accounts to verify cross-user access
- **Burp Suite or Proxy Tool**: Intercepting proxy for request manipulation
- **Authorization**: Written permission for security testing
- **Understanding of Application Flow**: Knowledge of how objects are referenced (IDs, filenames)

## Outputs / Deliverables

- **IDOR Vulnerability Report**: Documentation of discovered access control bypasses
- **Proof of Concept**: Evidence of unauthorized data access across user contexts
- **Affected Endpoints**: List of vulnerable API endpoints and parameters
- **Impact Assessment**: Classification of data exposure severity
- **Remediation Recommendations**: Specific fixes for identified vulnerabilities

## Core Workflow

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Understand IDOR Vulnerability Types](./sub-skills/1-understand-idor-vulnerability-types.md)
### 2. [2. Reconnaissance and Setup](./sub-skills/2-reconnaissance-and-setup.md)
### 3. [3. Detection Techniques](./sub-skills/3-detection-techniques.md)
### 4. [4. Exploitation with Burp Suite](./sub-skills/4-exploitation-with-burp-suite.md)
### 5. [5. Common IDOR Locations](./sub-skills/5-common-idor-locations.md)
### 6. [IDOR Testing Checklist](./sub-skills/idor-testing-checklist.md)
### 7. [Response Analysis](./sub-skills/response-analysis.md)
### 8. [Common Vulnerable Parameters](./sub-skills/common-vulnerable-parameters.md)
### 9. [Operational Boundaries](./sub-skills/operational-boundaries.md)
### 10. [Detection Challenges](./sub-skills/detection-challenges.md)
### 11. [Legal Requirements](./sub-skills/legal-requirements.md)
### 12. [Example 1: Basic ID Parameter IDOR](./sub-skills/example-1-basic-id-parameter-idor.md)
### 13. [Example 2: IDOR in Address Update Endpoint](./sub-skills/example-2-idor-in-address-update-endpoint.md)
### 14. [Example 3: Static File IDOR](./sub-skills/example-3-static-file-idor.md)
### 15. [Example 4: Burp Intruder Enumeration](./sub-skills/example-4-burp-intruder-enumeration.md)
### 16. [Example 5: Horizontal to Vertical Escalation](./sub-skills/example-5-horizontal-to-vertical-escalation.md)
### 17. [Issue: All Requests Return 403 Forbidden](./sub-skills/issue-all-requests-return-403-forbidden.md)
### 18. [Issue: Application Uses UUIDs Instead of Sequential IDs](./sub-skills/issue-application-uses-uuids-instead-of-sequential-ids.md)
### 19. [Issue: Session Token Bound to User](./sub-skills/issue-session-token-bound-to-user.md)
### 20. [Issue: Rate Limiting Blocks Enumeration](./sub-skills/issue-rate-limiting-blocks-enumeration.md)
### 21. [Issue: Cannot Verify IDOR Impact](./sub-skills/issue-cannot-verify-idor-impact.md)
### 22. [Implement Proper Access Control](./sub-skills/implement-proper-access-control.md)
### 23. [Use Indirect References](./sub-skills/use-indirect-references.md)
### 24. [Server-Side Validation](./sub-skills/server-side-validation.md)
