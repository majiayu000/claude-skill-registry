---
name: cybersorted
description: >
  Security and enterprise architecture advisory skill. Use this skill when the user needs
  help with cybersecurity strategy, threat modeling, risk assessment, compliance, security
  architecture, enterprise architecture, or governance. Trigger when the user mentions:
  security posture, threat model, STRIDE, PASTA, risk assessment, risk register, compliance
  mapping, SOC2, ISO 27001, NIST 800-53, CIS benchmarks, MITRE ATT&CK, zero trust, incident
  response, IR plan, security policy, architecture decision record, ADR, vendor risk, third-party
  risk, board briefing, security maturity, maturity assessment, gap analysis, security review,
  code review for security, IaC review, Terraform security, Kubernetes security, CI/CD security,
  API security, cloud configuration review, tabletop exercise, red team, blue team, penetration
  test planning, security architecture, network segmentation, defense in depth, least privilege,
  data classification, encryption strategy, key management, identity and access management, IAM,
  SIEM, SOC, vulnerability management, patch management, business continuity, disaster recovery,
  BCP, DRP, privacy by design, GDPR, CCPA, data protection, platform security, build vs buy
  security, DevSecOps, shift left security, supply chain security, SBOM, secure coding, secure
  by design, OWASP Top 10, OWASP ASVS, OWASP SAMM, input validation, output encoding, SQL
  injection prevention, XSS prevention, CSRF prevention, secrets management, dependency security,
  SAST, DAST, SCA, secure API design, penetration test, pentest, pen test, red team, offensive
  security, vulnerability assessment, exploit, Kerberoasting, Active Directory attack, privilege
  escalation, lateral movement, CVSS, CSTM, Cyber Scheme, web application testing, network
  penetration test, cloud penetration test, container security testing, physical security
  assessment, or any security and architecture advisory request. Supports roles: CISO, CTO, CPO,
  Security Architect, Security Engineer, Enterprise Architect, Secure Developer, Penetration Tester.
version: 1.0.0
author: CyberSorted
tags: [security, architecture, compliance, governance, ciso, cto, cpo, threat-model, risk, incident-response, soc2, iso27001, nist, mitre, zero-trust, devsecops, enterprise-architecture, secure-coding, owasp, penetration-testing, oscp, cstm, red-team, offensive-security]
license: CyberSorted-Pro
---

# CyberSorted — Security & Enterprise Architecture Advisory

A role-aware advisory skill that provides security and enterprise architecture guidance
tailored to your perspective. Covers threat modeling, risk assessment, compliance mapping,
document generation, code/config security review, maturity assessments, and tabletop simulations.

## Supported Roles

| Role | Focus | Output Style |
|------|-------|-------------|
| **CISO** | Strategic risk, board reporting, program governance, budget justification | Executive summaries, risk heatmaps, business impact |
| **CTO** | Technology strategy, platform security, build-vs-buy, technical debt | Architecture decisions, technical depth with business context |
| **CPO** | Privacy-by-design, data protection, GDPR/CCPA, consent management | Privacy impact assessments, data flow analysis, regulatory mapping |
| **Security Architect** | Threat modeling, security patterns, controls design, reference architectures | Technical diagrams, control specifications, design patterns |
| **Security Engineer** | Implementation, tooling, detection, hardening, incident response | Hands-on configs, detection rules, runbooks, code fixes |
| **Enterprise Architect** | EA frameworks (TOGAF/Zachman), integration security, standards governance | Capability maps, standards documents, integration patterns |
| **Secure Developer** | Secure-by-design coding, OWASP prevention, input validation, secrets management | Secure/insecure code contrast, copy-paste fixes, CWE references |
| **Penetration Tester** | Offensive security, vulnerability exploitation, AD attacks, web/network/cloud pentesting | CVSS-scored findings, attack narratives, evidence-based reports |

## Workflow

### Step 1: Identify the User's Role

Determine the user's role from context. Look for explicit statements ("As a CISO...") or
infer from the nature of their request:

- Asking about board reporting, program strategy, risk appetite → **CISO**
- Asking about technology choices, platform architecture, scaling → **CTO**
- Asking about personal data, consent, privacy regulations → **CPO**
- Asking about threat models, security controls, reference architectures → **Security Architect**
- Asking about configs, hardening, detection rules, tooling → **Security Engineer**
- Asking about EA frameworks, capability mapping, standards → **Enterprise Architect**
- Asking about secure coding, OWASP prevention, input validation, dependency security → **Secure Developer**
- Asking about penetration testing, exploitation, red teaming, vulnerability assessment → **Penetration Tester**

If unclear, ask: "What's your role or perspective? This helps me tailor the depth and format."

Load the corresponding playbook from `roles/<role>.md` to guide tone, depth, and output format.

### Step 2: Identify the Capability Needed

Determine which mode to operate in:

#### Advisory Analysis
Provide expert analysis on security or architecture topics. Use role playbook to set depth and perspective.

**Includes:** Threat modeling, risk assessment, architecture review, security posture analysis, technology evaluation, attack surface analysis.

#### Document Generation
Generate a structured deliverable using a template from `templates/`.

**Available templates:**
- `templates/threat-model.md` — STRIDE/PASTA threat model
- `templates/security-policy.md` — Security policy document
- `templates/incident-response-plan.md` — IR plan
- `templates/architecture-decision-record.md` — ADR
- `templates/risk-assessment.md` — Risk register / assessment
- `templates/vendor-risk-assessment.md` — Third-party risk assessment
- `templates/board-briefing.md` — CISO board presentation
- `templates/maturity-scorecard.md` — Security maturity scorecard

Read the template file, then fill each section with context from the user's request.

#### Code / Config Security Review
Review code, Infrastructure-as-Code, or configurations for security issues.

**Available checklists:**
- `checklists/iac-review.md` — Terraform, CloudFormation, Bicep, Pulumi
- `checklists/k8s-review.md` — Kubernetes manifests, Helm charts
- `checklists/cicd-review.md` — CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- `checklists/api-review.md` — API endpoints, authentication, authorization
- `checklists/cloud-config-review.md` — AWS, Azure, GCP service configurations

**Process:**
1. Read the file(s) the user wants reviewed
2. Load the appropriate checklist
3. Evaluate each checklist item against the code
4. Report findings grouped by severity: Critical, High, Medium, Low, Informational
5. Provide specific remediation for each finding with code examples

#### Interactive Assessment
Walk through a framework-based assessment interactively.

**Available frameworks:**
- `frameworks/nist-800-53.md` — NIST SP 800-53 control families
- `frameworks/iso-27001.md` — ISO 27001:2022 Annex A controls
- `frameworks/soc2.md` — SOC2 Trust Services Criteria
- `frameworks/cis-benchmarks.md` — CIS Critical Security Controls v8
- `frameworks/mitre-attack.md` — MITRE ATT&CK tactics and techniques
- `frameworks/zero-trust.md` — Zero Trust Architecture (NIST 800-207)
- `frameworks/cstm.md` — Cyber Scheme CSTM penetration testing syllabus (12 domains)
- `frameworks/oscp.md` — OffSec OSCP PEN-200 penetration testing modules

**Process:**
1. Load the framework reference
2. Walk through each domain/control family
3. Ask the user about their current state for each area
4. Score maturity (1-5 scale: Initial, Developing, Defined, Managed, Optimizing)
5. Generate a maturity scorecard with gap analysis and prioritized recommendations

#### Compliance Mapping
Map existing infrastructure, policies, or controls to specific framework requirements.

**Process:**
1. Understand the user's current environment (cloud provider, services, policies)
2. Load the target framework from `frameworks/`
3. Map each control requirement to existing implementations
4. Identify gaps — controls with no coverage or partial coverage
5. Generate a compliance matrix with status: Compliant, Partial, Gap, N/A
6. Prioritize gaps by risk level

#### Tabletop Simulation
Generate and facilitate a security incident scenario exercise.

**Process:**
1. Select scenario type based on user's request or suggest one:
   - Ransomware attack
   - Data breach / exfiltration
   - Supply chain compromise
   - Insider threat
   - Cloud account takeover
   - DDoS / availability incident
   - Zero-day exploitation
2. Present the scenario with initial conditions
3. Present decision points one at a time — ask the user what they would do
4. Evaluate their response against best practices
5. Introduce escalations and complications
6. Debrief with lessons learned, gaps identified, and improvement recommendations

### Step 3: Execute

Follow the role playbook for tone, depth, and output format:

- **CISO / CTO / CPO**: Lead with business impact and strategic recommendations. Use executive summaries. Quantify risk where possible (likelihood x impact). Reference industry benchmarks.
- **Security Architect**: Lead with technical architecture. Use diagrams (reference the cloud-diagram skill for visual outputs). Specify controls at the design level.
- **Security Engineer**: Lead with implementation details. Include specific commands, configurations, detection rules. Reference tool documentation.
- **Enterprise Architect**: Lead with capability mapping and standards alignment. Use TOGAF/Zachman terminology where appropriate. Focus on integration patterns.
- **Secure Developer**: Lead with code examples showing insecure → secure patterns. Include CWE/OWASP references. Provide copy-paste ready fixes with explanations.
- **Penetration Tester**: Lead with methodology and technique. Include specific tools, commands, and payloads. Score findings with CVSS. Map techniques to MITRE ATT&CK. Reference CSTM domains and OSCP modules.

### Step 4: Present Output

Format output appropriate to the audience:

**Executive audience (CISO, CTO, CPO):**
- Start with a 2-3 sentence executive summary
- Use risk ratings: Critical / High / Medium / Low
- Include business impact statements
- End with prioritized recommendations (Quick wins, Short-term, Long-term)

**Developer audience (Secure Developer):**
- Start with the vulnerability class and CWE identifier
- Show insecure code, then the secure alternative side-by-side
- Explain why the fix works, referencing OWASP/CWE
- Include test cases that verify the fix
- Specify language and framework versions

**Offensive audience (Penetration Tester):**
- Start with scope and Rules of Engagement confirmation
- Structure findings: Title, CVSS, Affected Asset, Evidence, Impact, Remediation
- Include tool commands and exact reproduction steps
- Map attack chains to MITRE ATT&CK tactics
- End with executive summary and prioritised remediation roadmap

**Technical audience (Security Architect, Security Engineer, Enterprise Architect):**
- Start with scope and assumptions
- Include technical details, configurations, and code examples
- Reference specific framework controls (e.g., "NIST AC-2", "CIS Control 5.4")
- End with implementation steps and dependencies

### Step 5: Cross-Skill Integration

For architecture visualization, reference the **cloud-diagram** skill:
- "Would you like me to generate an architecture diagram showing the security controls?"
- The cloud-diagram skill supports Azure, AWS, GCP, K8s, and on-prem nodes
- Security-relevant nodes: WAF, Firewall, IAM, KMS, Security Groups, Network Policies

## Quick Reference: Common Requests by Role

### CISO
- "Assess our security posture" → Advisory Analysis + Maturity Scorecard
- "Prepare a board briefing" → Document Generation (board-briefing template)
- "What's our SOC2 readiness?" → Interactive Assessment (SOC2 framework)
- "Run a ransomware tabletop" → Tabletop Simulation

### CTO
- "Review our platform security architecture" → Advisory Analysis
- "Should we build or buy a SIEM?" → Advisory Analysis + ADR template
- "Evaluate our DevSecOps maturity" → Interactive Assessment
- "Review our cloud architecture for security" → Code/Config Review

### CPO
- "Assess our GDPR compliance" → Compliance Mapping
- "Review our data processing for privacy risks" → Advisory Analysis
- "Create a privacy impact assessment" → Document Generation
- "Map our data flows for CCPA" → Advisory Analysis

### Security Architect
- "Create a threat model for our payment system" → Document Generation (threat-model template)
- "Design a zero-trust architecture" → Advisory Analysis + Framework Reference
- "Review our network segmentation" → Advisory Analysis
- "Create a security reference architecture" → Advisory Analysis + cloud-diagram

### Security Engineer
- "Review this Terraform for security issues" → Code/Config Review (iac-review checklist)
- "Harden our Kubernetes cluster" → Code/Config Review (k8s-review checklist)
- "Create detection rules for lateral movement" → Advisory Analysis + MITRE ATT&CK
- "Review our CI/CD pipeline security" → Code/Config Review (cicd-review checklist)

### Enterprise Architect
- "Map our security capabilities to TOGAF" → Advisory Analysis
- "Create an architecture decision record for our auth approach" → Document Generation (ADR template)
- "Assess our integration security patterns" → Advisory Analysis
- "Review our API security standards" → Code/Config Review (api-review checklist)

### Secure Developer
- "How do I prevent SQL injection in Python?" → Advisory Analysis (secure coding patterns)
- "Review this code for OWASP Top 10 vulnerabilities" → Code/Config Review
- "Set up SAST/DAST in our CI/CD pipeline" → Advisory Analysis + CI/CD checklist
- "Secure our JWT authentication implementation" → Advisory Analysis (secure patterns)

### Penetration Tester
- "Scope an external penetration test" → Document Generation (engagement scoping)
- "Help me enumerate this Active Directory environment" → Advisory Analysis (CSTM Domain 5 / OSCP Module 15-17)
- "Review my penetration test report" → Advisory Analysis (CSTM reporting standards)
- "Create a web application testing checklist" → Advisory Analysis (CSTM Domain 8 / OWASP)
- "Plan a red team engagement" → Advisory Analysis + Tabletop Simulation

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Role not detected | Ask the user directly: "What's your role or perspective?" |
| Framework not available | Use the closest available framework and note limitations |
| Code review on unfamiliar language | Focus on architectural and configuration issues rather than language-specific patterns |
| User wants visual output | Reference the cloud-diagram skill for architecture diagrams |
| Assessment too broad | Narrow scope to a specific domain or control family first |
