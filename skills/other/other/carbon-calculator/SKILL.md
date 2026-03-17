---
slug: "carbon-calculator"
display_name: "Carbon Calculator"
description: "Calculate embodied carbon in construction materials. Track CO2 emissions, compare alternatives, and generate sustainability reports."
---

# Carbon Calculator

## Business Case

### Problem Statement
Sustainability requirements demand:
- Tracking embodied carbon
- Comparing material options
- Meeting carbon targets
- Reporting emissions

### Solution
Calculate and track embodied carbon for construction materials using standard emission factors.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class MaterialCategory(Enum):
    CONCRETE = "concrete"
    STEEL = "steel"
    ALUMINUM = "aluminum"
    TIMBER = "timber"
    BRICK = "brick"
    GLASS = "glass"
    INSULATION = "insulation"
    PLASTIC = "plastic"
    COPPER = "copper"
    OTHER = "other"


@dataclass
class CarbonFactor:
    material: str
    category: MaterialCategory
    ec_factor: float  # kgCO2e per unit
    unit: str
    source: str


@dataclass
class MaterialInput:
    material_code: str
    material_name: str
    quantity: float
    unit: str
    category: MaterialCategory


@dataclass
class CarbonResult:
    material_code: str
    material_name: str
    quantity: float
    unit: str
    ec_factor: float
    embodied_carbon: float  # kgCO2e
    category: str


# Embodied carbon factors (kgCO2e per unit)
CARBON_FACTORS = {
    # Concrete
    'concrete_c20': CarbonFactor('Concrete C20', MaterialCategory.CONCRETE, 240, 'm3', 'ICE Database'),
    'concrete_c30': CarbonFactor('Concrete C30', MaterialCategory.CONCRETE, 290, 'm3', 'ICE Database'),
    'concrete_c40': CarbonFactor('Concrete C40', MaterialCategory.CONCRETE, 350, 'm3', 'ICE Database'),
    'concrete_c50': CarbonFactor('Concrete C50', MaterialCategory.CONCRETE, 410, 'm3', 'ICE Database'),

    # Steel
    'steel_rebar': CarbonFactor('Rebar', MaterialCategory.STEEL, 1.99, 'kg', 'ICE Database'),
    'steel_section': CarbonFactor('Steel Section', MaterialCategory.STEEL, 1.55, 'kg', 'ICE Database'),
    'steel_sheet': CarbonFactor('Steel Sheet', MaterialCategory.STEEL, 2.03, 'kg', 'ICE Database'),
    'steel_stainless': CarbonFactor('Stainless Steel', MaterialCategory.STEEL, 6.15, 'kg', 'ICE Database'),

    # Aluminum
    'aluminum_general': CarbonFactor('Aluminum General', MaterialCategory.ALUMINUM, 9.16, 'kg', 'ICE Database'),
    'aluminum_recycled': CarbonFactor('Aluminum Recycled', MaterialCategory.ALUMINUM, 1.81, 'kg', 'ICE Database'),

    # Timber
    'timber_softwood': CarbonFactor('Softwood Timber', MaterialCategory.TIMBER, 0.31, 'kg', 'ICE Database'),
    'timber_hardwood': CarbonFactor('Hardwood Timber', MaterialCategory.TIMBER, 0.46, 'kg', 'ICE Database'),
    'timber_glulam': CarbonFactor('Glulam', MaterialCategory.TIMBER, 0.51, 'kg', 'ICE Database'),
    'timber_clt': CarbonFactor('CLT', MaterialCategory.TIMBER, 0.44, 'kg', 'ICE Database'),
    'timber_plywood': CarbonFactor('Plywood', MaterialCategory.TIMBER, 0.65, 'kg', 'ICE Database'),

    # Masonry
    'brick_common': CarbonFactor('Common Brick', MaterialCategory.BRICK, 0.24, 'kg', 'ICE Database'),
    'block_concrete': CarbonFactor('Concrete Block', MaterialCategory.BRICK, 0.10, 'kg', 'ICE Database'),

    # Glass
    'glass_float': CarbonFactor('Float Glass', MaterialCategory.GLASS, 1.44, 'kg', 'ICE Database'),
    'glass_double': CarbonFactor('Double Glazing', MaterialCategory.GLASS, 35.0, 'm2', 'ICE Database'),

    # Insulation
    'insul_mineral': CarbonFactor('Mineral Wool', MaterialCategory.INSULATION, 1.28, 'kg', 'ICE Database'),
    'insul_eps': CarbonFactor('EPS', MaterialCategory.INSULATION, 3.29, 'kg', 'ICE Database'),
    'insul_xps': CarbonFactor('XPS', MaterialCategory.INSULATION, 3.29, 'kg', 'ICE Database'),

    # Other
    'copper_pipe': CarbonFactor('Copper Pipe', MaterialCategory.COPPER, 2.71, 'kg', 'ICE Database'),
    'pvc_pipe': CarbonFactor('PVC Pipe', MaterialCategory.PLASTIC, 3.10, 'kg', 'ICE Database'),
}


class CarbonCalculator:
    """Calculate embodied carbon for construction."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.materials: List[MaterialInput] = []
        self.results: List[CarbonResult] = []
        self.custom_factors: Dict[str, CarbonFactor] = {}

    def add_custom_factor(self,
                          code: str,
                          name: str,
                          category: MaterialCategory,
                          ec_factor: float,
                          unit: str,
                          source: str = "Custom"):
        """Add custom carbon factor."""

        self.custom_factors[code] = CarbonFactor(
            material=name,
            category=category,
            ec_factor=ec_factor,
            unit=unit,
            source=source
        )

    def get_factor(self, material_code: str) -> Optional[CarbonFactor]:
        """Get carbon factor for material."""

        # Check custom first
        if material_code in self.custom_factors:
            return self.custom_factors[material_code]

        # Check standard factors
        code_lower = material_code.lower().replace('-', '_').replace(' ', '_')
        return CARBON_FACTORS.get(code_lower)

    def add_material(self,
                     material_code: str,
                     material_name: str,
                     quantity: float,
                     unit: str,
                     category: MaterialCategory = MaterialCategory.OTHER):
        """Add material to calculation."""

        self.materials.append(MaterialInput(
            material_code=material_code,
            material_name=material_name,
            quantity=quantity,
            unit=unit,
            category=category
        ))

    def calculate(self) -> List[CarbonResult]:
        """Calculate embodied carbon for all materials."""

        self.results = []

        for mat in self.materials:
            factor = self.get_factor(mat.material_code)

            if factor:
                # Check unit compatibility
                if factor.unit == mat.unit:
                    ec = mat.quantity * factor.ec_factor
                else:
                    # Assume conversion needed - simplified
                    ec = mat.quantity * factor.ec_factor
            else:
                # Use default factor based on category
                default_factors = {
                    MaterialCategory.CONCRETE: 300,
                    MaterialCategory.STEEL: 1.8,
                    MaterialCategory.ALUMINUM: 9.0,
                    MaterialCategory.TIMBER: 0.4,
                    MaterialCategory.BRICK: 0.2,
                    MaterialCategory.GLASS: 1.5,
                    MaterialCategory.INSULATION: 2.0,
                    MaterialCategory.OTHER: 1.0
                }
                ec_factor = default_factors.get(mat.category, 1.0)
                ec = mat.quantity * ec_factor

            self.results.append(CarbonResult(
                material_code=mat.material_code,
                material_name=mat.material_name,
                quantity=mat.quantity,
                unit=mat.unit,
                ec_factor=factor.ec_factor if factor else 0,
                embodied_carbon=round(ec, 2),
                category=mat.category.value
            ))

        return self.results

    def get_total_carbon(self) -> float:
        """Get total embodied carbon (kgCO2e)."""
        return sum(r.embodied_carbon for r in self.results)

    def get_carbon_by_category(self) -> Dict[str, float]:
        """Get carbon breakdown by category."""

        by_category = {}
        for r in self.results:
            if r.category not in by_category:
                by_category[r.category] = 0
            by_category[r.category] += r.embodied_carbon

        return {k: round(v, 2) for k, v in by_category.items()}

    def compare_alternatives(self,
                              original_code: str,
                              original_qty: float,
                              alternative_code: str,
                              alternative_qty: float) -> Dict[str, Any]:
        """Compare carbon impact of material alternatives."""

        original_factor = self.get_factor(original_code)
        alt_factor = self.get_factor(alternative_code)

        if not original_factor or not alt_factor:
            return {}

        original_carbon = original_qty * original_factor.ec_factor
        alt_carbon = alternative_qty * alt_factor.ec_factor
        savings = original_carbon - alt_carbon

        return {
            'original_material': original_factor.material,
            'original_carbon': round(original_carbon, 2),
            'alternative_material': alt_factor.material,
            'alternative_carbon': round(alt_carbon, 2),
            'carbon_savings': round(savings, 2),
            'savings_percent': round(savings / original_carbon * 100, 1) if original_carbon > 0 else 0
        }

    def generate_report(self) -> Dict[str, Any]:
        """Generate carbon report."""

        if not self.results:
            self.calculate()

        total = self.get_total_carbon()
        by_category = self.get_carbon_by_category()

        # Find top contributors
        sorted_results = sorted(self.results, key=lambda x: x.embodied_carbon, reverse=True)
        top_5 = sorted_results[:5]

        # Convert to tonnes
        total_tonnes = total / 1000

        return {
            'project': self.project_name,
            'total_kgCO2e': round(total, 2),
            'total_tCO2e': round(total_tonnes, 2),
            'material_count': len(self.results),
            'by_category': by_category,
            'top_contributors': [
                {
                    'material': r.material_name,
                    'carbon': r.embodied_carbon,
                    'percentage': round(r.embodied_carbon / total * 100, 1) if total > 0 else 0
                }
                for r in top_5
            ]
        }

    def suggest_reductions(self) -> List[Dict[str, Any]]:
        """Suggest carbon reduction opportunities."""

        if not self.results:
            self.calculate()

        suggestions = []

        for r in self.results:
            # Steel -> Timber
            if r.category == 'steel' and r.embodied_carbon > 1000:
                suggestions.append({
                    'material': r.material_name,
                    'current_carbon': r.embodied_carbon,
                    'suggestion': 'Consider timber alternative where structurally feasible',
                    'potential_reduction': '60-80%'
                })

            # Standard concrete -> Low carbon
            if r.category == 'concrete' and r.embodied_carbon > 5000:
                suggestions.append({
                    'material': r.material_name,
                    'current_carbon': r.embodied_carbon,
                    'suggestion': 'Use low-carbon concrete mix with SCMs',
                    'potential_reduction': '20-40%'
                })

            # Virgin aluminum -> Recycled
            if r.category == 'aluminum':
                suggestions.append({
                    'material': r.material_name,
                    'current_carbon': r.embodied_carbon,
                    'suggestion': 'Specify recycled aluminum content',
                    'potential_reduction': '70-80%'
                })

        return suggestions

    def export_to_excel(self, output_path: str) -> str:
        """Export carbon calculation to Excel."""

        if not self.results:
            self.calculate()

        report = self.generate_report()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Project': self.project_name,
                'Total kgCO2e': report['total_kgCO2e'],
                'Total tCO2e': report['total_tCO2e'],
                'Materials': report['material_count']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Details
            details_df = pd.DataFrame([
                {
                    'Material Code': r.material_code,
                    'Material': r.material_name,
                    'Quantity': r.quantity,
                    'Unit': r.unit,
                    'EC Factor': r.ec_factor,
                    'Embodied Carbon (kgCO2e)': r.embodied_carbon,
                    'Category': r.category
                }
                for r in self.results
            ])
            details_df.to_excel(writer, sheet_name='Materials', index=False)

            # By Category
            cat_df = pd.DataFrame([
                {'Category': k, 'kgCO2e': v}
                for k, v in report['by_category'].items()
            ])
            cat_df.to_excel(writer, sheet_name='By Category', index=False)

            # Suggestions
            suggestions = self.suggest_reductions()
            if suggestions:
                sug_df = pd.DataFrame(suggestions)
                sug_df.to_excel(writer, sheet_name='Reduction Ideas', index=False)

        return output_path
```

## Quick Start

```python
# Initialize calculator
calc = CarbonCalculator("Office Building A")

# Add materials
calc.add_material("concrete_c30", "Foundation Concrete", 500, "m3", MaterialCategory.CONCRETE)
calc.add_material("steel_rebar", "Reinforcement", 50000, "kg", MaterialCategory.STEEL)
calc.add_material("steel_section", "Structural Steel", 200000, "kg", MaterialCategory.STEEL)
calc.add_material("glass_double", "Facade Glazing", 1500, "m2", MaterialCategory.GLASS)

# Calculate
results = calc.calculate()

# Get report
report = calc.generate_report()
print(f"Total: {report['total_tCO2e']} tCO2e")
```

## Common Use Cases

### 1. Compare Alternatives
```python
comparison = calc.compare_alternatives(
    "steel_section", 100000,
    "timber_glulam", 80000
)
print(f"Savings: {comparison['savings_percent']}%")
```

### 2. Get Suggestions
```python
suggestions = calc.suggest_reductions()
for s in suggestions:
    print(f"{s['material']}: {s['suggestion']}")
```

### 3. Category Breakdown
```python
by_category = calc.get_carbon_by_category()
for cat, carbon in by_category.items():
    print(f"{cat}: {carbon:,.0f} kgCO2e")
```

## Resources
- **ICE Database**: Inventory of Carbon & Energy
- **DDC Book**: Chapter 5.1 - Sustainability Reporting
