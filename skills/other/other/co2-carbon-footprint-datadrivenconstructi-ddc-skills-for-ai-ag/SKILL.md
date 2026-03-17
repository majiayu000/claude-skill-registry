---
slug: "co2-carbon-footprint"
display_name: "Co2 Carbon Footprint"
description: "Calculate and track CO2 emissions and carbon footprint for construction projects."
---

# CO2 Carbon Footprint Tracker

## Technical Implementation

```python
import pandas as pd
from datetime import date
from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class EmissionScope(Enum):
    SCOPE_1 = "scope_1"  # Direct emissions
    SCOPE_2 = "scope_2"  # Indirect from energy
    SCOPE_3 = "scope_3"  # Value chain emissions


class MaterialCategory(Enum):
    CONCRETE = "concrete"
    STEEL = "steel"
    ALUMINUM = "aluminum"
    TIMBER = "timber"
    GLASS = "glass"
    INSULATION = "insulation"
    OTHER = "other"


@dataclass
class EmissionFactor:
    material: str
    category: MaterialCategory
    factor: float  # kg CO2e per unit
    unit: str
    source: str


@dataclass
class EmissionEntry:
    entry_id: str
    material: str
    quantity: float
    unit: str
    emission_factor: float
    total_kgco2: float
    scope: EmissionScope
    lifecycle_stage: str  # A1-A3, A4, A5, etc.


class CarbonFootprintTracker:
    def __init__(self, project_name: str, gfa_m2: float):
        self.project_name = project_name
        self.gfa_m2 = gfa_m2
        self.entries: List[EmissionEntry] = []
        self.factors = self._load_default_factors()
        self._counter = 0

    def _load_default_factors(self) -> Dict[str, EmissionFactor]:
        factors = {
            'concrete_m3': EmissionFactor('Concrete C30/37', MaterialCategory.CONCRETE, 250, 'm3', 'EPD Generic'),
            'steel_kg': EmissionFactor('Structural Steel', MaterialCategory.STEEL, 2.5, 'kg', 'EPD Generic'),
            'rebar_kg': EmissionFactor('Reinforcement', MaterialCategory.STEEL, 1.99, 'kg', 'EPD Generic'),
            'aluminum_kg': EmissionFactor('Aluminum', MaterialCategory.ALUMINUM, 8.0, 'kg', 'EPD Generic'),
            'timber_m3': EmissionFactor('CLT Timber', MaterialCategory.TIMBER, -500, 'm3', 'EPD Generic'),
            'glass_m2': EmissionFactor('Double Glazing', MaterialCategory.GLASS, 35, 'm2', 'EPD Generic'),
        }
        return factors

    def add_material(self, material_key: str, quantity: float,
                    lifecycle_stage: str = "A1-A3") -> EmissionEntry:
        if material_key not in self.factors:
            return None

        self._counter += 1
        factor = self.factors[material_key]
        total = quantity * factor.factor

        entry = EmissionEntry(
            entry_id=f"EM-{self._counter:04d}",
            material=factor.material,
            quantity=quantity,
            unit=factor.unit,
            emission_factor=factor.factor,
            total_kgco2=total,
            scope=EmissionScope.SCOPE_3,
            lifecycle_stage=lifecycle_stage
        )
        self.entries.append(entry)
        return entry

    def add_custom_emission(self, description: str, quantity: float, unit: str,
                           factor: float, scope: EmissionScope,
                           stage: str = "A1-A3") -> EmissionEntry:
        self._counter += 1
        entry = EmissionEntry(
            entry_id=f"EM-{self._counter:04d}",
            material=description,
            quantity=quantity,
            unit=unit,
            emission_factor=factor,
            total_kgco2=quantity * factor,
            scope=scope,
            lifecycle_stage=stage
        )
        self.entries.append(entry)
        return entry

    def get_total_emissions(self) -> float:
        return sum(e.total_kgco2 for e in self.entries)

    def get_kgco2_per_m2(self) -> float:
        if self.gfa_m2 == 0:
            return 0
        return self.get_total_emissions() / self.gfa_m2

    def get_by_category(self) -> Dict[str, float]:
        by_category = {}
        for entry in self.entries:
            # Simplified category mapping
            for cat in MaterialCategory:
                if cat.value in entry.material.lower():
                    by_category[cat.value] = by_category.get(cat.value, 0) + entry.total_kgco2
                    break
            else:
                by_category['other'] = by_category.get('other', 0) + entry.total_kgco2
        return by_category

    def get_by_stage(self) -> Dict[str, float]:
        by_stage = {}
        for entry in self.entries:
            stage = entry.lifecycle_stage
            by_stage[stage] = by_stage.get(stage, 0) + entry.total_kgco2
        return by_stage

    def get_summary(self) -> Dict[str, Any]:
        total = self.get_total_emissions()
        return {
            'project': self.project_name,
            'gfa_m2': self.gfa_m2,
            'total_kgco2': round(total, 2),
            'total_tonco2': round(total / 1000, 2),
            'kgco2_per_m2': round(self.get_kgco2_per_m2(), 2),
            'entries_count': len(self.entries),
            'by_stage': self.get_by_stage()
        }

    def export_report(self, output_path: str):
        data = [{
            'ID': e.entry_id,
            'Material': e.material,
            'Quantity': e.quantity,
            'Unit': e.unit,
            'Factor': e.emission_factor,
            'kg CO2e': round(e.total_kgco2, 2),
            'Stage': e.lifecycle_stage
        } for e in self.entries]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
tracker = CarbonFootprintTracker("Office Tower", gfa_m2=25000)

# Add materials
tracker.add_material('concrete_m3', 5000)
tracker.add_material('steel_kg', 500000)
tracker.add_material('rebar_kg', 150000)
tracker.add_material('timber_m3', 200)

summary = tracker.get_summary()
print(f"Total: {summary['total_tonco2']} ton CO2e")
print(f"Per m2: {summary['kgco2_per_m2']} kg CO2e/m2")
```

## Resources
- **DDC Book**: Chapter 3.3 - CO2 Estimation
