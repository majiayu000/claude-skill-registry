---
name: capacity-planning
description: Analyze team capacity, plan resource allocation, and balance workload across projects. Forecast staffing needs and optimize team utilization while maintaining sustainable pace.
---

# Capacity Planning

## Overview

Capacity planning ensures teams have sufficient resources to deliver work at sustainable pace, prevents burnout, and enables accurate commitment to stakeholders.

## When to Use

- Annual or quarterly planning cycles
- Allocating people to projects
- Adjusting team size
- Planning for holidays and absences
- Forecasting resource needs
- Balancing multiple projects
- Identifying bottlenecks

## Instructions

### 1. **Capacity Assessment**

```python
# Team capacity calculation and planning

class CapacityPlanner:
    # Standard work hours per week
    STANDARD_WEEK_HOURS = 40

    # Activities that reduce available capacity
    OVERHEAD_HOURS = {
        'meetings': 5,           # standups, 1-on-1s, planning
        'training': 2,           # learning new tech
        'administrative': 2,     # emails, approvals
        'support': 2,            # helping teammates
        'contingency': 2         # interruptions, emergencies
    }

    def __init__(self, team_size, sprint_duration_weeks=2):
        self.team_size = team_size
        self.sprint_duration_weeks = sprint_duration_weeks
        self.members = []

    def calculate_team_capacity(self):
        """Calculate available capacity hours"""
        # Base capacity
        base_hours = self.team_size * self.STANDARD_WEEK_HOURS * self.sprint_duration_weeks

        # Subtract overhead
        overhead = sum(self.OVERHEAD_HOURS.values()) * self.team_size * self.sprint_duration_weeks

        # Subtract absences
        absence_hours = self.calculate_absences()

        # Available capacity
        available_capacity = base_hours - overhead - absence_hours

        return {
            'base_hours': base_hours,
            'overhead_hours': overhead,
            'absence_hours': absence_hours,
            'available_capacity': available_capacity,
            'utilization_target': '85%',  # Leave 15% buffer
            'target_commitment': available_capacity * 0.85
        }

    def calculate_absences(self):
        """Account for vacation, sick, etc."""
        absence_days = 0

        # Standard absences
        vacation_days = 15  # annual
        sick_days = 5       # annual
        holidays = 10       # annual

        # Convert to per-sprint
        absence_days = (vacation_days + sick_days + holidays) / 52 * self.sprint_duration_weeks

        absence_hours = absence_days * 8 * self.team_size
        return absence_hours

    def allocate_to_projects(self, projects, team):
        """Allocate capacity across multiple projects"""
        allocation = {}
        total_allocation = 0

        # Allocate by priority
        for project in sorted(projects, key=lambda p: p.priority):
            required_hours = project.effort_hours
            available = self.calculate_team_capacity()['available_capacity'] - total_allocation

            if available >= required_hours:
                allocation[project.id] = {
                    'project': project.name,
                    'allocated': required_hours,
                    'team_members': int(required_hours / (self.STANDARD_WEEK_HOURS * self.sprint_duration_weeks)),
                    'allocation_percent': (required_hours / available * 100)
                }
                total_allocation += required_hours
            else:
                allocation[project.id] = {
                    'project': project.name,
                    'allocated': available,
                    'status': 'Insufficient capacity',
                    'shortfall': required_hours - available,
                    'recommendation': 'Add resources or defer scope'
                }
                total_allocation = available

        return allocation

    def identify_bottlenecks(self, skills, projects):
        """Find skill constraints"""
        bottlenecks = []

        for skill in skills:
            people_with_skill = sum(1 for p in self.members if skill in p.skills)
            projects_needing_skill = sum(1 for p in projects if skill in p.required_skills)

            utilization = (projects_needing_skill / people_with_skill * 100) if people_with_skill > 0 else 0

            if utilization > 100:
                bottlenecks.append({
                    'skill': skill,
                    'people_available': people_with_skill,
                    'projects_needing': projects_needing_skill,
                    'utilization': utilization,
                    'severity': 'Critical',
                    'actions': ['Cross-train team', 'Hire specialist', 'Adjust scope']
                })

        return bottlenecks
```

### 2. **Capacity Planning Template**

```yaml
Capacity Plan for Q1 2025:

Team: Platform Engineering (12 people)
Period: January 1 - March 31, 2025
Planned Duration: 13 weeks

---

## Team Composition

Engineers:
  - Senior Engineers: 3 (1.2 FTE each)
  - Mid-Level Engineers: 6 (0.95 FTE each)
  - Junior Engineers: 2 (0.8 FTE each)
  - DevOps: 1 (1.0 FTE)

Total Available FTE: 11.1 (accounting for overhead, absences)
Total Available Hours: 11.1 * 40 * 13 = 5,772 hours

---

## Planned Absences

Vacation: 8 weeks across team (estimated)
Sick/Personal: 2 weeks across team
Holiday: 1 week (MLK, Presidents Day)
Total: ~480 hours

---

## Capacity Allocation

Project A: Critical Infrastructure
  Allocation: 60% (6,600 hours needed)
  Team: 3 senior, 3 mid-level engineers
  FTE: 6.6
  Status: Committed

Project B: Feature Development
  Allocation: 30% (3,300 hours needed)
  Team: 2 mid-level, 2 junior engineers
  FTE: 3.3
  Status: Committed

Infrastructure & Maintenance:
  Allocation: 10% (1,100 hours)
  Team: DevOps, 1 senior engineer
  FTE: 1.1
  Status: Operational capacity

Total: 100% allocation, 0% buffer

---

## Risk Assessment

Risks:
  1. Zero buffer capacity (100% allocation)
     Impact: Any absence/issue creates crisis
     Mitigation: Cross-training, automation

  2. Junior engineer ramp-up time
     Impact: Mid-level engineers pulled for mentoring
     Mitigation: Assign 1 mentoring hour/week

  3. Infrastructure bottleneck (1 DevOps)
     Impact: Scaling limitations
     Mitigation: Hire additional DevOps by Feb 1

---

## Recommendations

1. Reduce capacity planning from 100% to 85%
2. Hire 1 additional DevOps engineer
3. Cross-train 2 engineers on critical systems
4. Schedule vacations strategically (not during Phase 2)
5. Build 15% buffer for emergencies
```

### 3. **Resource Leveling**

```javascript
// Balance workload across team members

class ResourceLeveling {
  levelWorkload(team, tasks) {
    const workloadByPerson = {};

    // Initialize team member workload
    team.forEach(person => {
      workloadByPerson[person.id] = {
        name: person.name,
        skills: person.skills,
        capacity: person.capacity_hours,
        assigned: [],
        utilization: 0
      };
    });

    // Assign tasks to balance workload
    const sortedTasks = tasks.sort((a, b) => b.effort - a.effort); // Largest first

    sortedTasks.forEach(task => {
      const suitable = team.filter(p =>
        this.hasSufficientSkills(p.skills, task.required_skills) &&
        this.hasCapacity(workloadByPerson[p.id].utilization, p.capacity_hours)
      );

      if (suitable.length > 0) {
        const leastUtilized = suitable.reduce((a, b) =>
          workloadByPerson[a.id].utilization < workloadByPerson[b.id].utilization ? a : b
        );

        workloadByPerson[leastUtilized.id].assigned.push(task);
        workloadByPerson[leastUtilized.id].utilization += task.effort;
      }
    });

    return {
      assignments: workloadByPerson,
      balanceMetrics: this.calculateBalance(workloadByPerson),
      unassignedTasks: tasks.filter(t => !Object.values(workloadByPerson).some(p => p.assigned.includes(t)))
    };
  }

  calculateBalance(workloadByPerson) {
    const utilizations = Object.values(workloadByPerson).map(p => p.utilization);
    const average = utilizations.reduce((a, b) => a + b) / utilizations.length;
    const variance = Math.sqrt(
      utilizations.reduce((sum, u) => sum + Math.pow(u - average, 2)) / utilizations.length
    );

    return {
      average_utilization: average.toFixed(1),
      std_deviation: variance.toFixed(1),
      balance_score: this.calculateBalanceScore(variance),
      recommendations: this.getBalancingRecommendations(variance)
    };
  }

  calculateBalanceScore(variance) {
    if (variance < 5) return 'Excellent';
    if (variance < 10) return 'Good';
    if (variance < 15) return 'Fair';
    return 'Poor - needs rebalancing';
  }
}
```

### 4. **Capacity Forecasting**

```yaml
12-Month Capacity Forecast:

Team Growth Plan:
  Q1 2025: 12 people (current)
  Q2 2025: 13 people (hire 1 DevOps)
  Q3 2025: 15 people (hire 2 engineers)
  Q4 2025: 15 people (stable)

Monthly Capacity (FTE):

January 2025: 10.8 FTE (below normal - ramp-up)
February 2025: 11.1 FTE (normal)
March 2025: 11.0 FTE (1 person on leave)

Q2 Average: 12.5 FTE (new hire contributing)
Q3 Average: 14.2 FTE (2 new hires)
Q4 Average: 15.0 FTE (all at full capacity)

---

Project Commitments vs. Available Capacity:

Q1: Committed 11.0 FTE, Available 11.1 FTE (safe)
Q2: Committed 12.0 FTE, Available 12.5 FTE (buffer 4%)
Q3: Committed 13.0 FTE, Available 14.2 FTE (buffer 9%)
Q4: Committed 14.0 FTE, Available 15.0 FTE (buffer 7%)

---

Risk Alerts:
  - Q1 is tight (98% utilized)
  - Skill gap: Backend expertise in Q2
  - Attrition risk: Plan for 1 departure in Q3
```

## Best Practices

### ✅ DO
- Plan capacity at 85% utilization (15% buffer)
- Account for meetings, training, and overhead
- Include known absences (vacation, holidays)
- Identify skill bottlenecks early
- Balance workload fairly across team
- Review capacity monthly
- Adjust plans based on actual velocity
- Cross-train on critical skills
- Communicate realistic commitments to stakeholders
- Build contingency for emergencies

### ❌ DON'T
- Plan at 100% utilization
- Ignore meetings and overhead
- Assign work without checking skills
- Create overload with continuous surprises
- Forget about learning/training time
- Leave capacity planning to last minute
- Overcommit team consistently
- Burn out key people
- Ignore team feedback on workload
- Plan without considering absences

## Capacity Planning Tips

- Use velocity data from past sprints
- Track actual vs. planned utilization
- Review capacity weekly in standups
- Maintain 15% buffer for emergencies
- Cross-train on critical functions
