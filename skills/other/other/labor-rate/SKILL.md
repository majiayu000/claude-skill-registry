---
slug: "labor-rate"
display_name: "Labor Rate"
description: "Calculate construction labor rates with overhead, benefits, and productivity factors. Regional rate databases and crew composition."
---

# Labor Rate Calculator

## Overview
Labor costs account for 30-50% of construction costs. This skill calculates all-in labor rates including wages, benefits, overhead, and regional adjustments.

## Python Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class LaborCategory(Enum):
    """Labor skill categories."""
    LABORER = "laborer"
    CARPENTER = "carpenter"
    ELECTRICIAN = "electrician"
    PLUMBER = "plumber"
    IRONWORKER = "ironworker"
    MASON = "mason"
    OPERATOR = "equipment_operator"
    FOREMAN = "foreman"
    SUPERINTENDENT = "superintendent"


class WorkType(Enum):
    """Work type for productivity."""
    NEW_CONSTRUCTION = "new"
    RENOVATION = "renovation"
    DEMOLITION = "demolition"
    MAINTENANCE = "maintenance"


@dataclass
class LaborRate:
    """Complete labor rate breakdown."""
    category: str
    base_wage: float
    benefits: float
    taxes: float
    insurance: float
    overhead: float
    profit: float
    total_rate: float
    unit: str = "hour"


@dataclass
class CrewComposition:
    """Crew composition for work."""
    name: str
    workers: List[Dict[str, Any]]
    total_hourly_cost: float
    output_per_hour: float
    unit: str


class LaborRateCalculator:
    """Calculate construction labor rates."""

    # Default burden rates (percent of base wage)
    DEFAULT_BURDENS = {
        'benefits': 0.30,        # Health, pension, vacation
        'taxes': 0.10,           # FICA, unemployment
        'insurance': 0.08,       # Workers comp, liability
        'overhead': 0.15,        # General conditions
        'profit': 0.10           # Contractor profit
    }

    # Base wages by category (USD/hour, US average)
    BASE_WAGES = {
        LaborCategory.LABORER: 22,
        LaborCategory.CARPENTER: 32,
        LaborCategory.ELECTRICIAN: 38,
        LaborCategory.PLUMBER: 36,
        LaborCategory.IRONWORKER: 35,
        LaborCategory.MASON: 34,
        LaborCategory.OPERATOR: 40,
        LaborCategory.FOREMAN: 45,
        LaborCategory.SUPERINTENDENT: 55
    }

    # Regional factors
    REGIONAL_FACTORS = {
        'US_National': 1.00,
        'New_York': 1.45,
        'San_Francisco': 1.40,
        'Chicago': 1.15,
        'Houston': 0.95,
        'Atlanta': 0.90,
        'Germany_Berlin': 1.20,
        'UK_London': 1.35
    }

    def __init__(self, burden_rates: Dict[str, float] = None):
        self.burdens = burden_rates or self.DEFAULT_BURDENS

    def calculate_rate(self, category: LaborCategory,
                       region: str = 'US_National',
                       custom_wage: float = None) -> LaborRate:
        """Calculate all-in labor rate."""

        # Get base wage
        base = custom_wage or self.BASE_WAGES.get(category, 25)

        # Apply regional factor
        regional_factor = self.REGIONAL_FACTORS.get(region, 1.0)
        base *= regional_factor

        # Calculate burden components
        benefits = base * self.burdens['benefits']
        taxes = base * self.burdens['taxes']
        insurance = base * self.burdens['insurance']

        # Subtotal before markup
        subtotal = base + benefits + taxes + insurance

        # Overhead and profit
        overhead = subtotal * self.burdens['overhead']
        profit = (subtotal + overhead) * self.burdens['profit']

        total = subtotal + overhead + profit

        return LaborRate(
            category=category.value,
            base_wage=round(base, 2),
            benefits=round(benefits, 2),
            taxes=round(taxes, 2),
            insurance=round(insurance, 2),
            overhead=round(overhead, 2),
            profit=round(profit, 2),
            total_rate=round(total, 2)
        )

    def calculate_crew_cost(self, composition: Dict[LaborCategory, int],
                            region: str = 'US_National') -> float:
        """Calculate hourly cost for crew composition."""

        total = 0
        for category, count in composition.items():
            rate = self.calculate_rate(category, region)
            total += rate.total_rate * count

        return round(total, 2)

    def get_rate_table(self, region: str = 'US_National') -> pd.DataFrame:
        """Generate rate table for all categories."""

        rates = []
        for category in LaborCategory:
            rate = self.calculate_rate(category, region)
            rates.append({
                'category': rate.category,
                'base_wage': rate.base_wage,
                'benefits': rate.benefits,
                'taxes': rate.taxes,
                'insurance': rate.insurance,
                'overhead': rate.overhead,
                'profit': rate.profit,
                'total_rate': rate.total_rate
            })

        return pd.DataFrame(rates)


class ProductivityFactor:
    """Calculate productivity factors for labor."""

    # Base productivity factors
    WORK_TYPE_FACTORS = {
        WorkType.NEW_CONSTRUCTION: 1.0,
        WorkType.RENOVATION: 0.75,
        WorkType.DEMOLITION: 0.90,
        WorkType.MAINTENANCE: 0.65
    }

    # Condition factors
    CONDITION_FACTORS = {
        'ideal': 1.0,
        'normal': 0.90,
        'difficult': 0.75,
        'hazardous': 0.60,
        'confined_space': 0.50
    }

    # Weather factors
    WEATHER_FACTORS = {
        'clear': 1.0,
        'hot': 0.85,
        'cold': 0.80,
        'rain': 0.60,
        'wind': 0.75
    }

    def calculate_factor(self, work_type: WorkType,
                         condition: str = 'normal',
                         weather: str = 'clear',
                         overtime_hours: int = 0) -> float:
        """Calculate combined productivity factor."""

        base = self.WORK_TYPE_FACTORS.get(work_type, 1.0)
        cond = self.CONDITION_FACTORS.get(condition, 0.9)
        weath = self.WEATHER_FACTORS.get(weather, 1.0)

        # Overtime degradation (productivity drops after 8 hours)
        overtime_factor = 1.0
        if overtime_hours > 0:
            # Each OT hour is ~15% less productive
            overtime_factor = 1 - (overtime_hours * 0.015)

        combined = base * cond * weath * overtime_factor
        return round(max(combined, 0.3), 2)  # Minimum 30% productivity

    def adjust_labor_hours(self, base_hours: float,
                           work_type: WorkType,
                           condition: str = 'normal',
                           weather: str = 'clear') -> float:
        """Adjust labor hours for conditions."""

        factor = self.calculate_factor(work_type, condition, weather)
        return round(base_hours / factor, 1)


class CrewBuilder:
    """Build and optimize crew compositions."""

    # Standard crew compositions
    STANDARD_CREWS = {
        'concrete_pour': {
            LaborCategory.FOREMAN: 1,
            LaborCategory.CARPENTER: 2,
            LaborCategory.LABORER: 4,
            LaborCategory.OPERATOR: 1
        },
        'framing': {
            LaborCategory.FOREMAN: 1,
            LaborCategory.CARPENTER: 4,
            LaborCategory.LABORER: 2
        },
        'electrical_rough': {
            LaborCategory.FOREMAN: 1,
            LaborCategory.ELECTRICIAN: 3,
            LaborCategory.LABORER: 1
        },
        'plumbing_rough': {
            LaborCategory.FOREMAN: 1,
            LaborCategory.PLUMBER: 2,
            LaborCategory.LABORER: 1
        },
        'masonry': {
            LaborCategory.FOREMAN: 1,
            LaborCategory.MASON: 4,
            LaborCategory.LABORER: 4
        }
    }

    def __init__(self, rate_calculator: LaborRateCalculator):
        self.calc = rate_calculator

    def get_crew(self, work_type: str,
                 region: str = 'US_National') -> CrewComposition:
        """Get standard crew composition with costs."""

        if work_type not in self.STANDARD_CREWS:
            raise ValueError(f"Unknown work type: {work_type}")

        composition = self.STANDARD_CREWS[work_type]
        total_cost = self.calc.calculate_crew_cost(composition, region)

        workers = []
        for category, count in composition.items():
            rate = self.calc.calculate_rate(category, region)
            workers.append({
                'category': category.value,
                'count': count,
                'hourly_rate': rate.total_rate,
                'subtotal': rate.total_rate * count
            })

        return CrewComposition(
            name=work_type,
            workers=workers,
            total_hourly_cost=total_cost,
            output_per_hour=1.0,  # Placeholder
            unit='hour'
        )

    def custom_crew(self, workers: Dict[LaborCategory, int],
                    region: str = 'US_National') -> CrewComposition:
        """Build custom crew composition."""

        total_cost = self.calc.calculate_crew_cost(workers, region)

        worker_list = []
        for category, count in workers.items():
            rate = self.calc.calculate_rate(category, region)
            worker_list.append({
                'category': category.value,
                'count': count,
                'hourly_rate': rate.total_rate,
                'subtotal': rate.total_rate * count
            })

        return CrewComposition(
            name='custom',
            workers=worker_list,
            total_hourly_cost=total_cost,
            output_per_hour=1.0,
            unit='hour'
        )
```

## Quick Start

```python
calc = LaborRateCalculator()

# Get single rate
rate = calc.calculate_rate(LaborCategory.CARPENTER, region='New_York')
print(f"Carpenter rate NYC: ${rate.total_rate}/hr")

# Rate table
rates = calc.get_rate_table('US_National')
print(rates)
```

## Common Use Cases

### 1. Crew Cost
```python
builder = CrewBuilder(calc)
concrete_crew = builder.get_crew('concrete_pour', 'Chicago')
print(f"Crew cost: ${concrete_crew.total_hourly_cost}/hr")
```

### 2. Productivity Adjustment
```python
productivity = ProductivityFactor()
factor = productivity.calculate_factor(
    WorkType.RENOVATION,
    condition='difficult',
    weather='hot'
)
adjusted_hours = productivity.adjust_labor_hours(100, WorkType.RENOVATION)
```

## Resources
- **DDC Book**: Chapter 3.1 - Resource-Based Costing
