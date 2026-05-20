---
name: "look-ahead-scheduler"
description: "Generate rolling look-ahead schedules for construction. Create 2-week, 3-week, or 6-week look-aheads with constraint analysis and crew coordination."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⏱️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Look-Ahead Scheduler

## Overview

Generate rolling look-ahead schedules from the master schedule. Create actionable short-term plans with constraint analysis, crew assignments, and daily coordination.

> "Look-ahead planning catches 80% of schedule problems before they occur" — DDC Community

## Look-Ahead Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOOK-AHEAD PLANNING                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Master Schedule (12+ months)                                    │
│       ↓                                                         │
│  Phase Schedule (3-6 months)                                    │
│       ↓                                                         │
│  6-Week Look-Ahead (make-ready)                                 │
│       ↓                                                         │
│  3-Week Look-Ahead (constraint removal)                         │
│       ↓                                                         │
│  Weekly Work Plan (commitment)                                  │
│       ↓                                                         │
│  Daily Coordination                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

class ConstraintType(Enum):
    PREDECESSOR = "predecessor"
    LABOR = "labor"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    INFORMATION = "information"
    PERMIT = "permit"
    INSPECTION = "inspection"
    SPACE = "space"
    WEATHER = "weather"

class ConstraintStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    BLOCKED = "blocked"

class ActivityStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    DELAYED = "delayed"

@dataclass
class Constraint:
    id: str
    activity_id: str
    constraint_type: ConstraintType
    description: str
    responsible_party: str
    needed_by: datetime
    status: ConstraintStatus = ConstraintStatus.OPEN
    resolution_notes: str = ""
    resolved_date: Optional[datetime] = None

@dataclass
class LookAheadActivity:
    id: str
    name: str
    trade: str
    location: str
    planned_start: datetime
    planned_finish: datetime
    duration: int
    labor_hours: float
    crew_size: int
    predecessors: List[str] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    status: ActivityStatus = ActivityStatus.NOT_STARTED
    percent_complete: float = 0.0
    notes: str = ""
    can_start: bool = False

@dataclass
class WeeklyWorkPlan:
    week_start: datetime
    week_end: datetime
    activities: List[LookAheadActivity]
    total_labor_hours: float
    trades_involved: List[str]
    constraints_to_resolve: List[Constraint]

@dataclass
class DailyPlan:
    date: datetime
    activities: List[LookAheadActivity]
    labor_by_trade: Dict[str, int]
    equipment_needed: List[str]
    inspections: List[str]
    safety_focus: str

class LookAheadScheduler:
    """Generate rolling look-ahead schedules."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.activities: Dict[str, LookAheadActivity] = {}
        self.constraints: Dict[str, Constraint] = {}
        self.weekly_plans: List[WeeklyWorkPlan] = []

    def import_from_master(self, master_activities: List[Dict],
                          look_ahead_start: datetime,
                          look_ahead_weeks: int = 6) -> int:
        """Import activities from master schedule for look-ahead period."""
        look_ahead_end = look_ahead_start + timedelta(weeks=look_ahead_weeks)
        count = 0

        for act in master_activities:
            start = datetime.fromisoformat(act['planned_start']) if isinstance(act['planned_start'], str) else act['planned_start']
            finish = datetime.fromisoformat(act['planned_finish']) if isinstance(act['planned_finish'], str) else act['planned_finish']

            # Include if overlaps look-ahead period
            if start <= look_ahead_end and finish >= look_ahead_start:
                activity = LookAheadActivity(
                    id=act['id'],
                    name=act['name'],
                    trade=act.get('trade', ''),
                    location=act.get('location', ''),
                    planned_start=start,
                    planned_finish=finish,
                    duration=act.get('duration', (finish - start).days),
                    labor_hours=act.get('labor_hours', 0),
                    crew_size=act.get('crew_size', 0),
                    predecessors=act.get('predecessors', [])
                )
                self.activities[activity.id] = activity
                count += 1

        return count

    def add_constraint(self, activity_id: str, constraint_type: ConstraintType,
                      description: str, responsible_party: str,
                      needed_by: datetime) -> Constraint:
        """Add constraint to activity."""
        constraint_id = f"CON-{len(self.constraints)+1:04d}"

        constraint = Constraint(
            id=constraint_id,
            activity_id=activity_id,
            constraint_type=constraint_type,
            description=description,
            responsible_party=responsible_party,
            needed_by=needed_by
        )

        self.constraints[constraint_id] = constraint

        if activity_id in self.activities:
            self.activities[activity_id].constraints.append(constraint)

        return constraint

    def update_constraint(self, constraint_id: str, status: ConstraintStatus,
                         notes: str = "") -> Constraint:
        """Update constraint status."""
        if constraint_id not in self.constraints:
            raise ValueError(f"Constraint {constraint_id} not found")

        constraint = self.constraints[constraint_id]
        constraint.status = status
        constraint.resolution_notes = notes

        if status == ConstraintStatus.RESOLVED:
            constraint.resolved_date = datetime.now()

        return constraint

    def analyze_make_ready(self) -> Dict[str, List[str]]:
        """Analyze which activities are 'make-ready' (constraints resolved)."""
        ready = []
        not_ready = []
        blocked = []

        for act in self.activities.values():
            # Check predecessors complete
            pred_complete = all(
                self.activities.get(p, {}).status == ActivityStatus.COMPLETE
                for p in act.predecessors if p in self.activities
            )

            # Check constraints resolved
            open_constraints = [c for c in act.constraints
                              if c.status != ConstraintStatus.RESOLVED]

            if not pred_complete:
                blocked.append(act.id)
                act.can_start = False
            elif open_constraints:
                not_ready.append(act.id)
                act.can_start = False
            else:
                ready.append(act.id)
                act.can_start = True

        return {
            "ready": ready,
            "not_ready": not_ready,
            "blocked": blocked
        }

    def generate_weekly_plan(self, week_start: datetime) -> WeeklyWorkPlan:
        """Generate weekly work plan."""
        week_end = week_start + timedelta(days=6)

        # Get activities for this week
        week_activities = [
            act for act in self.activities.values()
            if act.planned_start <= week_end and act.planned_finish >= week_start
        ]

        # Calculate totals
        total_hours = sum(act.labor_hours for act in week_activities)
        trades = list(set(act.trade for act in week_activities if act.trade))

        # Get constraints needing resolution this week
        constraints_due = [
            c for c in self.constraints.values()
            if c.status == ConstraintStatus.OPEN and c.needed_by <= week_end
        ]

        plan = WeeklyWorkPlan(
            week_start=week_start,
            week_end=week_end,
            activities=week_activities,
            total_labor_hours=total_hours,
            trades_involved=trades,
            constraints_to_resolve=constraints_due
        )

        self.weekly_plans.append(plan)
        return plan

    def generate_daily_plan(self, date: datetime) -> DailyPlan:
        """Generate daily coordination plan."""
        # Get activities for this day
        day_activities = [
            act for act in self.activities.values()
            if act.planned_start <= date <= act.planned_finish
            and act.can_start
        ]

        # Labor by trade
        labor_by_trade = defaultdict(int)
        for act in day_activities:
            labor_by_trade[act.trade] += act.crew_size

        # Equipment needed
        equipment = []
        for act in day_activities:
            for c in act.constraints:
                if c.constraint_type == ConstraintType.EQUIPMENT:
                    equipment.append(c.description)

        # Inspections
        inspections = [
            c.description for c in self.constraints.values()
            if c.constraint_type == ConstraintType.INSPECTION
            and c.needed_by.date() == date.date()
        ]

        # Safety focus based on activities
        safety_focus = self._determine_safety_focus(day_activities)

        return DailyPlan(
            date=date,
            activities=day_activities,
            labor_by_trade=dict(labor_by_trade),
            equipment_needed=equipment,
            inspections=inspections,
            safety_focus=safety_focus
        )

    def _determine_safety_focus(self, activities: List[LookAheadActivity]) -> str:
        """Determine daily safety focus based on activities."""
        # Keywords to safety topics
        keywords = {
            "excavation": "Excavation Safety - Shoring, sloping, access",
            "steel": "Steel Erection - Fall protection, crane safety",
            "concrete": "Concrete Pour - Silica, formwork, PPE",
            "roof": "Fall Protection - 100% tie-off, guardrails",
            "electrical": "Electrical Safety - LOTO, qualified personnel",
            "crane": "Crane Safety - Rigging, load charts, signaling",
            "welding": "Hot Work - Fire watch, permits, ventilation"
        }

        for act in activities:
            name_lower = act.name.lower()
            for keyword, safety in keywords.items():
                if keyword in name_lower:
                    return safety

        return "General Site Safety - PPE, housekeeping, awareness"

    def generate_look_ahead_report(self, weeks: int = 3) -> str:
        """Generate look-ahead schedule report."""
        self.analyze_make_ready()
        today = datetime.now()

        lines = [
            f"# {weeks}-Week Look-Ahead Schedule",
            f"",
            f"**Project:** {self.project_name}",
            f"**Generated:** {today.strftime('%Y-%m-%d')}",
            f"**Period:** {today.strftime('%Y-%m-%d')} to {(today + timedelta(weeks=weeks)).strftime('%Y-%m-%d')}",
            f"",
        ]

        # Summary
        make_ready = self.analyze_make_ready()
        lines.extend([
            f"## Summary",
            f"",
            f"- **Total Activities:** {len(self.activities)}",
            f"- **Ready to Start:** {len(make_ready['ready'])}",
            f"- **Awaiting Constraints:** {len(make_ready['not_ready'])}",
            f"- **Blocked:** {len(make_ready['blocked'])}",
            f""
        ])

        # Open constraints
        open_constraints = [c for c in self.constraints.values()
                          if c.status == ConstraintStatus.OPEN]
        if open_constraints:
            lines.extend([
                f"## Open Constraints ({len(open_constraints)})",
                f"",
                f"| Activity | Type | Description | Responsible | Needed By |",
                f"|----------|------|-------------|-------------|-----------|"
            ])
            for c in sorted(open_constraints, key=lambda x: x.needed_by):
                lines.append(
                    f"| {c.activity_id} | {c.constraint_type.value} | {c.description} | "
                    f"{c.responsible_party} | {c.needed_by.strftime('%Y-%m-%d')} |"
                )
            lines.append("")

        # Weekly breakdown
        for week_num in range(weeks):
            week_start = today + timedelta(weeks=week_num)
            week_start = week_start - timedelta(days=week_start.weekday())  # Monday

            plan = self.generate_weekly_plan(week_start)

            lines.extend([
                f"## Week {week_num + 1}: {plan.week_start.strftime('%b %d')} - {plan.week_end.strftime('%b %d')}",
                f"",
                f"**Activities:** {len(plan.activities)} | **Labor:** {plan.total_labor_hours:.0f} hrs | **Trades:** {', '.join(plan.trades_involved)}",
                f""
            ])

            if plan.activities:
                lines.append("| Activity | Trade | Location | Start | Duration | Status |")
                lines.append("|----------|-------|----------|-------|----------|--------|")
                for act in sorted(plan.activities, key=lambda a: a.planned_start):
                    status = "Ready" if act.can_start else "Constraint"
                    lines.append(
                        f"| {act.name} | {act.trade} | {act.location} | "
                        f"{act.planned_start.strftime('%m/%d')} | {act.duration}d | {status} |"
                    )
                lines.append("")

        return "\n".join(lines)

    def get_constraint_log(self) -> str:
        """Generate constraint log."""
        lines = [
            "# Constraint Log",
            "",
            "| ID | Activity | Type | Description | Responsible | Status | Needed By |",
            "|----|----------|------|-------------|-------------|--------|-----------|"
        ]

        for c in sorted(self.constraints.values(), key=lambda x: x.needed_by):
            lines.append(
                f"| {c.id} | {c.activity_id} | {c.constraint_type.value} | "
                f"{c.description} | {c.responsible_party} | {c.status.value} | "
                f"{c.needed_by.strftime('%Y-%m-%d')} |"
            )

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize scheduler
scheduler = LookAheadScheduler("Office Tower Construction")

# Import activities from master schedule
master_activities = [
    {
        "id": "A100",
        "name": "Level 5 MEP Rough-in",
        "trade": "Mechanical",
        "location": "Level 5",
        "planned_start": datetime.now(),
        "planned_finish": datetime.now() + timedelta(days=10),
        "labor_hours": 400,
        "crew_size": 5
    },
    {
        "id": "A101",
        "name": "Level 5 Framing",
        "trade": "Carpentry",
        "location": "Level 5",
        "planned_start": datetime.now() + timedelta(days=5),
        "planned_finish": datetime.now() + timedelta(days=15),
        "labor_hours": 320,
        "crew_size": 4,
        "predecessors": ["A100"]
    }
]

scheduler.import_from_master(master_activities, datetime.now(), look_ahead_weeks=6)

# Add constraints
scheduler.add_constraint(
    "A100",
    ConstraintType.MATERIAL,
    "Ductwork delivery",
    "ABC Mechanical",
    datetime.now() + timedelta(days=2)
)

scheduler.add_constraint(
    "A101",
    ConstraintType.INFORMATION,
    "Framing layout drawings",
    "Architect",
    datetime.now() + timedelta(days=4)
)

# Analyze make-ready status
status = scheduler.analyze_make_ready()
print(f"Ready: {len(status['ready'])}, Not Ready: {len(status['not_ready'])}")

# Generate look-ahead report
print(scheduler.generate_look_ahead_report(weeks=3))

# Generate daily plan
daily = scheduler.generate_daily_plan(datetime.now())
print(f"Today's safety focus: {daily.safety_focus}")
```

## Requirements

```bash
pip install (no external dependencies)
```
