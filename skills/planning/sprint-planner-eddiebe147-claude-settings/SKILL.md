---
name: Sprint Planner
slug: sprint-planner
description: Plan and execute Agile sprints with velocity tracking, capacity planning, and retrospective insights
category: project
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "plan sprint"
  - "start sprint"
  - "sprint planning"
  - "create sprint"
  - "sprint velocity"
tags:
  - agile
  - scrum
  - sprint
  - velocity
  - capacity
  - backlog
---

# Sprint Planner

The Sprint Planner skill helps teams plan and execute effective Agile sprints using Scrum methodology. It focuses on capacity-based planning, velocity tracking, and continuous improvement through retrospectives. The skill ensures sprints are properly scoped, committed, and executed with clear goals and metrics.

This skill excels at breaking down epics and user stories into sprint-sized work, estimating effort using story points or hours, tracking team velocity, and facilitating sprint ceremonies (planning, daily standups, reviews, retrospectives).

Sprint Planner emphasizes sustainable pace, predictable delivery, and team empowerment through data-driven planning and retrospective learning.

## Core Workflows

### Workflow 1: Sprint Planning

**Steps:**
1. **Pre-Planning Preparation** (before ceremony)
   - Ensure backlog is groomed and prioritized
   - Verify user stories have acceptance criteria
   - Review team capacity for upcoming sprint
   - Gather velocity data from previous sprints
   - Identify any holidays, PTO, or known interruptions

2. **Set Sprint Goal**
   - Review product roadmap and priorities
   - Define 1-2 sentence sprint goal
   - Align with stakeholders on desired outcomes
   - Ensure goal is measurable and achievable

3. **Calculate Team Capacity**
   - List all team members and their availability
   - Account for meetings, support rotation, planned time off
   - Calculate total available hours or story points
   - Apply 70% rule (plan for 70% of theoretical capacity)

4. **Select Stories from Backlog**
   - Start with highest-priority items
   - Review story details and acceptance criteria
   - Estimate effort (if not already estimated)
   - Pull stories until capacity is reached
   - Ensure stories align with sprint goal

5. **Break Down Stories into Tasks**
   - Decompose each story into technical tasks
   - Estimate task hours (2-8 hour chunks)
   - Identify dependencies between tasks
   - Assign owners or leave for team self-organization

6. **Sprint Commitment**
   - Review total commitment vs. capacity
   - Identify risks and mitigation strategies
   - Get team agreement on sprint backlog
   - Document sprint goal and commitment

**Output:** Sprint backlog with committed stories, tasks, capacity allocation, and sprint goal.

### Workflow 2: Daily Standup Facilitation

**15-minute time-boxed meeting:**

Each team member answers:
1. **Yesterday**: What did I complete?
2. **Today**: What will I work on?
3. **Blockers**: What's preventing progress?

**As facilitator:**
- Keep updates brief (2 minutes per person)
- Note blockers for offline resolution
- Update sprint board in real-time
- Identify risks to sprint goal
- Schedule necessary follow-up conversations

**Output:** Updated sprint board and blocker resolution plan.

### Workflow 3: Sprint Review

**Steps:**
1. **Demo Completed Work**
   - Show each completed story in action
   - Demonstrate acceptance criteria met
   - Gather stakeholder feedback
   - Note any change requests or new ideas

2. **Review Sprint Metrics**
   - Completed vs. committed story points
   - Burndown chart analysis
   - Velocity trend
   - Quality metrics (bugs, test coverage)

3. **Capture Feedback**
   - What did stakeholders like?
   - What needs adjustment?
   - New requirements or priorities?
   - Add items to product backlog

**Output:** Demo recording, stakeholder feedback, updated backlog.

### Workflow 4: Sprint Retrospective

**Steps:**
1. **Set the Stage** (5 min)
   - Review retrospective goals and norms
   - Choose retro format (Start/Stop/Continue, etc.)

2. **Gather Data** (15 min)
   - What went well?
   - What didn't go well?
   - What puzzles us?
   - Review metrics and sprint data

3. **Generate Insights** (15 min)
   - Identify patterns and root causes
   - Discuss why things happened
   - Prioritize issues by impact

4. **Decide What to Do** (15 min)
   - Choose 1-3 improvement actions
   - Assign owners to each action
   - Define success criteria
   - Set follow-up date

5. **Close** (5 min)
   - Summarize decisions
   - Appreciate team contributions
   - Document retro outcomes

**Output:** Retrospective notes with 1-3 committed improvement actions.

### Workflow 5: Velocity Tracking

**Steps:**
1. Calculate completed story points per sprint
2. Track velocity over rolling 3-sprint average
3. Identify velocity trends (increasing, stable, declining)
4. Analyze factors affecting velocity
5. Use velocity for future sprint planning

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Plan new sprint | "plan sprint [number]" |
| Calculate capacity | "calculate team capacity" |
| Check velocity | "what's our velocity" |
| Create sprint goal | "set sprint goal" |
| Daily standup | "daily standup update" |
| Review sprint | "sprint review" |
| Run retrospective | "facilitate retro" |
| Burndown chart | "show sprint burndown" |
| Add to sprint | "add story to sprint" |
| Sprint health | "sprint health check" |

## Best Practices

- **Consistent sprint length**: Use 1-2 week sprints; consistency enables predictability
- **Sprint goal clarity**: Every sprint needs a clear, measurable goal that guides decisions
- **Capacity-based planning**: Never commit to more than 70% of theoretical capacity
- **No scope changes mid-sprint**: Protect the sprint commitment; changes go to backlog
- **Done means DONE**: Define "Definition of Done" and enforce it (coded, tested, reviewed, deployed)
- **Track velocity honestly**: Don't manipulate story points; accurate data enables better planning
- **Time-box ceremonies**: Sprint planning (2h), daily standup (15min), review (1h), retro (1h)
- **Visualize progress**: Use burndown charts and sprint boards for transparency
- **Address blockers daily**: Don't let blockers linger; escalate and resolve quickly
- **Retrospect every sprint**: Continuous improvement is non-negotiable
- **Protect team from interruptions**: Buffer capacity for support, bugs, and unplanned work
- **Carry over sparingly**: If stories regularly carry over, you're over-committing

## Sprint Ceremonies Schedule

| Ceremony | Duration | When | Purpose |
|----------|----------|------|---------|
| **Sprint Planning** | 2-4 hours | First day of sprint | Define sprint goal and commitment |
| **Daily Standup** | 15 minutes | Every day, same time | Sync progress and blockers |
| **Backlog Grooming** | 1 hour | Mid-sprint | Prepare upcoming work |
| **Sprint Review** | 1 hour | Last day of sprint | Demo and gather feedback |
| **Sprint Retrospective** | 1 hour | After review | Reflect and improve |

## Velocity Calculation

**Story Points Method:**
```
Velocity = Sum of completed story points

Example:
Sprint 1: 23 points
Sprint 2: 27 points
Sprint 3: 25 points
Average Velocity = (23 + 27 + 25) / 3 = 25 points/sprint
```

**Hours Method:**
```
Velocity = Completed hours / Committed hours

Example:
Committed: 80 hours
Completed: 68 hours
Velocity = 68/80 = 85% completion rate
```

Use average velocity from last 3 sprints for planning next sprint.

## Capacity Planning Formula

```
Team Capacity = Σ(Person Days Available) × Hours per Day × Utilization Factor

Example:
5 developers × 10 days × 6 hours/day × 0.7 = 210 hours

Utilization Factor (0.7) accounts for:
- Meetings and ceremonies (15%)
- Context switching (10%)
- Unplanned work (5%)
```

## Burndown Chart Analysis

**Healthy Burndown:**
- Steady downward trend
- Work completed daily
- Reaches zero by sprint end

**Warning Signs:**
- Flat line (no progress)
- Upward trend (scope added)
- Late drop (work completed last day)
- Staying above zero (over-committed)

## Retrospective Formats

### Start/Stop/Continue
- **Start**: What should we start doing?
- **Stop**: What should we stop doing?
- **Continue**: What should we keep doing?

### 4 L's
- **Liked**: What went well?
- **Learned**: What did we learn?
- **Lacked**: What was missing?
- **Longed For**: What do we wish we had?

### Mad/Sad/Glad
- **Mad**: What frustrated us?
- **Sad**: What disappointed us?
- **Glad**: What made us happy?

### Sailboat
- **Wind**: What helped us move forward?
- **Anchor**: What held us back?
- **Rocks**: What risks did we face?
- **Island**: What's our goal?

## Integration Points

- **Task Manager**: Daily task tracking and updates
- **Project Planner**: Long-term roadmap alignment
- **GitHub**: Issue and PR tracking
- **Jira/Linear**: Sprint board management
- **Slack**: Automated standup reminders and updates
- **Calendar**: Sprint ceremony scheduling
