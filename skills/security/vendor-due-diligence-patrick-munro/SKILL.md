---
name: vendor-due-diligence-patrick-munro
description: "Framework for assessing IT service providers, technology vendors, and third-party partners. Creates structured risk assessments across financial, operational, compliance, security, and reputational dimensions with regulatory checklists (GDPR, DORA, NIS2, SOX). Use when: (1) Evaluating new vendors or technology providers, (2) Conducting third-party risk assessments for procurement, (3) Performing critical vendor due diligence for regulatory compliance, (4) Creating vendor onboarding documentation, (5) Establishing ongoing vendor monitoring processes, (6) Assessing vendor concentration risk, or (7) Generating executive-level vendor risk reports."
metadata:
  author: Patrick Munro
  license: AGPL-3.0
  version: 2026.01.12
---

# Vendor Due Diligence Framework

## Overview
Comprehensive vendor assessment and due diligence framework for IT service providers, technology vendors, and third-party service providers. Creates structured risk assessments, evaluation reports, and ongoing monitoring frameworks across financial, operational, compliance, security, and reputational dimensions.

## LEGAL DISCLAIMER
**IMPORTANT: This skill provides general information and frameworks for vendor assessment purposes only. It does NOT constitute legal, financial, or professional advice. Users should:**
- Consult qualified legal counsel for specific legal requirements in their jurisdiction
- Engage appropriate financial and security professionals for detailed assessments
- Verify all regulatory requirements independently
- Adapt all frameworks to their specific organizational needs and risk tolerance
- Not rely on this skill as a substitute for professional due diligence services

**The frameworks provided are templates only. Actual vendor assessments require expertise in law, finance, cybersecurity, and risk management. Neither the skill creator nor Claude/Anthropic assumes any liability for decisions made based on this skill's output.**

## When to Use This Skill
Use this skill when you need to:
- Evaluate new vendors, technology providers, or service partners
- Conduct third-party risk assessments for procurement decisions
- Perform critical vendor due diligence for regulatory compliance (DORA, NIS2, GDPR, SOX, etc.)
- Create vendor onboarding documentation and assessment frameworks
- Establish ongoing vendor monitoring and review processes
- Assess vendor concentration risk and business continuity implications
- Generate executive-level vendor risk reports

## Core Capabilities

### 1. Three-Phase Assessment Process
**Phase 1: Initial Screening (Days 1-5)**
- Financial stability assessment (credit ratings, financial statements, market position)
- Basic compliance verification (certifications, licenses, regulatory status)
- Preliminary security posture review (ISO 27001, SOC 2, cyber insurance)
- Reputational check (news screening, litigation history, sanctions lists)
- Business continuity basics (disaster recovery, backup systems)

**Phase 2: Detailed Assessment (Days 5-15)**
- In-depth security evaluation (penetration testing, vulnerability management, incident response)
- Operational deep-dive (SLAs, performance metrics, capacity planning, change management)
- Compliance audit (GDPR, industry-specific regulations, data residency, cross-border transfers)
- Financial analysis (cash flow stability, debt ratios, insurance coverage, bonding capacity)
- Contractual risk review (liability caps, indemnification, IP ownership, termination rights)
- Subcontractor and fourth-party risk assessment

**Phase 3: Final Evaluation & Decision (Days 15-20)**
- Comprehensive risk scoring and rating (1-5 scale across all dimensions)
- Executive summary with recommendation (approve, approve with conditions, reject)
- Risk mitigation plan for identified gaps
- Onboarding roadmap with specific requirements
- Ongoing monitoring framework and KPIs

### 2. Multi-Factor Risk Scoring System
Each vendor receives scores (1=Low Risk to 5=Critical Risk) across:
- **Financial Risk**: Creditworthiness, revenue stability, insurance adequacy, concentration risk
- **Operational Risk**: Service delivery capability, business continuity, dependency/single points of failure
- **Compliance Risk**: Regulatory adherence, audit findings, data protection practices, certification status
- **Security Risk**: Cyber resilience, access controls, incident response, data encryption, vulnerability management
- **Reputational Risk**: Public perception, litigation history, ethical practices, ESG factors
- **Strategic Risk**: Service criticality, exit/transition difficulty, vendor lock-in, innovation capability

**Enhanced Feature**: Weighted risk calculations based on service criticality. Critical services (payment processing, customer data systems) receive 2x weight on security and compliance factors.

### 3. Regulatory Compliance Checklists
Pre-built assessment templates for:
- **GDPR**: Data processing agreements, sub-processor management, cross-border transfers, breach notification
- **DORA (Digital Operational Resilience Act)**: ICT third-party risk management, concentration risk, exit strategies
- **NIS2**: Supply chain security, incident reporting, security measures for essential/important entities
- **SOX**: Internal controls for financial reporting, audit trail requirements
- **PCI DSS**: Payment card data security (if applicable)
- **ISO 27001/SOC 2**: Information security management, control frameworks
- **Industry-specific**: HIPAA (healthcare), FINMA (financial services), FedRAMP (government)

**Enhanced Feature**: Regulatory gap analysis that identifies which requirements the vendor currently fails to meet and severity classification (blocker, major concern, minor gap, acceptable with mitigation).

### 4. Document Request Lists
Comprehensive documentation requirements organized by assessment phase:
- **Financial**: Audited financials (3 years), D&B reports, insurance certificates, bank references
- **Legal/Compliance**: Certifications (ISO, SOC 2), audit reports, privacy policies, DPAs, sub-processor lists
- **Security**: Penetration test results, vulnerability scan reports, incident response plans, disaster recovery documentation
- **Operational**: SLA templates, performance metrics, customer references, org charts, escalation procedures
- **Contractual**: Standard agreements, liability caps, indemnification terms, IP assignment provisions

### 5. Vendor Interview Frameworks
Structured interview guides for:
- **Executive Leadership**: Strategic vision, financial outlook, growth plans, M&A activity
- **Security/IT Teams**: Architecture reviews, access controls, encryption practices, patch management
- **Compliance Officers**: Regulatory adherence, audit processes, remediation tracking
- **Operations Managers**: Service delivery, incident management, change control, capacity planning
- **Legal/Contracts**: Negotiation flexibility, standard terms, liability frameworks

**Enhanced Feature**: Red flag detection prompts - specific questions designed to uncover hidden risks (e.g., "Describe your three most recent security incidents and response," "What percentage of revenue comes from your top 3 clients?")

### 6. Ongoing Monitoring Frameworks
Post-onboarding continuous oversight:
- **Quarterly Reviews**: Performance metrics, security updates, compliance status, financial health
- **Annual Assessments**: Full re-evaluation of risk scores, certification renewals, contract renegotiation
- **Event-Triggered Reviews**: M&A activity, security breaches, regulatory violations, leadership changes, service disruptions
- **KPI Dashboards**: Uptime, response times, security metrics, compliance status, financial indicators

**Enhanced Feature**: Early warning indicators (EWIs) that trigger immediate re-assessment - bankruptcy filings, mass layoffs, major customer losses, data breaches, audit failures, regulatory fines.

## Output Formats

### Vendor Risk Report
Comprehensive assessment report including:
- Executive summary with risk rating and recommendation
- Detailed findings by risk category with evidence
- Risk score matrix (visual heat map)
- Gap analysis against regulatory requirements
- Mitigation recommendations with priority levels
- Onboarding requirements and conditions
- Monitoring and review schedule

### Vendor Comparison Matrix
Side-by-side evaluation of multiple vendors:
- Risk scores across all dimensions
- Compliance coverage comparison
- Cost-benefit analysis
- Strengths/weaknesses summary
- Recommended vendor with justification

### Onboarding Checklist
Structured requirements list:
- Pre-contract deliverables (certifications, insurance, references)
- Contract negotiation priorities (liability, SLAs, termination rights)
- Integration requirements (APIs, data formats, security controls)
- Ongoing obligations (reporting, audit rights, performance reviews)

**Enhanced Feature**: Risk-based onboarding paths - higher risk vendors face stricter requirements (more frequent reviews, additional certifications, enhanced SLAs, stronger termination rights).

## Best Practices

1. **Proportional Assessment**: Scale diligence depth to service criticality and risk exposure
   - Critical/High Risk: Full Phase 1-3 assessment with external expert validation
   - Medium Risk: Phase 1-2 with selective Phase 3 elements
   - Low Risk: Phase 1 with streamlined Phase 2

2. **Document Everything**: Maintain audit trail of assessment decisions, risk acceptances, and mitigation measures

3. **Involve Stakeholders**: Include Legal, IT/Security, Procurement, Business Units, and Compliance in assessment process

4. **Challenge Vendor Claims**: Verify certifications independently, request evidence, conduct site visits for critical vendors

5. **Plan for Exit**: Always assess vendor replaceability, data portability, and transition complexity before signing

6. **Continuous Monitoring**: Due diligence is not one-time - reassess regularly and after triggering events

7. **Concentrate Risk Management**: Track total vendor exposure across organization to identify dangerous concentration

**Enhanced Feature**: Third-party validation recommendations - when to engage external auditors, security firms, or legal counsel for independent verification (critical vendors, regulated services, high-value contracts).

## Risk Mitigation Strategies
Common approaches to address identified gaps:
- **Financial**: Require parent company guarantees, increase insurance requirements, shorten payment terms, implement performance bonds
- **Security**: Mandate specific controls, require penetration testing, implement enhanced monitoring, restrict data access
- **Compliance**: Require certification achievement within timeframe, implement audit rights, add regulatory breach termination clauses
- **Operational**: Define stricter SLAs, require redundancy, implement escrow for critical IP/code, establish backup vendor relationships
- **Strategic**: Limit contract term, build exit provisions, avoid proprietary lock-in, maintain dual-source options

## Limitations and Disclaimers

**This skill does NOT:**
- Replace professional due diligence services (legal, financial, technical audits)
- Provide legal advice on specific contracts or regulatory requirements
- Guarantee vendor performance or eliminate all risks
- Substitute for organization-specific risk frameworks and policies
- Fulfill regulatory obligations without expert validation
- Create attorney-client, fiduciary, or advisory relationships

**Users must:**
- Adapt all frameworks to their specific industry, jurisdiction, and risk tolerance
- Engage qualified professionals for regulated assessments
- Verify all regulatory requirements independently
- Obtain necessary internal approvals before vendor engagement
- Maintain documentation for audit and compliance purposes
- Update assessment criteria as regulations and threats evolve

## Regulatory Context
While this skill references common regulations (GDPR, DORA, NIS2, etc.), users must:
- Verify current regulatory requirements in their jurisdiction
- Consult legal counsel for compliance obligations
- Not rely on this skill for legal interpretation
- Understand that regulatory landscapes change constantly
- Recognize that enforcement varies by regulator and jurisdiction

**Last Updated Framework Version**: January 2025 (Regulatory references may become outdated)

## Example Use Cases

1. **Financial Institution under DORA**: Assessing cloud service provider for critical payment systems
2. **Healthcare Organization**: Evaluating SaaS vendor handling protected health information (HIPAA)
3. **Manufacturing Company**: Third-party risk assessment for industrial control system provider
4. **E-commerce Platform**: Payment processor due diligence under PCI DSS requirements
5. **Government Agency**: FedRAMP compliance assessment for cloud infrastructure provider
6. **Startup**: Rapid vendor screening for limited-risk, non-critical services

---

**FINAL REMINDER**: This is an educational framework and starting point only. Professional due diligence requires expertise in law, finance, cybersecurity, and risk management. Always engage qualified professionals for critical vendor assessments and do not rely solely on this skill for decision-making.
