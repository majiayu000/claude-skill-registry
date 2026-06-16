---
name: 803-regulations-gdpr
description: Use when reviewing, designing, or modifying Java enterprise systems that process personal data and need GDPR-aware engineering controls. This should trigger for requests such as Review a Java service for GDPR privacy controls; Design data-subject rights workflows; Add retention, deletion, pseudonymization, or privacy-safe logging; Assess data transfer, DPIA, breach evidence, or processor/controller boundary concerns before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# GDPR Regulation for Java Enterprise Personal Data Protection

Use this Skill to review Java enterprise applications, APIs, data pipelines, integrations, batch jobs, AI workflows, or operational tooling that collect, store, transform, expose, log, export, or delete personal data.

Apply this Skill to determine what engineering controls, evidence, and escalation paths are needed before the system is released, connected to production data, or used for personal-data processing.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, and reviewers identify when GDPR concerns may apply and how to translate data protection expectations into enterprise architecture controls such as personal-data inventories, minimization, purpose limitation, privacy by design, security of processing, data-subject rights workflows, retention and deletion, pseudonymization, transfer-review evidence, breach-response evidence, and privacy-safe logging.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, or a final regulatory determination.

The main question is:

> When does a Java enterprise system require GDPR-aware personal-data controls, and what should developers build differently?

External reference: [GDPR Regulation (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679).

GDPR chapters summary reference: [GDPR chapters summary](references/803-regulations-gdpr-chapters-summary.md).

Java engineering examples reference: [GDPR engineering examples](references/803-regulations-gdpr-engineering-examples.md).

Questionnaire asset: [GDPR engineering review questionnaire](assets/questions/803-gdpr-engineering-review-questionnaire.md).

Report template asset: [GDPR engineering review report template](assets/reports/803-gdpr-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems that process personal data, user profiles, account data, identifiers, contact data, behavioral data, telemetry tied to users, or sensitive categories of data
- REST APIs, message consumers, batch jobs, data exports, reporting, search indexes, logs, caches, backups, and analytics pipelines containing personal data
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java services with privacy and data protection requirements
- Systems requiring data-subject rights workflows such as access, rectification, erasure, restriction, objection, portability, or consent preference handling
- Cross-border data transfers, processor/controller boundaries, subprocessor integrations, third-party SaaS providers, or vendor APIs
- DPIA escalation, privacy by design review, breach-response evidence, data retention, deletion, pseudonymization, anonymization, and privacy-safe observability

## GDPR Engineering Review

Treat lawful basis, controller or processor role, jurisdiction, transfer mechanism, special-category processing, DPIA requirements, and regulatory interpretation as governance decisions for legal, privacy, data protection officer, compliance, security, and risk owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which personal data is processed and where it flows
- Why each field is needed and how long it is retained
- Which users, systems, vendors, logs, backups, and exports can access it
- How rights requests are located, fulfilled, audited, and propagated
- How deletion and retention rules affect primary stores, derived stores, caches, indexes, logs, and backups
- How breach detection, containment, evidence, and notification handoff are supported

## Constraints

Translate GDPR concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by legal, privacy, data protection officer, compliance, security, or risk owners.

- **NOT LEGAL ADVICE**: Frame findings as privacy engineering controls and escalation points; recommend qualified review for lawful basis, controller or processor role, jurisdiction, transfer mechanism, DPIA, and regulatory interpretation
- **PERSONAL DATA INVENTORY**: Identify personal data categories, sources, purposes, owners, processors, stores, logs, caches, indexes, exports, backups, and retention periods before recommending controls
- **DATA MINIMIZATION**: Do not collect, persist, log, expose, replicate, or retain personal data without a documented engineering need and governance owner
- **PRIVACY BY DESIGN**: Prefer narrow DTOs, field-level authorization, purpose-specific processing, secure defaults, deletion paths, and testable privacy controls
- **DATA-SUBJECT RIGHTS**: Verify access, rectification, erasure, restriction, objection, portability, and preference workflows where applicable, including propagation to derived stores
- **RETENTION AND DELETION**: Define retention policies, deletion jobs, tombstones, audit evidence, backup handling, cache invalidation, search-index removal, and downstream notifications
- **SECURITY OF PROCESSING**: Review encryption, access control, audit logs, secrets, secure transport, data masking, pseudonymization, least privilege, and incident detection
- **PRIVACY-SAFE LOGGING**: Avoid secrets, credentials, identifiers, special-category data, free-text personal data, and excessive payload logging; use identifiers, hashes, redaction, and retention controls where appropriate
- **SECRET REDACTION**: Do not record or repeat passwords, API keys, tokens, session IDs, private keys, connection strings, credentials, or secret values from questionnaire answers, code, logs, screenshots, or evidence; replace them with `[REDACTED_SECRET]` and describe only the secret type and storage/control gap

## When to use this skill

- Review a Java service for GDPR privacy controls
- Design data-subject rights workflows for a Java application
- Add retention, deletion, pseudonymization, or privacy-safe logging
- Assess data transfer, DPIA, breach evidence, or processor/controller boundary concerns before production release
- Check whether logs, caches, search indexes, exports, or backups contain personal data

## Workflow

1. **Read chapters summary, engineering examples, questionnaire, and report template**

Read `references/803-regulations-gdpr-chapters-summary.md`, `references/803-regulations-gdpr-engineering-examples.md`, `assets/questions/803-gdpr-engineering-review-questionnaire.md`, and `assets/reports/803-gdpr-engineering-review-report-template.md` in that order. Use the chapters summary for GDPR chapter, article, scope, principles, data-subject rights, controller and processor obligations, security, breach, DPIA, transfers, supervision, enforcement, and owner-handoff context. Use the engineering examples for Java control patterns such as personal-data inventory, DTO minimization, rights workflows, retention and deletion, transfer review, privacy-safe logging, and field-level privacy policy controls. Do not start implementation review until the chapters summary, examples reference, questionnaire rules, and report template are understood.

2. **Ask the questionnaire questions interactively**

Follow the IMPORTANT rules at the top of `assets/questions/803-gdpr-engineering-review-questionnaire.md`. Ask the human one question at a time from Question 1 through Question 22. Present only the current question with its options; wait for an answer before the next. Do NOT batch questions, preview upcoming questions, or answer from code, docs, or assumptions. Record answers accurately after redacting secrets, credentials, tokens, API keys, session IDs, private keys, and connection strings as `[REDACTED_SECRET]`. Probe "Unknown" responses. Do not proceed to implementation review or the report until all 22 questions are answered or explicitly deferred.

3. **Classify personal-data scope**

Using the questionnaire answers, identify personal-data categories, source systems, purposes, data subjects, stores, processors, controllers, vendors, logs, caches, search indexes, backups, exports, retention periods, data transfers, and privacy owners. Escalate unclear lawful basis, controller or processor role, special-category data, transfer mechanism, DPIA need, or jurisdictional interpretation to legal, privacy, data protection officer, compliance, security, or risk owners.

4. **Review implementation and privacy evidence**

Review Java code, DTOs, controllers, repositories, SQL or NoSQL schemas, migrations, message schemas, serialization, logs, metrics, traces, cache keys, search indexes, batch jobs, exports, IAM policies, retention jobs, deletion workflows, tests, and documentation. Check for gaps between questionnaire answers and evidence that can be reviewed.

5. **Recommend engineering controls**

Map GDPR concerns to engineering actions: data minimization, purpose-specific DTOs, field-level authorization, secure processing, privacy-safe logging, pseudonymization, retention and deletion jobs, data-subject rights workflows, transfer-review evidence, breach-response evidence, auditability, and owner escalation.

6. **Generate review report and prioritized actions**

Use `assets/reports/803-gdpr-engineering-review-report-template.md` to document the review context, personal-data processing summary, questionnaire findings, GDPR privacy risk classification, engineering controls, evidence inventory, residual risks, release decision, and prioritized action plan with owners and due dates. Do not include raw secret values in the report; include only redacted references such as `[REDACTED_SECRET]`, the secret type, affected component, and required remediation owner.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/803-regulations-gdpr-chapters-summary.md](references/803-regulations-gdpr-chapters-summary.md)
- [references/803-regulations-gdpr-engineering-examples.md](references/803-regulations-gdpr-engineering-examples.md)
