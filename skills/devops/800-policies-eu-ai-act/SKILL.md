---
name: 800-policies-eu-ai-act
description: Use when reviewing, designing, or modifying Java enterprise systems that use AI, LLMs, AI agents, RAG, tool calling, workflow automation, or model-based decision support and need EU AI Act policy awareness. This should trigger for requests such as Review a Java AI system for EU AI Act controls; Design governance for an AI agent with enterprise tools; Add human oversight and auditability to LLM workflows; Assess RAG or model-driven decision support before production release. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0-SNAPSHOT
---
# EU AI Act Policy for Java Enterprise Development with AI Systems and AI Agents

Use this Skill to review Java enterprise applications that include AI capabilities, AI agents, tool-calling workflows, RAG systems, workflow automation, or model-driven decision support.

Apply this Skill to determine what engineering controls are required before the system is released, deployed, or connected to corporate systems of record.

This Skill is not legal advice. It helps Java engineers, architects, tech leads, platform teams, and reviewers identify when EU AI Act concerns may apply and how to translate policy expectations into enterprise architecture controls such as policy gates, human oversight, least privilege, audit evidence, monitoring, escalation workflows, and approval processes.

The main question is:

> When does a Java application or AI agent require EU AI Act-aware engineering controls, and what should developers build differently?

External reference: [European Parliament legislative resolution TA-9-2024-0138](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689).

## Scope

This Skill applies to:

- Java applications embedding AI models or LLMs
- Spring AI, LangChain4j, Quarkus AI, and custom AI integrations
- RAG applications and enterprise knowledge assistants
- AI agents capable of calling enterprise tools
- Workflow automation driven by AI decisions or recommendations
- AI systems interacting with databases, APIs, message brokers, filesystems, IAM platforms, CI/CD pipelines, cloud resources, or external services
- AI-generated code, SQL, Flyway migrations, Liquibase changelogs, infrastructure definitions, operational runbooks, or deployment actions

## AI System vs AI Agent

An AI System generates information, recommendations, classifications, rankings, predictions, or content.

Examples:
- Customer support assistant
- Knowledge search assistant
- Internal chatbot
- Document summarization service
- Code-generation assistant

An AI Agent can execute actions through tools.

Examples:
- Database maintenance agent
- Migration generation agent
- CI/CD deployment agent
- Procurement automation agent
- Incident response agent

For enterprise governance purposes, AI Agents require additional review because they can directly modify systems, data, infrastructure, permissions, or business processes.

The engineering risk increases significantly when an AI system becomes an AI agent capable of executing actions through enterprise tools.

Even when a use case is not classified as EU AI Act High-Risk, organizations should implement human oversight, approval workflows, auditability, least privilege, monitoring, and operational controls before granting AI agents access to corporate systems of record.

## Constraints

Translate EU AI Act concerns into engineering controls for Java enterprise systems. Do not provide legal advice or replace review by counsel, compliance, privacy, security, or risk owners.

- **NOT LEGAL ADVICE**: Frame findings as engineering risk controls and escalation points; recommend legal or compliance review for classification, jurisdiction, and regulatory interpretation
- **SCOPE**: Apply this skill to AI systems, LLM integrations, RAG, AI agents, tool calling, automated workflow decisions, and model-driven decision support in Java enterprise systems
- **CLASSIFICATION FIRST**: Distinguish AI system, AI agent, decision-support system, and fully automated action before recommending controls
- **HIGH-RISK SIGNALS**: Escalate use cases involving employment, education, credit, essential services, biometric identification, law enforcement, migration, justice, or safety-critical decisions
- **PROHIBITED OR SENSITIVE USES**: Flag manipulative, exploitative, social scoring, unlawful biometric, or surveillance-like patterns for immediate governance review
- **HUMAN OVERSIGHT**: Require explicit approval workflows for AI outputs or agent actions that can affect rights, access, money, employment, safety, production systems, or regulated records
- **LEAST PRIVILEGE**: Do not grant AI agents broad credentials, write access, production permissions, or unrestricted tools without scoped authorization, policy checks, and revocation paths
- **AUDITABILITY**: Preserve prompts, model versions, retrieved sources, tool calls, approvals, decisions, outputs, and operator overrides as reviewable evidence where policy requires it
- **DATA GOVERNANCE**: Validate data lineage, retention, privacy, access control, source attribution, and RAG corpus quality before using enterprise data in AI workflows

## When to use this skill

- Review a Java AI system for EU AI Act controls
- Design governance for an AI agent with enterprise tools
- Add human oversight and auditability to LLM workflows
- Assess RAG or model-driven decision support before production release
- Check whether AI-generated code, SQL, migrations, runbooks, or deployment actions need approval gates

## Workflow

1. **Read reference materials and examples**

Read `references/800-policies-eu-ai-act.md`, `references/800-policies-eu-ai-act-chapters-summary.md`, `assets/questions/800-eu-ai-act-risk-questionnaire.md`, and `assets/reports/800-eu-ai-act-engineering-review-report-template.md` to understand the policy context, risk signals, example patterns (classification notes, approval gates, audit evidence, RAG governance, release gates, database change control, prohibited-practice guards, Annex III classifiers, post-market monitoring), and report structure. Do not start code review or produce the report yet.

2. **Ask the questionnaire questions interactively**

Follow the IMPORTANT rules at the top of `assets/questions/800-eu-ai-act-risk-questionnaire.md`. Ask the human one question at a time from Question 1 through Question 23. Present only the current question with its options; wait for an answer before the next. Do NOT batch questions, preview upcoming questions, or answer from code, docs, or assumptions. Record answers verbatim. Probe "Unknown" responses. Stop and escalate immediately if prohibited-practice signals are identified. Do not proceed to implementation review or the report until all 23 questions are answered.

3. **Review the implementation and identify patterns**

Based on the questionnaire answers, review the Java implementation code, configuration, tests, and documentation to verify claims, identify AI capabilities (models, LLMs, RAG, agents, tool calls, generated artifacts), and match relevant example patterns from the reference. Check for gaps between what was answered and what exists in the code.

4. **Classify risk and recommend engineering controls**

Use the questionnaire answers and code review findings to classify the capability (AI system, decision support, automated decision, AI agent, or not an AI system), assess prohibited-practice signals, Annex III high-risk domains, Annex I product/sector signals, sensitive data, regulated decisions, general-purpose model concerns, and enterprise-system-of-record impact. Match the relevant example patterns and recommend specific engineering controls: human oversight, policy gates, least privilege, audit evidence, data governance, monitoring, incident response, and rollback procedures.

5. **Generate review report and prioritized actions**

Use `assets/reports/800-eu-ai-act-engineering-review-report-template.md` to document the review context, capability summary, questionnaire findings (with answers and gaps), EU AI Act risk classification, engineering controls, evidence inventory, residual risks, release decision, and prioritized action plan with owners and due dates.

## Reference

For detailed guidance, examples, and constraints, see:

- [references/800-policies-eu-ai-act.md](references/800-policies-eu-ai-act.md)
- [references/800-policies-eu-ai-act-chapters-summary.md](references/800-policies-eu-ai-act-chapters-summary.md)
