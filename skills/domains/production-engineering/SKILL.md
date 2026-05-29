---
name: production-engineering
version: "1.0.0"
category: engineering
description: "Production Engineering Skill"
---

# Production Engineering Skill

> Fundamentals of production, surveillance, and lessons learnt for offshore and onshore assets.

**Version:** 1.0.0
**Created:** 2026-01-12
**Category:** Subject Matter Expert (SME)

## Overview

Production engineering involves the design, monitoring, and optimization of well performance and production systems. This skill encapsulates the core knowledge extracted from legacy "Surveillance Workshops" and EOR evaluations, focusing on maximizing asset value while ensuring operational safety.

## Core Capabilities

### 1. Production Surveillance
- **Real-time Monitoring**: Tracking well performance (pressures, temperatures, flow rates).
- **Surveillance Workshops**: Structured review processes for identifying underperforming wells.
- **Diagnostics**: Pressure transient analysis (PTA), production logging tool (PLT) interpretation, and nodal analysis.

### 2. Enhanced Oil Recovery (EOR)
- **Waterflooding**: Optimization of injection rates and voidage replacement.
- **EOR Evaluations**: Assessment of advanced recovery techniques (CO2, Steam, Chemical).
- **Iron Sulfide Management**: Mitigating scaling and corrosion in EOR environments (Lessons Learnt from Permian Basin).

### 3. Artificial Lift Optimization
- **ESP (Electric Submersible Pumps)**: Selection and pump curve analysis.
- **Gas Lift**: Injection rate optimization and stability analysis.
- **Jet Pumps**: Operation and maintenance fundamentals.

### 4. Well Integrity & Maintenance
- **Liner Performance**: Monitoring and failure analysis from legacy surveillance logs.
- **Bacteria Control**: Managing microbial growth in production systems (Lessons Learnt from Seminole).
- **Scale & Corrosion**: Prevention and mitigation strategies.

## When to Use

### Use This Skill When:
- Designing or optimizing production systems.
- Preparing for a **Surveillance Workshop**.
- Troubleshooting well performance issues (e.g., sudden rate drop).
- Evaluating EOR opportunities or managing existing EOR projects.
- Reviewing "Lessons Learnt" for brownfield asset management.

### Do Not Use This Skill When:
- Performing primary reservoir modeling (use Reservoir Engineering).
- Conducting heavy structural analysis (use Structural Analysis).
- Designing subsea hardware (use Subsea Engineering).

## Knowledge Areas

### 1. Surveillance Workshop Fundamentals
Surveillance workshops are the backbone of production optimization. They involve:
1.  **Data Gathering**: Aligning production logs, well tests, and downhole gauges.
2.  **Trend Analysis**: Identifying deviations from historical performance.
3.  **Action Planning**: Recommending workovers, stimulations, or setting changes.

### 2. EOR Lessons Learnt (Permian Basin)
- **Scale Issues**: High H2S and CO2 environments lead to complex scale (Iron Sulfide).
- **Water Quality**: EOR effectiveness is highly dependent on the quality of injected water.
- **Surveillance**: EOR requires tighter monitoring of patterns and injection profiles.

## Code & Data Patterns

### Nodal Analysis Concept
```python
def check_well_performance(measured_rate, predicted_rate, threshold=0.15):
    """
    Check if a well is underperforming based on nodal analysis predictions.
    """
    deviation = (predicted_rate - measured_rate) / predicted_rate
    if deviation > threshold:
        return "Action Required: Potential Scaling or Blockage"
    return "Status: Optimal"
```

### Voidage Replacement Ratio (VRR)
```python
def calculate_vrr(injection_volume, production_volume, b_factor):
    """
    Calculate VRR for waterflood surveillance.
    Ideal VRR is usually ~1.0.
    """
    return injection_volume / (production_volume * b_factor)
```

## Best Practices

- **Integrate Disciplines**: Combine data from drilling, reservoir, and facilities.
- **Document Failures**: Maintain a "Lessons Learnt" database for every asset.
- **Regular Workshops**: Conduct surveillance workshops quarterly to prevent production decline.
- **Safety First**: Prioritize well integrity and pressure containment in all operations.

## Resources & References

- **Legacy Docs**: `/mnt/ace/Production/` (Workshop PPTs and EOR evaluations).
- **Standards**: API RP 19 (Artificial Lift), ISO 15156 (Material Selection for H2S).
- **Digital Model**: `digitalmodel/reservoir/` for analytical performance calculations.
