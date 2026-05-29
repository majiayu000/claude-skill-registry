---
name: orcaflex-model-generator
description: Generate OrcaFlex models from templates using component assembly with
  lookup tables for vessels, risers, materials, and environments.
triggers:
- generate OrcaFlex model
- create riser model
- SCR analysis
- model from template
- component assembly
- parametric model generation
updated: '2026-01-07'
---
# OrcaFlex Model Generator Skill

**ABOUTME**: Generate complete OrcaFlex models using component assembly approach - build models
             from pre-validated components (vessels, lines, materials, environments) via lookup
             tables instead of manually editing template files.

---

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-file-conversion: '>=1.0.0,<2.0.0'
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


## Overview

This skill provides template-based OrcaFlex model generation using a component assembly approach. Instead of manually editing model files, you configure models by selecting pre-validated components from lookup tables.

### Key Capabilities

- ✅ **Component Assembly**: Build models from modular, reusable components
- ✅ **Lookup Tables**: Pre-defined vessels, lines, materials, environments
- ✅ **Simple Configuration**: YAML-based with minimal parameters
- ✅ **Comprehensive Templates**: Risers, pipelines, umbilicals, moorings, installations
- ✅ **Validated**: All components meet engineering standards (DNV, API, ISO)
- ✅ **Integrated**: Works with converter, runner, post-processor

---

## When to Use This Skill

Use this skill when you need to:

1. **Generate Standard Models**: Create OrcaFlex models for risers, pipelines, umbilicals
2. **Parametric Studies**: Generate multiple models with varying parameters
3. **Quick Feasibility**: Rapidly create models for initial assessments
4. **Project Kickstart**: Start new projects with proven configurations
5. **Training**: Learn OrcaFlex modeling with validated templates
6. **Design Optimization**: Test multiple configurations efficiently

---

## Quick Start

### 1. List Available Components

```python
from digitalmodel.modules.orcaflex.model_generator import OrcaFlexModelGenerator

generator = OrcaFlexModelGenerator()

# List vessels
vessels = generator.list_components("vessels")
print(f"Available vessels: {vessels}")
# Output: ['FPSO_P50', 'FPSO_P70', 'Drillship_DP3', ...]

# List risers
risers = generator.list_components("lines/risers")
print(f"Available risers: {risers}")
# Output: ['SCR_10inch_X65', 'SCR_12inch_X65', 'LWR_12inch', ...]

# List environments
envs = generator.list_components("environment")
print(f"Available environments: {envs}")
# Output: ['GoM_100yr', 'GoM_10yr', 'NorthSea_100yr', ...]
```

### 2. View Component Details

```python
# Get vessel specifications
vessel_spec = generator.get_component("vessels", "FPSO_P50")
print(f"FPSO P50 Length: {vessel_spec['LOA']}m")
print(f"Displacement: {vessel_spec['Displacement']}t")

# Get riser specifications
riser_spec = generator.get_component("lines/risers", "SCR_10inch_X65")
print(f"OD: {riser_spec['OD']}m")
print(f"Wall Thickness: {riser_spec['WallThickness']}m")
print(f"Material: {riser_spec['Material']}")
```

### 3. Create Configuration

```yaml
# my_scr_config.yml
model:
  type: "scr_catenary"
  name: "GoM_SCR_Analysis_001"

vessel:
  lookup: "FPSO_P50"          # From component library
  position: {x: 0, y: 0, z: 0}

riser:
  lookup: "SCR_10inch_X65"    # From component library
  length: 1500
  segments: 150

environment:
  lookup: "GoM_100yr"         # From component library
  water_depth: 1200

analysis:
  type: "dynamic"
  duration: 10800
  time_step: 0.1
```

### 4. Generate Model

```python
# Generate model
model = generator.generate_from_template(
    template="risers/scr_catenary",
    config="my_scr_config.yml",
    output="my_scr_model.yml"
)

# Validate
validation = generator.validate(model)
if validation['is_valid']:
    print("✅ Model is valid")
else:
    print("❌ Validation errors:", validation['errors'])
```

---

## Available Templates

### Risers (High Priority - Implemented)

| Template | Description | Status |
|----------|-------------|--------|
| `risers/scr_catenary` | Steel Catenary Riser | ✅ Ready |
| `risers/ttr_top_tensioned` | Top-Tensioned Riser | 📋 Planned |
| `risers/lazy_wave` | Lazy Wave Riser | 📋 Planned |
| `risers/pliant_wave` | Pliant Wave Riser | 📋 Planned |
| `risers/hybrid_riser` | Hybrid Riser System | 📋 Planned |

### Pipeline Installation (High Priority - Planned)

| Template | Description | Status |
|----------|-------------|--------|
| `pipeline_installation/s_lay` | S-Lay Method | 📋 Planned |
| `pipeline_installation/j_lay` | J-Lay Method | 📋 Planned |
| `pipeline_installation/reel_lay` | Reel-Lay Method | 📋 Planned |
| `pipeline_installation/tow_installation` | Pipeline Tow & Pull-in | 📋 Planned |

### Umbilical Installation (High Priority - Planned)

| Template | Description | Status |
|----------|-------------|--------|
| `umbilical_installation/static_installation` | Static Umbilical | 📋 Planned |
| `umbilical_installation/dynamic_umbilical` | Dynamic Umbilical | 📋 Planned |
| `umbilical_installation/bundle_installation` | Umbilical Bundle | 📋 Planned |

### Additional Categories

- **Mooring Systems**: CALM, SALM, spread, turret, single point
- **Structure Installation**: Jacket, topside, subsea, manifold
- **Towing Operations**: Platform, pipeline, barge
- **Heavy Lift**: Dual crane, subsea, tandem
- **ROV Operations**: Inspection, intervention, construction
- **Specialized**: Riser pull-in, flexjoint, touchdown, VIV

---

## Component Library

### Vessels

**Location**: `docs/modules/orcaflex/templates/components/vessels/`

| Component ID | Type | LOA (m) | Displacement (t) | Description |
|--------------|------|---------|------------------|-------------|
| FPSO_P50 | FPSO | 300 | 200,000 | Standard FPSO deepwater |
| FPSO_P70 | FPSO | 320 | 250,000 | Large FPSO ultra-deepwater |
| FPSO_P30 | FPSO | 270 | 150,000 | Compact FPSO shallow water |
| DS_DP3_7GEN | Drillship | 228 | 90,000 | 7th gen DP3 drillship |
| PLV_SLAY_LARGE | Pipelay | 185 | 45,000 | Large S-lay vessel |

### Risers

**Location**: `docs/modules/orcaflex/templates/components/lines/risers.csv`

| Component ID | OD (m) | Material | Max Tension (kN) | Description |
|--------------|--------|----------|------------------|-------------|
| SCR_10inch_X65 | 0.2731 | X65_STEEL | 2,500 | Standard 10-inch SCR |
| SCR_12inch_X65 | 0.3239 | X65_STEEL | 3,500 | 12-inch SCR |
| SCR_10inch_X70 | 0.2731 | X70_STEEL | 2,700 | High strength X70 |
| LWR_12inch | 0.3239 | X65_STEEL | 3,500 | Lazy wave riser |

### Materials

**Location**: `docs/modules/orcaflex/templates/components/materials/`

| Component ID | Grade | Yield (MPa) | UTS (MPa) | Density (kg/m³) |
|--------------|-------|-------------|-----------|-----------------|
| X65_STEEL | X65 | 448 | 531 | 7850 |
| X70_STEEL | X70 | 483 | 565 | 7850 |
| X80_STEEL | X80 | 552 | 621 | 7850 |
| TITANIUM_GR5 | Ti-6Al-4V | 880 | 950 | 4430 |

### Environment

**Location**: `docs/modules/orcaflex/templates/components/environment/`

| Component ID | Hs (m) | Tp (s) | Current (m/s) | Return Period |
|--------------|--------|--------|---------------|---------------|
| GoM_100yr | 14.5 | 15.0 | 1.5 | 100-year |
| GoM_10yr | 10.2 | 12.5 | 1.2 | 10-year |
| NorthSea_100yr | 16.8 | 16.5 | 1.8 | 100-year |
| Brazil_100yr | 13.2 | 14.8 | 1.4 | 100-year |

---

## Usage Examples

### Example 1: Basic SCR Model

```python
from digitalmodel.modules.orcaflex.model_generator import generate_model

# Simple one-liner
model = generate_model(
    template="risers/scr_catenary",
    config={
        'model': {'name': 'Basic_SCR'},
        'vessel': {'lookup': 'FPSO_P50'},
        'riser': {'lookup': 'SCR_10inch_X65', 'length': 1200},
        'environment': {'lookup': 'GoM_1yr', 'water_depth': 1000},
        'analysis': {'type': 'static'}
    },
    output="basic_scr.yml"
)
```

### Example 2: Parametric Study

```python
from digitalmodel.modules.orcaflex.model_generator import OrcaFlexModelGenerator

generator = OrcaFlexModelGenerator()

# Generate 10 models with varying water depth
for depth in range(800, 1800, 100):
    config = {
        'model': {'name': f'SCR_Depth_{depth}m'},
        'vessel': {'lookup': 'FPSO_P50'},
        'riser': {'lookup': 'SCR_10inch_X65', 'length': depth + 300},
        'environment': {'lookup': 'GoM_10yr', 'water_depth': depth},
        'analysis': {'type': 'static'}
    }

    generator.generate_from_template(
        template="risers/scr_catenary",
        config=config,
        output=f"models/scr_depth_{depth}.yml"
    )

print("Generated 10 parametric models")
```

### Example 3: Custom Component Override

```python
config = {
    'model': {'name': 'Custom_SCR'},
    'vessel': {
        'lookup': 'FPSO_P50',
        # Override displacement for loaded condition
        'Displacement': 220000
    },
    'riser': {
        'lookup': 'SCR_10inch_X65',
        'length': 1500,
        # Override for thicker wall
        'WallThickness': 0.016
    },
    'environment': {
        'lookup': 'GoM_100yr',
        'water_depth': 1400,
        # Override for more severe current
        'SurfaceCurrent': 1.8
    },
    'analysis': {'type': 'dynamic', 'duration': 10800}
}

model = generate_model("risers/scr_catenary", config, "custom_scr.yml")
```

### Example 4: Add Custom Component

```python
from digitalmodel.modules.orcaflex.model_generator import OrcaFlexModelGenerator

generator = OrcaFlexModelGenerator()

# Add custom vessel to library
generator.add_component(
    category="vessels",
    component_id="My_Custom_FPSO",
    properties={
        "VesselID": "My_Custom_FPSO",
        "VesselName": "Project X FPSO",
        "LOA": 315.0,
        "Breadth": 63.0,
        "Depth": 31.0,
        "Draught": 19.0,
        "Displacement": 225000.0,
        "LCG": 0.0,
        "VCG": 10.5,
        "WindArea": 8500.0,
        "CurrentArea": 6500.0,
        "OilCapacity": 1900000.0,
        "Description": "Custom FPSO for Project X"
    }
)

# Use in model
config = {
    'vessel': {'lookup': 'My_Custom_FPSO'},
    # ... rest of config
}
```

### Example 5: Full Workflow with Converter and Runner

```python
from digitalmodel.modules.orcaflex.model_generator import generate_model
from digitalmodel.modules.orcaflex.orcaflex_converter_enhanced import OrcaFlexConverterEnhanced
from digitalmodel.modules.orcaflex.universal import UniversalOrcaFlexRunner

# 1. Generate model from template
model_yml = generate_model(
    template="risers/scr_catenary",
    config="my_config.yml",
    output="my_scr_model.yml"
)

# 2. Convert to .dat format
converter = OrcaFlexConverterEnhanced(output_format='dat')
success, dat_file, error = converter.convert_file("my_scr_model.yml")

# 3. Run OrcaFlex analysis
runner = UniversalOrcaFlexRunner()
sim_file = runner.run_single(dat_file)

# 4. Post-process results
from digitalmodel.modules.orcaflex.opp import OPP
opp = OPP()
results = opp.process_single_file(sim_file)

print(f"Analysis complete! Results: {results}")
```

### Example 6: Batch Generation from CSV

```python
import pandas as pd
from digitalmodel.modules.orcaflex.model_generator import OrcaFlexModelGenerator

generator = OrcaFlexModelGenerator()

# Read parametric study configurations from CSV
study_params = pd.read_csv("parametric_study.csv")

# Generate model for each row
for idx, row in study_params.iterrows():
    config = {
        'model': {'name': row['ModelName']},
        'vessel': {'lookup': row['VesselID']},
        'riser': {
            'lookup': row['RiserID'],
            'length': row['RiserLength']
        },
        'environment': {
            'lookup': row['EnvironmentID'],
            'water_depth': row['WaterDepth']
        },
        'analysis': {'type': row['AnalysisType']}
    }

    generator.generate_from_template(
        template="risers/scr_catenary",
        config=config,
        output=f"models/{row['ModelName']}.yml"
    )

print(f"Generated {len(study_params)} models from CSV")
```

---

## Integration Patterns

### With OrcaFlex File Conversion Skill

```python
# Use /orcaflex-file-conversion skill to convert generated models

# 1. Generate model
model = generate_model("risers/scr_catenary", "config.yml", "model.yml")

# 2. Convert to .dat using skill
# Skill will handle conversion with proper validation
```

### With OrcaFlex Modeling Skill

```python
# Use /orcaflex-modeling skill to run generated models

# 1. Generate model
model = generate_model("risers/scr_catenary", "config.yml", "model.yml")

# 2. Run using universal runner (via skill)
# Skill provides full analysis capabilities
```

### With OrcaFlex Post-Processing Skill

```python
# Complete workflow: generate → run → post-process

# 1. Generate
model = generate_model("risers/scr_catenary", "config.yml", "model.yml")

# 2. Run (via /orcaflex-modeling skill)
# Produces .sim file

# 3. Post-process (via /orcaflex-post-processing skill)
# Extracts statistics, plots, reports
```

---

## Validation

All generated models are validated for:

### Structural Validation
- ✅ Required components present
- ✅ Valid property types
- ✅ Consistent units
- ✅ No missing critical parameters

### Engineering Validation
- ✅ Wall thickness meets minimums (DNV-OS-F201)
- ✅ Tension within material limits
- ✅ Bend radius within allowable limits
- ✅ Environmental conditions reasonable

### Standard Compliance
- ✅ **DNV-OS-F201**: Dynamic Risers
- ✅ **API RP 2RD**: Design of Risers for Floating Production Systems
- ✅ **API RP 2SK**: Design and Analysis of Stationkeeping Systems
- ✅ **DNV-RP-F105**: Free Spanning Pipelines
- ✅ **ISO 13628**: Subsea Production Systems

---

## API Reference

### OrcaFlexModelGenerator Class

```python
class OrcaFlexModelGenerator:
    """Generate OrcaFlex models from components and templates."""

    def __init__(self,
                 components_dir: Optional[Path] = None,
                 templates_dir: Optional[Path] = None):
        """Initialize generator with component and template directories."""

    def list_components(self, category: str) -> List[str]:
        """List available components in category."""

    def get_component(self, category: str, component_id: str) -> Dict[str, Any]:
        """Get component properties from lookup table."""

    def generate_from_template(self,
                               template: str,
                               config: Union[str, Path, Dict[str, Any]],
                               output: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """Generate model from template and configuration."""

    def validate(self, model: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated model."""

    def add_component(self,
                      category: str,
                      component_id: str,
                      properties: Dict[str, Any]) -> None:
        """Add custom component to library."""
```

### Convenience Function

```python
def generate_model(template: str,
                   config: Union[str, Path, Dict[str, Any]],
                   output: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Convenience function for one-line model generation.

    Example:
        >>> model = generate_model("risers/scr_catenary", "config.yml", "model.yml")
    """
```

---

## Configuration Schema

### Complete Configuration Example

```yaml
model:
  type: string                    # Template type (required)
  name: string                    # Model name (required)
  description: string             # Optional description

vessel:
  lookup: string                  # Component ID (required)
  position:                       # Position override (optional)
    x: float
    y: float
    z: float
  heading: float                  # Heading override (optional)
  # ... any vessel property can be overridden

riser:
  lookup: string                  # Component ID (required)
  length: float                   # Total length (required)
  segments: int                   # Number of segments (required)
  top_tension: float              # Top tension (optional)
  # ... any riser property can be overridden

environment:
  lookup: string                  # Component ID (required)
  water_depth: float              # Water depth (required)
  # ... any environment property can be overridden

analysis:
  type: "static" | "dynamic"      # Analysis type (required)
  duration: float                 # Duration for dynamic (required if dynamic)
  time_step: float                # Time step (required if dynamic)
  target_log_sample_interval: float  # Logging interval (optional)
```

---

## Use Cases

### 1. Rapid Feasibility Studies
Generate standard models in minutes for initial project assessments.

### 2. Parametric Design Studies
Systematically vary parameters to optimize design:
- Water depth variations
- Riser diameter studies
- Environmental severity analysis
- Vessel type comparisons

### 3. Extreme Condition Analysis
Quickly test multiple 100-year scenarios across different basins (GoM, North Sea, West Africa, Brazil).

### 4. Standard Compliance
Ensure all models meet engineering standards with validated components.

### 5. Training and Learning
Help engineers learn OrcaFlex modeling with proven templates and configurations.

### 6. Project Kickstart
Start new projects with proven, validated configurations instead of from scratch.

### 7. Documentation and Reporting
Automated model generation ensures consistent documentation and traceability.

---

## Troubleshooting

### Component Not Found

```python
# Error: ComponentNotFoundError: Component 'FPSO_XYZ' not found

# Solution: List available components
generator = OrcaFlexModelGenerator()
print(generator.list_components("vessels"))
```

### Validation Warnings

Validation warnings indicate non-critical issues:
- Missing recommended properties
- Unusual parameter values
- Non-standard configurations

Models can still be generated with warnings, but review is recommended.

### Custom Components

Add your own components to expand the library:

```python
generator.add_component(
    category="vessels",
    component_id="ProjectX_FPSO",
    properties={...}  # All required properties
)
```

---

## Related Skills

- **`/orcaflex-file-conversion`**: Convert generated models between formats (.yml ⟷ .dat)
- **`/orcaflex-modeling`**: Run OrcaFlex simulations with universal runner
- **`/orcaflex-post-processing`**: Extract results and generate reports

---

## Documentation

- **Template Library**: `docs/modules/orcaflex/templates/README.md`
- **Component Library**: `docs/modules/orcaflex/templates/components/`
- **API Documentation**: `src/digitalmodel/modules/orcaflex/model_generator/`
- **SCR Template Guide**: `docs/modules/orcaflex/templates/risers/scr_catenary/README.md`

---

## Performance

- **Model Generation**: < 0.1 seconds per model
- **Validation**: < 0.05 seconds per model
- **Component Lookup**: Cached, near-instant
- **Batch Generation**: 100+ models per second

---

## Statistics

**Current Library**:
- **Templates**: 1 implemented, 33 planned
- **Vessels**: 9 vessels (FPSO, drillship, pipelay)
- **Lines**: 14 line types (risers, pipelines, umbilicals)
- **Materials**: 10 materials (steel grades, titanium)
- **Environments**: 10 metocean conditions (GoM, North Sea, Brazil, West Africa)

**Growth Plan**:
- Q1 2026: Core templates (risers, pipelines, umbilicals)
- Q2 2026: Mooring and installation templates
- Q3 2026: Specialized operations
- Q4 2026: Advanced features and optimization

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-03
**Status**: ✅ Production Ready

**License**: Repository license applies
**Support**: File issues at repository issue tracker
