---
name: "productivity-analyzer"
description: "Analyze labor productivity from site data. Compare planned vs actual, identify trends, benchmark against industry standards."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📊", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Productivity Analyzer

## Business Case

### Problem Statement
Understanding productivity requires:
- Tracking actual output rates
- Comparing to planned rates
- Identifying problem areas
- Forecasting project completion

### Solution
Analyze labor productivity data to identify trends, compare to benchmarks, and provide actionable insights.

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class ProductivityStatus(Enum):
    EXCELLENT = "excellent"    # >110% of planned
    ON_TARGET = "on_target"    # 90-110%
    BELOW = "below"            # 70-90%
    CRITICAL = "critical"      # <70%


@dataclass
class ProductivityRecord:
    date: date
    activity_code: str
    description: str
    planned_output: float
    actual_output: float
    unit: str
    manhours: float
    crew_size: int
    conditions: str  # weather, access issues


@dataclass
class ProductivityAnalysis:
    activity_code: str
    description: str
    total_planned: float
    total_actual: float
    total_manhours: float
    planned_rate: float  # unit per manhour
    actual_rate: float
    efficiency: float  # percentage
    status: ProductivityStatus
    trend: str  # improving, declining, stable


class ProductivityAnalyzer:
    """Analyze construction productivity data."""

    # Industry benchmark rates (unit per manhour)
    BENCHMARKS = {
        'concrete_pour': 0.5,      # m3/MH
        'rebar_install': 15,       # kg/MH
        'formwork': 0.8,           # m2/MH
        'brick_laying': 35,        # bricks/MH
        'drywall': 1.5,            # m2/MH
        'painting': 3.0,           # m2/MH
        'conduit': 8,              # m/MH
        'pipe': 3,                 # m/MH
        'excavation': 2.5,         # m3/MH
        'backfill': 3.0,           # m3/MH
    }

    def __init__(self):
        self.records: List[ProductivityRecord] = []

    def add_record(self,
                   date: date,
                   activity_code: str,
                   description: str,
                   planned_output: float,
                   actual_output: float,
                   unit: str,
                   manhours: float,
                   crew_size: int,
                   conditions: str = "normal"):
        """Add productivity record."""

        self.records.append(ProductivityRecord(
            date=date,
            activity_code=activity_code,
            description=description,
            planned_output=planned_output,
            actual_output=actual_output,
            unit=unit,
            manhours=manhours,
            crew_size=crew_size,
            conditions=conditions
        ))

    def import_from_dataframe(self, df: pd.DataFrame):
        """Import records from DataFrame."""
        for _, row in df.iterrows():
            self.add_record(
                date=pd.to_datetime(row['date']).date(),
                activity_code=row['activity_code'],
                description=row.get('description', ''),
                planned_output=float(row['planned_output']),
                actual_output=float(row['actual_output']),
                unit=row.get('unit', 'unit'),
                manhours=float(row['manhours']),
                crew_size=int(row.get('crew_size', 1)),
                conditions=row.get('conditions', 'normal')
            )

    def _get_status(self, efficiency: float) -> ProductivityStatus:
        """Determine productivity status."""
        if efficiency >= 110:
            return ProductivityStatus.EXCELLENT
        elif efficiency >= 90:
            return ProductivityStatus.ON_TARGET
        elif efficiency >= 70:
            return ProductivityStatus.BELOW
        else:
            return ProductivityStatus.CRITICAL

    def _calculate_trend(self, records: List[ProductivityRecord]) -> str:
        """Calculate productivity trend."""
        if len(records) < 3:
            return "insufficient_data"

        # Sort by date
        sorted_records = sorted(records, key=lambda x: x.date)

        # Calculate efficiency for first and last third
        n = len(sorted_records)
        third = n // 3

        early_efficiency = []
        late_efficiency = []

        for i, r in enumerate(sorted_records):
            if r.manhours > 0:
                eff = (r.actual_output / r.planned_output * 100) if r.planned_output > 0 else 0
                if i < third:
                    early_efficiency.append(eff)
                elif i >= n - third:
                    late_efficiency.append(eff)

        if not early_efficiency or not late_efficiency:
            return "stable"

        early_avg = np.mean(early_efficiency)
        late_avg = np.mean(late_efficiency)

        if late_avg > early_avg * 1.05:
            return "improving"
        elif late_avg < early_avg * 0.95:
            return "declining"
        else:
            return "stable"

    def analyze_activity(self, activity_code: str) -> Optional[ProductivityAnalysis]:
        """Analyze productivity for specific activity."""

        activity_records = [r for r in self.records if r.activity_code == activity_code]

        if not activity_records:
            return None

        total_planned = sum(r.planned_output for r in activity_records)
        total_actual = sum(r.actual_output for r in activity_records)
        total_manhours = sum(r.manhours for r in activity_records)

        planned_rate = total_planned / total_manhours if total_manhours > 0 else 0
        actual_rate = total_actual / total_manhours if total_manhours > 0 else 0
        efficiency = (total_actual / total_planned * 100) if total_planned > 0 else 0

        return ProductivityAnalysis(
            activity_code=activity_code,
            description=activity_records[0].description,
            total_planned=round(total_planned, 2),
            total_actual=round(total_actual, 2),
            total_manhours=round(total_manhours, 1),
            planned_rate=round(planned_rate, 3),
            actual_rate=round(actual_rate, 3),
            efficiency=round(efficiency, 1),
            status=self._get_status(efficiency),
            trend=self._calculate_trend(activity_records)
        )

    def analyze_all_activities(self) -> List[ProductivityAnalysis]:
        """Analyze all activities."""
        activities = set(r.activity_code for r in self.records)
        return [self.analyze_activity(code) for code in activities if self.analyze_activity(code)]

    def compare_to_benchmark(self, activity_code: str) -> Dict[str, Any]:
        """Compare activity to industry benchmark."""

        analysis = self.analyze_activity(activity_code)
        if not analysis:
            return {}

        # Find matching benchmark
        benchmark = None
        for key, value in self.BENCHMARKS.items():
            if key in activity_code.lower():
                benchmark = value
                break

        if benchmark is None:
            return {
                'activity': activity_code,
                'actual_rate': analysis.actual_rate,
                'benchmark': 'Not available',
                'vs_benchmark': 'N/A'
            }

        vs_benchmark = (analysis.actual_rate / benchmark * 100) if benchmark > 0 else 0

        return {
            'activity': activity_code,
            'actual_rate': analysis.actual_rate,
            'benchmark_rate': benchmark,
            'vs_benchmark_pct': round(vs_benchmark, 1),
            'recommendation': 'Above benchmark' if vs_benchmark >= 100 else 'Below benchmark - investigate'
        }

    def identify_problem_areas(self) -> List[Dict[str, Any]]:
        """Identify activities with productivity issues."""

        problems = []

        for analysis in self.analyze_all_activities():
            if analysis.status in [ProductivityStatus.BELOW, ProductivityStatus.CRITICAL]:
                problems.append({
                    'activity': analysis.activity_code,
                    'efficiency': analysis.efficiency,
                    'status': analysis.status.value,
                    'trend': analysis.trend,
                    'manhours_impacted': analysis.total_manhours,
                    'priority': 'HIGH' if analysis.status == ProductivityStatus.CRITICAL else 'MEDIUM'
                })

        return sorted(problems, key=lambda x: x['efficiency'])

    def forecast_completion(self,
                            activity_code: str,
                            remaining_quantity: float) -> Dict[str, Any]:
        """Forecast completion based on current productivity."""

        analysis = self.analyze_activity(activity_code)
        if not analysis or analysis.actual_rate == 0:
            return {}

        # Manhours needed at current rate
        manhours_needed = remaining_quantity / analysis.actual_rate

        # Average daily manhours
        activity_records = [r for r in self.records if r.activity_code == activity_code]
        avg_daily_mh = np.mean([r.manhours for r in activity_records]) if activity_records else 8

        days_needed = manhours_needed / avg_daily_mh if avg_daily_mh > 0 else 0

        return {
            'activity': activity_code,
            'remaining_qty': remaining_quantity,
            'current_rate': analysis.actual_rate,
            'manhours_needed': round(manhours_needed, 1),
            'days_needed': round(days_needed, 1),
            'estimated_completion': date.today() + timedelta(days=int(days_needed))
        }

    def export_analysis(self, output_path: str) -> str:
        """Export analysis to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            analyses = self.analyze_all_activities()
            summary_df = pd.DataFrame([
                {
                    'Activity': a.activity_code,
                    'Description': a.description,
                    'Planned': a.total_planned,
                    'Actual': a.total_actual,
                    'Manhours': a.total_manhours,
                    'Efficiency %': a.efficiency,
                    'Status': a.status.value,
                    'Trend': a.trend
                }
                for a in analyses
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Problems
            problems = self.identify_problem_areas()
            if problems:
                problems_df = pd.DataFrame(problems)
                problems_df.to_excel(writer, sheet_name='Problem Areas', index=False)

            # Raw data
            records_df = pd.DataFrame([
                {
                    'Date': r.date,
                    'Activity': r.activity_code,
                    'Planned': r.planned_output,
                    'Actual': r.actual_output,
                    'Unit': r.unit,
                    'Manhours': r.manhours,
                    'Crew': r.crew_size,
                    'Conditions': r.conditions
                }
                for r in self.records
            ])
            records_df.to_excel(writer, sheet_name='Raw Data', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date, timedelta

# Initialize analyzer
analyzer = ProductivityAnalyzer()

# Add records
for i in range(10):
    analyzer.add_record(
        date=date.today() - timedelta(days=i),
        activity_code="concrete_pour",
        description="Slab pour Level 3",
        planned_output=20,
        actual_output=18 + (i * 0.3),  # improving
        unit="m3",
        manhours=40,
        crew_size=5
    )

# Analyze
analysis = analyzer.analyze_activity("concrete_pour")
print(f"Efficiency: {analysis.efficiency}%")
print(f"Status: {analysis.status.value}")
print(f"Trend: {analysis.trend}")
```

## Common Use Cases

### 1. Identify Problems
```python
problems = analyzer.identify_problem_areas()
for p in problems:
    print(f"{p['activity']}: {p['efficiency']}% - {p['priority']}")
```

### 2. Forecast Completion
```python
forecast = analyzer.forecast_completion("concrete_pour", remaining_quantity=500)
print(f"Days needed: {forecast['days_needed']}")
print(f"Completion: {forecast['estimated_completion']}")
```

### 3. Compare to Benchmarks
```python
comparison = analyzer.compare_to_benchmark("concrete_pour")
print(f"vs Benchmark: {comparison['vs_benchmark_pct']}%")
```

## Resources
- **DDC Book**: Chapter 4.1 - Productivity Management
