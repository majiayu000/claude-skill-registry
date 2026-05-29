---
name: software-ux-research
description: UX research and analysis for discovering, validating, and evaluating software experiences, including research ops, governance, and measurement.
---

# Software UX Research Skill — Quick Reference

Use this skill to identify problems/opportunities and de-risk decisions. Use `software-ui-ux-design` to implement UI patterns, component changes, and design system updates.

---

## Dec 2025 Baselines (Core)

- **Human-centred design**: Iterative design + evaluation grounded in evidence (ISO 9241-210:2019) https://www.iso.org/standard/77520.html
- **Usability definition**: Effectiveness, efficiency, satisfaction in context (ISO 9241-11:2018) https://www.iso.org/standard/63500.html
- **Accessibility baseline**: WCAG 2.2 is a W3C Recommendation (12 Dec 2024) https://www.w3.org/TR/WCAG22/
- **EU shipping note**: European Accessibility Act applies to covered products/services after 28 Jun 2025 (Directive (EU) 2019/882) https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L0882

## When to Use This Skill

- Discovery: user needs, JTBD, opportunity sizing, mental models.
- Validation: concepts, prototypes, onboarding/first-run success.
- Evaluative: usability tests, heuristic evaluation, cognitive walkthroughs.
- Quant/behavioral: funnels, cohorts, instrumentation gaps, guardrails.
- Research Ops: intake, prioritization, repository/taxonomy, consent/PII handling.

---

## Operating Mode (Core)

If inputs are missing, ask for:

- Decision to unblock (what will change based on this research).
- Target roles/segments and top tasks.
- Platforms and contexts (web/mobile/desktop; remote/on-site; assisted tech).
- Existing evidence (analytics, tickets, reviews, recordings, prior studies).
- Constraints (timeline, recruitment access, compliance, budget).

Default outputs (pick what the user asked for):

- Research plan + output contract (prefer [../software-clean-code-standard/templates/checklists/ux-research-plan-template.md](../software-clean-code-standard/templates/checklists/ux-research-plan-template.md); use [templates/research-plan-template.md](templates/research-plan-template.md) for skill-specific detail)
- Study protocol (tasks/script + success metrics + recruitment plan)
- Findings report (issues + severity + evidence + recommendations + confidence)
- Decision brief (options + tradeoffs + recommendation + measurement plan)

---

## Method Chooser (Core)

### Research Types (Keep Explicit)

| Type | Goal | Primary Outputs |
|------|------|-----------------|
| Discovery | Understand needs and context | JTBD, opportunity areas, constraints |
| Validation | Reduce solution risk | Go/no-go, prioritization signals |
| Evaluative | Improve usability/accessibility | Severity-rated issues + fixes |

### Decision Tree (Fast)

```text
What do you need?
  ├─ WHY / needs / context → interviews, contextual inquiry, diary
  ├─ HOW / usability → moderated usability test, cognitive walkthrough, heuristic eval
  ├─ WHAT / scale → analytics/logs + targeted qual follow-ups
  └─ WHICH / causal → experiments (if feasible) or preference tests
```

### Method Selection Table (Practical)

| Question | Best methods | Avoid when | Output |
|----------|--------------|------------|--------|
| What problems matter most? | Interviews, contextual inquiry, diary | Only surveys/analytics | Problem framing + evidence |
| Can users complete key tasks? | Moderated usability tests, task analysis | Stakeholder review | Task success + issue list |
| Is navigation findable? | Tree test, first-click, card sort | Extremely small audience [Inference] | IA changes + labels |
| What is happening at scale? | Funnels, cohorts, logs, support taxonomy | Instrumentation missing | Baselines + segments + drop-offs |
| Which variant performs better? | A/B, switchback, holdout | Insufficient power or high risk | Decision with confidence + guardrails |

---

## Research by Product Stage

### Stage Framework (What to Do When)

| Stage | Decisions | Primary Methods | Secondary Methods | Output |
|-------|-----------|-----------------|-------------------|--------|
| Discovery | What to build and for whom | Interviews, field/diary, journey mapping | Competitive analysis, feedback mining | Opportunity brief + JTBD |
| Concept/MVP | Does the concept work? | Concept test, prototype usability | First-click/tree test | MVP scope + onboarding plan |
| Launch | Is it usable + accessible? | Usability testing, accessibility review | Heuristic eval, session replay | Launch blockers + fixes |
| Growth | What drives adoption/value? | Segmented analytics + qual follow-ups | Churn interviews, surveys | Retention drivers + friction |
| Maturity | What to optimize/deprecate? | Experiments, longitudinal tracking | Unmoderated tests | Incremental roadmap |

### Post-Launch Measurement (What to Track)

| Metric category | What it answers | Pair with |
|----------------|------------------|----------|
| Adoption | Are people using it? | Outcome/value metric |
| Value | Does it help users succeed? | Adoption + qualitative reasons |
| Reliability | Does it fail in ways users notice? | Error rate + recovery success |
| Accessibility | Can diverse users complete flows? | Assistive-tech coverage + defect trends |

---

## Research for Complex Systems (Workflows, Admin, Regulated)

### Complexity Indicators

| Indicator | Example | Research Implication |
|-----------|---------|----------------------|
| Multi-step workflows | Draft → approve → publish | Task analysis + state mapping |
| Multi-role permissions | Admin vs editor vs viewer | Test each role + transitions |
| Data dependencies | Requires integrations/sync | Error-path + recovery testing |
| High stakes | Finance, healthcare | Safety checks + confirmations |
| Expert users | Dev tools, analytics | Recruit real experts (not proxies) |

### Evaluation Methods (Core)

- Contextual inquiry: observe real work and constraints.
- Task analysis: map goals → steps → failure points.
- Cognitive walkthrough: evaluate learnability and signifiers.
- Error-path testing: timeouts, offline, partial data, permission loss, retries.
- Multi-role walkthrough: simulate handoffs (creator → reviewer → admin).

### Multi-Role Coverage Checklist

- [ ] Role-permission matrix documented.
- [ ] “No access” UX defined (request path, least-privilege defaults).
- [ ] Cross-role handoffs tested (notifications, state changes, audit history).
- [ ] Error recovery tested for each role (retry, undo, escalation).

---

## Research Ops & Governance (Core)

### Intake (Make Requests Comparable)

Minimum required fields:

- Decision to unblock and deadline.
- Research questions (primary + secondary).
- Target users/segments and recruitment constraints.
- Existing evidence and links.
- Deliverable format + audience.

### Prioritization (Simple Scoring)

Use a lightweight score to avoid backlog paralysis:

- Decision impact
- Knowledge gap
- Timing urgency
- Feasibility (recruitment + time)

### Repository & Taxonomy

- Store each study with: method, date, product area, roles, tasks, key findings, raw evidence links.
- Tag for reuse: problem type (navigation/forms/performance), component/pattern, funnel step.
- Prefer “atomic” findings (one insight per card) to enable recombination [Inference].

### Consent, PII, and Access Control

Follow applicable privacy laws; GDPR is a primary reference for EU processing https://eur-lex.europa.eu/eli/reg/2016/679/oj

PII handling checklist:

- [ ] Collect minimum PII needed for scheduling and incentives.
- [ ] Store identity/contact separately from study data.
- [ ] Redact names/emails from transcripts before broad sharing.
- [ ] Restrict raw recordings to need-to-know access.
- [ ] Document consent, purpose, retention, and opt-out path.

---

## Measurement & Decision Quality (Core)

### Triangulation Rubric

| Confidence | Evidence requirement | Use for |
|------------|----------------------|---------|
| High | Multiple methods or sources agree | High-impact decisions |
| Medium | Strong signal from one method + supporting indicators | Prioritization |
| Low | Single source / small sample | Exploratory hypotheses |

### Adoption vs Value (Avoid Vanity Metrics)

| Metric type | Example | Common pitfall |
|-------------|---------|----------------|
| Adoption | Feature usage rate | “Used” ≠ “helpful” |
| Value/outcome | Task success, goal completion | Harder to instrument |

### When NOT to Run A/B Tests

| Situation | Why it fails | Better method |
|----------|--------------|---------------|
| Low power/traffic | Inconclusive results | Usability tests + trends |
| Many variables change | Attribution impossible | Prototype tests → staged rollout |
| Need “why” | Experiments don’t explain | Interviews + observation |
| Ethical constraints | Harmful denial | Phased rollout + holdouts |
| Long-term effects | Short tests miss delayed impact | Longitudinal + retention analysis |

### Common Confounds (Call Out Early)

- Selection bias (only power users respond).
- Survivorship bias (you miss churned users).
- Novelty effect (short-term lift).
- Instrumentation changes mid-test (metrics drift).

---

## Optional: AI/Automation Research Considerations

> Use only when researching automation/AI-powered features. Skip for traditional software UX.

### Key Questions

| Dimension | Question | Methods |
|----------|----------|---------|
| Mental model | What do users think the system can/can’t do? | Interviews, concept tests |
| Trust calibration | When do users over/under-rely? | Scenario tests, log review |
| Explanation usefulness | Does “why” help decisions? | A/B explanation variants, interviews |
| Failure recovery | Do users recover and finish tasks? | Failure-path usability tests |

### Error Taxonomy (User-Visible)

| Failure type | Typical impact | What to measure |
|-------------|----------------|----------------|
| Wrong output | Rework, lost trust | Verification + override rate |
| Missing output | Manual fallback | Fallback completion rate |
| Unclear output | Confusion | Clarification requests |
| Non-recoverable failure | Blocked flow | Time-to-recovery, support contact |

### Optional: AI-Assisted Research Ops (Guardrailed)

- Use automation for transcription/tagging only after PII redaction.
- Maintain an audit trail: every theme links back to raw quotes/clips.
- Prohibit fabricated quotes and “synthetic users” as evidence for real decisions.

---

## Navigation

### Resources

- [resources/research-frameworks.md](resources/research-frameworks.md) — JTBD, Kano, Double Diamond, Service Blueprint, opportunity mapping
- [resources/ux-audit-framework.md](resources/ux-audit-framework.md) — Heuristic evaluation, cognitive walkthrough, severity rating
- [resources/usability-testing-guide.md](resources/usability-testing-guide.md) — Task design, facilitation, analysis
- [resources/ux-metrics-framework.md](resources/ux-metrics-framework.md) — Task metrics, SUS/HEART, measurement guidance
- [resources/customer-journey-mapping.md](resources/customer-journey-mapping.md) — Journey mapping and service blueprints
- [resources/pain-point-extraction.md](resources/pain-point-extraction.md) — Feedback-to-themes method
- [resources/review-mining-playbook.md](resources/review-mining-playbook.md) — B2B/B2C review mining
- [data/sources.json](data/sources.json) — Curated external references

### Templates

- Shared plan template: [../software-clean-code-standard/templates/checklists/ux-research-plan-template.md](../software-clean-code-standard/templates/checklists/ux-research-plan-template.md) — Product-agnostic research plan template (core + optional AI)
- [templates/research-plan-template.md](templates/research-plan-template.md) — UX research plan template
- [templates/testing/usability-test-plan.md](templates/testing/usability-test-plan.md) — Usability test plan
- [templates/testing/usability-testing-checklist.md](templates/testing/usability-testing-checklist.md) — Usability testing checklist
- [templates/audits/heuristic-evaluation-template.md](templates/audits/heuristic-evaluation-template.md) — Heuristic evaluation
- [templates/audits/ux-audit-report-template.md](templates/audits/ux-audit-report-template.md) — Audit report
