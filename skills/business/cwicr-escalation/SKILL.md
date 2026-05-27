---
name: cwicr-escalation
description: "Apply price escalation to CWICR estimates over time. Calculate inflation adjustments, material price indices, and labor rate increases."
---

# CWICR Escalation Calculator

## Business Case

### Problem Statement
Construction costs change over time:
- Inflation affects all costs
- Material prices fluctuate
- Labor rates increase annually
- Long projects need escalation

### Solution
Time-based cost escalation using historical indices, projected rates, and category-specific escalation factors.

### Business Value
- **Future pricing** - Estimate costs at construction time
- **Budget planning** - Account for inflation
- **Contract pricing** - Escalation clauses
- **Historical analysis** - Adjust past costs to current

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from enum import Enum


class EscalationType(Enum):
    """Types of escalation."""
    LABOR = "labor"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    GENERAL = "general"


@dataclass
class EscalationIndex:
    """Escalation index for a period."""
    period: str  # YYYY-MM
    labor_index: float
    material_index: float
    equipment_index: float
    general_index: float


@dataclass
class EscalationResult:
    """Result of escalation calculation."""
    base_cost: float
    base_date: date
    target_date: date
    months: int
    escalation_rate: float
    escalation_amount: float
    escalated_cost: float
    by_category: Dict[str, Dict[str, float]]


# Historical escalation rates (annual %)
HISTORICAL_RATES = {
    2020: {'labor': 2.5, 'material': 1.8, 'equipment': 1.5, 'general': 2.0},
    2021: {'labor': 3.2, 'material': 8.5, 'equipment': 2.0, 'general': 4.5},
    2022: {'labor': 4.5, 'material': 12.0, 'equipment': 3.5, 'general': 7.0},
    2023: {'labor': 4.0, 'material': 5.0, 'equipment': 3.0, 'general': 4.0},
    2024: {'labor': 3.5, 'material': 3.0, 'equipment': 2.5, 'general': 3.0},
    2025: {'labor': 3.0, 'material': 2.5, 'equipment': 2.0, 'general': 2.5},
}

# Material-specific escalation factors
MATERIAL_ESCALATION = {
    'steel': 1.20,      # Higher volatility
    'lumber': 1.30,     # High volatility
    'concrete': 0.90,   # Lower volatility
    'copper': 1.25,     # Commodity driven
    'aluminum': 1.15,
    'plastic': 1.10,
    'glass': 0.95,
    'default': 1.00
}


class CWICREscalation:
    """Calculate cost escalation over time."""

    def __init__(self,
                 cwicr_data: pd.DataFrame = None,
                 custom_rates: Dict[int, Dict[str, float]] = None):
        self.cost_data = cwicr_data
        self.rates = custom_rates or HISTORICAL_RATES
        if cwicr_data is not None:
            self._index_data()

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def get_rate(self,
                  year: int,
                  category: EscalationType = EscalationType.GENERAL) -> float:
        """Get escalation rate for year and category."""
        year_rates = self.rates.get(year, self.rates.get(max(self.rates.keys())))
        return year_rates.get(category.value, year_rates.get('general', 3.0))

    def calculate_compound_factor(self,
                                   base_date: date,
                                   target_date: date,
                                   category: EscalationType = EscalationType.GENERAL) -> float:
        """Calculate compound escalation factor between dates."""

        if target_date <= base_date:
            return 1.0

        factor = 1.0
        current = base_date

        while current < target_date:
            year = current.year
            annual_rate = self.get_rate(year, category) / 100

            # Calculate months in this year
            year_end = date(year + 1, 1, 1)
            if target_date < year_end:
                months = (target_date.year - current.year) * 12 + target_date.month - current.month
            else:
                months = (year_end.year - current.year) * 12 + year_end.month - current.month

            # Apply monthly compound rate
            monthly_rate = (1 + annual_rate) ** (1/12) - 1
            factor *= (1 + monthly_rate) ** months

            current = year_end

        return factor

    def escalate_cost(self,
                       base_cost: float,
                       base_date: date,
                       target_date: date,
                       cost_breakdown: Dict[str, float] = None) -> EscalationResult:
        """Escalate cost from base date to target date."""

        if cost_breakdown is None:
            cost_breakdown = {
                'labor': base_cost * 0.40,
                'material': base_cost * 0.45,
                'equipment': base_cost * 0.15
            }

        months = (target_date.year - base_date.year) * 12 + target_date.month - base_date.month

        # Escalate each category
        by_category = {}
        total_escalated = 0

        for category, amount in cost_breakdown.items():
            esc_type = EscalationType.LABOR if category == 'labor' else \
                       EscalationType.MATERIAL if category == 'material' else \
                       EscalationType.EQUIPMENT if category == 'equipment' else \
                       EscalationType.GENERAL

            factor = self.calculate_compound_factor(base_date, target_date, esc_type)
            escalated = amount * factor
            escalation = escalated - amount

            by_category[category] = {
                'base': round(amount, 2),
                'factor': round(factor, 4),
                'escalated': round(escalated, 2),
                'escalation': round(escalation, 2)
            }

            total_escalated += escalated

        total_escalation = total_escalated - base_cost
        esc_rate = (total_escalation / base_cost * 100) if base_cost > 0 else 0

        return EscalationResult(
            base_cost=round(base_cost, 2),
            base_date=base_date,
            target_date=target_date,
            months=months,
            escalation_rate=round(esc_rate, 2),
            escalation_amount=round(total_escalation, 2),
            escalated_cost=round(total_escalated, 2),
            by_category=by_category
        )

    def escalate_estimate(self,
                           items: List[Dict[str, Any]],
                           base_date: date,
                           target_date: date) -> Dict[str, Any]:
        """Escalate entire estimate."""

        escalated_items = []
        total_base = 0
        total_escalated = 0

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            # Get costs from CWICR
            labor = 0
            material = 0
            equipment = 0

            if self._code_index is not None and code in self._code_index.index:
                wi = self._code_index.loc[code]
                labor = float(wi.get('labor_cost', 0) or 0) * qty
                material = float(wi.get('material_cost', 0) or 0) * qty
                equipment = float(wi.get('equipment_cost', 0) or 0) * qty

            base = labor + material + equipment
            breakdown = {'labor': labor, 'material': material, 'equipment': equipment}

            result = self.escalate_cost(base, base_date, target_date, breakdown)

            escalated_items.append({
                'code': code,
                'base_cost': result.base_cost,
                'escalated_cost': result.escalated_cost,
                'escalation': result.escalation_amount
            })

            total_base += base
            total_escalated += result.escalated_cost

        return {
            'items': escalated_items,
            'total_base': round(total_base, 2),
            'total_escalated': round(total_escalated, 2),
            'total_escalation': round(total_escalated - total_base, 2),
            'escalation_rate': round((total_escalated - total_base) / total_base * 100, 2) if total_base > 0 else 0,
            'base_date': base_date,
            'target_date': target_date
        }

    def project_future_costs(self,
                              base_cost: float,
                              base_date: date,
                              years_forward: int = 5,
                              annual_rate: float = None) -> pd.DataFrame:
        """Project costs for multiple future years."""

        projections = []
        current = base_cost

        for i in range(years_forward + 1):
            target = base_date + relativedelta(years=i)
            year = target.year

            if annual_rate is None:
                rate = self.get_rate(year)
            else:
                rate = annual_rate

            if i > 0:
                current = current * (1 + rate / 100)

            projections.append({
                'Year': year,
                'Date': target,
                'Annual Rate': f"{rate}%",
                'Projected Cost': round(current, 2),
                'Cumulative Escalation': round(current - base_cost, 2),
                'Cumulative %': round((current - base_cost) / base_cost * 100, 1)
            })

        return pd.DataFrame(projections)

    def de_escalate_cost(self,
                          current_cost: float,
                          current_date: date,
                          base_date: date,
                          category: EscalationType = EscalationType.GENERAL) -> Dict[str, Any]:
        """De-escalate current cost back to base date."""

        factor = self.calculate_compound_factor(base_date, current_date, category)
        base_cost = current_cost / factor

        return {
            'current_cost': round(current_cost, 2),
            'current_date': current_date,
            'base_date': base_date,
            'de_escalation_factor': round(1 / factor, 4),
            'base_cost': round(base_cost, 2),
            'category': category.value
        }

    def export_escalation(self,
                          result: EscalationResult,
                          output_path: str) -> str:
        """Export escalation to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Base Cost': result.base_cost,
                'Base Date': result.base_date,
                'Target Date': result.target_date,
                'Months': result.months,
                'Escalation Rate': f"{result.escalation_rate}%",
                'Escalation Amount': result.escalation_amount,
                'Escalated Cost': result.escalated_cost
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # By Category
            cat_df = pd.DataFrame([
                {
                    'Category': cat,
                    'Base': data['base'],
                    'Factor': data['factor'],
                    'Escalated': data['escalated'],
                    'Escalation': data['escalation']
                }
                for cat, data in result.by_category.items()
            ])
            cat_df.to_excel(writer, sheet_name='By Category', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date

# Initialize escalation calculator
esc = CWICREscalation()

# Escalate single cost
result = esc.escalate_cost(
    base_cost=1000000,
    base_date=date(2024, 1, 1),
    target_date=date(2026, 6, 1)
)

print(f"Base Cost: ${result.base_cost:,.2f}")
print(f"Escalated: ${result.escalated_cost:,.2f}")
print(f"Escalation: {result.escalation_rate}%")
```

## Common Use Cases

### 1. Project Future Costs
```python
projections = esc.project_future_costs(
    base_cost=5000000,
    base_date=date.today(),
    years_forward=5
)
print(projections)
```

### 2. Escalate Estimate
```python
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")
esc = CWICREscalation(cwicr)

items = [
    {'work_item_code': 'CONC-001', 'quantity': 150},
    {'work_item_code': 'STRL-002', 'quantity': 25}
]

escalated = esc.escalate_estimate(
    items,
    base_date=date(2024, 1, 1),
    target_date=date(2025, 12, 1)
)
```

### 3. De-escalate Historical Cost
```python
base_cost = esc.de_escalate_cost(
    current_cost=1200000,
    current_date=date(2024, 6, 1),
    base_date=date(2020, 1, 1)
)
print(f"2020 equivalent: ${base_cost['base_cost']:,.2f}")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Cost Escalation Methods
