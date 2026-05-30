---
name: architecting-security
description: Design comprehensive security architectures using defense-in-depth, zero trust principles, threat modeling (STRIDE, PASTA), and control frameworks (NIST CSF, CIS Controls, ISO 27001). Use when designing security for new systems, auditing existing architectures, or establishing security governance programs.
---

# Security Architecture

Design and implement comprehensive security architectures that protect systems, data, and users through layered defense strategies, zero trust principles, and risk-based security controls.

## Purpose

Security architecture provides the strategic foundation for building resilient, compliant, and trustworthy systems. This skill guides the design of defense-in-depth layers, zero trust implementations, threat modeling methodologies, and mapping to control frameworks (NIST CSF, CIS Controls, ISO 27001).

Unlike tactical security skills (configuring firewalls, implementing authentication, scanning vulnerabilities), security architecture focuses on strategic planning, comprehensive defense strategies, and governance frameworks.

## When to Use This Skill

Use security architecture when:

- Designing security for greenfield systems (new applications, cloud migrations)
- Conducting security audits or risk assessments of existing systems
- Implementing zero trust architecture across enterprise environments
- Establishing security governance programs and compliance frameworks
- Threat modeling applications, APIs, or microservices architectures
- Selecting and mapping security controls to regulatory requirements (SOC 2, HIPAA, PCI DSS)
- Designing cloud security architectures (AWS, GCP, Azure multi-account strategies)
- Addressing supply chain security (SLSA framework, SBOM implementation)

## Core Security Architecture Principles

### 1. Defense in Depth

Implement multiple independent layers of security controls so that if one layer fails, others continue to protect critical assets.

**9 Defense Layers (2025 Model):**

1. **Physical Security:** Data center access, environmental controls, hardware security modules (HSMs)
2. **Network Perimeter:** Next-gen firewalls (NGFW), DDoS protection, web application firewalls (WAF)
3. **Network Segmentation:** VLANs, VPCs, security groups, micro-segmentation
4. **Endpoint Protection:** EDR, antivirus, device encryption, patch management
5. **Application Layer:** Secure coding, WAF, API security, SAST/DAST scanning
6. **Data Layer:** Encryption (at-rest, in-transit, in-use), DLP, backup/recovery
7. **Identity & Access Management:** MFA, SSO, RBAC/ABAC, privileged access management (PAM)
8. **Behavioral Analytics:** UEBA, ML-based anomaly detection, threat intelligence
9. **Security Operations:** SIEM, SOAR, incident response, continuous monitoring

**Key Principle:** Each layer provides independent protection. Failure of one layer does not compromise the entire system.

For detailed layer-by-layer implementation patterns, see `references/defense-in-depth.md`.

### 2. Zero Trust Architecture

Implement "never trust, always verify" principles where every access request is authenticated, authorized, and continuously validated.

**Core Zero Trust Principles:**

1. **Continuous Verification:** Authenticate and authorize every access request (no implicit trust)
2. **Least Privilege Access:** Grant minimal permissions required, use just-in-time (JIT) access
3. **Assume Breach:** Design systems expecting compromise, limit blast radius
4. **Explicit Verification:** Verify user identity (MFA), device health, application integrity, context (location, time, behavior)
5. **Micro-Segmentation:** Divide networks into small isolated zones, control east-west traffic

**Zero Trust Architecture Components:**

- **Policy Engine:** Centralized authorization decision point (allow/deny)
- **Identity Provider (IdP):** User/machine identity verification (Azure AD, Okta)
- **Device Posture Service:** Device health checks (MDM, EDR integration)
- **Context/Risk Engine:** Behavioral analytics, location, time, threat intelligence
- **Policy Enforcement Points:** Gateways enforcing decisions (ZTNA, API gateways)

For zero trust implementation roadmap and reference architecture, see `references/zero-trust-architecture.md`.

### 3. Threat Modeling

Systematically identify, prioritize, and mitigate security threats through structured methodologies.

**Primary Methodologies:**

| Methodology | Purpose | Complexity | Best For |
|-------------|---------|------------|----------|
| **STRIDE** | Threat identification | Low | Development teams, quick threat analysis |
| **PASTA** | Risk-centric analysis | High | Enterprise risk management |
| **DREAD** | Risk scoring | Low | Prioritizing existing threats |
| **Attack Trees** | Visual threat analysis | Medium | Security architecture reviews |

**STRIDE Threat Categories:**

- **S**poofing: Attacker impersonates another user/system (Mitigation: MFA, certificate validation)
- **T**ampering: Unauthorized data modification (Mitigation: Encryption, digital signatures)
- **R**epudiation: User denies action without proof (Mitigation: Audit logs, non-repudiation)
- **I**nformation Disclosure: Confidential data exposure (Mitigation: Encryption, access controls, DLP)
- **D**enial of Service: System unavailability (Mitigation: Rate limiting, DDoS protection, redundancy)
- **E**levation of Privilege: Gaining higher privileges (Mitigation: Least privilege, input validation, patching)

**STRIDE Application Process:**

1. Model the system using data flow diagrams (DFDs)
2. Identify threats by applying STRIDE to each component/data flow
3. Document threats with STRIDE categories
4. Prioritize threats using DREAD scoring or business impact
5. Design mitigation controls

For detailed threat modeling methodologies, PASTA process, DREAD scoring, and attack trees, see `references/threat-modeling.md`. For threat modeling examples, see `examples/threat-models/`.

## Security Control Frameworks

Map security controls to industry frameworks to ensure comprehensive coverage and compliance.

### NIST Cybersecurity Framework (CSF) 2.0

**6 Core Functions:**

1. **GOVERN (GV):** Risk management strategy, policies, supply chain risk management
2. **IDENTIFY (ID):** Asset inventory, risk assessment, continuous improvement
3. **PROTECT (PR):** Access control, data security, platform security, infrastructure resilience
4. **DETECT (DE):** Continuous monitoring, anomaly detection, security event analysis
5. **RESPOND (RS):** Incident management, analysis, communication, mitigation
6. **RECOVER (RC):** Recovery planning, execution, post-incident improvement

**Usage:** Map security controls to NIST CSF categories to ensure coverage of all security functions. Provides risk-based, flexible framework for security programs.

For detailed NIST CSF category mapping and subcategories, see `references/nist-csf-mapping.md`.

### CIS Critical Security Controls v8

**18 Controls organized in 3 Implementation Groups:**

- **IG1 (Basic):** 56 safeguards for small organizations (asset inventory, access control, logging, backups)
- **IG2 (Intermediate):** +74 safeguards for mid-sized organizations with IT security staff
- **IG3 (Advanced):** +23 safeguards for large enterprises with dedicated security teams

**Top Priority Controls (IG1):**
1. Inventory and Control of Enterprise Assets
2. Inventory and Control of Software Assets
3. Data Protection
4. Secure Configuration of Enterprise Assets
5. Account Management
6. Access Control Management
7. Continuous Vulnerability Management
8. Audit Log Management

**Usage:** CIS Controls provide prescriptive, measurable security baseline. Start with IG1, progress to IG2/IG3 as security maturity increases.

For detailed CIS Controls implementation guidance, see `references/cis-controls.md`.

### OWASP Top 10 Risk Mitigation

Map OWASP Top 10 application security risks to architectural controls:

| OWASP Risk | Primary Control | Framework Mapping |
|------------|-----------------|-------------------|
| **Injection** | Parameterized queries, input validation | NIST PR.DS, CIS 16 |
| **Broken Authentication** | MFA, secure session management | NIST PR.AC, CIS 5, 6 |
| **Sensitive Data Exposure** | Encryption, key management | NIST PR.DS, CIS 3 |
| **XXE** | Disable external entities, use JSON | NIST PR.DS, CIS 16 |
| **Broken Access Control** | Authorization checks, RBAC | NIST PR.AC, CIS 6 |
| **Security Misconfiguration** | Hardening, minimal configs | NIST PR.IP, CIS 4 |
| **XSS** | Output encoding, CSP | NIST PR.DS, CIS 16 |
| **Insecure Deserialization** | Validate objects, safe formats | NIST PR.DS, CIS 16 |
| **Known Vulnerabilities** | Patch management, SBOM | NIST ID.RA, CIS 7 |
| **Logging & Monitoring** | SIEM, centralized logging | NIST DE.CM, CIS 8 |

For detailed OWASP Top 10 mitigation strategies and code examples, see `references/owasp-top10-mitigation.md`.

## Architecture Selection Decision Framework

Select appropriate security architecture approach based on system characteristics:

**Greenfield (New System):**
- Implement Zero Trust from Day 1
- Identity-first architecture (MFA, SSO, RBAC/ABAC)
- Micro-segmentation by default
- Assume breach mentality (limit blast radius)
- Continuous verification and monitoring

**Brownfield (Existing System):**
- Hybrid: Maintain Defense in Depth + Zero Trust overlay
- Keep existing perimeter controls (firewalls, VPN)
- Layer Zero Trust controls progressively
- Segment critical assets first (data, admin access)
- Modernize identity and access management

**Compliance-Driven:**
- Map to control frameworks based on requirements:
  - **General Security:** NIST CSF for risk-based approach
  - **Baseline Hardening:** CIS Controls for prescriptive guidance
  - **Comprehensive ISMS:** ISO 27001 for certification
  - **Industry-Specific:** PCI DSS (payments), HIPAA Security Rule (healthcare), FedRAMP (government)

**Cloud-Native:**
- Use cloud provider reference architectures:
  - **AWS:** Well-Architected Framework (Security Pillar)
  - **GCP:** Security Best Practices, Security Command Center
  - **Azure:** Security Benchmark, Defender for Cloud
- Implement cloud-native security services (CSPM, CWPP)

**Hybrid/Multi-Cloud:**
- Cloud Security Posture Management (CSPM) for unified policy enforcement
- Cross-cloud visibility and monitoring
- Cloud-agnostic IAM (Okta, Azure AD)

For detailed architecture selection decision trees, see `references/defense-in-depth.md` and `references/zero-trust-architecture.md`.

## Supply Chain Security

Protect software supply chain from tampering, backdoors, and compromised dependencies.

### SLSA Framework

**Supply-chain Levels for Software Artifacts (4 levels):**

1. **SLSA Level 1 - Provenance:** Build process generates provenance metadata (not tamper-proof)
2. **SLSA Level 2 - Hosted Build:** Build on trusted platform (GitHub Actions, Cloud Build)
3. **SLSA Level 3 - Hardened Build:** Build platform prevents tampering, audit logs
4. **SLSA Level 4 - Hermetic, Reproducible:** Fully hermetic builds, reproducible, two-party review

**Implementation:** Start with Level 1 provenance generation, progress to Level 2 (GitHub Actions), then Level 3 (hardened CI/CD with audit logs).

### SBOM (Software Bill of Materials)

Generate and maintain inventory of software components and dependencies.

**SBOM Standards:**
- **CycloneDX:** OWASP standard (JSON/XML format)
- **SPDX:** Linux Foundation standard
- **SWID:** ISO/IEC 19770-2 standard

**SBOM Use Cases:**
- Vulnerability Management: Quickly identify affected components during CVE disclosures
- License Compliance: Track open-source licenses for legal compliance
- Supply Chain Risk: Visibility into third-party code and dependencies
- Incident Response: Rapid assessment of Log4Shell-type incidents

**Dependency Management Best Practices:**
1. Generate SBOM automatically in CI/CD pipeline
2. Continuous scanning with tools (Dependabot, Snyk, Trivy, Grype)
3. Automated security patch updates
4. License compliance tracking and approval workflows
5. Pin dependency versions using lock files
6. Minimize dependencies to reduce attack surface

For SLSA implementation guide, SBOM generation examples, and dependency scanning automation, see `references/supply-chain-security.md`.

## Cloud Security Architecture Patterns

### AWS Security Architecture

**Well-Architected Framework - Security Pillar Principles:**

1. **Strong identity foundation:** Centralize IAM, least privilege, IAM Identity Center (SSO)
2. **Enable traceability:** CloudTrail, GuardDuty, Security Hub for comprehensive logging
3. **Apply security at all layers:** Defense in depth across VPC, instances, applications, data
4. **Automate security best practices:** Infrastructure as Code (Terraform, CloudFormation)
5. **Protect data in transit and at rest:** TLS 1.3, AWS KMS, encryption everywhere

**Key AWS Security Services:**

- **IAM:** AWS IAM, IAM Identity Center (SSO), Cognito (customer identity)
- **Detection:** GuardDuty (threat detection), Security Hub (centralized findings), Detective (investigation)
- **Network:** AWS WAF, Shield (DDoS), Network Firewall
- **Data:** KMS (key management), Secrets Manager, Macie (data classification)
- **Compute:** Systems Manager (patch management), Inspector (vulnerability scanning)

**Multi-Account Strategy:** Use AWS Organizations with Security OU (Security Account, Logging Account, Audit Account) and Workload OUs (Production, Non-Production). Apply Service Control Policies (SCPs) for guardrails.

For AWS reference architectures and multi-account security setup, see `references/aws-security-architecture.md` and `examples/architectures/aws-multi-account-security.md`.

### GCP Security Architecture

**Key GCP Security Services:**

- **IAM:** Cloud IAM, Identity Platform (customer identity), Cloud Identity (workforce)
- **Detection:** Security Command Center (unified dashboard), Chronicle (SIEM), Event Threat Detection
- **Network:** Cloud Armor (DDoS/WAF), VPC Service Controls (data exfiltration prevention), Cloud Firewall
- **Data:** Cloud KMS, Secret Manager, Cloud DLP (data loss prevention)
- **Compute:** Binary Authorization (image signing), Confidential Computing (encryption in use)

**Organization Hierarchy:** Structure with Organization → Folders (Production, Non-Production, Security) → Projects. Apply IAM policies at folder level for inheritance.

For GCP security architecture patterns and organization setup, see `references/gcp-security-architecture.md` and `examples/architectures/gcp-security-hierarchy.md`.

### Azure Security Architecture

**Key Azure Security Services:**

- **IAM:** Azure AD (Entra ID), Privileged Identity Management (JIT access), Conditional Access
- **Detection:** Microsoft Defender for Cloud (CSPM/CWPP), Sentinel (SIEM/SOAR), Azure Monitor
- **Network:** Azure Firewall, Front Door + WAF, DDoS Protection
- **Data:** Key Vault (secrets, keys, certificates), Information Protection (DLP), Storage encryption
- **Compute:** Just-in-Time VM Access, Azure Policy (compliance enforcement)

**Hub-Spoke Landing Zone:** Implement hub VNet (shared services: firewall, VPN, Azure Bastion) with spoke VNets (workloads). Use Management Groups for policy hierarchy.

For Azure security architecture and hub-spoke design, see `references/azure-security-architecture.md` and `examples/architectures/azure-landing-zone.md`.

## Identity & Access Management Patterns

### Authentication Controls

**Multi-Factor Authentication (MFA):**
- **Types:** TOTP (time-based one-time passwords), push notifications, biometrics, hardware tokens (YubiKey, FIDO2)
- **Enforcement:** Require MFA for all users (workforce and customers), especially privileged accounts
- **Passwordless:** Transition to WebAuthn, FIDO2, passkeys to eliminate password-based attacks

**Single Sign-On (SSO):**
- **Protocols:** SAML 2.0, OAuth 2.0, OpenID Connect (OIDC)
- **Benefits:** Centralized authentication, reduced password fatigue, improved security posture
- **Implementation:** Azure AD, Okta, Auth0, Ping Identity

### Authorization Controls

**Role-Based Access Control (RBAC):**
- Users assigned to roles, roles have permissions
- Coarse-grained, simple to implement
- Best for: Organizations with stable role structures

**Attribute-Based Access Control (ABAC):**
- Fine-grained access based on attributes (user department, resource classification, time, location)
- More flexible than RBAC
- Best for: Complex, dynamic access requirements

**Policy-Based Access Control (PBAC):**
- Centralized policy engines (Open Policy Agent - OPA, AWS Cedar)
- Policies defined declaratively and versioned
- Best for: Microservices, API gateways, cloud-native architectures

### Privileged Access Management (PAM)

**Just-in-Time (JIT) Access:**
- Temporary elevated privileges for specific tasks
- Time-bound access grants (e.g., 4 hours)
- Reduces standing privileged access

**Credential Vaulting:**
- Centralized storage of privileged credentials (CyberArk, HashiCorp Vault, Azure Key Vault)
- Automatic password rotation
- Session recording and auditing

For detailed IAM implementation patterns, MFA configuration, and PAM setup, see `references/iam-patterns.md`.

## Security Monitoring & Operations

### SIEM (Security Information & Event Management)

Centralize log aggregation, correlation, and alerting for security events.

**Leading SIEM Platforms:**
- Splunk, Elastic Security, Microsoft Sentinel, Chronicle

**SIEM Architecture:**
1. **Log Collection:** Ingest logs from all layers (network, endpoints, applications, cloud)
2. **Normalization:** Standardize log formats for correlation
3. **Correlation:** Apply rules to detect patterns (failed logins → brute force attack)
4. **Alerting:** Notify SOC team of high-priority events
5. **Investigation:** Provide search and visualization for incident analysis

### SOAR (Security Orchestration, Automation & Response)

Automate incident response workflows to reduce mean time to respond (MTTR).

**SOAR Capabilities:**
- **Playbooks:** Automated response workflows (block IP, quarantine endpoint, revoke credentials)
- **Orchestration:** Integrate with security tools (SIEM, EDR, firewall, IAM)
- **Case Management:** Track incidents, assign to analysts, document resolution

**Leading SOAR Platforms:**
- Splunk SOAR, Palo Alto Cortex XSOAR, IBM Resilient

### Detection Strategies

**UEBA (User & Entity Behavior Analytics):**
- Machine learning-based anomaly detection
- Detects: Account compromise, insider threats, data exfiltration
- Baseline normal behavior, alert on deviations

**Threat Intelligence:**
- Integrate threat feeds (MISP, ThreatConnect, ISACs)
- Enrich alerts with threat context (known malicious IPs, IOCs)
- Proactive threat hunting using TTPs (MITRE ATT&CK framework)

For SIEM architecture, SOAR playbook examples, and detection strategies, see `references/security-operations.md`.

## Quick Reference: Control Framework Mapping

Use this table to map risks to appropriate control frameworks:

| Risk/Requirement | Framework | Key Controls |
|------------------|-----------|--------------|
| General security program | NIST CSF 2.0 | All 6 functions (GV, ID, PR, DE, RS, RC) |
| Compliance baseline | CIS Controls v8 | IG1: Controls 1-18 (56 safeguards) |
| ISO certification | ISO 27001/27002 | 114 controls across 14 domains |
| Application security | OWASP ASVS | 286 security requirements (3 levels) |
| Cloud security (AWS) | AWS Well-Architected | Security Pillar: 10 design principles |
| Cloud security (GCP) | GCP Security Best Practices | Security Command Center architecture |
| Cloud security (Azure) | Azure Security Benchmark | Defender for Cloud controls |
| Supply chain security | SLSA + SBOM | Level 2+ SLSA, CycloneDX SBOM |
| Zero trust architecture | NIST SP 800-207 | ZTA tenets, deployment models |
| Privacy/GDPR | NIST Privacy Framework | Privacy engineering objectives |

## Integration with Related Skills

Security architecture provides the strategic foundation for tactical security implementations:

- **`infrastructure-as-code`:** Implement security architecture as code (secure defaults, hardening)
- **`kubernetes-operations`:** Apply K8s security architecture (RBAC, Pod Security, Network Policies)
- **`secret-management`:** Architect secrets management (KMS, Vault, rotation strategies)
- **`building-ci-pipelines`:** Secure CI/CD architecture (SAST/DAST integration, artifact signing)
- **`configuring-firewalls`:** Implement network perimeter layer of defense-in-depth
- **`vulnerability-management`:** Integrate vulnerability scanning into security architecture
- **`auth-security`:** Implement IAM layer details (MFA, RBAC/ABAC, session management)
- **`siem-logging`:** Implement security monitoring architecture (SIEM, log aggregation)
- **`compliance-frameworks`:** Map security architecture to compliance requirements

## Common Security Architecture Patterns

### Pattern 1: Zero Trust Network Access (ZTNA)

Replace VPN with identity-based access to applications.

**Architecture:**
1. User authenticates to identity provider (Azure AD, Okta)
2. Device posture check validates device health
3. Policy engine evaluates access request (user, device, context)
4. Access granted through secure connector (no network access)

**Benefits:** Eliminates lateral movement, reduces attack surface, improves user experience

### Pattern 2: Defense in Depth for Web Applications

Layer multiple security controls for web application protection.

**Layers:**
1. DDoS Protection (Cloudflare, AWS Shield)
2. WAF (application firewall, OWASP Top 10 rules)
3. API Gateway (authentication, rate limiting)
4. Application Security (SAST/DAST, secure coding)
5. Database Security (encryption, least privilege)
6. Logging & Monitoring (SIEM, anomaly detection)

### Pattern 3: Cloud Security Posture Management (CSPM)

Continuously monitor and enforce security configurations across cloud environments.

**Architecture:**
1. Asset Discovery: Inventory all cloud resources
2. Configuration Assessment: Compare against security baselines (CIS Benchmarks)
3. Compliance Monitoring: Track regulatory compliance (SOC 2, ISO 27001)
4. Remediation: Automated fixes or guided workflows
5. Drift Detection: Alert on configuration changes

**Leading CSPM Tools:** Wiz, Orca Security, Prisma Cloud, Microsoft Defender for Cloud

## Resources and References

**Defense in Depth:**
- `references/defense-in-depth.md` - 9-layer defense model, implementation patterns, failure impact analysis

**Zero Trust Architecture:**
- `references/zero-trust-architecture.md` - ZTA principles, reference architecture, implementation roadmap

**Threat Modeling:**
- `references/threat-modeling.md` - STRIDE, PASTA, DREAD, Attack Trees methodologies
- `examples/threat-models/web-app-stride.md` - Web application STRIDE analysis example
- `examples/threat-models/api-threat-model.md` - REST API threat model example
- `examples/threat-models/microservices-threat-model.md` - Microservices threat model example

**Control Frameworks:**
- `references/nist-csf-mapping.md` - NIST CSF 2.0 functions, categories, subcategories
- `references/cis-controls.md` - CIS Controls v8, implementation groups, safeguards
- `references/owasp-top10-mitigation.md` - OWASP Top 10 risks and mitigation strategies

**Supply Chain Security:**
- `references/supply-chain-security.md` - SLSA framework, SBOM generation, dependency scanning

**Cloud Security:**
- `references/aws-security-architecture.md` - AWS Well-Architected Security Pillar, services, patterns
- `references/gcp-security-architecture.md` - GCP Security Best Practices, services, organization design
- `references/azure-security-architecture.md` - Azure Security Benchmark, Defender for Cloud, landing zones

**IAM & Operations:**
- `references/iam-patterns.md` - Authentication, authorization, MFA, RBAC/ABAC, PAM
- `references/security-operations.md` - SIEM, SOAR, UEBA, threat intelligence, incident response

**Architecture Examples:**
- `examples/architectures/aws-multi-account-security.md` - AWS Organizations security setup
- `examples/architectures/gcp-security-hierarchy.md` - GCP folder/project security hierarchy
- `examples/architectures/azure-landing-zone.md` - Azure hub-spoke landing zone
- `examples/architectures/zero-trust-network.md` - Zero trust network design

**Scripts:**
- `scripts/threat-model-template.py` - Generate STRIDE threat model templates
- `scripts/control-gap-analysis.sh` - Compare current controls against frameworks
- `scripts/sbom-generate.sh` - Generate SBOM in CycloneDX format
- `scripts/security-checklist.sh` - Automated security architecture checklist

## Summary

Security architecture requires strategic planning across multiple layers, from physical security to security operations. Implement defense-in-depth for comprehensive protection, adopt zero trust principles for modern cloud environments, use threat modeling to identify risks proactively, and map controls to frameworks for compliance and completeness.

Start with risk assessment to understand threats, select appropriate architecture approach (zero trust for greenfield, hybrid for brownfield), implement layered controls, and continuously monitor and improve security posture.
