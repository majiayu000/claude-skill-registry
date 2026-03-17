---
name: "cwicr-waste-calculator"
description: "Calculate material waste factors and losses using CWICR norms. Apply waste percentages, cutting losses, and spillage factors to material quantities."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Waste Calculator

## Business Case

### Problem Statement
Material estimates need waste factors:
- Cutting/trimming losses
- Spillage and breakage
- Overordering requirements
- Different waste by material type

### Solution
Systematic waste calculation using CWICR material data with industry-standard waste factors by material category.

### Business Value
- **Accurate ordering** - Include realistic waste
- **Cost control** - Budget for actual usage
- **Sustainability** - Track and reduce waste
- **Benchmarking** - Compare waste across projects

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class WasteCategory(Enum):
    """Waste category types."""
    CUTTING = "cutting"          # Cutting/trimming losses
    SPILLAGE = "spillage"        # Liquid material spillage
    BREAKAGE = "breakage"        # Damaged materials
    OVERRUN = "overrun"          # Installation overrun
    THEFT = "theft"              # Site theft allowance
    WEATHER = "weather"          # Weather damage


@dataclass
class WasteFactor:
    """Waste factor for a material."""
    material_code: str
    material_name: str
    base_quantity: float
    unit: str
    cutting_waste_pct: float
    spillage_pct: float
    breakage_pct: float
    overrun_pct: float
    total_waste_pct: float
    quantity_with_waste: float
    waste_quantity: float
    waste_cost: float


# Industry standard waste factors by material type
WASTE_FACTORS = {
    'concrete': {
        'cutting': 0.02, 'spillage': 0.03, 'breakage': 0.0, 'overrun': 0.02
    },
    'rebar': {
        'cutting': 0.05, 'spillage': 0.0, 'breakage': 0.01, 'overrun': 0.02
    },
    'brick': {
        'cutting': 0.05, 'spillage': 0.0, 'breakage': 0.03, 'overrun': 0.02
    },
    'block': {
        'cutting': 0.04, 'spillage': 0.0, 'breakage': 0.02, 'overrun': 0.02
    },
    'lumber': {
        'cutting': 0.10, 'spillage': 0.0, 'breakage': 0.02, 'overrun': 0.03
    },
    'plywood': {
        'cutting': 0.12, 'spillage': 0.0, 'breakage': 0.02, 'overrun': 0.02
    },
    'drywall': {
        'cutting': 0.10, 'spillage': 0.0, 'breakage': 0.03, 'overrun': 0.02
    },
    'tile': {
        'cutting': 0.10, 'spillage': 0.0, 'breakage': 0.05, 'overrun': 0.03
    },
    'paint': {
        'cutting': 0.0, 'spillage': 0.05, 'breakage': 0.0, 'overrun': 0.10
    },
    'mortar': {
        'cutting': 0.0, 'spillage': 0.05, 'breakage': 0.0, 'overrun': 0.03
    },
    'insulation': {
        'cutting': 0.08, 'spillage': 0.0, 'breakage': 0.02, 'overrun': 0.03
    },
    'roofing': {
        'cutting': 0.10, 'spillage': 0.0, 'breakage': 0.02, 'overrun': 0.05
    },
    'pipe': {
        'cutting': 0.05, 'spillage': 0.0, 'breakage': 0.01, 'overrun': 0.02
    },
    'wire': {
        'cutting': 0.03, 'spillage': 0.0, 'breakage': 0.0, 'overrun': 0.05
    },
    'conduit': {
        'cutting': 0.05, 'spillage': 0.0, 'breakage': 0.01, 'overrun': 0.02
    },
    'duct': {
        'cutting': 0.08, 'spillage': 0.0, 'breakage': 0.01, 'overrun': 0.03
    },
    'steel': {
        'cutting': 0.03, 'spillage': 0.0, 'breakage': 0.0, 'overrun': 0.02
    },
    'glass': {
        'cutting': 0.05, 'spillage': 0.0, 'breakage': 0.05, 'overrun': 0.02
    },
    'flooring': {
        'cutting': 0.10, 'spillage': 0.0, 'breakage': 0.02, 'overrun': 0.03
    },
    'adhesive': {
        'cutting': 0.0, 'spillage': 0.08, 'breakage': 0.0, 'overrun': 0.05
    },
    'default': {
        'cutting': 0.05, 'spillage': 0.02, 'breakage': 0.02, 'overrun': 0.03
    }
}


class CWICRWasteCalculator:
    """Calculate material waste using CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame):
        self.materials = cwicr_data
        self._index_data()

    def _index_data(self):
        """Index materials data."""
        if 'material_code' in self.materials.columns:
            self._mat_index = self.materials.set_index('material_code')
        elif 'work_item_code' in self.materials.columns:
            self._mat_index = self.materials.set_index('work_item_code')
        else:
            self._mat_index = None

    def _detect_material_type(self, description: str) -> str:
        """Detect material type from description."""
        desc_lower = str(description).lower()

        for mat_type in WASTE_FACTORS.keys():
            if mat_type in desc_lower:
                return mat_type

        # Check common synonyms
        synonyms = {
            'concrete': ['beton', 'cement'],
            'rebar': ['reinforcement', 'armature', 'арматура'],
            'brick': ['кирпич', 'block'],
            'lumber': ['wood', 'timber', 'древесина'],
            'drywall': ['gypsum', 'plasterboard', 'гипсокартон'],
            'tile': ['ceramic', 'плитка', 'керамика'],
            'paint': ['краска', 'coating'],
            'insulation': ['изоляция', 'утеплитель'],
            'pipe': ['труба', 'piping'],
            'wire': ['провод', 'cable', 'кабель']
        }

        for mat_type, words in synonyms.items():
            if any(word in desc_lower for word in words):
                return mat_type

        return 'default'

    def get_waste_factors(self, material_type: str) -> Dict[str, float]:
        """Get waste factors for material type."""
        return WASTE_FACTORS.get(material_type, WASTE_FACTORS['default'])

    def calculate_waste(self,
                        material_code: str,
                        base_quantity: float,
                        unit_cost: float = 0,
                        custom_factors: Dict[str, float] = None) -> WasteFactor:
        """Calculate waste for a material."""

        # Get material info
        material_name = material_code
        unit = "unit"

        if self._mat_index is not None and material_code in self._mat_index.index:
            mat = self._mat_index.loc[material_code]
            material_name = str(mat.get('description', mat.get('material_description', material_code)))
            unit = str(mat.get('unit', mat.get('material_unit', 'unit')))
            if unit_cost == 0:
                unit_cost = float(mat.get('material_cost', mat.get('unit_cost', 0)) or 0)

        # Detect material type and get factors
        mat_type = self._detect_material_type(material_name)
        factors = custom_factors or self.get_waste_factors(mat_type)

        cutting = factors.get('cutting', 0)
        spillage = factors.get('spillage', 0)
        breakage = factors.get('breakage', 0)
        overrun = factors.get('overrun', 0)

        # Calculate total waste
        total_waste_pct = cutting + spillage + breakage + overrun
        waste_quantity = base_quantity * total_waste_pct
        quantity_with_waste = base_quantity + waste_quantity
        waste_cost = waste_quantity * unit_cost

        return WasteFactor(
            material_code=material_code,
            material_name=material_name,
            base_quantity=base_quantity,
            unit=unit,
            cutting_waste_pct=round(cutting * 100, 1),
            spillage_pct=round(spillage * 100, 1),
            breakage_pct=round(breakage * 100, 1),
            overrun_pct=round(overrun * 100, 1),
            total_waste_pct=round(total_waste_pct * 100, 1),
            quantity_with_waste=round(quantity_with_waste, 2),
            waste_quantity=round(waste_quantity, 2),
            waste_cost=round(waste_cost, 2)
        )

    def calculate_project_waste(self,
                                 materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate waste for entire project."""

        results = []
        total_base_cost = 0
        total_waste_cost = 0

        for mat in materials:
            code = mat.get('material_code', mat.get('code'))
            qty = mat.get('quantity', 0)
            cost = mat.get('unit_cost', 0)
            custom = mat.get('waste_factors')

            waste = self.calculate_waste(code, qty, cost, custom)
            results.append(waste)

            total_base_cost += qty * cost
            total_waste_cost += waste.waste_cost

        # Summary by waste category
        by_category = {
            'cutting': sum(r.cutting_waste_pct * r.base_quantity / 100 for r in results),
            'spillage': sum(r.spillage_pct * r.base_quantity / 100 for r in results),
            'breakage': sum(r.breakage_pct * r.base_quantity / 100 for r in results),
            'overrun': sum(r.overrun_pct * r.base_quantity / 100 for r in results)
        }

        return {
            'materials': results,
            'total_base_cost': round(total_base_cost, 2),
            'total_waste_cost': round(total_waste_cost, 2),
            'waste_percentage': round(total_waste_cost / total_base_cost * 100, 1) if total_base_cost > 0 else 0,
            'by_category': by_category,
            'order_quantity_increase': round(sum(r.waste_quantity for r in results), 2)
        }

    def optimize_cutting(self,
                          material_code: str,
                          required_lengths: List[float],
                          stock_length: float) -> Dict[str, Any]:
        """Optimize cutting to minimize waste (1D cutting stock problem)."""

        # Simple first-fit decreasing algorithm
        sorted_lengths = sorted(required_lengths, reverse=True)
        stock_pieces = []
        waste_per_piece = []

        for length in sorted_lengths:
            placed = False
            for i, remaining in enumerate(stock_pieces):
                if remaining >= length:
                    stock_pieces[i] -= length
                    placed = True
                    break

            if not placed:
                stock_pieces.append(stock_length - length)

        total_stock_needed = len(stock_pieces)
        total_material = total_stock_needed * stock_length
        total_used = sum(required_lengths)
        total_waste = total_material - total_used
        waste_pct = total_waste / total_material * 100 if total_material > 0 else 0

        return {
            'material_code': material_code,
            'stock_pieces_needed': total_stock_needed,
            'stock_length': stock_length,
            'total_material': round(total_material, 2),
            'total_used': round(total_used, 2),
            'total_waste': round(total_waste, 2),
            'waste_percentage': round(waste_pct, 1),
            'cutting_efficiency': round(100 - waste_pct, 1)
        }

    def export_waste_report(self,
                            project_waste: Dict[str, Any],
                            output_path: str) -> str:
        """Export waste report to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Total Base Cost': project_waste['total_base_cost'],
                'Total Waste Cost': project_waste['total_waste_cost'],
                'Waste Percentage': project_waste['waste_percentage'],
                'Order Increase': project_waste['order_quantity_increase']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Materials
            mat_df = pd.DataFrame([
                {
                    'Material': m.material_name,
                    'Base Qty': m.base_quantity,
                    'Unit': m.unit,
                    'Cutting %': m.cutting_waste_pct,
                    'Spillage %': m.spillage_pct,
                    'Breakage %': m.breakage_pct,
                    'Overrun %': m.overrun_pct,
                    'Total Waste %': m.total_waste_pct,
                    'Order Qty': m.quantity_with_waste,
                    'Waste Cost': m.waste_cost
                }
                for m in project_waste['materials']
            ])
            mat_df.to_excel(writer, sheet_name='Materials', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize calculator
waste_calc = CWICRWasteCalculator(cwicr)

# Calculate waste for single material
waste = waste_calc.calculate_waste(
    material_code="CONC-001",
    base_quantity=100,
    unit_cost=150
)

print(f"Base Qty: {waste.base_quantity}")
print(f"Order Qty: {waste.quantity_with_waste}")
print(f"Waste: {waste.total_waste_pct}%")
print(f"Waste Cost: ${waste.waste_cost:,.2f}")
```

## Common Use Cases

### 1. Project-Wide Waste
```python
materials = [
    {'code': 'CONC-001', 'quantity': 200, 'unit_cost': 150},
    {'code': 'REBAR-002', 'quantity': 5000, 'unit_cost': 1.2},
    {'code': 'BRICK-003', 'quantity': 10000, 'unit_cost': 0.50}
]

project = waste_calc.calculate_project_waste(materials)
print(f"Total Waste Cost: ${project['total_waste_cost']:,.2f}")
```

### 2. Cutting Optimization
```python
cutting = waste_calc.optimize_cutting(
    material_code="REBAR-001",
    required_lengths=[2.5, 3.0, 1.8, 2.2, 4.0, 3.5],
    stock_length=6.0
)
print(f"Efficiency: {cutting['cutting_efficiency']}%")
```

### 3. Custom Waste Factors
```python
custom_factors = {'cutting': 0.15, 'spillage': 0, 'breakage': 0.05, 'overrun': 0.05}
waste = waste_calc.calculate_waste("TILE-001", 500, 25, custom_factors)
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Material Waste Management
