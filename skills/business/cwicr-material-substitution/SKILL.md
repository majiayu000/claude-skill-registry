---
name: "cwicr-material-substitution"
description: "Find substitute materials using CWICR data. Identify equivalent alternatives based on function, cost, and availability."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Material Substitution

## Business Case

### Problem Statement
Material substitution challenges:
- Supply chain issues
- Cost optimization
- Specification compliance
- Equivalent performance

### Solution
Systematic material substitution using CWICR data to find functionally equivalent alternatives with cost and performance analysis.

### Business Value
- **Supply flexibility** - Alternative sources
- **Cost savings** - Lower-cost equivalents
- **Compliance** - Specification matching
- **Quick decisions** - Rapid alternative search

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from difflib import SequenceMatcher


class SubstitutionType(Enum):
    """Types of substitution."""
    DIRECT = "direct"        # Drop-in replacement
    EQUIVALENT = "equivalent"  # Same function, different material
    UPGRADE = "upgrade"      # Better performance
    DOWNGRADE = "downgrade"  # Lower performance (cost saving)


class CompatibilityLevel(Enum):
    """Compatibility levels."""
    EXACT = "exact"          # Identical specs
    HIGH = "high"            # Minor differences
    MEDIUM = "medium"        # Requires review
    LOW = "low"              # Significant differences


@dataclass
class MaterialSubstitute:
    """Material substitution option."""
    original_code: str
    original_description: str
    substitute_code: str
    substitute_description: str
    substitution_type: SubstitutionType
    compatibility: CompatibilityLevel
    original_cost: float
    substitute_cost: float
    cost_difference: float
    cost_difference_pct: float
    notes: str


# Material compatibility groups
MATERIAL_GROUPS = {
    'concrete': ['cement', 'beton', 'concrete', 'C20', 'C25', 'C30', 'C35', 'C40'],
    'steel': ['steel', 'rebar', 'reinforcement', 'S235', 'S275', 'S355'],
    'lumber': ['wood', 'timber', 'lumber', 'plywood', 'OSB'],
    'masonry': ['brick', 'block', 'CMU', 'masonry'],
    'insulation': ['insulation', 'rockwool', 'glasswool', 'EPS', 'XPS', 'PIR'],
    'pipe': ['pipe', 'PVC', 'HDPE', 'copper', 'steel pipe'],
    'electrical': ['wire', 'cable', 'conduit'],
    'finishing': ['paint', 'plaster', 'drywall', 'gypsum'],
    'flooring': ['tile', 'vinyl', 'laminate', 'carpet', 'hardwood'],
    'roofing': ['shingle', 'membrane', 'metal roof', 'tile roof']
}


class CWICRMaterialSubstitution:
    """Find material substitutions using CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame):
        self.materials = cwicr_data
        self._index_data()

    def _index_data(self):
        """Index material data."""
        if 'work_item_code' in self.materials.columns:
            self._code_index = self.materials.set_index('work_item_code')
        elif 'material_code' in self.materials.columns:
            self._code_index = self.materials.set_index('material_code')
        else:
            self._code_index = None

    def _similarity(self, a: str, b: str) -> float:
        """Calculate string similarity."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def _get_material_group(self, description: str) -> Optional[str]:
        """Identify material group from description."""
        desc_lower = description.lower()

        for group, keywords in MATERIAL_GROUPS.items():
            if any(kw.lower() in desc_lower for kw in keywords):
                return group

        return None

    def _get_cost(self, code: str) -> Tuple[float, str]:
        """Get material cost."""
        if self._code_index is None or code not in self._code_index.index:
            return (0, 'unit')

        item = self._code_index.loc[code]
        cost = float(item.get('material_cost', item.get('total_cost', 0)) or 0)
        unit = str(item.get('unit', 'unit'))

        return (cost, unit)

    def find_substitutes(self,
                          material_code: str,
                          max_results: int = 10,
                          max_cost_increase: float = 0.20,
                          include_upgrades: bool = True) -> List[MaterialSubstitute]:
        """Find substitute materials."""

        if self._code_index is None or material_code not in self._code_index.index:
            return []

        original = self._code_index.loc[material_code]
        original_desc = str(original.get('description', material_code))
        original_cost, original_unit = self._get_cost(material_code)

        group = self._get_material_group(original_desc)

        substitutes = []

        for code, row in self._code_index.iterrows():
            if code == material_code:
                continue

            sub_desc = str(row.get('description', code))
            sub_group = self._get_material_group(sub_desc)

            # Check if same group or similar description
            if group and sub_group == group:
                similarity = 0.7
            else:
                similarity = self._similarity(original_desc, sub_desc)

            if similarity < 0.3:
                continue

            sub_cost, sub_unit = self._get_cost(code)

            if sub_unit != original_unit:
                continue

            cost_diff = sub_cost - original_cost
            cost_diff_pct = (cost_diff / original_cost * 100) if original_cost > 0 else 0

            # Filter by cost increase limit
            if not include_upgrades and cost_diff_pct > max_cost_increase * 100:
                continue

            # Determine substitution type
            if cost_diff_pct < -10:
                sub_type = SubstitutionType.DOWNGRADE
            elif cost_diff_pct > 10:
                sub_type = SubstitutionType.UPGRADE
            elif similarity > 0.8:
                sub_type = SubstitutionType.DIRECT
            else:
                sub_type = SubstitutionType.EQUIVALENT

            # Determine compatibility
            if similarity > 0.9:
                compat = CompatibilityLevel.EXACT
            elif similarity > 0.7:
                compat = CompatibilityLevel.HIGH
            elif similarity > 0.5:
                compat = CompatibilityLevel.MEDIUM
            else:
                compat = CompatibilityLevel.LOW

            substitutes.append(MaterialSubstitute(
                original_code=material_code,
                original_description=original_desc,
                substitute_code=code,
                substitute_description=sub_desc,
                substitution_type=sub_type,
                compatibility=compat,
                original_cost=round(original_cost, 2),
                substitute_cost=round(sub_cost, 2),
                cost_difference=round(cost_diff, 2),
                cost_difference_pct=round(cost_diff_pct, 1),
                notes=f"Similarity: {similarity:.0%}"
            ))

        # Sort by compatibility then cost
        substitutes.sort(key=lambda x: (
            list(CompatibilityLevel).index(x.compatibility),
            x.cost_difference
        ))

        return substitutes[:max_results]

    def find_cost_saving_alternatives(self,
                                       material_code: str,
                                       min_savings_pct: float = 5.0) -> List[MaterialSubstitute]:
        """Find lower-cost alternatives."""

        subs = self.find_substitutes(material_code, max_results=20)

        cost_saving = [
            s for s in subs
            if s.cost_difference_pct <= -min_savings_pct
        ]

        return sorted(cost_saving, key=lambda x: x.cost_difference)

    def find_by_group(self,
                       group_name: str,
                       max_results: int = 20) -> List[Dict[str, Any]]:
        """Find all materials in a group."""

        if self._code_index is None:
            return []

        results = []

        for code, row in self._code_index.iterrows():
            desc = str(row.get('description', code))
            item_group = self._get_material_group(desc)

            if item_group == group_name.lower():
                cost, unit = self._get_cost(code)
                results.append({
                    'code': code,
                    'description': desc,
                    'cost': cost,
                    'unit': unit,
                    'group': item_group
                })

        return sorted(results, key=lambda x: x['cost'])[:max_results]

    def substitution_impact(self,
                            original_code: str,
                            substitute_code: str,
                            quantity: float) -> Dict[str, Any]:
        """Calculate impact of substitution."""

        original_cost, _ = self._get_cost(original_code)
        substitute_cost, _ = self._get_cost(substitute_code)

        original_total = original_cost * quantity
        substitute_total = substitute_cost * quantity
        impact = substitute_total - original_total

        return {
            'original_code': original_code,
            'substitute_code': substitute_code,
            'quantity': quantity,
            'original_unit_cost': original_cost,
            'substitute_unit_cost': substitute_cost,
            'original_total': round(original_total, 2),
            'substitute_total': round(substitute_total, 2),
            'cost_impact': round(impact, 2),
            'impact_percent': round(impact / original_total * 100, 1) if original_total > 0 else 0
        }

    def batch_substitution(self,
                            materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find substitutions for multiple materials."""

        results = []
        total_original = 0
        total_potential_savings = 0

        for mat in materials:
            code = mat.get('material_code', mat.get('code'))
            qty = mat.get('quantity', 1)

            subs = self.find_cost_saving_alternatives(code)

            original_cost, _ = self._get_cost(code)
            original_total = original_cost * qty
            total_original += original_total

            best_sub = subs[0] if subs else None
            potential_savings = 0

            if best_sub:
                impact = self.substitution_impact(code, best_sub.substitute_code, qty)
                potential_savings = abs(impact['cost_impact']) if impact['cost_impact'] < 0 else 0
                total_potential_savings += potential_savings

            results.append({
                'code': code,
                'quantity': qty,
                'original_total': round(original_total, 2),
                'best_substitute': best_sub.substitute_code if best_sub else None,
                'potential_savings': round(potential_savings, 2),
                'alternatives_count': len(subs)
            })

        return {
            'materials': results,
            'total_original_cost': round(total_original, 2),
            'total_potential_savings': round(total_potential_savings, 2),
            'savings_percent': round(total_potential_savings / total_original * 100, 1) if total_original > 0 else 0
        }

    def export_substitution_report(self,
                                    substitutes: List[MaterialSubstitute],
                                    output_path: str) -> str:
        """Export substitution report to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df = pd.DataFrame([
                {
                    'Original Code': s.original_code,
                    'Original Description': s.original_description,
                    'Substitute Code': s.substitute_code,
                    'Substitute Description': s.substitute_description,
                    'Type': s.substitution_type.value,
                    'Compatibility': s.compatibility.value,
                    'Original Cost': s.original_cost,
                    'Substitute Cost': s.substitute_cost,
                    'Cost Difference': s.cost_difference,
                    'Difference %': s.cost_difference_pct,
                    'Notes': s.notes
                }
                for s in substitutes
            ])
            df.to_excel(writer, sheet_name='Substitutes', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize substitution finder
sub_finder = CWICRMaterialSubstitution(cwicr)

# Find substitutes
substitutes = sub_finder.find_substitutes("CONC-C30-001")

for sub in substitutes[:5]:
    print(f"{sub.substitute_code}: ${sub.cost_difference:+.2f} ({sub.cost_difference_pct:+.1f}%)")
```

## Common Use Cases

### 1. Cost Saving Alternatives
```python
savings = sub_finder.find_cost_saving_alternatives("STEEL-S355", min_savings_pct=10)
for s in savings:
    print(f"{s.substitute_code}: Save ${abs(s.cost_difference):.2f}/unit")
```

### 2. Batch Analysis
```python
materials = [
    {'code': 'CONC-001', 'quantity': 200},
    {'code': 'STEEL-002', 'quantity': 5000},
    {'code': 'BRICK-003', 'quantity': 10000}
]

batch = sub_finder.batch_substitution(materials)
print(f"Potential Savings: ${batch['total_potential_savings']:,.2f}")
```

### 3. Material Group Search
```python
concrete_options = sub_finder.find_by_group('concrete')
for opt in concrete_options[:5]:
    print(f"{opt['code']}: ${opt['cost']:.2f}/{opt['unit']}")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Material Management
