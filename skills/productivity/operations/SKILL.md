---
name: operations
description: "Business operations workflows — vendor management, runbooks, process documentation, risk assessment, capacity planning, change management, compliance tracking. Use when reviewing vendors, writing runbooks, documenting processes, assessing risk, planning capacity, or managing change."
routing:
  triggers:
    - "operations"
    - "vendor review"
    - "runbook"
    - "process documentation"
    - "risk assessment"
    - "capacity plan"
    - "change management"
    - "compliance tracking"
  category: business
  force_route: false
  pairs_with:
    - csuite
    - finance
    - hr
user-invocable: true
---

# Operations

Umbrella skill for business operations: vendor management, runbooks, process documentation, risk assessment, capacity planning, change management, compliance tracking, status reporting, and process optimization. Each mode loads its own reference files on demand.

**Scope**: Operational workflows that keep the business running. Use csuite for strategic decisions, finance for budgeting/forecasting, and hr for people operations.

---

## Mode Detection

Classify the request into exactly one mode. If it spans multiple, choose the primary and note the secondary.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **RUNBOOK** | runbook, procedure, on-call, playbook, step-by-step, ops task | `references/runbook-authoring.md` |
| **RISK** | risk assessment, risk register, what could go wrong, risk matrix | `references/risk-assessment.md` |
| **VENDOR** | vendor review, vendor evaluation, contract review, procurement | `references/vendor-management.md` |
| **PROCESS** | process doc, SOP, RACI, workflow documentation, process map | `references/process-documentation.md` |
| **CHANGE** | change request, change management, CAB, rollout, deployment change | `references/change-management.md` |
| **CAPACITY** | capacity plan, resource allocation, utilization, headcount planning | `references/process-documentation.md` |
| **COMPLIANCE** | compliance, audit prep, SOC 2, ISO 27001, GDPR, regulatory | `references/risk-assessment.md` |
| **STATUS** | status report, weekly update, project health, KPIs | (no deep reference needed) |
| **OPTIMIZE** | process improvement, bottleneck, streamline, too many steps | `references/process-documentation.md` |

Always load `references/llm-ops-failure-modes.md` regardless of mode. It contains the failure patterns that apply across all operations work.

---

## Instructions

### Mode: RUNBOOK

**Framework**: SCOPE -> AUTHOR -> VERIFY

**Phase 1: SCOPE** -- Define what the runbook covers.

- Name the task, its frequency, and who runs it
- List prerequisites: access, tools, credentials, prior state
- Identify the trigger: scheduled, event-driven, or manual invocation
- Ask: "If a new hire ran this at 3am during an incident, what would they need?"

**Gate**: Task named. Prerequisites listed. Trigger defined.

**Phase 2: AUTHOR** -- Write the procedure with painful specificity.

Load `references/runbook-authoring.md`.

Critical rules:
- Every step has: exact command/action, expected result, failure handling
- "Run the script" is NOT a step. `python sync.py --prod --dry-run` from `/opt/ops/` as `deploy-user` IS a step
- Include verification after every state-changing step
- Rollback procedure for the entire runbook AND per-step rollback where applicable
- Escalation paths with names, contact methods, and when-to-escalate triggers

| Step Component | Required | Example |
|---------------|----------|---------|
| Action | Yes | `kubectl rollout restart deployment/api -n production` |
| Expected result | Yes | "Pods restart within 60s. `kubectl get pods` shows 3/3 Running." |
| Failure handling | Yes | "If pods stay in CrashLoopBackOff >2min, proceed to Rollback." |
| Verification | Yes | `curl -s https://api.example.com/health | jq .status` returns `"ok"` |
| Rollback | Per-step | `kubectl rollout undo deployment/api -n production` |

**Gate**: Every step has all five components. Rollback procedure exists. Escalation path defined.

**Phase 3: VERIFY** -- Validate the runbook is actually usable.

- Walk through the runbook as if you have never seen the system
- Flag any step that requires unstated knowledge
- Confirm the troubleshooting table covers symptoms from each step's failure mode
- Check: could someone follow this at 3am with no prior context?

**Gate**: All steps self-contained. No implicit knowledge. Troubleshooting table complete.

---

### Mode: RISK

**Framework**: IDENTIFY -> ASSESS -> MITIGATE

**Phase 1: IDENTIFY** -- Enumerate risks systematically by category.

Load `references/risk-assessment.md`.

| Category | What to Look For |
|----------|-----------------|
| Operational | Process failures, staffing gaps, system outages, single points of failure |
| Financial | Budget overruns, vendor cost increases, revenue impact, currency exposure |
| Compliance | Regulatory violations, audit findings, policy breaches, certification gaps |
| Strategic | Market changes, competitive threats, technology shifts, dependency risks |
| Reputational | Customer impact, public perception, partner relationships, data incidents |
| Security | Data breaches, access control failures, third-party vulnerabilities |

- Extend risk identification beyond obvious items. Ask: "What kills us if it happens, even if it seems unlikely?"
- Separate risks from issues. A risk might happen. An issue already has.

**Gate**: Risks enumerated across all applicable categories. Each risk has a clear description.

**Phase 2: ASSESS** -- Score each risk on probability and impact.

Apply the probability x impact matrix:

| | Low Impact | Medium Impact | High Impact |
|---|-----------|---------------|-------------|
| **High Probability** | Medium | High | Critical |
| **Medium Probability** | Low | Medium | High |
| **Low Probability** | Low | Low | Medium |

For each risk:
- Probability: base on evidence, not optimism. "It hasn't happened yet" is not "low probability"
- Impact: quantify in dollars, hours, or affected users where possible
- Risk level: derived from matrix, not gut feel

**Gate**: Every risk scored. No unquantified "High" without supporting rationale.

**Phase 3: MITIGATE** -- Plan mitigations and track residual risk.

For each High/Critical risk:
- Mitigation action (specific, not "monitor the situation")
- Owner (named person, not "the team")
- Timeline (date, not "soon")
- Residual risk after mitigation
- Acceptance criteria: what makes the residual risk acceptable?

**Gate**: All High/Critical risks have mitigations with owners and dates. Residual risk documented.

---

### Mode: VENDOR

**Framework**: EVALUATE -> SCORE -> RECOMMEND

**Phase 1: EVALUATE** -- Gather structured information.

Load `references/vendor-management.md`.

Required inputs:
- Vendor name and what they provide
- Context: new evaluation, renewal, or comparison
- Available data: proposal, contract, performance history, pricing

Due diligence checklist (minimum):
- Financial stability signals
- Security posture (SOC 2, penetration testing, incident history)
- Customer references (ask for churned customers too)
- Contract terms: auto-renewal, termination notice, price escalation clauses
- Data portability: export format, migration support, data deletion

**Gate**: Due diligence complete. Contract terms reviewed. Red flags documented.

**Phase 2: SCORE** -- Apply the vendor scorecard.

| Dimension | Weight | Score (1-10) |
|-----------|--------|-------------|
| Functional fit | 5x | |
| Total cost of ownership | 4x | |
| Integration complexity | 4x | |
| Support quality | 3x | |
| Security/compliance | 3x | |
| Data portability | 3x | |
| Company stability | 2x | |
| Contract flexibility | 2x | |

TCO must include: license, implementation, training, support, ongoing maintenance, exit costs. License price alone is not TCO.

**Gate**: All dimensions scored with rationale. TCO calculated for Year 1 and Year 3.

**Phase 3: RECOMMEND** -- Deliver verdict with negotiation points.

- Verdict: Proceed / Negotiate / Pass
- Key strengths and concerns
- Negotiation leverage points
- Contract review triggers (price escalation >X%, SLA misses, acquisition)
- Performance monitoring plan post-contract

**Gate**: Recommendation stated. Negotiation points listed. Monitoring plan defined.

---

### Mode: PROCESS

**Framework**: MAP -> DOCUMENT -> OPTIMIZE

**Phase 1: MAP** -- Capture how the process actually works today.

Load `references/process-documentation.md`.

- Map the real process, not the idealized version. "We're supposed to do X but actually we do Y" is the most valuable input.
- Capture every step, decision point, handoff, and exception
- Identify: who does it (role, not name), what triggers it, what it produces, how long it takes
- Document exceptions and edge cases — these are where processes actually break

**Gate**: Current state mapped. All steps, handoffs, and exceptions documented.

**Phase 2: DOCUMENT** -- Produce the SOP.

Structure:
- Purpose and scope
- RACI matrix (Responsible, Accountable, Consulted, Informed for each step)
- Step-by-step procedure with inputs, actions, outputs, and exception handling
- Metrics: what to measure, target values, how to measure

RACI rules:
- Exactly one A (Accountable) per step. Multiple As = no one is accountable.
- R (Responsible) is who does the work. A is who owns the outcome.
- If a step has no R, it doesn't get done. If it has no A, no one notices when it doesn't.

**Gate**: SOP complete. RACI has exactly one A per step. Exceptions documented.

**Phase 3: OPTIMIZE** -- Identify improvement opportunities.

- Identify waste: waiting, rework, unnecessary handoffs, over-processing, manual work that could be automated
- Bottleneck analysis: which step constrains throughput?
- Recommendations: eliminate, automate, parallelize, simplify
- Before/after comparison with estimated impact

**Gate**: Bottlenecks identified. Recommendations specific and measurable.

---

### Mode: CHANGE

**Framework**: ASSESS -> PLAN -> EXECUTE

**Phase 1: ASSESS** -- Define the change and its impact.

Load `references/change-management.md`.

- What is changing and why (business justification, not just "improvement")
- Who is affected: users, systems, processes, teams
- Impact assessment by area (users, systems, processes, cost) rated High/Medium/Low
- Risk assessment: what could go wrong, likelihood, mitigation
- Resistance forecast: who will resist and why

**Gate**: Change defined. Impact assessed by area. Risks identified.

**Phase 2: PLAN** -- Build the implementation and communication plan.

| Plan Component | Required Elements |
|---------------|-------------------|
| Implementation | Steps, owners, timeline, dependencies |
| Communication | Audience, message, channel, timing |
| Training | What skills needed, delivery method, timeline |
| Rollback | Trigger criteria, steps, verification |
| Approval | Who approves, role, current status |

Communication rules:
- Explain WHY before WHAT
- Communicate early. Surprises create resistance; previews create buy-in.
- Acknowledge what is being lost, not just what is being gained
- "Everyone" is not a stakeholder. "200 users in the billing team" is.

**Gate**: All plan components complete. Rollback plan has trigger criteria. Approvals identified.

**Phase 3: EXECUTE** -- Monitor adoption and sustain.

- Track adoption metrics
- Address resistance (specific actions, not "manage change")
- Reinforce new behaviors
- Document lessons learned
- Define success criteria and measurement timeline

**Gate**: Adoption metrics defined. Lessons captured. Success criteria measurable.

---

### Mode: CAPACITY

**Framework**: INVENTORY -> FORECAST -> DECIDE

**Phase 1: INVENTORY** -- Map current capacity.

- List team members, roles, and current allocation
- Calculate actual available hours (subtract meetings, PTO, on-call, admin)
- Map current work to people

| Role Type | Target Utilization | Rationale |
|-----------|-------------------|-----------|
| IC / Specialist | 75-80% | Buffer for reactive work and growth |
| Manager | 60-70% | Management overhead, 1:1s, meetings |
| On-call / Support | 50-60% | Interrupt-driven work is unpredictable |

**Gate**: Current capacity mapped. Utilization calculated. Overallocations identified.

**Phase 2: FORECAST** -- Model upcoming demand.

- List upcoming projects with resource requirements and timelines
- Identify skill bottlenecks (the constraint is usually a specific skill, not generic headcount)
- Model scenarios: do nothing, hire X, deprioritize Y, contract Z

**Gate**: Demand mapped. Bottlenecks identified. Scenarios modeled.

**Phase 3: DECIDE** -- Recommend action.

- Compare scenarios: outcome, cost, timeline, risk
- Recommend: hire, contract, reprioritize, delay, or split
- Preserve buffer capacity for unplanned work (target 75-80%). 100% means no buffer for surprises.

**Gate**: Recommendation stated. Trade-offs explicit. Buffer preserved.

---

### Mode: COMPLIANCE

**Framework**: MAP -> GAP -> REMEDIATE

**Phase 1: MAP** -- Identify applicable frameworks and current state.

| Framework | Focus | Key Requirements |
|-----------|-------|-----------------|
| SOC 2 | Service organizations | Security, availability, processing integrity, confidentiality, privacy |
| ISO 27001 | Information security | Risk assessment, security controls, continuous improvement |
| GDPR | Data privacy (EU) | Consent, data rights, breach notification, DPO |
| HIPAA | Healthcare (US) | PHI protection, access controls, audit trails |
| PCI DSS | Payment card data | Encryption, access control, vulnerability management |

- Inventory controls mapped to framework requirements
- Document control owners and evidence locations

**Gate**: Frameworks identified. Controls inventoried.

**Phase 2: GAP** -- Find what is missing or deficient.

Load `references/risk-assessment.md` for risk-based prioritization of gaps.

- Requirements vs. current state for each control
- Evidence gaps: what evidence is needed but not collected
- Priority: compliance risk x remediation effort

**Gate**: Gaps identified and prioritized. Evidence gaps documented.

**Phase 3: REMEDIATE** -- Plan and track closure.

- Remediation plan with owner, timeline, and verification method
- Audit calendar with evidence collection deadlines
- Monitoring: control effectiveness tracking

**Gate**: Remediation plan complete. Audit calendar set. Owners assigned.

---

### Mode: STATUS

**Framework**: GATHER -> SYNTHESIZE -> DELIVER

Produce a status report covering:

| Section | Content |
|---------|---------|
| Executive Summary | 3-4 sentences. What is on track, what needs attention, key wins. |
| Overall Status | On Track / At Risk / Off Track with justification |
| Key Metrics | KPI, target, actual, trend, status |
| Accomplishments | What got done this period |
| In Progress | Item, owner, status, ETA |
| Risks and Issues | Risk, impact, mitigation, owner |
| Decisions Needed | Decision, context, deadline, recommendation |
| Next Priorities | Top 3 for next period |

Rules:
- Lead with the headline. Leadership reads the first 3 lines.
- Be honest about risks. Surfacing issues early builds trust. Surprises erode it.
- For each decision needed, provide context AND a recommendation. Include a recommendation with every decision request.

---

### Mode: OPTIMIZE

**Framework**: MAP -> ANALYZE -> REDESIGN

**Phase 1: MAP** -- Document current state with timing.

Load `references/process-documentation.md`.

- Every step, decision point, and handoff with time estimates
- Identify: who, what, how long, what triggers, what blocks

**Phase 2: ANALYZE** -- Identify waste.

| Waste Type | What to Look For |
|-----------|-----------------|
| Waiting | Time in queues, waiting for approvals |
| Rework | Steps that fail and repeat |
| Handoffs | Each handoff = potential failure/delay point |
| Over-processing | Steps that add no value |
| Manual work | Tasks that could be automated |

**Phase 3: REDESIGN** -- Propose improvements.

- Eliminate unnecessary steps
- Automate where deterministic
- Reduce handoffs
- Parallelize independent steps
- Before/after comparison with: time saved, error rate reduction, cost savings

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Vague runbook steps | LLM defaults to abstract language | Force each step through the 5-component template. Reject steps without exact commands. |
| Underestimated risk | Optimism bias in probability scoring | Challenge every "Low" probability. Ask: "What evidence supports Low, not Medium?" |
| Generic process docs | Template fill without reality check | Ask how the process actually works today, not how it should work. |
| Missing rollback | Assumed success path only | Require rollback before marking any change/runbook complete. |
| Scorecard inflation | All vendors score 7+ | Force relative scoring. At least one dimension per vendor must be below 5. |
| RACI with multiple As | Accountability diffusion | Enforce exactly one A per step. Multiple As = no one accountable. |
| Compliance checkbox theater | Controls documented but not tested | Require evidence of control effectiveness, not just existence. |

---

## Reference Loading Table

| Mode | Reference | Content |
|------|-----------|---------|
| RUNBOOK | `references/runbook-authoring.md` | Step structure, verification checklists, rollback procedures, escalation paths |
| RISK, COMPLIANCE | `references/risk-assessment.md` | Probability x impact matrix, risk categories, mitigation planning, residual risk tracking |
| VENDOR | `references/vendor-management.md` | Vendor scorecard, due diligence checklist, contract review triggers, performance monitoring |
| PROCESS, CAPACITY, OPTIMIZE | `references/process-documentation.md` | Process mapping, RACI matrices, bottleneck analysis, optimization methodology |
| CHANGE | `references/change-management.md` | Change request workflows, impact assessment, stakeholder communication, rollback criteria |
| ALL | `references/llm-ops-failure-modes.md` | LLM failure patterns in operations: vague procedures, underestimated risks, generic templates |
