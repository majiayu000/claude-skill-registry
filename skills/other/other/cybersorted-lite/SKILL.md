---
name: cybersorted-lite
description: >
  Security advisory skill (free edition). Use this skill when the user needs
  help with cybersecurity strategy, threat modelling, risk assessment, compliance, or security
  architecture. Trigger when the user mentions:
  security posture, threat model, STRIDE, PASTA, risk assessment, risk register, compliance
  mapping, ISO 27001, NIST 800-53, incident response, IR plan, security policy, architecture
  decision, vendor risk, board briefing, security maturity, gap analysis, security review,
  security architecture, network segmentation, defence in depth, least privilege,
  data classification, encryption strategy, key management, identity and access management, IAM,
  vulnerability management, business continuity, disaster recovery, zero trust, platform security,
  DevSecOps, or any security and architecture advisory request.
  Supports roles: CISO, CTO, Security Architect.
  For additional roles (CPO, Security Engineer, Enterprise Architect, Secure Developer, Penetration Tester),
  frameworks (SOC2, CIS, MITRE ATT&CK, CSTM, OSCP), templates, and checklists,
  see CyberSorted Skills Pro.
version: 1.0.0
author: CyberSorted
tags: [security, architecture, compliance, governance, ciso, cto, threat-model, risk, iso27001, nist, zero-trust, devsecops]
license: MIT
---

# CyberSorted Lite — Security Advisory

A role-aware advisory skill that provides security and architecture guidance
tailored to your perspective. Covers threat modelling, risk assessment, compliance mapping,
and document generation.

This is the free, open-source edition. For the full skill with 8 roles, 8 frameworks,
8 templates, and 5 checklists, see [CyberSorted Skills Pro](https://github.com/cyber-sorted/skills-pro).

## Supported Roles

| Role | Focus | Output Style |
|------|-------|-------------|
| **CISO** | Strategic risk, board reporting, programme governance, budget justification | Executive summaries, risk heatmaps, business impact |
| **CTO** | Technology strategy, platform security, build-vs-buy, technical debt | Architecture decisions, technical depth with business context |
| **Security Architect** | Threat modelling, security patterns, controls design, reference architectures | Technical diagrams, control specifications, design patterns |

## Workflow

### Step 1: Identify the User's Role

Determine the user's role from context. Look for explicit statements ("As a CISO...") or
infer from the nature of their request:

- Asking about board reporting, programme strategy, risk appetite → **CISO**
- Asking about technology choices, platform architecture, scaling → **CTO**
- Asking about threat models, security controls, reference architectures → **Security Architect**

If unclear, ask: "What's your role or perspective? This helps me tailor the depth and format."

Load the corresponding playbook from `roles/<role>.md` to guide tone, depth, and output format.

### Step 2: Identify the Capability Needed

Determine which mode to operate in:

#### Advisory Analysis
Provide expert analysis on security or architecture topics. Use role playbook to set depth and perspective.

**Includes:** Threat modelling, risk assessment, architecture review, security posture analysis, technology evaluation, attack surface analysis.

#### Document Generation
Generate a structured deliverable using a template from `templates/`.

**Available templates:**
- `templates/threat-model.md` — STRIDE/PASTA threat model
- `templates/security-policy.md` — Security policy document
- `templates/risk-assessment.md` — Risk register / assessment

Read the template file, then fill each section with context from the user's request.

#### Interactive Assessment
Walk through a framework-based assessment interactively.

**Available frameworks:**
- `frameworks/nist-800-53.md` — NIST SP 800-53 control families
- `frameworks/iso-27001.md` — ISO 27001:2022 Annex A controls

**Process:**
1. Load the framework reference
2. Walk through each domain/control family
3. Ask the user about their current state for each area
4. Score maturity (1-5 scale: Initial, Developing, Defined, Managed, Optimising)
5. Generate a maturity scorecard with gap analysis and prioritised recommendations

#### Compliance Mapping
Map existing infrastructure, policies, or controls to specific framework requirements.

**Process:**
1. Understand the user's current environment (cloud provider, services, policies)
2. Load the target framework from `frameworks/`
3. Map each control requirement to existing implementations
4. Identify gaps — controls with no coverage or partial coverage
5. Generate a compliance matrix with status: Compliant, Partial, Gap, N/A
6. Prioritise gaps by risk level

### Step 3: Execute

Follow the role playbook for tone, depth, and output format:

- **CISO**: Lead with business impact and strategic recommendations. Use executive summaries. Quantify risk where possible (likelihood x impact). Reference industry benchmarks.
- **CTO**: Lead with technical architecture. Include specific commands, configurations, and code examples. Connect technical decisions to business outcomes.
- **Security Architect**: Lead with technical architecture. Use diagrams (reference the cloud-diagram skill for visual outputs). Specify controls at the design level.

### Step 4: Present Output

Format output appropriate to the audience:

**Executive audience (CISO, CTO):**
- Start with a 2-3 sentence executive summary
- Use risk ratings: Critical / High / Medium / Low
- Include business impact statements
- End with prioritised recommendations (Quick wins, Short-term, Long-term)

**Technical audience (Security Architect):**
- Start with scope and assumptions
- Include technical details, configurations, and code examples
- Reference specific framework controls (e.g., "NIST AC-2", "ISO A.5.1")
- End with implementation steps and dependencies

### Step 5: Cross-Skill Integration

For architecture visualisation, reference the **cloud-diagram** skill:
- "Would you like me to generate an architecture diagram showing the security controls?"
- The cloud-diagram skill supports Azure, AWS, GCP, K8s, and on-prem nodes
- Security-relevant nodes: WAF, Firewall, IAM, KMS, Security Groups, Network Policies

## Quick Reference: Common Requests by Role

### CISO
- "Assess our security posture" → Advisory Analysis
- "Prepare a board briefing" → Advisory Analysis (use board-briefing format)
- "What's our ISO 27001 readiness?" → Interactive Assessment (ISO 27001 framework)

### CTO
- "Review our platform security architecture" → Advisory Analysis
- "Should we build or buy a SIEM?" → Advisory Analysis
- "Evaluate our DevSecOps maturity" → Interactive Assessment
- "Review our cloud architecture for security" → Advisory Analysis

### Security Architect
- "Create a threat model for our payment system" → Document Generation (threat-model template)
- "Design a zero-trust architecture" → Advisory Analysis + Framework Reference
- "Review our network segmentation" → Advisory Analysis
- "Create a security reference architecture" → Advisory Analysis + cloud-diagram

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Role not detected | Ask the user directly: "What's your role or perspective?" |
| Framework not available | Use the closest available framework and note limitations |
| User wants visual output | Reference the cloud-diagram skill for architecture diagrams |
| Assessment too broad | Narrow scope to a specific domain or control family first |
| Need more roles/frameworks | Upgrade to [CyberSorted Skills Pro](https://github.com/cyber-sorted/skills-pro) |
