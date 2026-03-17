---
name: project-workflow-patterns
description: Common GitHub Projects workflow patterns and best practices for team collaboration. Use when designing workflows, setting up new projects, or optimizing existing processes.
---

# GitHub Projects Workflow Patterns

This skill provides proven workflow patterns for different team types and development methodologies using GitHub Projects V2.

## Agile Scrum Workflow

### Project Structure

**Fields**:
- Status: Backlog → Todo → In Progress → In Review → Done
- Priority: P0, P1, P2, P3
- Story Points: 1, 2, 3, 5, 8, 13
- Sprint: 2-week iterations
- Assignee: Team member

**Views**:
1. **Sprint Board**: Board view grouped by Status, filtered to current sprint
2. **Sprint Backlog**: Table view showing all current sprint items sorted by priority
3. **Product Backlog**: Table view of all Backlog items sorted by priority
4. **Sprint Velocity**: Custom view tracking completed points

### Workflow Steps

1. **Backlog Refinement** (Weekly):
   - Review new items in Backlog
   - Assign Priority based on business value
   - Estimate Story Points for upcoming items
   - Add acceptance criteria in item body
   - Move refined items to top of Backlog

2. **Sprint Planning** (Every 2 weeks):
   - Review team velocity from last sprint
   - Select top-priority items from Backlog
   - Assign to current Sprint iteration
   - Move items from Backlog to Todo
   - Ensure total points ≤ team capacity

3. **Daily Standup** (Daily):
   - Review Sprint Board
   - Items "In Progress" are discussed
   - Blockers identified and marked P0/P1
   - Items "In Review" get review assignments

4. **Development**:
   - Pull item from Todo to In Progress
   - Self-assign the item
   - Create feature branch
   - Implement and test
   - Create PR linked to issue
   - Auto-move to In Review (via automation)

5. **Code Review**:
   - Team reviews items In Review
   - Approve or request changes
   - When PR merges → Auto-move to Done

6. **Sprint Review** (End of sprint):
   - Review all Done items
   - Demo completed features
   - Archive Done items
   - Celebrate wins

7. **Sprint Retrospective** (End of sprint):
   - Review sprint metrics
   - Discuss what went well/poorly
   - Create action items for improvements

### Success Metrics

- **Velocity**: Average points completed per sprint
- **Predictability**: % variance from planned vs actual
- **Cycle Time**: Average time from Todo → Done
- **Work in Progress**: Should stay ≤ team size
- **Sprint Completion**: Aim for >80% of committed work

## Kanban Continuous Flow

### Project Structure

**Fields**:
- Status: Ready → In Progress → Review → Done
- Priority: Critical, High, Normal, Low
- Size: S, M, L, XL
- Type: Bug, Feature, Chore, Tech Debt
- SLA Days: Number (days until due)

**Views**:
1. **Flow Board**: Board grouped by Status with WIP limits
2. **Blocked Items**: Table filtered to items with "blocked" label
3. **Priority Lane**: Board grouped by Priority
4. **Aging Report**: Table sorted by days in status

### Workflow Steps

1. **Item Entry**:
   - New items start in Ready
   - Assign Priority immediately
   - Assign Size estimate
   - Set Type category
   - Calculate SLA based on Priority

2. **Pull System**:
   - Team members pull from Ready when capacity available
   - WIP limits enforced per person (typically 2-3 items)
   - Highest priority items pulled first
   - Self-assign when pulling to In Progress

3. **Work In Progress**:
   - Focus on finishing items before starting new ones
   - Update item if blockers occur
   - Seek help if stuck >2 days

4. **Review**:
   - Items move to Review when PR opens
   - Automated PR → Review status transition
   - Reviews prioritized by age (oldest first)

5. **Completion**:
   - Merged PR auto-moves to Done
   - Done items archived after 7 days
   - Metrics tracked continuously

6. **WIP Limit Management**:
   - In Progress limit: [team size × 2]
   - Review limit: 5 items maximum
   - If limits exceeded, stop pulling new work

### Success Metrics

- **Throughput**: Items completed per week
- **Lead Time**: Time from Ready → Done
- **WIP**: Average items in progress (lower is better)
- **Flow Efficiency**: Value-add time / total time
- **Blocked Rate**: % of time items are blocked

## Bug Triage Workflow

### Project Structure

**Fields**:
- Status: New → Triaged → In Progress → Fixed → Verified → Closed
- Severity: Critical, High, Medium, Low
- Component: Frontend, Backend, API, Database, Infrastructure
- Affected Users: Number
- Reported Date: Date
- Fix Version: Text

**Views**:
1. **Triage Queue**: Board showing New bugs by Severity
2. **Active Bugs**: Table of In Progress/Fixed bugs sorted by Severity
3. **Component View**: Board grouped by Component
4. **Verification Queue**: Table of Fixed bugs awaiting verification

### Workflow Steps

1. **Bug Reported**:
   - User/QA creates issue with bug template
   - Auto-add to project with New status
   - Triage team notified

2. **Triage** (Daily):
   - Review all New bugs
   - Assign Severity based on impact:
     * Critical: Production down, data loss, security
     * High: Major feature broken, >100 users affected
     * Medium: Feature degraded, workaround exists
     * Low: Minor issue, cosmetic problem
   - Assign Component
   - Estimate Affected Users
   - Move to Triaged status
   - Assign to component owner if Critical/High

3. **Development**:
   - Developer pulls bug from Triaged
   - Move to In Progress
   - Investigate and fix
   - Create PR with "Fixes #[issue]" in description
   - Move to Fixed when PR merges

4. **Verification**:
   - QA/Reporter tests fix
   - If verified: Move to Verified, close issue
   - If not fixed: Move back to In Progress with notes

5. **Closed**:
   - Verified items move to Closed
   - Archive after 30 days
   - Track in Fix Version for release notes

### Success Metrics

- **Triage Time**: Time from New → Triaged (target: <1 day)
- **Time to Fix**: Time from Triaged → Fixed by severity
- **Bug Escape Rate**: Bugs found in production vs QA
- **Reopen Rate**: % of bugs reopened after fix
- **Critical SLA**: 100% of Critical bugs fixed within SLA

## Feature Development Roadmap

### Project Structure

**Fields**:
- Status: Idea → Spec → Development → Beta → Launched → Retired
- Priority: Must Have, Should Have, Nice to Have
- Quarter: Q1 2025, Q2 2025, Q3 2025, Q4 2025
- Effort: 1 week, 2 weeks, 1 month, 3 months, 6 months
- Customer Impact: Number (customers requesting)
- Owner: Text (PM name)
- Launch Date: Date

**Views**:
1. **Roadmap Timeline**: Roadmap view by Launch Date
2. **This Quarter**: Table filtered to current quarter sorted by Priority
3. **Ideas Board**: Board of Idea status items grouped by Priority
4. **Feature Status**: Board grouped by Status

### Workflow Steps

1. **Idea Collection**:
   - Create draft items in project
   - Status: Idea
   - Rough priority assignment
   - Track Customer Impact

2. **Quarterly Planning**:
   - Review all Ideas
   - Assign Priority: Must/Should/Nice to Have
   - Assign Quarter
   - Assign Owner (PM)
   - Top ideas move to Spec status

3. **Specification**:
   - Owner writes detailed spec
   - Define success metrics
   - Estimate Effort
   - Get stakeholder approval
   - Move to Development when eng committed

4. **Development**:
   - Link to engineering project/sprint
   - Track progress via linked issues
   - Status updates in weekly sync
   - Move to Beta when ready for testing

5. **Beta Testing**:
   - Limited rollout
   - Gather feedback
   - Fix critical issues
   - Refine based on learnings
   - Move to Launched when GA

6. **Launch**:
   - Full rollout
   - Marketing announcement
   - Track adoption metrics
   - Monitor for issues
   - Eventually move to Retired when deprecated

### Success Metrics

- **Delivery Accuracy**: % of features launched on time
- **Customer Satisfaction**: NPS or CSAT per feature
- **Adoption Rate**: % of users using new feature
- **Spec → Launch**: Average time from commit to ship
- **Roadmap Predictability**: % of quarterly commitments met

## Common Automation Patterns

### Status Automation
```
When PR opens → Move item to "In Review"
When PR merges → Move item to "Done"
When issue closed → Move item to "Done"
When item added → Set default Status to "Backlog"
```

### Priority Automation
```
When "critical" label added → Set Priority to P0
When "bug" label added → Set Priority to P1
When "enhancement" label added → Set Priority to P2
```

### Archival Automation
```
When item in "Done" for 30 days → Archive
When item closed and verified → Archive after 7 days
```

### Notification Automation
```
When P0 item added → Notify team on Slack
When item stuck in "In Review" >3 days → Notify assignee
When sprint ends → Generate velocity report
```

## Best Practices Across All Workflows

1. **Single Source of Truth**: Use project as primary view, not issue lists
2. **Consistent Field Usage**: Standardize field names/values across projects
3. **Regular Refinement**: Weekly grooming prevents backlog chaos
4. **Clear Definitions**: Document what each status/priority means
5. **Limit WIP**: Focus on finishing over starting
6. **Automate Transitions**: Reduce manual status updates
7. **Measure & Improve**: Track metrics, iterate on process
8. **Team Buy-in**: Involve team in workflow design
9. **Visual Management**: Use boards for transparency
10. **Archive Regularly**: Keep active views clean and focused

## Choosing the Right Workflow

| Team Type | Recommended Workflow | Why |
|-----------|---------------------|-----|
| Product Dev Team | Agile Scrum | Predictable planning, clear sprints |
| Platform/DevOps | Kanban | Continuous flow, varied work types |
| Support/Ops | Bug Triage | Prioritize by severity, fast response |
| Product Management | Feature Roadmap | Long-term planning, stakeholder communication |
| OSS Maintainers | Kanban + Priority | Flexible, contributor-friendly |
| Startup | Kanban | Fast iteration, changing priorities |

## Hybrid Workflows

Many teams combine patterns:

- **Scrum + Bug Triage**: Separate projects for planned work vs bugs
- **Kanban + Roadmap**: Tactical execution + strategic planning
- **Feature Roadmap → Scrum**: PM roadmap feeds eng sprint planning

Remember: Workflows should serve the team, not constrain them. Start simple, iterate based on what works for your team's unique needs.
