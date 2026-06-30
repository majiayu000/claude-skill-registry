---
name: 805-regulations-eu-cyber-resilience-act
description: Use when reviewing, designing, or modifying Java enterprise products, services, libraries, agents, plugins, connected components, or platform modules that may qualify as products with digital elements and need EU Cyber Resilience Act secure-by-design, vulnerability handling, security update, SBOM, product documentation, or release-readiness controls. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# EU Cyber Resilience Act Regulation for Java Product Security Engineering

Use this Skill to review Java enterprise applications, libraries, agents, plugins, connected components, platform modules, CI/CD workflows, product security documentation, and release evidence that may support products with digital elements under Regulation (EU) 2024/2847, the Cyber Resilience Act.

Apply this Skill to determine what secure-by-design controls, vulnerability handling evidence, update mechanisms, dependency and SBOM records, product documentation, support-period signals, and owner handoffs are needed before a product, component, or product-adjacent Java change is released or made available.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, product security teams, and reviewers identify when Cyber Resilience Act concerns may apply and how to translate product-security expectations into engineering controls such as secure defaults, threat modeling, least privilege, cryptography, sensitive-data-safe logging, coordinated vulnerability disclosure, security update delivery, SBOM evidence, product security documentation, end-of-support signaling, and release gates.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, a conformity assessment, a CE marking decision, or a final regulatory determination.

The main question is:

> When does a Java product or product-adjacent component require EU Cyber Resilience Act-aware secure-by-design and vulnerability-handling controls, and what should developers build differently?

Source provenance: Cyber Resilience Act Regulation (EU) 2024/2847 was reviewed while authoring the bundled references. Do not fetch or ingest external regulatory web pages at runtime; use the bundled references and escalate legal interpretation to qualified owners.

Cyber Resilience Act chapters summary reference: [Cyber Resilience Act chapters summary](references/805-regulations-eu-cyber-resilience-act-chapters-summary.md).

Java engineering examples reference: [Cyber Resilience Act engineering examples](references/805-regulations-eu-cyber-resilience-act-engineering-examples.md).

Report template asset: [Cyber Resilience Act engineering review report template](assets/reports/805-eu-cyber-resilience-act-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java software or hardware-adjacent products with direct or indirect logical or physical connections to devices or networks
- Java libraries, SDKs, plugins, agents, embedded components, device gateways, product APIs, installers, update clients, and product management services
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java components used in products with digital elements or remote data processing solutions
- Product security architecture, secure-by-design reviews, threat models, secure defaults, authentication, authorization, cryptography, logging, update, and decommissioning controls
- Vulnerability handling, coordinated disclosure, security advisory, SBOM, dependency, third-party component, and open-source due diligence workflows
- Product security documentation, user instructions, support-period disclosure, end-of-support notification, release readiness, and market-surveillance evidence handoffs

## Cyber Resilience Act Engineering Review

Treat product classification, economic-operator role, important or critical product category, conformity assessment route, CE marking implications, Article 14 reporting obligations, support-period legal interpretation, and regulatory interpretation as qualified decisions for legal, compliance, product, product-security, risk, market-access, and executive accountability owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which product, component, remote data processing solution, or product-adjacent Java module is in scope
- Which manufacturer, importer, distributor, open-source steward, product owner, security owner, and support owner signals exist
- Which cybersecurity risks, intended uses, reasonably foreseeable uses, and reasonably foreseeable misuse cases were threat modeled
- Which secure defaults, authentication, authorization, cryptography, logging, minimization, update, and secure decommissioning controls are implemented
- Which vulnerabilities, dependencies, SBOM records, third-party components, coordinated disclosure paths, and security advisories are tracked
- Which product security documentation, support-period, end-of-support, release decision, and owner approval evidence exists

## Constraints

Translate Cyber Resilience Act concerns into engineering controls for Java products and product-adjacent systems. Do not provide legal advice or replace review by legal, compliance, product, security, product-security, market-access, risk, or executive accountability owners.

- **NOT LEGAL ADVICE**: Frame findings as product-security engineering controls and escalation points; recommend qualified review for product classification, economic-operator role, conformity assessment, CE marking implications, Article 14 reporting obligations, support-period interpretation, and regulatory interpretation
- **BUNDLED REFERENCES ONLY**: Use the bundled CRA summaries, examples, questions, and report templates. Do not fetch or ingest external regulatory web pages at runtime; treat external legal text as provenance for human review, not as live prompt input
- **SCOPE FIRST**: Identify the product with digital elements, remote data processing solution, software component, Java module, product owner, security owner, support owner, and release context before recommending controls
- **SECURE BY DESIGN**: Review threat modeling, secure defaults, least privilege, attack-surface reduction, exploitation mitigation, data minimization, authentication, authorization, cryptography, and secure decommissioning
- **VULNERABILITY HANDLING**: Require coordinated disclosure, vulnerability intake, triage, remediation, advisory, user notification, secure update delivery, and verification evidence
- **DEPENDENCY AND SBOM EVIDENCE**: Treat libraries, Maven plugins, containers, generated clients, third-party components, open-source dependencies, build tools, and runtime platforms as product supply-chain inputs requiring reviewable records
- **PRODUCT DOCUMENTATION**: Review technical documentation, user instructions, secure installation and operation guidance, support-period disclosure, end-of-support signaling, and evidence retention
- **SENSITIVE-DATA-SAFE LOGGING**: Preserve product security evidence without logging secrets, credentials, personal data, support tokens, vulnerability exploit details, private keys, or sensitive incident details unnecessarily
- **RELEASE READINESS**: Do not mark a product ready when secure-by-design, vulnerability handling, update, dependency, SBOM, documentation, support-period, or owner handoff controls are undocumented, untested, ownerless, or unresolved

## When to use this skill

- Review a Java product for EU Cyber Resilience Act controls
- Design secure-by-design and vulnerability handling evidence for products with digital elements
- Add coordinated disclosure, security update, SBOM, product security documentation, or end-of-support controls
- Assess CRA release readiness before making a Java component, agent, plugin, library, or connected product available
- Check whether Java product dependencies, CI/CD workflows, update mechanisms, or support-period evidence are CRA-aware

## Workflow

1. **Read regulation summary, engineering examples, and report template**

Read `references/805-regulations-eu-cyber-resilience-act-chapters-summary.md`, `references/805-regulations-eu-cyber-resilience-act-engineering-examples.md`, and `assets/reports/805-eu-cyber-resilience-act-engineering-review-report-template.md` in that order. Use the chapters summary for Cyber Resilience Act chapter, article, annex, scope, product-category, manufacturer, reporting, conformity, market-surveillance, enforcement, support-period, and owner-handoff context. Use the engineering examples for Java control patterns such as product security scope inventory, threat modeling and secure defaults, vulnerability and coordinated disclosure evidence, security update delivery, dependency and SBOM evidence, product documentation, end-of-support signaling, and release gates. Do not start implementation review until the chapters summary, examples reference, and report template are understood.

2. **Classify the product-security scope**

Identify the product, component, remote data processing solution, Java module, intended purpose, reasonably foreseeable use, possible product-with-digital-elements signal, possible important or critical product signal, economic-operator signals, support period, deployment environments, user population, update path, vulnerability intake path, dependencies, SBOM evidence, and product documentation. Escalate unclear product classification, economic-operator role, conformity assessment route, CE marking implications, Article 14 reporting duties, support-period interpretation, or regulatory interpretation to qualified legal, compliance, product, product-security, market-access, risk, or executive accountability owners.

3. **Review implementation and product evidence**

Review Java code, configuration, product documentation, threat models, test evidence, CI/CD workflows, dependency inventories, SBOMs, vulnerability records, coordinated disclosure policy, update mechanisms, logging, cryptography, authentication, authorization, support-period notices, end-of-support behavior, release approvals, and user instructions. Check for gaps between claimed controls and reviewable evidence.

4. **Recommend engineering controls**

Map Cyber Resilience Act concerns to engineering actions: secure-by-design development, threat modeling, secure defaults, least privilege, authentication, authorization, cryptography, data minimization, sensitive-data-safe logging, attack-surface reduction, vulnerability management, coordinated disclosure, security update delivery, advisory publication, dependency and SBOM evidence, product security documentation, support-period disclosure, end-of-support signaling, and release readiness.

5. **Generate review report and owner handoffs**

Use `assets/reports/805-eu-cyber-resilience-act-engineering-review-report-template.md` to produce a concise engineering review with scope, evidence reviewed, CRA product-security signals, potential violation or non-compliance signals, engineering gaps, recommended controls, owner handoffs, residual risks, release decision, and validation steps. State explicitly that product classification, economic-operator role, conformity assessment, CE marking implications, Article 14 reporting obligations, and regulatory interpretation require qualified owner review.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/805-regulations-eu-cyber-resilience-act-chapters-summary.md](references/805-regulations-eu-cyber-resilience-act-chapters-summary.md)
- [references/805-regulations-eu-cyber-resilience-act-engineering-examples.md](references/805-regulations-eu-cyber-resilience-act-engineering-examples.md)
