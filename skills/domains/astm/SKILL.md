---
name: astm
version: "1.0.0"
category: engineering
description: "ASTM Standards Specialist"
---

# ASTM Standards Specialist

> American Society for Testing and Materials (ASTM) standards for material properties and testing methods.

**Version:** 1.0.0
**Created:** 2026-01-12
**Category:** SME / Codes & Standards

## Overview

ASTM standards define the specific properties of materials (steel, plastic, rubber) and the exact methods used to test them. They are referenced by almost all other design codes (API, DNV, ASME).

## Core Capabilities

### 1. Ferrous Metals (Steel)
- **ASTM A36**: Standard Carbon Structural Steel.
- **ASTM A193 / A320**: Alloy steel and stainless steel bolting materials (High/Low temp).
- **ASTM A370**: Standard Test Methods and Definitions for Mechanical Testing of Steel Products.

### 2. Testing Methods
- **ASTM E8**: Tension Testing of Metallic Materials.
- **ASTM E23**: Notched Bar Impact Testing (Charpy V-Notch).

## When to Use

### Use This Skill When:
- Specifying material grades on engineering drawings.
- Reviewing Material Test Reports (MTRs).
- Defining Charpy impact test requirements for low-temperature service.

## Knowledge Areas

### 1. Grades and Classes
ASTM specifications often have multiple Grades (strength levels) and Classes (heat treatment/processing).
*   Example: **ASTM A193 Grade B7** (Chromium-Molybdenum steel, Quenched & Tempered).

### 2. Charpy Impact Testing
Critical for offshore/subsea applications. Ensures material is ductile at operating temperature.

## Code & Data Patterns

### Bolting Material Selector
```python
def select_bolt_grade(temperature_c):
    """
    Suggest ASTM bolt grade based on service temperature.
    """
    if temperature_c < -40:
        return "ASTM A320 Grade L7 (Low Temp)"
    elif temperature_c > 400:
        return "ASTM A193 Grade B16 (High Temp)"
    else:
        return "ASTM A193 Grade B7 (Standard)"
```

## Best Practices

- **MTR Review**: Always verify that the Yield and Tensile strengths on the MTR meet the ASTM minimums.
- **Supplementary Requirements**: Use "S" codes (e.g., S1, S5) to mandate additional testing like Ultrasonics (UT) or Magnetic Particle (MT).

## Resources
- **Source Files**: `/mnt/ace/O&G-Standards/ASTM/`
