---
name: 806-regulations-eu-data-act
description: Use when reviewing, designing, or modifying Java enterprise systems that expose, exchange, store, process, export, or port data across users, businesses, connected products, cloud providers, APIs, event streams, AI data pipelines, data spaces, or SaaS platforms and need EU Data Act engineering controls. This should trigger for requests such as Review a Java platform for EU Data Act controls; Design data access and portability evidence; Add data-sharing request workflows, export formats, interoperability, metadata, audit logs, cloud-switching support, non-personal data safeguards, or trade-secret handoffs; Assess Data Act engineering readiness before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# EU Data Act Regulation for Java Enterprise Data Access and Portability Engineering

Use this Skill to review Java enterprise applications, SaaS platforms, APIs, data pipelines, connected-product integrations, event-driven systems, data spaces, and cloud services that may require EU Data Act-aware engineering controls.

Apply this Skill to determine what engineering controls, operational evidence, and owner handoffs are needed before a system exposes data access, data-sharing, export, portability, interoperability, cloud-switching, non-personal data, or data-processing-service workflows.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, data-governance teams, and reviewers identify where Data Act concerns may apply and how to translate those concerns into enterprise architecture controls such as data inventories, access authorization, user and recipient request workflows, machine-readable export formats, metadata, API quality of service, audit logs, cloud-switching support, interoperability evidence, non-personal data safeguards, trade-secret or sensitive-data handoff, contract evidence, and operational controls for data access requests.

The purpose of this Skill is to increase awareness of potential gaps in the system and create engineering evidence for qualified review. The response produced by this Skill does not represent legal advice, a legal opinion, or a final regulatory determination.

The main question is:

> When does a Java enterprise system require EU Data Act-aware data access, sharing, portability, interoperability, or cloud-switching controls, and what should developers build differently?

External reference: [Regulation (EU) 2023/2854 Data Act](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R2854).

EU Data Act chapters summary reference: [EU Data Act chapters summary](references/806-regulations-eu-data-act-chapters-summary.md).

Java engineering examples reference: [EU Data Act engineering examples](references/806-regulations-eu-data-act-engineering-examples.md).

Report template asset: [EU Data Act engineering review report template](assets/reports/806-eu-data-act-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems that expose, exchange, store, process, export, port, or derive data through REST APIs, GraphQL APIs, Kafka topics, batch exports, object storage, data lakes, SaaS APIs, data spaces, connected-product integrations, or cloud services
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java services with user-facing data access, third-party sharing, export, portability, interoperability, cloud-switching, or non-personal data governance requirements
- Systems with data holder, user, data recipient, third-party recipient, public-sector exceptional-need, data processing service, data-space participant, smart-contract, or provider-switching signals
- Data access request workflows, authorization checks, consent and entitlement evidence, API quality-of-service records, export jobs, schema registries, metadata catalogs, audit logs, retention and deletion controls, and provider exit runbooks
- Product data, related service data, exportable data, metadata, non-personal data, mixed personal and non-personal datasets, trade secrets, commercially sensitive data, cloud customer data, and data-sharing agreements

## EU Data Act Engineering Review

Treat applicability, data holder status, user entitlement, data recipient role, public-sector exceptional need, trade-secret decisions, contract interpretation, cloud-switching obligations, international access restrictions, and regulatory interpretation as governance decisions for legal, compliance, privacy, data governance, security, product, procurement, cloud, risk, and business owners.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which products, services, APIs, event streams, datasets, exports, data stores, cloud services, and providers are in scope
- Which product data, related service data, exportable data, metadata, personal data, non-personal data, trade secrets, or commercially sensitive data can be accessed or shared
- Which users, data holders, data recipients, third parties, cloud customers, public-sector requesters, and provider owners participate in data workflows
- Which authorization, entitlement, purpose limitation, audit, request, refusal, suspension, deletion, and handoff evidence exists
- Which portability APIs, machine-readable formats, metadata, schemas, quality-of-service expectations, interoperability controls, and switching runbooks are implemented
- Which unresolved legal, contractual, trade-secret, personal-data, international-transfer, or public-sector request questions require qualified owner review

## Constraints

Translate EU Data Act concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by legal, compliance, privacy, data governance, security, product, procurement, cloud, risk, or business owners.

- **NOT LEGAL ADVICE**: Frame findings as data access, portability, interoperability, cloud-switching, and operational engineering controls; recommend qualified review for applicability, roles, contracts, trade secrets, cloud-switching obligations, and regulatory interpretation
- **SCOPE FIRST**: Identify whether the system has connected-product, related-service, data holder, user, data recipient, third-party sharing, public-sector exceptional-need, data-processing-service, data-space, or smart-contract signals before recommending controls
- **DATA INVENTORY**: Require traceable inventories for datasets, metadata, APIs, Kafka topics, object stores, exports, data products, data owners, processors, recipients, and provider systems
- **ACCESS AUTHORIZATION**: Verify entitlement, authentication, authorization, purpose, request origin, recipient role, least privilege, revocation, refusal, suspension, deletion, and audit evidence for data access requests
- **PORTABILITY AND INTEROPERABILITY**: Review machine-readable export formats, API contracts, schemas, metadata, quality-of-service evidence, bulk download, real-time access where technically feasible, standards, and provider switching support
- **NON-PERSONAL DATA SAFEGUARDS**: Preserve non-personal data controls, mixed-dataset separation, confidentiality, international governmental access safeguards, and security during access, transfer, export, and switching
- **TRADE SECRET HANDOFF**: Do not decide trade-secret disclosure boundaries; identify trade-secret or commercially sensitive data and route confidentiality measures, refusals, suspensions, or exceptions to qualified owners
- **CONTRACT AND CLOUD SWITCHING EVIDENCE**: Review data-sharing terms, access terms, compensation evidence, provider exit information, exportable data registers, switching runbooks, continuity controls, and erasure evidence
- **OPERATIONAL REQUEST CONTROLS**: Require observable request intake, SLA handling, identity checks, approvals, audit logs, evidence-safe logging, dispute or complaint routing, support runbooks, and release gates for data access workflows

## When to use this skill

- Review a Java platform for EU Data Act controls
- Design data access and portability evidence for a Java service
- Add data-sharing request workflows, export formats, metadata, audit logs, interoperability, or cloud-switching support
- Assess Data Act engineering readiness before production release
- Check whether Java APIs, Kafka topics, cloud services, or data products support Data Act-aware owner handoffs

## Workflow

1. **Read regulation chapters summary, engineering examples, and report template**

Read `references/806-regulations-eu-data-act-chapters-summary.md`, `references/806-regulations-eu-data-act-engineering-examples.md`, and `assets/reports/806-eu-data-act-engineering-review-report-template.md` in that order. Use the chapters summary for Data Act chapter, article, data access, portability, cloud-switching, interoperability, enforcement, and owner-handoff context. Use the engineering examples for Java control patterns such as data inventory, access authorization, portability APIs, export formats, metadata, audit logs, cloud-switching evidence, non-personal data safeguards, trade-secret handoffs, data-sharing request workflows, contract evidence, and operational controls. Do not start implementation review until the chapters summary, examples reference, and report template are understood.

2. **Classify the data access and portability scope**

Identify service context, possible connected-product or related-service signals, data holder signals, user and recipient roles, public-sector exceptional-need signals, cloud or data-processing-service signals, data-space or smart-contract signals, system owner, data owner, privacy owner, security owner, product owner, provider owner, deployment environments, datasets, metadata, APIs, event streams, data stores, exports, retention, and provider-switching pathways. Escalate unclear applicability, data holder status, user entitlement, data recipient role, trade-secret decisions, contract interpretation, cloud-switching obligations, international access restrictions, or regulatory interpretation to qualified owners.

3. **Review implementation and operational evidence**

Review Java code, API contracts, DTOs, serializers, schema registries, Kafka contracts, batch exports, object storage layouts, metadata catalogs, access-control rules, request workflows, audit logs, privacy controls, tests, runbooks, cloud contracts, provider exit documentation, support workflows, monitoring, and release evidence. Check for gaps between claimed controls and reviewable evidence.

4. **Recommend engineering controls**

Map Data Act concerns to engineering actions: data inventory, role and entitlement evidence, request intake, purpose and authorization checks, machine-readable exports, metadata and schema publication, bulk or real-time API access where technically feasible, audit logging, evidence-safe support operations, non-personal data safeguards, mixed-dataset privacy handoff, trade-secret confidentiality measures, data-sharing terms, cloud-switching runbooks, interoperability standards, erasure controls, and release gates.

5. **Generate review report and owner handoffs**

Use `assets/reports/806-eu-data-act-engineering-review-report-template.md` to produce a concise engineering review with scope, evidence reviewed, Data Act risk signals, potential violation or non-compliance signals, engineering gaps, recommended controls, owner handoffs, residual risks, release decision, and validation steps. State explicitly that legal applicability, data holder/user/recipient roles, trade-secret decisions, contract interpretation, cloud-switching obligations, international access restrictions, and regulatory interpretation require qualified owner review.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/806-regulations-eu-data-act-chapters-summary.md](references/806-regulations-eu-data-act-chapters-summary.md)
- [references/806-regulations-eu-data-act-engineering-examples.md](references/806-regulations-eu-data-act-engineering-examples.md)
