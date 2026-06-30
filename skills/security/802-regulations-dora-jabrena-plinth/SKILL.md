---
name: 802-regulations-dora
description: Use when reviewing, designing, or modifying Java enterprise systems that may support financial entities, critical ICT services, third-party ICT provider integrations, or operational resilience obligations under DORA. This should trigger for requests such as Review a Java platform for DORA ICT risk controls; Design operational resilience evidence for a financial service; Add incident, continuity, backup, recovery, or third-party ICT controls; Assess resilience testing and monitoring before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# DORA Regulation for Java Enterprise Digital Operational Resilience

Use this Skill to review Java enterprise applications, platforms, integrations, or operational workflows that may support financial entities, critical ICT services, important business services, or outsourced ICT provider relationships.

Apply this Skill to determine what engineering controls, operational evidence, and escalation paths are needed before the system is released, connected to production dependencies, or relied on for regulated financial operations.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, and reviewers identify when DORA concerns may apply and how to translate operational resilience expectations into enterprise architecture controls such as ICT asset inventories, incident detection, monitoring, backup and recovery, continuity plans, change control, third-party risk evidence, resilience testing, and audit-ready operational records.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, or a final regulatory determination.

The main question is:

> When does a Java enterprise system require DORA-aware operational resilience controls, and what should developers build differently?

External reference: [DORA Regulation (EU) 2022/2554](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2554).

DORA chapters summary reference: [DORA chapters summary](references/802-regulations-dora-chapters-summary.md).

Java engineering examples reference: [DORA engineering examples](references/802-regulations-dora-engineering-examples.md).

Questionnaire asset: [DORA engineering review questionnaire](assets/questions/802-dora-engineering-review-questionnaire.md).

Report template asset: [DORA engineering review report template](assets/reports/802-dora-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems supporting financial entities, payment flows, trading, lending, insurance, investment, accounting, or regulated operations
- Platforms that provide ICT services to financial entities or important business services
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java services with operational resilience requirements
- Systems with critical databases, message brokers, job schedulers, batch workloads, APIs, IAM, secrets, observability, or infrastructure dependencies
- Third-party ICT provider integrations, cloud services, SaaS platforms, managed databases, messaging platforms, and external operational dependencies
- Incident detection, response, backup, recovery, continuity, change control, resilience testing, and operational evidence workflows

## DORA Engineering Review

Treat DORA applicability and interpretation as governance decisions for legal, compliance, security, risk, resilience, and business-continuity owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which business service depends on the Java system
- Which ICT assets, data stores, integrations, credentials, and providers are in scope
- Which incidents can be detected, triaged, reported, and reconstructed
- Which backups, recovery targets, continuity plans, and rollback paths exist
- Which third-party ICT risks are documented and monitored
- Which resilience tests prove controls work before production reliance

## Constraints

Translate DORA concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by legal, compliance, security, risk, resilience, business-continuity, or procurement owners.

- **NOT LEGAL ADVICE**: Frame findings as operational resilience controls and escalation points; recommend qualified review for applicability, entity classification, reporting obligations, outsourcing, and regulatory interpretation
- **SCOPE FIRST**: Identify whether the system supports a financial entity, important business service, critical ICT function, or third-party ICT provider relationship before recommending controls
- **ICT INVENTORY**: Require traceable inventories for applications, data stores, queues, jobs, dependencies, credentials, providers, deployment environments, and operational owners
- **INCIDENT READINESS**: Verify detection, triage, severity classification, escalation, evidence capture, customer or regulator handoff, and post-incident review paths
- **RESILIENCE CONTROLS**: Review backup, restore, continuity, failover, rollback, capacity, monitoring, alerting, logging, and change-control evidence
- **THIRD-PARTY ICT RISK**: Do not treat cloud, SaaS, managed database, messaging, observability, IAM, or payment providers as invisible dependencies; record contracts, controls, SLAs, exit paths, and monitoring evidence
- **TEST EVIDENCE**: Prefer tested recovery procedures, chaos or failover exercises, incident drills, and restore verification over untested runbooks
- **AUDITABILITY**: Preserve operational evidence for incidents, changes, approvals, provider outages, recovery tests, monitoring signals, and control exceptions
- **SECRET REDACTION**: Do not record or repeat passwords, API keys, tokens, session IDs, private keys, connection strings, credentials, or secret values from questionnaire answers, code, logs, screenshots, or evidence; replace them with `[REDACTED_SECRET]` and describe only the secret type and storage/control gap

## When to use this skill

- Review a Java platform for DORA ICT risk controls
- Design operational resilience evidence for a financial service
- Add incident, backup, recovery, continuity, or failover controls
- Assess third-party ICT provider risk before production release
- Check whether a Java service has audit-ready resilience testing and monitoring evidence

## Workflow

1. **Read chapters summary, engineering examples, questionnaire, and report template**

Read `references/802-regulations-dora-chapters-summary.md`, `references/802-regulations-dora-engineering-examples.md`, `assets/questions/802-dora-engineering-review-questionnaire.md`, and `assets/reports/802-dora-engineering-review-report-template.md` in that order. Use the chapters summary for DORA chapter, article, scope, ICT risk-management, incident reporting, resilience testing, third-party ICT risk, supervision, enforcement, and owner-handoff context. Use the engineering examples for Java control patterns such as ICT inventory, incident routing, recovery evidence, third-party ICT provider risk, resilience release gates, and Java release-policy controls. Do not start implementation review until the chapters summary, examples reference, questionnaire rules, and report template are understood.

2. **Ask the questionnaire questions interactively**

Follow the IMPORTANT rules at the top of `assets/questions/802-dora-engineering-review-questionnaire.md`. Ask the human one question at a time from Question 1 through Question 20. Present only the current question with its options; wait for an answer before the next. Do NOT batch questions, preview upcoming questions, or answer from code, docs, or assumptions. Record answers accurately after redacting secrets, credentials, tokens, API keys, session IDs, private keys, and connection strings as `[REDACTED_SECRET]`. Probe "Unknown" responses. Do not proceed to implementation review or the report until all 20 questions are answered or explicitly deferred.

3. **Classify the operational scope**

Using the questionnaire answers, identify the business service, financial or critical ICT context, system owner, operational owner, deployment environments, important dependencies, data stores, messaging systems, IAM, secrets, third-party providers, and resilience owners. Escalate unclear applicability, entity classification, reporting duties, or outsourcing interpretation to legal, compliance, security, risk, resilience, or procurement owners.

4. **Review implementation and operational evidence**

Review Java code, configuration, infrastructure descriptors, runbooks, monitoring, logging, tests, deployment workflows, dependency inventories, incident procedures, backup and restore evidence, business-continuity records, and third-party provider documentation. Check for gaps between questionnaire answers and evidence that can be reviewed.

5. **Recommend engineering controls**

Map DORA concerns to engineering actions: asset and dependency inventory, incident detection and escalation, evidence-safe logging, monitoring and alerting, backup and restore verification, continuity and rollback plans, resilience testing, change approval, provider monitoring, exit planning, and operational control owners.

6. **Generate review report and prioritized actions**

Use `assets/reports/802-dora-engineering-review-report-template.md` to document the review context, operational scope, questionnaire findings, DORA operational resilience classification, engineering controls, evidence inventory, residual risks, release decision, and prioritized action plan with owners and due dates. Do not include raw secret values in the report; include only redacted references such as `[REDACTED_SECRET]`, the secret type, affected component, and required remediation owner.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/802-regulations-dora-chapters-summary.md](references/802-regulations-dora-chapters-summary.md)
- [references/802-regulations-dora-engineering-examples.md](references/802-regulations-dora-engineering-examples.md)
