---
name: threat-model
description: Threat modeling methodologies (STRIDE, DREAD, PASTA, attack trees) for secure architecture design. Use when planning new systems, reviewing architecture security, identifying threats, or assessing risk. Triggers: threat modeling, threat model, STRIDE, DREAD, attack tree, attack surface, trust boundary, data flow diagram, DFD, threat analysis, risk assessment, adversary, threat actor, threat vector, mitigation, security architecture, attack scenario, vulnerability assessment, security posture, defense in depth.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Threat Modeling

## Overview

This skill provides structured methodologies for identifying, analyzing, and mitigating security threats in system designs. Use it when designing new systems, reviewing existing architectures, or assessing security posture.

## When to Use Threat Modeling

- **New system design**: Before implementation, identify security requirements
- **Architecture review**: Evaluate existing systems for security gaps
- **Feature additions**: Assess security impact of new functionality
- **Third-party integrations**: Evaluate risks of external dependencies
- **Compliance requirements**: Document security controls for audits

## Methodologies

### STRIDE

Categorize threats by type:

| Threat                     | Description                           | Security Property |
| -------------------------- | ------------------------------------- | ----------------- |
| **S**poofing               | Impersonating users or systems        | Authentication    |
| **T**ampering              | Modifying data or code                | Integrity         |
| **R**epudiation            | Denying actions occurred              | Non-repudiation   |
| **I**nformation Disclosure | Exposing data to unauthorized parties | Confidentiality   |
| **D**enial of Service      | Making system unavailable             | Availability      |
| **E**levation of Privilege | Gaining unauthorized access           | Authorization     |

### DREAD (Risk Scoring)

Score each threat (1-10) across five dimensions:

| Factor              | Question                            |
| ------------------- | ----------------------------------- |
| **D**amage          | How severe is the impact?           |
| **R**eproducibility | How easily can it be reproduced?    |
| **E**xploitability  | How much skill/resources needed?    |
| **A**ffected Users  | How many users impacted?            |
| **D**iscoverability | How easy to find the vulnerability? |

**Risk Score** = (D + R + E + A + D) / 5

- **High Risk**: 7-10 (immediate action)
- **Medium Risk**: 4-6 (planned remediation)
- **Low Risk**: 1-3 (accept or monitor)

### PASTA (Process for Attack Simulation and Threat Analysis)

Seven-stage process:

1. **Define Objectives**: Business goals, compliance requirements
2. **Define Technical Scope**: Architecture, technologies, data flows
3. **Application Decomposition**: Components, trust boundaries, entry points
4. **Threat Analysis**: Threat intelligence, attack patterns
5. **Vulnerability Analysis**: Weaknesses, existing controls
6. **Attack Modeling**: Attack trees, likely scenarios
7. **Risk & Impact Analysis**: Prioritized mitigations

## Threat Modeling Process

### Step 1: Define Scope and Assets

```markdown
## System Overview

- **Name**: [System name]
- **Purpose**: [What it does]
- **Sensitivity**: [Data classification]

## Assets to Protect

| Asset            | Classification | Impact if Compromised      |
| ---------------- | -------------- | -------------------------- |
| User credentials | Confidential   | Account takeover           |
| Payment data     | PCI-DSS        | Financial loss, compliance |
| Personal data    | PII/GDPR       | Privacy breach, fines      |
```

### Step 2: Create Data Flow Diagram

Identify:

- **External entities**: Users, third-party services
- **Processes**: Application components, services
- **Data stores**: Databases, caches, file systems
- **Data flows**: How data moves between components
- **Trust boundaries**: Where privilege levels change

```text
┌─────────────────────────────────────────────────────────────┐
│                     TRUST BOUNDARY: Internet                │
│  ┌──────────┐                                               │
│  │  User    │                                               │
│  │ Browser  │                                               │
│  └────┬─────┘                                               │
│       │ HTTPS                                               │
├───────┼─────────────────────────────────────────────────────┤
│       │            TRUST BOUNDARY: DMZ                      │
│       ▼                                                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐            │
│  │   Load   │────▶│   API    │────▶│  Auth    │            │
│  │ Balancer │     │ Gateway  │     │ Service  │            │
│  └──────────┘     └────┬─────┘     └──────────┘            │
│                        │                                    │
├────────────────────────┼────────────────────────────────────┤
│                        │   TRUST BOUNDARY: Internal         │
│                        ▼                                    │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐            │
│  │ App      │────▶│ Database │     │ Cache    │            │
│  │ Server   │     │ (PG)     │     │ (Redis)  │            │
│  └──────────┘     └──────────┘     └──────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Identify Threats (STRIDE per Element)

```markdown
## Threat Analysis

### API Gateway

| STRIDE | Threat                     | Likelihood | Impact   |
| ------ | -------------------------- | ---------- | -------- |
| S      | Forged JWT tokens          | Medium     | High     |
| T      | Request body manipulation  | Low        | Medium   |
| R      | Missing audit logs         | Medium     | Medium   |
| I      | Verbose error messages     | High       | Medium   |
| D      | Rate limiting bypass       | Medium     | High     |
| E      | IDOR to access other users | Medium     | Critical |

### Database

| STRIDE | Threat                        | Likelihood | Impact   |
| ------ | ----------------------------- | ---------- | -------- |
| S      | Connection impersonation      | Low        | Critical |
| T      | SQL injection                 | Medium     | Critical |
| I      | Unencrypted backups           | Medium     | High     |
| D      | Resource exhaustion           | Low        | High     |
| E      | Privilege escalation via SQLi | Medium     | Critical |
```

### Step 4: Build Attack Trees

```text
                    ┌─────────────────────┐
                    │ Steal User Data     │
                    │ (Root Goal)         │
                    └─────────┬───────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ Compromise    │ │ Exploit App   │ │ Social        │
    │ Credentials   │ │ Vulnerability │ │ Engineering   │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                 │                 │
    ┌───────┴───────┐ ┌───────┴───────┐ ┌───────┴───────┐
    │               │ │               │ │               │
    ▼               ▼ ▼               ▼ ▼               ▼
┌────────┐   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Phishing│   │Brute   │ │SQL     │ │IDOR    │ │Pretexting│
│        │   │Force   │ │Inject  │ │        │ │Support  │
└────────┘   └────────┘ └────────┘ └────────┘ └────────┘
[L:H,I:H]    [L:M,I:H]  [L:M,I:C]  [L:H,I:H]  [L:M,I:H]
```

### Step 5: Define Mitigations

```markdown
## Mitigation Plan

| Threat         | Mitigation                              | Priority | Status      |
| -------------- | --------------------------------------- | -------- | ----------- |
| SQL Injection  | Parameterized queries, input validation | P0       | In Progress |
| IDOR           | Authorization checks on all endpoints   | P0       | Not Started |
| JWT Forgery    | RS256 signing, short expiry, rotation   | P1       | Done        |
| Brute Force    | Rate limiting, account lockout, MFA     | P1       | Partial     |
| Verbose Errors | Generic error messages in prod          | P2       | Not Started |
```

## Threat Model Document Template

```markdown
# Threat Model: [System Name]

**Version**: 1.0
**Date**: YYYY-MM-DD
**Author**: [Name]
**Reviewers**: [Names]

## 1. Executive Summary

[High-level findings and recommendations]

## 2. System Description

### 2.1 Purpose

### 2.2 Architecture Overview

### 2.3 Data Classification

### 2.4 Trust Boundaries

## 3. Assets

| Asset | Classification | Owner |
| ----- | -------------- | ----- |

## 4. Threat Analysis

### 4.1 Data Flow Diagram

### 4.2 STRIDE Analysis by Component

### 4.3 Attack Trees

## 5. Risk Assessment

| Threat | DREAD Score | Risk Level |
| ------ | ----------- | ---------- |

## 6. Mitigations

| Threat | Mitigation | Owner | Timeline |
| ------ | ---------- | ----- | -------- |

## 7. Residual Risks

[Accepted risks and justification]

## 8. Review Schedule

[When to revisit this threat model]
```

## Domain-Specific Threat Modeling

### API Threat Modeling

Focus areas for REST, GraphQL, and gRPC APIs:

#### Authentication & Authorization

- Token-based auth vulnerabilities (JWT, OAuth 2.0)
- Broken object-level authorization (BOLA/IDOR)
- Broken function-level authorization
- API key leakage and rotation issues

#### Data Exposure

- Excessive data exposure in responses
- Mass assignment vulnerabilities
- GraphQL introspection in production
- Verbose error messages leaking architecture

#### Rate Limiting & Abuse

- Missing or bypassable rate limits
- Resource exhaustion (large payloads, deep queries)
- Batch request abuse
- Pagination vulnerabilities

#### Input Validation

- Injection attacks (SQL, NoSQL, command, LDAP)
- XML external entity (XXE) attacks
- Server-side request forgery (SSRF)
- GraphQL query complexity attacks

#### API-Specific Mitigations

- Schema validation (OpenAPI, GraphQL schema)
- Query depth/complexity limiting
- Field-level authorization
- API gateway security policies
- Request signing and replay protection

### Infrastructure Threat Modeling

Focus areas for cloud, containers, and orchestration:

#### Cloud Services

- Misconfigured S3 buckets/blob storage (public access)
- IAM privilege escalation paths
- Metadata service abuse (SSRF to credentials)
- Unencrypted storage/transit
- Network security group misconfigurations

#### Container Security

- Vulnerable base images
- Secrets in environment variables/layers
- Privileged containers
- Container escape vulnerabilities
- Registry security (image signing, scanning)

#### Orchestration (Kubernetes, Docker Swarm)

- Exposed API servers (unauthenticated kubelet)
- RBAC misconfigurations
- Pod security policies/standards violations
- Network policy gaps
- Secrets management (etcd encryption, external vaults)

#### CI/CD Pipeline

- Compromised build agents
- Dependency confusion/substitution
- Secrets in version control
- Unsigned artifacts
- Pipeline injection attacks

#### Infrastructure Mitigations

- Infrastructure as Code security scanning
- Least privilege IAM policies
- Network segmentation (VPCs, subnets, security groups)
- Immutable infrastructure patterns
- Runtime security monitoring (Falco, OSSEC)

### ML Model Threat Modeling

Focus areas for machine learning systems:

#### Adversarial Attacks

- Evasion attacks (adversarial examples at inference)
- Poisoning attacks (training data manipulation)
- Model inversion (extracting training data)
- Membership inference (detecting if data was in training set)

#### Model Theft

- Model extraction via API queries
- Intellectual property leakage
- Hyperparameter discovery
- Architecture reverse engineering

#### Data Privacy

- Training data exposure
- PII leakage in model outputs
- Differential privacy violations
- GDPR right-to-explanation challenges

#### Deployment Risks

- Model serving API vulnerabilities
- Feature store poisoning
- Model registry security
- A/B testing exploitation

#### ML-Specific Mitigations

- Adversarial training and robustness testing
- Input sanitization and anomaly detection
- Model watermarking
- Differential privacy techniques
- Explainability constraints
- Rate limiting on prediction APIs
- Model versioning and rollback capabilities

## Quick Reference: Common Threats by Component

### Web Application

- XSS, CSRF, clickjacking
- Session hijacking
- Insecure direct object references
- Open redirects

### API

- Broken authentication/authorization
- Mass assignment
- Rate limiting bypass
- Injection attacks

### Database

- SQL injection
- Privilege escalation
- Unencrypted data
- Backup exposure

### Authentication

- Credential stuffing
- Session fixation
- Token leakage
- MFA bypass

### File Upload

- Malware upload
- Path traversal
- Remote code execution
- Storage exhaustion

### Third-Party Integrations

- API key exposure
- Webhook spoofing
- Supply chain attacks
- Data leakage

## Best Practices

1. **Iterate**: Update threat models as systems evolve
2. **Collaborate**: Include developers, ops, and security
3. **Prioritize**: Focus on high-impact, likely threats first
4. **Document**: Maintain living threat model documents
5. **Validate**: Test mitigations through security testing
6. **Automate**: Integrate threat modeling into SDLC
