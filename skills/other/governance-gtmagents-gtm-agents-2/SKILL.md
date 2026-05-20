---
name: governance
description: Use to enforce approvals, compliance, and auditability for personalization
  programs.
---

# Personalization Governance Skill

## When to Use
- Deploying or updating personalization rules, models, or high-impact content variants.
- Running quarterly audits on consent, data usage, or fairness metrics.
- Investigating incidents related to personalization errors or policy breaches.

## Framework
1. **Policy Alignment** – document legal, privacy, accessibility, and ethical constraints per channel.
2. **Approval Workflow** – define RACI (architect, legal, security, marketing) and required evidence per change.
3. **Change Logging** – capture version metadata (who, what, when, why), including rollback steps.
4. **Risk Monitoring** – set KPIs + alerts for fairness, bias, consent violations, or performance regressions.
5. **Audit Trail** – maintain dashboards + storage for decision logs, approvals, and incident reports.

## Templates
- Change request form (summary, impact, risk score, approvers, attachments).
- Governance checklist (consent, accessibility, localization, security, QA evidence).
- Incident review template (root cause, remediation, follow-up actions, owner).

## Tips
- Pair governance checkpoints with CI/CD or deployment scripts to prevent bypass.
- Use unique change IDs to connect decision tree updates with content variants and experiments.
- Schedule quarterly tabletop exercises to keep stakeholders fluent in escalation paths.

---
