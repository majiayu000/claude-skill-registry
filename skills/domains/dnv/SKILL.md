---
name: dnv
version: "1.0.0"
category: engineering
description: "DNV Standards Specialist"
---

# DNV Standards Specialist

> Det Norske Veritas (DNV) rules and standards for marine, offshore, and renewable energy industries.

**Version:** 1.0.0
**Created:** 2026-01-12
**Category:** SME / Codes & Standards

## Overview

DNV (formerly DNV GL) provides the technical rules for ship classification and widely used standards for offshore structures, pipelines, and wind energy. This skill covers the navigation and application of DNV Offshore Standards (OS) and Recommended Practices (RP).

## Core Capabilities

### 1. Offshore Structures
- **DNV-OS-C101**: Design of Offshore Steel Structures (LRFD method).
- **DNV-OS-C201**: Structural Design of Offshore Units.
- **DNV-RP-C203**: Fatigue Design of Offshore Steel Structures (The industry gold standard for S-N curves).

### 2. Pipelines & Risers
- **DNV-OS-F101**: Submarine Pipeline Systems.
- **DNV-OS-F201**: Dynamic Risers.
- **DNV-RP-F105**: Free Spanning Pipelines.

### 3. Marine Operations
- **DNV-ST-N001**: Marine Operations and Marine Warranty.

## When to Use

### Use This Skill When:
- Performing fatigue analysis (S-N curves).
- Designing subsea pipelines or risers.
- Classifying vessels or floating units.
- Planning marine warranty surveys.

### Do Not Use This Skill When:
- Designing wellhead equipment (use API).
- Specifying raw material testing methods (use ASTM).

## Knowledge Areas

### 1. Document Types
- **OS (Offshore Standard)**: Technical provisions and acceptance criteria.
- **RP (Recommended Practice)**: Guidance on how to perform analysis (e.g., how to calculate fatigue).
- **ST (Standard)**: Technical standards (often replacing older OS).

### 2. LRFD (Load and Resistance Factor Design)
DNV relies heavily on the LRFD method, using partial safety factors for loads and material resistance.

## Code & Data Patterns

### Fatigue S-N Curve Lookup (DNV-RP-C203)
```python
def get_dnv_sn_curve(curve_name, environment='air'):
    """
    Retrieve parameters for DNV S-N curves.
    """
    curves = {
        'B1': {'log_a': 12.564, 'm': 3.0},
        'B2': {'log_a': 12.449, 'm': 3.0},
        'C':  {'log_a': 12.192, 'm': 3.0},
        'D':  {'log_a': 11.764, 'm': 3.0}
    }
    
    params = curves.get(curve_name)
    if not params:
        raise ValueError("Unknown curve")
        
    if environment == 'seawater_cathodic':
        # DNV adjustment for seawater with CP
        params['log_a'] -= 0.176  # Example adjustment
        
    return params
```

## Best Practices

- **Fatigue Factors**: Be careful with the "Design Fatigue Factor" (DFF), which ranges from 1.0 to 10.0 depending on criticality and inspectability.
- **Environmental Loads**: DNV metocean criteria often differ slightly from API. Ensure consistency.

## Resources
- **Source Files**: `/mnt/ace/O&G-Standards/DNV/`
