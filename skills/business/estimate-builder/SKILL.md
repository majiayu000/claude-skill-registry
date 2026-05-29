---
name: "estimate-builder"
description: "Build construction project estimates. Generate detailed cost breakdowns with labor, materials, equipment, and overhead."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw":{"emoji":"📊","os":["darwin","linux","win32"],"homepage":"https://datadrivenconstruction.io","requires":{"bins":["python3"]}}}
---

# Estimate Builder

## Business Case

### Problem Statement
Estimate creation challenges:
- Complex cost structures
- Multiple cost categories
- Markup calculations
- Format requirements vary

### Solution
Structured estimate builder that creates professional construction estimates with proper cost categorization, markups, and export capabilities.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class CostCategory(Enum):
    LABOR = "labor"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    SUBCONTRACTOR = "subcontractor"
    OTHER = "other"


@dataclass
class EstimateLineItem:
    line_number: int
    wbs_code: str
    description: str
    quantity: float
    unit: str
    unit_cost: float
    category: CostCategory
    notes: str = ""

    @property
    def total_cost(self) -> float:
        return round(self.quantity * self.unit_cost, 2)


@dataclass
class CostSummary:
    labor: float = 0
    material: float = 0
    equipment: float = 0
    subcontractor: float = 0
    other: float = 0

    @property
    def direct_cost(self) -> float:
        return self.labor + self.material + self.equipment + self.subcontractor + self.other


@dataclass
class Markup:
    name: str
    rate: float  # As decimal (0.10 = 10%)
    base: str = "direct"  # "direct" or "subtotal"


class EstimateBuilder:
    """Build construction project estimates."""

    def __init__(self, project_name: str, project_number: str = ""):
        self.project_name = project_name
        self.project_number = project_number
        self.estimate_date = date.today()
        self.items: List[EstimateLineItem] = []
        self.markups: List[Markup] = []
        self._next_line = 1

    def add_item(self,
                 wbs_code: str,
                 description: str,
                 quantity: float,
                 unit: str,
                 unit_cost: float,
                 category: CostCategory = CostCategory.OTHER,
                 notes: str = "") -> EstimateLineItem:
        """Add line item to estimate."""

        item = EstimateLineItem(
            line_number=self._next_line,
            wbs_code=wbs_code,
            description=description,
            quantity=quantity,
            unit=unit,
            unit_cost=unit_cost,
            category=category,
            notes=notes
        )
        self.items.append(item)
        self._next_line += 1
        return item

    def add_markup(self, name: str, rate: float, base: str = "direct"):
        """Add markup (overhead, profit, contingency, etc.)."""
        self.markups.append(Markup(name=name, rate=rate, base=base))

    def set_standard_markups(self,
                             overhead: float = 0.15,
                             profit: float = 0.10,
                             contingency: float = 0.05):
        """Set standard construction markups."""

        self.markups = [
            Markup("General Conditions / Overhead", overhead, "direct"),
            Markup("Profit", profit, "subtotal"),
            Markup("Contingency", contingency, "subtotal")
        ]

    def get_cost_summary(self) -> CostSummary:
        """Get cost summary by category."""

        summary = CostSummary()
        for item in self.items:
            cost = item.total_cost
            if item.category == CostCategory.LABOR:
                summary.labor += cost
            elif item.category == CostCategory.MATERIAL:
                summary.material += cost
            elif item.category == CostCategory.EQUIPMENT:
                summary.equipment += cost
            elif item.category == CostCategory.SUBCONTRACTOR:
                summary.subcontractor += cost
            else:
                summary.other += cost
        return summary

    def calculate_total(self) -> Dict[str, Any]:
        """Calculate total estimate with markups."""

        summary = self.get_cost_summary()
        direct_cost = summary.direct_cost

        markups_detail = []
        subtotal = direct_cost

        for markup in self.markups:
            if markup.base == "direct":
                amount = direct_cost * markup.rate
            else:
                amount = subtotal * markup.rate

            markups_detail.append({
                'name': markup.name,
                'rate': f"{markup.rate * 100:.1f}%",
                'amount': round(amount, 2)
            })
            subtotal += amount

        return {
            'cost_summary': {
                'labor': round(summary.labor, 2),
                'material': round(summary.material, 2),
                'equipment': round(summary.equipment, 2),
                'subcontractor': round(summary.subcontractor, 2),
                'other': round(summary.other, 2),
                'direct_cost': round(direct_cost, 2)
            },
            'markups': markups_detail,
            'total_markups': round(subtotal - direct_cost, 2),
            'grand_total': round(subtotal, 2)
        }

    def get_items_by_wbs(self) -> Dict[str, List[EstimateLineItem]]:
        """Group items by WBS code prefix."""

        by_wbs = {}
        for item in self.items:
            prefix = item.wbs_code.split('.')[0] if '.' in item.wbs_code else item.wbs_code
            if prefix not in by_wbs:
                by_wbs[prefix] = []
            by_wbs[prefix].append(item)
        return by_wbs

    def import_from_df(self, df: pd.DataFrame):
        """Import line items from DataFrame."""

        for _, row in df.iterrows():
            self.add_item(
                wbs_code=str(row.get('wbs_code', '')),
                description=row['description'],
                quantity=float(row['quantity']),
                unit=row['unit'],
                unit_cost=float(row['unit_cost']),
                category=CostCategory(row.get('category', 'other').lower()),
                notes=row.get('notes', '')
            )

    def export_to_df(self) -> pd.DataFrame:
        """Export estimate to DataFrame."""

        data = []
        for item in self.items:
            data.append({
                'Line': item.line_number,
                'WBS': item.wbs_code,
                'Description': item.description,
                'Qty': item.quantity,
                'Unit': item.unit,
                'Unit Cost': item.unit_cost,
                'Total': item.total_cost,
                'Category': item.category.value,
                'Notes': item.notes
            })
        return pd.DataFrame(data)

    def export_to_excel(self, output_path: str) -> str:
        """Export estimate to Excel."""

        totals = self.calculate_total()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Cover sheet
            cover_df = pd.DataFrame([{
                'Project Name': self.project_name,
                'Project Number': self.project_number,
                'Estimate Date': self.estimate_date,
                'Total Items': len(self.items),
                'Direct Cost': totals['cost_summary']['direct_cost'],
                'Grand Total': totals['grand_total']
            }])
            cover_df.to_excel(writer, sheet_name='Summary', index=False)

            # Line items
            items_df = self.export_to_df()
            items_df.to_excel(writer, sheet_name='Line Items', index=False)

            # Cost breakdown
            breakdown_df = pd.DataFrame([totals['cost_summary']])
            breakdown_df.to_excel(writer, sheet_name='Cost Breakdown', index=False)

            # Markups
            if totals['markups']:
                markups_df = pd.DataFrame(totals['markups'])
                markups_df.to_excel(writer, sheet_name='Markups', index=False)

        return output_path

    def validate(self) -> List[str]:
        """Validate estimate for common issues."""

        issues = []

        if not self.items:
            issues.append("Estimate has no line items")

        for item in self.items:
            if item.quantity <= 0:
                issues.append(f"Line {item.line_number}: Invalid quantity")
            if item.unit_cost < 0:
                issues.append(f"Line {item.line_number}: Negative unit cost")
            if not item.description:
                issues.append(f"Line {item.line_number}: Missing description")

        if not self.markups:
            issues.append("No markups defined (overhead, profit)")

        return issues
```

## Quick Start

```python
# Create estimate
estimate = EstimateBuilder("Office Building A", "PRJ-2024-001")

# Add line items
estimate.add_item("01.01", "Site Preparation", 5000, "SF", 2.50, CostCategory.OTHER)
estimate.add_item("03.01", "Concrete Foundation", 200, "CY", 350, CostCategory.MATERIAL)
estimate.add_item("03.02", "Foundation Formwork", 1500, "SF", 8.50, CostCategory.LABOR)
estimate.add_item("05.01", "Structural Steel", 50, "TON", 4500, CostCategory.SUBCONTRACTOR)

# Set markups
estimate.set_standard_markups(overhead=0.15, profit=0.10, contingency=0.05)

# Calculate total
result = estimate.calculate_total()
print(f"Direct Cost: ${result['cost_summary']['direct_cost']:,.2f}")
print(f"Grand Total: ${result['grand_total']:,.2f}")
```

## Common Use Cases

### 1. Cost by Category
```python
summary = estimate.get_cost_summary()
print(f"Labor: ${summary.labor:,.2f}")
print(f"Material: ${summary.material:,.2f}")
```

### 2. Export to Excel
```python
estimate.export_to_excel("estimate_output.xlsx")
```

### 3. Validate Estimate
```python
issues = estimate.validate()
for issue in issues:
    print(f"Warning: {issue}")
```

## Resources
- **DDC Book**: Chapter 3.1 - Cost Calculations and Estimates
- **Website**: https://datadrivenconstruction.io
