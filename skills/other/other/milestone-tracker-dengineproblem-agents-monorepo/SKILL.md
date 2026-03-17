---
name: milestone-tracker
description: Эксперт по отслеживанию milestones. Используй для трекинга прогресса, critical path, статус-репортов и earned value.
---

# Milestone Tracker Expert

Expert in milestone tracking, project progress monitoring, and critical path analysis for comprehensive project management.

## Core Principles

### SMART Milestone Definition
- **Specific**: Clear, unambiguous deliverable
- **Measurable**: Quantifiable completion criteria
- **Achievable**: Realistic given resources and constraints
- **Relevant**: Aligned with project objectives
- **Time-bound**: Specific deadline

### Milestone vs Task
```yaml
distinction:
  milestone:
    definition: "Significant checkpoint marking phase completion"
    characteristics:
      - "Zero duration (point in time)"
      - "Binary (complete or not)"
      - "Stakeholder visible"
      - "Often gates next phase"
    examples:
      - "Requirements approved"
      - "MVP deployed to production"
      - "Beta testing complete"

  task:
    definition: "Work item with duration"
    characteristics:
      - "Has duration"
      - "Can be % complete"
      - "May be internal only"
      - "Contributes to milestones"
    examples:
      - "Develop user authentication"
      - "Write test cases"
      - "Review security requirements"
```

## Milestone Structure Template

```yaml
milestone_definition:
  id: "MS-001"
  name: "MVP Launch"
  description: "Minimum viable product deployed to production environment"

  timing:
    baseline_date: "2024-06-30"
    current_target: "2024-07-15"
    actual_date: null
    variance_days: 15
    variance_status: "Yellow"

  ownership:
    accountable: "Product Manager"
    responsible: "Engineering Lead"
    consulted: ["QA Lead", "DevOps"]
    informed: ["Executive Sponsor", "Stakeholders"]

  dependencies:
    predecessors:
      - id: "MS-000"
        name: "Development Complete"
        type: "Finish-to-Start"
        lag: 0

    successors:
      - id: "MS-002"
        name: "Beta Program Start"
        type: "Start-to-Start"
        lag: 5

  acceptance_criteria:
    - criterion: "All P1 features functional"
      verification: "Feature checklist sign-off"
      verifier: "Product Manager"
      status: "Pending"

    - criterion: "No critical bugs"
      verification: "Bug tracker query"
      verifier: "QA Lead"
      status: "Pending"

    - criterion: "Performance benchmarks met"
      verification: "Load test results"
      verifier: "DevOps"
      status: "Pending"

    - criterion: "Security scan passed"
      verification: "Security report"
      verifier: "Security Team"
      status: "Pending"

  risks:
    - risk: "Third-party API integration delay"
      probability: "Medium"
      impact: "High"
      mitigation: "Parallel development with mock API"
      owner: "Tech Lead"

    - risk: "Resource availability"
      probability: "Low"
      impact: "Medium"
      mitigation: "Cross-training team members"
      owner: "Project Manager"

  deliverables:
    - name: "Production deployment"
      type: "System"
      location: "AWS Production Environment"

    - name: "Release notes"
      type: "Document"
      location: "Confluence"

    - name: "User documentation"
      type: "Document"
      location: "Help center"

  sign_off:
    required_approvers:
      - role: "Product Manager"
        status: "Pending"
        date: null

      - role: "Engineering Lead"
        status: "Pending"
        date: null

      - role: "QA Lead"
        status: "Pending"
        date: null
```

## Critical Path Analysis

### CPM Algorithm Implementation

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
import heapq

@dataclass
class Activity:
    id: str
    name: str
    duration: int  # days
    predecessors: List[str]
    early_start: int = 0
    early_finish: int = 0
    late_start: int = 0
    late_finish: int = 0
    total_float: int = 0
    free_float: int = 0
    is_critical: bool = False

class CriticalPathCalculator:
    def __init__(self, activities: List[Activity]):
        self.activities = {a.id: a for a in activities}
        self.successors: Dict[str, List[str]] = {a.id: [] for a in activities}

        for activity in activities:
            for pred in activity.predecessors:
                self.successors[pred].append(activity.id)

    def calculate(self) -> List[str]:
        """Calculate critical path and return list of critical activity IDs."""
        self._forward_pass()
        self._backward_pass()
        self._calculate_float()

        return [aid for aid, a in self.activities.items() if a.is_critical]

    def _forward_pass(self):
        """Calculate early start and early finish times."""
        # Topological sort
        in_degree = {aid: len(a.predecessors) for aid, a in self.activities.items()}
        queue = [aid for aid, d in in_degree.items() if d == 0]

        while queue:
            current_id = queue.pop(0)
            current = self.activities[current_id]

            # Early finish = Early start + Duration
            current.early_finish = current.early_start + current.duration

            # Update successors
            for succ_id in self.successors[current_id]:
                succ = self.activities[succ_id]
                succ.early_start = max(succ.early_start, current.early_finish)
                in_degree[succ_id] -= 1
                if in_degree[succ_id] == 0:
                    queue.append(succ_id)

    def _backward_pass(self):
        """Calculate late start and late finish times."""
        # Find project duration
        project_duration = max(a.early_finish for a in self.activities.values())

        # Initialize late finish for activities with no successors
        for aid, a in self.activities.items():
            if not self.successors[aid]:
                a.late_finish = project_duration
                a.late_start = a.late_finish - a.duration

        # Reverse topological sort
        out_degree = {aid: len(self.successors[aid]) for aid in self.activities}
        queue = [aid for aid, d in out_degree.items() if d == 0]
        processed = set()

        while queue:
            current_id = queue.pop(0)
            current = self.activities[current_id]
            processed.add(current_id)

            for pred_id in current.predecessors:
                pred = self.activities[pred_id]
                if pred.late_finish == 0 or current.late_start < pred.late_finish:
                    pred.late_finish = current.late_start
                    pred.late_start = pred.late_finish - pred.duration

                # Check if all successors processed
                if all(s in processed for s in self.successors[pred_id]):
                    if pred_id not in queue:
                        queue.append(pred_id)

    def _calculate_float(self):
        """Calculate float values and identify critical activities."""
        for activity in self.activities.values():
            activity.total_float = activity.late_start - activity.early_start
            activity.is_critical = activity.total_float == 0

            # Free float calculation
            if self.successors[activity.id]:
                min_early_start = min(
                    self.activities[s].early_start
                    for s in self.successors[activity.id]
                )
                activity.free_float = min_early_start - activity.early_finish
            else:
                activity.free_float = activity.total_float

# Usage example
activities = [
    Activity("A", "Requirements", 10, []),
    Activity("B", "Design", 15, ["A"]),
    Activity("C", "Development", 30, ["B"]),
    Activity("D", "Testing", 10, ["C"]),
    Activity("E", "Documentation", 5, ["B"]),
    Activity("F", "Deployment", 5, ["D", "E"]),
]

cpm = CriticalPathCalculator(activities)
critical_path = cpm.calculate()

print("Critical Path:", critical_path)
for aid, activity in cpm.activities.items():
    print(f"{activity.name}: ES={activity.early_start}, EF={activity.early_finish}, "
          f"LS={activity.late_start}, LF={activity.late_finish}, "
          f"TF={activity.total_float}, Critical={activity.is_critical}")
```

## Earned Value Management

### EVM Calculations

```yaml
earned_value_metrics:
  baseline_metrics:
    BAC: "Budget at Completion - Total planned budget"
    PV: "Planned Value - Budgeted cost of work scheduled"

  actual_metrics:
    AC: "Actual Cost - Cost incurred for work performed"
    EV: "Earned Value - Budgeted cost of work performed"

  variance_metrics:
    CV:
      formula: "EV - AC"
      interpretation: "Positive = under budget"

    SV:
      formula: "EV - PV"
      interpretation: "Positive = ahead of schedule"

  performance_indices:
    CPI:
      formula: "EV / AC"
      interpretation: "1.0 = on budget, >1.0 = under budget"
      threshold:
        green: ">= 0.95"
        yellow: "0.85 - 0.94"
        red: "< 0.85"

    SPI:
      formula: "EV / PV"
      interpretation: "1.0 = on schedule, >1.0 = ahead"
      threshold:
        green: ">= 0.95"
        yellow: "0.85 - 0.94"
        red: "< 0.85"

  forecasting:
    EAC_typical:
      formula: "BAC / CPI"
      use_when: "Current performance expected to continue"

    EAC_atypical:
      formula: "AC + (BAC - EV)"
      use_when: "Variance was one-time, future on plan"

    EAC_composite:
      formula: "AC + [(BAC - EV) / (CPI × SPI)]"
      use_when: "Both cost and schedule performance impact future"

    ETC:
      formula: "EAC - AC"
      interpretation: "Estimate to Complete remaining work"

    VAC:
      formula: "BAC - EAC"
      interpretation: "Variance at Completion"

    TCPI:
      formula: "(BAC - EV) / (BAC - AC)"
      interpretation: "Required performance to meet budget"
```

### EVM Implementation

```python
from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class EVMSnapshot:
    date: datetime.date
    planned_value: float
    earned_value: float
    actual_cost: float
    bac: float  # Budget at Completion

    @property
    def cost_variance(self) -> float:
        """CV = EV - AC"""
        return self.earned_value - self.actual_cost

    @property
    def schedule_variance(self) -> float:
        """SV = EV - PV"""
        return self.earned_value - self.planned_value

    @property
    def cpi(self) -> Optional[float]:
        """Cost Performance Index = EV / AC"""
        if self.actual_cost == 0:
            return None
        return self.earned_value / self.actual_cost

    @property
    def spi(self) -> Optional[float]:
        """Schedule Performance Index = EV / PV"""
        if self.planned_value == 0:
            return None
        return self.earned_value / self.planned_value

    @property
    def eac_typical(self) -> Optional[float]:
        """Estimate at Completion (typical variance)"""
        if self.cpi is None or self.cpi == 0:
            return None
        return self.bac / self.cpi

    @property
    def eac_composite(self) -> Optional[float]:
        """Estimate at Completion (composite)"""
        if self.cpi is None or self.spi is None:
            return None
        if self.cpi * self.spi == 0:
            return None
        return self.actual_cost + (self.bac - self.earned_value) / (self.cpi * self.spi)

    @property
    def etc(self) -> Optional[float]:
        """Estimate to Complete"""
        eac = self.eac_typical
        if eac is None:
            return None
        return eac - self.actual_cost

    @property
    def vac(self) -> Optional[float]:
        """Variance at Completion"""
        eac = self.eac_typical
        if eac is None:
            return None
        return self.bac - eac

    @property
    def percent_complete(self) -> float:
        """Progress percentage"""
        if self.bac == 0:
            return 0
        return (self.earned_value / self.bac) * 100

    @property
    def tcpi(self) -> Optional[float]:
        """To-Complete Performance Index"""
        remaining_work = self.bac - self.earned_value
        remaining_budget = self.bac - self.actual_cost
        if remaining_budget == 0:
            return None
        return remaining_work / remaining_budget

    def status_report(self) -> dict:
        """Generate status summary"""
        return {
            "date": self.date.isoformat(),
            "progress": {
                "percent_complete": round(self.percent_complete, 1),
                "planned_value": self.planned_value,
                "earned_value": self.earned_value,
                "actual_cost": self.actual_cost,
            },
            "variances": {
                "cost_variance": round(self.cost_variance, 2),
                "schedule_variance": round(self.schedule_variance, 2),
                "cv_status": "Under" if self.cost_variance >= 0 else "Over",
                "sv_status": "Ahead" if self.schedule_variance >= 0 else "Behind",
            },
            "indices": {
                "cpi": round(self.cpi, 2) if self.cpi else None,
                "spi": round(self.spi, 2) if self.spi else None,
            },
            "forecasts": {
                "eac_typical": round(self.eac_typical, 2) if self.eac_typical else None,
                "etc": round(self.etc, 2) if self.etc else None,
                "vac": round(self.vac, 2) if self.vac else None,
            },
            "health": self._calculate_health(),
        }

    def _calculate_health(self) -> str:
        """Determine overall project health"""
        cpi = self.cpi or 0
        spi = self.spi or 0

        if cpi >= 0.95 and spi >= 0.95:
            return "Green"
        elif cpi >= 0.85 and spi >= 0.85:
            return "Yellow"
        else:
            return "Red"
```

## Status Reporting

### Traffic Light System

```yaml
status_indicators:
  green:
    criteria:
      schedule: "On track or ahead (variance < 5%)"
      budget: "On track or under (variance < 5%)"
      scope: "No changes or approved changes only"
      risks: "All risks mitigated or low impact"
    action: "Continue monitoring"

  yellow:
    criteria:
      schedule: "5-15% behind"
      budget: "5-15% over"
      scope: "Pending change requests"
      risks: "Medium risks requiring attention"
    action: "Corrective action needed"

  red:
    criteria:
      schedule: ">15% behind"
      budget: ">15% over"
      scope: "Uncontrolled scope changes"
      risks: "High risks threatening success"
    action: "Escalation required"
```

### Weekly Status Report Template

```yaml
weekly_status_report:
  header:
    project_name: "Project Alpha"
    report_date: "2024-03-15"
    reporting_period: "2024-03-08 to 2024-03-14"
    project_manager: "Jane Smith"
    report_number: 12

  executive_summary:
    overall_status: "Yellow"
    summary: |
      Project is 5 days behind schedule due to third-party API
      integration delays. Recovery plan in place with expected
      return to schedule by March 29.

    key_messages:
      - "MVP features 85% complete"
      - "API integration issue being resolved"
      - "Additional QA resources approved"

  milestone_status:
    completed_this_period:
      - name: "UI Design Complete"
        planned: "2024-03-10"
        actual: "2024-03-08"
        variance: "-2 days"

    upcoming_milestones:
      - name: "API Integration Complete"
        planned: "2024-03-15"
        forecast: "2024-03-20"
        variance: "+5 days"
        status: "Yellow"
        risk: "Dependency on vendor fix"

      - name: "Beta Release"
        planned: "2024-03-25"
        forecast: "2024-03-29"
        variance: "+4 days"
        status: "Yellow"
        risk: "Dependent on API completion"

  progress_metrics:
    schedule:
      planned_progress: "75%"
      actual_progress: "70%"
      spi: 0.93
      status: "Yellow"

    budget:
      planned_spend: "$150,000"
      actual_spend: "$145,000"
      cpi: 1.03
      status: "Green"

    scope:
      total_requirements: 45
      completed: 38
      in_progress: 5
      not_started: 2
      status: "Green"

  accomplishments:
    - "Completed all frontend components"
    - "Passed security audit"
    - "Onboarded 2 additional developers"
    - "Resolved 15 defects"

  planned_next_period:
    - "Complete API integration"
    - "Begin end-to-end testing"
    - "Finalize user documentation"
    - "Prepare beta environment"

  issues_and_risks:
    active_issues:
      - id: "ISS-023"
        description: "Third-party API returning incorrect data"
        severity: "High"
        owner: "Tech Lead"
        action: "Vendor ticket escalated, workaround in dev"
        target_resolution: "2024-03-18"

    risks:
      - id: "RSK-012"
        description: "Beta testers availability"
        probability: "Medium"
        impact: "Medium"
        mitigation: "Recruiting backup testers"
        owner: "Product Manager"

  decisions_needed:
    - decision: "Approve 2-week schedule extension"
      deadline: "2024-03-18"
      decision_maker: "Steering Committee"

  resource_status:
    planned_fte: 8
    actual_fte: 9
    changes: "+1 QA engineer added"
    concerns: "None"
```

## Agile Integration

### Sprint-Milestone Alignment

```yaml
agile_milestone_mapping:
  release_planning:
    release: "v2.0"
    target_date: "2024-06-30"
    sprints: 6
    sprint_duration: "2 weeks"

    milestones:
      - milestone: "Feature Complete"
        sprint: 4
        date: "2024-05-17"
        criteria: "All user stories in Done"

      - milestone: "Code Freeze"
        sprint: 5
        date: "2024-05-31"
        criteria: "Only bug fixes after this"

      - milestone: "Release Candidate"
        sprint: 6
        date: "2024-06-14"
        criteria: "RC deployed to staging"

      - milestone: "Production Release"
        sprint: 6
        date: "2024-06-30"
        criteria: "Deployed to production"

  sprint_tracking:
    sprint: 3
    goal: "Complete user authentication and profile features"

    story_points:
      committed: 34
      completed: 28
      spillover: 6

    velocity:
      current: 28
      average: 30
      trend: "Stable"

    burndown:
      day_1: 34
      day_5: 22
      day_10: 6
      actual_vs_ideal: "Slightly behind"
```

### Epic Progress Tracking

```yaml
epic_milestone_tracker:
  epic: "User Management System"
  status: "In Progress"

  milestones:
    - name: "User Registration Live"
      target: "Sprint 2"
      status: "Complete"
      features:
        - "Email registration"
        - "Social login (Google, GitHub)"
        - "Email verification"

    - name: "Profile Management Live"
      target: "Sprint 3"
      status: "In Progress"
      features:
        - "View/edit profile (Done)"
        - "Avatar upload (Done)"
        - "Privacy settings (In Progress)"

    - name: "Admin Controls Live"
      target: "Sprint 4"
      status: "Not Started"
      features:
        - "User search"
        - "Role management"
        - "Bulk operations"

  metrics:
    story_points_total: 89
    story_points_done: 55
    percent_complete: 62
    remaining_sprints: 2
    on_track: true
```

## Tool Integration

### Jira Configuration

```yaml
jira_milestone_setup:
  custom_fields:
    - name: "Milestone"
      type: "Select List (single choice)"
      options:
        - "MS1: Requirements Complete"
        - "MS2: Design Complete"
        - "MS3: Development Complete"
        - "MS4: Testing Complete"
        - "MS5: Release"

    - name: "Milestone Date"
      type: "Date Picker"

    - name: "Milestone Status"
      type: "Select List (single choice)"
      options:
        - "On Track"
        - "At Risk"
        - "Delayed"
        - "Complete"

  filters:
    milestone_view:
      jql: "project = PROJ AND 'Milestone' is not EMPTY ORDER BY 'Milestone Date' ASC"

    at_risk_milestones:
      jql: "project = PROJ AND 'Milestone Status' = 'At Risk'"

  dashboard_gadgets:
    - type: "Filter Results"
      filter: "Upcoming Milestones"
      columns: ["Key", "Summary", "Milestone", "Milestone Date", "Status"]

    - type: "Two Dimensional Filter Statistics"
      x_axis: "Milestone"
      y_axis: "Status"
```

### Gantt Chart Data Structure

```python
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class GanttTask:
    id: str
    name: str
    start_date: date
    end_date: date
    progress: float  # 0-100
    dependencies: List[str]
    is_milestone: bool = False
    color: Optional[str] = None
    resource: Optional[str] = None

def generate_gantt_data(milestones: List[dict]) -> List[GanttTask]:
    """Convert milestone data to Gantt chart format."""
    tasks = []

    for ms in milestones:
        task = GanttTask(
            id=ms['id'],
            name=ms['name'],
            start_date=ms['baseline_date'] if ms['is_milestone']
                       else ms['start_date'],
            end_date=ms['baseline_date'] if ms['is_milestone']
                     else ms['end_date'],
            progress=100 if ms['status'] == 'Complete' else ms.get('progress', 0),
            dependencies=ms.get('predecessors', []),
            is_milestone=ms['is_milestone'],
            color=_status_to_color(ms['status']),
            resource=ms.get('owner')
        )
        tasks.append(task)

    return tasks

def _status_to_color(status: str) -> str:
    colors = {
        'Complete': '#4CAF50',
        'On Track': '#2196F3',
        'At Risk': '#FFC107',
        'Delayed': '#F44336',
        'Not Started': '#9E9E9E'
    }
    return colors.get(status, '#9E9E9E')
```

## Лучшие практики

1. **SMART milestones** — конкретные, измеримые, достижимые, релевантные, ограниченные во времени
2. **Clear ownership** — каждый milestone должен иметь ответственного
3. **Regular updates** — обновляйте статус минимум еженедельно
4. **Earned value** — используйте EVM для объективной оценки прогресса
5. **Critical path focus** — приоритизируйте задачи на критическом пути
6. **Risk buffers** — закладывайте contingency для сложных milestones
