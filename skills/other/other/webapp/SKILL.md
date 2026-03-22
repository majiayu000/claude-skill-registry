---
name: webapp
description: Web application security testing - OWASP Top 10, API security
---

# Web Application Testing

Run authorized web application security tests:
- OWASP Top 10 vulnerabilities
- SQL injection, XSS, command injection
- Authentication and session testing
- Authorization and access control (IDOR)
- API security testing
- Business logic flaws

## Required Context
1. **Target**: URL(s) in scope
2. **Authorization**: LOA, bug bounty program, or own app
3. **Scope**: In-scope/out-of-scope endpoints
4. **Constraints**: Rate limits, testing windows

## Tools Used
sqlmap, ffuf, gobuster, nuclei, dalfox, nikto, wpscan, burpsuite, jwt_tool, arjun

## Example
```
/webapp
Target: https://app.example.com
Authorization: Bug bounty program
Focus: Authentication bypass, SQLi
```
