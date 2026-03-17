---
name: "cwicr-overhead-markup"
description: "Apply overhead, profit, and markup to CWICR estimates. Calculate indirect costs, general conditions, and contractor margins."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Overhead & Markup Calculator

## Business Case

### Problem Statement
Direct costs need additional markups:
- General overhead (office, insurance)
- Project overhead (site costs)
- Profit margins
- Bonds and insurance

### Solution
Systematic markup application to CWICR direct costs with configurable rates for overhead, profit, bonds, and other indirect costs.

### Business Value
- **Complete pricing** - From cost to selling price
- **Configurable rates** - By project/client type
- **Transparency** - Clear markup breakdown
- **Consistency** - Standard markup application

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MarkupType(Enum):
    """Types of markup."""
    OVERHEAD = "overhead"
    PROFIT = "profit"
    BOND = "bond"
    INSURANCE = "insurance"
    CONTINGENCY = "contingency"
    TAX = "tax"
    ESCALATION = "escalation"
    CUSTOM = "custom"


class MarkupMethod(Enum):
    """Markup calculation methods."""
    ON_COST = "on_cost"              # Markup on direct cost
    ON_COST_PLUS = "on_cost_plus"    # Markup on cost + previous markups
    FIXED = "fixed"                   # Fixed amount


@dataclass
class MarkupItem:
    """Single markup item."""
    name: str
    markup_type: MarkupType
    rate: float
    method: MarkupMethod
    base_amount: float
    markup_amount: float


@dataclass
class MarkupSchedule:
    """Complete markup schedule."""
    name: str
    markups: List[MarkupItem]

    def get_total_rate(self) -> float:
        """Get combined markup rate."""
        return sum(m.rate for m in self.markups)


@dataclass
class PricingResult:
    """Complete pricing with all markups."""
    direct_cost: float
    labor_cost: float
    material_cost: float
    equipment_cost: float
    subcontractor_cost: float
    markups: List[MarkupItem]
    total_markup: float
    total_price: float
    markup_percentage: float


# Standard markup templates
MARKUP_TEMPLATES = {
    'residential': {
        'overhead': 0.10,
        'profit': 0.10,
        'contingency': 0.05
    },
    'commercial': {
        'overhead': 0.12,
        'profit': 0.08,
        'bond': 0.015,
        'insurance': 0.02,
        'contingency': 0.05
    },
    'industrial': {
        'overhead': 0.15,
        'profit': 0.08,
        'bond': 0.02,
        'insurance': 0.025,
        'contingency': 0.08
    },
    'government': {
        'overhead': 0.12,
        'profit': 0.06,
        'bond': 0.025,
        'contingency': 0.05
    },
    'subcontractor': {
        'overhead': 0.08,
        'profit': 0.10
    }
}


class CWICROverheadMarkup:
    """Apply overhead and markup to CWICR estimates."""

    def __init__(self, cwicr_data: pd.DataFrame = None):
        self.cost_data = cwicr_data
        if cwicr_data is not None:
            self._index_data()

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def get_template(self, template_name: str) -> Dict[str, float]:
        """Get markup template."""
        return MARKUP_TEMPLATES.get(template_name, MARKUP_TEMPLATES['commercial'])

    def create_markup_schedule(self,
                                name: str,
                                markups: Dict[str, float],
                                method: MarkupMethod = MarkupMethod.ON_COST) -> MarkupSchedule:
        """Create markup schedule from rates."""

        items = []
        for markup_name, rate in markups.items():
            markup_type = MarkupType.CUSTOM
            for mt in MarkupType:
                if mt.value in markup_name.lower():
                    markup_type = mt
                    break

            items.append(MarkupItem(
                name=markup_name,
                markup_type=markup_type,
                rate=rate,
                method=method,
                base_amount=0,
                markup_amount=0
            ))

        return MarkupSchedule(name=name, markups=items)

    def apply_markups(self,
                      direct_cost: float,
                      schedule: MarkupSchedule,
                      cost_breakdown: Dict[str, float] = None) -> PricingResult:
        """Apply markup schedule to direct cost."""

        if cost_breakdown is None:
            cost_breakdown = {
                'labor': direct_cost * 0.40,
                'material': direct_cost * 0.45,
                'equipment': direct_cost * 0.10,
                'subcontractor': direct_cost * 0.05
            }

        markup_items = []
        running_total = direct_cost

        for markup in schedule.markups:
            if markup.method == MarkupMethod.ON_COST:
                base = direct_cost
            elif markup.method == MarkupMethod.ON_COST_PLUS:
                base = running_total
            else:  # FIXED
                base = 1

            amount = base * markup.rate

            markup_items.append(MarkupItem(
                name=markup.name,
                markup_type=markup.markup_type,
                rate=markup.rate,
                method=markup.method,
                base_amount=round(base, 2),
                markup_amount=round(amount, 2)
            ))

            running_total += amount

        total_markup = running_total - direct_cost
        markup_pct = (total_markup / direct_cost * 100) if direct_cost > 0 else 0

        return PricingResult(
            direct_cost=round(direct_cost, 2),
            labor_cost=round(cost_breakdown.get('labor', 0), 2),
            material_cost=round(cost_breakdown.get('material', 0), 2),
            equipment_cost=round(cost_breakdown.get('equipment', 0), 2),
            subcontractor_cost=round(cost_breakdown.get('subcontractor', 0), 2),
            markups=markup_items,
            total_markup=round(total_markup, 2),
            total_price=round(running_total, 2),
            markup_percentage=round(markup_pct, 1)
        )

    def price_estimate(self,
                       items: List[Dict[str, Any]],
                       template: str = 'commercial') -> PricingResult:
        """Price complete estimate with markups."""

        # Calculate direct costs
        labor = 0
        material = 0
        equipment = 0
        subcontractor = 0

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if self._code_index is not None and code in self._code_index.index:
                wi = self._code_index.loc[code]
                labor += float(wi.get('labor_cost', 0) or 0) * qty
                material += float(wi.get('material_cost', 0) or 0) * qty
                equipment += float(wi.get('equipment_cost', 0) or 0) * qty

            subcontractor += item.get('subcontractor_cost', 0)

        direct_cost = labor + material + equipment + subcontractor
        cost_breakdown = {
            'labor': labor,
            'material': material,
            'equipment': equipment,
            'subcontractor': subcontractor
        }

        # Get template and create schedule
        rates = self.get_template(template)
        schedule = self.create_markup_schedule(template, rates)

        return self.apply_markups(direct_cost, schedule, cost_breakdown)

    def calculate_bid_price(self,
                            direct_cost: float,
                            overhead_rate: float = 0.12,
                            profit_rate: float = 0.08,
                            bond_rate: float = 0.015,
                            contingency_rate: float = 0.05) -> Dict[str, Any]:
        """Calculate bid price with standard markups."""

        overhead = direct_cost * overhead_rate
        subtotal1 = direct_cost + overhead

        profit = subtotal1 * profit_rate
        subtotal2 = subtotal1 + profit

        bond = subtotal2 * bond_rate
        subtotal3 = subtotal2 + bond

        contingency = direct_cost * contingency_rate

        total = subtotal3 + contingency

        return {
            'direct_cost': round(direct_cost, 2),
            'overhead': round(overhead, 2),
            'overhead_rate': f"{overhead_rate:.1%}",
            'profit': round(profit, 2),
            'profit_rate': f"{profit_rate:.1%}",
            'bond': round(bond, 2),
            'bond_rate': f"{bond_rate:.1%}",
            'contingency': round(contingency, 2),
            'contingency_rate': f"{contingency_rate:.1%}",
            'bid_price': round(total, 2),
            'total_markup': round(total - direct_cost, 2),
            'total_markup_pct': round((total - direct_cost) / direct_cost * 100, 1)
        }

    def compare_markup_scenarios(self,
                                  direct_cost: float,
                                  scenarios: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """Compare different markup scenarios."""

        results = []

        for name, rates in scenarios.items():
            schedule = self.create_markup_schedule(name, rates)
            pricing = self.apply_markups(direct_cost, schedule)

            results.append({
                'Scenario': name,
                'Direct Cost': pricing.direct_cost,
                'Total Markup': pricing.total_markup,
                'Markup %': pricing.markup_percentage,
                'Total Price': pricing.total_price
            })

        return pd.DataFrame(results)

    def export_pricing(self,
                        result: PricingResult,
                        output_path: str) -> str:
        """Export pricing breakdown to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Direct Cost': result.direct_cost,
                'Labor': result.labor_cost,
                'Material': result.material_cost,
                'Equipment': result.equipment_cost,
                'Subcontractor': result.subcontractor_cost,
                'Total Markup': result.total_markup,
                'Markup %': result.markup_percentage,
                'Total Price': result.total_price
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Markup Details
            markup_df = pd.DataFrame([
                {
                    'Markup': m.name,
                    'Type': m.markup_type.value,
                    'Rate': f"{m.rate:.1%}",
                    'Base': m.base_amount,
                    'Amount': m.markup_amount
                }
                for m in result.markups
            ])
            markup_df.to_excel(writer, sheet_name='Markups', index=False)

        return output_path
```

## Quick Start

```python
# Initialize markup calculator
markup = CWICROverheadMarkup()

# Calculate bid price
bid = markup.calculate_bid_price(
    direct_cost=1000000,
    overhead_rate=0.12,
    profit_rate=0.08
)

print(f"Direct Cost: ${bid['direct_cost']:,.2f}")
print(f"Bid Price: ${bid['bid_price']:,.2f}")
print(f"Total Markup: {bid['total_markup_pct']}%")
```

## Common Use Cases

### 1. Template-Based Pricing
```python
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")
markup = CWICROverheadMarkup(cwicr)

items = [
    {'work_item_code': 'CONC-001', 'quantity': 150},
    {'work_item_code': 'STRL-002', 'quantity': 25}
]

pricing = markup.price_estimate(items, template='commercial')
print(f"Total Price: ${pricing.total_price:,.2f}")
```

### 2. Compare Scenarios
```python
scenarios = {
    'Aggressive': {'overhead': 0.08, 'profit': 0.05},
    'Standard': {'overhead': 0.12, 'profit': 0.08},
    'Premium': {'overhead': 0.15, 'profit': 0.12}
}

comparison = markup.compare_markup_scenarios(1000000, scenarios)
print(comparison)
```

### 3. Custom Markup Schedule
```python
schedule = markup.create_markup_schedule('Custom', {
    'overhead': 0.10,
    'profit': 0.08,
    'bond': 0.02,
    'insurance': 0.015
})

pricing = markup.apply_markups(500000, schedule)
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Cost Markup Methods
