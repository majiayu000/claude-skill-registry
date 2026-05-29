---
name: yaml-configuration
version: 1.0.0
description: YAML for configuration-driven engineering workflows, model setup, and analysis parameters
author: workspace-hub
category: programming
tags: [yaml, configuration, engineering, orcaflex, automation, data-structures]
platforms: [yaml, python]
---

# YAML Configuration Management Skill

Master YAML for configuration-driven engineering workflows, enabling reproducible analyses and automated model generation.

## When to Use This Skill

Use YAML configuration when you need:
- **Configuration-driven workflows** - Separate data from code
- **Reproducible analyses** - Version-controlled parameters
- **Model templates** - Reusable configurations
- **Complex nested structures** - Hierarchical data organization
- **Human-readable configs** - Easy to review and modify
- **Automated model generation** - OrcaFlex, FEA, CAD models

**Avoid when:**
- Binary data needed (use pickle, HDF5)
- Extremely large datasets (use CSV, databases)
- Real-time performance critical (use JSON)

## Core Capabilities

### 1. Basic YAML Syntax

**Scalars:**
```yaml
# Strings
project_name: "FPSO Mooring Analysis"
description: Simple mooring system

# Numbers
water_depth: 1500        # Integer
wave_height: 8.5         # Float
scientific: 1.5e-3       # Scientific notation

# Booleans
include_current: true
dynamic_analysis: false

# Null values
optional_parameter: null
# or
optional_parameter: ~
```

**Lists:**
```yaml
# Inline list
mooring_lines: [1, 2, 3, 4, 5, 6]

# Block list
vessel_types:
  - FPSO
  - Semi-submersible
  - TLP
  - SPAR

# List of dictionaries
load_cases:
  - name: "Operating"
    Hs: 4.5
    Tp: 10.0
  - name: "Storm"
    Hs: 8.5
    Tp: 12.0
```

**Dictionaries:**
```yaml
# Nested dictionaries
vessel:
  name: "FPSO Vessel"
  dimensions:
    length: 320
    beam: 58
    draft: 22
  mass_properties:
    displacement: 150000
    lcg: 160
    vcg: 15
```

### 2. Advanced Features

**Anchors and Aliases (Reuse):**
```yaml
# Define anchor
default_material: &steel
  name: "Steel"
  density: 7850
  youngs_modulus: 200e9

# Reuse with alias
chain_material: *steel

mooring_line:
  material: *steel  # References same data

# Merge keys
base_config: &base
  version: 1.0
  author: "Engineering Team"

analysis_1:
  <<: *base  # Merge base_config
  name: "Analysis 1"
  parameters:
    duration: 3600

analysis_2:
  <<: *base  # Merge base_config
  name: "Analysis 2"
  parameters:
    duration: 7200
```

**Multi-line Strings:**
```yaml
# Preserve newlines (literal style)
description: |
  This is a multi-line string.
  Newlines are preserved.
  Use for comments or descriptions.

# Fold newlines (folded style)
notes: >
  This string will have
  newlines replaced with spaces,
  except for blank lines.

  This starts a new paragraph.
```

**Comments:**
```yaml
# This is a comment
project: "Mooring Analysis"  # Inline comment

# Comments for documentation
vessel:
  # Main dimensions
  length: 320  # meters
  beam: 58     # meters
```

## Complete Examples

### Example 1: OrcaFlex Mooring Configuration

```yaml
# config/mooring_analysis.yaml
---
metadata:
  analysis_name: "FPSO Mooring System"
  analysis_type: "dynamic_mooring"
  created: "2026-01-06"
  author: "Marine Engineering Team"
  version: 1.0

environment:
  water_depth: 1500  # meters
  wave:
    type: "JONSWAP"
    Hs: 8.5  # meters
    Tp: 12.0  # seconds
    gamma: 3.3
    direction: 0  # degrees
  current:
    surface_speed: 1.2  # m/s
    direction: 0  # degrees
    profile: "linear"  # or "power_law"
  wind:
    speed: 25  # m/s
    direction: 0  # degrees

vessel:
  name: "FPSO_Model"
  type: "Vessel"
  dimensions:
    length: 320  # meters
    beam: 58
    draft: 22
  mass_properties:
    mass: 150000  # tonnes
    lcg: 160  # from aft perpendicular
    vcg: 15  # from keel
    radii_of_gyration:
      roll: 22
      pitch: 95
      yaw: 95

mooring_system:
  configuration: "spread"  # or "turret"
  number_of_lines: 12
  lines:
    - name: "Line_1"
      type: "chain_wire_chain"
      azimuth: 0  # degrees
      segments:
        - type: "chain"
          length: 500
          diameter: 127  # mm
          grade: "R4"
        - type: "wire"
          length: 1000
          diameter: 120  # mm
        - type: "chain"
          length: 500
          diameter: 127  # mm
      anchor:
        type: "drag_embedment"
        capacity: 5000  # kN
    - name: "Line_2"
      type: "chain_wire_chain"
      azimuth: 30
      # ... similar structure

  pretension:
    method: "automatic"  # or "manual"
    target: 2000  # kN

analysis_parameters:
  static:
    tolerance: 0.001
    max_iterations: 100
  dynamic:
    duration: 10800  # seconds (3 hours)
    time_step: 0.05  # seconds
    ramp_time: 300  # seconds
    output_interval: 1.0  # seconds

output:
  format: "html"  # or "csv", "excel"
  include_plots: true
  statistics: ["max", "min", "mean", "std"]
  results:
    - "vessel_motions"
    - "mooring_tensions"
    - "anchor_loads"
```

### Example 2: Hydrodynamic Analysis Configuration

```yaml
# config/hydrodynamic_analysis.yaml
---
analysis:
  type: "frequency_domain"
  software: "AQWA"  # or "WAMIT", "OrcaWave"

geometry:
  input_file: "../models/vessel_geometry.gdf"
  mesh:
    element_size: 2.0  # meters
    refinement_zones:
      - location: "bow"
        size: 0.5
      - location: "stern"
        size: 0.5

wave_directions:
  start: 0
  end: 180
  step: 15  # degrees

wave_frequencies:
  min: 0.1  # rad/s
  max: 2.0
  number: 40
  spacing: "logarithmic"  # or "linear"

mass_properties:
  displacement: 150000  # tonnes
  center_of_gravity:
    x: 160  # from origin
    y: 0
    z: 15
  radii_of_gyration:
    Rxx: 22  # roll
    Ryy: 95  # pitch
    Rzz: 95  # yaw

water_depth: 1500  # meters, or "infinite"

output:
  added_mass: true
  damping: true
  wave_excitation: true
  raos: true
  drift_forces: true
  qtf: false  # Quadratic Transfer Functions (slow)

  export_formats:
    - "txt"
    - "csv"
    - "yml"

  plots:
    - "added_mass_vs_frequency"
    - "damping_vs_frequency"
    - "rao_amplitude_vs_frequency"
    - "rao_phase_vs_frequency"
```

### Example 3: Fatigue Analysis Configuration

```yaml
# config/fatigue_analysis.yaml
---
analysis:
  name: "Mooring Line Fatigue Assessment"
  type: "spectral_fatigue"
  standard: "DNV-RP-C203"

input_data:
  tension_rao:
    file: "../results/mooring_rao.csv"
    format: "csv"
    columns:
      frequency: "freq_rad_s"
      amplitude: "tension_amplitude_kN"

  wave_scatter:
    file: "../data/wave_scatter_diagram.yml"
    annual_probability: true

material:
  type: "chain"
  grade: "R4"
  diameter: 127  # mm
  sn_curve:
    class: "F3"  # DNV classification
    m: 3.0  # S-N curve slope
    a: 1.52e12  # S-N curve constant
    thickness_exponent: 0.25

stress_concentration:
  factor: 1.2  # SCF
  location: "connector"

analysis_parameters:
  short_term:
    duration: 3  # hours
    bins: 100

  long_term:
    design_life: 25  # years
    damage_limit: 1.0

output:
  damage_per_sea_state: true
  annual_damage: true
  fatigue_life: true
  utilization: true

  plots:
    - "damage_vs_hs_tp"
    - "cumulative_damage"
    - "rainflow_histogram"

  export:
    format: ["html", "csv"]
    include_raw_data: false
```

### Example 4: Multi-Analysis Workflow

```yaml
# config/workflow_config.yaml
---
workflow:
  name: "Complete Mooring Analysis Workflow"
  version: 1.0

stages:
  - stage: 1
    name: "Hydrodynamic Analysis"
    config: "../config/hydrodynamic_analysis.yaml"
    outputs:
      - "../results/added_mass.csv"
      - "../results/damping.csv"
      - "../results/raos.csv"

  - stage: 2
    name: "Mooring Static Analysis"
    config: "../config/mooring_static.yaml"
    inputs:
      - "../results/vessel_properties.yml"
    outputs:
      - "../results/mooring_configuration.yml"
      - "../results/static_tensions.csv"

  - stage: 3
    name: "Mooring Dynamic Analysis"
    config: "../config/mooring_dynamic.yaml"
    dependencies: [1, 2]  # Requires stages 1 and 2
    inputs:
      - "../results/raos.csv"
      - "../results/mooring_configuration.yml"
    outputs:
      - "../results/dynamic_tensions.csv"
      - "../reports/mooring_report.html"

  - stage: 4
    name: "Fatigue Assessment"
    config: "../config/fatigue_analysis.yaml"
    dependencies: [3]
    inputs:
      - "../results/dynamic_tensions.csv"
    outputs:
      - "../results/fatigue_damage.csv"
      - "../reports/fatigue_report.html"

execution:
  parallel: false  # Run stages sequentially
  stop_on_error: true
  save_intermediate: true
```

### Example 5: Vessel Library

```yaml
# config/vessel_library.yaml
---
# Vessel templates library

vessels:
  fpso_standard: &fpso
    type: "FPSO"
    dimensions:
      length: 320
      beam: 58
      draft: 22
    mass: 150000
    mooring: "spread"

  semi_sub_standard: &semi
    type: "Semi-submersible"
    dimensions:
      length: 110
      beam: 78
      draft: 25
    mass: 45000
    mooring: "tendon"

  spar_standard: &spar
    type: "SPAR"
    dimensions:
      length: 200  # height
      diameter: 40
      draft: 180
    mass: 30000
    mooring: "taut"

# Use templates in specific projects
project_1:
  vessel:
    <<: *fpso
    name: "Project_1_FPSO"
    custom_modifications:
      draft: 24  # Override default

project_2:
  vessel:
    <<: *semi
    name: "Project_2_SemiSub"
```

### Example 6: Parameter Variations

```yaml
# config/parametric_study.yaml
---
parametric_study:
  name: "Mooring Pretension Sensitivity"
  base_config: "../config/mooring_analysis.yaml"

  parameters:
    - name: "pretension"
      type: "linear"
      min: 1000
      max: 3000
      steps: 11
      unit: "kN"

    - name: "water_depth"
      type: "list"
      values: [1000, 1500, 2000, 2500]
      unit: "m"

  combinations: "full_factorial"  # or "latin_hypercube"

  output:
    summary_table: true
    plots:
      - type: "line"
        x: "pretension"
        y: "max_tension"
      - type: "contour"
        x: "pretension"
        y: "water_depth"
        z: "max_offset"
```

## Python Integration

### Loading YAML in Python

```python
import yaml
from pathlib import Path

def load_config(config_file: str) -> dict:
    """Load YAML configuration file."""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Usage
config = load_config('../config/mooring_analysis.yaml')

water_depth = config['environment']['water_depth']
vessel_name = config['vessel']['name']
num_lines = config['mooring_system']['number_of_lines']
```

### Writing YAML from Python

```python
import yaml

def save_config(config: dict, output_file: str):
    """Save configuration to YAML file."""
    with open(output_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

# Create configuration
config = {
    'analysis': {
        'name': 'Test Analysis',
        'duration': 3600
    },
    'parameters': {
        'Hs': 8.5,
        'Tp': 12.0
    }
}

save_config(config, '../config/generated_config.yaml')
```

### Validation

```python
import yaml
from jsonschema import validate, ValidationError

def validate_config(config_file: str, schema_file: str) -> bool:
    """Validate YAML against JSON schema."""
    with open(config_file) as f:
        config = yaml.safe_load(f)

    with open(schema_file) as f:
        schema = yaml.safe_load(f)

    try:
        validate(instance=config, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        return False
```

### Merging Configs

```python
def merge_configs(base_config: dict, override_config: dict) -> dict:
    """Deep merge two configuration dictionaries."""
    import copy

    result = copy.deepcopy(base_config)

    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result

# Usage
base = load_config('../config/default.yaml')
custom = load_config('../config/custom.yaml')
merged = merge_configs(base, custom)
```

## Best Practices

### 1. Use Consistent Indentation
```yaml
# ✅ Good: 2 spaces
vessel:
  dimensions:
    length: 320
    beam: 58

# ❌ Bad: Mixed indentation
vessel:
   dimensions:
     length: 320
   beam: 58
```

### 2. Quote Strings When Needed
```yaml
# Quote strings that could be interpreted as numbers or booleans
name: "12345"  # Without quotes, would be number
flag: "true"   # Without quotes, would be boolean

# Quote strings with special characters
description: "Wave height: 8.5m"
```

### 3. Use Anchors for Reusability
```yaml
# Define common material
steel: &steel
  density: 7850
  E: 200e9

# Reuse
chain_material: *steel
pipe_material: *steel
```

### 4. Add Comments for Clarity
```yaml
environment:
  water_depth: 1500  # meters, site-specific
  wave:
    Hs: 8.5  # 100-year return period
    Tp: 12.0  # Associated peak period
```

### 5. Organize Logically
```yaml
# Group related items
analysis:
  # ... analysis settings

environment:
  # ... environmental parameters

vessel:
  # ... vessel properties

mooring:
  # ... mooring system
```

## Common Patterns

### Pattern 1: Configuration Hierarchy
```yaml
# Global defaults
defaults: &defaults
  version: 1.0
  units: "SI"
  precision: 6

# Project-specific configs inherit defaults
project_a:
  <<: *defaults
  name: "Project A"
  # ... specific settings

project_b:
  <<: *defaults
  name: "Project B"
  # ... specific settings
```

### Pattern 2: Environment-Specific Configs
```yaml
# development.yaml
database:
  host: "localhost"
  port: 5432

# production.yaml
database:
  host: "prod-server.example.com"
  port: 5432
```

### Pattern 3: Parameterized Templates
```yaml
# template.yaml
analysis:
  name: "${PROJECT_NAME}"
  water_depth: ${WATER_DEPTH}
  wave_height: ${HS}
```

## Installation

```bash
# Python YAML library
pip install pyyaml

# With validation
pip install pyyaml jsonschema

# Advanced features
pip install ruamel.yaml  # Preserves comments and formatting
```

## Resources

- **YAML Official Spec**: https://yaml.org/spec/
- **PyYAML Documentation**: https://pyyaml.org/wiki/PyYAMLDocumentation
- **YAML Lint**: http://www.yamllint.com/
- **JSON Schema**: https://json-schema.org/

---

**Use this skill to create maintainable, version-controlled configurations for all DigitalModel analyses!**
