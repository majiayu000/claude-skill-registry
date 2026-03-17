---
name: "cwicr-unit-converter"
description: "Convert between construction measurement units. Handle metric/imperial conversion, area/volume calculations, and unit normalization for CWICR data."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Unit Converter

## Business Case

### Problem Statement
Construction data comes in various unit systems:
- Metric vs Imperial measurements
- Different unit conventions by trade
- BIM quantities need normalization
- Regional standards differ

### Solution
Comprehensive unit conversion for construction quantities, normalizing data for CWICR integration and analysis.

### Business Value
- **Accuracy** - Eliminate unit conversion errors
- **Consistency** - Standardize across projects
- **Integration** - BIM to cost data alignment
- **Global** - Support international projects

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum


class UnitCategory(Enum):
    """Categories of measurement units."""
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    WEIGHT = "weight"
    TIME = "time"
    QUANTITY = "quantity"


class UnitSystem(Enum):
    """Unit systems."""
    METRIC = "metric"
    IMPERIAL = "imperial"
    MIXED = "mixed"


@dataclass
class UnitConversion:
    """Unit conversion result."""
    original_value: float
    original_unit: str
    converted_value: float
    target_unit: str
    conversion_factor: float
    category: UnitCategory


# Conversion factors to base units
# Base units: meter (length), m² (area), m³ (volume), kg (weight), hour (time)

CONVERSIONS = {
    # Length to meters
    'm': {'factor': 1.0, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'meter': {'factor': 1.0, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'meters': {'factor': 1.0, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'cm': {'factor': 0.01, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'mm': {'factor': 0.001, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'km': {'factor': 1000.0, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'ft': {'factor': 0.3048, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'feet': {'factor': 0.3048, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'foot': {'factor': 0.3048, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'in': {'factor': 0.0254, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'inch': {'factor': 0.0254, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'inches': {'factor': 0.0254, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'yd': {'factor': 0.9144, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'yard': {'factor': 0.9144, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'yards': {'factor': 0.9144, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'mi': {'factor': 1609.344, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'mile': {'factor': 1609.344, 'category': UnitCategory.LENGTH, 'base': 'm'},
    'lf': {'factor': 0.3048, 'category': UnitCategory.LENGTH, 'base': 'm'},  # Linear foot

    # Area to m²
    'm2': {'factor': 1.0, 'category': UnitCategory.AREA, 'base': 'm2'},
    'm²': {'factor': 1.0, 'category': UnitCategory.AREA, 'base': 'm2'},
    'sqm': {'factor': 1.0, 'category': UnitCategory.AREA, 'base': 'm2'},
    'cm2': {'factor': 0.0001, 'category': UnitCategory.AREA, 'base': 'm2'},
    'mm2': {'factor': 0.000001, 'category': UnitCategory.AREA, 'base': 'm2'},
    'ha': {'factor': 10000.0, 'category': UnitCategory.AREA, 'base': 'm2'},
    'hectare': {'factor': 10000.0, 'category': UnitCategory.AREA, 'base': 'm2'},
    'ft2': {'factor': 0.092903, 'category': UnitCategory.AREA, 'base': 'm2'},
    'sf': {'factor': 0.092903, 'category': UnitCategory.AREA, 'base': 'm2'},
    'sqft': {'factor': 0.092903, 'category': UnitCategory.AREA, 'base': 'm2'},
    'yd2': {'factor': 0.836127, 'category': UnitCategory.AREA, 'base': 'm2'},
    'sy': {'factor': 0.836127, 'category': UnitCategory.AREA, 'base': 'm2'},  # Square yard
    'acre': {'factor': 4046.86, 'category': UnitCategory.AREA, 'base': 'm2'},

    # Volume to m³
    'm3': {'factor': 1.0, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'm³': {'factor': 1.0, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'cbm': {'factor': 1.0, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'l': {'factor': 0.001, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'liter': {'factor': 0.001, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'litre': {'factor': 0.001, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'ml': {'factor': 0.000001, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'ft3': {'factor': 0.0283168, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'cf': {'factor': 0.0283168, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'cuft': {'factor': 0.0283168, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'yd3': {'factor': 0.764555, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'cy': {'factor': 0.764555, 'category': UnitCategory.VOLUME, 'base': 'm3'},  # Cubic yard
    'cuyd': {'factor': 0.764555, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'gal': {'factor': 0.00378541, 'category': UnitCategory.VOLUME, 'base': 'm3'},
    'gallon': {'factor': 0.00378541, 'category': UnitCategory.VOLUME, 'base': 'm3'},

    # Weight to kg
    'kg': {'factor': 1.0, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'kilogram': {'factor': 1.0, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'g': {'factor': 0.001, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'gram': {'factor': 0.001, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'mg': {'factor': 0.000001, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    't': {'factor': 1000.0, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'ton': {'factor': 1000.0, 'category': UnitCategory.WEIGHT, 'base': 'kg'},  # Metric ton
    'tonne': {'factor': 1000.0, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'mt': {'factor': 1000.0, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'lb': {'factor': 0.453592, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'lbs': {'factor': 0.453592, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'pound': {'factor': 0.453592, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'oz': {'factor': 0.0283495, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'ounce': {'factor': 0.0283495, 'category': UnitCategory.WEIGHT, 'base': 'kg'},
    'st': {'factor': 907.185, 'category': UnitCategory.WEIGHT, 'base': 'kg'},  # Short ton (US)

    # Time to hours
    'hr': {'factor': 1.0, 'category': UnitCategory.TIME, 'base': 'hr'},
    'hour': {'factor': 1.0, 'category': UnitCategory.TIME, 'base': 'hr'},
    'hours': {'factor': 1.0, 'category': UnitCategory.TIME, 'base': 'hr'},
    'h': {'factor': 1.0, 'category': UnitCategory.TIME, 'base': 'hr'},
    'min': {'factor': 1/60, 'category': UnitCategory.TIME, 'base': 'hr'},
    'minute': {'factor': 1/60, 'category': UnitCategory.TIME, 'base': 'hr'},
    'day': {'factor': 8.0, 'category': UnitCategory.TIME, 'base': 'hr'},  # 8-hour workday
    'days': {'factor': 8.0, 'category': UnitCategory.TIME, 'base': 'hr'},
    'week': {'factor': 40.0, 'category': UnitCategory.TIME, 'base': 'hr'},  # 40-hour week

    # Quantity (no conversion, just counting)
    'ea': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'each': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'pc': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'pcs': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'piece': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'pieces': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'no': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'nr': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'set': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'lot': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},
    'ls': {'factor': 1.0, 'category': UnitCategory.QUANTITY, 'base': 'ea'},  # Lump sum
}


class CWICRUnitConverter:
    """Convert between construction units."""

    def __init__(self):
        self.conversions = CONVERSIONS

    def normalize_unit(self, unit: str) -> str:
        """Normalize unit string for lookup."""
        return str(unit).lower().strip().replace(' ', '').replace('.', '')

    def get_unit_info(self, unit: str) -> Optional[Dict[str, Any]]:
        """Get conversion info for unit."""
        normalized = self.normalize_unit(unit)
        return self.conversions.get(normalized)

    def convert(self,
                value: float,
                from_unit: str,
                to_unit: str) -> UnitConversion:
        """Convert value between units."""

        from_info = self.get_unit_info(from_unit)
        to_info = self.get_unit_info(to_unit)

        if not from_info:
            raise ValueError(f"Unknown source unit: {from_unit}")
        if not to_info:
            raise ValueError(f"Unknown target unit: {to_unit}")

        if from_info['category'] != to_info['category']:
            raise ValueError(
                f"Cannot convert between {from_info['category'].value} and {to_info['category'].value}"
            )

        # Convert: source -> base -> target
        base_value = value * from_info['factor']
        converted_value = base_value / to_info['factor']
        conversion_factor = from_info['factor'] / to_info['factor']

        return UnitConversion(
            original_value=value,
            original_unit=from_unit,
            converted_value=round(converted_value, 6),
            target_unit=to_unit,
            conversion_factor=conversion_factor,
            category=from_info['category']
        )

    def to_metric(self, value: float, from_unit: str) -> UnitConversion:
        """Convert to standard metric unit."""

        info = self.get_unit_info(from_unit)
        if not info:
            raise ValueError(f"Unknown unit: {from_unit}")

        base_unit = info['base']
        return self.convert(value, from_unit, base_unit)

    def to_imperial(self, value: float, from_unit: str) -> UnitConversion:
        """Convert to common imperial unit."""

        info = self.get_unit_info(from_unit)
        if not info:
            raise ValueError(f"Unknown unit: {from_unit}")

        imperial_map = {
            'm': 'ft',
            'm2': 'sf',
            'm3': 'cy',
            'kg': 'lb',
            'hr': 'hr'
        }

        base = info['base']
        imperial_unit = imperial_map.get(base, base)

        return self.convert(value, from_unit, imperial_unit)

    def convert_dataframe(self,
                          df: pd.DataFrame,
                          value_column: str,
                          unit_column: str,
                          target_unit: str,
                          output_column: str = None) -> pd.DataFrame:
        """Convert units in DataFrame column."""

        result = df.copy()
        if output_column is None:
            output_column = f"{value_column}_converted"

        converted_values = []
        for _, row in df.iterrows():
            try:
                conversion = self.convert(
                    row[value_column],
                    row[unit_column],
                    target_unit
                )
                converted_values.append(conversion.converted_value)
            except ValueError:
                converted_values.append(None)

        result[output_column] = converted_values
        result[f'{output_column}_unit'] = target_unit

        return result

    def normalize_units(self,
                        df: pd.DataFrame,
                        value_column: str,
                        unit_column: str) -> pd.DataFrame:
        """Normalize all units to base metric units."""

        result = df.copy()
        normalized_values = []
        normalized_units = []

        for _, row in df.iterrows():
            try:
                conversion = self.to_metric(row[value_column], row[unit_column])
                normalized_values.append(conversion.converted_value)
                normalized_units.append(conversion.target_unit)
            except ValueError:
                normalized_values.append(row[value_column])
                normalized_units.append(row[unit_column])

        result[f'{value_column}_normalized'] = normalized_values
        result[f'{unit_column}_normalized'] = normalized_units

        return result


class ConstructionUnitHelper:
    """Helper for construction-specific unit operations."""

    def __init__(self):
        self.converter = CWICRUnitConverter()

    def calculate_area(self,
                       length: float, length_unit: str,
                       width: float, width_unit: str,
                       result_unit: str = 'm2') -> float:
        """Calculate area from length and width."""

        # Convert both to meters
        length_m = self.converter.convert(length, length_unit, 'm').converted_value
        width_m = self.converter.convert(width, width_unit, 'm').converted_value

        # Calculate area in m²
        area_m2 = length_m * width_m

        # Convert to requested unit
        return self.converter.convert(area_m2, 'm2', result_unit).converted_value

    def calculate_volume(self,
                         length: float, length_unit: str,
                         width: float, width_unit: str,
                         height: float, height_unit: str,
                         result_unit: str = 'm3') -> float:
        """Calculate volume from dimensions."""

        # Convert all to meters
        length_m = self.converter.convert(length, length_unit, 'm').converted_value
        width_m = self.converter.convert(width, width_unit, 'm').converted_value
        height_m = self.converter.convert(height, height_unit, 'm').converted_value

        # Calculate volume in m³
        volume_m3 = length_m * width_m * height_m

        # Convert to requested unit
        return self.converter.convert(volume_m3, 'm3', result_unit).converted_value

    def concrete_volume(self,
                        length_ft: float,
                        width_ft: float,
                        thickness_in: float) -> Dict[str, float]:
        """Calculate concrete volume (common US method)."""

        # Convert to meters
        length_m = self.converter.convert(length_ft, 'ft', 'm').converted_value
        width_m = self.converter.convert(width_ft, 'ft', 'm').converted_value
        thickness_m = self.converter.convert(thickness_in, 'in', 'm').converted_value

        volume_m3 = length_m * width_m * thickness_m
        volume_cy = self.converter.convert(volume_m3, 'm3', 'cy').converted_value

        return {
            'm3': round(volume_m3, 3),
            'cy': round(volume_cy, 2)
        }

    def rebar_weight(self,
                     length: float, length_unit: str,
                     bar_size: str) -> Dict[str, float]:
        """Calculate rebar weight from length and bar size."""

        # Rebar weight per meter (kg/m) - US bar sizes
        rebar_weights = {
            '#3': 0.561, '#4': 0.996, '#5': 1.556,
            '#6': 2.24, '#7': 3.049, '#8': 3.982,
            '#9': 5.06, '#10': 6.41, '#11': 7.91
        }

        weight_per_m = rebar_weights.get(bar_size, 1.0)
        length_m = self.converter.convert(length, length_unit, 'm').converted_value

        weight_kg = length_m * weight_per_m
        weight_lb = self.converter.convert(weight_kg, 'kg', 'lb').converted_value

        return {
            'kg': round(weight_kg, 2),
            'lb': round(weight_lb, 2),
            'ton': round(weight_kg / 1000, 4)
        }
```

## Quick Start

```python
# Initialize converter
converter = CWICRUnitConverter()

# Simple conversion
result = converter.convert(100, 'ft', 'm')
print(f"{result.original_value} {result.original_unit} = {result.converted_value} {result.target_unit}")

# Convert to metric
metric = converter.to_metric(1000, 'sf')
print(f"1000 sf = {metric.converted_value} m²")

# Convert DataFrame
df = pd.DataFrame({
    'quantity': [100, 50, 25],
    'unit': ['cy', 'm3', 'cf']
})
normalized = converter.normalize_units(df, 'quantity', 'unit')
```

## Common Use Cases

### 1. Area Calculation
```python
helper = ConstructionUnitHelper()
area = helper.calculate_area(
    length=50, length_unit='ft',
    width=30, width_unit='ft',
    result_unit='m2'
)
print(f"Area: {area} m²")
```

### 2. Concrete Volume
```python
volume = helper.concrete_volume(
    length_ft=20,
    width_ft=10,
    thickness_in=6
)
print(f"Concrete: {volume['cy']} CY = {volume['m3']} m³")
```

### 3. Rebar Weight
```python
weight = helper.rebar_weight(length=100, length_unit='m', bar_size='#5')
print(f"Rebar weight: {weight['kg']} kg")
```

### 4. Normalize BIM Quantities
```python
bim_data = pd.read_excel("bim_quantities.xlsx")
normalized = converter.normalize_units(bim_data, 'Quantity', 'Unit')
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 2.3 - Data Standardization
