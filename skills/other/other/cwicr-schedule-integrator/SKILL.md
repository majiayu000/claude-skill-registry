---
name: "cwicr-schedule-integrator"
description: "Integrate CWICR cost data with project schedules. Link work items to schedule activities, generate cost-loaded schedules, and cash flow projections."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Schedule Integrator

## Business Case

### Problem Statement
Project planning requires:
- Linking costs to schedule activities
- Generating cost-loaded schedules
- Projecting cash flow requirements
- Tracking earned value

### Solution
Integrate CWICR cost data with project schedules to create cost-loaded Gantt charts, cash flow curves, and earned value tracking.

### Business Value
- **Cost visibility** - See when costs occur
- **Cash flow** - Project funding requirements
- **Earned value** - Track cost/schedule performance
- **Integration** - Connect cost and schedule data

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from enum import Enum
from collections import defaultdict


class CostDistribution(Enum):
    """Methods for distributing costs over time."""
    UNIFORM = "uniform"          # Even distribution
    FRONT_LOADED = "front_loaded"  # More at start
    BACK_LOADED = "back_loaded"    # More at end
    S_CURVE = "s_curve"          # S-curve distribution


@dataclass
class ScheduleActivity:
    """Project schedule activity."""
    activity_id: str
    description: str
    start_date: date
    end_date: date
    duration_days: int
    work_items: List[str]
    budgeted_cost: float
    predecessors: List[str] = field(default_factory=list)


@dataclass
class CostLoadedActivity:
    """Activity with daily cost distribution."""
    activity: ScheduleActivity
    daily_costs: Dict[date, float]
    cumulative_costs: Dict[date, float]


@dataclass
class CashFlowProjection:
    """Cash flow projection."""
    project_name: str
    start_date: date
    end_date: date
    total_cost: float
    daily_costs: Dict[date, float]
    weekly_costs: Dict[str, float]
    monthly_costs: Dict[str, float]
    cumulative: Dict[date, float]


@dataclass
class EarnedValueMetrics:
    """Earned value metrics at point in time."""
    data_date: date
    planned_value: float  # PV / BCWS
    earned_value: float   # EV / BCWP
    actual_cost: float    # AC / ACWP
    schedule_variance: float  # SV = EV - PV
    cost_variance: float      # CV = EV - AC
    spi: float               # Schedule Performance Index
    cpi: float               # Cost Performance Index
    eac: float               # Estimate at Completion
    etc: float               # Estimate to Complete


class CWICRScheduleIntegrator:
    """Integrate CWICR costs with project schedules."""

    def __init__(self, cwicr_data: pd.DataFrame):
        self.cost_data = cwicr_data
        self._index_data()

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def get_work_item_cost(self, code: str, quantity: float) -> float:
        """Get total cost for work item."""
        if self._code_index is None or code not in self._code_index.index:
            return 0

        item = self._code_index.loc[code]
        labor = float(item.get('labor_cost', 0) or 0)
        material = float(item.get('material_cost', 0) or 0)
        equipment = float(item.get('equipment_cost', 0) or 0)

        return (labor + material + equipment) * quantity

    def create_schedule_activity(self,
                                  activity_id: str,
                                  description: str,
                                  start_date: date,
                                  duration_days: int,
                                  work_items: List[Dict[str, Any]],
                                  predecessors: List[str] = None) -> ScheduleActivity:
        """Create schedule activity with linked work items."""

        # Calculate budgeted cost
        total_cost = 0
        codes = []
        for item in work_items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)
            total_cost += self.get_work_item_cost(code, qty)
            codes.append(code)

        end_date = start_date + timedelta(days=duration_days)

        return ScheduleActivity(
            activity_id=activity_id,
            description=description,
            start_date=start_date,
            end_date=end_date,
            duration_days=duration_days,
            work_items=codes,
            budgeted_cost=round(total_cost, 2),
            predecessors=predecessors or []
        )

    def distribute_cost(self,
                        activity: ScheduleActivity,
                        method: CostDistribution = CostDistribution.UNIFORM) -> CostLoadedActivity:
        """Distribute activity cost over duration."""

        daily_costs = {}
        days = activity.duration_days

        if days == 0:
            daily_costs[activity.start_date] = activity.budgeted_cost
        else:
            if method == CostDistribution.UNIFORM:
                daily_amount = activity.budgeted_cost / days
                for i in range(days):
                    day = activity.start_date + timedelta(days=i)
                    daily_costs[day] = daily_amount

            elif method == CostDistribution.FRONT_LOADED:
                # Higher at start, decreasing
                total_weight = sum(range(days, 0, -1))
                for i in range(days):
                    day = activity.start_date + timedelta(days=i)
                    weight = (days - i) / total_weight
                    daily_costs[day] = activity.budgeted_cost * weight

            elif method == CostDistribution.BACK_LOADED:
                # Lower at start, increasing
                total_weight = sum(range(1, days + 1))
                for i in range(days):
                    day = activity.start_date + timedelta(days=i)
                    weight = (i + 1) / total_weight
                    daily_costs[day] = activity.budgeted_cost * weight

            elif method == CostDistribution.S_CURVE:
                # S-curve distribution (sigmoid)
                for i in range(days):
                    day = activity.start_date + timedelta(days=i)
                    # Sigmoid function normalized
                    x = (i / days - 0.5) * 10
                    sigmoid = 1 / (1 + np.exp(-x))
                    daily_costs[day] = activity.budgeted_cost * sigmoid / days * 2

        # Calculate cumulative
        cumulative = {}
        running_total = 0
        for day in sorted(daily_costs.keys()):
            running_total += daily_costs[day]
            cumulative[day] = running_total

        return CostLoadedActivity(
            activity=activity,
            daily_costs=daily_costs,
            cumulative_costs=cumulative
        )

    def generate_cash_flow(self,
                           activities: List[ScheduleActivity],
                           project_name: str = "Project",
                           distribution: CostDistribution = CostDistribution.S_CURVE) -> CashFlowProjection:
        """Generate project cash flow projection."""

        # Distribute costs for all activities
        loaded_activities = [
            self.distribute_cost(a, distribution)
            for a in activities
        ]

        # Aggregate daily costs
        daily_costs = defaultdict(float)
        for loaded in loaded_activities:
            for day, cost in loaded.daily_costs.items():
                daily_costs[day] += cost

        # Sort and calculate cumulative
        sorted_days = sorted(daily_costs.keys())
        cumulative = {}
        running_total = 0
        for day in sorted_days:
            running_total += daily_costs[day]
            cumulative[day] = running_total

        # Aggregate to weekly
        weekly_costs = defaultdict(float)
        for day, cost in daily_costs.items():
            week_key = day.strftime('%Y-W%W')
            weekly_costs[week_key] += cost

        # Aggregate to monthly
        monthly_costs = defaultdict(float)
        for day, cost in daily_costs.items():
            month_key = day.strftime('%Y-%m')
            monthly_costs[month_key] += cost

        return CashFlowProjection(
            project_name=project_name,
            start_date=min(daily_costs.keys()) if daily_costs else date.today(),
            end_date=max(daily_costs.keys()) if daily_costs else date.today(),
            total_cost=sum(daily_costs.values()),
            daily_costs=dict(daily_costs),
            weekly_costs=dict(weekly_costs),
            monthly_costs=dict(monthly_costs),
            cumulative=cumulative
        )

    def calculate_earned_value(self,
                                activities: List[ScheduleActivity],
                                progress: Dict[str, float],  # activity_id -> percent complete
                                actual_costs: Dict[str, float],  # activity_id -> actual cost
                                data_date: date) -> EarnedValueMetrics:
        """Calculate earned value metrics."""

        # Generate planned value curve
        cash_flow = self.generate_cash_flow(activities)

        # Planned Value (BCWS) - budgeted cost through data date
        pv = sum(
            cost for day, cost in cash_flow.daily_costs.items()
            if day <= data_date
        )

        # Earned Value (BCWP) - budgeted cost * percent complete
        ev = sum(
            a.budgeted_cost * progress.get(a.activity_id, 0) / 100
            for a in activities
        )

        # Actual Cost (ACWP)
        ac = sum(actual_costs.values())

        # Variances
        sv = ev - pv
        cv = ev - ac

        # Indices
        spi = ev / pv if pv > 0 else 0
        cpi = ev / ac if ac > 0 else 0

        # Estimate at completion
        bac = sum(a.budgeted_cost for a in activities)
        if cpi > 0:
            eac = bac / cpi
        else:
            eac = bac

        etc = eac - ac

        return EarnedValueMetrics(
            data_date=data_date,
            planned_value=round(pv, 2),
            earned_value=round(ev, 2),
            actual_cost=round(ac, 2),
            schedule_variance=round(sv, 2),
            cost_variance=round(cv, 2),
            spi=round(spi, 2),
            cpi=round(cpi, 2),
            eac=round(eac, 2),
            etc=round(etc, 2)
        )

    def export_cash_flow(self,
                         cash_flow: CashFlowProjection,
                         output_path: str) -> str:
        """Export cash flow to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Project': cash_flow.project_name,
                'Start Date': cash_flow.start_date,
                'End Date': cash_flow.end_date,
                'Total Cost': cash_flow.total_cost
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Monthly
            monthly_df = pd.DataFrame([
                {'Month': month, 'Cost': cost}
                for month, cost in sorted(cash_flow.monthly_costs.items())
            ])
            monthly_df.to_excel(writer, sheet_name='Monthly', index=False)

            # Weekly
            weekly_df = pd.DataFrame([
                {'Week': week, 'Cost': cost}
                for week, cost in sorted(cash_flow.weekly_costs.items())
            ])
            weekly_df.to_excel(writer, sheet_name='Weekly', index=False)

            # Daily with cumulative
            daily_df = pd.DataFrame([
                {
                    'Date': day.strftime('%Y-%m-%d'),
                    'Daily Cost': round(cash_flow.daily_costs[day], 2),
                    'Cumulative': round(cash_flow.cumulative[day], 2)
                }
                for day in sorted(cash_flow.daily_costs.keys())
            ])
            daily_df.to_excel(writer, sheet_name='Daily', index=False)

        return output_path

    def import_schedule_from_csv(self,
                                  schedule_file: str,
                                  work_items_file: str) -> List[ScheduleActivity]:
        """Import schedule and work items from CSV files."""

        schedule_df = pd.read_csv(schedule_file)
        work_items_df = pd.read_csv(work_items_file)

        activities = []

        for _, row in schedule_df.iterrows():
            activity_id = row['activity_id']

            # Get work items for this activity
            activity_items = work_items_df[
                work_items_df['activity_id'] == activity_id
            ].to_dict('records')

            activity = self.create_schedule_activity(
                activity_id=activity_id,
                description=row['description'],
                start_date=pd.to_datetime(row['start_date']).date(),
                duration_days=int(row['duration_days']),
                work_items=activity_items,
                predecessors=row.get('predecessors', '').split(',') if pd.notna(row.get('predecessors')) else []
            )
            activities.append(activity)

        return activities
```

## Quick Start

```python
from datetime import date

# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize integrator
integrator = CWICRScheduleIntegrator(cwicr)

# Create activities
activity1 = integrator.create_schedule_activity(
    activity_id="A001",
    description="Foundation Excavation",
    start_date=date(2024, 6, 1),
    duration_days=10,
    work_items=[
        {'work_item_code': 'EXCV-001', 'quantity': 500}
    ]
)

activity2 = integrator.create_schedule_activity(
    activity_id="A002",
    description="Foundation Concrete",
    start_date=date(2024, 6, 11),
    duration_days=15,
    work_items=[
        {'work_item_code': 'CONC-001', 'quantity': 150},
        {'work_item_code': 'REBAR-002', 'quantity': 5000}
    ],
    predecessors=["A001"]
)

# Generate cash flow
activities = [activity1, activity2]
cash_flow = integrator.generate_cash_flow(activities, "Building Project")

print(f"Total Cost: ${cash_flow.total_cost:,.2f}")
print(f"Project Duration: {(cash_flow.end_date - cash_flow.start_date).days} days")
```

## Common Use Cases

### 1. Monthly Cash Flow
```python
for month, cost in cash_flow.monthly_costs.items():
    print(f"{month}: ${cost:,.2f}")
```

### 2. Earned Value Analysis
```python
progress = {'A001': 100, 'A002': 60}
actual_costs = {'A001': 45000, 'A002': 72000}

evm = integrator.calculate_earned_value(
    activities,
    progress,
    actual_costs,
    data_date=date(2024, 6, 20)
)

print(f"CPI: {evm.cpi}")
print(f"SPI: {evm.spi}")
print(f"EAC: ${evm.eac:,.2f}")
```

### 3. Export Cash Flow
```python
integrator.export_cash_flow(cash_flow, "project_cash_flow.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.2 - Cost-Schedule Integration
