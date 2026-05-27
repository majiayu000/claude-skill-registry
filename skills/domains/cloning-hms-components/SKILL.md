---
name: cloning-hms-components
description: |
  Clones HEC-HMS components (basins, met models, control specs, runs) using the
  CLB Engineering LLM Forward approach. Creates non-destructive, traceable, GUI-verifiable
  copies for QAQC comparison, scenario analysis, and parameter sensitivity testing.
  Use when creating alternative scenarios, setting up QAQC workflows, comparing baseline
  vs updated models, or preserving original while testing modifications. All clones
  appear in HEC-HMS GUI with separate DSS outputs for side-by-side comparison.
  Trigger keywords: clone, duplicate, copy, QAQC, scenario, alternative, baseline,
  comparison, side-by-side, non-destructive, traceable.
---

# Cloning HMS Components

## Quick Start

```python
from hms_commander import init_hms_project, hms
from hms_commander import HmsBasin, HmsMet, HmsControl, HmsRun

init_hms_project("project")

# Clone components
HmsBasin.clone_basin("Baseline", "Updated_Basin", hms_object=hms)
HmsMet.clone_met("Baseline_Met", "Atlas14_Met", hms_object=hms)
HmsControl.clone_control("Jan2020", "Jun2020", hms_object=hms)
HmsRun.clone_run("Run_Baseline", "Run_Updated", hms_object=hms)
```

## Primary Sources

**Code**:
- `hms_commander/HmsBasin.py#clone_basin()`
- `hms_commander/HmsMet.py#clone_met()`
- `hms_commander/HmsControl.py#clone_control()`
- `hms_commander/HmsRun.py#clone_run()`

**Rules**: `.claude/rules/hec-hms/clone-workflows.md` - CLB Engineering approach

**Examples**: `examples/clone_workflow.ipynb` - Complete QAQC workflow

## When to Use This Skill

- Setting up QAQC comparison workflows (baseline vs updated)
- Creating scenario alternatives without modifying originals
- Parameter sensitivity testing (multiple variations)
- Preserving working models before experiments
- Atlas 14 precipitation updates (keep TP40 baseline)
- Model calibration (test different parameter sets)

## CLB Engineering LLM Forward Approach

**Three Principles**:

1. **Non-Destructive**: Preserves original components
2. **Traceable**: Updates description with clone metadata
3. **GUI-Verifiable**: Clones appear in HEC-HMS GUI immediately

**Why This Matters**:

QAQC workflows require side-by-side comparison in the HMS GUI:
- Baseline run → Baseline DSS file
- Updated run → Updated DSS file
- Compare hydrographs visually in HMS
- Verify changes are intentional

**See**: `.claude/rules/hec-hms/clone-workflows.md` for complete pattern

## Core Capabilities

### 1. Basin Cloning

```python
HmsBasin.clone_basin(
    template="Baseline",
    new_name="Updated_Basin",
    description="Updated with Atlas 14 precip",
    hms_object=hms
)
```

**Result**:
- New .basin file created
- Description includes clone metadata
- Appears in HMS GUI's Basin Manager
- All parameters copied from template

### 2. Met Model Cloning

```python
HmsMet.clone_met(
    template="TP40_Met",
    new_name="Atlas14_Met",
    description="Updated to Atlas 14 depths",
    hms_object=hms
)
```

**Result**:
- New .met file created
- Gage assignments preserved
- Ready for precipitation updates

### 3. Control Specification Cloning

```python
HmsControl.clone_control(
    template="Jan2020",
    new_name="Jun2020",
    hms_object=hms
)
```

**Use case**: Same model, different time periods

### 4. Run Cloning (Critical for QAQC)

```python
HmsRun.clone_run(
    source_run="Baseline",
    new_run_name="Updated",
    new_basin="Updated_Basin",
    new_met="Atlas14_Met",
    output_dss="results_updated.dss",
    description="Atlas 14 update QAQC",
    hms_object=hms
)
```

**Result**:
- New run configuration
- Points to cloned basin/met
- Separate DSS file (critical for comparison!)
- Appears in HMS Compute menu

## Common Workflows

### Workflow 1: Atlas 14 Update QAQC

```python
init_hms_project("project")

# 1. Clone met model
HmsMet.clone_met("Baseline_Met", "Atlas14_Met", hms_object=hms)

# 2. Update Atlas 14 depths
new_depths = [2.8, 3.5, 4.2, 4.9, 5.7, 6.5]
HmsMet.set_precipitation_depths("project/Atlas14_Met.met", new_depths)

# 3. Clone run with new met
HmsRun.clone_run(
    source_run="Baseline",
    new_run_name="Atlas14_Update",
    new_met="Atlas14_Met",
    output_dss="results_atlas14.dss",
    hms_object=hms
)

# 4. Execute both runs
HmsCmdr.compute_parallel(["Baseline", "Atlas14_Update"])

# 5. Compare in HMS GUI
# Open both DSS files side-by-side
```

### Workflow 2: Parameter Sensitivity

```python
# Test multiple curve numbers
for cn in [70, 75, 80, 85, 90]:
    # Clone basin
    HmsBasin.clone_basin("Baseline", f"CN{cn}", hms_object=hms)

    # Update curve number
    HmsBasin.set_loss_parameters(f"project/CN{cn}.basin", "Sub1", curve_number=cn)

    # Clone run
    HmsRun.clone_run(
        "Baseline_Run",
        f"Run_CN{cn}",
        new_basin=f"CN{cn}",
        output_dss=f"results_cn{cn}.dss",
        hms_object=hms
    )

# Execute all runs in parallel
HmsCmdr.compute_parallel([f"Run_CN{cn}" for cn in [70, 75, 80, 85, 90]])
```

### Workflow 3: Scenario Comparison

```python
scenarios = ["Baseline", "Alternative_1", "Alternative_2"]

for scenario in scenarios[1:]:  # Skip baseline
    # Clone all components
    HmsBasin.clone_basin("Baseline", f"{scenario}_Basin", hms_object=hms)
    HmsMet.clone_met("Baseline_Met", f"{scenario}_Met", hms_object=hms)
    HmsRun.clone_run(
        "Baseline_Run",
        f"Run_{scenario}",
        new_basin=f"{scenario}_Basin",
        new_met=f"{scenario}_Met",
        output_dss=f"results_{scenario}.dss",
        hms_object=hms
    )

    # Modify scenario-specific parameters
    # ...
```

## Reference Files

- `reference/clone_basin.md` - Complete HmsBasin.clone_basin() API
- `reference/clone_met.md` - Complete HmsMet.clone_met() API
- `reference/clone_run.md` - Complete HmsRun.clone_run() API
- `examples/qaqc_workflow.md` - Complete QAQC setup

## Related Skills

- **parsing-basin-models** - Modify cloned basins
- **updating-met-models** - Modify cloned met models
- **executing-hms-runs** - Run cloned scenarios
- **extracting-dss-results** - Compare results from clones
