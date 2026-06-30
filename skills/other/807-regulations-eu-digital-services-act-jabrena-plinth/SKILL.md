---
name: 807-regulations-eu-digital-services-act
description: Use when reviewing, designing, or modifying Java enterprise systems that may support intermediary services, hosting services, online platforms, marketplaces, content moderation, recommender systems, advertising delivery, complaint workflows, transparency reporting, or systemic-risk evidence under the EU Digital Services Act. This should trigger for requests such as Review a Java online platform for DSA controls; Design notice-and-action or appeal workflows; Add recommender, ad transparency, moderation, audit, researcher access, or privacy-safe observability evidence; Assess online-platform transparency controls before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# EU Digital Services Act Regulation for Java Online Platform Engineering

Use this Skill to review Java enterprise applications, online platforms, marketplaces, hosting services, content moderation tools, recommender systems, advertising systems, complaint workflows, transparency reporting pipelines, operational dashboards, or audit evidence that may require Digital Services Act-aware engineering controls.

Apply this Skill to determine what engineering controls, operational evidence, and escalation paths are needed before a Java system is released, connected to production traffic, used for online platform operations, or relied on for content moderation, recommender, advertising, complaint, or systemic-risk workflows.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, trust-and-safety teams, and reviewers identify when Digital Services Act concerns may apply and how to translate online platform expectations into enterprise architecture controls such as content decision audit logs, moderation workflow state, notice intake and response tracking, recommender and ranking explanation evidence, advertising transparency metadata, user controls, complaint and appeal workflows, risk assessment evidence, incident escalation, data access for auditors or researchers where applicable, and privacy-safe observability.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, or a final regulatory determination.

The main question is:

> When does a Java enterprise system require Digital Services Act-aware online platform controls, and what should developers build differently?

External reference: [Regulation (EU) 2022/2065 Digital Services Act](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).

Digital Services Act chapters summary reference: [Digital Services Act chapters summary](references/807-regulations-eu-digital-services-act-chapters-summary.md).

Java engineering examples reference: [Digital Services Act engineering examples](references/807-regulations-eu-digital-services-act-engineering-examples.md).

Report template asset: [Digital Services Act engineering review report template](assets/reports/807-eu-digital-services-act-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems that may provide intermediary services, hosting services, online platforms, online marketplaces, or online interfaces where users, traders, or third parties provide content, products, services, or information
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java services with notice-and-action, content moderation, statement-of-reasons, trusted flagger, complaint, appeal, or out-of-court dispute evidence requirements
- Search, ranking, recommendation, feed, catalog ordering, personalization, advertising, ad repository, trader traceability, transparency reporting, user controls, and minor-protection workflows
- Very large online platform or very large online search engine evidence where applicable, including systemic risk assessment, mitigation, crisis response, independent audit, compliance function, data access, vetted researcher access, and transparency reporting
- Privacy-safe observability, incident escalation, moderation audit logging, user notification, workflow state, data access control, retention, and evidence reconstruction for platform governance

## Digital Services Act Engineering Review

Treat intermediary classification, hosting or online-platform classification, very-large-online-platform or very-large-online-search-engine scope, illegal-content policy, advertising or recommender interpretation, audit or researcher access duties, systemic-risk conclusions, and regulatory interpretation as governance decisions for legal, compliance, trust-and-safety, privacy, security, product, risk, and executive accountability owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which user, trader, platform, marketplace, hosting, recommendation, advertising, complaint, or moderation workflows are in scope
- Which content or product decisions are made, why they are made, which policy or order drove them, who can appeal them, and how decisions are audited
- Which notices, orders, complaints, appeals, trusted flagger reports, and out-of-court dispute outcomes can be tracked end to end
- Which recommender, ranking, advertising, user-control, minor-protection, trader-traceability, and transparency-reporting evidence exists
- Which risk assessment, mitigation, audit, data access, researcher access, incident escalation, and privacy-safe observability evidence is available where VLOP or VLOSE concerns may apply

## Constraints

Translate Digital Services Act concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by legal, compliance, trust-and-safety, privacy, security, product, risk, audit, research-access, or executive accountability owners.

- **NOT LEGAL ADVICE**: Frame findings as online platform engineering controls and escalation points; recommend qualified review for intermediary classification, platform classification, VLOP or VLOSE status, illegal-content determinations, advertising or recommender interpretation, audit or researcher access duties, systemic-risk conclusions, and regulatory interpretation
- **SCOPE FIRST**: Identify whether the Java system supports an intermediary service, hosting service, online platform, online marketplace, online search engine, recommender system, advertising workflow, or VLOP/VLOSE evidence flow before recommending controls
- **MODERATION EVIDENCE**: Require traceable content decision audit logs, statement-of-reasons data, moderation workflow state, affected user notification, policy references, authority order references, and appeal eligibility where applicable
- **NOTICE AND RESPONSE TRACKING**: Verify notice intake, validation, deduplication, triage, action, response, redress, trusted flagger handling, and misuse protections are auditable end to end
- **TRANSPARENCY CONTROLS**: Review transparency reporting, recommender and ranking explanation evidence, ad transparency metadata, user-facing controls, trader traceability, and online interface design evidence
- **USER REDRESS**: Verify complaint, appeal, out-of-court dispute, reinstatement, and support workflows preserve state, deadlines, reasons, evidence, and owner handoffs
- **SYSTEMIC RISK WHERE APPLICABLE**: For potential VLOP or VLOSE scope, require risk assessment, mitigation, crisis response, independent audit, compliance function, data access, vetted researcher access, and transparency evidence
- **PRIVACY-SAFE OBSERVABILITY**: Preserve platform governance evidence without exposing secrets, credentials, personal data, illegal-content details, sensitive user reports, researcher data, or moderation training data unnecessarily
- **RELATIONSHIP TO OTHER RULES**: Use GDPR, AI Act, DORA, NIS2, Data Act, or sector guidance together with this Skill when the same system crosses privacy, AI, cybersecurity, resilience, data access, or platform governance boundaries

## When to use this skill

- Review a Java online platform for Digital Services Act controls
- Design notice-and-action, content moderation, complaint, appeal, or transparency reporting workflows
- Add recommender explanation, ranking controls, advertising transparency metadata, trader traceability, or user controls
- Assess VLOP, VLOSE, audit, researcher access, systemic risk, or crisis-response evidence before production release
- Check whether Java platform logs, metrics, traces, and dashboards preserve DSA evidence without exposing sensitive data

## Workflow

1. **Read regulation summary, engineering examples, and report template**

Read `references/807-regulations-eu-digital-services-act-chapters-summary.md`, `references/807-regulations-eu-digital-services-act-engineering-examples.md`, and `assets/reports/807-eu-digital-services-act-engineering-review-report-template.md` in that order. Use the chapters summary for Digital Services Act chapter, article, scope, liability, due diligence, transparency, online platform, marketplace, VLOP/VLOSE, supervision, enforcement, and owner-handoff context. Use the engineering examples for Java control patterns such as content decision audit logs, moderation workflow state, notice intake and response tracking, recommender and ranking explanation evidence, ad transparency metadata, user controls, complaint and appeal workflows, risk assessment evidence, incident escalation, data access for auditors or researchers where applicable, and privacy-safe observability. Do not start implementation review until the chapters summary, examples reference, and report template are understood.

2. **Classify the platform scope**

Identify service context, possible intermediary-service signals, hosting signals, online-platform or marketplace signals, online search or recommender signals, advertising workflows, trader interactions, user-generated content, terms and policy owners, content moderation decisions, user-redress paths, active-recipient evidence, VLOP/VLOSE indicators, deployment geography, data stores, observability systems, and governance owners. Escalate unclear intermediary or platform classification, VLOP/VLOSE status, illegal-content interpretation, advertising or recommender interpretation, audit or researcher access duties, systemic-risk conclusions, and regulatory interpretation to legal, compliance, trust-and-safety, privacy, security, product, risk, audit, research-access, or executive accountability owners.

3. **Review implementation and platform evidence**

Review Java code, configuration, controllers, DTOs, moderation services, policy engines, workflow state machines, persistence models, message schemas, search or ranking code, recommender configuration, ad delivery metadata, user-control settings, complaint and appeal records, transparency reporting jobs, logs, metrics, traces, audit exports, runbooks, tests, deployment workflows, and provider documentation. Check for gaps between claimed DSA controls and reviewable evidence.

4. **Recommend engineering controls**

Map Digital Services Act concerns to engineering actions: scope inventory, content decision audit logs, notice-and-action tracking, statement-of-reasons records, moderation workflow state, trusted flagger routing, misuse protections, complaint and appeal workflows, recommender explanation evidence, ranking controls, user controls, ad transparency metadata, trader traceability, transparency reporting, minor-protection controls, privacy-safe observability, incident escalation, and VLOP/VLOSE risk, audit, and researcher-access evidence where applicable.

5. **Generate review report and owner handoffs**

Use `assets/reports/807-eu-digital-services-act-engineering-review-report-template.md` to produce a concise engineering review with scope, evidence reviewed, Digital Services Act risk signals, potential violation or non-compliance signals, engineering gaps, recommended controls, owner handoffs, residual risks, release decision, and validation steps. State explicitly that intermediary classification, platform classification, VLOP/VLOSE status, illegal-content determinations, advertising or recommender interpretation, audit or researcher access duties, systemic-risk conclusions, and regulatory interpretation require qualified owner review.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/807-regulations-eu-digital-services-act-chapters-summary.md](references/807-regulations-eu-digital-services-act-chapters-summary.md)
- [references/807-regulations-eu-digital-services-act-engineering-examples.md](references/807-regulations-eu-digital-services-act-engineering-examples.md)
