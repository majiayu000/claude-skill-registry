---
name: threat-modeling
description: Identify and analyze security threats. Use when designing systems, reviewing architecture, or assessing risk. Covers STRIDE methodology.
allowed-tools: Read, Write, Glob, Grep, mcp__sequential-thinking__*
---

# Threat Modeling

## MCP Tools

**Sequential Thinking** (systematic analysis):
Use for structured STRIDE analysis:
1. Enumerate each threat category systematically
2. Consider attack vectors step-by-step
3. Evaluate mitigations with pros/cons
4. Document reasoning for risk acceptance

## Why Threat Model?

- Identify threats early
- Prioritize security efforts
- Document security assumptions
- Guide security testing

## STRIDE Methodology

Use **Sequential Thinking** to work through each category:

### S - Spoofing
Pretending to be someone else.
- **Example**: Forged authentication tokens
- **Mitigation**: Strong authentication, MFA

### T - Tampering
Modifying data without authorization.
- **Example**: Changing request parameters
- **Mitigation**: Integrity checks, signatures
- **Trace with Grep**: Find all input handlers

### R - Repudiation
Denying an action occurred.
- **Example**: User denies making transaction
- **Mitigation**: Audit logging, non-repudiation

### I - Information Disclosure
Exposing confidential data.
- **Example**: API returns sensitive fields
- **Mitigation**: Encryption, access controls
- **Trace with Grep**: Find data return points

### D - Denial of Service
Making system unavailable.
- **Example**: Resource exhaustion attack
- **Mitigation**: Rate limiting, auto-scaling

### E - Elevation of Privilege
Gaining unauthorized access.
- **Example**: User becomes admin
- **Mitigation**: Least privilege, input validation
- **Trace with Grep**: Find authorization checks

## Threat Modeling Process

### 1. Decompose System
- Use Grep and Glob to identify entry points
- Draw data flow diagrams
- Identify trust boundaries

### 2. Identify Threats
Use **Sequential Thinking** to systematically ask STRIDE questions for each component.

### 3. Trace Data Flow
Use Grep to trace:
- User input → processing → storage
- Authentication token flow
- Sensitive data paths

### 4. Rate Threats
Use DREAD or CVSS scoring:
- **D**amage potential
- **R**eproducibility
- **E**xploitability
- **A**ffected users
- **D**iscoverability

### 5. Mitigate
- Avoid: Remove the feature
- Transfer: Use third-party
- Mitigate: Add controls
- Accept: Document risk (use Sequential Thinking to justify)

## Threat Model Document

```markdown
## Asset: User Database

### Threats
| Threat | Type | Likelihood | Impact | Risk |
|--------|------|------------|--------|------|
| SQL Injection | Tampering | Medium | High | High |
| Data Breach | Info Disclosure | Low | Critical | High |

### Mitigations
1. Parameterized queries
2. Encryption at rest
3. Access logging
```
