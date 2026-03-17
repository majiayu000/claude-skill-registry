---
name: "schedule-compression"
description: "Compress construction schedules using crashing and fast-tracking techniques. Analyze cost-time tradeoffs and find optimal acceleration strategies."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⏱️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Schedule Compression

## Overview

Compress construction schedules when project deadlines are at risk. Apply crashing (adding resources) and fast-tracking (parallel activities) to accelerate delivery while managing cost and risk.

> "Strategic compression can recover 20% of schedule with 10% cost increase" — DDC Community

## Compression Techniques

```
┌─────────────────────────────────────────────────────────────────┐
│                  SCHEDULE COMPRESSION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CRASHING                          FAST-TRACKING                 │
│  ────────                          ─────────────                 │
│  Add resources to reduce           Overlap sequential            │
│  activity duration                 activities                    │
│                                                                  │
│  Before:  ████████ (10d)          Before:  A ──→ B ──→ C        │
│  After:   █████ (5d) + $$$         After:   A ──→ B             │
│                                              └──→ C              │
│  Cost: Higher labor/OT             Risk: Rework if A changes    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class CompressionMethod(Enum):
    CRASH = "crash"
    FAST_TRACK = "fast_track"
    HYBRID = "hybrid"

@dataclass
class Activity:
    id: str
    name: str
    normal_duration: int
    crash_duration: int  # Minimum possible duration
    normal_cost: float
    crash_cost: float  # Cost at crash duration
    predecessors: List[str] = field(default_factory=list)
    is_critical: bool = False
    current_duration: int = 0

    def __post_init__(self):
        if self.current_duration == 0:
            self.current_duration = self.normal_duration

    @property
    def crash_slope(self) -> float:
        """Cost per day of crashing."""
        duration_diff = self.normal_duration - self.crash_duration
        if duration_diff == 0:
            return float('inf')
        return (self.crash_cost - self.normal_cost) / duration_diff

    @property
    def days_available_to_crash(self) -> int:
        """Days activity can still be crashed."""
        return self.current_duration - self.crash_duration

@dataclass
class FastTrackOption:
    activity1_id: str
    activity2_id: str
    overlap_days: int
    risk_level: str  # low, medium, high
    risk_description: str
    rework_probability: float
    potential_rework_cost: float

@dataclass
class CompressionPlan:
    target_reduction: int
    achieved_reduction: int
    crash_activities: List[Tuple[str, int]]  # (activity_id, days_crashed)
    fast_track_options: List[FastTrackOption]
    total_additional_cost: float
    new_project_duration: int
    risk_assessment: str

class ScheduleCompressor:
    """Compress construction schedules using crashing and fast-tracking."""

    def __init__(self):
        self.activities: Dict[str, Activity] = {}
        self.fast_track_options: List[FastTrackOption] = []
        self.project_duration: int = 0
        self.critical_path: List[str] = []

    def add_activity(self, id: str, name: str,
                    normal_duration: int, crash_duration: int,
                    normal_cost: float, crash_cost: float,
                    predecessors: List[str] = None,
                    is_critical: bool = False) -> Activity:
        """Add activity with crash data."""
        activity = Activity(
            id=id,
            name=name,
            normal_duration=normal_duration,
            crash_duration=crash_duration,
            normal_cost=normal_cost,
            crash_cost=crash_cost,
            predecessors=predecessors or [],
            is_critical=is_critical
        )
        self.activities[id] = activity
        return activity

    def add_fast_track_option(self, activity1_id: str, activity2_id: str,
                             overlap_days: int, risk_level: str,
                             risk_description: str,
                             rework_probability: float = 0.1,
                             potential_rework_cost: float = 0) -> FastTrackOption:
        """Add fast-tracking option between activities."""
        option = FastTrackOption(
            activity1_id=activity1_id,
            activity2_id=activity2_id,
            overlap_days=overlap_days,
            risk_level=risk_level,
            risk_description=risk_description,
            rework_probability=rework_probability,
            potential_rework_cost=potential_rework_cost
        )
        self.fast_track_options.append(option)
        return option

    def calculate_project_duration(self) -> int:
        """Calculate current project duration using CPM."""
        # Simple forward pass
        finish_times = {}

        def get_finish(act_id: str) -> int:
            if act_id in finish_times:
                return finish_times[act_id]

            act = self.activities[act_id]
            if not act.predecessors:
                start = 0
            else:
                start = max(get_finish(p) for p in act.predecessors)

            finish_times[act_id] = start + act.current_duration
            return finish_times[act_id]

        for act_id in self.activities:
            get_finish(act_id)

        self.project_duration = max(finish_times.values()) if finish_times else 0
        return self.project_duration

    def identify_critical_path(self) -> List[str]:
        """Identify critical path activities."""
        # Simplified - in practice, use full CPM
        self.calculate_project_duration()

        # Mark activities with zero float as critical
        critical = [act.id for act in self.activities.values() if act.is_critical]
        self.critical_path = critical
        return critical

    def analyze_crash_options(self) -> List[Dict]:
        """Analyze all crashing options sorted by cost efficiency."""
        crash_options = []

        for act in self.activities.values():
            if act.days_available_to_crash > 0 and act.is_critical:
                crash_options.append({
                    'activity_id': act.id,
                    'activity_name': act.name,
                    'crash_slope': act.crash_slope,
                    'max_days': act.days_available_to_crash,
                    'current_duration': act.current_duration,
                    'crash_duration': act.crash_duration
                })

        # Sort by crash slope (cost per day)
        return sorted(crash_options, key=lambda x: x['crash_slope'])

    def crash_schedule(self, target_days: int,
                      max_budget: float = float('inf')) -> CompressionPlan:
        """Crash schedule to reduce duration by target days."""
        self.calculate_project_duration()
        original_duration = self.project_duration

        crashed_activities = []
        total_cost = 0
        days_achieved = 0

        # Get crash options
        options = self.analyze_crash_options()

        while days_achieved < target_days and options:
            # Find cheapest option
            best_option = None
            for opt in options:
                if opt['max_days'] > 0:
                    best_option = opt
                    break

            if not best_option:
                break

            # Crash by 1 day
            act = self.activities[best_option['activity_id']]
            crash_cost = act.crash_slope

            if total_cost + crash_cost > max_budget:
                break

            act.current_duration -= 1
            total_cost += crash_cost
            days_achieved += 1

            # Update option
            best_option['max_days'] -= 1

            # Track what was crashed
            existing = next((c for c in crashed_activities if c[0] == act.id), None)
            if existing:
                crashed_activities.remove(existing)
                crashed_activities.append((act.id, existing[1] + 1))
            else:
                crashed_activities.append((act.id, 1))

            # Refresh options (critical path may change)
            options = self.analyze_crash_options()

        new_duration = self.calculate_project_duration()

        return CompressionPlan(
            target_reduction=target_days,
            achieved_reduction=days_achieved,
            crash_activities=crashed_activities,
            fast_track_options=[],
            total_additional_cost=total_cost,
            new_project_duration=new_duration,
            risk_assessment="Low risk - crashing uses proven methods"
        )

    def fast_track_schedule(self, target_days: int,
                           max_risk: str = "medium") -> CompressionPlan:
        """Fast-track schedule by overlapping activities."""
        risk_order = {"low": 1, "medium": 2, "high": 3}
        max_risk_level = risk_order.get(max_risk, 2)

        # Filter options by risk level
        viable_options = [
            opt for opt in self.fast_track_options
            if risk_order.get(opt.risk_level, 3) <= max_risk_level
        ]

        # Sort by overlap (most time saved first)
        viable_options.sort(key=lambda x: -x.overlap_days)

        selected_options = []
        total_overlap = 0
        total_risk_cost = 0

        for opt in viable_options:
            if total_overlap >= target_days:
                break

            selected_options.append(opt)
            total_overlap += opt.overlap_days
            total_risk_cost += opt.rework_probability * opt.potential_rework_cost

        self.calculate_project_duration()
        new_duration = self.project_duration - total_overlap

        risk_text = "High risk" if max_risk == "high" else "Moderate risk" if max_risk == "medium" else "Low risk"

        return CompressionPlan(
            target_reduction=target_days,
            achieved_reduction=total_overlap,
            crash_activities=[],
            fast_track_options=selected_options,
            total_additional_cost=total_risk_cost,
            new_project_duration=new_duration,
            risk_assessment=f"{risk_text} - potential rework if predecessor changes"
        )

    def optimize_compression(self, target_days: int,
                            max_budget: float,
                            max_risk: str = "medium") -> CompressionPlan:
        """Find optimal combination of crashing and fast-tracking."""
        # Try crash-only
        crash_plan = self.crash_schedule(target_days, max_budget)

        if crash_plan.achieved_reduction >= target_days:
            return crash_plan

        # Need additional fast-tracking
        remaining_days = target_days - crash_plan.achieved_reduction
        remaining_budget = max_budget - crash_plan.total_additional_cost

        fast_track_plan = self.fast_track_schedule(remaining_days, max_risk)

        # Combine plans
        total_reduction = crash_plan.achieved_reduction + fast_track_plan.achieved_reduction
        total_cost = crash_plan.total_additional_cost + fast_track_plan.total_additional_cost

        return CompressionPlan(
            target_reduction=target_days,
            achieved_reduction=total_reduction,
            crash_activities=crash_plan.crash_activities,
            fast_track_options=fast_track_plan.fast_track_options,
            total_additional_cost=total_cost,
            new_project_duration=self.project_duration - total_reduction,
            risk_assessment="Combined approach - balance of cost and risk"
        )

    def generate_cost_curve(self, max_compression: int) -> List[Dict]:
        """Generate time-cost tradeoff curve."""
        curve = []
        self.calculate_project_duration()
        original_duration = self.project_duration

        # Reset all activities to normal
        for act in self.activities.values():
            act.current_duration = act.normal_duration

        base_cost = sum(act.normal_cost for act in self.activities.values())

        curve.append({
            'duration': original_duration,
            'cost': base_cost,
            'compression': 0
        })

        for days in range(1, max_compression + 1):
            # Reset and crash by 'days'
            for act in self.activities.values():
                act.current_duration = act.normal_duration

            plan = self.crash_schedule(days)

            if plan.achieved_reduction < days:
                break

            curve.append({
                'duration': plan.new_project_duration,
                'cost': base_cost + plan.total_additional_cost,
                'compression': days
            })

        return curve

    def generate_compression_report(self, plan: CompressionPlan) -> str:
        """Generate compression analysis report."""
        lines = [
            "# Schedule Compression Report",
            "",
            f"**Target Reduction:** {plan.target_reduction} days",
            f"**Achieved Reduction:** {plan.achieved_reduction} days",
            f"**New Duration:** {plan.new_project_duration} days",
            f"**Additional Cost:** ${plan.total_additional_cost:,.0f}",
            "",
            f"## Risk Assessment",
            f"{plan.risk_assessment}",
            ""
        ]

        if plan.crash_activities:
            lines.append("## Crashed Activities")
            lines.append("")
            lines.append("| Activity | Days Crashed | Cost Impact |")
            lines.append("|----------|--------------|-------------|")
            for act_id, days in plan.crash_activities:
                act = self.activities[act_id]
                cost = days * act.crash_slope
                lines.append(f"| {act.name} | {days} | ${cost:,.0f} |")
            lines.append("")

        if plan.fast_track_options:
            lines.append("## Fast-Tracked Activities")
            lines.append("")
            for opt in plan.fast_track_options:
                lines.append(f"- **{opt.activity1_id} → {opt.activity2_id}**: {opt.overlap_days} days overlap")
                lines.append(f"  - Risk: {opt.risk_level} - {opt.risk_description}")
            lines.append("")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize compressor
compressor = ScheduleCompressor()

# Add activities with crash data
compressor.add_activity(
    "A", "Foundation",
    normal_duration=20, crash_duration=15,
    normal_cost=100000, crash_cost=130000,
    is_critical=True
)
compressor.add_activity(
    "B", "Steel Erection",
    normal_duration=30, crash_duration=22,
    normal_cost=200000, crash_cost=260000,
    predecessors=["A"],
    is_critical=True
)
compressor.add_activity(
    "C", "MEP Rough-in",
    normal_duration=25, crash_duration=20,
    normal_cost=150000, crash_cost=180000,
    predecessors=["B"],
    is_critical=True
)

# Add fast-track options
compressor.add_fast_track_option(
    "A", "B", overlap_days=5,
    risk_level="medium",
    risk_description="Steel may need rework if foundation changes",
    rework_probability=0.15,
    potential_rework_cost=30000
)

# Analyze crash options
print("Crash Options (sorted by cost/day):")
for opt in compressor.analyze_crash_options():
    print(f"  {opt['activity_name']}: ${opt['crash_slope']:.0f}/day, max {opt['max_days']} days")

# Compress schedule by 15 days
plan = compressor.optimize_compression(
    target_days=15,
    max_budget=80000,
    max_risk="medium"
)

print(compressor.generate_compression_report(plan))

# Generate cost curve
curve = compressor.generate_cost_curve(20)
for point in curve:
    print(f"Duration: {point['duration']}d, Cost: ${point['cost']:,.0f}")
```

## Requirements

```bash
pip install (no external dependencies)
```
