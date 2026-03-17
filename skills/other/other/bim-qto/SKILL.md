---
name: "bim-qto"
description: "Extract quantities from BIM/CAD data for cost estimation. Group by type, level, zone. Generate QTO reports."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⚡", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# BIM Quantity Takeoff

## Overview
Quantity Takeoff (QTO) extracts measurable quantities from BIM models. This skill processes BIM exports to generate grouped quantity reports for cost estimation.

## Python Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class QTOUnit(Enum):
    """Quantity takeoff measurement units."""
    COUNT = "ea"
    LENGTH = "m"
    AREA = "m2"
    VOLUME = "m3"
    WEIGHT = "kg"
    LINEAR_FOOT = "lf"
    SQUARE_FOOT = "sf"
    CUBIC_YARD = "cy"


@dataclass
class QTOItem:
    """Single QTO line item."""
    category: str
    type_name: str
    description: str
    quantity: float
    unit: str
    level: Optional[str] = None
    material: Optional[str] = None
    element_count: int = 0


@dataclass
class QTOReport:
    """Complete QTO report."""
    project_name: str
    items: List[QTOItem]
    total_elements: int
    categories: int
    generated_date: str


class BIMQuantityTakeoff:
    """Extract quantities from BIM data."""

    # Column mappings for different BIM exports
    COLUMN_MAPPINGS = {
        'type': ['Type Name', 'TypeName', 'type_name', 'Family and Type', 'IfcType'],
        'category': ['Category', 'category', 'IfcClass', 'Element Category'],
        'level': ['Level', 'level', 'Building Storey', 'BuildingStorey', 'Floor'],
        'volume': ['Volume', 'volume', 'Volume (m³)', 'Qty_Volume'],
        'area': ['Area', 'area', 'Surface Area', 'Area (m²)', 'Qty_Area'],
        'length': ['Length', 'length', 'Length (m)', 'Qty_Length'],
        'count': ['Count', 'count', 'Quantity', 'ElementCount'],
        'material': ['Material', 'material', 'Structural Material', 'MaterialName']
    }

    def __init__(self, df: pd.DataFrame):
        """Initialize with BIM data DataFrame."""
        self.df = df
        self.column_map = self._detect_columns()

    def _detect_columns(self) -> Dict[str, str]:
        """Detect which columns exist in data."""
        mapping = {}

        for standard, variants in self.COLUMN_MAPPINGS.items():
            for variant in variants:
                if variant in self.df.columns:
                    mapping[standard] = variant
                    break

        return mapping

    def get_column(self, standard_name: str) -> Optional[str]:
        """Get actual column name from standard name."""
        return self.column_map.get(standard_name)

    def group_by_type(self, sum_column: str = 'volume') -> pd.DataFrame:
        """Group quantities by type name."""

        type_col = self.get_column('type')
        qty_col = self.get_column(sum_column)

        if type_col is None:
            raise ValueError("Type column not found")

        if qty_col is None:
            # Fall back to count
            result = self.df.groupby(type_col).size().reset_index(name='count')
        else:
            result = self.df.groupby(type_col).agg({
                qty_col: 'sum'
            }).reset_index()
            result['count'] = self.df.groupby(type_col).size().values

        result.columns = ['Type', 'Quantity', 'Count'] if len(result.columns) == 3 else ['Type', 'Count']
        return result.sort_values('Count', ascending=False)

    def group_by_category(self, sum_column: str = 'volume') -> pd.DataFrame:
        """Group quantities by category."""

        cat_col = self.get_column('category')
        qty_col = self.get_column(sum_column)

        if cat_col is None:
            raise ValueError("Category column not found")

        agg_dict = {}
        if qty_col:
            agg_dict[qty_col] = 'sum'

        if agg_dict:
            result = self.df.groupby(cat_col).agg(agg_dict).reset_index()
            result['count'] = self.df.groupby(cat_col).size().values
        else:
            result = self.df.groupby(cat_col).size().reset_index(name='count')

        return result.sort_values('count', ascending=False)

    def group_by_level(self, sum_column: str = 'volume') -> pd.DataFrame:
        """Group quantities by building level."""

        level_col = self.get_column('level')
        qty_col = self.get_column(sum_column)

        if level_col is None:
            raise ValueError("Level column not found")

        agg_dict = {}
        if qty_col:
            agg_dict[qty_col] = 'sum'

        if agg_dict:
            result = self.df.groupby(level_col).agg(agg_dict).reset_index()
            result['count'] = self.df.groupby(level_col).size().values
        else:
            result = self.df.groupby(level_col).size().reset_index(name='count')

        return result

    def pivot_by_level_and_type(self) -> pd.DataFrame:
        """Create pivot table: levels as rows, types as columns."""

        level_col = self.get_column('level')
        type_col = self.get_column('type')

        if level_col is None or type_col is None:
            raise ValueError("Level or Type column not found")

        pivot = pd.crosstab(
            self.df[level_col],
            self.df[type_col],
            margins=True
        )

        return pivot

    def filter_by_category(self, categories: List[str]) -> 'BIMQuantityTakeoff':
        """Filter to specific categories."""

        cat_col = self.get_column('category')
        if cat_col is None:
            raise ValueError("Category column not found")

        filtered_df = self.df[self.df[cat_col].isin(categories)]
        return BIMQuantityTakeoff(filtered_df)

    def filter_by_level(self, levels: List[str]) -> 'BIMQuantityTakeoff':
        """Filter to specific levels."""

        level_col = self.get_column('level')
        if level_col is None:
            raise ValueError("Level column not found")

        filtered_df = self.df[self.df[level_col].isin(levels)]
        return BIMQuantityTakeoff(filtered_df)

    def get_walls(self) -> pd.DataFrame:
        """Get wall quantities."""
        cat_col = self.get_column('category')
        if cat_col:
            walls = self.df[self.df[cat_col].str.contains('Wall', case=False, na=False)]
            return BIMQuantityTakeoff(walls).group_by_type()
        return pd.DataFrame()

    def get_floors(self) -> pd.DataFrame:
        """Get floor/slab quantities."""
        cat_col = self.get_column('category')
        if cat_col:
            floors = self.df[self.df[cat_col].str.contains('Floor|Slab', case=False, na=False)]
            return BIMQuantityTakeoff(floors).group_by_type()
        return pd.DataFrame()

    def get_doors(self) -> pd.DataFrame:
        """Get door quantities."""
        cat_col = self.get_column('category')
        if cat_col:
            doors = self.df[self.df[cat_col].str.contains('Door', case=False, na=False)]
            return BIMQuantityTakeoff(doors).group_by_type()
        return pd.DataFrame()

    def get_windows(self) -> pd.DataFrame:
        """Get window quantities."""
        cat_col = self.get_column('category')
        if cat_col:
            windows = self.df[self.df[cat_col].str.contains('Window', case=False, na=False)]
            return BIMQuantityTakeoff(windows).group_by_type()
        return pd.DataFrame()

    def generate_report(self, project_name: str = "Project") -> QTOReport:
        """Generate complete QTO report."""

        from datetime import datetime

        items = []
        type_col = self.get_column('type')
        cat_col = self.get_column('category')
        level_col = self.get_column('level')
        vol_col = self.get_column('volume')
        area_col = self.get_column('area')
        mat_col = self.get_column('material')

        # Group by type
        grouped = self.df.groupby(type_col if type_col else self.df.columns[0])

        for type_name, group in grouped:
            # Determine primary quantity
            qty = 0
            unit = QTOUnit.COUNT.value

            if vol_col and vol_col in group.columns:
                qty = group[vol_col].sum()
                unit = QTOUnit.VOLUME.value
            elif area_col and area_col in group.columns:
                qty = group[area_col].sum()
                unit = QTOUnit.AREA.value
            else:
                qty = len(group)
                unit = QTOUnit.COUNT.value

            # Get category and material
            category = group[cat_col].iloc[0] if cat_col and cat_col in group.columns else ""
            material = group[mat_col].iloc[0] if mat_col and mat_col in group.columns else ""
            level = group[level_col].iloc[0] if level_col and level_col in group.columns else ""

            items.append(QTOItem(
                category=str(category),
                type_name=str(type_name),
                description=str(type_name),
                quantity=round(qty, 2),
                unit=unit,
                level=str(level) if level else None,
                material=str(material) if material else None,
                element_count=len(group)
            ))

        return QTOReport(
            project_name=project_name,
            items=items,
            total_elements=len(self.df),
            categories=self.df[cat_col].nunique() if cat_col else 0,
            generated_date=datetime.now().isoformat()
        )

    def to_excel(self, output_path: str, project_name: str = "Project"):
        """Export QTO to Excel with multiple sheets."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary by category
            self.group_by_category().to_excel(
                writer, sheet_name='By Category', index=False)

            # Summary by type
            self.group_by_type().to_excel(
                writer, sheet_name='By Type', index=False)

            # Level breakdown
            try:
                self.pivot_by_level_and_type().to_excel(
                    writer, sheet_name='Level-Type Matrix')
            except:
                pass

            # Walls
            walls = self.get_walls()
            if not walls.empty:
                walls.to_excel(writer, sheet_name='Walls', index=False)

            # Doors and Windows
            doors = self.get_doors()
            if not doors.empty:
                doors.to_excel(writer, sheet_name='Doors', index=False)

            windows = self.get_windows()
            if not windows.empty:
                windows.to_excel(writer, sheet_name='Windows', index=False)

        return output_path
```

## Quick Start

```python
# Load BIM export
df = pd.read_excel("revit_export.xlsx")

# Initialize QTO
qto = BIMQuantityTakeoff(df)

# Get quantities by type
by_type = qto.group_by_type()
print(by_type.head(10))

# Get wall schedule
walls = qto.get_walls()
print(walls)
```

## Common Use Cases

### 1. Full QTO Report
```python
qto = BIMQuantityTakeoff(df)
report = qto.generate_report("Office Building")
print(f"Elements: {report.total_elements}")
for item in report.items[:5]:
    print(f"{item.type_name}: {item.quantity} {item.unit}")
```

### 2. Level-by-Level Analysis
```python
pivot = qto.pivot_by_level_and_type()
print(pivot)
```

### 3. Export to Excel
```python
qto.to_excel("qto_report.xlsx", "My Project")
```

## Resources
- **DDC Book**: Chapter 3.2 - Quantity Take-Off
