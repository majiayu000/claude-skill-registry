---
name: 808-regulations-eu-digital-markets-act
description: Use when reviewing, designing, or modifying Java enterprise systems that may support EU Digital Markets Act gatekeeper-platform concerns, core platform services, interoperability, business-user data access, consent-dependent data combination, ranking, self-preferencing, advertising transparency, or anti-circumvention controls. This should trigger for requests such as Review a Java platform for DMA controls; Design interoperability and business-user data access evidence; Add ranking, consent, preference, or anti-circumvention audit controls; Assess gatekeeper-platform engineering evidence before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# EU Digital Markets Act Regulation for Java Enterprise Gatekeeper Platform Controls

Use this Skill to review Java enterprise applications, platform APIs, marketplaces, app stores, advertising systems, ranking systems, identity services, browser or operating-system integrations, messaging interoperability, business-user portals, data access APIs, analytics pipelines, CI/CD workflows, or operational tooling that may support Digital Markets Act (DMA) gatekeeper-platform obligations.

Apply this Skill to determine what engineering controls, compliance evidence, and escalation paths are needed before a system is released, connected to production platform data, exposed to business users, or used to operate a core platform service.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, product teams, and reviewers identify when DMA concerns may apply and how to translate gatekeeper-platform expectations into enterprise architecture controls such as interoperability interfaces, business-user data access APIs, consent and preference evidence, ranking and self-preferencing audit signals, advertising transparency evidence, app-store or marketplace access controls, anti-circumvention guardrails, observability, change control, documentation, and compliance evidence handoff.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, a gatekeeper designation, a core platform service classification, or a final regulatory determination.

The main question is:

> When does a Java enterprise platform require DMA-aware gatekeeper controls, and what should developers build differently?

External reference: [Digital Markets Act Regulation (EU) 2022/1925](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R1925).

Digital Markets Act chapters summary reference: [DMA chapters summary](references/808-regulations-eu-digital-markets-act-chapters-summary.md).

Java engineering examples reference: [DMA engineering examples](references/808-regulations-eu-digital-markets-act-engineering-examples.md).

Report template asset: [DMA engineering review report template](assets/reports/808-eu-digital-markets-act-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems that may support a gatekeeper, core platform service, online intermediation service, app store, online search engine, social network, video-sharing platform, number-independent interpersonal communications service, operating system, web browser, virtual assistant, cloud computing service, or online advertising service
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java services with platform access, interoperability, ranking, self-preferencing, business-user data access, advertising transparency, or consent-dependent data-combination concerns
- APIs, message consumers, batch jobs, exports, reports, ranking pipelines, search indexes, recommendation services, marketplace catalogs, app-store workflows, identity services, payment-service integrations, browser or operating-system defaults, and compliance reporting workflows
- Systems requiring evidence for business-user export workflows, end-user portability, third-party interoperability, advertising metrics, ranking fairness, access terms, consent and preference capture, anti-circumvention controls, and compliance-owner handoff
- Platform changes involving database migrations, Kafka message contracts, feature flags, ranking experiments, access-policy changes, consent UI changes, telemetry schemas, business-user data exports, and production release gates

## Digital Markets Act Engineering Review

Treat gatekeeper designation, core platform service scope, obligation applicability, consent interpretation, self-preferencing assessments, fair and reasonable access terms, suspension or exemption requests, and regulatory interpretation as governance decisions for legal, compliance, platform governance, product, privacy, security, risk, competition, and executive accountability owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which core platform service, business-user journey, end-user journey, data store, API, event stream, ranking system, advertising system, interoperability interface, or platform policy may be in scope
- Which business users, end users, third-party providers, advertisers, publishers, developers, or competitors are affected by the Java system
- Which data access, export, portability, interoperability, consent, preference, ranking, self-preferencing, and anti-circumvention controls exist
- Which logs, metrics, traces, audit events, data lineage records, decision records, release approvals, and compliance reports support review
- Which gaps require owner handoff before production release or continued operation

## Constraints

Translate Digital Markets Act concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by legal, compliance, platform governance, product, privacy, security, risk, competition, or executive accountability owners.

- **NOT LEGAL ADVICE**: Frame findings as gatekeeper-platform engineering controls and escalation points; recommend qualified review for gatekeeper designation, core platform service scope, obligation applicability, consent interpretation, self-preferencing assessments, fair access terms, and regulatory interpretation
- **SCOPE FIRST**: Identify possible core platform service, business-user journey, end-user journey, platform owner, data owner, product owner, privacy owner, and compliance owner before recommending controls
- **INTEROPERABILITY INTERFACES**: Review technical interfaces, reference offers, security controls, compatibility tests, rate limits, access terms, request workflows, and evidence that interoperability is effective and not degraded
- **DATA ACCESS AND EXPORT**: Verify business-user and end-user data access APIs, export workflows, portability tools, advertiser and publisher transparency data, search data access, and consent-dependent personal-data sharing evidence
- **CONSENT AND PREFERENCES**: Preserve evidence for specific choice, opt-in, withdrawal, retry limits, neutral UI, preference history, purpose binding, and privacy-owner handoff where personal data is combined, cross-used, or shared
- **RANKING AND SELF-PREFERENCING**: Require audit signals for ranking inputs, experiments, business rules, indexing, crawling, sponsored placement, own-service treatment, fairness checks, and non-discriminatory access terms
- **ANTI-CIRCUMVENTION**: Do not accept designs that fragment services, degrade quality, hide choices, make rights hard to exercise, or use interface design, technical limits, contractual terms, or data flows to undermine Articles 5, 6, or 7 controls
- **ACCESS CONTROL AND OBSERVABILITY**: Verify least privilege, request authentication, authorization, tamper-evident audit logs, metrics, traces, dashboards, alerting, evidence retention, and safe handling of business secrets and personal data
- **CHANGE CONTROL**: Treat ranking changes, consent flows, data export schemas, interoperability APIs, access terms, advertising metrics, data lineage, platform defaults, and release gates as DMA evidence events requiring traceable review

## When to use this skill

- Review a Java platform for Digital Markets Act controls
- Design interoperability interfaces or business-user data access APIs for a core platform service
- Add consent, preference, ranking, self-preferencing, advertising transparency, or anti-circumvention audit controls
- Assess gatekeeper-platform evidence before production release
- Check whether marketplace, app-store, search, advertising, messaging, browser, operating-system, identity, or cloud-platform changes need DMA-aware owner handoff

## Workflow

1. **Read DMA chapters summary, engineering examples, and report template**

Read `references/808-regulations-eu-digital-markets-act-chapters-summary.md`, `references/808-regulations-eu-digital-markets-act-engineering-examples.md`, and `assets/reports/808-eu-digital-markets-act-engineering-review-report-template.md` in that order. Use the chapters summary for DMA chapter, article, scope, designation, obligations, interoperability, anti-circumvention, monitoring, enforcement, reporting, and owner-handoff context. Use the engineering examples for Java control patterns such as interoperability interfaces, business-user data access, consent and preference evidence, ranking audit signals, export workflows, anti-circumvention release gates, observability, and compliance evidence handoff. Do not start implementation review until the DMA chapters summary, examples reference, and report template are understood.

2. **Classify the platform scope**

Identify service context, possible core platform service signals, gatekeeper-scope signals, business-user and end-user journeys, platform owners, data owners, product owners, privacy owners, security owners, compliance owners, deployment environments, APIs, data stores, event streams, ranking systems, advertising systems, consent flows, access policies, interoperability interfaces, export workflows, and production release paths. Escalate gatekeeper designation, core platform service classification, obligation applicability, consent interpretation, self-preferencing assessment, fair access terms, suspension or exemption questions, and regulatory interpretation to qualified owners.

3. **Review implementation and compliance evidence**

Review Java code, configuration, APIs, DTOs, repositories, schemas, migrations, Kafka messages, ranking code, feature flags, experiments, consent and preference records, audit logs, metrics, traces, dashboards, alerts, export jobs, business-user portals, documentation, tests, release records, and compliance reports. Check for gaps between claimed controls and reviewable evidence.

4. **Recommend engineering controls**

Map DMA concerns to engineering actions: interoperability API contracts, reference-offer evidence, data access APIs, export workflows, consent and preference records, ranking and self-preferencing audit signals, advertising transparency metrics, business-user access terms, anti-circumvention guardrails, least privilege, observability, documentation, change approval, and compliance evidence handoff.

5. **Generate review report and owner handoffs**

Use `assets/reports/808-eu-digital-markets-act-engineering-review-report-template.md` to produce a concise engineering review with scope, evidence reviewed, DMA risk signals, potential violation or non-compliance signals, engineering gaps, recommended controls, owner handoffs, residual risks, release decision, and validation steps. State explicitly that gatekeeper designation, core platform service scope, obligation applicability, consent interpretation, self-preferencing assessments, fair access terms, and regulatory interpretation require qualified owner review.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/808-regulations-eu-digital-markets-act-chapters-summary.md](references/808-regulations-eu-digital-markets-act-chapters-summary.md)
- [references/808-regulations-eu-digital-markets-act-engineering-examples.md](references/808-regulations-eu-digital-markets-act-engineering-examples.md)
