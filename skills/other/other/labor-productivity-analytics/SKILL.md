---
name: "labor-productivity-analytics"
description: "Analyze construction labor productivity using data analytics. Track worker performance, identify inefficiencies, predict resource needs, and optimize crew allocation for maximum efficiency."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Labor Productivity Analytics

## Overview

This skill implements data-driven labor productivity analysis for construction projects. Track, measure, and optimize workforce performance to improve project efficiency and reduce costs.

**Capabilities:**
- Productivity metrics calculation
- Time series analysis
- Crew optimization
- Resource forecasting
- Benchmarking
- Variance analysis

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import numpy as np

@dataclass
class WorkLog:
    worker_id: str
    work_date: date
    activity_code: str
    hours_worked: float
    quantity_completed: float
    unit: str
    crew_id: str
    weather: str = "normal"
    notes: str = ""

@dataclass
class ProductivityMetric:
    activity: str
    unit_rate: float  # units per hour
    hours_per_unit: float  # hours per unit
    standard_rate: float  # benchmark
    variance_pct: float

def calculate_productivity(logs: List[WorkLog], standard_rates: Dict[str, float]) -> List[ProductivityMetric]:
    """Calculate productivity metrics from work logs"""
    # Group by activity
    by_activity = {}
    for log in logs:
        if log.activity_code not in by_activity:
            by_activity[log.activity_code] = {'hours': 0, 'quantity': 0, 'unit': log.unit}
        by_activity[log.activity_code]['hours'] += log.hours_worked
        by_activity[log.activity_code]['quantity'] += log.quantity_completed

    metrics = []
    for activity, data in by_activity.items():
        if data['hours'] > 0 and data['quantity'] > 0:
            unit_rate = data['quantity'] / data['hours']
            hours_per_unit = data['hours'] / data['quantity']
            standard = standard_rates.get(activity, hours_per_unit)
            variance = (hours_per_unit - standard) / standard * 100

            metrics.append(ProductivityMetric(
                activity=activity,
                unit_rate=unit_rate,
                hours_per_unit=hours_per_unit,
                standard_rate=standard,
                variance_pct=variance
            ))

    return metrics

# Example
logs = [
    WorkLog("W001", date.today(), "CONCRETE", 8, 10, "m³", "C01"),
    WorkLog("W002", date.today(), "CONCRETE", 8, 12, "m³", "C01"),
    WorkLog("W003", date.today(), "REBAR", 8, 500, "kg", "C02"),
]

standards = {"CONCRETE": 0.7, "REBAR": 0.015}  # hours per unit
metrics = calculate_productivity(logs, standards)
for m in metrics:
    print(f"{m.activity}: {m.hours_per_unit:.3f} h/unit (variance: {m.variance_pct:+.1f}%)")
```

## Comprehensive Productivity System

### Data Collection and Management

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import pandas as pd
import numpy as np
from collections import defaultdict

class TradeCode(Enum):
    CARPENTER = "carpenter"
    IRONWORKER = "ironworker"
    ELECTRICIAN = "electrician"
    PLUMBER = "plumber"
    LABORER = "laborer"
    OPERATOR = "operator"
    MASON = "mason"
    PAINTER = "painter"
    HVAC = "hvac"
    WELDER = "welder"

@dataclass
class Worker:
    worker_id: str
    name: str
    trade: TradeCode
    skill_level: int  # 1-5
    hourly_rate: float
    certifications: List[str] = field(default_factory=list)
    hire_date: date = None

@dataclass
class Crew:
    crew_id: str
    name: str
    foreman_id: str
    workers: List[str] = field(default_factory=list)
    primary_trade: TradeCode = None
    avg_productivity: float = 1.0

@dataclass
class DailyProductionRecord:
    record_id: str
    date: date
    crew_id: str
    activity_code: str
    activity_name: str

    # Time tracking
    start_time: datetime
    end_time: datetime
    total_hours: float
    overtime_hours: float = 0

    # Production
    quantity_completed: float
    unit: str
    percent_complete: float = 0

    # Conditions
    weather: str = "clear"
    temperature: float = 20
    disruptions: List[str] = field(default_factory=list)

    # Calculated
    productivity_factor: float = 1.0
    unit_rate: float = 0

    def calculate_metrics(self):
        """Calculate derived metrics"""
        if self.total_hours > 0 and self.quantity_completed > 0:
            self.unit_rate = self.quantity_completed / self.total_hours

class ProductivityDatabase:
    """Manage productivity data collection"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.workers: Dict[str, Worker] = {}
        self.crews: Dict[str, Crew] = {}
        self.records: List[DailyProductionRecord] = []
        self.standards: Dict[str, Dict] = {}

    def add_worker(self, worker: Worker):
        self.workers[worker.worker_id] = worker

    def add_crew(self, crew: Crew):
        self.crews[crew.crew_id] = crew

    def log_production(self, record: DailyProductionRecord):
        """Log daily production"""
        record.calculate_metrics()
        self.records.append(record)

        # Update crew average
        crew = self.crews.get(record.crew_id)
        if crew:
            crew_records = [r for r in self.records if r.crew_id == crew.crew_id]
            if crew_records:
                rates = [r.productivity_factor for r in crew_records if r.productivity_factor > 0]
                crew.avg_productivity = sum(rates) / len(rates) if rates else 1.0

    def set_standard(self, activity_code: str, hours_per_unit: float,
                    unit: str, trade: TradeCode = None):
        """Set productivity standard"""
        self.standards[activity_code] = {
            'hours_per_unit': hours_per_unit,
            'unit': unit,
            'trade': trade.value if trade else None,
            'source': 'manual'
        }

    def get_records_df(self) -> pd.DataFrame:
        """Get records as DataFrame"""
        data = []
        for r in self.records:
            data.append({
                'date': r.date,
                'crew_id': r.crew_id,
                'activity_code': r.activity_code,
                'hours': r.total_hours,
                'quantity': r.quantity_completed,
                'unit': r.unit,
                'unit_rate': r.unit_rate,
                'weather': r.weather,
                'productivity_factor': r.productivity_factor
            })
        return pd.DataFrame(data)
```

### Productivity Analysis Engine

```python
from scipy import stats
import numpy as np
import pandas as pd

class ProductivityAnalyzer:
    """Analyze labor productivity data"""

    def __init__(self, database: ProductivityDatabase):
        self.db = database
        self.df = database.get_records_df()

    def calculate_earned_value_metrics(self) -> Dict:
        """Calculate earned value productivity metrics"""
        if self.df.empty:
            return {}

        total_hours = self.df['hours'].sum()
        total_quantity = self.df['quantity'].sum()

        # Calculate budgeted hours (from standards)
        budgeted_hours = 0
        for _, row in self.df.iterrows():
            standard = self.db.standards.get(row['activity_code'], {})
            if standard:
                budgeted_hours += row['quantity'] * standard.get('hours_per_unit', 1)

        # Productivity Index
        productivity_index = budgeted_hours / total_hours if total_hours > 0 else 0

        return {
            'actual_hours': total_hours,
            'budgeted_hours': budgeted_hours,
            'hours_variance': budgeted_hours - total_hours,
            'productivity_index': productivity_index,
            'interpretation': 'efficient' if productivity_index > 1 else 'needs_improvement'
        }

    def analyze_by_activity(self) -> pd.DataFrame:
        """Analyze productivity by activity"""
        if self.df.empty:
            return pd.DataFrame()

        grouped = self.df.groupby('activity_code').agg({
            'hours': 'sum',
            'quantity': 'sum',
            'unit_rate': ['mean', 'std', 'min', 'max']
        })

        grouped.columns = ['total_hours', 'total_quantity', 'avg_rate', 'std_rate', 'min_rate', 'max_rate']
        grouped['hours_per_unit'] = grouped['total_hours'] / grouped['total_quantity']

        # Add standard comparison
        grouped['standard_rate'] = grouped.index.map(
            lambda x: 1 / self.db.standards.get(x, {}).get('hours_per_unit', 1)
        )
        grouped['variance_pct'] = (grouped['avg_rate'] - grouped['standard_rate']) / grouped['standard_rate'] * 100

        return grouped

    def analyze_by_crew(self) -> pd.DataFrame:
        """Analyze productivity by crew"""
        if self.df.empty:
            return pd.DataFrame()

        grouped = self.df.groupby('crew_id').agg({
            'hours': 'sum',
            'quantity': 'sum',
            'productivity_factor': 'mean',
            'date': 'nunique'
        }).rename(columns={'date': 'work_days'})

        grouped['avg_daily_hours'] = grouped['hours'] / grouped['work_days']
        grouped['avg_daily_quantity'] = grouped['quantity'] / grouped['work_days']

        return grouped

    def analyze_trends(self, window_days: int = 7) -> Dict:
        """Analyze productivity trends over time"""
        if self.df.empty:
            return {}

        self.df['date'] = pd.to_datetime(self.df['date'])
        daily = self.df.groupby('date').agg({
            'hours': 'sum',
            'quantity': 'sum',
            'productivity_factor': 'mean'
        })

        # Rolling average
        daily['productivity_ma'] = daily['productivity_factor'].rolling(window=window_days).mean()

        # Trend analysis
        if len(daily) > window_days:
            x = np.arange(len(daily))
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                x, daily['productivity_factor'].values
            )

            trend = 'improving' if slope > 0.001 else 'declining' if slope < -0.001 else 'stable'
        else:
            slope, trend = 0, 'insufficient_data'

        return {
            'daily_data': daily.to_dict(),
            'trend': trend,
            'trend_slope': slope,
            'avg_productivity': daily['productivity_factor'].mean(),
            'productivity_std': daily['productivity_factor'].std()
        }

    def analyze_weather_impact(self) -> Dict:
        """Analyze weather impact on productivity"""
        if self.df.empty:
            return {}

        weather_impact = self.df.groupby('weather').agg({
            'productivity_factor': ['mean', 'count'],
            'hours': 'sum'
        })

        weather_impact.columns = ['avg_productivity', 'record_count', 'total_hours']

        baseline = weather_impact.loc['clear']['avg_productivity'] if 'clear' in weather_impact.index else 1.0

        impact = {}
        for weather in weather_impact.index:
            productivity = weather_impact.loc[weather]['avg_productivity']
            impact[weather] = {
                'productivity': productivity,
                'impact_pct': (productivity - baseline) / baseline * 100,
                'records': weather_impact.loc[weather]['record_count']
            }

        return impact

    def identify_inefficiencies(self) -> List[Dict]:
        """Identify areas of inefficiency"""
        issues = []

        # Low performing crews
        crew_analysis = self.analyze_by_crew()
        for crew_id, row in crew_analysis.iterrows():
            if row['productivity_factor'] < 0.8:
                issues.append({
                    'type': 'low_crew_productivity',
                    'crew_id': crew_id,
                    'productivity': row['productivity_factor'],
                    'recommendation': 'Review crew composition and training needs'
                })

        # High variance activities
        activity_analysis = self.analyze_by_activity()
        for activity, row in activity_analysis.iterrows():
            if row['std_rate'] > row['avg_rate'] * 0.5:
                issues.append({
                    'type': 'high_variance',
                    'activity': activity,
                    'std_rate': row['std_rate'],
                    'recommendation': 'Standardize work methods and improve planning'
                })

        # Weather impact
        weather_impact = self.analyze_weather_impact()
        for weather, impact in weather_impact.items():
            if impact['impact_pct'] < -20:
                issues.append({
                    'type': 'weather_impact',
                    'weather': weather,
                    'impact_pct': impact['impact_pct'],
                    'recommendation': 'Plan weather-sensitive activities for better conditions'
                })

        return issues
```

### Resource Forecasting

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd

class ResourceForecaster:
    """Forecast labor resource needs"""

    def __init__(self, database: ProductivityDatabase):
        self.db = database
        self.models = {}

    def forecast_hours(self, activity_code: str, remaining_quantity: float,
                      crew_id: str = None) -> Dict:
        """Forecast hours needed to complete remaining work"""
        records = [r for r in self.db.records if r.activity_code == activity_code]

        if not records:
            # Use standard
            standard = self.db.standards.get(activity_code, {})
            hours_per_unit = standard.get('hours_per_unit', 1)
            return {
                'method': 'standard',
                'forecasted_hours': remaining_quantity * hours_per_unit,
                'confidence': 'low'
            }

        # Calculate from historical data
        if crew_id:
            crew_records = [r for r in records if r.crew_id == crew_id]
            if crew_records:
                records = crew_records

        total_hours = sum(r.total_hours for r in records)
        total_quantity = sum(r.quantity_completed for r in records)
        avg_rate = total_hours / total_quantity if total_quantity > 0 else 1

        # Consider trend
        if len(records) >= 5:
            recent_records = sorted(records, key=lambda x: x.date)[-5:]
            recent_rate = sum(r.total_hours for r in recent_records) / sum(r.quantity_completed for r in recent_records)
            # Weighted average (recent performance weighted more)
            adjusted_rate = avg_rate * 0.3 + recent_rate * 0.7
        else:
            adjusted_rate = avg_rate

        return {
            'method': 'historical',
            'forecasted_hours': remaining_quantity * adjusted_rate,
            'avg_rate': avg_rate,
            'adjusted_rate': adjusted_rate,
            'sample_size': len(records),
            'confidence': 'high' if len(records) >= 10 else 'medium' if len(records) >= 5 else 'low'
        }

    def forecast_crew_needs(self, planned_work: List[Dict],
                           available_hours_per_day: float = 8) -> Dict:
        """Forecast crew requirements for planned work

        planned_work: List of {activity_code, quantity, deadline_days}
        """
        crew_needs = []
        total_hours = 0

        for work in planned_work:
            forecast = self.forecast_hours(work['activity_code'], work['quantity'])
            hours_needed = forecast['forecasted_hours']
            total_hours += hours_needed

            workers_per_day = hours_needed / (work['deadline_days'] * available_hours_per_day)

            crew_needs.append({
                'activity': work['activity_code'],
                'hours_needed': hours_needed,
                'deadline_days': work['deadline_days'],
                'workers_needed': int(np.ceil(workers_per_day)),
                'daily_production_target': work['quantity'] / work['deadline_days']
            })

        return {
            'crew_needs': crew_needs,
            'total_hours': total_hours,
            'peak_workers': max(c['workers_needed'] for c in crew_needs),
            'avg_workers': sum(c['workers_needed'] for c in crew_needs) / len(crew_needs)
        }

    def optimize_crew_allocation(self, crews: List[Crew],
                                work_items: List[Dict]) -> Dict:
        """Optimize crew allocation to work items"""
        # Simple greedy allocation based on productivity
        allocations = []
        remaining_work = list(work_items)

        for crew in sorted(crews, key=lambda c: c.avg_productivity, reverse=True):
            if not remaining_work:
                break

            # Find best matching work for this crew
            crew_trade = crew.primary_trade

            best_work = None
            best_score = -1

            for work in remaining_work:
                activity = work['activity_code']
                standard = self.db.standards.get(activity, {})
                work_trade = standard.get('trade')

                # Score based on trade match and productivity
                if work_trade == crew_trade.value if crew_trade else True:
                    score = crew.avg_productivity
                    if score > best_score:
                        best_score = score
                        best_work = work

            if best_work:
                allocations.append({
                    'crew_id': crew.crew_id,
                    'activity': best_work['activity_code'],
                    'expected_productivity': crew.avg_productivity,
                    'quantity': best_work['quantity']
                })
                remaining_work.remove(best_work)

        return {
            'allocations': allocations,
            'unassigned_work': remaining_work
        }
```

### Reporting and Visualization

```python
def generate_productivity_report(analyzer: ProductivityAnalyzer,
                                forecaster: ResourceForecaster,
                                output_path: str) -> str:
    """Generate comprehensive productivity report"""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary
        ev_metrics = analyzer.calculate_earned_value_metrics()
        summary = pd.DataFrame([ev_metrics])
        summary.to_excel(writer, sheet_name='Summary', index=False)

        # By Activity
        activity_analysis = analyzer.analyze_by_activity()
        activity_analysis.to_excel(writer, sheet_name='By_Activity')

        # By Crew
        crew_analysis = analyzer.analyze_by_crew()
        crew_analysis.to_excel(writer, sheet_name='By_Crew')

        # Issues
        issues = analyzer.identify_inefficiencies()
        pd.DataFrame(issues).to_excel(writer, sheet_name='Issues', index=False)

        # Weather Impact
        weather = analyzer.analyze_weather_impact()
        pd.DataFrame(weather).T.to_excel(writer, sheet_name='Weather_Impact')

    return output_path
```

## Quick Reference

| Trade | Typical Unit Rate | Unit | Notes |
|-------|-------------------|------|-------|
| Carpenter | 0.5-1.0 | m²/hr | Formwork |
| Ironworker | 15-25 | kg/hr | Rebar tying |
| Mason | 0.3-0.5 | m²/hr | Brickwork |
| Electrician | 2-4 | points/hr | Rough-in |
| Plumber | 2-3 | fixtures/hr | Install |
| Painter | 3-5 | m²/hr | Interior |

## Resources

- **RS Means Labor Rates**: Industry benchmarks
- **AGC Productivity Standards**: https://www.agc.org
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `cost-prediction` for labor cost forecasting
- See `4d-simulation` for schedule integration
- See `risk-assessment-ml` for productivity risk
