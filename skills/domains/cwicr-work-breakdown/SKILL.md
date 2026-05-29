---
name: cwicr-work-breakdown
description: "Break down CWICR work items into component resources. Decompose aggregate items, analyze resource composition, and generate detailed bills of resources."
---

# CWICR Work Breakdown

## Business Case

### Problem Statement
Work items in CWICR contain aggregated resources:
- What materials make up a concrete work item?
- What labor categories are needed?
- What equipment is involved?
- How to generate detailed resource bills?

### Solution
Decompose CWICR work items into their constituent resources (labor, materials, equipment) with quantities and costs.

### Business Value
- **Transparency** - See inside aggregated items
- **Procurement** - Generate material lists
- **Scheduling** - Identify resource needs
- **Cost control** - Track resource consumption

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict


class ResourceType(Enum):
    """Types of resources in work items."""
    LABOR = "labor"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    OVERHEAD = "overhead"


@dataclass
class ResourceComponent:
    """Single resource component of a work item."""
    resource_code: str
    resource_type: ResourceType
    description: str
    unit: str
    quantity_per_unit: float  # Per unit of work item
    unit_rate: float
    cost_per_unit: float  # Per unit of work item


@dataclass
class WorkItemBreakdown:
    """Complete breakdown of a work item."""
    work_item_code: str
    work_item_description: str
    work_item_unit: str
    components: List[ResourceComponent]
    labor_cost_per_unit: float
    material_cost_per_unit: float
    equipment_cost_per_unit: float
    total_cost_per_unit: float


@dataclass
class BillOfResources:
    """Bill of resources for multiple work items."""
    project_name: str
    total_labor_cost: float
    total_material_cost: float
    total_equipment_cost: float
    total_cost: float
    labor_resources: List[Dict[str, Any]]
    material_resources: List[Dict[str, Any]]
    equipment_resources: List[Dict[str, Any]]


class CWICRWorkBreakdown:
    """Break down work items into resources."""

    def __init__(self, cwicr_data: pd.DataFrame,
                 resources_data: pd.DataFrame = None):
        self.work_items = cwicr_data
        self.resources = resources_data
        self._index_data()

    def _index_data(self):
        """Index data for fast lookup."""
        if 'work_item_code' in self.work_items.columns:
            self._work_index = self.work_items.set_index('work_item_code')
        else:
            self._work_index = None

        if self.resources is not None and 'resource_code' in self.resources.columns:
            self._resource_index = self.resources.set_index('resource_code')
        else:
            self._resource_index = None

    def breakdown_work_item(self, work_item_code: str) -> Optional[WorkItemBreakdown]:
        """Break down single work item into components."""

        if self._work_index is None or work_item_code not in self._work_index.index:
            return None

        item = self._work_index.loc[work_item_code]
        components = []

        # Extract labor component
        labor_norm = float(item.get('labor_norm', 0) or 0)
        labor_rate = float(item.get('labor_rate', 35) or 35)
        labor_cost = float(item.get('labor_cost', labor_norm * labor_rate) or labor_norm * labor_rate)

        if labor_norm > 0:
            components.append(ResourceComponent(
                resource_code=f"{work_item_code}-LABOR",
                resource_type=ResourceType.LABOR,
                description=f"Labor for {item.get('description', '')}",
                unit="hr",
                quantity_per_unit=labor_norm,
                unit_rate=labor_rate,
                cost_per_unit=labor_cost
            ))

        # Extract material component
        material_norm = float(item.get('material_norm', 1) or 1)
        material_cost = float(item.get('material_cost', 0) or 0)

        if material_cost > 0:
            components.append(ResourceComponent(
                resource_code=f"{work_item_code}-MAT",
                resource_type=ResourceType.MATERIAL,
                description=str(item.get('material_description', 'Materials')),
                unit=str(item.get('material_unit', item.get('unit', 'ea'))),
                quantity_per_unit=material_norm,
                unit_rate=material_cost / material_norm if material_norm > 0 else material_cost,
                cost_per_unit=material_cost
            ))

        # Extract equipment component
        equipment_norm = float(item.get('equipment_norm', 0) or 0)
        equipment_rate = float(item.get('equipment_rate', 0) or 0)
        equipment_cost = float(item.get('equipment_cost', equipment_norm * equipment_rate) or 0)

        if equipment_norm > 0 or equipment_cost > 0:
            components.append(ResourceComponent(
                resource_code=f"{work_item_code}-EQUIP",
                resource_type=ResourceType.EQUIPMENT,
                description=str(item.get('equipment_description', 'Equipment')),
                unit="hr",
                quantity_per_unit=equipment_norm,
                unit_rate=equipment_rate,
                cost_per_unit=equipment_cost
            ))

        return WorkItemBreakdown(
            work_item_code=work_item_code,
            work_item_description=str(item.get('description', '')),
            work_item_unit=str(item.get('unit', '')),
            components=components,
            labor_cost_per_unit=labor_cost,
            material_cost_per_unit=material_cost,
            equipment_cost_per_unit=equipment_cost,
            total_cost_per_unit=labor_cost + material_cost + equipment_cost
        )

    def generate_bill_of_resources(self,
                                    items: List[Dict[str, Any]],
                                    project_name: str = "Project") -> BillOfResources:
        """Generate bill of resources from work items."""

        labor_agg = defaultdict(lambda: {'hours': 0, 'cost': 0, 'work_items': []})
        material_agg = defaultdict(lambda: {'quantity': 0, 'cost': 0, 'unit': '', 'work_items': []})
        equipment_agg = defaultdict(lambda: {'hours': 0, 'cost': 0, 'work_items': []})

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            breakdown = self.breakdown_work_item(code)
            if not breakdown:
                continue

            for component in breakdown.components:
                scaled_qty = component.quantity_per_unit * qty
                scaled_cost = component.cost_per_unit * qty

                if component.resource_type == ResourceType.LABOR:
                    key = 'General Labor'  # Could be more specific with skill data
                    labor_agg[key]['hours'] += scaled_qty
                    labor_agg[key]['cost'] += scaled_cost
                    labor_agg[key]['work_items'].append(code)

                elif component.resource_type == ResourceType.MATERIAL:
                    key = component.description
                    material_agg[key]['quantity'] += scaled_qty
                    material_agg[key]['cost'] += scaled_cost
                    material_agg[key]['unit'] = component.unit
                    material_agg[key]['work_items'].append(code)

                elif component.resource_type == ResourceType.EQUIPMENT:
                    key = component.description
                    equipment_agg[key]['hours'] += scaled_qty
                    equipment_agg[key]['cost'] += scaled_cost
                    equipment_agg[key]['work_items'].append(code)

        # Convert to lists
        labor_resources = [
            {
                'resource': name,
                'hours': round(data['hours'], 1),
                'cost': round(data['cost'], 2),
                'work_items': len(set(data['work_items']))
            }
            for name, data in labor_agg.items()
        ]

        material_resources = [
            {
                'resource': name,
                'quantity': round(data['quantity'], 2),
                'unit': data['unit'],
                'cost': round(data['cost'], 2),
                'work_items': len(set(data['work_items']))
            }
            for name, data in material_agg.items()
        ]

        equipment_resources = [
            {
                'resource': name,
                'hours': round(data['hours'], 1),
                'cost': round(data['cost'], 2),
                'work_items': len(set(data['work_items']))
            }
            for name, data in equipment_agg.items()
        ]

        total_labor = sum(r['cost'] for r in labor_resources)
        total_material = sum(r['cost'] for r in material_resources)
        total_equipment = sum(r['cost'] for r in equipment_resources)

        return BillOfResources(
            project_name=project_name,
            total_labor_cost=round(total_labor, 2),
            total_material_cost=round(total_material, 2),
            total_equipment_cost=round(total_equipment, 2),
            total_cost=round(total_labor + total_material + total_equipment, 2),
            labor_resources=labor_resources,
            material_resources=material_resources,
            equipment_resources=equipment_resources
        )

    def get_resource_composition(self, work_item_code: str) -> Dict[str, float]:
        """Get percentage composition of work item by resource type."""

        breakdown = self.breakdown_work_item(work_item_code)
        if not breakdown or breakdown.total_cost_per_unit == 0:
            return {'labor': 0, 'material': 0, 'equipment': 0}

        total = breakdown.total_cost_per_unit
        return {
            'labor': round(breakdown.labor_cost_per_unit / total * 100, 1),
            'material': round(breakdown.material_cost_per_unit / total * 100, 1),
            'equipment': round(breakdown.equipment_cost_per_unit / total * 100, 1)
        }

    def analyze_labor_intensity(self,
                                 work_items: List[str]) -> pd.DataFrame:
        """Analyze labor intensity of work items."""

        data = []
        for code in work_items:
            breakdown = self.breakdown_work_item(code)
            if breakdown:
                composition = self.get_resource_composition(code)
                labor_components = [c for c in breakdown.components if c.resource_type == ResourceType.LABOR]
                labor_hours = sum(c.quantity_per_unit for c in labor_components)

                data.append({
                    'work_item_code': code,
                    'description': breakdown.work_item_description,
                    'labor_hours_per_unit': labor_hours,
                    'labor_cost_pct': composition['labor'],
                    'material_cost_pct': composition['material'],
                    'equipment_cost_pct': composition['equipment'],
                    'labor_intensive': composition['labor'] > 50
                })

        return pd.DataFrame(data).sort_values('labor_cost_pct', ascending=False)

    def export_breakdown(self,
                         breakdown: WorkItemBreakdown,
                         output_path: str) -> str:
        """Export single work item breakdown."""

        df = pd.DataFrame([
            {
                'Resource Code': c.resource_code,
                'Type': c.resource_type.value,
                'Description': c.description,
                'Unit': c.unit,
                'Quantity/Unit': c.quantity_per_unit,
                'Rate': c.unit_rate,
                'Cost/Unit': c.cost_per_unit
            }
            for c in breakdown.components
        ])

        df.to_excel(output_path, index=False)
        return output_path

    def export_bill_of_resources(self,
                                  bill: BillOfResources,
                                  output_path: str) -> str:
        """Export bill of resources to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Project': bill.project_name,
                'Total Labor Cost': bill.total_labor_cost,
                'Total Material Cost': bill.total_material_cost,
                'Total Equipment Cost': bill.total_equipment_cost,
                'Grand Total': bill.total_cost
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Labor
            labor_df = pd.DataFrame(bill.labor_resources)
            labor_df.to_excel(writer, sheet_name='Labor', index=False)

            # Materials
            material_df = pd.DataFrame(bill.material_resources)
            material_df.to_excel(writer, sheet_name='Materials', index=False)

            # Equipment
            equipment_df = pd.DataFrame(bill.equipment_resources)
            equipment_df.to_excel(writer, sheet_name='Equipment', index=False)

        return output_path


class ResourceAggregator:
    """Aggregate resources across work items."""

    def __init__(self, breakdown_tool: CWICRWorkBreakdown):
        self.breakdown = breakdown_tool

    def aggregate_by_trade(self,
                           items: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Aggregate resources by trade/category."""

        by_trade = defaultdict(lambda: {'labor_hours': 0, 'labor_cost': 0, 'items': 0})

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            # Extract trade from code prefix
            trade = code.split('-')[0] if '-' in code else 'General'

            breakdown = self.breakdown.breakdown_work_item(code)
            if breakdown:
                by_trade[trade]['labor_hours'] += breakdown.labor_cost_per_unit / 35 * qty  # Estimate hours
                by_trade[trade]['labor_cost'] += breakdown.labor_cost_per_unit * qty
                by_trade[trade]['items'] += 1

        return dict(by_trade)

    def identify_critical_resources(self,
                                     bill: BillOfResources,
                                     threshold_pct: float = 10) -> Dict[str, List[Dict]]:
        """Identify resources that contribute significantly to cost."""

        critical = {
            'labor': [],
            'material': [],
            'equipment': []
        }

        # Labor
        for r in bill.labor_resources:
            if bill.total_labor_cost > 0:
                pct = r['cost'] / bill.total_labor_cost * 100
                if pct >= threshold_pct:
                    critical['labor'].append({**r, 'percentage': round(pct, 1)})

        # Materials
        for r in bill.material_resources:
            if bill.total_material_cost > 0:
                pct = r['cost'] / bill.total_material_cost * 100
                if pct >= threshold_pct:
                    critical['material'].append({**r, 'percentage': round(pct, 1)})

        # Equipment
        for r in bill.equipment_resources:
            if bill.total_equipment_cost > 0:
                pct = r['cost'] / bill.total_equipment_cost * 100
                if pct >= threshold_pct:
                    critical['equipment'].append({**r, 'percentage': round(pct, 1)})

        return critical
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize breakdown tool
breakdown = CWICRWorkBreakdown(cwicr)

# Break down single item
item_breakdown = breakdown.breakdown_work_item("CONC-001")

print(f"Work Item: {item_breakdown.work_item_description}")
print(f"Labor: ${item_breakdown.labor_cost_per_unit}")
print(f"Material: ${item_breakdown.material_cost_per_unit}")
print(f"Equipment: ${item_breakdown.equipment_cost_per_unit}")

for comp in item_breakdown.components:
    print(f"  - {comp.resource_type.value}: {comp.description}")
```

## Common Use Cases

### 1. Bill of Resources
```python
items = [
    {'work_item_code': 'CONC-001', 'quantity': 150},
    {'work_item_code': 'REBAR-002', 'quantity': 5000},
    {'work_item_code': 'FORM-003', 'quantity': 300}
]

bill = breakdown.generate_bill_of_resources(items, "Building A")
print(f"Total Labor: ${bill.total_labor_cost:,.2f}")
print(f"Total Material: ${bill.total_material_cost:,.2f}")
```

### 2. Resource Composition
```python
composition = breakdown.get_resource_composition("CONC-001")
print(f"Labor: {composition['labor']}%")
print(f"Material: {composition['material']}%")
```

### 3. Labor Intensity Analysis
```python
analysis = breakdown.analyze_labor_intensity(['CONC-001', 'EXCV-002', 'REBAR-003'])
print(analysis)
```

### 4. Export Report
```python
breakdown.export_bill_of_resources(bill, "bill_of_resources.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Resource-Based Estimating
