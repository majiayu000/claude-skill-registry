---
name: 813-regulations-iso-42001
description: Use when reviewing, designing, or modifying Java enterprise systems that use GenAI, LLMs, AI-assisted coding, RAG, AI agents, generated code, generated dependencies, prompt workflows, external model providers, or AI-enabled business logic and need ISO/IEC 42001 AI management system-aware engineering guidance. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# ISO/IEC 42001 AI Management System Guidance for GenAI Java Engineering

Use this Skill to review Java enterprise applications, delivery pipelines, AI-assisted development workflows, LLM integrations, RAG systems, AI agents, generated code, generated dependencies, external model-provider usage, prompt handling, and AI-enabled business logic through an ISO/IEC 42001 AI management system lens.

Apply this Skill to determine what engineering controls, evidence, lifecycle governance, risk treatment, monitoring, and owner handoffs are needed before GenAI-assisted Java work is merged, released, connected to enterprise systems, or relied on for business behavior.

This Skill is not legal advice, certification advice, audit advice, an audit conclusion, or a final conformity decision. It helps Java engineers, architects, tech leads, platform teams, security teams, AI governance reviewers, product teams, and reviewers identify when ISO/IEC 42001 AI management system concerns may apply and how to translate them into engineering controls such as AI inventory records, risk treatment, prompt and data governance, secure generated-code review, dependency provenance, model-provider boundaries, monitoring, corrective action, and qualified owner escalation.

The purpose of this Skill is to increase awareness of potential gaps in GenAI Java delivery and create reviewable engineering evidence for qualified owners. The response produced by this Skill does not represent legal advice, certification readiness, audit findings, compliance approval, or final conformity with ISO/IEC 42001.

The main question is:

> What should a Java team build, review, document, and escalate so GenAI development and AI-enabled Java systems are governed as part of an AI management system?

Source provenance: ISO/IEC 42001 public overview material and issue #939 were reviewed while authoring the bundled references. Official source references include:

- ISO 42001 explained: https://www.iso.org/home/insights-news/resources/iso-42001-explained-what-it-is.html
- ISO/IEC 42001 standard page: https://www.iso.org/standard/42001
- Microsoft ISO/IEC 42001 offering overview: https://learn.microsoft.com/en-us/compliance/regulatory/offering-iso-42001

Do not fetch or ingest external regulatory, standard, certification, or audit web pages at runtime. Use the bundled references and escalate interpretation, certification, audit, legal, compliance, and conformity questions to qualified owners.

ISO/IEC 42001 summary reference: [ISO/IEC 42001 AI management system summary](references/813-regulations-iso-42001-chapters-summary.md).

Java engineering examples reference: [ISO/IEC 42001 GenAI Java engineering examples](references/813-regulations-iso-42001-engineering-examples.md).

Questionnaire asset: [ISO/IEC 42001 engineering review questionnaire](assets/questions/813-iso-42001-engineering-review-questionnaire.md).

Report template asset: [ISO/IEC 42001 engineering review report template](assets/reports/813-iso-42001-engineering-review-report-template.md).

## Scope

This Skill applies to:

- Java systems using LLMs, RAG, embeddings, prompt templates, AI agents, tool calling, model gateways, or external AI services
- AI-assisted Java development where generated code, tests, SQL, migrations, API contracts, infrastructure definitions, dependencies, or business rules may enter the codebase
- Spring Boot, Quarkus, Micronaut, and framework-agnostic Java systems that use generated implementation patterns or generated business logic
- Prompt, source-code, log, ticket, production-data, customer-data, regulated-data, and trade-secret exposure paths to AI tools or model providers
- Generated dependency and supply-chain review, including package provenance, license, vulnerability, malicious-package, and unsuitable-dependency signals
- AI management system evidence such as AI inventory, risk assessment, risk treatment, lifecycle controls, data governance, model-provider boundaries, monitoring, incident handling, corrective action, and continual improvement
- Owner handoffs to legal, compliance, privacy, security, risk, AI governance, platform, architecture, product, business, procurement, and model-provider owners

## ISO/IEC 42001 Engineering Review

Treat certification scope, conformity, audit conclusions, legal obligations, regulatory applicability, official interpretation, and final risk acceptance as qualified owner decisions.

Engineering teams should still create evidence that makes those decisions reviewable:

- Which GenAI capability, AI-assisted delivery path, generated artifact, model provider, prompt flow, RAG corpus, AI agent, or AI-enabled business rule is in scope
- Which risk owner, data owner, system owner, product owner, security owner, privacy owner, compliance owner, model-provider owner, and release owner are accountable
- Which generated Java implementation, dependency, prompt, retrieval source, tool action, test, business rule, model version, and production behavior can be reconstructed
- Which controls prevent hallucinated code, insecure generated implementation, generated dependency and supply-chain contamination, IP leakage, confidentiality breach, regulatory non-compliance risk, and biased generated business logic
- Which monitoring, incident, corrective-action, rollback, disablement, retraining, source-removal, dependency-removal, prompt-remediation, and owner-escalation paths exist

## Constraints

Translate ISO/IEC 42001 AI management system concerns into engineering controls for GenAI Java development. Do not provide legal advice, certification advice, audit conclusions, conformity decisions, or replace qualified owner review.

- **NOT LEGAL, CERTIFICATION, OR AUDIT ADVICE**: Frame findings as engineering controls, evidence gaps, and escalation points; never claim ISO/IEC 42001 certification readiness, audit pass/fail status, legal compliance, or final conformity
- **BUNDLED REFERENCES FIRST**: Read the bundled ISO/IEC 42001 summary and engineering examples before implementation review; do not fetch external regulatory, standard, certification, or audit pages at runtime
- **AI MANAGEMENT SYSTEM SCOPE FIRST**: Identify the GenAI capability, AI-assisted delivery path, generated artifact, lifecycle stage, owners, data boundaries, model-provider boundary, risk treatment path, and release context before recommending controls
- **GENAI RISK COVERAGE**: Address hallucinated code, insecure generated implementation, generated dependency and supply-chain contamination, IP leakage, confidentiality breach, regulatory non-compliance risk, and biased generated business logic
- **SOURCE AND PROMPT CONFIDENTIALITY**: Do not send proprietary source code, secrets, credentials, regulated data, customer data, private logs, or trade-secret business logic to external models without approved policy, redaction, minimization, and owner approval
- **GENERATED CODE REVIEW**: Require human engineering review, tests, static analysis, security review, architecture fit, and traceable source context before generated Java code, SQL, migrations, configuration, or business rules are merged or released
- **SUPPLY CHAIN GOVERNANCE**: Validate generated dependency suggestions through approved repositories, dependency policies, SBOM, vulnerability scanning, license review, provenance checks, and malicious-package detection before adoption
- **BIAS AND BUSINESS LOGIC**: Escalate AI-generated decision rules, eligibility logic, pricing, ranking, fraud, employment, credit, health, insurance, access, or rights-impacting behavior to business, legal, compliance, privacy, and risk owners
- **EVIDENCE FIRST**: Prefer reviewable evidence over claims that AI use, generated code, model selection, data governance, monitoring, or corrective action is controlled
- **OWNER HANDOFFS**: Include legal, compliance, privacy, security, AI governance, platform, product, business, procurement, and model-provider owners when risk ownership, certification scope, audit evidence, or regulatory interpretation is unclear

## When to use this skill

- Review GenAI-assisted Java development for ISO/IEC 42001 AI management system controls
- Assess AI-generated Java code, SQL, migrations, tests, dependencies, prompts, RAG sources, or business logic before merge or release
- Add governance evidence for LLM integrations, model providers, RAG workflows, AI agents, or prompt handling in Java systems
- Check generated dependency, supply-chain, IP leakage, confidentiality, bias, hallucination, or regulatory non-compliance risks in Java delivery
- Escalate certification, audit, conformity, legal, compliance, privacy, security, or risk questions to qualified owners

## Workflow

1. **Read ISO/IEC 42001 references, questionnaire, and report template**

Read `references/813-regulations-iso-42001-chapters-summary.md`, `references/813-regulations-iso-42001-engineering-examples.md`, `assets/questions/813-iso-42001-engineering-review-questionnaire.md`, and `assets/reports/813-iso-42001-engineering-review-report-template.md` in that order. Use the summary for AI management system scope, context, leadership, planning, support, operation, evaluation, improvement, lifecycle governance, risk treatment, and owner-handoff context. Use the engineering examples for Java control patterns such as AI inventory, prompt and data boundaries, generated-code review, dependency provenance, RAG source governance, AI-agent controls, bias review, monitoring, incident handling, and corrective action. Use the questionnaire to classify scope and evidence gaps before producing the report. Do not start implementation review until the summary, examples reference, questionnaire rules, and report template are understood.

2. **Complete questionnaire and classify GenAI delivery scope**

Use `assets/questions/813-iso-42001-engineering-review-questionnaire.md` as a checklist against trusted local project evidence and maintainer-approved sanitized facts. Identify the Java system, GenAI capability, AI-assisted development workflow, generated artifacts, model provider, prompts, retrieval sources, data classes, dependencies, business logic, environments, users, lifecycle stage, system owner, data owner, risk owner, security owner, privacy owner, compliance owner, product owner, platform owner, and release owner. Mark unknowns as evidence gaps and escalate missing ownership before release recommendations.

3. **Review implementation and delivery evidence**

Review Java code, configuration, tests, build files, Maven dependencies, SBOM or dependency evidence, prompts, RAG source registries, model version records, generated outputs, AI-agent tool policies, CI/CD workflows, deployment records, monitoring, incident records, and owner approvals. Check for gaps between claimed AI management controls and reviewable evidence.

4. **Map GenAI risks to engineering controls**

Map hallucinated code, insecure generated implementation, generated dependency and supply-chain contamination, IP leakage, confidentiality breach, regulatory non-compliance risk, and biased generated business logic to concrete controls: source verification, human review, tests, static analysis, secure coding review, dependency policy gates, approved model/provider routes, data minimization, redaction, access control, retrieval governance, bias and impact testing, monitoring, incident response, rollback, disablement, corrective action, and owner escalation.

5. **Generate review report and owner handoffs**

Use `assets/reports/813-iso-42001-engineering-review-report-template.md` to produce a concise engineering review with scope, evidence reviewed, ISO/IEC 42001 AI management system risk signals, GenAI Java risk findings, potential management-system nonconformity signals, evidence gaps, recommended controls, owner handoffs, residual risks, release readiness notes, validation steps, and action plan. State explicitly that legal advice, certification advice, audit conclusions, official interpretation, final risk acceptance, and final conformity decisions require qualified owner review.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/813-regulations-iso-42001-chapters-summary.md](references/813-regulations-iso-42001-chapters-summary.md)
- [references/813-regulations-iso-42001-engineering-examples.md](references/813-regulations-iso-42001-engineering-examples.md)
