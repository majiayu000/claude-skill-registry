---
slug: "co2-carbon-footprint"
display_name: "Co2 Carbon Footprint"
description: "Calculate CO2 emissions and carbon footprint from BIM model data. Analyze embodied carbon by material, element, and building system."
---

# CO2 Carbon Footprint Calculator

## Business Case

### Problem Statement
Sustainability requirements demand carbon tracking:
- Need to quantify embodied carbon
- Material selection impact unclear
- Reporting requirements increasing
- No integration with BIM workflow

### Solution
Calculate CO2 emissions from BIM quantities using EPD (Environmental Product Declaration) data and carbon coefficients.

### Business Value
- **Sustainability** - Meet green building requirements
- **Design optimization** - Identify high-carbon elements
- **Reporting** - Automated carbon reports
- **Decision support** - Compare material alternatives

## Technical Implementation

```python
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class LifeCycleStage(Enum):
    """EN 15978 Life Cycle Stages."""
    A1_A3 = "a1_a3"  # Product stage
    A4 = "a4"        # Transport to site
    A5 = "a5"        # Construction
    B1_B7 = "b1_b7"  # Use stage
    C1_C4 = "c1_c4"  # End of life
    D = "d"          # Beyond system boundary


class MaterialCategory(Enum):
    """Material categories for carbon calculation."""
    CONCRETE = "concrete"
    STEEL = "steel"
    TIMBER = "timber"
    ALUMINUM = "aluminum"
    GLASS = "glass"
    BRICK = "brick"
    INSULATION = "insulation"
    GYPSUM = "gypsum"
    OTHER = "other"


@dataclass
class CarbonCoefficient:
    """Carbon emission coefficient for a material."""
    material: str
    category: MaterialCategory
    kgco2_per_unit: float  # kg CO2e per unit
    unit: str  # kg, m3, m2, etc.
    stage: LifeCycleStage
    source: str  # EPD reference
    uncertainty: float = 0.1  # 10% default uncertainty


@dataclass
class CarbonResult:
    """Carbon calculation result for an element."""
    element_id: str
    element_name: str
    material: str
    category: MaterialCategory
    quantity: float
    unit: str
    kgco2_per_unit: float
    total_kgco2: float
    stage: LifeCycleStage
    level: str = ""
    notes: str = ""


@dataclass
class CarbonSummary:
    """Carbon footprint summary."""
    total_kgco2: float
    total_tonco2: float
    by_material: Dict[str, float]
    by_category: Dict[str, float]
    by_stage: Dict[str, float]
    by_level: Dict[str, float]
    element_count: int
    gfa: float  # Gross Floor Area
    kgco2_per_m2: float


class CarbonCoefficientDatabase:
    """Database of carbon emission coefficients."""

    def __init__(self):
        self.coefficients: List[CarbonCoefficient] = []
        self._load_default_coefficients()

    def _load_default_coefficients(self):
        """Load standard carbon coefficients (EPD-based)."""
        # Concrete products
        self.add_coefficient(CarbonCoefficient(
            material="Concrete C30/37", category=MaterialCategory.CONCRETE,
            kgco2_per_unit=250, unit="m3", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Concrete"
        ))
        self.add_coefficient(CarbonCoefficient(
            material="Concrete C40/50", category=MaterialCategory.CONCRETE,
            kgco2_per_unit=300, unit="m3", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - High Strength Concrete"
        ))
        self.add_coefficient(CarbonCoefficient(
            material="Reinforcement Steel", category=MaterialCategory.STEEL,
            kgco2_per_unit=1.99, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Rebar"
        ))

        # Steel products
        self.add_coefficient(CarbonCoefficient(
            material="Structural Steel", category=MaterialCategory.STEEL,
            kgco2_per_unit=2.5, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Structural Steel"
        ))
        self.add_coefficient(CarbonCoefficient(
            material="Steel Sheet", category=MaterialCategory.STEEL,
            kgco2_per_unit=2.3, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Sheet Metal"
        ))

        # Timber products
        self.add_coefficient(CarbonCoefficient(
            material="Softwood Timber", category=MaterialCategory.TIMBER,
            kgco2_per_unit=-500, unit="m3", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - CLT (carbon sequestration)"
        ))
        self.add_coefficient(CarbonCoefficient(
            material="Glulam", category=MaterialCategory.TIMBER,
            kgco2_per_unit=-350, unit="m3", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Glued Laminated Timber"
        ))

        # Aluminum
        self.add_coefficient(CarbonCoefficient(
            material="Aluminum Profile", category=MaterialCategory.ALUMINUM,
            kgco2_per_unit=8.0, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Aluminum"
        ))

        # Glass
        self.add_coefficient(CarbonCoefficient(
            material="Float Glass", category=MaterialCategory.GLASS,
            kgco2_per_unit=15.0, unit="m2", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Float Glass"
        ))
        self.add_coefficient(CarbonCoefficient(
            material="Double Glazing Unit", category=MaterialCategory.GLASS,
            kgco2_per_unit=35.0, unit="m2", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - IGU"
        ))

        # Masonry
        self.add_coefficient(CarbonCoefficient(
            material="Clay Brick", category=MaterialCategory.BRICK,
            kgco2_per_unit=0.24, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Clay Brick"
        ))

        # Insulation
        self.add_coefficient(CarbonCoefficient(
            material="Mineral Wool", category=MaterialCategory.INSULATION,
            kgco2_per_unit=1.2, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Mineral Wool"
        ))
        self.add_coefficient(CarbonCoefficient(
            material="EPS Insulation", category=MaterialCategory.INSULATION,
            kgco2_per_unit=3.5, unit="kg", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - EPS"
        ))

        # Gypsum
        self.add_coefficient(CarbonCoefficient(
            material="Gypsum Board", category=MaterialCategory.GYPSUM,
            kgco2_per_unit=2.8, unit="m2", stage=LifeCycleStage.A1_A3,
            source="Generic EPD - Plasterboard"
        ))

    def add_coefficient(self, coefficient: CarbonCoefficient):
        """Add carbon coefficient to database."""
        self.coefficients.append(coefficient)

    def find_coefficient(self, material_name: str,
                        stage: LifeCycleStage = LifeCycleStage.A1_A3) -> Optional[CarbonCoefficient]:
        """Find matching coefficient for material."""
        material_lower = material_name.lower()

        # Direct match
        for coef in self.coefficients:
            if coef.material.lower() == material_lower and coef.stage == stage:
                return coef

        # Partial match
        for coef in self.coefficients:
            if material_lower in coef.material.lower() or coef.material.lower() in material_lower:
                if coef.stage == stage:
                    return coef

        # Category match
        category = self._guess_category(material_name)
        for coef in self.coefficients:
            if coef.category == category and coef.stage == stage:
                return coef

        return None

    def _guess_category(self, material_name: str) -> MaterialCategory:
        """Guess material category from name."""
        name_lower = material_name.lower()

        if any(w in name_lower for w in ['concrete', 'cement', 'mortar']):
            return MaterialCategory.CONCRETE
        if any(w in name_lower for w in ['steel', 'iron', 'metal']):
            return MaterialCategory.STEEL
        if any(w in name_lower for w in ['wood', 'timber', 'lumber', 'plywood', 'clt']):
            return MaterialCategory.TIMBER
        if any(w in name_lower for w in ['aluminum', 'aluminium']):
            return MaterialCategory.ALUMINUM
        if any(w in name_lower for w in ['glass', 'glazing']):
            return MaterialCategory.GLASS
        if any(w in name_lower for w in ['brick', 'masonry', 'block']):
            return MaterialCategory.BRICK
        if any(w in name_lower for w in ['insulation', 'wool', 'foam', 'eps', 'xps']):
            return MaterialCategory.INSULATION
        if any(w in name_lower for w in ['gypsum', 'drywall', 'plaster']):
            return MaterialCategory.GYPSUM

        return MaterialCategory.OTHER


class CO2FootprintCalculator:
    """Calculate carbon footprint from BIM data."""

    def __init__(self, coefficient_db: CarbonCoefficientDatabase = None):
        self.db = coefficient_db or CarbonCoefficientDatabase()
        self.results: List[CarbonResult] = []
        self.warnings: List[str] = []

    def calculate_element(self, element: Dict[str, Any],
                         stage: LifeCycleStage = LifeCycleStage.A1_A3) -> Optional[CarbonResult]:
        """Calculate carbon for single element."""
        material = element.get('material', '')
        if not material:
            self.warnings.append(f"Element {element.get('element_id')} has no material")
            return None

        coefficient = self.db.find_coefficient(material, stage)
        if not coefficient:
            self.warnings.append(f"No coefficient found for material: {material}")
            return None

        # Get quantity in correct unit
        quantity = self._get_quantity(element, coefficient.unit)
        if quantity is None or quantity <= 0:
            return None

        total_kgco2 = quantity * coefficient.kgco2_per_unit

        result = CarbonResult(
            element_id=str(element.get('element_id', '')),
            element_name=str(element.get('name', '')),
            material=material,
            category=coefficient.category,
            quantity=quantity,
            unit=coefficient.unit,
            kgco2_per_unit=coefficient.kgco2_per_unit,
            total_kgco2=total_kgco2,
            stage=stage,
            level=str(element.get('level', ''))
        )

        self.results.append(result)
        return result

    def _get_quantity(self, element: Dict[str, Any], unit: str) -> Optional[float]:
        """Get quantity in required unit."""
        unit_lower = unit.lower()

        if unit_lower == 'm3':
            return float(element.get('volume', 0) or 0)
        elif unit_lower == 'm2':
            return float(element.get('area', 0) or 0)
        elif unit_lower in ['kg', 'kilogram']:
            # Try weight, then estimate from volume
            weight = element.get('weight', 0)
            if weight:
                return float(weight)
            # Estimate from volume with density
            volume = element.get('volume', 0)
            if volume:
                density = self._estimate_density(element.get('material', ''))
                return float(volume) * density
        elif unit_lower in ['m', 'meter']:
            return float(element.get('length', 0) or 0)

        return None

    def _estimate_density(self, material: str) -> float:
        """Estimate material density in kg/m3."""
        material_lower = material.lower()

        densities = {
            'concrete': 2400,
            'steel': 7850,
            'timber': 500,
            'aluminum': 2700,
            'glass': 2500,
            'brick': 1800,
            'gypsum': 800
        }

        for key, density in densities.items():
            if key in material_lower:
                return density

        return 1500  # Default density

    def calculate_from_dataframe(self, df: pd.DataFrame,
                                 stage: LifeCycleStage = LifeCycleStage.A1_A3) -> List[CarbonResult]:
        """Calculate carbon for all elements in DataFrame."""
        self.results = []
        self.warnings = []

        for _, row in df.iterrows():
            self.calculate_element(row.to_dict(), stage)

        return self.results

    def get_summary(self, gfa: float = 0) -> CarbonSummary:
        """Generate carbon footprint summary."""
        by_material = {}
        by_category = {}
        by_stage = {}
        by_level = {}

        for result in self.results:
            # By material
            by_material[result.material] = by_material.get(result.material, 0) + result.total_kgco2

            # By category
            cat = result.category.value
            by_category[cat] = by_category.get(cat, 0) + result.total_kgco2

            # By stage
            stg = result.stage.value
            by_stage[stg] = by_stage.get(stg, 0) + result.total_kgco2

            # By level
            if result.level:
                by_level[result.level] = by_level.get(result.level, 0) + result.total_kgco2

        total_kgco2 = sum(r.total_kgco2 for r in self.results)

        return CarbonSummary(
            total_kgco2=round(total_kgco2, 2),
            total_tonco2=round(total_kgco2 / 1000, 2),
            by_material=by_material,
            by_category=by_category,
            by_stage=by_stage,
            by_level=by_level,
            element_count=len(self.results),
            gfa=gfa,
            kgco2_per_m2=round(total_kgco2 / gfa, 2) if gfa > 0 else 0
        )

    def export_results(self, output_path: str):
        """Export results to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Detailed results
            results_df = pd.DataFrame([{
                'Element ID': r.element_id,
                'Element Name': r.element_name,
                'Material': r.material,
                'Category': r.category.value,
                'Quantity': r.quantity,
                'Unit': r.unit,
                'kg CO2e/unit': r.kgco2_per_unit,
                'Total kg CO2e': round(r.total_kgco2, 2),
                'Level': r.level
            } for r in self.results])

            results_df.to_excel(writer, sheet_name='Details', index=False)

            # Summary
            summary = self.get_summary()
            summary_df = pd.DataFrame([
                {'Metric': 'Total kg CO2e', 'Value': summary.total_kgco2},
                {'Metric': 'Total ton CO2e', 'Value': summary.total_tonco2},
                {'Metric': 'Elements Analyzed', 'Value': summary.element_count}
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

        return output_path
```

## Quick Start

```python
# Initialize calculator
calculator = CO2FootprintCalculator()

# Load BIM quantities
elements = pd.read_excel("bim_quantities.xlsx")

# Calculate carbon
results = calculator.calculate_from_dataframe(elements)

# Get summary
summary = calculator.get_summary(gfa=5000)  # 5000 m2 GFA
print(f"Total: {summary.total_tonco2} ton CO2e")
print(f"Per m2: {summary.kgco2_per_m2} kg CO2e/m2")
```

## Common Use Cases

### 1. Material Comparison
```python
# Compare concrete vs timber
concrete_elements = elements[elements['material'].str.contains('Concrete')]
timber_elements = elements[elements['material'].str.contains('Timber')]
```

### 2. Target Compliance
```python
TARGET_KGCO2_M2 = 500  # LEED/BREEAM target
if summary.kgco2_per_m2 > TARGET_KGCO2_M2:
    print(f"Warning: Exceeds target by {summary.kgco2_per_m2 - TARGET_KGCO2_M2} kg/m2")
```

### 3. Export Report
```python
calculator.export_results("carbon_report.xlsx")
```

## Resources
- **DDC Book**: Chapter 3.3 - CO2 Estimation
- **Reference**: EN 15978, EPD databases
