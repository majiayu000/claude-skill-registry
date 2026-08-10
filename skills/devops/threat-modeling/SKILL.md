---
name: threat-modeling
description: Conduct structured threat modeling for software systems using established methodologies to identify, prioritize, and mitigate security threats before they are exploited. Use when the user requests threat modeling or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Threat Modeling

This skill enables the agent to perform structured threat modeling for software applications, APIs, and infrastructure. The agent analyzes system architecture, data flows, and trust boundaries to systematically identify potential security threats using established methodologies such as STRIDE, DREAD, PASTA, and attack trees. The output is a prioritized threat register with specific, actionable mitigation strategies that development teams can integrate into their backlog.

## Workflow

1. **Decompose the System Architecture** — Analyze architecture diagrams, code repositories, infrastructure-as-code files, and deployment configurations to identify all components, data stores, external services, and communication channels. Map trust boundaries between networks, services, and user privilege levels. Produce a data flow diagram (DFD) showing how data moves through the system.

2. **Select a Threat Modeling Methodology** — Choose the appropriate methodology based on the project's needs. Use STRIDE for systematic enumeration of threat categories per component. Use DREAD for scoring and prioritizing known threats. Use PASTA (Process for Attack Simulation and Threat Analysis) for risk-centric analysis aligned with business objectives. Use attack trees for deep analysis of specific high-value targets like authentication or payment systems.

3. **Enumerate Threats** — Apply the selected methodology to each component and data flow in the DFD. For STRIDE, evaluate each element against all six threat categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. Document each threat with a unique identifier, description, affected component, and the trust boundary it crosses.

4. **Assess Risk and Prioritize** — Score each threat using DREAD (Damage, Reproducibility, Exploitability, Affected Users, Discoverability) or a similar quantitative framework. Combine the score with business context — a threat to the payment service is higher priority than the same threat to an internal admin dashboard. Produce a ranked threat register.

5. **Define Mitigations and Security Controls** — For each high and medium priority threat, specify concrete mitigation strategies: architectural changes, code-level fixes, configuration hardening, or operational controls. Map mitigations to security frameworks (NIST 800-53, CIS Controls) where applicable. Estimate implementation effort for each mitigation.

6. **Document and Maintain the Threat Model** — Produce a living document that captures the DFD, threat register, risk scores, and mitigation status. Update the threat model whenever the architecture changes, new features are added, or new attack techniques emerge. Integrate threat model reviews into sprint planning and design review processes.

## Supported Technologies

- **Methodologies**: STRIDE, DREAD, PASTA, Attack Trees, VAST (Visual Agile Simple Threat modeling)
- **Diagramming**: Data Flow Diagrams (DFD), Mermaid, draw.io, Microsoft Threat Modeling Tool
- **Architecture Types**: Monoliths, microservices, serverless, event-driven, mobile backends, IoT systems
- **Infrastructure**: AWS, GCP, Azure, Kubernetes, on-premises hybrid environments
- **Standards Mapping**: OWASP Top 10, MITRE ATT&CK, NIST 800-53, CIS Controls

## Usage

Provide the agent with access to architecture documentation, source code, infrastructure-as-code files, or a description of the system. Specify the desired methodology and any compliance standards to map against. The agent will produce a complete threat model with a prioritized threat register and mitigation plan.

**Prompt example:**

```
Perform a STRIDE threat model on our microservices architecture. The services are defined in /infra/docker-compose.yml and the source code is in /services/. Focus on the API gateway, authentication service, and payment service. Map findings to OWASP Top 10.
```

## Examples

### Example 1: STRIDE Analysis for a Microservices E-Commerce Platform

**System Components**: API Gateway, Auth Service, Product Service, Payment Service, PostgreSQL database, Redis cache, RabbitMQ message broker.

**STRIDE Threat Table:**

| ID | Component | STRIDE Category | Threat Description | Risk | OWASP | Mitigation |
|----|-----------|-----------------|-------------------|------|-------|------------|
| T-01 | API Gateway | Spoofing | Attacker forges JWT tokens to impersonate users | High | A07:2021 | Validate JWT signatures using RS256 with key rotation; reject HS256 tokens |
| T-02 | API Gateway | Denial of Service | Volumetric attack overwhelms the gateway, blocking legitimate traffic | High | — | Implement rate limiting per client IP and API key; deploy behind a CDN with DDoS protection |
| T-03 | Auth Service | Spoofing | Credential stuffing using leaked username/password databases | High | A07:2021 | Enforce MFA, implement rate limiting on `/login`, integrate breach-detection APIs (HaveIBeenPwned) |
| T-04 | Auth Service | Repudiation | User denies performing a sensitive action (e.g., changing email) | Medium | A09:2021 | Log all authentication events and account changes to an immutable audit log with timestamps and source IP |
| T-05 | Payment Service | Tampering | Attacker modifies order total in transit between Product Service and Payment Service | Critical | A04:2021 | Sign inter-service messages with HMAC; Payment Service re-fetches price from database instead of trusting the request payload |
| T-06 | Payment Service | Information Disclosure | Credit card numbers logged in plaintext to application logs | Critical | A02:2021 | Mask PAN data in all logs; use a PCI-compliant tokenization service; restrict log access |
| T-07 | PostgreSQL | Tampering | SQL injection via Product Service search endpoint alters database records | High | A03:2021 | Use parameterized queries exclusively; apply least-privilege database roles per service |
| T-08 | RabbitMQ | Information Disclosure | Messages in transit between services are readable by network attackers | Medium | A02:2021 | Enable TLS for all RabbitMQ connections; encrypt sensitive message payloads at the application layer |
| T-09 | Redis Cache | Elevation of Privilege | Unauthenticated Redis instance allows any service to read/write session data | High | A01:2021 | Enable Redis AUTH with a strong password; bind to private network interface only; use ACLs to restrict key access per service |

### Example 2: Attack Tree for an Authentication System

**Root Goal**: Gain unauthorized access to a user account.

```
Gain Unauthorized Access to User Account
├── 1. Steal Valid Credentials
│   ├── 1.1 Phishing attack targeting user email [Likelihood: High]
│   ├── 1.2 Credential stuffing from breached databases [Likelihood: High]
│   └── 1.3 Keylogger malware on user device [Likelihood: Medium]
├── 2. Bypass Authentication
│   ├── 2.1 Exploit password reset flow
│   │   ├── 2.1.1 Predictable reset token (insufficient entropy) [Likelihood: Medium]
│   │   └── 2.1.2 Reset link does not expire [Likelihood: Low]
│   ├── 2.2 Session hijacking
│   │   ├── 2.2.1 Steal session cookie via XSS [Likelihood: Medium]
│   │   └── 2.2.2 Session fixation attack [Likelihood: Low]
│   └── 2.3 Forge or tamper with JWT
│       ├── 2.3.1 Algorithm confusion attack (HS256 vs RS256) [Likelihood: Medium]
│       └── 2.3.2 Weak signing secret (brute-forceable) [Likelihood: Medium]
├── 3. Exploit Authorization Flaws
│   ├── 3.1 IDOR — access another user's resources by changing user ID in URL [Likelihood: High]
│   └── 3.2 Privilege escalation — modify role claim in JWT payload [Likelihood: Medium]
└── 4. Compromise the Auth Service Directly
    ├── 4.1 SQL injection in login endpoint [Likelihood: Medium]
    └── 4.2 Exploit unpatched dependency in auth service [Likelihood: Medium]
```

**Mitigations derived from the attack tree:**

| Attack Path | Mitigation | Priority |
|-------------|-----------|----------|
| 1.2 Credential stuffing | Rate limit login to 5 attempts per minute per IP; integrate HaveIBeenPwned API; require MFA | Critical |
| 2.1.1 Predictable reset token | Generate tokens with 256-bit cryptographic randomness; expire after 15 minutes | High |
| 2.3.1 Algorithm confusion | Explicitly set `algorithms: ["RS256"]` in JWT verification; reject tokens with `alg: none` or `HS256` | High |
| 3.1 IDOR | Enforce server-side ownership checks on every resource access; never rely on client-supplied user IDs | High |
| 4.1 SQL injection | Use parameterized queries; deploy a WAF rule for SQL injection patterns on the login endpoint | High |

## Best Practices

- **Threat model early in the design phase** — identifying threats before code is written is dramatically cheaper than discovering them in production. Include threat modeling as a gate in the design review process.
- **Keep the model a living document** — a threat model created once and never updated is worse than useless because it creates a false sense of security. Review and update it with every major architectural change or new feature.
- **Involve cross-functional stakeholders** — developers understand the code, ops understands the deployment, and product understands the business impact. Effective threat modeling requires input from all three perspectives.
- **Focus on trust boundaries** — the most exploitable vulnerabilities occur where data crosses trust boundaries: between the user and the application, between services, between the application and the database. Prioritize threats at these junctions.
- **Use threat modeling to drive backlog items** — every mitigation identified should become a trackable work item with an owner and a deadline. Threat models that do not produce actionable backlog items have failed.
- **Validate threats with testing** — after identifying a threat, write a corresponding security test (penetration test, integration test, or DAST rule) that verifies the mitigation is effective.

## Safety Boundaries

- Work only on systems the user owns or is explicitly authorized to assess, and record the approved scope before testing.
- Start with passive or read-only inspection. Obtain explicit approval before active scanning, exploitation, load generation, or disruptive remediation.
- Never expose secrets, extract unrelated data, weaken production controls, or expand beyond the approved targets.
- Preserve evidence, minimize impact, stop on instability, and provide rollback or containment steps for every material change.

## Edge Cases

- **Microservices with shared databases** — when multiple services read and write to the same database, trust boundaries are blurred. A vulnerability in one service can compromise data that "belongs" to another service. Model each service's database access as a separate trust boundary and enforce schema-level isolation.
- **Third-party API integrations** — external APIs (payment processors, identity providers, analytics) introduce threats outside your control. Model the integration as an untrusted data source, validate all responses, and plan for API outages or data integrity failures.
- **Event-driven architectures** — in systems with message queues and event buses, threats include message injection, replay attacks, and out-of-order processing. Model the message broker as a component with its own trust boundary and ensure message authentication and idempotent processing.
- **Multi-tenant SaaS platforms** — threats unique to multi-tenancy include cross-tenant data leakage, noisy-neighbor denial of service, and tenant impersonation. Model tenant isolation at the network, application, and data layers separately.
- **Rapidly evolving systems with frequent deploys** — if the architecture changes weekly, a quarterly threat model review is insufficient. Integrate lightweight threat assessments into the PR review process for changes that modify trust boundaries, add new data flows, or introduce new external integrations.
