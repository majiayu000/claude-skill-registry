---
slug: "project-kpi-dashboard"
display_name: "Project KPI Dashboard"
description: "Create interactive KPI dashboards for construction projects. Track schedule, cost, quality, and safety metrics in real-time."
---

# Project KPI Dashboard

## Business Case

### Problem Statement
Project stakeholders struggle with:
- Scattered data across multiple systems
- Delayed reporting on project health
- No real-time visibility into KPIs
- Inconsistent metric definitions

### Solution
Centralized KPI dashboard that aggregates data from multiple sources and presents key metrics with drill-down capabilities.

### Business Value
- **Real-time visibility** - Live project health status
- **Data-driven decisions** - Actionable insights
- **Stakeholder alignment** - Single source of truth
- **Early warning** - Proactive issue detection

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class KPIStatus(Enum):
    """KPI health status."""
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class KPICategory(Enum):
    """KPI categories."""
    SCHEDULE = "schedule"
    COST = "cost"
    QUALITY = "quality"
    SAFETY = "safety"
    PRODUCTIVITY = "productivity"
    SUSTAINABILITY = "sustainability"


@dataclass
class KPIMetric:
    """Single KPI metric."""
    name: str
    category: KPICategory
    current_value: float
    target_value: float
    unit: str
    status: KPIStatus
    trend: str  # up, down, stable
    last_updated: datetime
    description: str = ""

    @property
    def variance(self) -> float:
        """Calculate variance from target."""
        if self.target_value == 0:
            return 0
        return ((self.current_value - self.target_value) / self.target_value) * 100

    @property
    def achievement(self) -> float:
        """Calculate achievement percentage."""
        if self.target_value == 0:
            return 0
        return (self.current_value / self.target_value) * 100


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    project_name: str
    project_code: str
    start_date: date
    end_date: date
    budget: float
    currency: str = "USD"
    refresh_interval_minutes: int = 15


class ProjectKPIDashboard:
    """Construction project KPI dashboard."""

    # Standard thresholds for RAG status
    THRESHOLDS = {
        'schedule': {'green': 0.95, 'amber': 0.85},
        'cost': {'green': 1.05, 'amber': 1.15},
        'quality': {'green': 0.98, 'amber': 0.95},
        'safety': {'green': 0, 'amber': 1}  # incident count
    }

    def __init__(self, config: DashboardConfig):
        self.config = config
        self.metrics: Dict[str, KPIMetric] = {}
        self.history: List[Dict[str, Any]] = []

    def add_metric(self, metric: KPIMetric):
        """Add or update a KPI metric."""
        self.metrics[metric.name] = metric
        self._record_history(metric)

    def _record_history(self, metric: KPIMetric):
        """Record metric history for trending."""
        self.history.append({
            'name': metric.name,
            'value': metric.current_value,
            'timestamp': metric.last_updated,
            'status': metric.status.value
        })

    def calculate_schedule_kpis(self,
                                 planned_activities: int,
                                 completed_activities: int,
                                 planned_duration_days: int,
                                 actual_duration_days: int) -> List[KPIMetric]:
        """Calculate schedule-related KPIs."""

        # Schedule Performance Index (SPI)
        spi = completed_activities / planned_activities if planned_activities > 0 else 0
        spi_status = self._get_status(spi, 'schedule')

        # Schedule Variance
        sv = completed_activities - planned_activities

        # Percent Complete
        pct_complete = (completed_activities / planned_activities * 100) if planned_activities > 0 else 0

        metrics = [
            KPIMetric(
                name="Schedule Performance Index",
                category=KPICategory.SCHEDULE,
                current_value=round(spi, 2),
                target_value=1.0,
                unit="ratio",
                status=spi_status,
                trend=self._calculate_trend("Schedule Performance Index"),
                last_updated=datetime.now(),
                description="SPI = Earned Value / Planned Value"
            ),
            KPIMetric(
                name="Percent Complete",
                category=KPICategory.SCHEDULE,
                current_value=round(pct_complete, 1),
                target_value=100,
                unit="%",
                status=spi_status,
                trend=self._calculate_trend("Percent Complete"),
                last_updated=datetime.now()
            ),
            KPIMetric(
                name="Schedule Variance",
                category=KPICategory.SCHEDULE,
                current_value=sv,
                target_value=0,
                unit="activities",
                status=spi_status,
                trend=self._calculate_trend("Schedule Variance"),
                last_updated=datetime.now()
            )
        ]

        for m in metrics:
            self.add_metric(m)

        return metrics

    def calculate_cost_kpis(self,
                            budgeted_cost: float,
                            actual_cost: float,
                            earned_value: float) -> List[KPIMetric]:
        """Calculate cost-related KPIs."""

        # Cost Performance Index (CPI)
        cpi = earned_value / actual_cost if actual_cost > 0 else 0
        cpi_status = self._get_status(cpi, 'cost', inverse=True)

        # Cost Variance
        cv = earned_value - actual_cost

        # Budget utilization
        budget_used = (actual_cost / budgeted_cost * 100) if budgeted_cost > 0 else 0

        metrics = [
            KPIMetric(
                name="Cost Performance Index",
                category=KPICategory.COST,
                current_value=round(cpi, 2),
                target_value=1.0,
                unit="ratio",
                status=cpi_status,
                trend=self._calculate_trend("Cost Performance Index"),
                last_updated=datetime.now(),
                description="CPI = Earned Value / Actual Cost"
            ),
            KPIMetric(
                name="Cost Variance",
                category=KPICategory.COST,
                current_value=round(cv, 2),
                target_value=0,
                unit=self.config.currency,
                status=cpi_status,
                trend=self._calculate_trend("Cost Variance"),
                last_updated=datetime.now()
            ),
            KPIMetric(
                name="Budget Utilization",
                category=KPICategory.COST,
                current_value=round(budget_used, 1),
                target_value=100,
                unit="%",
                status=cpi_status,
                trend=self._calculate_trend("Budget Utilization"),
                last_updated=datetime.now()
            )
        ]

        for m in metrics:
            self.add_metric(m)

        return metrics

    def calculate_quality_kpis(self,
                               total_inspections: int,
                               passed_inspections: int,
                               rework_items: int,
                               total_items: int) -> List[KPIMetric]:
        """Calculate quality-related KPIs."""

        # First Pass Yield
        fpy = passed_inspections / total_inspections if total_inspections > 0 else 0
        fpy_status = self._get_status(fpy, 'quality')

        # Rework Rate
        rework_rate = rework_items / total_items * 100 if total_items > 0 else 0

        metrics = [
            KPIMetric(
                name="First Pass Yield",
                category=KPICategory.QUALITY,
                current_value=round(fpy * 100, 1),
                target_value=98,
                unit="%",
                status=fpy_status,
                trend=self._calculate_trend("First Pass Yield"),
                last_updated=datetime.now()
            ),
            KPIMetric(
                name="Rework Rate",
                category=KPICategory.QUALITY,
                current_value=round(rework_rate, 1),
                target_value=2,
                unit="%",
                status=fpy_status,
                trend=self._calculate_trend("Rework Rate"),
                last_updated=datetime.now()
            )
        ]

        for m in metrics:
            self.add_metric(m)

        return metrics

    def calculate_safety_kpis(self,
                              incidents: int,
                              near_misses: int,
                              worked_hours: float,
                              safety_observations: int) -> List[KPIMetric]:
        """Calculate safety-related KPIs."""

        # TRIR (Total Recordable Incident Rate)
        trir = (incidents * 200000) / worked_hours if worked_hours > 0 else 0
        trir_status = KPIStatus.ON_TRACK if incidents == 0 else (
            KPIStatus.AT_RISK if incidents <= 2 else KPIStatus.CRITICAL
        )

        # LTIR (Lost Time Incident Rate)
        ltir = (incidents * 1000000) / worked_hours if worked_hours > 0 else 0

        metrics = [
            KPIMetric(
                name="TRIR",
                category=KPICategory.SAFETY,
                current_value=round(trir, 2),
                target_value=0,
                unit="per 200k hrs",
                status=trir_status,
                trend=self._calculate_trend("TRIR"),
                last_updated=datetime.now(),
                description="Total Recordable Incident Rate"
            ),
            KPIMetric(
                name="Safety Observations",
                category=KPICategory.SAFETY,
                current_value=safety_observations,
                target_value=50,
                unit="count",
                status=KPIStatus.ON_TRACK if safety_observations >= 50 else KPIStatus.AT_RISK,
                trend=self._calculate_trend("Safety Observations"),
                last_updated=datetime.now()
            ),
            KPIMetric(
                name="Near Miss Reports",
                category=KPICategory.SAFETY,
                current_value=near_misses,
                target_value=10,
                unit="count",
                status=KPIStatus.ON_TRACK,
                trend=self._calculate_trend("Near Miss Reports"),
                last_updated=datetime.now()
            )
        ]

        for m in metrics:
            self.add_metric(m)

        return metrics

    def _get_status(self, value: float, category: str, inverse: bool = False) -> KPIStatus:
        """Determine RAG status based on thresholds."""
        thresholds = self.THRESHOLDS.get(category, {'green': 0.95, 'amber': 0.85})

        if inverse:
            if value >= thresholds['green']:
                return KPIStatus.ON_TRACK
            elif value >= thresholds['amber']:
                return KPIStatus.AT_RISK
            else:
                return KPIStatus.CRITICAL
        else:
            if value >= thresholds['green']:
                return KPIStatus.ON_TRACK
            elif value >= thresholds['amber']:
                return KPIStatus.AT_RISK
            else:
                return KPIStatus.CRITICAL

    def _calculate_trend(self, metric_name: str) -> str:
        """Calculate trend based on historical data."""
        history = [h for h in self.history if h['name'] == metric_name]
        if len(history) < 2:
            return "stable"

        recent = history[-1]['value']
        previous = history[-2]['value']

        if recent > previous * 1.02:
            return "up"
        elif recent < previous * 0.98:
            return "down"
        return "stable"

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Generate dashboard summary."""
        by_category = {}
        for metric in self.metrics.values():
            cat = metric.category.value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                'name': metric.name,
                'value': metric.current_value,
                'target': metric.target_value,
                'unit': metric.unit,
                'status': metric.status.value,
                'trend': metric.trend,
                'variance': round(metric.variance, 1)
            })

        # Overall health
        statuses = [m.status for m in self.metrics.values()]
        critical_count = sum(1 for s in statuses if s == KPIStatus.CRITICAL)
        at_risk_count = sum(1 for s in statuses if s == KPIStatus.AT_RISK)

        if critical_count > 0:
            overall = "CRITICAL"
        elif at_risk_count > 2:
            overall = "AT_RISK"
        else:
            overall = "ON_TRACK"

        return {
            'project': self.config.project_name,
            'project_code': self.config.project_code,
            'generated_at': datetime.now().isoformat(),
            'overall_health': overall,
            'metrics_count': len(self.metrics),
            'critical_count': critical_count,
            'at_risk_count': at_risk_count,
            'kpis_by_category': by_category
        }

    def export_to_dataframe(self) -> pd.DataFrame:
        """Export all KPIs to DataFrame."""
        data = []
        for metric in self.metrics.values():
            data.append({
                'KPI': metric.name,
                'Category': metric.category.value,
                'Current': metric.current_value,
                'Target': metric.target_value,
                'Unit': metric.unit,
                'Variance %': round(metric.variance, 1),
                'Status': metric.status.value,
                'Trend': metric.trend,
                'Last Updated': metric.last_updated
            })
        return pd.DataFrame(data)
```

## Quick Start

```python
from datetime import date

# Configure dashboard
config = DashboardConfig(
    project_name="Office Tower Construction",
    project_code="PRJ-2024-001",
    start_date=date(2024, 1, 1),
    end_date=date(2025, 12, 31),
    budget=50000000,
    currency="USD"
)

# Initialize dashboard
dashboard = ProjectKPIDashboard(config)

# Calculate schedule KPIs
dashboard.calculate_schedule_kpis(
    planned_activities=100,
    completed_activities=85,
    planned_duration_days=180,
    actual_duration_days=195
)

# Calculate cost KPIs
dashboard.calculate_cost_kpis(
    budgeted_cost=25000000,
    actual_cost=24500000,
    earned_value=24000000
)

# Get summary
summary = dashboard.get_dashboard_summary()
print(f"Overall Health: {summary['overall_health']}")
```

## Common Use Cases

### 1. Weekly Executive Report
```python
df = dashboard.export_to_dataframe()
critical = df[df['Status'] == 'critical']
print(f"Critical KPIs requiring attention: {len(critical)}")
```

### 2. Trend Analysis
```python
# Get historical data for a metric
spi_history = [h for h in dashboard.history if h['name'] == 'Schedule Performance Index']
```

### 3. Multi-Project Dashboard
```python
projects = []
for project_config in project_configs:
    dash = ProjectKPIDashboard(project_config)
    # ... calculate KPIs
    projects.append(dash.get_dashboard_summary())
```

## Resources
- **DDC Book**: Chapter 4.1 - Construction Analytics
- **Reference**: PMI Earned Value Management
