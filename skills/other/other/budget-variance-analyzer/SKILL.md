---
name: "budget-variance-analyzer"
description: "Analyze construction budget variances. Compare estimated vs actual costs, identify trends, forecast final costs, and generate variance reports for cost control."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "💵", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Budget Variance Analyzer

## Overview

Analyze construction budget variances between estimated and actual costs. Track cost performance by category, identify concerning trends, forecast final costs, and provide actionable insights for cost control.

## Variance Analysis Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                  BUDGET VARIANCE ANALYSIS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Budget    vs    Actual    =    Variance    →    Forecast      │
│  ──────         ──────          ────────         ────────       │
│  📋 Original    💰 Spent        📊 Over/Under    🔮 EAC         │
│  📝 Revised     📈 Committed    📉 Trend         📋 ETC         │
│  🎯 Baseline    🧾 Invoiced     ⚠️ Alerts        📊 VAC         │
│                                                                  │
│  EAC = Estimate at Completion                                   │
│  ETC = Estimate to Complete                                     │
│  VAC = Variance at Completion                                   │
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

class CostCategory(Enum):
    LABOR = "labor"
    MATERIALS = "materials"
    EQUIPMENT = "equipment"
    SUBCONTRACTOR = "subcontractor"
    GENERAL_CONDITIONS = "general_conditions"
    OVERHEAD = "overhead"
    CONTINGENCY = "contingency"
    FEE = "fee"

class VarianceStatus(Enum):
    ON_BUDGET = "on_budget"
    UNDER_BUDGET = "under_budget"
    OVER_BUDGET = "over_budget"
    CRITICAL = "critical"

@dataclass
class CostCode:
    code: str
    description: str
    category: CostCategory
    original_budget: float
    revised_budget: float = 0.0
    committed: float = 0.0
    actual: float = 0.0
    forecast: float = 0.0
    percent_complete: float = 0.0

    @property
    def budget(self) -> float:
        return self.revised_budget if self.revised_budget else self.original_budget

    @property
    def variance(self) -> float:
        return self.budget - self.actual

    @property
    def variance_percent(self) -> float:
        return (self.variance / self.budget * 100) if self.budget else 0

    @property
    def committed_variance(self) -> float:
        return self.budget - self.committed

    @property
    def estimate_to_complete(self) -> float:
        if self.percent_complete >= 100:
            return 0
        return self.forecast - self.actual

    @property
    def variance_at_completion(self) -> float:
        return self.budget - self.forecast

@dataclass
class CostSnapshot:
    date: datetime
    cost_code: str
    actual: float
    committed: float
    forecast: float

@dataclass
class VarianceReport:
    report_date: datetime
    project_name: str
    total_budget: float
    total_actual: float
    total_committed: float
    total_forecast: float
    variance: float
    variance_percent: float
    eac: float
    etc: float
    vac: float
    variances_by_category: Dict[str, Dict]
    critical_items: List[CostCode]
    trend: str

class BudgetVarianceAnalyzer:
    """Analyze construction budget variances."""

    # Thresholds for variance status
    VARIANCE_THRESHOLDS = {
        "under_budget": 0.05,   # 5% under
        "on_budget": 0.00,
        "over_budget": -0.05,  # 5% over
        "critical": -0.10      # 10% over
    }

    def __init__(self, project_name: str, original_budget: float):
        self.project_name = project_name
        self.original_budget = original_budget
        self.cost_codes: Dict[str, CostCode] = {}
        self.snapshots: List[CostSnapshot] = []
        self.contingency_used = 0.0

    def add_cost_code(self, code: str, description: str,
                     category: CostCategory, budget: float) -> CostCode:
        """Add cost code to budget."""
        cost_code = CostCode(
            code=code,
            description=description,
            category=category,
            original_budget=budget,
            revised_budget=budget,
            forecast=budget
        )
        self.cost_codes[code] = cost_code
        return cost_code

    def import_budget(self, items: List[Dict]) -> int:
        """Import budget from list of items."""
        count = 0
        for item in items:
            self.add_cost_code(
                item['code'],
                item['description'],
                CostCategory(item.get('category', 'other')),
                item['budget']
            )
            count += 1
        return count

    def update_actual(self, code: str, actual: float) -> CostCode:
        """Update actual cost for cost code."""
        if code not in self.cost_codes:
            raise ValueError(f"Cost code {code} not found")

        cost_code = self.cost_codes[code]
        cost_code.actual = actual

        # Record snapshot
        self._record_snapshot(code)

        return cost_code

    def update_committed(self, code: str, committed: float) -> CostCode:
        """Update committed cost (contracts, POs)."""
        if code not in self.cost_codes:
            raise ValueError(f"Cost code {code} not found")

        cost_code = self.cost_codes[code]
        cost_code.committed = committed

        # Update forecast if committed exceeds current forecast
        if committed > cost_code.forecast:
            cost_code.forecast = committed

        self._record_snapshot(code)
        return cost_code

    def update_forecast(self, code: str, forecast: float,
                       percent_complete: float = None) -> CostCode:
        """Update forecast for cost code."""
        if code not in self.cost_codes:
            raise ValueError(f"Cost code {code} not found")

        cost_code = self.cost_codes[code]
        cost_code.forecast = forecast

        if percent_complete is not None:
            cost_code.percent_complete = percent_complete

        self._record_snapshot(code)
        return cost_code

    def revise_budget(self, code: str, new_budget: float,
                     reason: str = "") -> CostCode:
        """Revise budget for cost code."""
        if code not in self.cost_codes:
            raise ValueError(f"Cost code {code} not found")

        cost_code = self.cost_codes[code]
        cost_code.revised_budget = new_budget
        cost_code.forecast = new_budget

        return cost_code

    def use_contingency(self, amount: float, target_code: str,
                       reason: str = "") -> float:
        """Use contingency to cover variance."""
        self.contingency_used += amount

        if target_code in self.cost_codes:
            cc = self.cost_codes[target_code]
            cc.revised_budget += amount

        return self.contingency_used

    def _record_snapshot(self, code: str):
        """Record cost snapshot for trending."""
        if code not in self.cost_codes:
            return

        cc = self.cost_codes[code]
        snapshot = CostSnapshot(
            date=datetime.now(),
            cost_code=code,
            actual=cc.actual,
            committed=cc.committed,
            forecast=cc.forecast
        )
        self.snapshots.append(snapshot)

    def get_variance_status(self, variance_percent: float) -> VarianceStatus:
        """Determine variance status."""
        if variance_percent >= self.VARIANCE_THRESHOLDS["under_budget"]:
            return VarianceStatus.UNDER_BUDGET
        elif variance_percent >= self.VARIANCE_THRESHOLDS["over_budget"]:
            return VarianceStatus.ON_BUDGET
        elif variance_percent >= self.VARIANCE_THRESHOLDS["critical"]:
            return VarianceStatus.OVER_BUDGET
        else:
            return VarianceStatus.CRITICAL

    def analyze_by_category(self) -> Dict[str, Dict]:
        """Analyze variances by cost category."""
        by_category = {}

        for category in CostCategory:
            codes = [cc for cc in self.cost_codes.values()
                    if cc.category == category]

            if not codes:
                continue

            budget = sum(cc.budget for cc in codes)
            actual = sum(cc.actual for cc in codes)
            committed = sum(cc.committed for cc in codes)
            forecast = sum(cc.forecast for cc in codes)

            variance = budget - actual
            variance_pct = (variance / budget * 100) if budget else 0

            by_category[category.value] = {
                "budget": budget,
                "actual": actual,
                "committed": committed,
                "forecast": forecast,
                "variance": variance,
                "variance_percent": variance_pct,
                "status": self.get_variance_status(variance_pct / 100).value
            }

        return by_category

    def identify_critical_items(self, threshold: float = -0.10) -> List[CostCode]:
        """Identify cost codes with critical variance."""
        critical = []

        for cc in self.cost_codes.values():
            variance_pct = cc.variance_percent / 100
            if variance_pct < threshold:
                critical.append(cc)

        return sorted(critical, key=lambda x: x.variance_percent)

    def calculate_cpi(self) -> float:
        """Calculate Cost Performance Index."""
        total_budget = sum(cc.budget * cc.percent_complete / 100
                          for cc in self.cost_codes.values())
        total_actual = sum(cc.actual for cc in self.cost_codes.values())

        if total_actual == 0:
            return 1.0

        return total_budget / total_actual

    def forecast_eac(self, method: str = "cpi") -> float:
        """Forecast Estimate at Completion."""
        total_budget = sum(cc.budget for cc in self.cost_codes.values())
        total_actual = sum(cc.actual for cc in self.cost_codes.values())

        if method == "cpi":
            cpi = self.calculate_cpi()
            if cpi == 0:
                return total_budget
            return total_actual + (total_budget - total_actual * cpi) / cpi

        elif method == "forecast":
            return sum(cc.forecast for cc in self.cost_codes.values())

        elif method == "committed":
            return sum(max(cc.committed, cc.actual) for cc in self.cost_codes.values())

        return total_budget

    def analyze_trend(self, code: str = None) -> Dict:
        """Analyze variance trend over time."""
        if code:
            snapshots = [s for s in self.snapshots if s.cost_code == code]
        else:
            snapshots = self.snapshots

        if len(snapshots) < 2:
            return {"trend": "insufficient_data", "slope": 0}

        # Group by week
        weekly_actuals = {}
        for s in snapshots:
            week = s.date.isocalendar()[1]
            if week not in weekly_actuals:
                weekly_actuals[week] = []
            weekly_actuals[week].append(s.actual)

        # Calculate trend
        weeks = sorted(weekly_actuals.keys())
        if len(weeks) < 2:
            return {"trend": "insufficient_data", "slope": 0}

        week_avgs = [statistics.mean(weekly_actuals[w]) for w in weeks]

        # Simple slope calculation
        n = len(weeks)
        x_mean = sum(range(n)) / n
        y_mean = sum(week_avgs) / n

        numerator = sum((i - x_mean) * (week_avgs[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator else 0

        if slope > 1000:
            trend = "increasing_rapidly"
        elif slope > 0:
            trend = "increasing"
        elif slope < -1000:
            trend = "decreasing_rapidly"
        elif slope < 0:
            trend = "decreasing"
        else:
            trend = "stable"

        return {"trend": trend, "slope": slope, "data_points": len(snapshots)}

    def generate_variance_report(self) -> VarianceReport:
        """Generate comprehensive variance report."""
        total_budget = sum(cc.budget for cc in self.cost_codes.values())
        total_actual = sum(cc.actual for cc in self.cost_codes.values())
        total_committed = sum(cc.committed for cc in self.cost_codes.values())
        total_forecast = sum(cc.forecast for cc in self.cost_codes.values())

        variance = total_budget - total_actual
        variance_pct = (variance / total_budget * 100) if total_budget else 0

        eac = self.forecast_eac()
        etc = eac - total_actual
        vac = total_budget - eac

        trend_analysis = self.analyze_trend()

        return VarianceReport(
            report_date=datetime.now(),
            project_name=self.project_name,
            total_budget=total_budget,
            total_actual=total_actual,
            total_committed=total_committed,
            total_forecast=total_forecast,
            variance=variance,
            variance_percent=variance_pct,
            eac=eac,
            etc=etc,
            vac=vac,
            variances_by_category=self.analyze_by_category(),
            critical_items=self.identify_critical_items(),
            trend=trend_analysis["trend"]
        )

    def generate_report_markdown(self, report: VarianceReport) -> str:
        """Generate markdown report."""
        lines = [
            "# Budget Variance Report",
            "",
            f"**Project:** {report.project_name}",
            f"**Report Date:** {report.report_date.strftime('%Y-%m-%d')}",
            "",
            "## Executive Summary",
            "",
            f"| Metric | Amount |",
            f"|--------|--------|",
            f"| Total Budget | ${report.total_budget:,.0f} |",
            f"| Actual to Date | ${report.total_actual:,.0f} |",
            f"| Committed | ${report.total_committed:,.0f} |",
            f"| **Variance** | **${report.variance:,.0f} ({report.variance_percent:.1f}%)** |",
            "",
            "## Forecast",
            "",
            f"| Metric | Amount |",
            f"|--------|--------|",
            f"| Estimate at Completion (EAC) | ${report.eac:,.0f} |",
            f"| Estimate to Complete (ETC) | ${report.etc:,.0f} |",
            f"| Variance at Completion (VAC) | ${report.vac:,.0f} |",
            f"| CPI | {self.calculate_cpi():.2f} |",
            f"| Trend | {report.trend} |",
            "",
            "## By Category",
            "",
            "| Category | Budget | Actual | Variance | Status |",
            "|----------|--------|--------|----------|--------|"
        ]

        for cat, data in report.variances_by_category.items():
            status_icon = "🟢" if data["status"] == "under_budget" else "🟡" if data["status"] == "on_budget" else "🔴"
            lines.append(
                f"| {cat} | ${data['budget']:,.0f} | ${data['actual']:,.0f} | "
                f"${data['variance']:,.0f} ({data['variance_percent']:.1f}%) | {status_icon} |"
            )

        if report.critical_items:
            lines.extend([
                "",
                "## Critical Items (>10% Over Budget)",
                "",
                "| Code | Description | Budget | Actual | Variance |",
                "|------|-------------|--------|--------|----------|"
            ])
            for cc in report.critical_items[:10]:
                lines.append(
                    f"| {cc.code} | {cc.description[:25]} | ${cc.budget:,.0f} | "
                    f"${cc.actual:,.0f} | ${cc.variance:,.0f} ({cc.variance_percent:.1f}%) |"
                )

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize analyzer
analyzer = BudgetVarianceAnalyzer("Office Tower", 5000000)

# Add cost codes
analyzer.add_cost_code("01-100", "Project Management", CostCategory.GENERAL_CONDITIONS, 150000)
analyzer.add_cost_code("03-100", "Concrete", CostCategory.MATERIALS, 400000)
analyzer.add_cost_code("05-100", "Structural Steel", CostCategory.SUBCONTRACTOR, 800000)
analyzer.add_cost_code("15-100", "Mechanical", CostCategory.SUBCONTRACTOR, 600000)
analyzer.add_cost_code("16-100", "Electrical", CostCategory.SUBCONTRACTOR, 450000)

# Update actuals
analyzer.update_actual("01-100", 120000)
analyzer.update_actual("03-100", 380000)
analyzer.update_actual("05-100", 850000)  # Over budget
analyzer.update_actual("15-100", 300000)
analyzer.update_actual("16-100", 200000)

# Update committed
analyzer.update_committed("05-100", 900000)

# Update forecast
analyzer.update_forecast("05-100", 920000, percent_complete=85)

# Analyze
cpi = analyzer.calculate_cpi()
print(f"Cost Performance Index: {cpi:.2f}")

critical = analyzer.identify_critical_items()
print(f"Critical items: {len(critical)}")

# Generate report
report = analyzer.generate_variance_report()
print(analyzer.generate_report_markdown(report))
```

## Requirements

```bash
pip install (no external dependencies)
```
