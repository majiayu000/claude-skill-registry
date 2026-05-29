---
skill: 'milestone-tracking'
version: '2.0.0'
updated: '2025-12-31'
category: 'program-management'
complexity: 'intermediate'
prerequisite_skills: ['document-structure', 'program-planning']
composable_with: ['program-planning', 'stakeholder-management', 'risk-assessment']
---

# Milestone Tracking Skill

## Overview
Expertise in tracking program milestones, deliverables, and dependencies throughout the 30-60-90 day vendor replacement program, ensuring visibility, accountability, and timely completion.

## Core Tracking Framework

### Milestone Components

**Essential Elements:**
1. **Name:** Clear, action-oriented description
2. **Owner:** Single person accountable
3. **Due Date:** Specific date (not "end of month")
4. **Success Criteria:** How you know it's complete
5. **Dependencies:** What must finish first
6. **Status:** Not Started | In Progress | At Risk | Complete | Blocked
7. **% Complete:** Quantified progress
8. **Notes:** Context, issues, changes

### Milestone Status Definitions

**🔵 Not Started (0%)**
- Work has not begun
- Resources not yet assigned
- Prerequisites not met

**🟡 In Progress (1-99%)**
- Work actively underway
- On track to meet deadline
- No major blockers

**🟠 At Risk (1-99%)**
- Behind schedule
- Quality concerns
- Resource constraints
- External dependencies delayed

**🔴 Blocked (0-99%)**
- Cannot proceed
- Waiting on external input/decision
- Critical blocker identified
- Requires escalation

**✅ Complete (100%)**
- All success criteria met
- Deliverable accepted
- Sign-off obtained
- Documented

## Tracking Tools and Methods

### Master Milestone Schedule

**Template:**
```markdown
# Vendor Replacement Program - Master Milestone Schedule

**Program:** [Name]
**Version:** [X.X]
**Last Updated:** [Date]
**Program Manager:** [Name]

## Phase 1: Planning & Preparation (Days 1-30)

| ID | Milestone | Owner | Due Date | Status | % | Dependencies | Notes |
|----|-----------|-------|----------|--------|---|--------------|-------|
| 1.1 | Program kickoff complete | PM | Day 1 | ✅ | 100% | None | Completed on time |
| 1.2 | Executive business case approved | Exec Advisor | Day 7 | ✅ | 100% | 1.1 | Board approved |
| 1.3 | Tool evaluation complete | Tool Spec | Day 14 | 🟡 | 85% | 1.2 | Security review pending |
| 1.4 | Pilot team trained | Change Mgr | Day 21 | 🔵 | 0% | 1.3 | Starts next week |
| 1.5 | Phase Gate 1 passed | PM | Day 30 | 🔵 | 0% | 1.1-1.4 | On track |

## Phase 2: Pilot & Validation (Days 31-60)

| ID | Milestone | Owner | Due Date | Status | % | Dependencies | Notes |
|----|-----------|-------|----------|--------|---|--------------|-------|
| 2.1 | Pilot launch | PM | Day 31 | 🔵 | 0% | 1.5 | Dependent on Gate 1 |
| 2.2 | Parallel run start | Vendor Trans | Day 35 | 🔵 | 0% | 2.1 | Vendor notified |
| 2.3 | Mid-pilot review | PM | Day 45 | 🔵 | 0% | 2.2 | Review scheduled |
| 2.4 | Pilot complete | PM | Day 53 | 🔵 | 0% | 2.3 | - |
| 2.5 | Phase Gate 2 passed | PM | Day 60 | 🔵 | 0% | 2.1-2.4 | - |

## Phase 3: Transition & Scale (Days 61-90)

| ID | Milestone | Owner | Due Date | Status | % | Dependencies | Notes |
|----|-----------|-------|----------|--------|---|--------------|-------|
| 3.1 | Full team training complete | Change Mgr | Day 65 | 🔵 | 0% | 2.5 | - |
| 3.2 | Vendor transition started | Vendor Trans | Day 70 | 🔵 | 0% | 2.5 | - |
| 3.3 | Cutover ready | PM | Day 80 | 🔵 | 0% | 3.1, 3.2 | - |
| 3.4 | Production cutover | PM | Day 85 | 🔵 | 0% | 3.3 | - |
| 3.5 | Program closure | PM | Day 90 | 🔵 | 0% | 3.4 | - |

## Summary Statistics

- **Total Milestones:** 15
- **Complete:** 2 (13%)
- **In Progress:** 1 (7%)
- **At Risk:** 0 (0%)
- **Blocked:** 0 (0%)
- **Not Started:** 12 (80%)

**Overall Program Health:** 🟢 On Track
```

### Weekly Milestone Updates

**Update Process:**
1. **Monday:** Program Manager requests updates from all milestone owners
2. **Tuesday:** Owners update status, % complete, notes
3. **Wednesday:** Program Manager reviews, identifies risks
4. **Thursday:** Status report compiled and distributed
5. **Friday:** Steering committee review (if needed)

**Update Email Template:**
```markdown
Subject: Milestone Update Request - Week [X]

Hi [Milestone Owner],

Please update the status of your milestone(s) by EOD Tuesday:

**Your Milestones:**
- [ID]: [Milestone name] - Due: [Date]
  - Current status: [Previous status]
  - Current %: [Previous %]

**Please provide:**
1. Updated status: Not Started | In Progress | At Risk | Complete | Blocked
2. Updated % complete (0-100%)
3. Expected completion date (if changed)
4. Key accomplishments this week
5. Blockers or issues
6. Help needed from me or others

**Template for your response:**
```
Milestone: [ID] [Name]
Status: [Status]
% Complete: [X]%
Expected Complete: [Date]
This Week: [What was accomplished]
Blockers: [Any issues or blockers]
Help Needed: [Support required]
```

Thanks,
[Program Manager]
```

### Dependency Tracking

**Dependency Types and Management:**

**Internal Dependencies (within program):**
```markdown
## Dependency Chain Example

Milestone 1.2: Executive Approval
  ↓ (blocks)
Milestone 1.3: Tool Selection
  ↓ (blocks)
Milestone 1.4: Tool Procurement
  ↓ (blocks)
Milestone 1.5: Tool Deployment
  ↓ (blocks)
Milestone 2.1: Pilot Launch

**If 1.3 delays 3 days:**
- 1.4 delays 3 days
- 1.5 delays 3 days
- 2.1 delays 3 days
- Entire program slips 3 days (on critical path)

**Mitigation:**
- Monitor 1.3 closely (high priority)
- Accelerate 1.4 if possible (parallel procurement)
- Have contingency plan for 1.5 (alternative tools ready)
```

**External Dependencies (outside program control):**
```markdown
## External Dependency Register

| Dependency | Source | Impact | Due Date | Status | Owner | Mitigation |
|------------|--------|--------|----------|--------|-------|------------|
| Budget approval | CFO | High - blocks program | Day 5 | 🟡 At risk | Finance | Backup budget source identified |
| Security clearance | CISO | Medium - blocks Phase 2 | Day 14 | 🟢 On track | Security | Weekly check-ins |
| Vendor cooperation | Vendor PM | High - knowledge transfer | Day 70 | 🟢 Confirmed | Vendor Mgr | Contract clause enforcement |
| Legal contract review | Legal | Low - advisory only | Day 10 | ✅ Complete | Legal | - |

**Escalation Triggers:**
- Any High impact dependency at risk: Escalate immediately
- Any dependency blocked: Escalate within 24 hours
- Any dependency >3 days overdue: Executive escalation
```

## Deliverable Tracking

### Deliverable vs. Milestone

**Milestone:** A significant point in time (approval, decision, event)
- Example: "Executive approval obtained"

**Deliverable:** A tangible work product produced
- Example: "Executive business case presentation"

**Relationship:** Milestones often require deliverables as evidence
- Milestone 1.2: Executive approval obtained
  - Deliverable: Business case presentation (PowerPoint)
  - Deliverable: Financial model (Excel)
  - Deliverable: Risk assessment (Document)

### Deliverable Tracking Template

```markdown
## Deliverable Register

| Del ID | Deliverable | Type | Owner | Due | Status | Quality | Milestone |
|--------|-------------|------|-------|-----|--------|---------|-----------|
| D1.1 | Program charter | Document | PM | Day 1 | ✅ | Approved | M1.1 |
| D1.2 | Business case PPT | Presentation | Exec Adv | Day 6 | ✅ | Approved | M1.2 |
| D1.3 | Financial model | Spreadsheet | ROI Calc | Day 6 | ✅ | Approved | M1.2 |
| D1.4 | Tool scorecard | Spreadsheet | Tool Spec | Day 12 | 🟡 | In review | M1.3 |
| D1.5 | Security assessment | Report | Security | Day 13 | 🟡 | Draft | M1.3 |
| D1.6 | Training curriculum | Document | Change Mgr | Day 18 | 🔵 | Not started | M1.4 |

**Deliverable Status:**
- ✅ Complete and approved
- 🟢 Complete, pending review
- 🟡 In progress
- 🔵 Not started
- 🔴 At risk or blocked

**Quality Gates:**
- Draft: First version, internal review only
- In Review: Shared with stakeholders for feedback
- Approved: Signed off by required approvers
- Final: No further changes expected
```

### Deliverable Quality Checklist

**Before marking deliverable complete:**
- [ ] Meets all requirements in scope
- [ ] Reviewed by at least one other person
- [ ] Approved by required stakeholders (per RACI)
- [ ] Follows template or standards (if applicable)
- [ ] Free of major errors or typos
- [ ] Version numbered and dated
- [ ] Stored in agreed location (SharePoint, Google Drive, etc.)
- [ ] Stakeholders notified of completion

## Dashboard and Visualization

### Executive Dashboard

**Key Metrics to Display:**
```markdown
## Program Dashboard - Week [X]

### Overall Health: 🟢 On Track

### Timeline
- Days elapsed: 15 / 90 (17%)
- Days remaining: 75
- Status: On schedule

### Milestones
- Complete: 2 / 15 (13%)
- In Progress: 3 / 15 (20%)
- At Risk: 0 / 15 (0%)
- Blocked: 0 / 15 (0%)
- Not Started: 10 / 15 (67%)

### Deliverables
- Complete: 3 / 25 (12%)
- In Progress: 5 / 25 (20%)
- Approved: 2 / 3 complete (67%)

### Budget
- Spent: $25K / $230K (11%)
- Status: Under budget by $2K

### Risks
- High: 0
- Medium: 2 (managed)
- Low: 5

### Phase Gates
- Gate 1 (Day 30): On track
- Gate 2 (Day 60): Not yet assessed
- Gate 3 (Day 90): Not yet assessed

### This Week's Focus
1. Complete tool evaluation
2. Security clearance approval
3. Pilot team finalization
```

### Visual Progress Tracking

**Gantt Chart Elements:**
- Milestones (diamonds)
- Tasks/deliverables (bars)
- Dependencies (arrows)
- Critical path (red)
- Today's date (vertical line)
- % complete (fill within bars)
- Resource assignments (labels)

**Burndown Chart:**
- X-axis: Time (weeks 1-12)
- Y-axis: Remaining milestones
- Ideal line (straight diagonal)
- Actual line (shows progress)
- Ahead/behind visualized

## Status Reporting Integration

### Milestone Section in Weekly Status

```markdown
## Milestones Update

### Completed This Week
- ✅ M1.2: Executive business case approved (Day 7)
  - Board approved with no changes
  - Budget allocated: $230K

### In Progress (On Track)
- 🟢 M1.3: Tool evaluation (85% complete)
  - Scorecard complete
  - Security review in progress
  - On track for Day 14

### At Risk
- 🟠 None this week

### Blocked
- 🔴 None this week

### Starting Next Week
- M1.4: Pilot team training
- M1.5: Phase Gate 1 preparation

### Upcoming Critical Dates
- Day 14: Tool selection finalized
- Day 21: Pilot team trained
- Day 30: Phase Gate 1
```

## Common Tracking Pitfalls

### Pitfall 1: Optimistic % Complete
**Problem:** Reporting 90% complete when significant work remains
**Why:** "90% done, 90% to go" syndrome - last 10% takes as long as first 90%
**Solution:** Define clear completion criteria, be honest about remaining work

### Pitfall 2: Ignoring Dependencies
**Problem:** Not tracking what blocks what
**Why:** Delays cascade unexpectedly
**Solution:** Map dependencies explicitly, monitor upstream tasks closely

### Pitfall 3: Infrequent Updates
**Problem:** Only updating status monthly
**Why:** Problems discovered too late to address
**Solution:** Weekly updates minimum, daily for critical milestones

### Pitfall 4: No Owner Accountability
**Problem:** Milestones assigned to "team" not individuals
**Why:** Diffusion of responsibility, no one feels accountable
**Solution:** Single owner per milestone, by name not role

### Pitfall 5: Vague Success Criteria
**Problem:** Unclear what "complete" means
**Why:** Disagreements on whether milestone is truly done
**Solution:** Define specific, measurable completion criteria upfront

### Pitfall 6: Status Hiding
**Problem:** Owners afraid to report "at risk" or "blocked"
**Why:** Shoot-the-messenger culture, problems hidden until crisis
**Solution:** Create psychological safety, reward early escalation

## Tracking Tools

### Simple (Small Programs)
- **Excel/Google Sheets:** Milestone list with formulas
- **Project Management:** Asana, Trello, Monday.com
- **Communication:** Slack, Teams for daily updates

### Advanced (Large Programs)
- **Enterprise PM:** Microsoft Project, Smartsheet, Jira
- **Visualization:** Tableau, PowerBI for dashboards
- **Integration:** API connections between tools
- **Automation:** Zapier for status updates

### Essential Features
- Task/milestone tracking
- Dependency mapping
- Resource assignment
- Status workflows
- Reporting and dashboards
- Collaboration and comments
- Document attachment
- Mobile access

## Best Practices

### Do's ✅
- Update status weekly minimum
- Be honest about risks and blockers
- Escalate early when problems arise
- Celebrate milestone completions
- Keep tracking simple and lightweight
- Focus on critical path
- Communicate changes promptly
- Document assumptions and decisions

### Don'ts ❌
- Update status only when asked
- Hide problems until they're crises
- Let "at risk" become "blocked" without action
- Ignore small delays (they compound)
- Over-engineer tracking (paralysis by analysis)
- Track everything (focus on what matters)
- Change status definitions mid-program
- Forget to communicate completed milestones

## Success Metrics

**Tracking Effectiveness:**
- Update frequency: ≥weekly (100% on time)
- Owner accountability: 100% milestones have named owner
- Dependency visibility: All dependencies documented
- Early warning: Risks identified ≥2 weeks before impact
- Completion accuracy: <5% milestones slip >3 days

**Program Performance:**
- Milestone on-time: ≥90% complete by due date
- Deliverable quality: ≥95% approved first time
- Stakeholder satisfaction: ≥4/5 with tracking visibility
- Decision speed: <48 hours for unblocking decisions

This skill ensures nothing falls through the cracks and stakeholders always know program status.

## Related Skills

- **#program-planning** - Overall program structure and milestones
- **#stakeholder-management** - Communicating milestone status
- **#risk-assessment** - Tracking risks alongside milestones
- **#document-structure** - Status report formatting
