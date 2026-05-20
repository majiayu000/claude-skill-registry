---
name: "portfolio-dashboard"
description: "Multi-project portfolio analytics dashboard. Aggregate KPIs across projects, track portfolio health, compare performance, and support executive decision-making."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Portfolio Dashboard

## Overview

Aggregate and analyze data across multiple construction projects for portfolio-level visibility. Track KPIs, identify trends, compare project performance, and support strategic resource allocation decisions.

## Portfolio Analytics Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                  PORTFOLIO DASHBOARD                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PROJECT A    PROJECT B    PROJECT C    PROJECT D               │
│     ↓             ↓            ↓            ↓                   │
│  ┌─────────────────────────────────────────────┐                │
│  │           DATA AGGREGATION                   │                │
│  │  Cost | Schedule | Safety | Quality | Risk   │                │
│  └─────────────────────────────────────────────┘                │
│                         ↓                                        │
│  ┌─────────────────────────────────────────────┐                │
│  │          PORTFOLIO KPIs                      │                │
│  │  📊 Total Value    📈 On-Schedule %          │                │
│  │  💰 On-Budget %    🛡️ Safety Rate            │                │
│  │  ⚠️ Risk Score     📋 Resource Util          │                │
│  └─────────────────────────────────────────────┘                │
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

class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETE = "complete"
    CANCELLED = "cancelled"

class HealthStatus(Enum):
    GREEN = "green"       # On track
    YELLOW = "yellow"     # At risk
    RED = "red"           # Critical
    GREY = "grey"         # Not started/on hold

@dataclass
class ProjectMetrics:
    project_id: str
    project_name: str
    status: ProjectStatus
    contract_value: float
    percent_complete: float

    # Schedule
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime]
    forecast_end: datetime
    schedule_variance_days: int = 0

    # Cost
    budget: float
    actual_cost: float
    forecast_cost: float
    cost_variance: float = 0.0
    cpi: float = 1.0
    spi: float = 1.0

    # Safety
    recordable_incidents: int = 0
    total_hours: float = 0
    trir: float = 0.0

    # Quality
    defects_open: int = 0
    rework_cost: float = 0.0

    # Risk
    risk_score: float = 0.0
    critical_risks: int = 0

    @property
    def health(self) -> HealthStatus:
        """Determine overall project health."""
        if self.status in [ProjectStatus.ON_HOLD, ProjectStatus.CANCELLED]:
            return HealthStatus.GREY

        # Critical if significantly over budget/schedule
        if self.cpi < 0.85 or self.spi < 0.85 or self.critical_risks > 3:
            return HealthStatus.RED

        # At risk if moderately off track
        if self.cpi < 0.95 or self.spi < 0.95 or self.critical_risks > 0:
            return HealthStatus.YELLOW

        return HealthStatus.GREEN

@dataclass
class PortfolioSummary:
    report_date: datetime
    total_projects: int
    active_projects: int
    total_contract_value: float
    total_budget: float
    total_actual_cost: float
    total_forecast_cost: float

    # Performance
    avg_cpi: float
    avg_spi: float
    on_budget_pct: float
    on_schedule_pct: float

    # Safety
    portfolio_trir: float
    total_incidents: int

    # Health distribution
    green_count: int
    yellow_count: int
    red_count: int

    # Trends
    cost_trend: str
    schedule_trend: str

@dataclass
class ProjectComparison:
    metric: str
    projects: Dict[str, float]
    avg: float
    best: Tuple[str, float]
    worst: Tuple[str, float]

class PortfolioDashboard:
    """Multi-project portfolio analytics."""

    # Health thresholds
    THRESHOLDS = {
        "cpi_warning": 0.95,
        "cpi_critical": 0.85,
        "spi_warning": 0.95,
        "spi_critical": 0.85,
        "trir_warning": 2.0,
        "risk_score_warning": 7.0
    }

    def __init__(self, portfolio_name: str):
        self.portfolio_name = portfolio_name
        self.projects: Dict[str, ProjectMetrics] = {}
        self.snapshots: List[Dict] = []  # Historical data

    def add_project(self, metrics: ProjectMetrics):
        """Add or update project in portfolio."""
        self.projects[metrics.project_id] = metrics

    def import_projects(self, projects_data: List[Dict]) -> int:
        """Import multiple projects from data."""
        count = 0
        for p in projects_data:
            metrics = ProjectMetrics(
                project_id=p['id'],
                project_name=p['name'],
                status=ProjectStatus(p.get('status', 'active')),
                contract_value=p['contract_value'],
                percent_complete=p.get('percent_complete', 0),
                planned_start=p['planned_start'],
                planned_end=p['planned_end'],
                actual_start=p.get('actual_start'),
                forecast_end=p.get('forecast_end', p['planned_end']),
                budget=p['budget'],
                actual_cost=p.get('actual_cost', 0),
                forecast_cost=p.get('forecast_cost', p['budget']),
                cpi=p.get('cpi', 1.0),
                spi=p.get('spi', 1.0),
                recordable_incidents=p.get('incidents', 0),
                total_hours=p.get('total_hours', 0),
                risk_score=p.get('risk_score', 0),
                critical_risks=p.get('critical_risks', 0)
            )

            # Calculate derived metrics
            metrics.cost_variance = metrics.budget - metrics.actual_cost
            metrics.schedule_variance_days = (metrics.planned_end - metrics.forecast_end).days

            if metrics.total_hours > 0:
                metrics.trir = (metrics.recordable_incidents * 200000) / metrics.total_hours

            self.add_project(metrics)
            count += 1

        return count

    def get_active_projects(self) -> List[ProjectMetrics]:
        """Get list of active projects."""
        return [p for p in self.projects.values()
                if p.status == ProjectStatus.ACTIVE]

    def calculate_portfolio_summary(self) -> PortfolioSummary:
        """Calculate portfolio-level summary metrics."""
        active = self.get_active_projects()
        all_projects = list(self.projects.values())

        if not all_projects:
            return None

        # Totals
        total_contract = sum(p.contract_value for p in all_projects)
        total_budget = sum(p.budget for p in all_projects)
        total_actual = sum(p.actual_cost for p in all_projects)
        total_forecast = sum(p.forecast_cost for p in all_projects)

        # Performance averages (weighted by budget)
        if total_budget > 0:
            avg_cpi = sum(p.cpi * p.budget for p in active) / sum(p.budget for p in active) if active else 1.0
            avg_spi = sum(p.spi * p.budget for p in active) / sum(p.budget for p in active) if active else 1.0
        else:
            avg_cpi = avg_spi = 1.0

        # On budget/schedule percentages
        on_budget = len([p for p in active if p.cpi >= 0.95])
        on_schedule = len([p for p in active if p.spi >= 0.95])

        on_budget_pct = (on_budget / len(active) * 100) if active else 100
        on_schedule_pct = (on_schedule / len(active) * 100) if active else 100

        # Safety metrics
        total_incidents = sum(p.recordable_incidents for p in all_projects)
        total_hours = sum(p.total_hours for p in all_projects)
        portfolio_trir = (total_incidents * 200000 / total_hours) if total_hours > 0 else 0

        # Health distribution
        green = len([p for p in active if p.health == HealthStatus.GREEN])
        yellow = len([p for p in active if p.health == HealthStatus.YELLOW])
        red = len([p for p in active if p.health == HealthStatus.RED])

        # Trends (compare to previous snapshot if available)
        cost_trend = "stable"
        schedule_trend = "stable"

        if self.snapshots:
            prev = self.snapshots[-1]
            if avg_cpi > prev.get('avg_cpi', 1.0):
                cost_trend = "improving"
            elif avg_cpi < prev.get('avg_cpi', 1.0):
                cost_trend = "declining"

            if avg_spi > prev.get('avg_spi', 1.0):
                schedule_trend = "improving"
            elif avg_spi < prev.get('avg_spi', 1.0):
                schedule_trend = "declining"

        return PortfolioSummary(
            report_date=datetime.now(),
            total_projects=len(all_projects),
            active_projects=len(active),
            total_contract_value=total_contract,
            total_budget=total_budget,
            total_actual_cost=total_actual,
            total_forecast_cost=total_forecast,
            avg_cpi=avg_cpi,
            avg_spi=avg_spi,
            on_budget_pct=on_budget_pct,
            on_schedule_pct=on_schedule_pct,
            portfolio_trir=portfolio_trir,
            total_incidents=total_incidents,
            green_count=green,
            yellow_count=yellow,
            red_count=red,
            cost_trend=cost_trend,
            schedule_trend=schedule_trend
        )

    def compare_projects(self, metric: str) -> ProjectComparison:
        """Compare projects by specific metric."""
        active = self.get_active_projects()

        if not active:
            return None

        metric_map = {
            "cpi": lambda p: p.cpi,
            "spi": lambda p: p.spi,
            "percent_complete": lambda p: p.percent_complete,
            "cost_variance": lambda p: p.cost_variance,
            "trir": lambda p: p.trir,
            "risk_score": lambda p: p.risk_score
        }

        if metric not in metric_map:
            raise ValueError(f"Unknown metric: {metric}")

        getter = metric_map[metric]
        values = {p.project_name: getter(p) for p in active}

        avg = statistics.mean(values.values())

        # Best/worst depends on metric (higher CPI good, lower TRIR good)
        if metric in ["trir", "risk_score"]:
            best = min(values.items(), key=lambda x: x[1])
            worst = max(values.items(), key=lambda x: x[1])
        else:
            best = max(values.items(), key=lambda x: x[1])
            worst = min(values.items(), key=lambda x: x[1])

        return ProjectComparison(
            metric=metric,
            projects=values,
            avg=avg,
            best=best,
            worst=worst
        )

    def get_projects_at_risk(self) -> List[ProjectMetrics]:
        """Get projects that need attention."""
        return [p for p in self.get_active_projects()
                if p.health in [HealthStatus.YELLOW, HealthStatus.RED]]

    def get_top_risks(self, limit: int = 10) -> List[Dict]:
        """Get top risks across portfolio."""
        risks = []

        for p in self.get_active_projects():
            if p.risk_score > 0:
                risks.append({
                    "project": p.project_name,
                    "risk_score": p.risk_score,
                    "critical_risks": p.critical_risks,
                    "cpi": p.cpi,
                    "spi": p.spi
                })

        return sorted(risks, key=lambda x: -x['risk_score'])[:limit]

    def forecast_cash_needs(self, months: int = 6) -> List[Dict]:
        """Forecast cash needs across portfolio."""
        forecasts = []

        for month in range(1, months + 1):
            month_date = datetime.now() + timedelta(days=month * 30)

            month_spend = 0
            for p in self.get_active_projects():
                # Simple linear projection based on remaining work
                remaining = p.forecast_cost - p.actual_cost
                months_remaining = max(1, (p.forecast_end - datetime.now()).days / 30)
                monthly_burn = remaining / months_remaining
                month_spend += monthly_burn

            forecasts.append({
                "month": month_date.strftime("%Y-%m"),
                "projected_spend": month_spend
            })

        return forecasts

    def save_snapshot(self):
        """Save current state for trend analysis."""
        summary = self.calculate_portfolio_summary()
        if summary:
            self.snapshots.append({
                "date": datetime.now(),
                "avg_cpi": summary.avg_cpi,
                "avg_spi": summary.avg_spi,
                "on_budget_pct": summary.on_budget_pct,
                "on_schedule_pct": summary.on_schedule_pct,
                "total_forecast": summary.total_forecast_cost
            })

    def generate_report(self) -> str:
        """Generate portfolio dashboard report."""
        summary = self.calculate_portfolio_summary()

        if not summary:
            return "No projects in portfolio"

        lines = [
            "# Portfolio Dashboard",
            "",
            f"**Portfolio:** {self.portfolio_name}",
            f"**Report Date:** {summary.report_date.strftime('%Y-%m-%d')}",
            "",
            "## Executive Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Projects | {summary.total_projects} ({summary.active_projects} active) |",
            f"| Total Contract Value | ${summary.total_contract_value:,.0f} |",
            f"| Total Budget | ${summary.total_budget:,.0f} |",
            f"| Actual Cost to Date | ${summary.total_actual_cost:,.0f} |",
            f"| Forecast at Completion | ${summary.total_forecast_cost:,.0f} |",
            "",
            "## Performance Indicators",
            "",
            f"| KPI | Value | Trend |",
            f"|-----|-------|-------|",
            f"| Avg CPI | {summary.avg_cpi:.2f} | {summary.cost_trend} |",
            f"| Avg SPI | {summary.avg_spi:.2f} | {summary.schedule_trend} |",
            f"| On Budget | {summary.on_budget_pct:.0f}% | |",
            f"| On Schedule | {summary.on_schedule_pct:.0f}% | |",
            f"| Portfolio TRIR | {summary.portfolio_trir:.2f} | |",
            "",
            "## Health Distribution",
            "",
            f"🟢 Green: {summary.green_count} | 🟡 Yellow: {summary.yellow_count} | 🔴 Red: {summary.red_count}",
            ""
        ]

        # Projects at risk
        at_risk = self.get_projects_at_risk()
        if at_risk:
            lines.extend([
                "## Projects Requiring Attention",
                "",
                "| Project | Health | CPI | SPI | Critical Risks |",
                "|---------|--------|-----|-----|----------------|"
            ])
            for p in sorted(at_risk, key=lambda x: x.cpi):
                health_icon = "🟡" if p.health == HealthStatus.YELLOW else "🔴"
                lines.append(
                    f"| {p.project_name} | {health_icon} | {p.cpi:.2f} | {p.spi:.2f} | {p.critical_risks} |"
                )
            lines.append("")

        # Project comparison
        lines.extend([
            "## Project Comparison - CPI",
            "",
            "| Project | CPI |",
            "|---------|-----|"
        ])

        cpi_compare = self.compare_projects("cpi")
        if cpi_compare:
            for name, value in sorted(cpi_compare.projects.items(), key=lambda x: -x[1]):
                lines.append(f"| {name} | {value:.2f} |")

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize dashboard
dashboard = PortfolioDashboard("Regional Construction Portfolio")

# Import project data
projects = [
    {
        "id": "PRJ-001",
        "name": "Downtown Office Tower",
        "status": "active",
        "contract_value": 50000000,
        "budget": 48000000,
        "actual_cost": 25000000,
        "forecast_cost": 49000000,
        "percent_complete": 55,
        "planned_start": datetime(2024, 1, 1),
        "planned_end": datetime(2025, 6, 30),
        "forecast_end": datetime(2025, 7, 15),
        "cpi": 0.92,
        "spi": 0.95,
        "incidents": 2,
        "total_hours": 150000,
        "risk_score": 7.5,
        "critical_risks": 2
    },
    {
        "id": "PRJ-002",
        "name": "Hospital Expansion",
        "status": "active",
        "contract_value": 80000000,
        "budget": 75000000,
        "actual_cost": 30000000,
        "forecast_cost": 74000000,
        "percent_complete": 40,
        "planned_start": datetime(2024, 3, 1),
        "planned_end": datetime(2026, 2, 28),
        "forecast_end": datetime(2026, 2, 28),
        "cpi": 1.02,
        "spi": 1.00,
        "incidents": 0,
        "total_hours": 100000,
        "risk_score": 4.0,
        "critical_risks": 0
    }
]

dashboard.import_projects(projects)

# Get portfolio summary
summary = dashboard.calculate_portfolio_summary()
print(f"Portfolio Value: ${summary.total_contract_value:,.0f}")
print(f"Avg CPI: {summary.avg_cpi:.2f}")
print(f"On Budget: {summary.on_budget_pct:.0f}%")

# Find projects at risk
at_risk = dashboard.get_projects_at_risk()
print(f"Projects at risk: {len(at_risk)}")

# Compare projects
cpi_comparison = dashboard.compare_projects("cpi")
print(f"Best CPI: {cpi_comparison.best[0]} ({cpi_comparison.best[1]:.2f})")

# Generate report
print(dashboard.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
