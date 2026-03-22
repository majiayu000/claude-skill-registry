---
name: launch-checklist
description: Comprehensive product launch planning
---

## Quick Start

1. Tell me what you are launching (feature name, PRD link, or description)
2. I check the PRD, past launches, and stakeholder profiles for context
3. I ask about launch type: **Small feature**, **Major launch**, or **Regulatory product**
4. I generate a prioritized checklist with owners, dependencies, and due dates
5. I identify the critical path so you know what cannot slip

**Example:** "Create a launch checklist for the checkout redesign, targeting March 15"

**Output:** Saved to `outputs/launches/[feature-name]-launch-checklist.md`

**Time:** 15-20 minutes to generate, then ongoing tracking

## Purpose

Generate comprehensive launch checklist ensuring nothing falls through the cracks. Covers pre-launch prep, launch execution, and post-launch monitoring.

## Usage

- `/launch-checklist` - Create checklist for a feature/product
- `/launch-checklist [prd-name]` - Create for specific PRD
- `/launch-checklist --template small|major|regulatory` - Use specific template

---

## Context Routing

**Check these files first:**
1. `outputs/prds/` or `context-library/prds/` - PRD for feature details
2. `context-library/launches/` - Past launch checklists (learn from history)
3. `context-library/strategy/` - GTM approach, stakeholders
4. `context-library/stakeholder-*.md` - Who needs to be involved
5. `templates/launch-checklist-template.md` - Base template (if exists)

---

## Workflow

### Step 1: Gather Context

**Read the PRD:**
- Feature scope and complexity
- Success metrics (for post-launch monitoring)
- Rollout plan (A/B test, % rollout, full launch)
- Target launch date
- Stakeholders involved

**Determine checklist size:**
- **Small feature:** 20-30 items, 2 week timeline
- **Major launch:** 50-70 items, 4 week timeline
- **Regulatory product:** 70-100 items, 6+ week timeline

---

### Step 2: Generate Checklist

Create file: `outputs/launches/[feature-name]-launch-checklist.md`

**Template Structure:**

```markdown
---
feature: [Feature name]
prd: [Link to PRD]
launch_date: YYYY-MM-DD
launch_type: [A/B test / Staged rollout / Full launch]
risk_level: [Low / Medium / High]
---

# Launch Checklist: [Feature Name]

**Target Launch:** [Date]
**Rollout Strategy:** [Strategy]
**Owner:** [PM Name]

---

## Pre-Launch: T-4 Weeks

### Product & Design
- [ ] [P0] PRD reviewed by all stakeholders - **Owner:** PM
- [ ] [P0] Design finalized and approved - **Owner:** Design
- [ ] [P1] User flows documented - **Owner:** Design
- [ ] [P1] Accessibility requirements defined - **Owner:** Design
- [ ] [P1] Design QA complete - **Owner:** Design

### Engineering
- [ ] [P0] Technical design doc approved - **Owner:** Eng Lead
- [ ] [P0] Engineering estimates validated - **Owner:** Eng Lead
- [ ] [P0] Dependencies identified and scheduled - **Owner:** Eng
- [ ] [P0] API contracts defined (if applicable) - **Owner:** Eng
- [ ] [P1] Database schema reviewed - **Owner:** Eng

### Legal & Compliance
- [ ] [P0] Legal review initiated - **Owner:** Legal
- [ ] [P0] Privacy impact assessment complete - **Owner:** Legal/Privacy
- [ ] [P1] ToS/Privacy Policy updates drafted (if needed) - **Owner:** Legal
- [ ] [P1] Compliance requirements documented - **Owner:** Compliance
- [ ] [P0] Security review scheduled - **Owner:** Security

### Analytics & Data
- [ ] [P0] Success metrics defined (STEDII framework) - **Owner:** PM
- [ ] [P0] Analytics instrumentation plan - **Owner:** Data/Eng
- [ ] [P1] Dashboards mocked up - **Owner:** PM/Data
- [ ] [P0] Kill criteria established - **Owner:** PM
- [ ] [P1] Data retention policy defined - **Owner:** Legal/Data

---

## Pre-Launch: T-2 Weeks

### Quality & Testing
- [ ] [P0] QA test plan created - **Owner:** QA
- [ ] [P0] Unit tests written and passing - **Owner:** Eng
- [ ] [P0] Integration tests passing - **Owner:** Eng
- [ ] [P0] E2E tests passing - **Owner:** QA
- [ ] [P1] Performance testing complete - **Owner:** Eng/QA
- [ ] [P0] Security testing complete - **Owner:** Security
- [ ] [P1] Accessibility testing complete - **Owner:** QA/Design
- [ ] [P1] Cross-browser/device testing - **Owner:** QA

### Beta & Early Access
- [ ] [P1] Beta users identified (if applicable) - **Owner:** PM
- [ ] [P1] Beta cohort configured - **Owner:** Eng
- [ ] [P1] Beta feedback mechanism set up - **Owner:** PM
- [ ] [P2] Early access partners notified - **Owner:** PM/Partnerships

### Documentation
- [ ] [P1] User-facing docs drafted - **Owner:** Docs/PM
- [ ] [P1] FAQ created - **Owner:** PM/Support
- [ ] [P1] Help center articles written - **Owner:** Docs
- [ ] [P1] API documentation updated (if applicable) - **Owner:** Eng
- [ ] [P2] Internal knowledge base updated - **Owner:** PM

### Support & Success
- [ ] [P0] Support team briefed - **Owner:** PM/Support
- [ ] [P1] Support playbook created - **Owner:** Support
- [ ] [P1] CS team enablement session - **Owner:** PM/CS
- [ ] [P0] Escalation path defined - **Owner:** Support

### Sales & Marketing
- [ ] [P1] Sales enablement materials prepared - **Owner:** PM/Sales
- [ ] [P1] One-pager/pitch deck created - **Owner:** PM/Marketing
- [ ] [P1] Demo environment ready - **Owner:** Eng/Solutions
- [ ] [P0] Pricing finalized (if new SKU) - **Owner:** PM/Finance
- [ ] [P1] Marketing assets created - **Owner:** Marketing

### Rollout Plan
- [ ] [P0] Rollout strategy finalized - **Owner:** PM
- [ ] [P0] Feature flags configured - **Owner:** Eng
- [ ] [P0] % rollout schedule defined - **Owner:** PM
- [ ] [P0] Rollback plan documented - **Owner:** Eng/PM
- [ ] [P0] Rollback criteria established - **Owner:** PM

---

## Launch Week: T-0

### Final Checks
- [ ] [P0] All stakeholders signed off - **Owner:** PM
- [ ] [P0] Code freeze (if applicable) - **Owner:** Eng Lead
- [ ] [P0] Final regression testing - **Owner:** QA
- [ ] [P1] Load testing complete - **Owner:** Eng
- [ ] [P0] Launch checklist reviewed with team - **Owner:** PM

### Monitoring & Operations
- [ ] [P0] Dashboards live and tested - **Owner:** Data/Eng
- [ ] [P0] Alerts configured - **Owner:** Eng
- [ ] [P0] On-call rotation set - **Owner:** Eng Lead
- [ ] [P0] Incident response plan ready - **Owner:** Eng/PM
- [ ] [P0] Rollback runbook accessible - **Owner:** Eng

### Communications
- [ ] [P1] Internal announcement drafted - **Owner:** PM
- [ ] [P1] Customer communication drafted - **Owner:** PM/Marketing
- [ ] [P1] Email/in-app message scheduled - **Owner:** Marketing/PM
- [ ] [P2] Blog post ready (if applicable) - **Owner:** Marketing
- [ ] [P2] Social media posts queued - **Owner:** Marketing
- [ ] [P2] Press release (if major launch) - **Owner:** Comms

### Launch Day
- [ ] [P0] Feature flag enabled (or % rollout started) - **Owner:** Eng
- [ ] [P0] Metrics monitored in real-time - **Owner:** PM/Data
- [ ] [P0] Support monitoring Zendesk/Intercom - **Owner:** Support
- [ ] [P0] Team available for issues - **Owner:** All
- [ ] [P1] Launch comms sent - **Owner:** Marketing/PM

---

## Post-Launch: T+1 Week

### Monitoring & Triage
- [ ] [P0] Metrics reviewed daily - **Owner:** PM
- [ ] [P0] User feedback collected - **Owner:** PM/Support
- [ ] [P0] Bug triage process active - **Owner:** Eng/PM
- [ ] [P0] Performance monitoring - **Owner:** Eng
- [ ] [P0] No critical bugs blocking users - **Owner:** Eng/QA

### Communication
- [ ] [P1] Stakeholder update sent (early results) - **Owner:** PM
- [ ] [P1] Support team debrief - **Owner:** PM/Support
- [ ] [P1] Sales/CS team update - **Owner:** PM
- [ ] [P2] Early wins documented and shared - **Owner:** PM

### Iteration
- [ ] [P1] User feedback synthesized - **Owner:** PM
- [ ] [P0] High-priority bugs prioritized - **Owner:** PM/Eng
- [ ] [P1] Quick wins identified - **Owner:** PM
- [ ] [P2] V1.1 backlog created - **Owner:** PM

---

## Post-Launch: T+4 Weeks

### Impact Review
- [ ] [P0] Metrics vs targets analyzed - **Owner:** PM
- [ ] [P1] A/B test results (if applicable) - **Owner:** PM/Data
- [ ] [P0] User adoption measured - **Owner:** PM/Data
- [ ] [P0] Success criteria met/missed - **Owner:** PM
- [ ] [P1] Run `/feature-results` for deep analysis - **Owner:** PM

### Documentation
- [ ] [P1] Lessons learned captured - **Owner:** PM
- [ ] [P1] What went well / what didn't - **Owner:** Team
- [ ] [P2] Process improvements identified - **Owner:** PM/Eng Lead
- [ ] [P0] Post-mortem (if issues) - **Owner:** PM/Eng

### Next Steps
- [ ] [P1] Iteration roadmap defined - **Owner:** PM
- [ ] [P2] V2 scoped (if applicable) - **Owner:** PM
- [ ] [P1] Success communicated broadly - **Owner:** PM
- [ ] [P2] Wins celebrated with team - **Owner:** PM/Lead

---

## Risk Mitigation

**High-risk items flagged:**
[Automatically flag based on PRD complexity, regulatory requirements, etc.]

⚠️ **Risks:**
- [Risk 1] - Mitigation: [Action]
- [Risk 2] - Mitigation: [Action]

**Rollback criteria:**
- [Metric] drops below [threshold]
- [X] critical bugs reported
- [Stakeholder] requests pause

---

*Generated: [Timestamp]*
*Launch date: [Date] ([X] weeks away)*
*Items: [Y] total, [Z] critical path*
```

---

### Step 2b: Add Prioritization and Dependencies

Organize checklist items with explicit priorities and dependency chains. Use this format for every item:

```
- [ ] **[P0] Item name** (Blocks: items X, Y) -- @Owner -- Due: Date
- [ ] **[P1] Item name** (Blocked by: item Z) -- @Owner -- Due: Date
- [ ] **[P2] Item name** (No dependencies) -- @Owner -- Due: Date
```

**Priority definitions:**
- **P0** = Must complete or launch does not happen. Zero flexibility. Examples: security review, legal sign-off, feature flags configured, rollback plan documented.
- **P1** = Should complete. Launch can proceed without it, but with documented risk. Examples: help center articles, sales enablement, non-critical QA edge cases.
- **P2** = Nice to have for launch. Can follow up post-launch without impact. Examples: social media posts, internal wiki updates, demo environment polish.

**Dependency format examples:**
```
- [ ] **[P0] Database schema reviewed** (Blocks: API implementation, integration tests) -- @Eng Lead -- Due: T-4 weeks
- [ ] **[P0] API endpoints implemented** (Blocked by: DB schema; Blocks: Frontend integration) -- @Backend Eng -- Due: T-3 weeks
- [ ] **[P0] Frontend integration complete** (Blocked by: API endpoints, Design finalized) -- @Frontend Eng -- Due: T-2 weeks
```

### Step 2c: Identify Critical Path

After generating the full checklist, identify the critical path: the longest chain of dependent items that determines the earliest possible launch date.

**Critical path format:**

```
CRITICAL PATH (longest dependency chain):
[DB Schema Review] --> [API Implementation] --> [Frontend Integration] --> [E2E Tests] --> [Final Regression] --> [Launch]

Total duration: [X] weeks
Slack: [Y] days (buffer before launch date)

WARNING: Any delay in this chain delays launch by the same amount.
```

**How to identify it:**
1. List all P0 items with their dependencies
2. Trace the longest chain from first prerequisite to launch day
3. Sum up the durations of each item in the chain
4. Compare to available time before launch date
5. If critical path exceeds available time, flag immediately: "Launch date at risk. Critical path requires [X] weeks but only [Y] weeks available."

**Also flag:**
- Items on the critical path that have no owner assigned
- Items on the critical path with estimated duration > 1 week (candidates for parallelization)
- External dependencies on the critical path (legal review, partner sign-off) that the team cannot control

---

### Step 3: Customize Based on Feature Type

**Small Feature (< 2 week build):**
- Remove beta section
- Simplify compliance section
- Lighter communications

**Major Launch (new product/major feature):**
- Add press/media section
- Add investor/board communication
- Add partner enablement
- Expand marketing activities

**Regulatory Product (healthcare, finance, etc.):**
- Expand legal/compliance section
- Add audit trail requirements
- Add certification process
- Add regulatory submission items

---

### Step 4: Integrate with Tools

**If Linear/Jira MCP available:**
- Offer to create tasks for each checklist item
- Assign owners automatically
- Set due dates based on launch date
- Link to PRD

**If Calendar MCP available:**
- Schedule key milestones (T-4 weeks, T-2 weeks, Launch Day, T+1 week)
- Block time for critical activities

---

## Integration with Other Skills

**Before `/launch-checklist`:**
- `/prd-draft` - Define what's launching
- `/prd-review-panel` - Ensure PRD is solid
- `/prototype` - Validate solution before building

**After `/launch-checklist`:**
- `/create-tickets` - Convert to Linear/Jira tasks
- `/daily-plan` - Surface checklist items in daily planning
- `/feature-results` - Analyze post-launch impact

**During launch:**
- `/weekly-review` - Track checklist progress each week
- `/status-update` - Share launch status with stakeholders

---

## Related Skills

**Before this:**
- `/prd-draft` - Create PRD
- `/prd-review-panel` - Validate approach
- `/impact-sizing` - Estimate value

**After this:**
- `/create-tickets` - Track in Linear/Jira
- `/feature-results` - Post-launch analysis
- `/weekly-review` - Monitor progress weekly

---

## Output Quality Self-Check

Before delivering the launch checklist, verify:

- [ ] **Every item has an owner** -- No orphan tasks with "TBD" or missing owner assignments
- [ ] **Every item has a priority** -- P0, P1, or P2 assigned to each item
- [ ] **Dependencies are explicit** -- "Blocked by" and "Blocks" noted where they exist
- [ ] **Critical path identified** -- Longest dependency chain is highlighted with total duration
- [ ] **Launch date feasibility checked** -- Critical path duration compared to available time; risk flagged if tight
- [ ] **Rollback plan included** -- Clear criteria for when to roll back and how to do it
- [ ] **Kill criteria defined** -- Specific metric thresholds that would stop the launch
- [ ] **All stakeholder groups covered** -- Engineering, design, legal, support, sales, marketing, and comms are represented
- [ ] **Post-launch monitoring planned** -- Dashboards, alerts, and review cadence are specified
- [ ] **Customized to launch type** -- Small features have a streamlined checklist; major launches have expanded sections

If any check fails, fix it before delivering. A launch checklist with missing owners or unclear dependencies creates false confidence.
