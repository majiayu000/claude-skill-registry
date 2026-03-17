---
name: "cwicr-resource-analyzer"
description: "Analyze construction resources (labor, materials, equipment) from DDC CWICR database. Calculate resource requirements, productivity metrics, and optimization recommendations."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Resource Analyzer

## Business Case

### Problem Statement
Construction projects require precise resource planning:
- How many labor hours are needed?
- What materials need to be procured?
- What equipment is required and for how long?

Traditional methods rely on experience-based estimates, leading to over/under allocation.

### Solution
Data-driven resource analysis using CWICR's 27,672 resources with detailed breakdowns of labor norms, material requirements, and equipment usage.

### Business Value
- **Accurate planning** - Based on validated resource norms
- **Cost optimization** - Identify resource inefficiencies
- **Procurement support** - Generate material lists
- **Labor planning** - Calculate crew requirements

## Technical Implementation

### Python Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class ResourceType(Enum):
    """Types of construction resources."""
    LABOR = "labor"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    SUBCONTRACT = "subcontract"


class LaborCategory(Enum):
    """Labor skill categories."""
    UNSKILLED = "unskilled"
    SEMI_SKILLED = "semi_skilled"
    SKILLED = "skilled"
    FOREMAN = "foreman"
    SUPERVISOR = "supervisor"
    SPECIALIST = "specialist"


class EquipmentCategory(Enum):
    """Equipment categories."""
    EARTHMOVING = "earthmoving"
    LIFTING = "lifting"
    CONCRETE = "concrete"
    TRANSPORT = "transport"
    COMPACTION = "compaction"
    PUMPING = "pumping"
    POWER_TOOLS = "power_tools"
    SCAFFOLDING = "scaffolding"


@dataclass
class LaborResource:
    """Represents a labor resource."""
    resource_code: str
    description: str
    category: LaborCategory
    hourly_rate: float
    skill_level: int
    productivity_factor: float = 1.0


@dataclass
class MaterialResource:
    """Represents a material resource."""
    resource_code: str
    description: str
    unit: str
    unit_price: float
    category: str
    waste_factor: float = 0.05  # 5% default waste


@dataclass
class EquipmentResource:
    """Represents an equipment resource."""
    resource_code: str
    description: str
    category: EquipmentCategory
    hourly_rate: float
    daily_rate: float
    monthly_rate: float
    fuel_consumption: float = 0.0  # liters per hour
    operator_required: bool = True


@dataclass
class ResourceRequirement:
    """Calculated resource requirement."""
    resource_code: str
    description: str
    resource_type: ResourceType
    quantity: float
    unit: str
    unit_cost: float
    total_cost: float
    duration_hours: float = 0.0


@dataclass
class ResourceSummary:
    """Summary of all resource requirements."""
    labor_hours: float
    labor_cost: float
    material_cost: float
    equipment_cost: float
    total_cost: float

    labor_by_category: Dict[str, float] = field(default_factory=dict)
    materials_list: List[Dict[str, Any]] = field(default_factory=list)
    equipment_list: List[Dict[str, Any]] = field(default_factory=list)


class CWICRResourceAnalyzer:
    """Analyze resources from CWICR database."""

    def __init__(self, cwicr_data: pd.DataFrame,
                 resources_data: Optional[pd.DataFrame] = None):
        self.work_items = cwicr_data
        self.resources = resources_data

        # Create indexes
        self._index_work_items()
        if resources_data is not None:
            self._index_resources()

    def _index_work_items(self):
        """Index work items for fast lookup."""
        if 'work_item_code' in self.work_items.columns:
            self._work_index = self.work_items.set_index('work_item_code')
        else:
            self._work_index = None

    def _index_resources(self):
        """Index resources for fast lookup."""
        if self.resources is not None and 'resource_code' in self.resources.columns:
            self._resource_index = self.resources.set_index('resource_code')
        else:
            self._resource_index = None

    def analyze_labor_requirements(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze labor requirements for work items."""

        total_hours = 0.0
        labor_by_category = defaultdict(float)
        labor_by_skill = defaultdict(float)
        labor_details = []

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if self._work_index is not None and code in self._work_index.index:
                work_item = self._work_index.loc[code]
                labor_norm = float(work_item.get('labor_norm', 0) or 0)
                hours = labor_norm * qty

                total_hours += hours

                # Get category if available
                category = str(work_item.get('category', 'General'))
                labor_by_category[category] += hours

                labor_details.append({
                    'work_item_code': code,
                    'description': work_item.get('description', ''),
                    'quantity': qty,
                    'labor_norm': labor_norm,
                    'total_hours': hours
                })

        return {
            'total_labor_hours': round(total_hours, 2),
            'labor_by_category': dict(labor_by_category),
            'crew_days_8hr': round(total_hours / 8, 1),
            'crew_weeks_40hr': round(total_hours / 40, 1),
            'details': labor_details
        }

    def analyze_material_requirements(self, items: List[Dict[str, Any]],
                                       include_waste: bool = True) -> Dict[str, Any]:
        """Analyze material requirements."""

        materials = defaultdict(lambda: {'quantity': 0, 'unit': '', 'cost': 0})
        total_cost = 0.0

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if self._work_index is not None and code in self._work_index.index:
                work_item = self._work_index.loc[code]
                material_cost = float(work_item.get('material_cost', 0) or 0) * qty

                if include_waste:
                    material_cost *= 1.05  # 5% waste factor

                total_cost += material_cost

                # Aggregate by category
                category = str(work_item.get('category', 'General'))
                materials[category]['cost'] += material_cost

        return {
            'total_material_cost': round(total_cost, 2),
            'by_category': dict(materials),
            'waste_included': include_waste,
            'waste_factor': 0.05 if include_waste else 0
        }

    def analyze_equipment_requirements(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze equipment requirements."""

        equipment_hours = defaultdict(float)
        total_cost = 0.0

        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if self._work_index is not None and code in self._work_index.index:
                work_item = self._work_index.loc[code]
                equipment_cost = float(work_item.get('equipment_cost', 0) or 0) * qty
                equipment_norm = float(work_item.get('equipment_norm', 0) or 0) * qty

                total_cost += equipment_cost

                category = str(work_item.get('category', 'General'))
                equipment_hours[category] += equipment_norm

        return {
            'total_equipment_cost': round(total_cost, 2),
            'equipment_hours_by_category': dict(equipment_hours),
            'total_equipment_hours': sum(equipment_hours.values())
        }

    def generate_resource_summary(self, items: List[Dict[str, Any]]) -> ResourceSummary:
        """Generate complete resource summary."""

        labor = self.analyze_labor_requirements(items)
        materials = self.analyze_material_requirements(items)
        equipment = self.analyze_equipment_requirements(items)

        # Calculate labor cost
        avg_labor_rate = 35.0  # Default hourly rate
        labor_cost = labor['total_labor_hours'] * avg_labor_rate

        return ResourceSummary(
            labor_hours=labor['total_labor_hours'],
            labor_cost=labor_cost,
            material_cost=materials['total_material_cost'],
            equipment_cost=equipment['total_equipment_cost'],
            total_cost=labor_cost + materials['total_material_cost'] + equipment['total_equipment_cost'],
            labor_by_category=labor['labor_by_category']
        )

    def calculate_crew_requirements(self, labor_hours: float,
                                     project_duration_days: int,
                                     hours_per_day: int = 8) -> Dict[str, Any]:
        """Calculate crew size requirements."""

        available_hours = project_duration_days * hours_per_day
        min_crew_size = labor_hours / available_hours if available_hours > 0 else 0

        return {
            'total_labor_hours': labor_hours,
            'project_duration_days': project_duration_days,
            'hours_per_day': hours_per_day,
            'minimum_crew_size': round(min_crew_size, 1),
            'recommended_crew_size': int(np.ceil(min_crew_size * 1.15)),  # 15% buffer
            'utilization_at_recommended': round(min_crew_size / np.ceil(min_crew_size * 1.15) * 100, 1)
        }

    def identify_critical_resources(self, items: List[Dict[str, Any]],
                                     top_n: int = 10) -> Dict[str, List[Dict]]:
        """Identify critical resources by cost impact."""

        breakdowns = []
        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if self._work_index is not None and code in self._work_index.index:
                work_item = self._work_index.loc[code]

                breakdowns.append({
                    'work_item_code': code,
                    'description': work_item.get('description', ''),
                    'quantity': qty,
                    'labor_cost': float(work_item.get('labor_cost', 0) or 0) * qty,
                    'material_cost': float(work_item.get('material_cost', 0) or 0) * qty,
                    'equipment_cost': float(work_item.get('equipment_cost', 0) or 0) * qty,
                    'total_cost': (
                        float(work_item.get('labor_cost', 0) or 0) +
                        float(work_item.get('material_cost', 0) or 0) +
                        float(work_item.get('equipment_cost', 0) or 0)
                    ) * qty
                })

        df = pd.DataFrame(breakdowns)
        if df.empty:
            return {'labor': [], 'material': [], 'equipment': [], 'total': []}

        return {
            'labor': df.nlargest(top_n, 'labor_cost')[['work_item_code', 'description', 'labor_cost']].to_dict('records'),
            'material': df.nlargest(top_n, 'material_cost')[['work_item_code', 'description', 'material_cost']].to_dict('records'),
            'equipment': df.nlargest(top_n, 'equipment_cost')[['work_item_code', 'description', 'equipment_cost']].to_dict('records'),
            'total': df.nlargest(top_n, 'total_cost')[['work_item_code', 'description', 'total_cost']].to_dict('records')
        }

    def analyze_productivity(self, items: List[Dict[str, Any]],
                             actual_hours: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Analyze productivity vs planned norms."""

        if actual_hours is None:
            return {'error': 'Actual hours required for productivity analysis'}

        analysis = []
        for item in items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if code in actual_hours and self._work_index is not None:
                if code in self._work_index.index:
                    work_item = self._work_index.loc[code]
                    planned_hours = float(work_item.get('labor_norm', 0) or 0) * qty
                    actual = actual_hours[code]

                    productivity = planned_hours / actual * 100 if actual > 0 else 0

                    analysis.append({
                        'work_item_code': code,
                        'planned_hours': planned_hours,
                        'actual_hours': actual,
                        'productivity_percent': round(productivity, 1),
                        'variance_hours': planned_hours - actual
                    })

        df = pd.DataFrame(analysis)
        if df.empty:
            return {'items': [], 'average_productivity': 0}

        return {
            'items': analysis,
            'average_productivity': round(df['productivity_percent'].mean(), 1),
            'total_variance': round(df['variance_hours'].sum(), 1),
            'underperforming_items': len(df[df['productivity_percent'] < 90])
        }


class ResourceOptimizer:
    """Optimize resource allocation."""

    def __init__(self, analyzer: CWICRResourceAnalyzer):
        self.analyzer = analyzer

    def suggest_material_substitutions(self, items: List[Dict[str, Any]],
                                        cost_threshold: float = 0.9) -> List[Dict]:
        """Suggest cheaper material substitutions."""
        # Placeholder for substitution logic
        return []

    def optimize_crew_allocation(self, labor_by_category: Dict[str, float],
                                  available_crew: Dict[str, int]) -> Dict[str, Any]:
        """Optimize crew allocation across categories."""

        allocation = {}
        unmet_demand = {}

        for category, hours_needed in labor_by_category.items():
            available = available_crew.get(category, 0)
            days_needed = hours_needed / 8

            if available > 0:
                days_available = available * 1  # 1 day per person
                if days_available >= days_needed:
                    allocation[category] = {
                        'assigned': int(np.ceil(days_needed)),
                        'remaining': available - int(np.ceil(days_needed))
                    }
                else:
                    allocation[category] = {'assigned': available, 'remaining': 0}
                    unmet_demand[category] = days_needed - days_available
            else:
                unmet_demand[category] = days_needed

        return {
            'allocation': allocation,
            'unmet_demand': unmet_demand,
            'fully_staffed': len(unmet_demand) == 0
        }
```

## Quick Start

```python
from cwicr_data_loader import CWICRDataLoader

# Load data
loader = CWICRDataLoader()
cwicr = loader.load("ddc_cwicr_en.parquet")

# Initialize analyzer
analyzer = CWICRResourceAnalyzer(cwicr)

# Define project items
items = [
    {'work_item_code': 'CONC-001', 'quantity': 150},
    {'work_item_code': 'EXCV-002', 'quantity': 200},
    {'work_item_code': 'REBAR-003', 'quantity': 15000}
]

# Analyze labor
labor = analyzer.analyze_labor_requirements(items)
print(f"Total Labor Hours: {labor['total_labor_hours']}")
print(f"Crew Days (8hr): {labor['crew_days_8hr']}")
```

## Common Use Cases

### 1. Crew Planning
```python
# Calculate required crew size
labor = analyzer.analyze_labor_requirements(items)
crew = analyzer.calculate_crew_requirements(
    labor_hours=labor['total_labor_hours'],
    project_duration_days=30
)
print(f"Minimum Crew: {crew['minimum_crew_size']}")
print(f"Recommended Crew: {crew['recommended_crew_size']}")
```

### 2. Material Procurement
```python
materials = analyzer.analyze_material_requirements(items, include_waste=True)
print(f"Total Material Cost: ${materials['total_material_cost']:,.2f}")
```

### 3. Productivity Tracking
```python
actual_hours = {
    'CONC-001': 280,
    'EXCV-002': 85,
    'REBAR-003': 450
}
productivity = analyzer.analyze_productivity(items, actual_hours)
print(f"Average Productivity: {productivity['average_productivity']}%")
```

## Resources

- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Resource-Based Cost Estimation
