---
name: unit-converter
description: Convert between physical units (length, mass, temperature, time, etc.). Use for scientific calculations, data transformation, or unit standardization.
---

# Unit Converter

Convert between units across multiple physical dimensions.

## Features

- **Multiple Categories**: Length, mass, temperature, time, volume, etc.
- **Compound Units**: Speed, density, pressure
- **Precision Control**: Configurable decimal places
- **Batch Conversion**: Convert lists of values
- **Formula Display**: Show conversion formulas

## Quick Start

```python
from unit_converter import UnitConverter

converter = UnitConverter()

# Simple conversion
result = converter.convert(100, "km", "miles")
print(f"100 km = {result:.2f} miles")

# With full details
result = converter.convert_with_details(72, "fahrenheit", "celsius")
print(result)
```

## CLI Usage

```bash
# Basic conversion
python unit_converter.py 100 km miles

# Temperature
python unit_converter.py 98.6 fahrenheit celsius

# With precision
python unit_converter.py 1.5 kg lbs --precision 4

# List supported units
python unit_converter.py --list

# List units in category
python unit_converter.py --list length

# Show formula
python unit_converter.py 100 cm inches --formula
```

## API Reference

### UnitConverter Class

```python
class UnitConverter:
    def __init__(self)

    # Conversion
    def convert(self, value: float, from_unit: str, to_unit: str) -> float
    def convert_with_details(self, value: float, from_unit: str, to_unit: str) -> dict
    def batch_convert(self, values: list, from_unit: str, to_unit: str) -> list

    # Information
    def list_categories(self) -> list
    def list_units(self, category: str = None) -> dict
    def get_formula(self, from_unit: str, to_unit: str) -> str
    def find_unit(self, query: str) -> list
```

## Supported Categories

### Length
| Unit | Aliases |
|------|---------|
| meter | m |
| kilometer | km |
| centimeter | cm |
| millimeter | mm |
| inch | in |
| foot | ft |
| yard | yd |
| mile | mi |
| nautical_mile | nm |

### Mass
| Unit | Aliases |
|------|---------|
| kilogram | kg |
| gram | g |
| milligram | mg |
| pound | lb, lbs |
| ounce | oz |
| ton | |
| metric_ton | tonne |

### Temperature
| Unit | Aliases |
|------|---------|
| celsius | c |
| fahrenheit | f |
| kelvin | k |

### Time
| Unit | Aliases |
|------|---------|
| second | s, sec |
| minute | min |
| hour | h, hr |
| day | d |
| week | wk |
| month | mo |
| year | yr |

### Volume
| Unit | Aliases |
|------|---------|
| liter | l |
| milliliter | ml |
| gallon | gal |
| quart | qt |
| pint | pt |
| cup | |
| fluid_ounce | fl_oz |
| cubic_meter | m3 |

### Area
| Unit | Aliases |
|------|---------|
| square_meter | m2, sqm |
| square_kilometer | km2 |
| square_foot | sqft, ft2 |
| acre | |
| hectare | ha |

### Speed
| Unit | Aliases |
|------|---------|
| meters_per_second | m/s, mps |
| kilometers_per_hour | km/h, kph |
| miles_per_hour | mph |
| knots | kt |

### Digital Storage
| Unit | Aliases |
|------|---------|
| byte | b |
| kilobyte | kb |
| megabyte | mb |
| gigabyte | gb |
| terabyte | tb |

### Energy
| Unit | Aliases |
|------|---------|
| joule | j |
| kilojoule | kj |
| calorie | cal |
| kilocalorie | kcal |
| watt_hour | wh |
| kilowatt_hour | kwh |

## Example Workflows

### Batch Conversion
```python
converter = UnitConverter()
weights_kg = [50, 75, 100, 125]
weights_lbs = converter.batch_convert(weights_kg, "kg", "lbs")
for kg, lbs in zip(weights_kg, weights_lbs):
    print(f"{kg} kg = {lbs:.1f} lbs")
```

### Find Compatible Units
```python
converter = UnitConverter()
# Search for units
matches = converter.find_unit("meter")
# Returns: ['meter', 'kilometer', 'centimeter', ...]
```

### Get Conversion Formula
```python
converter = UnitConverter()
formula = converter.get_formula("celsius", "fahrenheit")
print(formula)  # "F = (C × 9/5) + 32"
```

## Output Format

### convert_with_details()
```python
{
    "value": 100,
    "from_unit": "km",
    "to_unit": "miles",
    "result": 62.1371,
    "formula": "miles = km × 0.621371",
    "category": "length"
}
```

## Dependencies

No external dependencies - uses Python standard library.
