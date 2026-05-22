---
name: agile-sprint-planning
description: Plan and execute effective sprints using Agile methodologies. Define sprint goals, estimate user stories, manage sprint backlog, and facilitate daily standups to maximize team productivity and deliver value incrementally.
---

# Agile Sprint Planning

## Overview

Agile sprint planning provides a structured approach to organize work into time-boxed iterations, enabling teams to deliver value incrementally while maintaining flexibility and responding to change.

## When to Use

- Starting a new sprint cycle
- Defining sprint goals and objectives
- Estimating user stories and tasks
- Managing sprint backlog prioritization
- Handling mid-sprint changes or scope adjustments
- Preparing sprint reviews and retrospectives
- Training team members on Agile practices

## Instructions

### 1. **Pre-Sprint Planning**

```markdown
# Sprint Planning Checklist

## 1-2 Days Before Planning Meeting
- [ ] Groom product backlog (ensure top items are detailed)
- [ ] Update user story acceptance criteria
- [ ] Identify dependencies and blockers
- [ ] Prepare estimates from previous sprints
- [ ] Review team velocity (average story points per sprint)
- [ ] Identify team availability/absences
- [ ] Prepare sprint goals draft

## Information to Gather
- Product Owner priorities
- Team capacity (working hours available)
- Previous sprint metrics
- Upcoming holidays or interruptions
- Technical debt items to address
```

### 2. **Sprint Planning Meeting Structure**

```javascript
// Example sprint planning agenda and execution

class SprintPlanner {
  constructor(team, sprintLength = 2) {
    this.team = team;
    this.sprintLength = sprintLength; // weeks
    this.userStories = [];
    this.sprintGoal = '';
    this.capacity = 0;
  }

  calculateTeamCapacity() {
    // Capacity = available hours - meetings - buffer
    const workHours = 40; // per person per week
    const meetingHours = 5; // estimated standups, retros, etc.
    const bufferPercent = 0.2; // 20% buffer for interruptions

    const capacityPerPerson = (workHours - meetingHours) * (1 - bufferPercent);
    this.capacity = capacityPerPerson * this.team.length * this.sprintLength;

    return this.capacity;
  }

  conductPlanningMeeting() {
    return {
      part1: {
        duration: '15 minutes',
        activity: 'Product Owner presents sprint goal',
        deliverable: 'Team understands business objective'
      },
      part2: {
        duration: '45-60 minutes',
        activity: 'Team discusses and estimates user stories',
        deliverable: 'Prioritized sprint backlog with story points'
      },
      part3: {
        duration: '15 minutes',
        activity: 'Team commits to sprint goal',
        deliverable: 'Formal sprint backlog committed'
      }
    };
  }

  createSprintBacklog(stories, capacity) {
    let currentCapacity = capacity;
    const sprintBacklog = [];

    for (let story of stories) {
      if (currentCapacity >= story.points) {
        sprintBacklog.push({
          ...story,
          status: 'planned',
          sprint: this.currentSprint
        });
        currentCapacity -= story.points;
      }
    }

    return {
      goal: this.sprintGoal,
      backlog: sprintBacklog,
      remainingCapacity: currentCapacity,
      utilization: ((capacity - currentCapacity) / capacity * 100).toFixed(1) + '%'
    };
  }
}
```

### 3. **Story Point Estimation**

```python
# Story point estimation using Planning Poker approach

class StoryEstimation:
    # Fibonacci sequence for estimation
    ESTIMATE_OPTIONS = [1, 2, 3, 5, 8, 13, 21, 34]

    @staticmethod
    def calculate_story_points(complexity, effort, risk):
        """
        Estimate story points based on multiple factors
        Factors should be rated 1-5
        """
        base_points = (complexity * effort) / 5
        risk_multiplier = 1 + (risk * 0.1)
        estimated_points = base_points * risk_multiplier

        # Round to nearest Fibonacci number
        for estimate in StoryEstimation.ESTIMATE_OPTIONS:
            if estimated_points <= estimate:
                return estimate

        return StoryEstimation.ESTIMATE_OPTIONS[-1]

    @staticmethod
    def conduct_planning_poker(team_estimates):
        """
        Handle Planning Poker consensus process
        """
        estimates = sorted(team_estimates)
        median = estimates[len(estimates) // 2]

        # If significant disagreement, discuss and re-estimate
        if estimates[-1] - estimates[0] > 5:
            return {
                'consensus': False,
                'median': median,
                'low': estimates[0],
                'high': estimates[-1],
                'action': 'Discuss and re-estimate'
            }

        return {'consensus': True, 'estimate': median}

# Example usage
print(StoryEstimation.calculate_story_points(
    complexity=3,  # Medium complexity
    effort=2,      # Low effort
    risk=1         # Low risk
))  # Output: 3 points
```

### 4. **Sprint Goal Definition**

```yaml
Sprint Goal Template:

Sprint: Sprint 23 (Nov 7 - Nov 20)

Goal Statement: |
  Enable users to manage multiple payment methods with a secure,
  intuitive interface that reduces checkout time by 40%

Success Criteria:
  - Payment method management UI implemented
  - 95% test coverage on payment logic
  - Performance: <200ms payment processing
  - Zero critical security issues
  - Feature released to 20% of users for A/B testing

Team Commitment: 89 story points
Expected Velocity: 85-95 points

Key Risks:
  - Payment gateway API changes
  - Security compliance requirements
  - Integration complexity

Acceptance:
  - All criteria met
  - Feature deployed to staging
  - Security review approved
  - Team and PO sign-off
```

### 5. **Daily Standup Management**

```javascript
// Daily standup structure and tracking

class DailyStandup {
  constructor(team) {
    this.team = team;
    this.standups = [];
  }

  conductStandup(date) {
    const standup = {
      date,
      startTime: new Date(),
      participants: [],
      timeboxed: true,
      durationMinutes: 15
    };

    for (let member of this.team) {
      standup.participants.push({
        name: member.name,
        yesterday: member.getYesterdayWork(),
        today: member.getPlanForToday(),
        blockers: member.getBlockers(),
        helpNeeded: member.getHelpNeeded()
      });
    }

    return {
      standup,
      followUpActions: this.identifyFollowUps(standup),
      blockerResolutionOwners: this.assignBlockerOwners(standup)
    };
  }

  identifyFollowUps(standup) {
    return standup.participants
      .filter(p => p.blockers.length > 0)
      .map(p => ({
        owner: p.name,
        blockers: p.blockers,
        deadline: new Date(Date.now() + 24 * 60 * 60 * 1000)
      }));
  }
}
```

## Best Practices

### ✅ DO
- Base capacity on actual team velocity from past sprints
- Include buffer time for interruptions and support work
- Focus sprint goal on business value, not technical tasks
- Timeboxe planning meeting (2 hours max for 2-week sprint)
- Include entire team in planning discussion
- Break down large stories into smaller, manageable pieces
- Track story points for velocity trending
- Review and adjust estimates based on actual completion
- Maintain consistent sprint length
- Include retrospective improvements in planning

### ❌ DON'T
- Plan for 100% capacity utilization
- Skip story grooming before planning meeting
- Add stories after sprint starts (unless emergency)
- Let one person estimate for entire team
- Use story points as employee performance metrics
- Ignore team velocity trends
- Plan without clear sprint goal
- Force stories into sprints to match capacity numbers
- Skip sprint planning to save time
- Use planning poker results as final estimate without discussion

## Sprint Planning Tips

- Keep stories to 5-13 points (break larger stories down)
- Maintain 85-90% capacity utilization (leave buffer for interruptions)
- Document sprint goal visibly (physical board or Jira)
- Track velocity over 5-10 sprints to identify trends
- Use historical data for better estimates
- Celebrate sprint successes in reviews
- Identify and address estimation biases
- Adjust processes based on retrospective feedback
