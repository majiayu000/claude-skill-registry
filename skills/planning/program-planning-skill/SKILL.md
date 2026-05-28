---
skill: 'program-planning'
version: '2.0.0'
updated: '2025-12-31'
category: 'organizational'
complexity: 'advanced'
prerequisite_skills: []
composable_with:
  - 'milestone-tracking'
  - 'stakeholder-management'
  - 'risk-assessment'
  - 'change-management'
---

# Program Planning Skill

## Overview
Expertise in creating and executing vendor replacement programs using the proven 30-60-90 day framework, including milestone planning, resource allocation, dependency management, and phase gate governance.

## Core Framework: 30-60-90 Day Planning

### Phase Structure

**Phase 1: Planning & Preparation (Days 1-30)**
- **Focus:** Build foundation, make decisions, prepare for action
- **Key Activities:** Business case, tool selection, team prep, risk assessment
- **Deliverables:** Approved plan, selected tools, trained pilot team, baseline metrics
- **Success Criteria:** Executive approval, budget allocated, team ready

**Phase 2: Pilot & Validation (Days 31-60)**
- **Focus:** Prove the approach works with real projects
- **Key Activities:** Pilot execution, metrics tracking, vendor comparison, validation
- **Deliverables:** Quality data, cost validation, Go/No-Go decision
- **Success Criteria:** Quality ≥90% vendor, cost validated, team satisfied

**Phase 3: Transition & Scale (Days 61-90)**
- **Focus:** Full rollout and vendor cutover
- **Key Activities:** Team training, vendor wind-down, cutover, optimization
- **Deliverables:** Full deployment, vendor exit, success validation
- **Success Criteria:** Production live, vendor exited, ROI achieved

### Planning Principles

1. **Start with the End:** Define success criteria before planning
2. **Phase Gates:** Clear go/no-go decisions between phases
3. **Risk-Based:** Identify and mitigate risks proactively
4. **Iterative:** Adjust plan based on learnings
5. **Stakeholder-Driven:** Align with stakeholder needs and constraints
6. **Measurable:** Track progress with objective metrics
7. **Realistic:** Buffer for unknowns and learning curves
8. **Documented:** Write everything down, share widely

## Program Planning Process

### Step 1: Program Charter Development

**Program Charter Template:**
```markdown
# Vendor Replacement Program Charter

## Program Overview
**Name:** [Program Name]
**Sponsor:** [Executive Sponsor Name, Title]
**Manager:** [Program Manager Name]
**Duration:** [Start Date] - [End Date] (90 days)
**Budget:** $[Amount]

## Business Case
**Problem:** [Vendor pain points and costs]
**Solution:** [AI-augmented team approach]
**Expected Benefits:**
- Cost reduction: [X]% ($[Y]/year)
- Productivity gain: [X]x multiplier
- Quality improvement: [Metrics]
- Strategic value: [IP retention, flexibility, etc.]

## Scope

**In Scope:**
- [Function 1 - e.g., backend development]
- [Function 2 - e.g., API development]
- [Team size - e.g., 5 FTEs]

**Out of Scope:**
- [Function 3 - e.g., frontend development - future phase]
- [Constraint 1 - e.g., production support (vendor retained)]

**Success Criteria:**
- Phase 1: Executive approval, tools selected, team ready
- Phase 2: Pilot quality ≥90% vendor, cost validated
- Phase 3: Production live, vendor exited, 60% cost reduction

## Stakeholders
**Executive Sponsor:** [Name] - Budget approval, strategic decisions
**R&D Leadership:** [Name] - Team allocation, technical decisions
**Finance:** [Name] - Budget tracking, ROI validation
**Security/Compliance:** [Name] - Risk assessment, approval
**Vendor Account Manager:** [Name] - Transition coordination

## Assumptions
1. Executive budget approved by [date]
2. Pilot team available full-time for weeks 5-8
3. Vendor will cooperate with 90-day notice
4. No major production incidents during cutover
5. AI tools perform as demonstrated in POCs

## Constraints
1. Budget: $[X] maximum
2. Timeline: Must complete by [date] (fiscal year end)
3. Resources: 5 FTEs available, no new hires
4. Vendor contract: 90-day notice required
5. Risk tolerance: No production downtime acceptable

## Governance
- **Steering Committee:** [Members] - Monthly reviews
- **Program Team:** [Core members] - Weekly meetings
- **Phase Gates:** Day 30, Day 60, Day 90
- **Status Reporting:** Weekly to sponsor, monthly to executives
```

### Step 2: Milestone Planning

**Milestone Planning Framework:**
```markdown
## Program Milestones

### Phase 1 Milestones (Days 1-30)

**M1.1: Program Kickoff (Day 1)**
- Executive sponsor approval
- Program team assembled
- Communication plan launched

**M1.2: Business Case Complete (Day 7)**
- Executive presentation delivered
- Financial model finalized
- Board approval (if required)

**M1.3: Tool Selection (Day 14)**
- Evaluation completed
- Security cleared
- Procurement initiated

**M1.4: Pilot Team Ready (Day 21)**
- Team identified and committed
- Training curriculum complete
- Baseline metrics established

**M1.5: Phase Gate 1 (Day 30)**
- All deliverables complete
- Executive go-decision
- Pilot launch authorized

### Phase 2 Milestones (Days 31-60)

**M2.1: Pilot Launch (Day 31)**
- Tools deployed
- Team trained
- First project started

**M2.2: Parallel Run Start (Day 35)**
- Vendor and AI outputs being compared
- Metrics dashboard live
- Daily tracking initiated

**M2.3: Mid-Pilot Review (Day 45)**
- Preliminary results analyzed
- Issues addressed
- Plan adjustments made

**M2.4: Pilot Complete (Day 53)**
- All pilot projects finished
- Final metrics collected
- Team feedback gathered

**M2.5: Phase Gate 2 (Day 60)**
- Go/No-Go decision
- Full rollout approved
- Vendor transition plan finalized

### Phase 3 Milestones (Days 61-90)

**M3.1: Full Team Training (Day 65)**
- All team members trained
- Tools deployed organization-wide
- Support structure in place

**M3.2: Vendor Transition Start (Day 70)**
- Contract wind-down initiated
- Knowledge transfer executing
- Parallel run continuing

**M3.3: Cutover Ready (Day 80)**
- Knowledge transfer complete
- Quality parity achieved
- Cutover approved

**M3.4: Production Cutover (Day 85)**
- Vendor contract concluded
- Full internal operation
- Monitoring intensive

**M3.5: Phase Gate 3 / Program Close (Day 90)**
- Success metrics validated
- ROI achieved
- Program closed
```

### Step 3: Dependency Mapping

**Dependency Types:**
1. **Finish-to-Start (FS):** Task B can't start until Task A finishes
2. **Start-to-Start (SS):** Task B can't start until Task A starts
3. **Finish-to-Finish (FF):** Task B can't finish until Task A finishes
4. **Start-to-Finish (SF):** Task B can't finish until Task A starts (rare)

**Critical Path Analysis:**
```markdown
## Critical Path: Longest Dependent Chain

Day 1-7: Business Case → Budget Approval [CRITICAL]
  ↓
Day 8-14: Tool Selection → Security Clearance [CRITICAL]
  ↓
Day 15-21: Procurement → Tool Deployment [CRITICAL]
  ↓
Day 22-30: Training → Pilot Launch [CRITICAL]
  ↓
Day 31-60: Pilot Execution → Validation [CRITICAL]
  ↓
Day 61-70: Full Training → Team Readiness [CRITICAL]
  ↓
Day 71-85: Vendor Transition → Cutover [CRITICAL]

**Total Critical Path: 85 days**
**Buffer: 5 days**

Any delay on critical path delays entire program.
Non-critical tasks (e.g., documentation, case study) have slack.
```

### Step 4: Resource Allocation

**Resource Planning Template:**
```markdown
## Resource Allocation Plan

### Core Program Team (Full-time)
- **Program Manager:** 1 FTE × 90 days = 90 person-days
- **Change Manager:** 0.5 FTE × 90 days = 45 person-days
- **Technical Lead:** 0.5 FTE × 60 days = 30 person-days
**Total Core:** 165 person-days

### Pilot Team (Phase 2: Days 31-60)
- **Developers:** 5 FTE × 30 days = 150 person-days
- **QA/Validation:** 2 FTE × 30 days = 60 person-days
**Total Pilot:** 210 person-days

### Full Team (Phase 3: Days 61-90)
- **All Team Members:** 20 FTE × 30 days = 600 person-days
- **Training time (20%):** 120 person-days
- **Productive time (80%):** 480 person-days

### Support Resources (Part-time)
- **Executive Sponsor:** 2 hours/week × 12 weeks = 24 hours
- **Security/Compliance:** 8 hours/month × 3 months = 24 hours
- **Legal:** 16 hours (contract review)
- **Finance:** 8 hours (ROI tracking)

### External Resources
- **Vendor Transition:** Vendor team cooperation (no cost)
- **Tool Vendor Support:** Included in licensing
- **External Consultant (optional):** 40 hours @ $200/hr = $8,000
```

### Step 5: Budget Planning

**Program Budget Template:**
```markdown
## Program Budget

### AI Tools & Technology
- GitHub Copilot: 20 users × $39/mo × 3 mo = $2,340
- GPT-4 API: $500/month × 3 months = $1,500
- Infrastructure: $300/month × 3 months = $900
**Subtotal Technology:** $4,740

### Training & Enablement
- Training curriculum development: 80 hours @ $150/hr = $12,000
- Training delivery (workshops): $5,000
- Training materials and resources: $2,000
**Subtotal Training:** $19,000

### Transition & Knowledge Transfer
- Vendor knowledge transfer sessions: Included in contract
- Documentation sprint: 40 hours @ $100/hr = $4,000
- Parallel run costs (overlapping): $10,000
**Subtotal Transition:** $14,000

### Program Management
- Program Manager: 90 days @ $1,000/day = $90,000
- Change Manager: 45 days @ $800/day = $36,000
- Technical Lead: 30 days @ $1,200/day = $36,000
**Subtotal Management:** $162,000

### Contingency & Buffer
- Risk buffer (10%): $19,974
- Scope change reserve: $10,000
**Subtotal Contingency:** $29,974

**TOTAL PROGRAM BUDGET: $229,714**

### Cost Avoidance (Savings)
- Vendor costs avoided (3 months): $120,000
- **Net Cost Year 1:** $109,714
- **Savings Year 1 (months 4-12):** $360,000
- **Year 1 ROI:** 228%
```

## Phase Gate Governance

### Phase Gate Purpose
- **Ensure readiness** before proceeding to next phase
- **Validate assumptions** and adjust plans
- **Obtain approvals** for continued investment
- **Identify and mitigate risks** early
- **Prevent costly mistakes** from proceeding when not ready

### Phase Gate Process

**1. Gate Preparation (1 week before)**
- Program Manager compiles evidence
- All deliverables finalized
- Metrics and data validated
- Stakeholder pre-briefings

**2. Gate Assessment (Gate day)**
- Criteria scorecard review
- Evidence presentation
- Stakeholder Q&A
- Risk review
- Decision discussion

**3. Gate Decision**
- **PASS:** Proceed to next phase as planned
- **CONDITIONAL PASS:** Proceed with specific conditions to address
- **DELAY:** Address critical gaps before proceeding
- **CANCEL:** Abort program (rare, but possible)

**4. Post-Gate Actions**
- Document decision and rationale
- Communicate to all stakeholders
- Update plan based on conditions or delays
- Kick off next phase

### Gate Criteria Examples

**Phase Gate 1 Criteria:**
```markdown
| Criterion | Weight | Target | Evidence Required |
|-----------|--------|--------|-------------------|
| Executive approval | 20% | Signed charter | Approval email/signature |
| Budget allocated | 20% | $[X] committed | Finance confirmation |
| Tools selected | 15% | 2+ options evaluated | Evaluation scorecard |
| Security cleared | 15% | No red flags | Security signoff |
| Team ready | 15% | 5 trained | Training completion % |
| Baseline metrics | 10% | Defined and measured | Metrics dashboard |
| Risk mitigation | 5% | Plans for top 5 risks | Risk register |

**Pass Criteria:** ≥85% weighted score, no individual criterion <50%
```

## Common Planning Pitfalls

### Pitfall 1: Unrealistic Timeline
**Problem:** Trying to do 90-day program in 60 days
**Why it fails:** Corners cut, quality suffers, team burns out
**How to avoid:** Use proven 30-60-90 framework, buffer for unknowns

### Pitfall 2: Insufficient Planning Time
**Problem:** Rushing into pilot without adequate preparation
**Why it fails:** Missing foundation, poor tool selection, team unready
**How to avoid:** Spend full 30 days on Phase 1, don't skip

### Pitfall 3: Vague Success Criteria
**Problem:** "Improve productivity" without specific targets
**Why it fails:** Can't measure success, stakeholders disagree on outcomes
**How to avoid:** Quantify everything (≥90% quality, 60% cost reduction, etc.)

### Pitfall 4: Ignoring Change Management
**Problem:** Treating as purely technical program
**Why it fails:** Team resistance, adoption failure, quality issues
**How to avoid:** Dedicate resources to training, communication, support

### Pitfall 5: No Risk Management
**Problem:** Assuming everything will go as planned
**Why it fails:** Surprises cause delays, cost overruns, failures
**How to avoid:** Identify risks early, mitigate proactively, monitor continuously

### Pitfall 6: Poor Stakeholder Management
**Problem:** Executives surprised by issues, Finance questions costs
**Why it fails:** Loss of support, budget challenges, program cancellation
**How to avoid:** Weekly reports, transparent communication, early escalation

### Pitfall 7: Inadequate Knowledge Transfer
**Problem:** Rushing vendor exit to save money
**Why it fails:** Critical knowledge lost, team struggles, quality drops
**How to avoid:** Allocate 4-6 weeks for thorough knowledge transfer

### Pitfall 8: Skipping Parallel Run
**Problem:** Cutting directly from vendor to AI
**Why it fails:** No validation, quality unknown, high risk
**How to avoid:** Minimum 3-4 week parallel run for comparison

## Program Planning Checklist

### Initial Planning
- [ ] Program charter drafted and approved
- [ ] Success criteria defined (quantified)
- [ ] Stakeholders identified and mapped
- [ ] Budget estimated and approved
- [ ] Timeline baselined (30-60-90 days)
- [ ] Risks identified (top 10)
- [ ] Governance structure defined

### Detailed Planning
- [ ] All milestones defined with dates
- [ ] Dependencies mapped
- [ ] Critical path identified
- [ ] Resources allocated (names, not just roles)
- [ ] Budget breakdown by category
- [ ] Phase gate criteria defined
- [ ] Communication plan complete

### Execution Preparation
- [ ] Tracking tools set up (dashboards, reports)
- [ ] Kickoff meeting scheduled
- [ ] Team roles and responsibilities clear
- [ ] Escalation paths defined
- [ ] Change control process established
- [ ] Quality standards documented
- [ ] Lessons learned process defined

## Tools and Templates

**Program Management Tools:**
- **Gantt Chart:** Microsoft Project, Monday.com, Asana
- **Kanban Board:** Jira, Trello, Linear
- **Dashboards:** Tableau, Looker, Excel
- **Communication:** Slack, Teams, Email
- **Documentation:** Confluence, Notion, Google Docs

**Essential Templates:**
- Program charter
- 30-60-90 day plan (Excel/Google Sheets)
- Weekly status report
- Phase gate assessment
- Risk register
- RACI matrix (Responsible, Accountable, Consulted, Informed)
- Milestone schedule
- Budget tracker

## Success Metrics

**Program Execution:**
- Timeline adherence: Within 2 weeks of 90-day plan
- Budget adherence: Within 10% of approved budget
- Deliverable completion: >95% on time and quality
- Phase gates: All passed (first time or conditional)

**Stakeholder Satisfaction:**
- Executive sponsor: ≥4/5 rating
- Team members: ≥4/5 rating
- Program team: ≥4/5 rating

**Business Outcomes:**
- Cost reduction: Achieved or exceeded target
- Productivity gain: Achieved or exceeded target
- Quality maintenance: ≥95% of baseline
- ROI: Positive in Year 1

This skill ensures programs are properly planned, resourced, and governed for maximum success probability.
