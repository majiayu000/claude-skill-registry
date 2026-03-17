---
name: portfolio-helpdesk-sprint
description: "Run a time-boxed portfolio support sprint with triage, SLAs, and outcome tracking. Use when multiple requests come in and you need repeatable execution with gates."
license: Proprietary
compatibility: Works offline; improved with operator network; Salesforce logging recommended.
metadata:
  author: evalops
  version: "0.2"
---
# Portfolio helpdesk sprint

## When to use
Use this skill when:
- Portfolio support requests are coming in continuously
- You need a triage system and SLA-like execution
- You want to measure whether support actually helped
- Running a dedicated "support week" or "office hours" sprint

## Inputs you should request (only if missing)
- Sprint duration (1 day, 1 week)
- Request backlog (all open requests)
- Capacity constraints (hours available)
- Company context (stage, priorities) for each request

## Outputs you must produce
1) **Prioritized queue** (P0/P1/P2 with SLAs)
2) **Daily action plan** (owner, deliverable, deadline)
3) **Delivered help** with outcome tracking
4) **Sprint summary** with metrics

**Every sprint ends with:** Metrics report + next sprint priorities + help menu updates.

## Triage rubric

| Priority | Definition | Response SLA | Resolution SLA |
|---|---|---|---|
| P0 | Urgent: fundraising, key hire closing, customer escalation | 4 hours | 48 hours |
| P1 | Important: hiring pipeline, customer intros, partner intros | 24 hours | 1 week |
| P2 | Useful: market intel, light strategy review | 48 hours | 1 week |

**Triage criteria:**
- P0 if: Revenue at risk, funding at risk, or executive hire decision pending
- P1 if: Advances a stated quarterly priority
- P2 if: Helpful but not on critical path

## 5-day sprint structure

### Day 0: Setup + triage (2 hours)
**Deliverables:**
- All requests logged and prioritized
- SLAs assigned
- Owners assigned
- Capacity allocated

**Gate:** Is the queue triaged and achievable in the sprint? If not, deprioritize P2s or extend timeline.

### Day 1: P0 execution
**Focus:** All P0 requests get first response and action started
**Deliverables:**
- P0 requests responded to
- First actions taken (intros requested, candidates identified, materials reviewed)
- Blockers identified

**End of day check:**
| Request | Responded? | Action taken? | Blocked? |
|---|---|---|---|
| | | | |

### Day 2: P0 resolution + P1 start
**Focus:** Close P0s, start P1s
**Deliverables:**
- P0 requests resolved or on clear path
- P1 requests responded to
- Intros sent, candidates submitted

**Gate:** Are P0s resolved or blocked with escalation path?

### Day 3: P1 execution
**Focus:** Execute on P1 requests
**Deliverables:**
- Customer intros made
- Recruiting pipelines built
- Partner outreach sent

**Tracking:**
| Request | Action | Outcome | Next step |
|---|---|---|---|

### Day 4: P1 resolution + P2 start
**Focus:** Close P1s, start P2s
**Deliverables:**
- P1 requests resolved or on clear path
- P2 requests responded to
- Follow-ups sent on all pending intros

### Day 5: Close out + metrics
**Focus:** Resolve remaining, measure outcomes
**Deliverables:**
- All requests resolved or explicitly deferred
- Outcomes documented for each
- Sprint metrics calculated
- Help menus updated
- Next sprint priorities identified

## Daily standup format (15 min)

1. **Yesterday:** What was delivered?
2. **Today:** What will be delivered?
3. **Blockers:** What's stuck and needs help?
4. **Metrics check:** On track for SLAs?

## Sprint metrics (calculate at end)

| Metric | Target | Actual |
|---|---|---|
| P0 response SLA hit | 100% | |
| P0 resolution SLA hit | 90% | |
| P1 response SLA hit | 90% | |
| P1 resolution SLA hit | 80% | |
| Overall success rate | 70% | |
| High-impact outcomes | 30% | |
| Requests completed | | |
| Requests deferred | | |
| Intros -> meetings | 60% | |

## Request tracking template

| ID | Company | Type | Priority | Request | "Done" looks like | Owner | Due | Status | Outcome | Impact |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | P0/P1/P2 | | | | | Open/Done/Deferred | Success/Partial/Fail | H/M/L |

## Outcome documentation (per request)

```markdown
## Request: [ID] - [Company] - [Type]

### Request
- Goal:
- "Done" looks like:
- Priority:
- SLA:

### Actions taken
1. [Date] [Action] [Result]
2. ...

### Resolution
- Status: Resolved / Deferred / Blocked
- Within SLA: Yes / No
- Outcome: Success / Partial / Failed

### Impact
- Rating: High / Medium / Low
- Evidence:
- Founder feedback:

### Learnings
- What worked:
- What to do differently:
```

## Gates (mandatory checkpoints)

**End of Day 1:**
- All P0s responded to?
- Any P0s blocked without escalation path?

**End of Day 3:**
- All P0s resolved?
- All P1s responded to?
- On track for P1 resolution SLA?

**End of Day 5:**
- All requests resolved or explicitly deferred?
- Metrics calculated?
- Help menus updated?
- Next sprint planned?

## Salesforce logging

- Log each request as a Task on the Account
- Update Task status as you progress
- Log each action (intro, candidate submission) as an Activity
- Tag by support type
- Record outcome and impact when resolved

Use `salesforce-crm-ops` for API patterns.

## Reference
Use `portfolio-support-ops` for deeper playbooks on specific support types (recruiting, customer intros, fundraising).

## Edge cases
- If P0 volume exceeds capacity: Escalate to partner for prioritization or additional help.
- If a request is blocked on external party: Set a reminder, move to "waiting" status, continue with other requests.
- If founder doesn't provide needed info: One reminder, then deprioritize until they respond.
