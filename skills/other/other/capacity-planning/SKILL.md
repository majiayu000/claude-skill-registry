---
name: "capacity-planning"
description: "Plan organizational capacity for construction projects. Forecast resource needs, identify capacity gaps, and support strategic planning for project pursuit and staffing."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Capacity Planning

## Overview

Strategic capacity planning for construction organizations. Forecast resource requirements based on project pipeline, identify capacity constraints, optimize staffing levels, and support go/no-go decisions on new project pursuits.

## Capacity Planning Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                  CAPACITY PLANNING                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DEMAND FORECAST           CAPACITY ANALYSIS        DECISIONS   │
│  ───────────────           ─────────────────        ─────────   │
│                                                                  │
│  Current Projects    →     Available:               Pursue new  │
│  • Project A (Active)      👷 PM: 5                 project?    │
│  • Project B (Active)      👷 Supers: 12            ────────    │
│  • Project C (Starting)    📐 Engineers: 8         ✅ Capacity  │
│                                                    ⚠️ Stretch   │
│  Pipeline:            →    Required:               ❌ Decline   │
│  • Bid D (60% win)         👷 PM: 7                             │
│  • Bid E (40% win)         👷 Supers: 15                        │
│  • Opportunity F           📐 Engineers: 10                     │
│                                                                  │
│  GAP ANALYSIS:             ACTIONS:                             │
│  • PM: -2 (deficit)        • Hire 2 PMs                         │
│  • Supers: -3 (deficit)    • Promote from within                │
│  • Engineers: -2 (deficit) • Partner with firm                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics

class ResourceRole(Enum):
    PROJECT_MANAGER = "project_manager"
    SUPERINTENDENT = "superintendent"
    PROJECT_ENGINEER = "project_engineer"
    ESTIMATOR = "estimator"
    SCHEDULER = "scheduler"
    SAFETY_MANAGER = "safety_manager"
    QC_MANAGER = "qc_manager"
    ADMIN = "admin"

class ProjectPhase(Enum):
    PURSUIT = "pursuit"
    PRECONSTRUCTION = "preconstruction"
    CONSTRUCTION = "construction"
    CLOSEOUT = "closeout"

class OpportunityStatus(Enum):
    IDENTIFIED = "identified"
    PURSUING = "pursuing"
    BID_SUBMITTED = "bid_submitted"
    NEGOTIATING = "negotiating"
    WON = "won"
    LOST = "lost"

@dataclass
class StaffMember:
    id: str
    name: str
    role: ResourceRole
    capacity: float = 1.0  # FTE
    current_assignment: str = ""
    availability_date: datetime = None
    skills: List[str] = field(default_factory=list)
    max_project_value: float = 0  # Max project size they can handle

@dataclass
class ProjectDemand:
    project_id: str
    project_name: str
    value: float
    phase: ProjectPhase
    start_date: datetime
    end_date: datetime
    probability: float = 1.0  # 1.0 for active, <1 for pipeline
    resource_needs: Dict[ResourceRole, float] = field(default_factory=dict)

@dataclass
class CapacityGap:
    role: ResourceRole
    period_start: datetime
    period_end: datetime
    demand: float
    capacity: float
    gap: float
    severity: str

@dataclass
class CapacityForecast:
    forecast_date: datetime
    horizon_months: int
    total_demand_fte: float
    total_capacity_fte: float
    utilization_pct: float
    gaps: List[CapacityGap]
    recommendations: List[str]

class CapacityPlanner:
    """Plan organizational capacity for construction projects."""

    # Typical staffing ratios by project value
    STAFFING_RATIOS = {
        ResourceRole.PROJECT_MANAGER: 20000000,      # 1 PM per $20M
        ResourceRole.SUPERINTENDENT: 10000000,       # 1 Super per $10M
        ResourceRole.PROJECT_ENGINEER: 15000000,     # 1 PE per $15M
        ResourceRole.ESTIMATOR: 50000000,            # 1 Estimator per $50M (pursuit)
        ResourceRole.SCHEDULER: 30000000,            # 1 Scheduler per $30M
        ResourceRole.SAFETY_MANAGER: 25000000,       # 1 Safety per $25M
    }

    # Phase factors (multiply by role ratio)
    PHASE_FACTORS = {
        ProjectPhase.PURSUIT: {"estimator": 1.5, "pm": 0.3},
        ProjectPhase.PRECONSTRUCTION: {"pm": 0.7, "pe": 0.5, "scheduler": 0.5},
        ProjectPhase.CONSTRUCTION: {"pm": 1.0, "super": 1.0, "pe": 1.0, "safety": 1.0},
        ProjectPhase.CLOSEOUT: {"pm": 0.5, "pe": 0.3, "admin": 1.0}
    }

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.staff: Dict[str, StaffMember] = {}
        self.projects: Dict[str, ProjectDemand] = {}
        self.pipeline: Dict[str, ProjectDemand] = {}

    def add_staff(self, id: str, name: str, role: ResourceRole,
                 capacity: float = 1.0, current_assignment: str = "",
                 availability_date: datetime = None,
                 max_project_value: float = 0) -> StaffMember:
        """Add staff member to capacity pool."""
        member = StaffMember(
            id=id,
            name=name,
            role=role,
            capacity=capacity,
            current_assignment=current_assignment,
            availability_date=availability_date or datetime.now(),
            max_project_value=max_project_value
        )
        self.staff[id] = member
        return member

    def add_active_project(self, id: str, name: str, value: float,
                          phase: ProjectPhase, start_date: datetime,
                          end_date: datetime) -> ProjectDemand:
        """Add active project to demand forecast."""
        # Calculate resource needs based on value and phase
        needs = self._calculate_resource_needs(value, phase)

        project = ProjectDemand(
            project_id=id,
            project_name=name,
            value=value,
            phase=phase,
            start_date=start_date,
            end_date=end_date,
            probability=1.0,
            resource_needs=needs
        )
        self.projects[id] = project
        return project

    def add_pipeline_opportunity(self, id: str, name: str, value: float,
                                 win_probability: float,
                                 expected_start: datetime,
                                 duration_months: int) -> ProjectDemand:
        """Add pipeline opportunity to demand forecast."""
        needs = self._calculate_resource_needs(value, ProjectPhase.CONSTRUCTION)

        opportunity = ProjectDemand(
            project_id=id,
            project_name=name,
            value=value,
            phase=ProjectPhase.PURSUIT,
            start_date=expected_start,
            end_date=expected_start + timedelta(days=duration_months * 30),
            probability=win_probability,
            resource_needs=needs
        )
        self.pipeline[id] = opportunity
        return opportunity

    def _calculate_resource_needs(self, value: float,
                                  phase: ProjectPhase) -> Dict[ResourceRole, float]:
        """Calculate resource needs based on project value and phase."""
        needs = {}

        for role, ratio in self.STAFFING_RATIOS.items():
            base_need = value / ratio

            # Apply phase factor
            phase_key = role.value.split('_')[0][:3]
            factor = 1.0
            if phase in self.PHASE_FACTORS:
                factor = self.PHASE_FACTORS[phase].get(phase_key, 1.0)

            needs[role] = base_need * factor

        return needs

    def get_current_capacity(self) -> Dict[ResourceRole, float]:
        """Get current capacity by role."""
        capacity = {role: 0.0 for role in ResourceRole}

        for member in self.staff.values():
            if member.availability_date <= datetime.now():
                capacity[member.role] += member.capacity

        return capacity

    def get_capacity_at_date(self, target_date: datetime) -> Dict[ResourceRole, float]:
        """Get projected capacity at future date."""
        capacity = {role: 0.0 for role in ResourceRole}

        for member in self.staff.values():
            if member.availability_date <= target_date:
                capacity[member.role] += member.capacity

        return capacity

    def calculate_demand(self, target_date: datetime,
                        include_pipeline: bool = True,
                        pipeline_threshold: float = 0.0) -> Dict[ResourceRole, float]:
        """Calculate resource demand at date."""
        demand = {role: 0.0 for role in ResourceRole}

        # Active projects
        for project in self.projects.values():
            if project.start_date <= target_date <= project.end_date:
                for role, need in project.resource_needs.items():
                    demand[role] += need * project.probability

        # Pipeline (weighted by probability)
        if include_pipeline:
            for opp in self.pipeline.values():
                if opp.probability >= pipeline_threshold:
                    if opp.start_date <= target_date <= opp.end_date:
                        for role, need in opp.resource_needs.items():
                            demand[role] += need * opp.probability

        return demand

    def identify_gaps(self, horizon_months: int = 12) -> List[CapacityGap]:
        """Identify capacity gaps over forecast horizon."""
        gaps = []

        for month in range(horizon_months):
            period_start = datetime.now() + timedelta(days=month * 30)
            period_end = period_start + timedelta(days=30)

            capacity = self.get_capacity_at_date(period_start)
            demand = self.calculate_demand(period_start, include_pipeline=True)

            for role in ResourceRole:
                cap = capacity.get(role, 0)
                dem = demand.get(role, 0)
                gap = cap - dem

                if gap < 0:
                    severity = "critical" if gap < -1 else "warning"
                    gaps.append(CapacityGap(
                        role=role,
                        period_start=period_start,
                        period_end=period_end,
                        demand=dem,
                        capacity=cap,
                        gap=gap,
                        severity=severity
                    ))

        return gaps

    def can_pursue_project(self, value: float, start_date: datetime,
                          duration_months: int) -> Dict:
        """Evaluate if organization can pursue new project."""
        # Calculate needs for potential project
        needs = self._calculate_resource_needs(value, ProjectPhase.CONSTRUCTION)
        end_date = start_date + timedelta(days=duration_months * 30)

        # Check capacity over project duration
        can_staff = True
        bottlenecks = []

        current_date = start_date
        while current_date <= end_date:
            capacity = self.get_capacity_at_date(current_date)
            demand = self.calculate_demand(current_date)

            for role, need in needs.items():
                available = capacity.get(role, 0) - demand.get(role, 0)
                if need > available:
                    can_staff = False
                    bottlenecks.append({
                        "date": current_date,
                        "role": role.value,
                        "needed": need,
                        "available": available,
                        "gap": need - available
                    })

            current_date += timedelta(days=30)

        # Determine recommendation
        if can_staff:
            recommendation = "GO - Sufficient capacity"
        elif len(bottlenecks) <= 2:
            recommendation = "CONDITIONAL - Minor gaps, consider hiring"
        else:
            recommendation = "CAUTION - Significant capacity constraints"

        return {
            "can_staff": can_staff,
            "recommendation": recommendation,
            "resource_needs": {r.value: v for r, v in needs.items()},
            "bottlenecks": bottlenecks[:10],
            "actions_required": self._suggest_hiring(bottlenecks)
        }

    def _suggest_hiring(self, bottlenecks: List[Dict]) -> List[str]:
        """Suggest hiring actions based on gaps."""
        if not bottlenecks:
            return []

        # Aggregate gaps by role
        role_gaps = {}
        for b in bottlenecks:
            role = b['role']
            if role not in role_gaps:
                role_gaps[role] = 0
            role_gaps[role] = max(role_gaps[role], b['gap'])

        actions = []
        for role, gap in sorted(role_gaps.items(), key=lambda x: -x[1]):
            hires = int(gap) + 1
            actions.append(f"Hire {hires} {role}(s) - Gap: {gap:.1f} FTE")

        return actions

    def generate_forecast(self, horizon_months: int = 12) -> CapacityForecast:
        """Generate capacity forecast."""
        gaps = self.identify_gaps(horizon_months)

        # Calculate totals
        capacity = self.get_current_capacity()
        demand = self.calculate_demand(datetime.now())

        total_capacity = sum(capacity.values())
        total_demand = sum(demand.values())
        utilization = (total_demand / total_capacity * 100) if total_capacity > 0 else 0

        # Generate recommendations
        recommendations = []

        if utilization > 90:
            recommendations.append("High utilization - consider hiring")
        elif utilization < 60:
            recommendations.append("Low utilization - review project pipeline")

        # Role-specific recommendations
        critical_gaps = [g for g in gaps if g.severity == "critical"]
        gap_roles = set(g.role.value for g in critical_gaps)
        for role in gap_roles:
            recommendations.append(f"Critical gap in {role} - immediate action needed")

        return CapacityForecast(
            forecast_date=datetime.now(),
            horizon_months=horizon_months,
            total_demand_fte=total_demand,
            total_capacity_fte=total_capacity,
            utilization_pct=utilization,
            gaps=gaps,
            recommendations=recommendations
        )

    def generate_report(self) -> str:
        """Generate capacity planning report."""
        forecast = self.generate_forecast()

        lines = [
            "# Capacity Planning Report",
            "",
            f"**Organization:** {self.organization_name}",
            f"**Report Date:** {forecast.forecast_date.strftime('%Y-%m-%d')}",
            "",
            "## Executive Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Active Projects | {len(self.projects)} |",
            f"| Pipeline Opportunities | {len(self.pipeline)} |",
            f"| Total Staff | {len(self.staff)} |",
            f"| Current Capacity (FTE) | {forecast.total_capacity_fte:.1f} |",
            f"| Current Demand (FTE) | {forecast.total_demand_fte:.1f} |",
            f"| Utilization | {forecast.utilization_pct:.0f}% |",
            "",
            "## Capacity by Role",
            "",
            "| Role | Capacity | Demand | Gap |",
            "|------|----------|--------|-----|"
        ]

        capacity = self.get_current_capacity()
        demand = self.calculate_demand(datetime.now())

        for role in ResourceRole:
            cap = capacity.get(role, 0)
            dem = demand.get(role, 0)
            gap = cap - dem
            gap_icon = "✅" if gap >= 0 else "⚠️" if gap > -1 else "🔴"
            lines.append(
                f"| {role.value} | {cap:.1f} | {dem:.1f} | {gap:+.1f} {gap_icon} |"
            )

        # Active projects
        lines.extend([
            "",
            "## Active Projects",
            "",
            "| Project | Value | Phase | End Date |",
            "|---------|-------|-------|----------|"
        ])

        for p in sorted(self.projects.values(), key=lambda x: x.value, reverse=True):
            lines.append(
                f"| {p.project_name} | ${p.value:,.0f} | {p.phase.value} | "
                f"{p.end_date.strftime('%Y-%m-%d')} |"
            )

        # Pipeline
        if self.pipeline:
            lines.extend([
                "",
                "## Pipeline",
                "",
                "| Opportunity | Value | Probability | Expected Start |",
                "|-------------|-------|-------------|----------------|"
            ])

            for p in sorted(self.pipeline.values(), key=lambda x: -x.probability):
                lines.append(
                    f"| {p.project_name} | ${p.value:,.0f} | {p.probability:.0%} | "
                    f"{p.start_date.strftime('%Y-%m-%d')} |"
                )

        # Gaps
        critical_gaps = [g for g in forecast.gaps if g.severity == "critical"]
        if critical_gaps:
            lines.extend([
                "",
                f"## Critical Capacity Gaps ({len(critical_gaps)})",
                "",
                "| Role | Period | Gap |",
                "|------|--------|-----|"
            ])

            for gap in critical_gaps[:10]:
                lines.append(
                    f"| {gap.role.value} | {gap.period_start.strftime('%Y-%m')} | "
                    f"{gap.gap:.1f} FTE |"
                )

        # Recommendations
        if forecast.recommendations:
            lines.extend([
                "",
                "## Recommendations",
                ""
            ])
            for rec in forecast.recommendations:
                lines.append(f"- {rec}")

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize planner
planner = CapacityPlanner("ABC Construction")

# Add staff
planner.add_staff("PM-001", "John Smith", ResourceRole.PROJECT_MANAGER)
planner.add_staff("PM-002", "Jane Doe", ResourceRole.PROJECT_MANAGER)
planner.add_staff("SUP-001", "Mike Johnson", ResourceRole.SUPERINTENDENT)
planner.add_staff("SUP-002", "Bob Williams", ResourceRole.SUPERINTENDENT)
planner.add_staff("SUP-003", "Tom Brown", ResourceRole.SUPERINTENDENT)
planner.add_staff("PE-001", "Sarah Davis", ResourceRole.PROJECT_ENGINEER)
planner.add_staff("PE-002", "Chris Wilson", ResourceRole.PROJECT_ENGINEER)

# Add active projects
planner.add_active_project(
    "PRJ-001", "Downtown Tower",
    value=25000000,
    phase=ProjectPhase.CONSTRUCTION,
    start_date=datetime(2024, 6, 1),
    end_date=datetime(2025, 12, 31)
)

planner.add_active_project(
    "PRJ-002", "Hospital Wing",
    value=40000000,
    phase=ProjectPhase.CONSTRUCTION,
    start_date=datetime(2024, 9, 1),
    end_date=datetime(2026, 6, 30)
)

# Add pipeline opportunities
planner.add_pipeline_opportunity(
    "OPP-001", "Office Complex",
    value=30000000,
    win_probability=0.6,
    expected_start=datetime(2025, 3, 1),
    duration_months=18
)

# Check if can pursue new project
evaluation = planner.can_pursue_project(
    value=20000000,
    start_date=datetime(2025, 6, 1),
    duration_months=12
)
print(f"Recommendation: {evaluation['recommendation']}")
for action in evaluation['actions_required']:
    print(f"  - {action}")

# Generate forecast
forecast = planner.generate_forecast()
print(f"Utilization: {forecast.utilization_pct:.0f}%")
print(f"Critical gaps: {len([g for g in forecast.gaps if g.severity == 'critical'])}")

# Generate report
print(planner.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
