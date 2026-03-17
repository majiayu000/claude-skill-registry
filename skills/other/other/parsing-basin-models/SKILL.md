---
name: parsing-basin-models
description: |
  Parses HEC-HMS basin model files (.basin) to extract and modify subbasins, junctions,
  reaches, loss parameters, transform parameters, baseflow, and routing. Use when reading
  basin files, modifying hydrologic parameters, analyzing basin structure, or updating
  curve numbers, lag times, and routing coefficients. Handles clone workflows for QAQC.
  Trigger keywords: basin file, subbasin, junction, reach, loss method, curve number,
  transform, lag time, baseflow, routing, Muskingum, parse basin, get parameters.
---

# Parsing Basin Models

## Quick Start

```python
from hms_commander import HmsBasin

# Read basin components
subbasins = HmsBasin.get_subbasins("project.basin")
junctions = HmsBasin.get_junctions("project.basin")
reaches = HmsBasin.get_reaches("project.basin")

# Get/set parameters
loss_params = HmsBasin.get_loss_parameters("project.basin", "Subbasin1")
HmsBasin.set_loss_parameters("project.basin", "Subbasin1", curve_number=85)
```

## Primary Sources

**Code**: `hms_commander/HmsBasin.py` - Complete API with docstrings

**Examples**: `examples/03_project_dataframes.ipynb` - Basin operations

**Rules**: `.claude/rules/hec-hms/basin-files.md` - Basin file patterns

**File Format**: `tests/projects/.../02_Basin_File.md` - HMS file structure

## When to Use This Skill

- Extracting basin components for analysis
- Modifying loss method parameters (CN, deficit, constant rate)
- Updating transform parameters (lag time, time of concentration)
- Analyzing basin connectivity (downstream relationships)
- Cloning basins for QAQC comparison

## Core Capabilities

### 1. Component Extraction

Returns DataFrames with basin elements:
- `get_subbasins()` - Area, downstream, loss/transform methods
- `get_junctions()` - Connectivity nodes
- `get_reaches()` - Channel routing elements

### 2. Parameter Operations

Get/set hydrologic parameters:
- Loss methods (Deficit & Constant, SCS CN, Green & Ampt, etc.)
- Transform methods (SCS UH, Clark UH, ModClark, etc.)
- Baseflow methods (Recession, Constant Monthly, etc.)
- Routing methods (Muskingum, Lag, ModPuls, etc.)

**See**: `hms_commander/HmsBasin.py` for complete method list

### 3. Clone Workflows

Non-destructive basin cloning:
- Preserves original basin
- Updates description with clone metadata
- Appears in HEC-HMS GUI
- Enables side-by-side QAQC comparison

**See**: `.claude/rules/hec-hms/clone-workflows.md` for CLB Engineering pattern

## Common Workflows

### Workflow 1: Extract All Components

```python
subbasins = HmsBasin.get_subbasins("project.basin")
print(f"Found {len(subbasins)} subbasins")
print(f"Total area: {subbasins['Area'].sum()} sq mi")
```

### Workflow 2: Bulk Parameter Update

```python
# Update all curve numbers
subbasins = HmsBasin.get_subbasins("project.basin")
for name in subbasins.index:
    HmsBasin.set_loss_parameters("project.basin", name, curve_number=85)
```

### Workflow 3: Clone for QAQC

```python
from hms_commander import init_hms_project, hms, HmsBasin

init_hms_project("project")
HmsBasin.clone_basin("Baseline", "Updated_Basin", hms_object=hms)
# Now modify Updated_Basin parameters for comparison
```

## Reference Files

- `reference/get_subbasins.md` - DataFrame structure and usage
- `reference/loss_methods.md` - All loss method parameters
- `reference/transform_methods.md` - All transform method parameters
- `examples/parameter_sweep.md` - Bulk parameter updates

## Related Skills

- **cloning-hms-components** - Complete clone workflow
- **executing-hms-runs** - Run after modifying parameters
