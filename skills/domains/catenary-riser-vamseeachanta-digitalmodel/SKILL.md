---
name: catenary-riser
description: Analyze catenary and lazy wave riser configurations for static shape,
  forces, and OrcaFlex model generation. Use for riser static configuration analysis,
  catenary force calculations, lazy wave design, and generating OrcaFlex models from
  catenary parameters.
updated: '2026-01-07'
---
# Catenary Riser Analysis Skill

Analyze catenary and lazy wave riser configurations for static shape, forces, tension distribution, and OrcaFlex model generation.

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

### [1.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- Catenary riser static analysis
- Lazy wave catenary design and optimization
- Riser static configuration calculation
- Catenary force and tension analysis
- Generating OrcaFlex models from catenary geometry
- Fatigue loading extraction from riser configurations
- Pipe property calculations (buoyancy, effective weight)

## Prerequisites

- Python environment with `digitalmodel` package installed
- Riser geometry and material properties
- Environmental data (water depth, current if applicable)

## Analysis Types

### 1. Simple Catenary Analysis

```yaml
catenary:
  simple_catenary:
    flag: true
    geometry:
      top_end:
        x: 0.0
        z: 100.0
      touchdown:
        x: 500.0
        z: 0.0
    properties:
      outer_diameter: 0.2032
      wall_thickness: 0.0127
      steel_density: 7850
      internal_fluid_density: 800
      seawater_density: 1025
    output:
      shape_file: "results/catenary_shape.csv"
      forces_file: "results/catenary_forces.csv"
      plot_file: "results/catenary_plot.html"
```

### 2. Lazy Wave Catenary

```yaml
catenary:
  lazy_wave:
    flag: true
    geometry:
      water_depth: 1500.0
      hang_off_angle: 8.0
      buoyancy_section:
        start_arc_length: 800.0
        end_arc_length: 1200.0
        buoyancy_factor: 1.5
      target_sag_bend_depth: 800.0
      target_hog_bend_depth: 600.0
    pipe_properties:
      outer_diameter: 0.273
      wall_thickness: 0.0159
    output:
      configuration_file: "results/lazy_wave_config.csv"
      plot_file: "results/lazy_wave_plot.html"
```

### 3. OrcaFlex Model Generation

```yaml
catenary:
  orcaflex_model:
    flag: true
    catenary_config: "results/lazy_wave_config.csv"
    orcaflex_settings:
      line_name: "Riser1"
      segment_length: 5.0
      include_buoyancy_modules: true
    output:
      yml_file: "models/riser_model.yml"
```

## Python API

### Simple Catenary Equation

```python
from digitalmodel.modules.catenary.catenary_equation import CatenaryEquation
import numpy as np

catenary = CatenaryEquation()
top_end = (0.0, 100.0)
touchdown = (500.0, 0.0)

horizontal_tension = catenary.solve(
    top_end=top_end,
    bottom_end=touchdown,
    unit_weight=500.0
)

arc_lengths = np.linspace(0, catenary.total_length, 100)
x, z = catenary.get_shape(arc_lengths)
tensions = catenary.get_tension(arc_lengths)
```

### Catenary Riser Analysis

```python
from digitalmodel.modules.catenary.catenary_riser import CatenaryRiser
from digitalmodel.modules.catenary.pipe_properties import PipeProperties

pipe = PipeProperties(
    outer_diameter=0.2032,
    wall_thickness=0.0127,
    steel_density=7850,
    internal_fluid_density=800
)

riser = CatenaryRiser(pipe_properties=pipe)
results = riser.analyze(
    water_depth=1000.0,
    hang_off_angle=10.0,
    top_tension=1500e3
)

print(f"TDP position: x={results['tdp_x']:.1f}m")
print(f"Total length: {results['total_length']:.1f} m")
```

### Lazy Wave Catenary

```python
from digitalmodel.modules.catenary.lazy_wave_catenary import LazyWaveCatenary

lazy_wave = LazyWaveCatenary()
config = {
    "water_depth": 1500.0,
    "hang_off_angle": 8.0,
    "buoyancy_section": {
        "start_length": 800.0,
        "end_length": 1200.0,
        "net_buoyancy": 300.0
    },
    "pipe_properties": pipe
}

results = lazy_wave.analyze(config)
sag_bend = results["sag_bend"]
hog_bend = results["hog_bend"]
```

### OrcaFlex Model Building

```python
from digitalmodel.modules.catenary.orcaflex_model import OrcaFlexModelBuilder

builder = OrcaFlexModelBuilder()
builder.set_line_from_catenary(
    catenary_results=results,
    line_name="Riser1",
    segment_length=5.0
)
builder.add_buoyancy_section(
    start_arc_length=800.0,
    end_arc_length=1200.0,
    buoyancy_od=0.6
)
builder.export_yml("models/riser.yml")
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `CatenaryEquation` | Mathematical catenary solver |
| `CatenaryRiser` | Main analysis orchestrator |
| `LazyWaveCatenary` | Dynamic catenary with buoyancy |
| `PipeProperties` | Material and geometric properties |
| `OrcaFlexModelBuilder` | Model export to OrcaFlex |

## Output Formats

### Catenary Shape CSV

```csv
arc_length,x,z,tension,curvature,bend_moment
0.0,0.0,100.0,1523456.7,0.000123,1875.4
10.0,9.8,98.5,1518234.5,0.000145,2215.6
```

## Best Practices

1. **Consistent units** - Use SI units (meters, Newtons)
2. **Coordinate system** - Z positive upward, origin at seabed
3. **Segment resolution** - Use small segments near critical points
4. **Curvature check** - Verify minimum bend radius constraints

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Fatigue at critical locations
- [structural-analysis](../structural-analysis/SKILL.md) - Stress verification

## References

- API RP 2RD: Design of Risers for Floating Production Systems
- DNV-OS-F201: Dynamic Risers
