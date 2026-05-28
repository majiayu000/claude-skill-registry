---
name: "resource-allocation-optimizer"
description: "Optimize construction resource allocation across activities. Level resources, resolve over-allocations, and balance workload while minimizing schedule impact."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⏱️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Resource Allocation Optimizer

## Overview

Optimize resource allocation in construction schedules. Level workforce and equipment utilization, resolve over-allocations, and balance workload across the project duration.

> "Resource leveling reduces peak demand by 30% and improves productivity" — DDC Community

## Resource Leveling Concept

```
Before Leveling:                    After Leveling:
Workers                             Workers
  20│    ████                         15│  ████████████
  15│  ████████                        10│████████████████
  10│████████████                       5│████████████████████
   5│██████████████████                 0└──────────────────────
   0└────────────────────                  Week 1  2  3  4  5  6
      Week 1  2  3  4  5
                                       Peak reduced, duration extended
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import heapq

@dataclass
class Resource:
    id: str
    name: str
    resource_type: str  # labor, equipment, material
    capacity: float  # units available per day
    cost_per_unit: float = 0.0
    skills: List[str] = field(default_factory=list)

@dataclass
class ResourceAssignment:
    activity_id: str
    resource_id: str
    units: float  # units required per day
    start_day: int
    end_day: int

@dataclass
class Activity:
    id: str
    name: str
    duration: int
    early_start: int
    late_start: int
    total_float: int
    resource_requirements: Dict[str, float] = field(default_factory=dict)
    is_critical: bool = False

@dataclass
class ResourceProfile:
    resource_id: str
    daily_usage: Dict[int, float]  # day -> units used
    peak_usage: float
    average_usage: float
    utilization_rate: float

@dataclass
class LevelingResult:
    original_duration: int
    new_duration: int
    activities_shifted: List[Tuple[str, int, int]]  # (id, old_start, new_start)
    resource_profiles: Dict[str, ResourceProfile]
    peak_reduction: Dict[str, float]

class ResourceOptimizer:
    """Optimize construction resource allocation."""

    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        self.activities: Dict[str, Activity] = {}
        self.assignments: List[ResourceAssignment] = []

    def add_resource(self, id: str, name: str, resource_type: str,
                    capacity: float, cost_per_unit: float = 0.0,
                    skills: List[str] = None) -> Resource:
        """Add resource to pool."""
        resource = Resource(
            id=id,
            name=name,
            resource_type=resource_type,
            capacity=capacity,
            cost_per_unit=cost_per_unit,
            skills=skills or []
        )
        self.resources[id] = resource
        return resource

    def add_activity(self, id: str, name: str, duration: int,
                    early_start: int, late_start: int,
                    resource_requirements: Dict[str, float] = None,
                    is_critical: bool = False) -> Activity:
        """Add activity with resource requirements."""
        activity = Activity(
            id=id,
            name=name,
            duration=duration,
            early_start=early_start,
            late_start=late_start,
            total_float=late_start - early_start,
            resource_requirements=resource_requirements or {},
            is_critical=is_critical
        )
        self.activities[id] = activity

        # Create assignments
        for res_id, units in activity.resource_requirements.items():
            assignment = ResourceAssignment(
                activity_id=id,
                resource_id=res_id,
                units=units,
                start_day=early_start,
                end_day=early_start + duration
            )
            self.assignments.append(assignment)

        return activity

    def calculate_resource_profile(self, resource_id: str,
                                  activity_starts: Dict[str, int] = None) -> ResourceProfile:
        """Calculate daily resource usage profile."""
        if resource_id not in self.resources:
            raise ValueError(f"Resource {resource_id} not found")

        resource = self.resources[resource_id]
        daily_usage = defaultdict(float)

        # Use provided starts or early starts
        starts = activity_starts or {act.id: act.early_start for act in self.activities.values()}

        for assignment in self.assignments:
            if assignment.resource_id != resource_id:
                continue

            act_start = starts.get(assignment.activity_id, assignment.start_day)
            act = self.activities[assignment.activity_id]

            for day in range(act_start, act_start + act.duration):
                daily_usage[day] += assignment.units

        usage_values = list(daily_usage.values()) if daily_usage else [0]
        project_duration = max(daily_usage.keys()) + 1 if daily_usage else 0

        return ResourceProfile(
            resource_id=resource_id,
            daily_usage=dict(daily_usage),
            peak_usage=max(usage_values),
            average_usage=sum(usage_values) / len(usage_values) if usage_values else 0,
            utilization_rate=sum(usage_values) / (project_duration * resource.capacity) if project_duration else 0
        )

    def identify_overallocations(self) -> Dict[str, List[Tuple[int, float]]]:
        """Identify days where resources are over-allocated."""
        overallocations = {}

        for resource in self.resources.values():
            profile = self.calculate_resource_profile(resource.id)
            over_days = [
                (day, usage - resource.capacity)
                for day, usage in profile.daily_usage.items()
                if usage > resource.capacity
            ]
            if over_days:
                overallocations[resource.id] = over_days

        return overallocations

    def level_resources(self, resource_ids: List[str] = None,
                       allow_duration_extension: bool = True,
                       max_extension_days: int = 30) -> LevelingResult:
        """Level resources by shifting non-critical activities."""
        resource_ids = resource_ids or list(self.resources.keys())

        # Store original starts
        original_starts = {act.id: act.early_start for act in self.activities.values()}
        original_duration = max(act.early_start + act.duration for act in self.activities.values())

        # Current activity starts (will be modified)
        current_starts = dict(original_starts)

        # Sort activities by float (most float = most flexibility)
        sorted_activities = sorted(
            [a for a in self.activities.values() if not a.is_critical],
            key=lambda a: -a.total_float
        )

        activities_shifted = []

        # Iteratively resolve overallocations
        for _ in range(100):  # Max iterations
            overallocations = self._check_overallocations(current_starts, resource_ids)

            if not overallocations:
                break

            # Find activity to shift
            shifted = False
            for act in sorted_activities:
                if act.id in [o[0] for o in overallocations]:
                    # Try to shift this activity
                    new_start = self._find_valid_start(
                        act, current_starts, resource_ids,
                        allow_duration_extension, max_extension_days
                    )

                    if new_start is not None and new_start != current_starts[act.id]:
                        old_start = current_starts[act.id]
                        current_starts[act.id] = new_start
                        activities_shifted.append((act.id, old_start, new_start))
                        shifted = True
                        break

            if not shifted:
                break

        # Calculate new duration and profiles
        new_duration = max(
            current_starts[act.id] + act.duration
            for act in self.activities.values()
        )

        resource_profiles = {}
        peak_reduction = {}

        for res_id in resource_ids:
            original_profile = self.calculate_resource_profile(res_id, original_starts)
            new_profile = self.calculate_resource_profile(res_id, current_starts)
            resource_profiles[res_id] = new_profile
            peak_reduction[res_id] = original_profile.peak_usage - new_profile.peak_usage

        return LevelingResult(
            original_duration=original_duration,
            new_duration=new_duration,
            activities_shifted=activities_shifted,
            resource_profiles=resource_profiles,
            peak_reduction=peak_reduction
        )

    def _check_overallocations(self, starts: Dict[str, int],
                               resource_ids: List[str]) -> List[Tuple[str, int, str]]:
        """Check for overallocations with given starts."""
        overallocations = []

        for res_id in resource_ids:
            resource = self.resources[res_id]
            daily_usage = defaultdict(list)

            for assignment in self.assignments:
                if assignment.resource_id != res_id:
                    continue

                act = self.activities[assignment.activity_id]
                act_start = starts[assignment.activity_id]

                for day in range(act_start, act_start + act.duration):
                    daily_usage[day].append((assignment.activity_id, assignment.units))

            for day, activities in daily_usage.items():
                total = sum(units for _, units in activities)
                if total > resource.capacity:
                    for act_id, _ in activities:
                        overallocations.append((act_id, day, res_id))

        return overallocations

    def _find_valid_start(self, activity: Activity, current_starts: Dict[str, int],
                         resource_ids: List[str], allow_extension: bool,
                         max_extension: int) -> Optional[int]:
        """Find valid start day that doesn't cause overallocation."""
        min_start = activity.early_start
        max_start = activity.late_start if not allow_extension else activity.late_start + max_extension

        for start in range(min_start, max_start + 1):
            # Check if this start causes overallocation
            test_starts = dict(current_starts)
            test_starts[activity.id] = start

            overallocations = self._check_overallocations(test_starts, resource_ids)
            activity_over = [o for o in overallocations if o[0] == activity.id]

            if not activity_over:
                return start

        return None

    def optimize_for_cost(self, target_duration: int = None) -> Dict:
        """Optimize resource allocation for minimum cost."""
        # Calculate baseline cost
        baseline_cost = self._calculate_total_cost()

        # Try different allocation strategies
        strategies = []

        # Strategy 1: Minimize overtime
        overtime_result = self._minimize_overtime()
        strategies.append({
            "strategy": "Minimize Overtime",
            "cost": overtime_result["cost"],
            "duration": overtime_result["duration"]
        })

        # Strategy 2: Level resources
        level_result = self.level_resources()
        level_cost = self._calculate_total_cost(
            {act.id: act.early_start for act in self.activities.values()}
        )
        strategies.append({
            "strategy": "Level Resources",
            "cost": level_cost,
            "duration": level_result.new_duration
        })

        return {
            "baseline_cost": baseline_cost,
            "strategies": strategies,
            "recommended": min(strategies, key=lambda s: s["cost"])
        }

    def _calculate_total_cost(self, starts: Dict[str, int] = None) -> float:
        """Calculate total resource cost."""
        starts = starts or {act.id: act.early_start for act in self.activities.values()}
        total_cost = 0.0

        for res_id, resource in self.resources.items():
            profile = self.calculate_resource_profile(res_id, starts)

            for day, usage in profile.daily_usage.items():
                # Regular cost
                regular_units = min(usage, resource.capacity)
                total_cost += regular_units * resource.cost_per_unit

                # Overtime cost (1.5x)
                overtime_units = max(0, usage - resource.capacity)
                total_cost += overtime_units * resource.cost_per_unit * 1.5

        return total_cost

    def _minimize_overtime(self) -> Dict:
        """Minimize overtime by resource leveling."""
        result = self.level_resources(allow_duration_extension=True)
        cost = self._calculate_total_cost(
            {act.id: act.early_start for act in self.activities.values()}
        )
        return {"cost": cost, "duration": result.new_duration}

    def generate_resource_histogram(self, resource_id: str,
                                   starts: Dict[str, int] = None) -> str:
        """Generate ASCII histogram of resource usage."""
        profile = self.calculate_resource_profile(resource_id, starts)
        resource = self.resources[resource_id]

        if not profile.daily_usage:
            return "No usage data"

        max_day = max(profile.daily_usage.keys())
        max_usage = max(profile.daily_usage.values())

        lines = [
            f"# Resource Histogram: {resource.name}",
            f"Capacity: {resource.capacity} | Peak: {profile.peak_usage}",
            ""
        ]

        # Scale for display
        scale = 20 / max_usage if max_usage > 0 else 1

        for day in range(max_day + 1):
            usage = profile.daily_usage.get(day, 0)
            bar_len = int(usage * scale)
            over = "!" if usage > resource.capacity else " "
            lines.append(f"Day {day:3d}: {'█' * bar_len}{over} ({usage:.1f})")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize optimizer
optimizer = ResourceOptimizer()

# Add resources
optimizer.add_resource("CARP", "Carpenters", "labor", capacity=10, cost_per_unit=450)
optimizer.add_resource("IRON", "Ironworkers", "labor", capacity=8, cost_per_unit=550)
optimizer.add_resource("CRANE", "Tower Crane", "equipment", capacity=1, cost_per_unit=2500)

# Add activities with resource requirements
optimizer.add_activity(
    "A", "Foundation Forms", duration=10,
    early_start=0, late_start=0,
    resource_requirements={"CARP": 8},
    is_critical=True
)
optimizer.add_activity(
    "B", "Rebar Installation", duration=8,
    early_start=5, late_start=10,
    resource_requirements={"IRON": 6, "CRANE": 1}
)
optimizer.add_activity(
    "C", "Steel Erection", duration=15,
    early_start=10, late_start=10,
    resource_requirements={"IRON": 10, "CRANE": 1},
    is_critical=True
)

# Check for overallocations
overallocations = optimizer.identify_overallocations()
for res_id, days in overallocations.items():
    print(f"{res_id} over-allocated on days: {[d[0] for d in days]}")

# Level resources
result = optimizer.level_resources()
print(f"Duration change: {result.original_duration} → {result.new_duration} days")
print(f"Activities shifted: {len(result.activities_shifted)}")

for res_id, reduction in result.peak_reduction.items():
    print(f"{res_id} peak reduced by: {reduction:.1f} units")

# Generate histogram
print(optimizer.generate_resource_histogram("IRON"))
```

## Requirements

```bash
pip install (no external dependencies)
```
