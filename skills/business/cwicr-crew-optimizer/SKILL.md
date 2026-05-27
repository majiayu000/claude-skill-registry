---
name: cwicr-crew-optimizer
description: "Optimize crew composition using CWICR labor norms. Balance productivity, cost, and skill requirements for construction crews."
---

# CWICR Crew Optimizer

## Business Case

### Problem Statement
Crew planning challenges:
- Right mix of workers?
- Optimal crew size?
- Balance cost vs productivity?
- Match skills to work?

### Solution
Optimize crew composition using CWICR labor productivity data to balance cost, output, and skill requirements.

### Business Value
- **Optimal productivity** - Right-sized crews
- **Cost efficiency** - No overstaffing
- **Skill matching** - Proper worker mix
- **Schedule support** - Meet deadlines

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import date, timedelta


class WorkerType(Enum):
    """Types of workers."""
    FOREMAN = "foreman"
    JOURNEYMAN = "journeyman"
    APPRENTICE = "apprentice"
    LABORER = "laborer"
    OPERATOR = "operator"
    HELPER = "helper"


class Trade(Enum):
    """Construction trades."""
    CONCRETE = "concrete"
    CARPENTRY = "carpentry"
    MASONRY = "masonry"
    STEEL = "steel"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    HVAC = "hvac"
    PAINTING = "painting"
    ROOFING = "roofing"
    GENERAL = "general"


@dataclass
class Worker:
    """Worker definition."""
    worker_type: WorkerType
    trade: Trade
    hourly_rate: float
    productivity_factor: float = 1.0
    overtime_multiplier: float = 1.5


@dataclass
class CrewComposition:
    """Crew composition."""
    name: str
    trade: Trade
    workers: List[Tuple[WorkerType, int]]  # (type, count)
    base_productivity: float  # Output per hour
    hourly_cost: float
    daily_output: float


@dataclass
class CrewOptimizationResult:
    """Result of crew optimization."""
    work_item: str
    quantity: float
    unit: str
    recommended_crew: CrewComposition
    alternative_crews: List[CrewComposition]
    duration_days: float
    total_labor_cost: float
    cost_per_unit: float


# Standard crew compositions
STANDARD_CREWS = {
    'concrete_small': {
        'trade': Trade.CONCRETE,
        'workers': [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 2), (WorkerType.LABORER, 2)],
        'productivity': 1.0
    },
    'concrete_large': {
        'trade': Trade.CONCRETE,
        'workers': [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 4), (WorkerType.LABORER, 4), (WorkerType.OPERATOR, 1)],
        'productivity': 1.8
    },
    'masonry_standard': {
        'trade': Trade.MASONRY,
        'workers': [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 2), (WorkerType.HELPER, 2)],
        'productivity': 1.0
    },
    'carpentry_framing': {
        'trade': Trade.CARPENTRY,
        'workers': [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 3), (WorkerType.APPRENTICE, 1)],
        'productivity': 1.0
    },
    'electrical_rough': {
        'trade': Trade.ELECTRICAL,
        'workers': [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 2), (WorkerType.APPRENTICE, 1)],
        'productivity': 1.0
    },
    'plumbing_rough': {
        'trade': Trade.PLUMBING,
        'workers': [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 2), (WorkerType.APPRENTICE, 1)],
        'productivity': 1.0
    }
}

# Default hourly rates by worker type
DEFAULT_RATES = {
    WorkerType.FOREMAN: 65,
    WorkerType.JOURNEYMAN: 55,
    WorkerType.APPRENTICE: 35,
    WorkerType.LABORER: 30,
    WorkerType.OPERATOR: 60,
    WorkerType.HELPER: 28
}


class CWICRCrewOptimizer:
    """Optimize crew composition using CWICR data."""

    HOURS_PER_DAY = 8

    def __init__(self,
                 cwicr_data: pd.DataFrame = None,
                 custom_rates: Dict[WorkerType, float] = None):
        self.cost_data = cwicr_data
        self.rates = custom_rates or DEFAULT_RATES
        if cwicr_data is not None:
            self._index_data()

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def get_labor_norm(self, code: str) -> Tuple[float, str]:
        """Get labor hours per unit from CWICR."""
        if self._code_index is None or code not in self._code_index.index:
            return (1.0, 'unit')

        item = self._code_index.loc[code]
        norm = float(item.get('labor_norm', item.get('labor_hours', 1)) or 1)
        unit = str(item.get('unit', 'unit'))

        return (norm, unit)

    def calculate_crew_cost(self, workers: List[Tuple[WorkerType, int]]) -> float:
        """Calculate hourly cost of crew."""
        total = 0
        for worker_type, count in workers:
            rate = self.rates.get(worker_type, 40)
            total += rate * count
        return total

    def build_crew(self,
                   name: str,
                   trade: Trade,
                   workers: List[Tuple[WorkerType, int]],
                   base_productivity: float = 1.0) -> CrewComposition:
        """Build crew composition."""

        hourly_cost = self.calculate_crew_cost(workers)
        daily_output = base_productivity * self.HOURS_PER_DAY

        return CrewComposition(
            name=name,
            trade=trade,
            workers=workers,
            base_productivity=base_productivity,
            hourly_cost=hourly_cost,
            daily_output=daily_output
        )

    def optimize_for_work(self,
                           work_item_code: str,
                           quantity: float,
                           target_days: int = None,
                           max_crew_size: int = 10) -> CrewOptimizationResult:
        """Optimize crew for specific work item."""

        labor_norm, unit = self.get_labor_norm(work_item_code)
        total_hours = quantity * labor_norm

        # Detect trade from code
        trade = self._detect_trade(work_item_code)

        # Generate crew options
        crews = []

        # Small crew
        small_workers = [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 2), (WorkerType.LABORER, 1)]
        small_crew = self.build_crew("Small Crew", trade, small_workers, 1.0)
        crews.append(small_crew)

        # Medium crew
        med_workers = [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 3), (WorkerType.LABORER, 2)]
        med_crew = self.build_crew("Medium Crew", trade, med_workers, 1.4)
        crews.append(med_crew)

        # Large crew
        large_workers = [(WorkerType.FOREMAN, 1), (WorkerType.JOURNEYMAN, 5), (WorkerType.LABORER, 3)]
        large_crew = self.build_crew("Large Crew", trade, large_workers, 2.0)
        crews.append(large_crew)

        # Calculate metrics for each crew
        results = []
        for crew in crews:
            # Adjusted productivity considering crew efficiency
            crew_workers = sum(count for _, count in crew.workers)
            efficiency = self._crew_efficiency(crew_workers)

            effective_productivity = crew.base_productivity * efficiency
            hours_needed = total_hours / effective_productivity
            days_needed = hours_needed / self.HOURS_PER_DAY
            labor_cost = hours_needed * crew.hourly_cost
            cost_per_unit = labor_cost / quantity if quantity > 0 else 0

            results.append({
                'crew': crew,
                'days': days_needed,
                'cost': labor_cost,
                'cost_per_unit': cost_per_unit,
                'efficiency': efficiency
            })

        # Select best crew based on target
        if target_days:
            # Find crew that meets target with lowest cost
            valid = [r for r in results if r['days'] <= target_days]
            if valid:
                best = min(valid, key=lambda x: x['cost'])
            else:
                best = min(results, key=lambda x: x['days'])
        else:
            # Optimize for cost
            best = min(results, key=lambda x: x['cost'])

        recommended = best['crew']
        alternatives = [r['crew'] for r in results if r['crew'] != recommended]

        return CrewOptimizationResult(
            work_item=work_item_code,
            quantity=quantity,
            unit=unit,
            recommended_crew=recommended,
            alternative_crews=alternatives,
            duration_days=round(best['days'], 1),
            total_labor_cost=round(best['cost'], 2),
            cost_per_unit=round(best['cost_per_unit'], 2)
        )

    def _detect_trade(self, code: str) -> Trade:
        """Detect trade from work item code."""
        code_lower = code.lower()

        trade_map = {
            'conc': Trade.CONCRETE,
            'carp': Trade.CARPENTRY,
            'mason': Trade.MASONRY,
            'steel': Trade.STEEL,
            'strl': Trade.STEEL,
            'elec': Trade.ELECTRICAL,
            'plumb': Trade.PLUMBING,
            'hvac': Trade.HVAC,
            'paint': Trade.PAINTING,
            'roof': Trade.ROOFING
        }

        for key, trade in trade_map.items():
            if key in code_lower:
                return trade

        return Trade.GENERAL

    def _crew_efficiency(self, crew_size: int) -> float:
        """Calculate crew efficiency based on size (law of diminishing returns)."""
        if crew_size <= 4:
            return 1.0
        elif crew_size <= 6:
            return 0.95
        elif crew_size <= 8:
            return 0.90
        elif crew_size <= 10:
            return 0.85
        else:
            return 0.80

    def analyze_overtime(self,
                          result: CrewOptimizationResult,
                          available_days: int,
                          max_overtime_hours: float = 2) -> Dict[str, Any]:
        """Analyze if overtime can meet schedule."""

        if result.duration_days <= available_days:
            return {
                'overtime_needed': False,
                'regular_days': result.duration_days,
                'overtime_hours': 0,
                'overtime_cost': 0,
                'total_cost': result.total_labor_cost
            }

        # Calculate overtime needed
        regular_hours = available_days * self.HOURS_PER_DAY
        total_hours_available = available_days * (self.HOURS_PER_DAY + max_overtime_hours)

        labor_norm, _ = self.get_labor_norm(result.work_item)
        total_hours_needed = result.quantity * labor_norm / result.recommended_crew.base_productivity

        if total_hours_needed > total_hours_available:
            # Can't meet schedule even with overtime
            overtime_hours = available_days * max_overtime_hours
            shortage = total_hours_needed - total_hours_available
        else:
            overtime_hours = total_hours_needed - regular_hours
            shortage = 0

        overtime_cost = overtime_hours * result.recommended_crew.hourly_cost * 1.5

        return {
            'overtime_needed': True,
            'regular_days': available_days,
            'overtime_hours_per_day': max_overtime_hours,
            'total_overtime_hours': round(overtime_hours, 1),
            'overtime_cost': round(overtime_cost, 2),
            'total_cost': round(result.total_labor_cost + overtime_cost, 2),
            'shortage_hours': round(shortage, 1) if shortage > 0 else 0,
            'can_meet_schedule': shortage == 0
        }

    def export_crew_plan(self,
                          results: List[CrewOptimizationResult],
                          output_path: str) -> str:
        """Export crew plan to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_data = []
            for r in results:
                workers_str = ", ".join(f"{count}x {wt.value}" for wt, count in r.recommended_crew.workers)
                summary_data.append({
                    'Work Item': r.work_item,
                    'Quantity': r.quantity,
                    'Unit': r.unit,
                    'Crew': r.recommended_crew.name,
                    'Workers': workers_str,
                    'Duration Days': r.duration_days,
                    'Labor Cost': r.total_labor_cost,
                    'Cost/Unit': r.cost_per_unit
                })

            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Crew Plan', index=False)

            # Totals
            totals_df = pd.DataFrame([{
                'Total Duration': max(r.duration_days for r in results),
                'Total Labor Cost': sum(r.total_labor_cost for r in results)
            }])
            totals_df.to_excel(writer, sheet_name='Totals', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize optimizer
optimizer = CWICRCrewOptimizer(cwicr)

# Optimize crew for work item
result = optimizer.optimize_for_work(
    work_item_code="CONC-SLAB-001",
    quantity=500,  # m2
    target_days=10
)

print(f"Recommended: {result.recommended_crew.name}")
print(f"Duration: {result.duration_days} days")
print(f"Labor Cost: ${result.total_labor_cost:,.2f}")
```

## Common Use Cases

### 1. Meet Schedule with Overtime
```python
overtime = optimizer.analyze_overtime(result, available_days=8)
print(f"Overtime needed: {overtime['overtime_needed']}")
print(f"Total cost: ${overtime['total_cost']:,.2f}")
```

### 2. Compare Crews
```python
for crew in [result.recommended_crew] + result.alternative_crews:
    print(f"{crew.name}: ${crew.hourly_cost}/hr")
```

### 3. Custom Crew
```python
custom = optimizer.build_crew(
    name="Custom Concrete",
    trade=Trade.CONCRETE,
    workers=[
        (WorkerType.FOREMAN, 1),
        (WorkerType.JOURNEYMAN, 4),
        (WorkerType.LABORER, 2)
    ],
    base_productivity=1.5
)
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Crew Productivity Analysis
