---
name: "cwicr-assembly-builder"
description: "Build cost assemblies from CWICR work items. Combine multiple items into reusable templates for common construction elements."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Assembly Builder

## Business Case

### Problem Statement
Estimating repetitive elements requires:
- Consistent item groupings
- Reusable templates
- Standard assemblies
- Quick application

### Solution
Build and manage assemblies of CWICR work items that can be applied as templates to speed up estimating and ensure completeness.

### Business Value
- **Speed** - Apply complete assemblies quickly
- **Consistency** - Standard item groupings
- **Completeness** - No missed items
- **Reusability** - Template library

## Technical Implementation

```python
import pandas as pd
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class AssemblyType(Enum):
    """Types of assemblies."""
    STRUCTURAL = "structural"
    ARCHITECTURAL = "architectural"
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    SITEWORK = "sitework"
    GENERAL = "general"


@dataclass
class AssemblyItem:
    """Single item in assembly."""
    work_item_code: str
    description: str
    quantity_per_unit: float  # Quantity per assembly unit
    unit: str
    unit_cost: float
    total_cost: float
    notes: str = ""


@dataclass
class Assembly:
    """Complete assembly definition."""
    assembly_code: str
    name: str
    description: str
    assembly_type: AssemblyType
    unit: str  # Assembly unit (e.g., "m2", "each", "LF")
    items: List[AssemblyItem]
    total_cost_per_unit: float
    labor_hours_per_unit: float
    created_date: datetime
    version: int = 1


class CWICRAssemblyBuilder:
    """Build and manage assemblies from CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame):
        self.cwicr = cwicr_data
        self._index_cwicr()
        self._assemblies: Dict[str, Assembly] = {}

    def _index_cwicr(self):
        """Index CWICR data."""
        if 'work_item_code' in self.cwicr.columns:
            self._cwicr_index = self.cwicr.set_index('work_item_code')
        else:
            self._cwicr_index = None

    def _get_item_cost(self, code: str) -> Tuple[float, float, str]:
        """Get item unit cost and labor hours."""
        if self._cwicr_index is None or code not in self._cwicr_index.index:
            return (0, 0, 'unit')

        item = self._cwicr_index.loc[code]
        labor = float(item.get('labor_cost', 0) or 0)
        material = float(item.get('material_cost', 0) or 0)
        equipment = float(item.get('equipment_cost', 0) or 0)
        labor_hours = float(item.get('labor_norm', item.get('labor_hours', 0)) or 0)
        unit = str(item.get('unit', 'unit'))

        return (labor + material + equipment, labor_hours, unit)

    def create_assembly(self,
                        assembly_code: str,
                        name: str,
                        description: str,
                        assembly_type: AssemblyType,
                        unit: str,
                        items: List[Dict[str, Any]]) -> Assembly:
        """Create new assembly from work items."""

        assembly_items = []
        total_cost = 0
        total_hours = 0

        for item_def in items:
            code = item_def.get('work_item_code', item_def.get('code'))
            qty_per_unit = item_def.get('quantity_per_unit', 1)
            notes = item_def.get('notes', '')

            unit_cost, labor_hours, item_unit = self._get_item_cost(code)

            # Get description from CWICR
            if self._cwicr_index is not None and code in self._cwicr_index.index:
                desc = str(self._cwicr_index.loc[code].get('description', code))
            else:
                desc = item_def.get('description', code)

            item_total = unit_cost * qty_per_unit

            assembly_items.append(AssemblyItem(
                work_item_code=code,
                description=desc,
                quantity_per_unit=qty_per_unit,
                unit=item_unit,
                unit_cost=round(unit_cost, 2),
                total_cost=round(item_total, 2),
                notes=notes
            ))

            total_cost += item_total
            total_hours += labor_hours * qty_per_unit

        assembly = Assembly(
            assembly_code=assembly_code,
            name=name,
            description=description,
            assembly_type=assembly_type,
            unit=unit,
            items=assembly_items,
            total_cost_per_unit=round(total_cost, 2),
            labor_hours_per_unit=round(total_hours, 2),
            created_date=datetime.now(),
            version=1
        )

        self._assemblies[assembly_code] = assembly
        return assembly

    def apply_assembly(self,
                        assembly_code: str,
                        quantity: float,
                        location_factor: float = 1.0) -> Dict[str, Any]:
        """Apply assembly to get estimate."""

        assembly = self._assemblies.get(assembly_code)
        if assembly is None:
            return {'error': f"Assembly {assembly_code} not found"}

        items = []
        total_cost = 0
        total_hours = 0

        for item in assembly.items:
            qty = item.quantity_per_unit * quantity
            cost = item.total_cost * quantity * location_factor
            hours = qty * (item.unit_cost / 50 if item.unit_cost > 0 else 0)  # Approximate labor hours

            items.append({
                'work_item_code': item.work_item_code,
                'description': item.description,
                'quantity': round(qty, 2),
                'unit': item.unit,
                'cost': round(cost, 2)
            })

            total_cost += cost
            total_hours += hours

        return {
            'assembly_code': assembly_code,
            'assembly_name': assembly.name,
            'quantity': quantity,
            'unit': assembly.unit,
            'location_factor': location_factor,
            'items': items,
            'total_cost': round(total_cost, 2),
            'total_labor_hours': round(total_hours, 2),
            'cost_per_unit': round(total_cost / quantity, 2) if quantity > 0 else 0
        }

    def get_assembly(self, assembly_code: str) -> Optional[Assembly]:
        """Get assembly by code."""
        return self._assemblies.get(assembly_code)

    def list_assemblies(self, assembly_type: AssemblyType = None) -> List[Dict[str, Any]]:
        """List all assemblies."""

        assemblies = self._assemblies.values()

        if assembly_type:
            assemblies = [a for a in assemblies if a.assembly_type == assembly_type]

        return [
            {
                'code': a.assembly_code,
                'name': a.name,
                'type': a.assembly_type.value,
                'unit': a.unit,
                'cost_per_unit': a.total_cost_per_unit,
                'item_count': len(a.items)
            }
            for a in assemblies
        ]

    def clone_assembly(self,
                        source_code: str,
                        new_code: str,
                        new_name: str = None) -> Optional[Assembly]:
        """Clone existing assembly."""

        source = self._assemblies.get(source_code)
        if source is None:
            return None

        new_assembly = Assembly(
            assembly_code=new_code,
            name=new_name or f"{source.name} (Copy)",
            description=source.description,
            assembly_type=source.assembly_type,
            unit=source.unit,
            items=source.items.copy(),
            total_cost_per_unit=source.total_cost_per_unit,
            labor_hours_per_unit=source.labor_hours_per_unit,
            created_date=datetime.now(),
            version=1
        )

        self._assemblies[new_code] = new_assembly
        return new_assembly

    def compare_assemblies(self,
                            codes: List[str],
                            quantity: float = 1) -> pd.DataFrame:
        """Compare multiple assemblies."""

        data = []

        for code in codes:
            assembly = self._assemblies.get(code)
            if assembly:
                result = self.apply_assembly(code, quantity)
                data.append({
                    'Assembly': assembly.name,
                    'Code': code,
                    'Unit': assembly.unit,
                    'Cost/Unit': assembly.total_cost_per_unit,
                    'Hours/Unit': assembly.labor_hours_per_unit,
                    f'Total ({quantity} {assembly.unit})': result['total_cost'],
                    'Items': len(assembly.items)
                })

        return pd.DataFrame(data)

    def create_standard_assemblies(self):
        """Create standard construction assemblies."""

        # Concrete slab assembly
        self.create_assembly(
            assembly_code="SLAB-100",
            name="Concrete Slab 100mm",
            description="Standard 100mm concrete slab on grade",
            assembly_type=AssemblyType.STRUCTURAL,
            unit="m2",
            items=[
                {'code': 'PREP-001', 'quantity_per_unit': 1.0, 'notes': 'Subgrade preparation'},
                {'code': 'GRAVEL-001', 'quantity_per_unit': 0.15, 'notes': '150mm gravel base'},
                {'code': 'VAPOR-001', 'quantity_per_unit': 1.1, 'notes': 'Vapor barrier'},
                {'code': 'MESH-001', 'quantity_per_unit': 1.1, 'notes': 'Welded wire mesh'},
                {'code': 'CONC-001', 'quantity_per_unit': 0.1, 'notes': '100mm concrete'},
                {'code': 'FINISH-001', 'quantity_per_unit': 1.0, 'notes': 'Power trowel finish'}
            ]
        )

        # Stud wall assembly
        self.create_assembly(
            assembly_code="WALL-STUD",
            name="Metal Stud Wall",
            description="Metal stud wall with drywall both sides",
            assembly_type=AssemblyType.ARCHITECTURAL,
            unit="m2",
            items=[
                {'code': 'TRACK-001', 'quantity_per_unit': 0.8, 'notes': 'Floor/ceiling track'},
                {'code': 'STUD-001', 'quantity_per_unit': 2.5, 'notes': 'Studs @ 400mm OC'},
                {'code': 'INSUL-001', 'quantity_per_unit': 1.0, 'notes': 'Batt insulation'},
                {'code': 'GYP-001', 'quantity_per_unit': 2.2, 'notes': 'Drywall both sides'},
                {'code': 'TAPE-001', 'quantity_per_unit': 2.0, 'notes': 'Tape and mud'}
            ]
        )

    def export_assemblies(self, output_path: str) -> str:
        """Export assemblies to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([
                {
                    'Code': a.assembly_code,
                    'Name': a.name,
                    'Type': a.assembly_type.value,
                    'Unit': a.unit,
                    'Cost/Unit': a.total_cost_per_unit,
                    'Hours/Unit': a.labor_hours_per_unit,
                    'Items': len(a.items),
                    'Version': a.version
                }
                for a in self._assemblies.values()
            ])
            summary_df.to_excel(writer, sheet_name='Assemblies', index=False)

            # Details for each assembly
            for code, assembly in self._assemblies.items():
                if len(code) > 25:
                    sheet_name = code[:25]
                else:
                    sheet_name = code

                detail_df = pd.DataFrame([
                    {
                        'Work Item': item.work_item_code,
                        'Description': item.description,
                        'Qty/Unit': item.quantity_per_unit,
                        'Item Unit': item.unit,
                        'Unit Cost': item.unit_cost,
                        'Total Cost': item.total_cost,
                        'Notes': item.notes
                    }
                    for item in assembly.items
                ])
                detail_df.to_excel(writer, sheet_name=sheet_name, index=False)

        return output_path

    def save_library(self, filepath: str):
        """Save assembly library to JSON."""
        data = {}

        for code, assembly in self._assemblies.items():
            data[code] = {
                'assembly_code': assembly.assembly_code,
                'name': assembly.name,
                'description': assembly.description,
                'assembly_type': assembly.assembly_type.value,
                'unit': assembly.unit,
                'items': [
                    {
                        'work_item_code': item.work_item_code,
                        'description': item.description,
                        'quantity_per_unit': item.quantity_per_unit,
                        'unit': item.unit,
                        'notes': item.notes
                    }
                    for item in assembly.items
                ],
                'version': assembly.version
            }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize builder
builder = CWICRAssemblyBuilder(cwicr)

# Create assembly
builder.create_assembly(
    assembly_code="FDN-STRIP",
    name="Strip Foundation",
    description="Standard strip foundation 600x300",
    assembly_type=AssemblyType.STRUCTURAL,
    unit="LM",
    items=[
        {'code': 'EXCV-001', 'quantity_per_unit': 0.5},
        {'code': 'CONC-001', 'quantity_per_unit': 0.18},
        {'code': 'REBAR-001', 'quantity_per_unit': 15}
    ]
)

# Apply assembly
result = builder.apply_assembly("FDN-STRIP", quantity=50)
print(f"Total Cost: ${result['total_cost']:,.2f}")
```

## Common Use Cases

### 1. Standard Assemblies
```python
builder.create_standard_assemblies()
assemblies = builder.list_assemblies()
for a in assemblies:
    print(f"{a['code']}: ${a['cost_per_unit']:.2f}/{a['unit']}")
```

### 2. Compare Options
```python
comparison = builder.compare_assemblies(
    ["WALL-STUD", "WALL-BLOCK"],
    quantity=100
)
print(comparison)
```

### 3. Clone and Modify
```python
builder.clone_assembly("SLAB-100", "SLAB-150", "Concrete Slab 150mm")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Assembly-Based Estimating
