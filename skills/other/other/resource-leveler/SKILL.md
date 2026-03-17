---
name: "resource-leveler"
description: "Level and optimize construction resource allocation across project schedule. Balance labor, equipment usage, and avoid overallocation while maintaining critical path."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🎬", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Resource Leveler for Construction

## Overview

Optimize resource allocation across construction schedules. Level labor and equipment to avoid peaks, balance workload, and maintain project deadlines while reducing costs.

## Business Case

Resource leveling provides:
- **Cost Reduction**: Avoid overtime and idle time
- **Workforce Stability**: Consistent crew sizes
- **Equipment Optimization**: Reduce rental costs
- **Realistic Schedules**: Achievable resource plans

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict

@dataclass
class Resource:
    id: str
    name: str
    resource_type: str  # labor, equipment, material
    max_units: float
    cost_per_unit: float
    unit: str  # hours, days, each

@dataclass
class ResourceAssignment:
    task_id: str
    resource_id: str
    units: float
    start_date: date
    end_date: date

@dataclass
class Task:
    id: str
    name: str
    duration: int  # days
    start_date: date
    end_date: date
    predecessors: List[str]
    total_float: int
    is_critical: bool
    resource_assignments: List[ResourceAssignment] = field(default_factory=list)

@dataclass
class LevelingResult:
    success: bool
    original_end_date: date
    leveled_end_date: date
    tasks_moved: int
    peak_reduction: Dict[str, float]
    warnings: List[str]

class ConstructionResourceLeveler:
    """Level resources across construction schedules."""

    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        self.tasks: Dict[str, Task] = {}
        self.assignments: List[ResourceAssignment] = []

    def add_resource(self, resource: Resource):
        """Add a resource to the pool."""
        self.resources[resource.id] = resource

    def add_task(self, task: Task):
        """Add a task to the schedule."""
        self.tasks[task.id] = task

    def add_assignment(self, assignment: ResourceAssignment):
        """Assign a resource to a task."""
        self.assignments.append(assignment)
        if assignment.task_id in self.tasks:
            self.tasks[assignment.task_id].resource_assignments.append(assignment)

    def calculate_resource_usage(self, start_date: date = None,
                                  end_date: date = None) -> pd.DataFrame:
        """Calculate daily resource usage."""
        if not self.assignments:
            return pd.DataFrame()

        # Determine date range
        if start_date is None:
            start_date = min(a.start_date for a in self.assignments)
        if end_date is None:
            end_date = max(a.end_date for a in self.assignments)

        # Create date range
        dates = pd.date_range(start_date, end_date, freq='D')

        # Initialize usage matrix
        usage = {r_id: [0.0] * len(dates) for r_id in self.resources}

        # Fill in usage
        for assignment in self.assignments:
            if assignment.resource_id in usage:
                for i, d in enumerate(dates):
                    if assignment.start_date <= d.date() <= assignment.end_date:
                        usage[assignment.resource_id][i] += assignment.units

        df = pd.DataFrame(usage, index=dates)
        df.index.name = 'date'

        return df

    def identify_overallocations(self) -> List[Dict]:
        """Identify resource overallocations."""
        usage = self.calculate_resource_usage()
        overallocations = []

        for resource_id, resource in self.resources.items():
            if resource_id in usage.columns:
                daily_usage = usage[resource_id]
                over_days = daily_usage[daily_usage > resource.max_units]

                if len(over_days) > 0:
                    overallocations.append({
                        'resource_id': resource_id,
                        'resource_name': resource.name,
                        'max_units': resource.max_units,
                        'peak_usage': daily_usage.max(),
                        'over_by': daily_usage.max() - resource.max_units,
                        'days_overallocated': len(over_days),
                        'first_overallocation': over_days.index[0].date(),
                        'worst_day': daily_usage.idxmax().date()
                    })

        return overallocations

    def level_resources(self, method: str = 'float_priority',
                        protect_critical_path: bool = True,
                        max_extension: int = 30) -> LevelingResult:
        """Level resources to resolve overallocations."""

        original_end = max(t.end_date for t in self.tasks.values())
        tasks_moved = 0
        warnings = []

        # Get initial overallocations
        initial_over = self.identify_overallocations()
        if not initial_over:
            return LevelingResult(
                success=True,
                original_end_date=original_end,
                leveled_end_date=original_end,
                tasks_moved=0,
                peak_reduction={},
                warnings=["No overallocations found"]
            )

        # Track peak usage before
        usage_before = self.calculate_resource_usage()
        peaks_before = {r: usage_before[r].max() for r in usage_before.columns}

        # Leveling loop
        iteration = 0
        max_iterations = len(self.tasks) * 2

        while iteration < max_iterations:
            iteration += 1
            overallocations = self.identify_overallocations()

            if not overallocations:
                break

            # Find task to move
            moved = False
            for over in overallocations:
                resource_id = over['resource_id']
                worst_day = over['worst_day']

                # Find tasks using this resource on worst day
                candidates = self._find_movable_tasks(
                    resource_id, worst_day, protect_critical_path
                )

                if candidates:
                    # Sort by priority (lowest float first to preserve options)
                    candidates.sort(key=lambda t: -t.total_float)
                    task_to_move = candidates[0]

                    # Calculate new dates
                    new_start, new_end = self._calculate_shift(
                        task_to_move, resource_id, max_extension
                    )

                    if new_start:
                        self._shift_task(task_to_move.id, new_start, new_end)
                        tasks_moved += 1
                        moved = True
                        break

            if not moved:
                warnings.append("Could not resolve all overallocations")
                break

        # Calculate results
        usage_after = self.calculate_resource_usage()
        peaks_after = {r: usage_after[r].max() for r in usage_after.columns}

        peak_reduction = {}
        for r in peaks_before:
            if r in peaks_after:
                reduction = (peaks_before[r] - peaks_after[r]) / peaks_before[r] * 100
                peak_reduction[r] = reduction

        leveled_end = max(t.end_date for t in self.tasks.values())

        if leveled_end > original_end + timedelta(days=max_extension):
            warnings.append(f"Project extended beyond max allowed ({max_extension} days)")

        remaining_over = self.identify_overallocations()

        return LevelingResult(
            success=len(remaining_over) == 0,
            original_end_date=original_end,
            leveled_end_date=leveled_end,
            tasks_moved=tasks_moved,
            peak_reduction=peak_reduction,
            warnings=warnings
        )

    def _find_movable_tasks(self, resource_id: str, on_date: date,
                            protect_critical: bool) -> List[Task]:
        """Find tasks that can be moved to reduce overallocation."""
        candidates = []

        for task in self.tasks.values():
            # Check if task uses this resource on this date
            uses_resource = any(
                a.resource_id == resource_id and
                a.start_date <= on_date <= a.end_date
                for a in task.resource_assignments
            )

            if not uses_resource:
                continue

            # Check if critical path protected
            if protect_critical and task.is_critical:
                continue

            # Check if has float
            if task.total_float > 0:
                candidates.append(task)

        return candidates

    def _calculate_shift(self, task: Task, resource_id: str,
                         max_extension: int) -> Tuple[date, date]:
        """Calculate optimal shift for a task."""
        resource = self.resources[resource_id]

        # Try shifting forward
        for days in range(1, min(task.total_float + 1, max_extension + 1)):
            new_start = task.start_date + timedelta(days=days)
            new_end = task.end_date + timedelta(days=days)

            # Check if this resolves overallocation
            temp_usage = self._calculate_usage_if_moved(task.id, new_start, new_end)

            if temp_usage.get(resource_id, 0) <= resource.max_units:
                return new_start, new_end

        return None, None

    def _calculate_usage_if_moved(self, task_id: str, new_start: date,
                                   new_end: date) -> Dict[str, float]:
        """Calculate resource usage if task were moved."""
        # Simplified: calculate peak on affected dates
        usage = defaultdict(float)

        for assignment in self.assignments:
            if assignment.task_id == task_id:
                # Use new dates
                for d in pd.date_range(new_start, new_end):
                    usage[assignment.resource_id] = max(
                        usage[assignment.resource_id],
                        assignment.units
                    )
            else:
                # Use existing dates
                for d in pd.date_range(assignment.start_date, assignment.end_date):
                    usage[assignment.resource_id] = max(
                        usage[assignment.resource_id],
                        assignment.units
                    )

        return dict(usage)

    def _shift_task(self, task_id: str, new_start: date, new_end: date):
        """Shift a task to new dates."""
        task = self.tasks[task_id]
        delta = new_start - task.start_date

        # Update task
        task.start_date = new_start
        task.end_date = new_end

        # Update assignments
        for assignment in self.assignments:
            if assignment.task_id == task_id:
                assignment.start_date += delta
                assignment.end_date += delta

    def optimize_crew_size(self, resource_id: str,
                            target_utilization: float = 0.85) -> Dict:
        """Recommend optimal crew size for a resource."""
        usage = self.calculate_resource_usage()

        if resource_id not in usage.columns:
            return None

        daily_usage = usage[resource_id]
        resource = self.resources[resource_id]

        # Calculate statistics
        peak = daily_usage.max()
        avg = daily_usage.mean()
        working_days = (daily_usage > 0).sum()

        # Current utilization
        current_util = avg / resource.max_units if resource.max_units > 0 else 0

        # Optimal size for target utilization
        optimal_size = avg / target_utilization

        return {
            'resource_id': resource_id,
            'current_max_units': resource.max_units,
            'peak_usage': peak,
            'average_usage': avg,
            'working_days': int(working_days),
            'current_utilization': current_util,
            'recommended_max_units': round(optimal_size, 1),
            'potential_savings': (resource.max_units - optimal_size) * resource.cost_per_unit * working_days
        }

    def generate_histogram(self, resource_id: str) -> pd.DataFrame:
        """Generate resource histogram data."""
        usage = self.calculate_resource_usage()

        if resource_id not in usage.columns:
            return pd.DataFrame()

        resource = self.resources[resource_id]

        df = pd.DataFrame({
            'date': usage.index,
            'usage': usage[resource_id].values,
            'capacity': resource.max_units,
            'overallocated': usage[resource_id].values > resource.max_units
        })

        return df

    def generate_report(self) -> str:
        """Generate resource leveling report."""
        lines = ["# Resource Leveling Report", ""]
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Resources:** {len(self.resources)}")
        lines.append(f"**Tasks:** {len(self.tasks)}")
        lines.append("")

        # Overallocations
        overallocations = self.identify_overallocations()
        if overallocations:
            lines.append("## Overallocations Found")
            for over in overallocations:
                lines.append(f"\n### {over['resource_name']}")
                lines.append(f"- **Max Units:** {over['max_units']}")
                lines.append(f"- **Peak Usage:** {over['peak_usage']}")
                lines.append(f"- **Days Overallocated:** {over['days_overallocated']}")
                lines.append(f"- **Worst Day:** {over['worst_day']}")
        else:
            lines.append("## No Overallocations")
            lines.append("All resources are within capacity.")

        # Resource utilization
        lines.append("\n## Resource Utilization")
        for resource_id in self.resources:
            opt = self.optimize_crew_size(resource_id)
            if opt:
                lines.append(f"\n### {self.resources[resource_id].name}")
                lines.append(f"- **Utilization:** {opt['current_utilization']:.1%}")
                lines.append(f"- **Peak:** {opt['peak_usage']:.1f}")
                lines.append(f"- **Average:** {opt['average_usage']:.1f}")

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import date

# Initialize leveler
leveler = ConstructionResourceLeveler()

# Add resources
leveler.add_resource(Resource(
    id="CARP",
    name="Carpenters",
    resource_type="labor",
    max_units=10,
    cost_per_unit=75,
    unit="hours"
))

# Add tasks
leveler.add_task(Task(
    id="T1",
    name="Frame Level 1",
    duration=10,
    start_date=date(2026, 3, 1),
    end_date=date(2026, 3, 14),
    predecessors=[],
    total_float=5,
    is_critical=False
))

# Add assignments
leveler.add_assignment(ResourceAssignment(
    task_id="T1",
    resource_id="CARP",
    units=8,
    start_date=date(2026, 3, 1),
    end_date=date(2026, 3, 14)
))

# Check overallocations
overallocations = leveler.identify_overallocations()
for over in overallocations:
    print(f"{over['resource_name']}: {over['peak_usage']} vs {over['max_units']} max")

# Level resources
result = leveler.level_resources(protect_critical_path=True)
print(f"Tasks moved: {result.tasks_moved}")
print(f"End date change: {result.original_end_date} -> {result.leveled_end_date}")

# Generate report
print(leveler.generate_report())
```

## Dependencies

```bash
pip install pandas numpy
```
