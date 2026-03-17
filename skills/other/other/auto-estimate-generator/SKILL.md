---
name: "auto-estimate-generator"
description: "Automatically generate estimates from QTO data. Apply pricing rules to BIM quantities for cost estimates."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw":{"emoji":"⚡","os":["darwin","linux","win32"],"homepage":"https://datadrivenconstruction.io","requires":{"bins":["python3"]}}}
---

# Auto Estimate Generator

## Business Case

### Problem Statement
Manual estimate creation challenges:
- Time-consuming quantity mapping
- Inconsistent pricing rules
- Errors in calculations
- Difficulty updating estimates

### Solution
Automated estimate generation from BIM/QTO data using configurable pricing rules and assembly mappings.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class ElementType(Enum):
    WALL = "wall"
    FLOOR = "floor"
    CEILING = "ceiling"
    DOOR = "door"
    WINDOW = "window"
    COLUMN = "column"
    BEAM = "beam"
    FOUNDATION = "foundation"
    ROOF = "roof"
    STAIR = "stair"
    MEP = "mep"


@dataclass
class QTOItem:
    element_id: str
    element_type: ElementType
    name: str
    quantity: float
    unit: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PricingRule:
    rule_id: str
    name: str
    element_type: ElementType
    conditions: Dict[str, Any] = field(default_factory=dict)
    unit_cost: float = 0
    assembly_code: str = ""
    cost_breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class EstimateItem:
    qto_element_id: str
    description: str
    quantity: float
    unit: str
    unit_cost: float
    total_cost: float
    rule_applied: str
    wbs_code: str = ""


class AutoEstimateGenerator:
    """Generate estimates from QTO data automatically."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.pricing_rules: List[PricingRule] = []
        self.qto_items: List[QTOItem] = []
        self.estimate_items: List[EstimateItem] = []
        self.unmapped_items: List[QTOItem] = []

    def add_pricing_rule(self, rule: PricingRule):
        """Add pricing rule."""
        self.pricing_rules.append(rule)

    def load_pricing_rules_from_df(self, df: pd.DataFrame):
        """Load pricing rules from DataFrame."""

        for _, row in df.iterrows():
            conditions = {}
            if 'material' in row:
                conditions['material'] = row['material']
            if 'thickness_min' in row:
                conditions['thickness_min'] = row['thickness_min']
            if 'thickness_max' in row:
                conditions['thickness_max'] = row['thickness_max']

            rule = PricingRule(
                rule_id=row['rule_id'],
                name=row['name'],
                element_type=ElementType(row['element_type'].lower()),
                conditions=conditions,
                unit_cost=float(row['unit_cost']),
                assembly_code=row.get('assembly_code', ''),
                cost_breakdown={
                    'labor': float(row.get('labor_pct', 0.4)),
                    'material': float(row.get('material_pct', 0.5)),
                    'equipment': float(row.get('equipment_pct', 0.1))
                }
            )
            self.add_pricing_rule(rule)

    def load_qto_from_df(self, df: pd.DataFrame):
        """Load QTO items from DataFrame."""

        for _, row in df.iterrows():
            properties = {}
            for col in df.columns:
                if col not in ['element_id', 'element_type', 'name', 'quantity', 'unit']:
                    properties[col] = row[col]

            qto = QTOItem(
                element_id=str(row['element_id']),
                element_type=ElementType(row['element_type'].lower()),
                name=row['name'],
                quantity=float(row['quantity']),
                unit=row['unit'],
                properties=properties
            )
            self.qto_items.append(qto)

    def find_matching_rule(self, qto_item: QTOItem) -> Optional[PricingRule]:
        """Find pricing rule that matches QTO item."""

        matching_rules = []

        for rule in self.pricing_rules:
            if rule.element_type != qto_item.element_type:
                continue

            # Check conditions
            match = True
            for key, value in rule.conditions.items():
                if key.endswith('_min'):
                    prop_name = key[:-4]
                    if prop_name in qto_item.properties:
                        if qto_item.properties[prop_name] < value:
                            match = False
                elif key.endswith('_max'):
                    prop_name = key[:-4]
                    if prop_name in qto_item.properties:
                        if qto_item.properties[prop_name] > value:
                            match = False
                else:
                    if key in qto_item.properties:
                        if qto_item.properties[key] != value:
                            match = False

            if match:
                matching_rules.append(rule)

        # Return most specific rule (most conditions)
        if matching_rules:
            return max(matching_rules, key=lambda r: len(r.conditions))
        return None

    def generate_estimate(self) -> Dict[str, Any]:
        """Generate estimate from QTO items."""

        self.estimate_items = []
        self.unmapped_items = []
        total_cost = 0

        for qto in self.qto_items:
            rule = self.find_matching_rule(qto)

            if rule:
                item_cost = qto.quantity * rule.unit_cost

                self.estimate_items.append(EstimateItem(
                    qto_element_id=qto.element_id,
                    description=f"{qto.name} ({rule.name})",
                    quantity=qto.quantity,
                    unit=qto.unit,
                    unit_cost=rule.unit_cost,
                    total_cost=round(item_cost, 2),
                    rule_applied=rule.rule_id,
                    wbs_code=rule.assembly_code
                ))
                total_cost += item_cost
            else:
                self.unmapped_items.append(qto)

        return {
            'project': self.project_name,
            'total_qto_items': len(self.qto_items),
            'mapped_items': len(self.estimate_items),
            'unmapped_items': len(self.unmapped_items),
            'mapping_rate': round(len(self.estimate_items) / len(self.qto_items) * 100, 1) if self.qto_items else 0,
            'total_cost': round(total_cost, 2),
            'items': self.estimate_items
        }

    def get_cost_by_element_type(self) -> Dict[str, float]:
        """Get cost breakdown by element type."""

        by_type = {}
        for qto in self.qto_items:
            for est_item in self.estimate_items:
                if est_item.qto_element_id == qto.element_id:
                    type_name = qto.element_type.value
                    by_type[type_name] = by_type.get(type_name, 0) + est_item.total_cost

        return {k: round(v, 2) for k, v in by_type.items()}

    def get_unmapped_summary(self) -> pd.DataFrame:
        """Get summary of unmapped items."""

        if not self.unmapped_items:
            return pd.DataFrame()

        data = []
        for item in self.unmapped_items:
            data.append({
                'Element ID': item.element_id,
                'Type': item.element_type.value,
                'Name': item.name,
                'Quantity': item.quantity,
                'Unit': item.unit,
                'Properties': str(item.properties)
            })

        return pd.DataFrame(data)

    def export_to_excel(self, output_path: str) -> str:
        """Export estimate to Excel."""

        result = self.generate_estimate()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Project': self.project_name,
                'Total QTO Items': result['total_qto_items'],
                'Mapped Items': result['mapped_items'],
                'Unmapped Items': result['unmapped_items'],
                'Mapping Rate %': result['mapping_rate'],
                'Total Cost': result['total_cost']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Estimate items
            items_df = pd.DataFrame([{
                'Element ID': item.qto_element_id,
                'Description': item.description,
                'Quantity': item.quantity,
                'Unit': item.unit,
                'Unit Cost': item.unit_cost,
                'Total Cost': item.total_cost,
                'WBS': item.wbs_code,
                'Rule': item.rule_applied
            } for item in self.estimate_items])
            items_df.to_excel(writer, sheet_name='Estimate', index=False)

            # By element type
            by_type_df = pd.DataFrame([
                {'Element Type': k, 'Cost': v}
                for k, v in self.get_cost_by_element_type().items()
            ])
            by_type_df.to_excel(writer, sheet_name='By Type', index=False)

            # Unmapped items
            unmapped_df = self.get_unmapped_summary()
            if not unmapped_df.empty:
                unmapped_df.to_excel(writer, sheet_name='Unmapped', index=False)

        return output_path

    def suggest_missing_rules(self) -> List[Dict[str, Any]]:
        """Suggest pricing rules for unmapped items."""

        suggestions = []
        seen_types = set()

        for item in self.unmapped_items:
            key = (item.element_type.value, str(item.properties))
            if key not in seen_types:
                seen_types.add(key)
                suggestions.append({
                    'element_type': item.element_type.value,
                    'sample_name': item.name,
                    'properties': item.properties,
                    'count': sum(1 for i in self.unmapped_items
                                if i.element_type == item.element_type
                                and str(i.properties) == str(item.properties))
                })

        return sorted(suggestions, key=lambda x: x['count'], reverse=True)
```

## Quick Start

```python
# Initialize generator
generator = AutoEstimateGenerator("Office Building A")

# Add pricing rules
generator.add_pricing_rule(PricingRule(
    rule_id="W-001",
    name="Interior Wall - Drywall",
    element_type=ElementType.WALL,
    conditions={"material": "Drywall"},
    unit_cost=45.00,
    assembly_code="09.29.10"
))

generator.add_pricing_rule(PricingRule(
    rule_id="W-002",
    name="Exterior Wall - Masonry",
    element_type=ElementType.WALL,
    conditions={"material": "Masonry"},
    unit_cost=125.00,
    assembly_code="04.21.13"
))

# Load QTO data
generator.qto_items = [
    QTOItem("W-001", ElementType.WALL, "Interior Wall L1", 500, "SF", {"material": "Drywall"}),
    QTOItem("W-002", ElementType.WALL, "Exterior Wall", 1200, "SF", {"material": "Masonry"})
]

# Generate estimate
result = generator.generate_estimate()
print(f"Total Cost: ${result['total_cost']:,.2f}")
print(f"Mapping Rate: {result['mapping_rate']}%")
```

## Common Use Cases

### 1. Cost by Element Type
```python
by_type = generator.get_cost_by_element_type()
for element_type, cost in by_type.items():
    print(f"{element_type}: ${cost:,.2f}")
```

### 2. Unmapped Items
```python
unmapped = generator.get_unmapped_summary()
print(unmapped)
```

### 3. Rule Suggestions
```python
suggestions = generator.suggest_missing_rules()
for s in suggestions:
    print(f"Need rule for: {s['element_type']} ({s['count']} items)")
```

## Resources
- **DDC Book**: Chapter 3.2 - QTO and Automated Estimates
- **Website**: https://datadrivenconstruction.io
