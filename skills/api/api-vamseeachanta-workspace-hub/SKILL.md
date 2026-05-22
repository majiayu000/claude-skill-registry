---
name: api
version: "1.0.0"
category: engineering
description: "API Standards Specialist"
---

# API Standards Specialist

> American Petroleum Institute (API) codes and standards for oil & gas production, refining, and offshore structures.

**Version:** 1.0.0
**Created:** 2026-01-12
**Category:** SME / Codes & Standards

## Overview

API standards are the globally recognized benchmarks for the oil and gas industry. This skill focuses on the application, lookup, and programmatic compliance verification of API specifications (Specs), Recommended Practices (RPs), and Standards (Std).

## Core Capabilities

### 1. Offshore Structures (Series 2)
- **API 2RD**: Dynamic Risers for Floating Production Systems.
- **API 2INT-MET**: Interim Metocean Criteria.
- **API 2A-WSD**: Planning, Designing, and Constructing Fixed Offshore Platforms.

### 2. Equipment & Valves (Series 6)
- **API 6A**: Wellhead and Christmas Tree Equipment.
- **API 6D**: Pipeline Valves.
- **API 610**: Centrifugal Pumps.

### 3. Subsea Production (Series 17)
- **API 17D**: Subsea Wellhead and Tree Equipment.
- **API 17N**: Subsea Production System Reliability, Technical Risk, and Integrity Management.

## When to Use

### Use This Skill When:
- Specifying equipment for drilling or production operations.
- Designing offshore structures (fixed or floating).
- Verifying valve and pump requirements.
- Conducting risk assessments (API 17N, API 14C).

### Do Not Use This Skill When:
- Designing ship hulls (use Class Society rules like DNV/ABS).
- Checking material testing protocols (use ASTM).
- Checking European pressure vessel codes (use PED/EN).

## Knowledge Areas

### 1. Spec vs. RP vs. Std
- **Spec (Specification)**: Prescriptive requirements. "Shall" statements are mandatory. (e.g., API 6A).
- **RP (Recommended Practice)**: Guidance and best practices. "Should" statements. (e.g., API RP 2SK for Mooring).
- **Std (Standard)**: Established norms.

### 2. Digital Lookup
Use the `StandardsLookup` tool to find full documents.
Path: `/mnt/ace/O&G-Standards/API/`

## Code & Data Patterns

### Compliance Check Pattern
```python
def check_api_6a_compliance(pressure_rating, temp_class, material_class):
    """
    Verify API 6A equipment rating.
    """
    valid_pressures = [2000, 3000, 5000, 10000, 15000, 20000]
    if pressure_rating not in valid_pressures:
        return False, f"Invalid API 6A pressure rating: {pressure_rating}"
        
    valid_temp_classes = ['K', 'L', 'P', 'R', 'S', 'T', 'U', 'V']
    if temp_class not in valid_temp_classes:
        return False, f"Invalid API 6A temp class: {temp_class}"
        
    return True, "Compliant"
```

### Search Implementation
```python
from digitalmodel.modules.standards_lookup import StandardsLookup

def find_api_docs(query):
    lookup = StandardsLookup()
    # Filter for API specifically
    results = [r for r in lookup.search(query) if "/API/" in r['path']]
    return results
```

## Best Practices

- **Version Control**: Always check the "Effective Date" of the standard. API standards are updated frequently.
- **Addenda**: Check for published addenda or errata sheets which modify the base document.
- **Monogram**: Ensure equipment manufacturers hold a valid API Monogram license if required.

## Resources
- **Source Files**: `/mnt/ace/O&G-Standards/API/`
- **Official Site**: api.org
