---
name: updating-met-models
description: |
  Updates HEC-HMS meteorologic model files (.met) including precipitation methods,
  gage assignments, evapotranspiration, and Atlas 14 frequency storms. Use when
  configuring precipitation, assigning gages to subbasins, updating TP40 to Atlas 14,
  or modifying ET methods. Handles clone workflows for QAQC comparison.
  Trigger keywords: met model, precipitation, gage assignment, Atlas 14, TP40,
  frequency storm, evapotranspiration, ET, meteorologic model, update precip.
---

# Updating Meteorologic Models

## Quick Start

```python
from hms_commander import HmsMet

# Read met configuration
precip_method = HmsMet.get_precipitation_method("project.met")
gage_assignments = HmsMet.get_gage_assignments("project.met")

# Update gage assignments
HmsMet.set_gage_assignment("project.met", "Subbasin1", "Gage1")

# Update Atlas 14 depths
new_depths = [2.5, 3.1, 3.8, 4.5, 5.2, 6.0]  # 6-hour storm depths
HmsMet.set_precipitation_depths("project.met", new_depths)
```

## Primary Sources

**Code**: `hms_commander/HmsMet.py` - Complete API

**Task Agent**: `hms_agents/hms_atlas14/` - Automated Atlas 14 updates

**Rules**: `.claude/rules/hec-hms/met-files.md` - Met file patterns

**Examples**: `examples/04_hms_workflow.ipynb` cells 8-12 - Met operations

## When to Use This Skill

- Configuring precipitation methods (Gage weights, Gridded, Frequency storm)
- Assigning gages to subbasins
- Updating TP40 to Atlas 14 precipitation depths
- Modifying evapotranspiration methods
- Cloning met models for scenario comparison

## Core Capabilities

### 1. Precipitation Configuration

Supported methods:
- Specified Hyetograph
- Gage Weights
- Gridded Precipitation
- Frequency Storm (TP40, Atlas 14)
- SCS Storm
- Standard Project Storm

### 2. Gage Assignment

Map gages to subbasins:
```python
assignments = HmsMet.get_gage_assignments("project.met")
# Returns DataFrame: Subbasin → Gage mapping
```

### 3. Atlas 14 Integration

Update frequency storm depths:
```python
# Get current depths
depths = HmsMet.get_precipitation_depths("project.met")

# Update with Atlas 14 (from NOAA API or manual)
atlas14_depths = [2.8, 3.5, 4.2, 4.9, 5.7, 6.5]
HmsMet.set_precipitation_depths("project.met", atlas14_depths)
```

**See**: `hms_agents/hms_atlas14/` for automated workflow

### 4. Clone Workflows

```python
from hms_commander import init_hms_project, hms, HmsMet

init_hms_project("project")
HmsMet.clone_met("Baseline_Met", "Atlas14_Met", hms_object=hms)
# Update Atlas14_Met with new precipitation depths
```

## Common Workflows

### Workflow 1: Atlas 14 Update

**Automated approach** (Recommended):
```python
# Use hms_atlas14 task agent
# See: hms_agents/hms_atlas14/README.md
```

**Manual approach**:
```python
# 1. Get project centroid
from hms_commander import HmsGeo
lat, lon = HmsGeo.get_project_centroid_latlon("project.geo")

# 2. Download Atlas 14 from NOAA API (requires manual step)

# 3. Update met file
HmsMet.set_precipitation_depths("project.met", atlas14_depths)
```

### Workflow 2: Gage Weight Configuration

```python
# Assign gages to all subbasins
subbasins = ["Sub1", "Sub2", "Sub3"]
gages = ["Gage1", "Gage1", "Gage2"]

for sub, gage in zip(subbasins, gages):
    HmsMet.set_gage_assignment("project.met", sub, gage)
```

## Reference Files

- `reference/precipitation_methods.md` - All precip method details
- `reference/atlas14.md` - Atlas 14 integration guide
- `examples/atlas14_update.md` - Complete Atlas 14 workflow

## Related Skills

- **executing-hms-runs** - Run after updating precipitation
- **cloning-hms-components** - Clone met for scenario comparison
