---
name: API Fuzzing for Bug Bounty
description: This skill should be used when the user asks to "test API security", "fuzz APIs", "find IDOR vulnerabilities", "test REST API", "test GraphQL", "API penetration testing", "bug bounty API testing", or needs guidance on API security assessment techniques.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# API Fuzzing for Bug Bounty

## Purpose

Provide comprehensive techniques for testing REST, SOAP, and GraphQL APIs during bug bounty hunting and penetration testing engagements. Covers vulnerability discovery, authentication bypass, IDOR exploitation, and API-specific attack vectors.

## Inputs/Prerequisites

- Burp Suite or similar proxy tool
- API wordlists (SecLists, api_wordlist)
- Understanding of REST/GraphQL/SOAP protocols
- Python for scripting
- Target API endpoints and documentation (if available)

## Outputs/Deliverables

- Identified API vulnerabilities
- IDOR exploitation proofs
- Authentication bypass techniques
- SQL injection points
- Unauthorized data access documentation

---

## API Types Overview

| Type | Protocol | Data Format | Structure |
|------|----------|-------------|-----------|
| SOAP | HTTP | XML | Header + Body |
| REST | HTTP | JSON/XML/URL | Defined endpoints |
| GraphQL | HTTP | Custom Query | Single endpoint |

---

## Core Workflow

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Step 1: API Reconnaissance](./sub-skills/step-1-api-reconnaissance.md)
### 2. [Step 2: Authentication Testing](./sub-skills/step-2-authentication-testing.md)
### 3. [Step 3: IDOR Testing](./sub-skills/step-3-idor-testing.md)
### 4. [Step 4: Injection Testing](./sub-skills/step-4-injection-testing.md)
### 5. [Step 5: Method Testing](./sub-skills/step-5-method-testing.md)
### 6. [Introspection Query](./sub-skills/introspection-query.md)
### 7. [GraphQL IDOR](./sub-skills/graphql-idor.md)
### 8. [GraphQL SQL/NoSQL Injection](./sub-skills/graphql-sqlnosql-injection.md)
### 9. [Rate Limit Bypass (Batching)](./sub-skills/rate-limit-bypass-batching.md)
### 10. [GraphQL DoS (Nested Queries)](./sub-skills/graphql-dos-nested-queries.md)
### 11. [GraphQL XSS](./sub-skills/graphql-xss.md)
### 12. [GraphQL Tools](./sub-skills/graphql-tools.md)
### 13. [PDF Export Attacks](./sub-skills/pdf-export-attacks.md)
### 14. [DoS via Limits](./sub-skills/dos-via-limits.md)
### 15. [Example 1: IDOR Exploitation](./sub-skills/example-1-idor-exploitation.md)
### 16. [Example 2: GraphQL Introspection](./sub-skills/example-2-graphql-introspection.md)
