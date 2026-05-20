---
name: onboarding-orchestrator
description: Design and execute customer onboarding playbooks with milestones, success metrics, and automated touchpoints
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Onboarding Orchestrator

> Create structured onboarding programs that drive rapid time-to-value through milestone-based playbooks, proactive touchpoints, and early success metrics.

## When to Use This Skill

- Designing new onboarding programs
- Improving existing onboarding metrics
- Creating segment-specific playbooks
- Automating onboarding touchpoints
- Measuring onboarding effectiveness

## Methodology Foundation

Based on **Lincoln Murphy's First Value Delivery** and **Gainsight Onboarding Best Practices**, focusing on:
- Time to First Value (TTFV)
- Milestone-based progression
- Success criteria definition
- Risk identification during ramp

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs milestone frameworks | Implementation timeline |
| Creates touchpoint schedules | Resource allocation |
| Identifies success metrics | Definition of "success" |
| Suggests automation triggers | Tool selection |
| Builds playbook templates | Customization per segment |

## Instructions

### Step 1: Define Onboarding Phases

**Standard 4-Phase Model:**

| Phase | Duration | Focus | Exit Criteria |
|-------|----------|-------|---------------|
| **Kickoff** | Week 1 | Alignment, access | Kickoff complete, logins work |
| **Setup** | Week 2-3 | Configuration | Core setup done |
| **Adoption** | Week 4-6 | First use case | TTFV achieved |
| **Optimization** | Week 7-12 | Full rollout | Steady state reached |

### Step 2: Map Milestones per Phase

**Kickoff Milestones:**
- [ ] Kickoff call completed
- [ ] Success criteria documented
- [ ] Admin account created
- [ ] Integration requirements identified
- [ ] Timeline agreed

**Setup Milestones:**
- [ ] Technical setup complete
- [ ] Data migration (if needed)
- [ ] Integrations connected
- [ ] User accounts provisioned
- [ ] Admin trained

**Adoption Milestones:**
- [ ] First workflow created
- [ ] 50% users logged in
- [ ] First value moment achieved
- [ ] End user training complete
- [ ] Champion identified

**Optimization Milestones:**
- [ ] 80% users active
- [ ] Full use case deployed
- [ ] Self-service adoption
- [ ] QBR scheduled
- [ ] Expansion discussed

### Step 3: Design Touchpoint Cadence

| Day | Type | Purpose | Owner |
|-----|------|---------|-------|
| 0 | Email | Welcome + next steps | Auto |
| 1 | Call | Kickoff call | CSM |
| 3 | Email | Setup checklist | Auto |
| 7 | Call | Setup review | CSM |
| 14 | Email | Training resources | Auto |
| 21 | Call | Adoption check-in | CSM |
| 30 | Email | 30-day survey | Auto |
| 45 | Call | Value review | CSM |
| 60 | Email | Optimization tips | Auto |
| 90 | Call | QBR/Health check | CSM |

### Step 4: Define Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to Kickoff | <3 days | Contract → Kickoff |
| Time to Setup | <14 days | Kickoff → Setup complete |
| Time to First Value | <30 days | Contract → First use case |
| 30-day activation | >70% | Users logged in |
| 60-day adoption | >50% | Users weekly active |
| Onboarding CSAT | >4.5 | Survey score |
| Onboarding NPS | >50 | Survey score |

## Examples

### Example 1: B2B SaaS Onboarding Playbook

**Output:**
```
## Customer Onboarding Playbook: Enterprise Segment

### Overview
- **Segment**: Enterprise ($100K+ ARR)
- **Target TTFV**: 45 days
- **CSM:Account Ratio**: 1:15
- **Onboarding Duration**: 90 days

---

### Phase 1: Kickoff (Days 0-7)

**Objectives:**
- Establish relationship and trust
- Align on success criteria
- Set expectations and timeline

**Milestones:**
| Milestone | Owner | Day | Status |
|-----------|-------|-----|--------|
| Welcome email sent | Auto | 0 | |
| Kickoff scheduled | CSM | 1 | |
| Kickoff call completed | CSM | 3 | |
| Success criteria doc sent | CSM | 4 | |
| Technical requirements gathered | CSM | 5 | |
| Project plan shared | CSM | 7 | |

**Kickoff Call Agenda (60 min):**
1. Introductions (5 min)
2. Business objectives (15 min)
3. Success criteria definition (15 min)
4. Technical overview (10 min)
5. Timeline and milestones (10 min)
6. Q&A and next steps (5 min)

**Success Criteria Template:**
```markdown
## [Customer] Success Criteria

**Business Objectives:**
1. [Primary goal]
2. [Secondary goal]

**Success Metrics:**
| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| [Metric 1] | X | Y | 90 days |

**Key Stakeholders:**
| Name | Role | Involvement |
|------|------|-------------|

**Risks/Dependencies:**
-
```

**Exit Criteria → Phase 2:**
- [ ] Kickoff call complete
- [ ] Success criteria documented and signed off
- [ ] Technical requirements understood
- [ ] Project timeline agreed

---

### Phase 2: Setup (Days 8-21)

**Objectives:**
- Complete technical implementation
- Configure product for use case
- Provision and train admins

**Milestones:**
| Milestone | Owner | Day | Status |
|-----------|-------|-----|--------|
| SSO/Auth configured | Tech | 10 | |
| Core integration connected | Tech | 12 | |
| Data migration complete | Tech | 14 | |
| Admin accounts created | CSM | 14 | |
| Admin training session | CSM | 16 | |
| Setup review call | CSM | 21 | |

**Setup Check-In Call (Day 14, 30 min):**
1. Progress review (10 min)
2. Blocker resolution (10 min)
3. Admin training preview (5 min)
4. Next steps (5 min)

**Admin Training Agenda (60 min):**
1. Platform overview (15 min)
2. User management (15 min)
3. Core workflows (20 min)
4. Reporting basics (10 min)

**Exit Criteria → Phase 3:**
- [ ] Technical setup 100% complete
- [ ] At least 1 admin trained
- [ ] Users provisioned
- [ ] No open blockers

---

### Phase 3: Adoption (Days 22-45)

**Objectives:**
- Achieve first value moment
- Drive user adoption
- Establish usage patterns

**Milestones:**
| Milestone | Owner | Day | Status |
|-----------|-------|-----|--------|
| End user training scheduled | CSM | 22 | |
| First training session | CSM | 25 | |
| First workflow live | Customer | 28 | |
| 50% users logged in | - | 30 | |
| First value achieved | - | 35 | |
| Adoption review call | CSM | 45 | |

**End User Training (60 min per session):**
- Session 1: Core functionality
- Session 2: Advanced features
- Session 3: Best practices

**First Value Checklist:**
- [ ] Primary use case configured
- [ ] First real work completed
- [ ] Customer confirms value
- [ ] Quote-worthy moment captured

**30-Day Survey:**
```
1. How easy was onboarding? (1-5)
2. Did you achieve your first goal? (Y/N)
3. What could we improve?
4. NPS: How likely to recommend? (0-10)
```

**Exit Criteria → Phase 4:**
- [ ] First value moment achieved
- [ ] 50%+ users logged in
- [ ] No critical blockers
- [ ] Customer confirms progress

---

### Phase 4: Optimization (Days 46-90)

**Objectives:**
- Full use case deployment
- Drive to steady-state adoption
- Prepare for ongoing success

**Milestones:**
| Milestone | Owner | Day | Status |
|-----------|-------|-----|--------|
| Second use case identified | CSM | 50 | |
| Full team rollout | Customer | 60 | |
| 80% adoption achieved | - | 75 | |
| QBR scheduled | CSM | 80 | |
| Handoff to ongoing success | CSM | 90 | |

**60-Day Check-In (30 min):**
1. Adoption metrics review (10 min)
2. Value realization check (10 min)
3. Expansion opportunities (5 min)
4. Ongoing cadence (5 min)

**90-Day QBR Handoff:**
- Full value review
- Health score baseline
- Ongoing success plan
- Expansion discussion

---

### Automation Triggers

| Trigger | Action | Timing |
|---------|--------|--------|
| Contract signed | Welcome email | Immediate |
| Day 3, no kickoff | Alert CSM | Day 3 |
| Setup incomplete | Nudge email | Day 18 |
| Day 30, <25% login | Risk alert | Day 30 |
| First value achieved | Celebration email | On event |
| Day 45, low adoption | Intervention call | Day 45 |

---

### Risk Indicators

| Signal | Risk Level | Response |
|--------|------------|----------|
| No kickoff by Day 5 | 🟠 High | Escalate internally |
| Setup blocked >7 days | 🟠 High | Technical escalation |
| <25% login at Day 30 | 🔴 Critical | Intervention call |
| Champion disengaged | 🟠 High | Find alternate contact |
| No first value by Day 45 | 🔴 Critical | Executive involvement |
```

## Skill Boundaries

### What This Skill Does Well
- Structuring onboarding programs
- Defining milestones and metrics
- Creating touchpoint schedules
- Building playbook templates

### What This Skill Cannot Do
- Know your specific product setup
- Execute onboarding automatically
- Replace customer relationship skills
- Predict implementation blockers

### When to Escalate to Human
- Technical implementation issues
- Customer relationship problems
- Scope changes or delays
- Executive involvement needs

## References

- Lincoln Murphy's Customer Success Onboarding
- Gainsight Onboarding Best Practices
- Totango Time to First Value Guide
- ChurnZero Onboarding Automation

## Related Skills

- `account-health` - Post-onboarding health
- `churn-prediction` - Onboarding risk signals
- `expansion-signals` - Early expansion opportunities

## Skill Metadata

- **Domain**: Customer Success
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 2-4 hours for playbook design
- **Prerequisites**: Product knowledge, segment definitions
