---
name: 804-regulations-eu-nis2
description: Use when reviewing, designing, or modifying Java enterprise systems that may support essential or important entities, critical-sector services, managed service providers, supply-chain dependencies, or cybersecurity incident escalation obligations under NIS2. This should trigger for requests such as Review a Java platform for NIS2 cybersecurity controls; Design operational evidence for critical-sector services; Add incident detection, escalation, continuity, or supply-chain security controls; Assess cybersecurity risk management before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# NIS2 Regulation for Java Enterprise Cybersecurity Risk Management

Use this Skill to review Java enterprise applications, platforms, integrations, operational workflows, CI/CD pipelines, managed-service-provider tooling, or critical-sector services that may require NIS2-aware cybersecurity risk-management controls.

Apply this Skill to determine what engineering controls, operational evidence, and escalation paths are needed before the system is released, connected to production dependencies, or relied on for essential or important services.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, and reviewers identify when NIS2 concerns may apply and how to translate cybersecurity risk-management expectations into enterprise architecture controls such as asset and service inventories, dependency mapping, secure configuration, vulnerability handling, logging and monitoring, incident detection and escalation, backup and recovery, business continuity, supply-chain security, access control, cryptography, secure development, and change control.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, or a final regulatory determination.

The main question is:

> When does a Java enterprise system require NIS2-aware cybersecurity controls, and what should developers build differently?

External reference: [NIS2 Directive (EU) 2022/2555](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022L2555).

NIS2 directive chapters summary reference: [NIS2 directive chapters summary](references/804-regulations-eu-nis2-chapters-summary.md).

Java engineering examples reference: [NIS2 engineering examples](references/804-regulations-eu-nis2-engineering-examples.md).

Report template asset: [NIS2 engineering review report template](assets/reports/804-nis2-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems supporting essential or important entities, critical-sector services, managed service providers, cloud or platform services, operational technology integrations, public-sector services, health, energy, transport, banking, financial-market infrastructure, digital infrastructure, or ICT service management
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java services with cybersecurity risk-management, continuity, incident-readiness, or supply-chain security requirements
- Systems with critical APIs, databases, message brokers, schedulers, batch jobs, IAM, secrets, observability, deployment pipelines, infrastructure dependencies, or external service providers
- Incident detection, severity triage, escalation, evidence capture, backup and recovery, continuity, change control, secure configuration, vulnerability management, and operational assurance workflows
- Dependency and provider reviews involving libraries, containers, CI/CD actions, SaaS platforms, managed databases, cloud services, observability providers, IAM providers, and external APIs

## NIS2 Engineering Review

Treat entity classification, member-state applicability, incident-reporting obligations, and regulatory interpretation as governance decisions for legal, compliance, security, risk, resilience, business-continuity, and executive accountability owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which essential or important service depends on the Java system
- Which assets, data stores, APIs, jobs, queues, credentials, providers, and deployment environments are in scope
- Which cybersecurity risks, vulnerabilities, misconfigurations, and dependency exposures are identified and tracked
- Which incidents can be detected, triaged, escalated, contained, reconstructed, and handed off
- Which backup, recovery, continuity, rollback, and change-control evidence exists
- Which supply-chain and provider risks are documented, monitored, and assigned to owners

## Constraints

Translate NIS2 concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by legal, compliance, security, risk, resilience, business-continuity, procurement, or executive accountability owners.

- **NOT LEGAL ADVICE**: Frame findings as cybersecurity engineering controls and escalation points; recommend qualified review for entity classification, member-state applicability, reporting obligations, and regulatory interpretation
- **SCOPE FIRST**: Identify whether the system supports an essential entity, important entity, critical-sector service, managed service provider, or supply-chain dependency before recommending controls
- **ASSET AND SERVICE INVENTORY**: Require traceable inventories for applications, APIs, jobs, data stores, queues, credentials, providers, deployment environments, network paths, and operational owners
- **CYBERSECURITY RISK MANAGEMENT**: Review secure configuration, vulnerability handling, dependency management, hardening, patch evidence, risk acceptance, and exception ownership
- **INCIDENT READINESS**: Verify detection, logging, monitoring, severity classification, escalation, containment, evidence capture, handoff, post-incident review, and corrective action paths
- **CONTINUITY CONTROLS**: Review backup, restore, continuity, failover, rollback, capacity, recovery targets, runbooks, and tested recovery evidence
- **SUPPLY-CHAIN SECURITY**: Do not treat libraries, build plugins, containers, CI/CD actions, SaaS tools, cloud services, managed databases, IAM, or observability providers as invisible dependencies
- **ACCESS AND CRYPTOGRAPHY**: Verify least privilege, MFA signals, secrets management, credential rotation, secure transport, encryption, key ownership, and privileged operation auditability
- **CHANGE CONTROL**: Treat releases, configuration changes, schema migrations, IAM changes, dependency upgrades, provider changes, and emergency fixes as cybersecurity risk events requiring traceable review

## When to use this skill

- Review a Java platform for NIS2 cybersecurity controls
- Design operational evidence for critical-sector or important services
- Add incident detection, escalation, backup, recovery, continuity, or supply-chain security controls
- Assess cybersecurity risk management before production release
- Check whether Java service dependencies, CI/CD workflows, or provider integrations have NIS2-aware evidence

## Workflow

1. **Read directive chapters summary, engineering examples, and report template**

Read `references/804-regulations-eu-nis2-chapters-summary.md`, `references/804-regulations-eu-nis2-engineering-examples.md`, and `assets/reports/804-nis2-engineering-review-report-template.md` in that order. Use the directive chapters summary for NIS2 chapter, article, annex, scope, reporting, supervision, enforcement, and owner-handoff context. Use the engineering examples for Java control patterns such as asset and service inventory, incident detection and escalation, vulnerability and dependency evidence, backup and continuity evidence, supply-chain risk, secure change control, and Java release-policy controls. Do not start implementation review until the directive chapters summary, examples reference, and report template are understood.

2. **Classify the cybersecurity scope**

Identify service context, possible essential or important entity signals, sector signals, system owner, security owner, resilience owner, deployment environments, assets, data stores, messaging systems, IAM, secrets, third-party providers, recovery expectations, and incident pathways. Escalate unclear applicability, entity classification, member-state implementation, reporting obligations, or regulatory interpretation to legal, compliance, security, risk, resilience, or executive accountability owners.

3. **Review implementation and operational evidence**

Review Java code, configuration, infrastructure descriptors, runbooks, monitoring, logging, tests, deployment workflows, dependency inventories, vulnerability records, incident procedures, backup and restore evidence, business-continuity records, and provider documentation. Check for gaps between claimed controls and reviewable evidence.

4. **Recommend engineering controls**

Map NIS2 concerns to engineering actions: asset and service inventory, secure configuration, dependency and vulnerability management, incident detection and escalation, evidence-safe logging, monitoring and alerting, backup and restore verification, continuity and rollback plans, supply-chain risk review, access control, cryptography, secure development, and change approval.

5. **Generate review report and owner handoffs**

Use `assets/reports/804-nis2-engineering-review-report-template.md` to produce a concise engineering review with scope, evidence reviewed, NIS2 risk signals, potential violation or non-compliance signals, engineering gaps, recommended controls, owner handoffs, residual risks, release decision, and validation steps. State explicitly that legal applicability, entity classification, reporting duties, and regulatory interpretation require qualified owner review.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/804-regulations-eu-nis2-chapters-summary.md](references/804-regulations-eu-nis2-chapters-summary.md)
- [references/804-regulations-eu-nis2-engineering-examples.md](references/804-regulations-eu-nis2-engineering-examples.md)
