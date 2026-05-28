---
name: orcaflex-installation-analysis
description: Create and analyze OrcaFlex models for offshore installation sequences
  including subsea structure lowering, pipeline installation, and crane operations.
  Generate models at multiple water depths and orientations for installation feasibility
  studies.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- installation analysis
- subsea installation
- structure lowering
- crane operation
- installation sequence
- depth variation
- installation feasibility
- heavy lift
- payload handling
---
# OrcaFlex Installation Analysis Skill

Generate and analyze OrcaFlex models for offshore installation sequences with automated depth variation and orientation studies.

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
- Initial release with installation sequence capabilities
- Multi-depth model generation
- Orientation variation support
- Crane wire length adjustment

## When to Use

- Subsea structure installation analysis
- Pipeline/umbilical installation sequences
- Heavy lift crane operations
- Installation depth variation studies
- Lowering phase analysis
- Splash zone analysis
- Installation feasibility assessment
- Crane wire and sling configuration

## Prerequisites

- OrcaFlex license (for simulation)
- Python environment with `digitalmodel` package installed
- Reference model files (.yml format recommended)
- Reference elevation configuration

## Installation Sequence Workflow

```
[Reference Model] → [Define Delta Elevations] → [Generate Depth Models]
        ↓                    ↓                           ↓
   Base geometry      [-10m, -20m, -30m, ...]    Model per depth:
   at datum                                       - Update structure Z
                                                  - Update buoy Z
                                                  - Extend crane wire
                                                  - Update sling connections
                                                           ↓
                                               [Orientation Variants]
                                                           ↓
                                               [Batch Simulation]
```

## Configuration

### Basic Installation Depth Study

```yaml
# configs/installation_config.yml

structure:
  BaseFile: "reference_model.yml"
  reference_model_file: "models/installation_reference.yml"
  reference_elevation_file: "models/elevation_reference.yml"

  # Objects to update
  6DBuoys:
    - "Subsea_Structure"
  3DBuoys:
    - "Masterlink"

  # Lines to extend
  Lines:
    - name: "Crane_Wire"
      EndBZ: true           # Update end B Z coordinate
      length_index: 2       # Section index to extend
      TargetSegmentLength: 5.0
    - name: "Intermediate_Sling"
      EndBZ: true

  # Depth increments from reference
  delta_elevations:
    - 0      # Reference position
    - -10    # 10m below reference
    - -20    # 20m below reference
    - -30    # 30m below reference
    - -50    # 50m below reference
    - -75    # 75m below reference
    - -100   # 100m below reference

Analysis:
  analysis_root_folder: "results/installation/"
```

### Heavy Lift Configuration

```yaml
# configs/heavy_lift_config.yml

reference_elevation_file: "models/heavy_lift_reference.yml"

# Key components
structure: "Topside_Module"
masterlink: "Lifting_Padeye"
crane_wire: "Main_Crane_Wire"
intermediate_sling: "Spreader_Sling"

# Output naming
output_basefile: "topside_installation"

# Installation depths (negative = below reference)
delta_elevations:
  - 0      # At deck level
  - -5     # Splash zone entry
  - -10    # Through splash zone
  - -15    # Below splash zone
  - -20    # Mid-water
  - -30    # Approaching seabed
  - -40    # Near seabed
  - -45    # Final position
```

## Python API

### Generate Installation Depth Models

```python
from digitalmodel.modules.orcaflex.orcaflex_installation import OrcInstallation

# Initialize
installer = OrcInstallation()

# Configuration for depth variation
cfg = {
    "structure": {
        "BaseFile": "reference.yml",
        "reference_model_file": "models/reference_model.yml",
        "reference_elevation_file": "models/elevations.yml",
        "6DBuoys": ["Structure"],
        "3DBuoys": ["Masterlink"],
        "Lines": [
            {
                "name": "Crane_Wire",
                "EndBZ": True,
                "length_index": 1,
                "TargetSegmentLength": 5.0
            }
        ],
        "delta_elevations": [0, -10, -20, -30, -50, -75, -100]
    },
    "Analysis": {
        "analysis_root_folder": "results/"
    }
}

# Generate models for all depths
installer.create_model_for_water_depth(cfg)
```

### Simple Depth Model Generation

```python
from digitalmodel.modules.orcaflex.orcaflex_installation import OrcInstallation

installer = OrcInstallation()

# Simpler configuration
cfg = {
    "reference_elevation_file": "models/reference.yml",
    "structure": "Subsea_Template",
    "masterlink": "Lifting_Point",
    "crane_wire": "Main_Wire",
    "intermediate_sling": None,  # Optional
    "output_basefile": "template_installation",
    "delta_elevations": [0, -10, -20, -30, -40, -50]
}

# Generate depth models
installer.create_installation_depth_model(cfg)
```

### With Structure Orientation

```python
from digitalmodel.modules.orcaflex.orcaflex_installation import OrcInstallation

installer = OrcInstallation()

# This generates:
# 1. Base model at each depth
# 2. Orientation variant (rotation about Z)
cfg = {
    "structure": {
        "BaseFile": "reference.yml",
        "reference_model_file": "models/reference.yml",
        "reference_elevation_file": "models/elevations.yml",
        "6DBuoys": ["Mudmat"],
        "3DBuoys": [],
        "Lines": [
            {"name": "Wire1", "EndBZ": True, "length_index": 0}
        ],
        "delta_elevations": [0, -5, -10, -15, -20]
    },
    "Analysis": {
        "analysis_root_folder": "results/mudmat/"
    }
}

# Generates files:
# - _el_00000m.yml (reference)
# - _el_00000m_str_orientation.yml (with Rotation3 = 0)
# - el_00000m.yml (final model)
# - _el_-0010m.yml
# - ... etc for each depth

installer.create_model_for_water_depth(cfg)
```

## Output File Structure

```
results/installation/
├── _el_00000m.yml              # Reference depth, base orientation
├── _el_00000m_str_orentation.yml   # Reference depth, zero rotation
├── el_00000m.yml               # Final reference model
├── _el_-0010m.yml              # 10m below reference
├── _el_-0010m_str_orentation.yml
├── el_-0010m.yml
├── _el_-0020m.yml              # 20m below reference
├── _el_-0020m_str_orentation.yml
├── el_-0020m.yml
└── ...
```

## Key Concepts

### Reference Elevation File

Contains the initial Z positions for all objects:

```yaml
# models/elevation_reference.yml

6DBuoys:
  Subsea_Structure:
    InitialZ: -50.0      # Initial elevation
    InitialRotation3: 45  # Initial rotation (deg)

3DBuoys:
  Masterlink:
    InitialZ: -45.0

Lines:
  Crane_Wire:
    EndBZ: -45.0
    Sections:
      - Length: 10.0
      - Length: 50.0      # Section to extend
      - Length: 5.0
```

### Delta Elevation Application

For each `delta_elevation`:
1. **6DBuoys**: `NewZ = ReferenceZ + delta_elevation`
2. **3DBuoys**: `NewZ = ReferenceZ + delta_elevation`
3. **Line EndBZ**: `NewEndBZ = ReferenceEndBZ + delta_elevation`
4. **Line Length**: `NewLength = ReferenceLength + |delta_elevation|`

### Crane Wire Extension

As structure lowers, crane wire extends:

```python
# For each delta_elevation
new_wire_length = reference_length + abs(delta_elevation)
```

## Integration with Universal Runner

After generating installation models, run batch simulations:

```python
from digitalmodel.modules.orcaflex.universal import UniversalOrcaFlexRunner

# Initialize runner
runner = UniversalOrcaFlexRunner(
    input_directory="results/installation/",
    output_directory="results/installation/.sim/",
    mock_mode=False
)

# Run all installation models
results = runner.run_batch(
    pattern="el_*.yml",
    parallel=True,
    max_workers=4
)

# Check results
for file_name, status in results.items():
    print(f"{file_name}: {'SUCCESS' if status['success'] else 'FAILED'}")
```

## Analysis Types

### 1. Splash Zone Analysis

Focus on depths around waterline:

```yaml
delta_elevations:
  - 5     # Above water
  - 2     # Near waterline
  - 0     # At waterline
  - -2    # Just below
  - -5    # Submerged
  - -10   # Below splash zone
```

### 2. Full Lowering Sequence

Complete installation from deck to seabed:

```yaml
delta_elevations:
  - 0     # At deck
  - -5    # Clear of vessel
  - -10   # Splash zone entry
  - -15   # Through splash zone
  - -20   # Mid-water (upper)
  - -30   # Mid-water
  - -50   # Mid-water (lower)
  - -75   # Approaching seabed
  - -95   # Near seabed
  - -100  # At seabed
```

### 3. Landing Sequence

Fine resolution near seabed:

```yaml
# Reference at 5m above seabed
delta_elevations:
  - 0     # 5m above seabed
  - -1    # 4m above
  - -2    # 3m above
  - -3    # 2m above
  - -4    # 1m above
  - -4.5  # 0.5m above (touchdown)
  - -5    # On seabed
```

## Post-Processing Installation Results

```python
from digitalmodel.modules.orcaflex.opp import OrcaFlexPostProcess

opp = OrcaFlexPostProcess()

# Extract crane wire tensions at each depth
cfg = {
    "orcaflex": {
        "postprocess": {
            "summary": {
                "flag": True,
                "variables": [
                    {"object": "Crane_Wire", "variable_name": "Effective Tension"},
                    {"object": "Structure", "variable_name": "Z"}
                ]
            }
        }
    }
}

# Process all simulation files
sim_files = list(Path("results/installation/.sim/").glob("*.sim"))
for sim_file in sim_files:
    results = opp.process_single_file(sim_file, cfg)
    depth = extract_depth_from_filename(sim_file.stem)
    print(f"Depth {depth}m: Max tension = {results['max_tension']:.1f} kN")
```

## Best Practices

### Model Preparation

1. **Reference model at datum** - Start with well-converged static model
2. **Appropriate segment lengths** - Finer segments for crane wire
3. **Buoyancy and mass** - Verify structure properties
4. **Crane capacity** - Check against maximum tensions

### Depth Increments

1. **Fine resolution at splash zone** - Wave loading peaks here
2. **Coarse mid-water** - Quasi-static behavior
3. **Fine at seabed** - Landing dynamics critical

### Output Validation

1. **Check crane wire tensions** - Must be within capacity
2. **Verify structure orientation** - No unexpected rotations
3. **Validate connections** - All links maintained
4. **Review static convergence** - Each depth should converge

## Error Handling

### Common Issues

```python
# File not found
try:
    installer.create_model_for_water_depth(cfg)
except FileNotFoundError as e:
    print(f"Reference file not found: {e}")
    print("Check: reference_model_file and reference_elevation_file paths")

# Invalid line section index
# Error: "Key not found in line item"
# Fix: Verify length_index matches actual line sections

# Convergence failure at depth
# Check: Environmental loads, line lengths, tensions
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Extract results
- [orcaflex-static-debug](../orcaflex-static-debug/SKILL.md) - Debug convergence issues
- [orcaflex-line-wizard](../orcaflex-line-wizard/SKILL.md) - Configure line properties

## References

- OrcaFlex Installation Analysis: Orcina Documentation
- DNV-RP-H103: Modelling and Analysis of Marine Operations
- API RP 2A: Planning, Designing and Constructing Fixed Offshore Platforms
- Source: `src/digitalmodel/modules/orcaflex/orcaflex_installation.py`
