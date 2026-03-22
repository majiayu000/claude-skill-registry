---
name: kanban-systems
description: "Implement Kanban workflow management with visual boards, WIP limits, and continuous flow optimization. Use for: visualizing work, limiting work-in-progress, managing flow, continuous delivery, process improvement, bottleneck identification, and pull-based systems."
---

# Kanban Systems

Implement visual workflow management systems that optimize flow through WIP limits and continuous improvement.

## Overview

Kanban is a workflow management method that visualizes work, limits work-in-progress, and optimizes flow for continuous delivery. Originating from Toyota's manufacturing system and adapted for knowledge work by David J. Anderson, Kanban provides a practical system for managing work with flexibility and efficiency. This skill covers Kanban principles, board design, WIP limits, flow optimization, and metrics.

## Core Principles

### 1. Visualize the Workflow

Make invisible work visible using a Kanban board with columns representing workflow stages.

**Basic Board Structure**:
```
| Backlog | To Do | In Progress | Review | Done |
```

**Advanced Elements**:
- Swim lanes for work types (features, bugs, tech debt)
- Color coding by priority or class of service
- Blocked indicators
- Work item age
- Assignee avatars

### 2. Limit Work in Progress (WIP)

Restrict the number of items in each workflow stage to prevent overload and improve flow.

**Setting WIP Limits**:
- Initial: 1.5 × number of team members per stage
- Adjust based on observation and metrics
- Different limits for different stages
- Enforce strictly to drive improvement

**Benefits**:
- Faster completion of individual items
- Reduced multitasking
- Earlier identification of bottlenecks
- Improved focus and quality

### 3. Manage Flow

Ensure smooth, continuous movement of work through the system.

**Flow Metrics**:
- **Lead Time**: Request to delivery
- **Cycle Time**: Start to completion
- **Throughput**: Items completed per period
- **Work Item Age**: Time in system

**Flow Optimization**:
- Reduce batch sizes
- Minimize handoffs
- Balance capacity across stages
- Eliminate waste
- Address bottlenecks promptly

### 4. Make Policies Explicit

Document and share the rules governing the process.

**Policies to Define**:
- Definition of Ready for each column
- Definition of Done for each column
- Pull criteria (when to move work)
- Class of service policies
- Blocking and escalation procedures

### 5. Implement Feedback Loops

Regular meetings for inspection and adaptation.

**Kanban Cadences**:
- **Daily Standup** (15 min): Walk the board, identify blockers
- **Replenishment Meeting** (Weekly): Select new work from backlog
- **Service Delivery Review** (Monthly): Review metrics and customer satisfaction
- **Operations Review** (Monthly): Process improvements and capability development
- **Retrospective** (Bi-weekly/Monthly): Team reflection and improvement

### 6. Improve Collaboratively, Evolve Experimentally

Use scientific method for continuous improvement.

**Improvement Process**:
1. Observe problem or opportunity
2. Hypothesize potential improvement
3. Experiment with change
4. Measure impact
5. Decide: keep, modify, or discard
6. Repeat continuously

## Kanban Board Design

### Column Design

**Typical Software Development Board**:
```
Backlog → Analysis → Development → Code Review → Testing → Deployment → Done
```

**Support/Maintenance Board**:
```
Inbox → Triage → Investigation → Resolution → Verification → Closed
```

**Marketing Board**:
```
Ideas → Planning → Creation → Review → Approval → Publishing → Analysis
```

### Swim Lanes

Horizontal rows for different work types or priorities:
- **By Type**: Features, Bugs, Technical Debt
- **By Priority**: Expedite, Standard, Intangible
- **By Team**: Team A, Team B, Shared
- **By Project**: Project X, Project Y, BAU

### Card Information

Each work item card should include:
- Title and description
- Assignee(s)
- Priority/class of service
- Due date (if applicable)
- Blocked status and reason
- Age (days in system)
- Links to details

## WIP Limits in Detail

### Types of WIP Limits

**Column Limits**: Maximum items in entire column
```
| To Do (5) | In Progress (3) | Review (2) | Done |
```

**Per-Person Limits**: Maximum items per individual (1-2)

**CONWIP**: Constant WIP across entire board

**Work Type Limits**: Separate limits for bugs vs. features

### Adjusting WIP Limits

**Increase when**:
- Frequent idle time
- Team members waiting for work
- High process efficiency (>80%)

**Decrease when**:
- Too much multitasking
- Items aging excessively
- Bottlenecks not visible
- Low process efficiency (<40%)

### Handling WIP Limit Violations

- Make violations visible (different color, alert)
- Discuss in standup why limit exceeded
- Swarm to resolve before adding more work
- Track violation frequency as metric
- Adjust limits if consistently violated

## Classes of Service

Differentiate work types with different risk profiles and urgency.

| Class | Description | WIP Limit | SLA | % of Work |
|-------|-------------|-----------|-----|-----------|
| Expedite | Critical, urgent (production down) | 1 max | Hours | <5% |
| Fixed Date | Hard deadline (regulatory) | 20-30% | By date | 10-20% |
| Standard | Normal business value | 60-70% | 2 weeks | 60-70% |
| Intangible | Tech debt, research | 10-20% | Best effort | 10-20% |

**Visual Representation**:
- Use swim lanes or color coding
- Red: Expedite
- Orange: Fixed Date
- Blue: Standard
- Green: Intangible

## Identifying and Resolving Bottlenecks

### Bottleneck Indicators

1. **Card Accumulation**: Column consistently at WIP limit
2. **Increasing Cycle Time**: Time in specific stage growing
3. **CFD Widening**: Cumulative Flow Diagram band expanding
4. **Team Feedback**: Complaints about waiting or overload
5. **Aging Items**: Cards stuck in same stage

### Resolution Strategies

**Clarify Exit Criteria**: Ensure Definition of Done is clear

**Redistribute Capacity**: Move people to bottleneck stage, cross-train

**Break Down Work**: Split large items into smaller pieces

**Address Dependencies**: Identify and resolve external blockers

**Adjust WIP Limits**: Reduce upstream WIP to prevent overloading

**Automate or Eliminate**: Streamline repetitive tasks

**Add Capacity**: Hire or contract (last resort)

## Kanban Metrics

### Cumulative Flow Diagram (CFD)

Stacked area chart showing work items in each stage over time.

**Healthy CFD**:
- Smooth, parallel bands
- Consistent vertical distance (stable WIP)
- Steady upward slope (consistent throughput)

**Problem Indicators**:
- Widening band: Bottleneck
- Flat band: No work in stage
- Vertical jump: Batch arrival
- Narrowing band: Starvation

### Lead Time Distribution

Histogram of lead times with percentiles.

**Example**:
- 50th percentile: 5 days
- 85th percentile: 10 days
- 95th percentile: 15 days

**Commitment**: "We'll deliver in 10 days with 85% confidence"

### Throughput

Items completed per week/month.

**Uses**:
- Capacity planning
- Forecasting completion dates
- Identifying trends

**Forecasting**:
- Average throughput: 20 items/week
- Backlog: 100 items
- Forecast: 5 weeks (100 ÷ 20)
- Add buffer for confidence

### Flow Efficiency

Percentage of time spent on value-adding work.

**Formula**: (Active time / Total lead time) × 100

**Typical Knowledge Work**: 15-20%
**Target**: >40%

## Kanban vs. Scrum

| Aspect | Kanban | Scrum |
|--------|--------|-------|
| Cadence | Continuous flow | Fixed sprints |
| Roles | No prescribed roles | PO, SM, Dev Team |
| Commitment | No fixed commitment | Sprint commitment |
| Changes | Anytime | Between sprints |
| Metrics | Lead time, cycle time | Velocity, burndown |
| WIP | Limited explicitly | Limited by sprint |
| Board | Persistent | Reset each sprint |
| Best for | Continuous delivery, support | Product development |

## Scrumban

Combining Kanban and Scrum for best of both.

**From Scrum**:
- Sprint planning (or replenishment)
- Daily standup
- Retrospectives
- Optional roles

**From Kanban**:
- Visual board
- WIP limits
- Continuous flow
- Pull system
- Flow metrics

**When to Use**:
- Transitioning from Scrum to Kanban
- Need sprint structure with flow optimization
- Maintenance teams with project work
- Want flexibility with structure

## Tools

### Physical Boards

**Advantages**: High visibility, tactile, easy to modify
**Best Practices**: Whiteboard, sticky notes, high-traffic area

### Digital Tools

**Trello**: Simple, visual, good for small teams
**Jira**: Comprehensive, advanced reporting, enterprise-grade
**Azure DevOps**: Microsoft integration, built-in CI/CD
**LeanKit**: Purpose-built for Kanban, advanced analytics
**Kanbanize**: Advanced features, portfolio management
**Monday.com**: Flexible, visual, non-technical teams

## Using the Reference Files

### When to Read Each Reference

**`/references/board-design-guide.md`** — Read when setting up new Kanban boards, optimizing workflow stages, or designing swim lanes and card layouts.

**`/references/wip-limits-optimization.md`** — Read when establishing or adjusting WIP limits, analyzing flow constraints, or resolving bottlenecks.

**`/references/metrics-and-analytics.md`** — Read when implementing Kanban metrics, creating CFDs, analyzing lead time distributions, or forecasting with throughput.

**`/references/advanced-practices.md`** — Read when implementing classes of service, scaling Kanban across teams, or integrating with other methodologies.
