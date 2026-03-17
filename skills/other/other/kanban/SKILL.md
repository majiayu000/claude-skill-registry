---
name: kanban
description: Kanban methodology including boards, WIP limits, flow metrics, and continuous delivery. Activate for Kanban boards, workflow visualization, and lean project management.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Kanban Skill

Provides comprehensive Kanban methodology capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Kanban board setup
- WIP limit configuration
- Flow metrics analysis
- Continuous delivery workflows
- Pull-based systems

## Kanban Board Structure

\`\`\`
┌────────────┬────────────┬────────────┬────────────┬────────────┐
│  BACKLOG   │   TO DO    │ IN PROGRESS│  REVIEW    │    DONE    │
│   (∞)      │   (10)     │    (5)     │    (3)     │    (∞)     │
├────────────┼────────────┼────────────┼────────────┼────────────┤
│            │            │            │            │            │
│  ┌──────┐  │  ┌──────┐  │  ┌──────┐  │  ┌──────┐  │  ┌──────┐  │
│  │ Task │  │  │ Task │  │  │ Task │  │  │ Task │  │  │ Task │  │
│  │  1   │  │  │  2   │  │  │  3   │  │  │  4   │  │  │  5   │  │
│  └──────┘  │  └──────┘  │  └──────┘  │  └──────┘  │  └──────┘  │
│            │            │            │            │            │
│  ┌──────┐  │  ┌──────┐  │  ┌──────┐  │            │  ┌──────┐  │
│  │ Task │  │  │ Task │  │  │ Task │  │            │  │ Task │  │
│  │  6   │  │  │  7   │  │  │  8   │  │            │  │  9   │  │
│  └──────┘  │  └──────┘  │  └──────┘  │            │  └──────┘  │
│            │            │            │            │            │
└────────────┴────────────┴────────────┴────────────┴────────────┘
\`\`\`

## Kanban Principles

### Core Practices
1. **Visualize the workflow** - Make work visible
2. **Limit WIP** - Focus on finishing, not starting
3. **Manage flow** - Optimize throughput
4. **Make policies explicit** - Clear rules for moving work
5. **Implement feedback loops** - Regular reviews
6. **Improve collaboratively** - Continuous improvement

### WIP Limits

\`\`\`markdown
## WIP Limit Guidelines

| Column        | WIP Limit | Rationale                     |
|---------------|-----------|-------------------------------|
| Backlog       | ∞         | Unlimited ideas storage       |
| To Do         | 10        | Committed work for near-term  |
| In Progress   | 5         | Active development capacity   |
| Review        | 3         | Prevent review bottleneck     |
| Done          | ∞         | Completed work archive        |

### Setting WIP Limits
- Start with team size × 1.5
- Adjust based on flow metrics
- Too high = loss of focus
- Too low = idle time
\`\`\`

## Flow Metrics

### Lead Time vs Cycle Time
\`\`\`
                      Lead Time
    ◄───────────────────────────────────────────►
    │                                           │
    │         Cycle Time                        │
    │    ◄─────────────────────►                │
    │    │                     │                │
┌───▼────▼───┐   ┌──────────┐   ┌──────────┐   ┌▼─────────┐
│  Created   │──►│In Progress│──►│  Review  │──►│   Done   │
│ (Backlog)  │   │           │   │          │   │          │
└────────────┘   └──────────┘   └──────────┘   └──────────┘

Lead Time: Time from request to delivery
Cycle Time: Time from start to completion
\`\`\`

### Throughput Calculation
\`\`\`python
# Throughput: Items completed per time period
def calculate_throughput(completed_items: list, period_days: int) -> float:
    items_completed = len(completed_items)
    throughput = items_completed / period_days
    return throughput

# Example
completed_this_week = 15
throughput = completed_this_week / 7  # 2.14 items per day
\`\`\`

### Cumulative Flow Diagram
\`\`\`
Items │
  50  │                              ●──── Done
      │                        ●────●
  40  │                  ●────●
      │            ●────●              ●──── Review
  30  │      ●────●              ●────●
      │●────●                 ●───●      ●──── In Progress
  20  │                   ●───●     ●───●
      │              ●───●              ●──── To Do
  10  │         ●───●
      │    ●───●
   0  │●──●_________________________________
      Week 1   2    3    4    5    6    7
\`\`\`

## Card Structure

\`\`\`markdown
## Kanban Card Template

### Title
[Clear, concise description]

### Type
[ ] Feature  [ ] Bug  [ ] Tech Debt  [ ] Support

### Details
- **Requester:** [Name]
- **Priority:** [High/Medium/Low]
- **Size:** [S/M/L/XL]
- **Due Date:** [If applicable]

### Description
[What needs to be done]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Blockers
[Any dependencies or impediments]

### Class of Service
[ ] Expedite (Urgent, bypass WIP)
[ ] Fixed Date (External deadline)
[ ] Standard (Normal flow)
[ ] Intangible (Low priority)
\`\`\`

## Service Level Expectations

\`\`\`markdown
## SLE by Card Type

| Type          | Target Lead Time | % On Time Target |
|---------------|------------------|------------------|
| Expedite      | 1 day            | 95%              |
| Bug Fix       | 3 days           | 90%              |
| Feature       | 2 weeks          | 85%              |
| Tech Debt     | 1 month          | 80%              |
\`\`\`

## Swimlanes

\`\`\`
┌────────────────────────────────────────────────────────────┐
│ EXPEDITE (WIP: 1)                                          │
├────────────────────────────────────────────────────────────┤
│ ┌──────────┐                                               │
│ │ CRITICAL │                                               │
│ │ Bug #123 │                                               │
│ └──────────┘                                               │
├────────────────────────────────────────────────────────────┤
│ STANDARD (WIP: 5)                                          │
├────────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                       │
│ │ Task │ │ Task │ │ Task │ │ Task │                       │
│ │  1   │ │  2   │ │  3   │ │  4   │                       │
│ └──────┘ └──────┘ └──────┘ └──────┘                       │
├────────────────────────────────────────────────────────────┤
│ INTANGIBLE (WIP: 2)                                        │
├────────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐                                          │
│ │ Docs │ │ Tech │                                          │
│ │ Task │ │ Debt │                                          │
│ └──────┘ └──────┘                                          │
└────────────────────────────────────────────────────────────┘
\`\`\`

## Kanban Meetings

### Daily Standup (Walking the Board)
- Start from right (Done) to left (Backlog)
- Focus on blocked items
- Identify bottlenecks
- 15 minutes max

### Replenishment Meeting (Weekly)
- Review backlog
- Prioritize incoming work
- Pull items to "To Do"
- Discuss capacity

### Delivery Planning (Bi-weekly)
- Review completed items
- Update forecasts
- Communicate delivery dates

## Golden Armada Kanban Commands

\`\`\`bash
# View board status
/kanban-status --board golden-armada

# Add item to backlog
/kanban-add --title "Feature X" --type feature --size M

# Move item
/kanban-move GA-123 --to "In Progress"

# Generate metrics report
/kanban-metrics --period 30d
\`\`\`
