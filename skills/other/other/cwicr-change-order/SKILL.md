---
slug: "cwicr-change-order"
display_name: "CWICR Change Order"
description: "Process construction change orders using CWICR data. Calculate cost impact, compare to original estimate, and generate change order documentation."
---

# CWICR Change Order Processor

## Business Case

### Problem Statement
Change orders require:
- Quick cost impact analysis
- Comparison to original scope
- Fair pricing for added work
- Documentation for disputes

### Solution
Systematic change order processing using CWICR data to calculate fair costs, document changes, and analyze impact on project budget.

### Business Value
- **Fair pricing** - Based on validated norms
- **Quick turnaround** - Rapid cost analysis
- **Documentation** - Clear change records
- **Budget tracking** - Cumulative impact

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum


class ChangeType(Enum):
    """Types of changes."""
    ADDITION = "addition"        # New work added
    DELETION = "deletion"        # Work removed
    MODIFICATION = "modification"  # Changed scope
    SUBSTITUTION = "substitution"  # Material/method change


class ChangeStatus(Enum):
    """Change order status."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


@dataclass
class ChangeItem:
    """Single change item."""
    item_number: int
    work_item_code: str
    description: str
    change_type: ChangeType
    original_qty: float
    revised_qty: float
    unit: str
    unit_cost: float
    original_cost: float
    revised_cost: float
    cost_impact: float


@dataclass
class ChangeOrder:
    """Complete change order."""
    co_number: str
    project_name: str
    date_created: date
    status: ChangeStatus
    description: str
    items: List[ChangeItem]
    direct_cost_impact: float
    overhead_markup: float
    profit_markup: float
    total_impact: float
    schedule_impact_days: int
    justification: str


class CWICRChangeOrder:
    """Process change orders using CWICR data."""

    def __init__(self,
                 cwicr_data: pd.DataFrame,
                 overhead_rate: float = 0.12,
                 profit_rate: float = 0.08):
        self.cost_data = cwicr_data
        self.overhead_rate = overhead_rate
        self.profit_rate = profit_rate
        self._index_data()
        self._change_orders: Dict[str, ChangeOrder] = {}

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def get_unit_cost(self, code: str) -> Tuple[float, str]:
        """Get unit cost from CWICR."""
        if self._code_index is None or code not in self._code_index.index:
            return (0, 'unit')

        item = self._code_index.loc[code]
        labor = float(item.get('labor_cost', 0) or 0)
        material = float(item.get('material_cost', 0) or 0)
        equipment = float(item.get('equipment_cost', 0) or 0)
        unit = str(item.get('unit', 'unit'))

        return (labor + material + equipment, unit)

    def create_change_order(self,
                            co_number: str,
                            project_name: str,
                            description: str,
                            justification: str = "") -> str:
        """Create new change order."""

        co = ChangeOrder(
            co_number=co_number,
            project_name=project_name,
            date_created=date.today(),
            status=ChangeStatus.DRAFT,
            description=description,
            items=[],
            direct_cost_impact=0,
            overhead_markup=0,
            profit_markup=0,
            total_impact=0,
            schedule_impact_days=0,
            justification=justification
        )

        self._change_orders[co_number] = co
        return co_number

    def add_change_item(self,
                        co_number: str,
                        work_item_code: str,
                        change_type: ChangeType,
                        original_qty: float,
                        revised_qty: float,
                        description: str = None) -> ChangeItem:
        """Add item to change order."""

        co = self._change_orders.get(co_number)
        if co is None:
            raise ValueError(f"Change order {co_number} not found")

        unit_cost, unit = self.get_unit_cost(work_item_code)

        if description is None:
            if self._code_index is not None and work_item_code in self._code_index.index:
                description = str(self._code_index.loc[work_item_code].get('description', work_item_code))
            else:
                description = work_item_code

        original_cost = original_qty * unit_cost
        revised_cost = revised_qty * unit_cost
        cost_impact = revised_cost - original_cost

        item = ChangeItem(
            item_number=len(co.items) + 1,
            work_item_code=work_item_code,
            description=description,
            change_type=change_type,
            original_qty=original_qty,
            revised_qty=revised_qty,
            unit=unit,
            unit_cost=unit_cost,
            original_cost=round(original_cost, 2),
            revised_cost=round(revised_cost, 2),
            cost_impact=round(cost_impact, 2)
        )

        co.items.append(item)
        self._recalculate_totals(co_number)

        return item

    def _recalculate_totals(self, co_number: str):
        """Recalculate change order totals."""
        co = self._change_orders.get(co_number)
        if co is None:
            return

        direct_impact = sum(item.cost_impact for item in co.items)
        overhead = direct_impact * self.overhead_rate
        profit = (direct_impact + overhead) * self.profit_rate

        co.direct_cost_impact = round(direct_impact, 2)
        co.overhead_markup = round(overhead, 2)
        co.profit_markup = round(profit, 2)
        co.total_impact = round(direct_impact + overhead + profit, 2)

    def set_schedule_impact(self, co_number: str, days: int):
        """Set schedule impact for change order."""
        co = self._change_orders.get(co_number)
        if co:
            co.schedule_impact_days = days

    def update_status(self, co_number: str, status: ChangeStatus):
        """Update change order status."""
        co = self._change_orders.get(co_number)
        if co:
            co.status = status

    def get_change_order(self, co_number: str) -> Optional[ChangeOrder]:
        """Get change order by number."""
        return self._change_orders.get(co_number)

    def calculate_quick_impact(self,
                                changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Quick impact calculation without creating CO."""

        additions = 0
        deletions = 0
        modifications = 0

        for change in changes:
            code = change.get('work_item_code', change.get('code'))
            change_type = change.get('change_type', 'modification')
            original = change.get('original_qty', 0)
            revised = change.get('revised_qty', 0)

            unit_cost, _ = self.get_unit_cost(code)

            if change_type == 'addition':
                additions += revised * unit_cost
            elif change_type == 'deletion':
                deletions += original * unit_cost
            else:
                modifications += (revised - original) * unit_cost

        net_direct = additions - deletions + modifications
        overhead = net_direct * self.overhead_rate
        profit = (net_direct + overhead) * self.profit_rate

        return {
            'additions': round(additions, 2),
            'deletions': round(deletions, 2),
            'modifications': round(modifications, 2),
            'net_direct_impact': round(net_direct, 2),
            'overhead': round(overhead, 2),
            'profit': round(profit, 2),
            'total_impact': round(net_direct + overhead + profit, 2)
        }

    def compare_to_budget(self,
                          co_number: str,
                          original_budget: float,
                          approved_changes: float = 0) -> Dict[str, Any]:
        """Compare change order to project budget."""

        co = self._change_orders.get(co_number)
        if co is None:
            return {}

        current_budget = original_budget + approved_changes
        new_budget = current_budget + co.total_impact

        return {
            'original_budget': original_budget,
            'previously_approved_changes': approved_changes,
            'current_budget': current_budget,
            'this_change_order': co.total_impact,
            'new_budget': round(new_budget, 2),
            'change_from_original': round(new_budget - original_budget, 2),
            'change_percent': round((new_budget - original_budget) / original_budget * 100, 1)
        }

    def get_project_changes_summary(self,
                                     project_name: str) -> Dict[str, Any]:
        """Get summary of all changes for a project."""

        project_cos = [
            co for co in self._change_orders.values()
            if co.project_name == project_name
        ]

        total_additions = 0
        total_deletions = 0
        total_impact = 0
        total_schedule_impact = 0

        for co in project_cos:
            for item in co.items:
                if item.change_type == ChangeType.ADDITION:
                    total_additions += item.cost_impact
                elif item.change_type == ChangeType.DELETION:
                    total_deletions += abs(item.cost_impact)

            total_impact += co.total_impact
            total_schedule_impact += co.schedule_impact_days

        return {
            'project': project_name,
            'total_change_orders': len(project_cos),
            'approved': len([co for co in project_cos if co.status == ChangeStatus.APPROVED]),
            'pending': len([co for co in project_cos if co.status == ChangeStatus.PENDING]),
            'total_additions': round(total_additions, 2),
            'total_deletions': round(total_deletions, 2),
            'net_cost_impact': round(total_impact, 2),
            'total_schedule_days': total_schedule_impact
        }

    def export_change_order(self,
                             co_number: str,
                             output_path: str) -> str:
        """Export change order to Excel."""

        co = self._change_orders.get(co_number)
        if co is None:
            raise ValueError(f"Change order {co_number} not found")

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Header
            header_df = pd.DataFrame([{
                'Change Order': co.co_number,
                'Project': co.project_name,
                'Date': co.date_created,
                'Status': co.status.value,
                'Description': co.description,
                'Schedule Impact (days)': co.schedule_impact_days
            }])
            header_df.to_excel(writer, sheet_name='Summary', index=False)

            # Items
            items_df = pd.DataFrame([
                {
                    '#': item.item_number,
                    'Code': item.work_item_code,
                    'Description': item.description,
                    'Type': item.change_type.value,
                    'Original Qty': item.original_qty,
                    'Revised Qty': item.revised_qty,
                    'Unit': item.unit,
                    'Unit Cost': item.unit_cost,
                    'Original Cost': item.original_cost,
                    'Revised Cost': item.revised_cost,
                    'Impact': item.cost_impact
                }
                for item in co.items
            ])
            items_df.to_excel(writer, sheet_name='Items', index=False)

            # Totals
            totals_df = pd.DataFrame([{
                'Direct Cost Impact': co.direct_cost_impact,
                f'Overhead ({self.overhead_rate:.0%})': co.overhead_markup,
                f'Profit ({self.profit_rate:.0%})': co.profit_markup,
                'Total Impact': co.total_impact
            }])
            totals_df.to_excel(writer, sheet_name='Totals', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize change order processor
co_processor = CWICRChangeOrder(cwicr, overhead_rate=0.12, profit_rate=0.08)

# Create change order
co_processor.create_change_order(
    co_number="CO-001",
    project_name="Building A",
    description="Additional foundation work due to soil conditions"
)

# Add items
co_processor.add_change_item(
    co_number="CO-001",
    work_item_code="EXCV-002",
    change_type=ChangeType.ADDITION,
    original_qty=0,
    revised_qty=150
)

# Get change order
co = co_processor.get_change_order("CO-001")
print(f"Direct Impact: ${co.direct_cost_impact:,.2f}")
print(f"Total Impact: ${co.total_impact:,.2f}")
```

## Common Use Cases

### 1. Quick Impact Analysis
```python
changes = [
    {'code': 'CONC-001', 'change_type': 'addition', 'original_qty': 0, 'revised_qty': 50},
    {'code': 'REBAR-002', 'change_type': 'modification', 'original_qty': 1000, 'revised_qty': 1500}
]

impact = co_processor.calculate_quick_impact(changes)
print(f"Net Impact: ${impact['total_impact']:,.2f}")
```

### 2. Compare to Budget
```python
comparison = co_processor.compare_to_budget(
    co_number="CO-001",
    original_budget=5000000,
    approved_changes=150000
)
print(f"Budget Change: {comparison['change_percent']}%")
```

### 3. Export Documentation
```python
co_processor.export_change_order("CO-001", "change_order_001.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.2 - Change Order Management
