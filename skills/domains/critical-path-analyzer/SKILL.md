---
name: "critical-path-analyzer"
description: "Analyze construction schedule critical path. Identify critical activities, calculate float, simulate schedule impacts, and optimize project duration."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⏱️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Critical Path Analyzer

## Overview

Analyze construction schedules using Critical Path Method (CPM). Identify critical activities, calculate total and free float, simulate what-if scenarios, and find opportunities to compress schedule.

> "Understanding the critical path is essential for effective schedule management" — DDC Community

## CPM Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRITICAL PATH METHOD                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Activity A (5d)  ──→  Activity C (10d)  ──→  Activity E (3d)   │
│       ↓                                            ↑             │
│  Activity B (8d)  ──────────→  Activity D (6d)  ───┘            │
│                                                                  │
│  Critical Path: A → C → E (18 days)                             │
│  Float on B→D: 4 days                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import heapq

@dataclass
class Activity:
    id: str
    name: str
    duration: int  # days
    predecessors: List[str] = field(default_factory=list)
    successors: List[str] = field(default_factory=list)

    # Calculated values
    early_start: int = 0
    early_finish: int = 0
    late_start: int = 0
    late_finish: int = 0
    total_float: int = 0
    free_float: int = 0
    is_critical: bool = False

    # Optional attributes
    resources: List[str] = field(default_factory=list)
    cost: float = 0.0
    actual_start: Optional[datetime] = None
    actual_finish: Optional[datetime] = None
    percent_complete: float = 0.0

@dataclass
class ScheduleAnalysis:
    project_duration: int
    critical_path: List[str]
    critical_activities: List[Activity]
    near_critical_activities: List[Activity]  # Float <= threshold
    total_activities: int
    float_distribution: Dict[int, int]

class CriticalPathAnalyzer:
    """Analyze construction schedule critical path."""

    def __init__(self):
        self.activities: Dict[str, Activity] = {}
        self.analysis: Optional[ScheduleAnalysis] = None

    def add_activity(self, id: str, name: str, duration: int,
                    predecessors: List[str] = None,
                    resources: List[str] = None,
                    cost: float = 0.0) -> Activity:
        """Add activity to schedule."""
        activity = Activity(
            id=id,
            name=name,
            duration=duration,
            predecessors=predecessors or [],
            resources=resources or [],
            cost=cost
        )
        self.activities[id] = activity

        # Update successor relationships
        for pred_id in activity.predecessors:
            if pred_id in self.activities:
                self.activities[pred_id].successors.append(id)

        return activity

    def import_schedule(self, activities: List[Dict]) -> int:
        """Import activities from list of dicts."""
        count = 0
        for act in activities:
            self.add_activity(
                id=act['id'],
                name=act['name'],
                duration=act['duration'],
                predecessors=act.get('predecessors', []),
                resources=act.get('resources', []),
                cost=act.get('cost', 0)
            )
            count += 1
        return count

    def calculate_critical_path(self, near_critical_threshold: int = 5) -> ScheduleAnalysis:
        """Calculate critical path using forward and backward pass."""
        if not self.activities:
            raise ValueError("No activities to analyze")

        # Reset calculations
        for act in self.activities.values():
            act.early_start = 0
            act.early_finish = 0
            act.late_start = 0
            act.late_finish = 0
            act.total_float = 0
            act.free_float = 0
            act.is_critical = False

        # Forward pass - calculate early start/finish
        self._forward_pass()

        # Determine project duration
        project_duration = max(act.early_finish for act in self.activities.values())

        # Backward pass - calculate late start/finish
        self._backward_pass(project_duration)

        # Calculate float and identify critical activities
        critical_path = []
        critical_activities = []
        near_critical = []

        for act in self.activities.values():
            act.total_float = act.late_start - act.early_start

            # Calculate free float
            if act.successors:
                min_succ_es = min(self.activities[s].early_start for s in act.successors)
                act.free_float = min_succ_es - act.early_finish
            else:
                act.free_float = project_duration - act.early_finish

            # Identify critical (zero float)
            if act.total_float == 0:
                act.is_critical = True
                critical_activities.append(act)
            elif act.total_float <= near_critical_threshold:
                near_critical.append(act)

        # Build critical path sequence
        critical_path = self._build_critical_path_sequence(critical_activities)

        # Float distribution
        float_dist = defaultdict(int)
        for act in self.activities.values():
            float_dist[act.total_float] += 1

        self.analysis = ScheduleAnalysis(
            project_duration=project_duration,
            critical_path=critical_path,
            critical_activities=critical_activities,
            near_critical_activities=near_critical,
            total_activities=len(self.activities),
            float_distribution=dict(float_dist)
        )

        return self.analysis

    def _forward_pass(self):
        """Forward pass to calculate early start/finish."""
        # Topological sort
        in_degree = {act_id: len(act.predecessors) for act_id, act in self.activities.items()}
        queue = [act_id for act_id, degree in in_degree.items() if degree == 0]

        while queue:
            act_id = queue.pop(0)
            act = self.activities[act_id]

            # Early start is max of predecessor early finishes
            if act.predecessors:
                act.early_start = max(
                    self.activities[pred].early_finish for pred in act.predecessors
                )
            else:
                act.early_start = 0

            act.early_finish = act.early_start + act.duration

            # Process successors
            for succ_id in act.successors:
                in_degree[succ_id] -= 1
                if in_degree[succ_id] == 0:
                    queue.append(succ_id)

    def _backward_pass(self, project_duration: int):
        """Backward pass to calculate late start/finish."""
        # Start from end activities
        end_activities = [act for act in self.activities.values() if not act.successors]

        for act in end_activities:
            act.late_finish = project_duration
            act.late_start = act.late_finish - act.duration

        # Process in reverse topological order
        processed = set(act.id for act in end_activities)
        queue = list(end_activities)

        while queue:
            act = queue.pop(0)

            for pred_id in act.predecessors:
                pred = self.activities[pred_id]

                # Late finish is min of successor late starts
                new_late_finish = act.late_start
                if pred.late_finish == 0 or new_late_finish < pred.late_finish:
                    pred.late_finish = new_late_finish
                    pred.late_start = pred.late_finish - pred.duration

                # Check if all successors processed
                all_succ_processed = all(
                    s in processed for s in pred.successors
                )
                if all_succ_processed and pred_id not in processed:
                    processed.add(pred_id)
                    queue.append(pred)

    def _build_critical_path_sequence(self, critical_activities: List[Activity]) -> List[str]:
        """Build ordered critical path sequence."""
        if not critical_activities:
            return []

        # Find start of critical path (no critical predecessors)
        critical_ids = {act.id for act in critical_activities}

        start_acts = [act for act in critical_activities
                     if not any(p in critical_ids for p in act.predecessors)]

        if not start_acts:
            return [act.id for act in critical_activities]

        # Build sequence
        path = []
        current = start_acts[0]

        while current:
            path.append(current.id)
            # Find next critical successor
            critical_successors = [s for s in current.successors if s in critical_ids]
            current = self.activities[critical_successors[0]] if critical_successors else None

        return path

    def simulate_delay(self, activity_id: str, delay_days: int) -> Dict:
        """Simulate impact of delay on an activity."""
        if activity_id not in self.activities:
            raise ValueError(f"Activity {activity_id} not found")

        activity = self.activities[activity_id]
        original_duration = activity.duration

        # Temporarily modify duration
        activity.duration = original_duration + delay_days

        # Recalculate
        new_analysis = self.calculate_critical_path()

        # Restore original
        activity.duration = original_duration
        original_analysis = self.calculate_critical_path()

        impact = {
            "activity": activity_id,
            "delay_days": delay_days,
            "original_duration": self.analysis.project_duration,
            "new_duration": new_analysis.project_duration,
            "project_impact": new_analysis.project_duration - original_analysis.project_duration,
            "absorbed_by_float": delay_days <= activity.total_float,
            "new_critical_path": new_analysis.critical_path,
            "critical_path_changed": new_analysis.critical_path != original_analysis.critical_path
        }

        return impact

    def find_compression_opportunities(self, target_reduction: int) -> List[Dict]:
        """Find activities that could be crashed to reduce duration."""
        if not self.analysis:
            self.calculate_critical_path()

        opportunities = []

        for act in self.analysis.critical_activities:
            # Assume activities can be crashed by 20% max
            max_crash = int(act.duration * 0.2)
            if max_crash > 0:
                opportunities.append({
                    "activity_id": act.id,
                    "activity_name": act.name,
                    "current_duration": act.duration,
                    "max_crash_days": max_crash,
                    "crash_cost_per_day": act.cost * 0.5 / max_crash if max_crash else 0,
                    "on_critical_path": True
                })

        # Sort by crash cost
        opportunities.sort(key=lambda x: x["crash_cost_per_day"])

        return opportunities

    def get_float_report(self) -> str:
        """Generate float analysis report."""
        if not self.analysis:
            self.calculate_critical_path()

        lines = [
            "# Float Analysis Report",
            "",
            f"**Project Duration:** {self.analysis.project_duration} days",
            f"**Critical Activities:** {len(self.analysis.critical_activities)}",
            f"**Near-Critical Activities:** {len(self.analysis.near_critical_activities)}",
            "",
            "## Critical Path",
            "",
            " → ".join(self.analysis.critical_path),
            "",
            "## Activities by Float",
            "",
            "| Activity | Duration | ES | EF | LS | LF | TF | FF | Critical |",
            "|----------|----------|----|----|----|----|----|----|----------|"
        ]

        # Sort by float
        sorted_acts = sorted(self.activities.values(), key=lambda a: a.total_float)

        for act in sorted_acts:
            crit = "YES" if act.is_critical else ""
            lines.append(
                f"| {act.id} | {act.duration} | {act.early_start} | {act.early_finish} | "
                f"{act.late_start} | {act.late_finish} | {act.total_float} | {act.free_float} | {crit} |"
            )

        return "\n".join(lines)

    def generate_gantt_data(self, start_date: datetime) -> List[Dict]:
        """Generate data for Gantt chart visualization."""
        gantt_data = []

        for act in self.activities.values():
            gantt_data.append({
                "id": act.id,
                "name": act.name,
                "start": (start_date + timedelta(days=act.early_start)).isoformat(),
                "end": (start_date + timedelta(days=act.early_finish)).isoformat(),
                "duration": act.duration,
                "float": act.total_float,
                "is_critical": act.is_critical,
                "predecessors": act.predecessors,
                "progress": act.percent_complete
            })

        return gantt_data
```

## Quick Start

```python
# Initialize analyzer
analyzer = CriticalPathAnalyzer()

# Add activities
analyzer.add_activity("A", "Site Prep", 5)
analyzer.add_activity("B", "Foundation Excavation", 8, predecessors=["A"])
analyzer.add_activity("C", "Foundation Forms", 4, predecessors=["B"])
analyzer.add_activity("D", "Foundation Pour", 2, predecessors=["C"])
analyzer.add_activity("E", "Foundation Cure", 7, predecessors=["D"])
analyzer.add_activity("F", "Steel Erection", 15, predecessors=["E"])
analyzer.add_activity("G", "MEP Rough-in", 20, predecessors=["F"])
analyzer.add_activity("H", "Exterior Envelope", 25, predecessors=["F"])
analyzer.add_activity("I", "Interior Finishes", 30, predecessors=["G", "H"])
analyzer.add_activity("J", "Final Inspection", 3, predecessors=["I"])

# Calculate critical path
analysis = analyzer.calculate_critical_path()

print(f"Project Duration: {analysis.project_duration} days")
print(f"Critical Path: {' → '.join(analysis.critical_path)}")
print(f"Critical Activities: {len(analysis.critical_activities)}")

# Simulate delay
impact = analyzer.simulate_delay("F", 5)
print(f"\nDelay Impact: {impact['project_impact']} days")
print(f"Absorbed by Float: {impact['absorbed_by_float']}")

# Find compression opportunities
opportunities = analyzer.find_compression_opportunities(10)
for opp in opportunities[:3]:
    print(f"Crash {opp['activity_name']}: up to {opp['max_crash_days']} days")

# Generate report
print(analyzer.get_float_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
