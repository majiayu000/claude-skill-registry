---
name: scrum
description: Scrum methodology including sprints, ceremonies, backlog management, and agile practices. Activate for sprint planning, standups, retrospectives, and agile workflows.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Scrum Skill

Provides comprehensive Scrum methodology capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Sprint planning and management
- Daily standups
- Sprint reviews and retrospectives
- Backlog grooming
- Agile estimation

## Scrum Framework Overview

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCT BACKLOG                         │
│  (Prioritized list of features, enhancements, fixes)        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   SPRINT PLANNING                            │
│  (Select items for sprint, create Sprint Backlog)           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SPRINT (2 weeks)                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Daily   │  │ Daily   │  │ Daily   │  │ Daily   │  ...   │
│  │ Standup │  │ Standup │  │ Standup │  │ Standup │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  SPRINT REVIEW          │        SPRINT RETROSPECTIVE       │
│  (Demo to stakeholders) │  (Team improvement discussion)    │
└─────────────────────────────────────────────────────────────┘
\`\`\`

## Scrum Roles

### Product Owner
- Owns the Product Backlog
- Prioritizes items by business value
- Accepts/rejects completed work
- Represents stakeholders

### Scrum Master
- Facilitates Scrum events
- Removes impediments
- Coaches the team
- Protects the team from distractions

### Development Team
- Self-organizing (3-9 members)
- Cross-functional
- Delivers potentially shippable increments
- Commits to Sprint goals

## Sprint Ceremonies

### Sprint Planning (2-4 hours)
\`\`\`markdown
## Sprint Planning Agenda

### Part 1: What (1-2 hours)
- Product Owner presents prioritized backlog items
- Team asks clarifying questions
- Team selects items for sprint based on capacity

### Part 2: How (1-2 hours)
- Team breaks stories into tasks
- Team estimates tasks (hours)
- Team creates Sprint Backlog

### Outputs:
- Sprint Goal
- Sprint Backlog
- Capacity commitment
\`\`\`

### Daily Standup (15 minutes)
\`\`\`markdown
## Daily Standup Format

Each team member answers:
1. What did I complete yesterday?
2. What will I work on today?
3. Are there any blockers?

### Rules:
- Same time, same place daily
- Standing up (keeps it short)
- Focus on sprint goal progress
- Detailed discussions after standup
\`\`\`

### Sprint Review (1-2 hours)
\`\`\`markdown
## Sprint Review Agenda

1. Sprint Goal Review (5 min)
   - Did we achieve the sprint goal?

2. Demo Completed Work (30-45 min)
   - Show working software
   - Stakeholder feedback

3. Product Backlog Update (15 min)
   - New items from feedback
   - Reprioritization

4. Release Discussion (15 min)
   - What can be released?
   - Timeline for deployment
\`\`\`

### Sprint Retrospective (1-2 hours)
\`\`\`markdown
## Retrospective Formats

### Start-Stop-Continue
- Start: What should we begin doing?
- Stop: What should we stop doing?
- Continue: What's working well?

### 4Ls (Liked, Learned, Lacked, Longed For)
- Liked: What went well?
- Learned: What did we learn?
- Lacked: What was missing?
- Longed For: What do we wish we had?

### Mad-Sad-Glad
- Mad: What frustrated us?
- Sad: What disappointed us?
- Glad: What made us happy?
\`\`\`

## User Stories

### Story Format
\`\`\`markdown
## User Story Template

**Title:** [Feature Name]

**As a** [type of user]
**I want** [goal/feature]
**So that** [benefit/value]

### Acceptance Criteria:
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

### Definition of Done:
- [ ] Code complete
- [ ] Unit tests written (>80% coverage)
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] QA tested
- [ ] Product Owner accepted
\`\`\`

### INVEST Criteria
- **I**ndependent: Can be developed separately
- **N**egotiable: Details can be discussed
- **V**aluable: Delivers value to user
- **E**stimable: Can be sized
- **S**mall: Fits in one sprint
- **T**estable: Has clear acceptance criteria

## Estimation

### Story Points (Fibonacci)
\`\`\`
1  - Trivial (< 1 hour)
2  - Small (few hours)
3  - Medium (1 day)
5  - Large (2-3 days)
8  - Very Large (1 week)
13 - Epic (needs breakdown)
\`\`\`

### Planning Poker
1. Product Owner presents story
2. Team discusses and asks questions
3. Each member privately selects estimate
4. All reveal simultaneously
5. Discuss outliers
6. Re-vote if needed
7. Consensus reached

## Velocity & Capacity

### Velocity Calculation
\`\`\`python
# Average of last 3-5 sprints
velocities = [45, 42, 48, 40, 50]
average_velocity = sum(velocities) / len(velocities)  # 45 points

# Sprint capacity planning
team_members = 5
sprint_days = 10
availability = 0.8  # 80% (meetings, etc.)
capacity_hours = team_members * sprint_days * 6 * availability  # 240 hours
\`\`\`

### Burndown Chart
\`\`\`
Points │
  50   │●
       │  ●
  40   │    ●  (Actual)
       │      ●
  30   │        ●
       │   - - - - (Ideal)
  20   │              ●
       │
  10   │                  ●
       │
   0   │____________________●___
       Day 1   5    10    Sprint End
\`\`\`

## Golden Armada Scrum Commands

\`\`\`bash
# Sprint planning
/sprint-plan --velocity 45 --capacity 240

# Daily standup
/standup --team golden-armada

# Sprint review
/sprint-review --sprint 15

# Retrospective
/retro --format start-stop-continue

# Backlog grooming
/backlog-groom --limit 20
\`\`\`
