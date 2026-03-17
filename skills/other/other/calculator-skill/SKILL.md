---
name: calculator
description: Simple calculator for basic arithmetic operations (addition, subtraction, multiplication, division). Use when performing calculations, converting units, or working with numbers.
---

# Calculator

## Overview

Perform basic arithmetic calculations with step-by-step computation display.

## Quick Start

### Basic Operations

**Addition**:
```python
result = 15 + 27
# Result: 42
```

**Subtraction**:
```python
result = 100 - 42
# Result: 58
```

**Multiplication**:
```python
result = 6 * 7
# Result: 42
```

**Division**:
```python
result = 84 / 2
# Result: 42.0
```

## Supported Operations

| Operation | Symbol | Example | Result |
|-----------|--------|---------|--------|
| Addition | + | 10 + 5 | 15 |
| Subtraction | - | 10 - 5 | 5 |
| Multiplication | * | 10 * 5 | 50 |
| Division | / | 10 / 5 | 2.0 |
| Modulo | % | 10 % 3 | 1 |
| Exponent | ** | 2 ** 8 | 256 |

## Complex Expressions

Calculate multi-step expressions:

```python
# Order of operations (PEMDAS)
result = (10 + 5) * 2 ** 3 / 4
# Step 1: Parentheses: 10 + 5 = 15
# Step 2: Exponent: 2 ** 3 = 8
# Step 3: Multiplication: 15 * 8 = 120
# Step 4: Division: 120 / 4 = 30.0
# Result: 30.0
```

## Unit Conversions

### Temperature

```python
# Celsius to Fahrenheit
celsius = 25
fahrenheit = (celsius * 9/5) + 32
# Result: 77.0°F

# Fahrenheit to Celsius
fahrenheit = 77
celsius = (fahrenheit - 32) * 5/9
# Result: 25.0°C
```

### Length

```python
# Meters to feet
meters = 10
feet = meters * 3.28084
# Result: 32.8084 feet

# Miles to kilometers
miles = 5
kilometers = miles * 1.60934
# Result: 8.0467 km
```

## Tips

- Use parentheses to control order of operations
- Division by zero returns error
- Use `//` for integer division
- Use `%` for remainder (modulo)

---

**Version**: 1.0
**Last Updated**: October 25, 2025
**Example Type**: Minimal skill (SKILL.md only)
