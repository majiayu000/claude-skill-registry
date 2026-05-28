---
name: norsok
version: "1.0.0"
category: engineering
description: "NORSOK Standards Specialist"
---

# NORSOK Standards Specialist

> Norsk Sokkels Konkurranseposisjon (NORSOK) standards for the Norwegian petroleum industry.

**Version:** 1.0.0
**Created:** 2026-01-12
**Category:** SME / Codes & Standards

## Overview

NORSOK standards are developed by the Norwegian petroleum industry to ensure adequate safety, value adding, and cost effectiveness. They are known for being more stringent than international standards, particularly regarding materials and safety in harsh North Sea environments.

## Core Capabilities

### 1. Materials & Corrosion (M-Series)
- **M-001**: Materials selection.
- **M-501**: Surface preparation and protective coating.
- **M-601**: Welding and inspection of piping.

### 2. Drilling & Well (D-Series)
- **D-010**: Well integrity in drilling and well operations. (The global benchmark for well barriers).

### 3. Safety & Working Environment (S-Series)
- **S-001**: Technical Safety.
- **S-002**: Working Environment.

## When to Use

### Use This Skill When:
- Designing for the North Sea or harsh cold-climate environments.
- Defining Well Barrier Schematics (D-010).
- Specifying high-durability coating systems (M-501).

## Knowledge Areas

### 1. Well Barriers (D-010)
NORSOK D-010 defines the "Two Barrier Principle":
1.  **Primary Barrier**: First line of defense (e.g., fluid column, packer).
2.  **Secondary Barrier**: Back-up (e.g., BOP, Wellhead).

### 2. Material Data Sheets (MDS)
M-001 refers to specific MDSs that precisely define chemistry and testing for steel grades (e.g., "MDS D46" for Duplex Stainless Steel).

## Code & Data Patterns

### Barrier Status Check
```python
def check_barrier_status(primary_status, secondary_status):
    """
    Evaluate well integrity based on NORSOK D-010 principles.
    """
    if primary_status == "OK" and secondary_status == "OK":
        return "GREEN: Healthy"
    elif primary_status == "FAILED" and secondary_status == "OK":
        return "ORANGE: Degraded (Single Barrier Failure)"
    elif secondary_status == "FAILED":
        return "RED: Unsafe (Secondary or Double Failure)"
    else:
        return "UNKNOWN"
```

## Best Practices

- **Strictness**: Assume NORSOK requirements exceed API/ISO unless proven otherwise.
- **Coatings**: M-501 systems (e.g., System 7 for submerged) are industry standards even outside Norway.

## Resources
- **Source Files**: `/mnt/ace/O&G-Standards/Norsok/`
