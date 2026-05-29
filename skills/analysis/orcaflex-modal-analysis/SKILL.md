---
name: orcaflex-modal-analysis
description: Perform modal and frequency analysis on OrcaFlex models to extract natural
  frequencies, mode shapes, and identify dominant DOF responses. Use for VIV assessment,
  resonance identification, and structural dynamics characterization.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- modal analysis
- natural frequency
- mode shapes
- frequency analysis
- eigenvalue analysis
- resonance identification
- DOF analysis
- structural dynamics
---
# OrcaFlex Modal Analysis Skill

Extract natural frequencies, mode shapes, and dominant DOF responses from OrcaFlex models for structural dynamics characterization.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-17

**Added:**
- Initial release with modal analysis capabilities
- Mode shape extraction and visualization
- DOF-based mode filtering
- Multi-file batch processing

## When to Use

- Extract natural frequencies from OrcaFlex models
- Calculate mode shapes for risers, lines, and structures
- Identify dominant degrees of freedom in each mode
- Filter modes by specific DOF (heave, surge, pitch, etc.)
- VIV susceptibility screening (compare natural frequencies to shedding frequencies)
- Resonance identification for environmental loading
- Batch processing multiple water depths or configurations

## Prerequisites

- OrcaFlex license (for OrcFxAPI)
- Python environment with `digitalmodel` package installed
- Model files (.dat, .yml, or .sim)

## Analysis Workflow

### 1. Static Equilibrium → Modal Analysis

```
[Load Model] → [Calculate Statics] → [Modal Analysis Specification] → [Extract Modes]
      ↓                                        ↓
  .dat/.yml                              Configure:
                                         - lastMode (number of modes)
                                         - calculateShapes (mode shapes)
                                               ↓
                                     [Mode Details Extraction]
                                               ↓
                                     - Period/Frequency
                                     - Mode shapes (shapeWrtGlobal)
                                     - DOF percentages
```

## Configuration

### Basic Modal Analysis

```yaml
# configs/modal_analysis.yml

default:
  log_level: DEBUG

  Analysis:
    Analyze:
      flag: true
      simulation: false
      statics: false
      modal:
        flag: true
        lastMode: 20              # Number of modes to extract
        mode_shapes: true         # Save full mode shape data
        ObjectName:               # Objects to analyze
          - "Riser1"
          - "Mooring_Line_1"
        dof_analysis:
          dofs:                   # DOFs to filter by
            - "X"
            - "Y"
            - "Z"
            - "Rotation 1"
            - "Rotation 2"
            - "Rotation 3"
          threshold_percentages:  # Filter thresholds
            X: 10.0
            Y: 10.0
            Z: 10.0
            Rotation 1: 10.0
            Rotation 2: 10.0
            Rotation 3: 10.0

Files:
  - Label: "Depth_200m"
    Name: "models/riser_200m.yml"
  - Label: "Depth_500m"
    Name: "models/riser_500m.yml"
```

### Multi-Depth Study

```yaml
# configs/modal_depth_study.yml

default:
  Analysis:
    Analyze:
      modal:
        flag: true
        lastMode: 30
        ObjectName:
          - "SCR"
        dof_analysis:
          dofs: ["Z", "Rotation 1", "Rotation 2"]
          threshold_percentages:
            Z: 15.0
            Rotation 1: 10.0
            Rotation 2: 10.0

Files:
  - Label: "WD_800m"
    Name: "models/scr_wd_800m.yml"
  - Label: "WD_1000m"
    Name: "models/scr_wd_1000m.yml"
  - Label: "WD_1200m"
    Name: "models/scr_wd_1200m.yml"
  - Label: "WD_1500m"
    Name: "models/scr_wd_1500m.yml"
```

## Python API

### Basic Modal Analysis

```python
from digitalmodel.modules.orcaflex.orcaflex_modal_analysis import OrcModalAnalysis

# Initialize analyzer
modal = OrcModalAnalysis()

# Configure analysis
cfg = {
    "default": {
        "Analysis": {
            "Analyze": {
                "modal": {
                    "flag": True,
                    "lastMode": 20,
                    "mode_shapes": True,
                    "ObjectName": ["Riser1"],
                    "dof_analysis": {
                        "dofs": ["X", "Y", "Z"],
                        "threshold_percentages": {
                            "X": 10.0,
                            "Y": 10.0,
                            "Z": 10.0
                        }
                    }
                }
            },
            "result_folder": "results/",
            "file_name_for_overwrite": "modal_study"
        }
    },
    "Files": [
        {"Label": "Case1", "Name": "model.yml"}
    ]
}

# Run analysis
results = modal.run_modal_analysis(cfg)
```

### Direct OrcFxAPI Usage

```python
import OrcFxAPI

# Load model and calculate statics
model = OrcFxAPI.Model()
model.LoadData("model.yml")
model.CalculateStatics()

# Configure modal analysis
spec = OrcFxAPI.ModalAnalysisSpecification(
    calculateShapes=True,
    lastMode=20
)

# Run modal analysis
modes = OrcFxAPI.Modes(model, spec)

# Access results
print(f"Number of modes: {modes.modeCount}")
print(f"Number of DOFs: {modes.dofCount}")
print(f"Periods: {modes.period}")

# Iterate through modes
for modeIndex in range(modes.modeCount):
    details = modes.modeDetails(modeIndex)
    print(f"Mode {modeIndex + 1}:")
    print(f"  Period: {details.period:.3f} s")
    print(f"  Frequency: {1/details.period:.3f} Hz")

    # Access mode shapes for each DOF
    for dofIndex in range(modes.dofCount):
        name = modes.owner[dofIndex].name
        node = modes.nodeNumber[dofIndex]
        dof = modes.dof[dofIndex]
        shape = details.shapeWrtGlobal[dofIndex]

        if abs(shape) > 0.1:  # Filter significant shapes
            print(f"    {name} node {node} {dof}: {shape:.4f}")
```

### Extract Dominant DOFs

```python
from digitalmodel.modules.orcaflex.orcaflex_modal_analysis import OrcModalAnalysis
import pandas as pd

modal = OrcModalAnalysis()

# After running analysis, get summary
all_modes_summary_df = modal.all_file_summary["Case1"]

# Filter modes dominated by specific DOF
heave_modes = all_modes_summary_df[
    all_modes_summary_df['modes_selected'].apply(lambda x: x.get('Z', False))
]

print("Heave-dominated modes:")
for idx, row in heave_modes.iterrows():
    print(f"  Mode {row['modeIndex']}: Period = {row['period']:.3f}s")
```

## Output Files

### Mode Shapes CSV

```csv
modeIndex,name,node,dof,shapeWrtGlobal
0,Riser1,1,X,0.0012
0,Riser1,1,Y,0.0001
0,Riser1,1,Z,0.8523
0,Riser1,2,X,0.0015
...
```

### Mode Summary CSV

```csv
modeIndex,period,name,abs_max_dof,max_dof_values,max_dof_nodes,max_dof_percentages,modes_selected
0,8.523,Riser1,0.852,{'X': 0.001, 'Y': 0.0, 'Z': 0.852},{'X': 1, 'Y': 1, 'Z': 75},{'X': 0.1, 'Y': 0.0, 'Z': 99.8},{'X': False, 'Y': False, 'Z': True}
1,5.234,Riser1,0.723,{'X': 0.723, 'Y': 0.001, 'Z': 0.05},{'X': 50, 'Y': 1, 'Z': 1},{'X': 99.5, 'Y': 0.1, 'Z': 0.4},{'X': True, 'Y': False, 'Z': False}
```

### DOF-Filtered Summary

Output file: `{model_name}_modes_summary_{dof}.csv`

Contains only modes where the specified DOF exceeds the threshold percentage.

## Key Concepts

### DOF Percentage Calculation

For each mode, the DOF percentage indicates how much of the mode's energy is in each degree of freedom:

```
DOF_percentage = (|max_DOF_value|² / Σ|all_DOF_values|²) × 100
```

### Mode Selection Criteria

A mode is "selected" for a DOF when:
- `DOF_percentage > threshold_percentage`

This filtering helps identify:
- **Heave-dominated modes** (Z threshold)
- **Surge/sway modes** (X/Y threshold)
- **Roll/pitch/yaw modes** (Rotation thresholds)

### Relationship to VIV

Modal frequencies are critical for VIV assessment:

```python
# VIV lock-in check
from digitalmodel.modules.viv_analysis.viv_analysis import VIVAnalysis

viv = VIVAnalysis()

# Get natural frequency from modal analysis
natural_freq = 1 / mode_period  # Hz

# Calculate reduced velocity
current_velocity = 1.5  # m/s
diameter = 0.273  # m
reduced_velocity = viv.reduced_velocity(
    velocity=current_velocity,
    frequency=natural_freq,
    diameter=diameter
)

# Check lock-in
is_lock_in = viv.check_lock_in(reduced_velocity, vr_min=4.0, vr_max=8.0)
```

## Best Practices

### Model Preparation

1. **Ensure static convergence** before modal analysis
2. **Use appropriate segment lengths** for accurate mode shapes
3. **Include all relevant objects** in the analysis
4. **Consider boundary conditions** (fixed vs. free ends)

### Analysis Configuration

1. **Number of modes** - Start with 20-30 modes, increase if needed
2. **DOF thresholds** - Use 10-15% for initial screening
3. **Object selection** - Focus on critical structural members
4. **Batch processing** - Compare across configurations

### Results Interpretation

1. **Low-frequency modes** - Often global bending/heave
2. **High-frequency modes** - Local vibrations, may indicate VIV risk
3. **Mixed DOF modes** - Coupled motions, require careful assessment
4. **Clustering** - Multiple modes at similar frequencies indicate sensitivity

## Error Handling

### Static Analysis Failure

```python
try:
    model.CalculateStatics()
except OrcFxAPI.OrcaFlexError as e:
    print(f"Static analysis failed: {e}")
    print("Check:")
    print("  - Line connectivity")
    print("  - Environmental conditions")
    print("  - Initial tensions")
```

### Mode Extraction Issues

```python
try:
    modes = OrcFxAPI.Modes(model, spec)
except OrcFxAPI.OrcaFlexError as e:
    print(f"Modal analysis failed: {e}")
    print("Possible causes:")
    print("  - Singular stiffness matrix")
    print("  - Zero-tension lines")
    print("  - Disconnected components")
```

## Integration with Other Skills

### With VIV Analysis

```python
# 1. Run modal analysis to get natural frequencies
modal_results = modal.run_modal_analysis(cfg)

# 2. Use frequencies in VIV assessment
from digitalmodel.modules.viv_analysis.viv_analysis import VIVAnalysis
viv = VIVAnalysis()
viv_results = viv.screen_for_viv(natural_frequencies, current_profile)
```

### With OrcaFlex Post-Processing

```python
# After modal analysis, run dynamic simulation
# and extract time series at modal frequencies
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [viv-analysis](../viv-analysis/SKILL.md) - VIV susceptibility assessment
- [orcaflex-static-debug](../orcaflex-static-debug/SKILL.md) - Static convergence troubleshooting

## References

- OrcFxAPI Modal Analysis: Orcina Documentation
- DNV-RP-C205: Environmental Conditions and Environmental Loads
- API RP 2RD: Design of Risers for Floating Production Systems
- Source: `src/digitalmodel/modules/orcaflex/orcaflex_modal_analysis.py`
- Config: `src/digitalmodel/base_configs/modules/orcaflex/orcaflex_modal_analysis.yml`
