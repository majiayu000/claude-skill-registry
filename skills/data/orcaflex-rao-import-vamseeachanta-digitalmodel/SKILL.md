---
name: orcaflex-rao-import
description: Import RAO (Response Amplitude Operator) data from external sources including
  AQWA, OrcaFlex, and CSV files. Includes validation, interpolation, and conversion
  for OrcaFlex vessel type creation.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- RAO import
- import vessel RAOs
- AQWA to OrcaFlex
- RAO conversion
- vessel hydrodynamics
- transfer functions
- motion RAOs
- RAO interpolation
---
# OrcaFlex RAO Import Skill

Import, validate, and process RAO data from external sources for OrcaFlex vessel type creation.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  hydrodynamics: '>=1.0.0,<2.0.0'
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
- Initial release with multi-format RAO import
- AQWA .lis file parsing
- OrcaFlex YAML RAO extraction
- Validation and interpolation
- OrcaFlex vessel type export

## When to Use

- Import RAOs from ANSYS AQWA analysis
- Extract RAOs from existing OrcaFlex models
- Import RAOs from experimental data (CSV/Excel)
- Validate RAO data quality
- Interpolate RAOs to new frequency/heading grids
- Create OrcaFlex vessel types with imported RAOs

## Supported Formats

| Source | Format | Extension | Support Level |
|--------|--------|-----------|---------------|
| ANSYS AQWA | LIS output | .lis | Full |
| OrcaFlex | YAML | .yml | Full |
| Excel | Tabular | .xlsx | Full |
| CSV | Tabular | .csv | Full |
| WAMIT | Output | .out | Planned |
| HydroD | Database | .h5 | Planned |

## RAO Data Structure

### 6-DOF Motion RAOs

| DOF | Description | Units (Amplitude) | Units (Phase) |
|-----|-------------|-------------------|---------------|
| Surge | Translation X | m/m | deg |
| Sway | Translation Y | m/m | deg |
| Heave | Translation Z | m/m | deg |
| Roll | Rotation X | deg/m | deg |
| Pitch | Rotation Y | deg/m | deg |
| Yaw | Rotation Z | deg/m | deg |

## Configuration

### Basic Import Configuration

```yaml
# configs/rao_import.yml

rao_import:
  source:
    type: "aqwa"
    file: "data/hydrodynamics/vessel_aqwa.lis"

  # Target frequency grid
  frequencies:
    min: 0.02    # rad/s
    max: 2.0
    count: 50

  # Target heading grid
  headings:
    values: [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    symmetry: "port_starboard"  # Mirror for 180-360

  # Validation settings
  validation:
    enabled: true
    amplitude_limits:
      surge: 10.0    # m/m
      sway: 10.0
      heave: 5.0
      roll: 50.0     # deg/m
      pitch: 20.0
      yaw: 30.0
    phase_continuity_check: true
    frequency_range_check: true

  # Output
  output:
    format: "orcaflex_yml"
    file: "output/vessel_raos.yml"
```

### Multi-Source Import

```yaml
# configs/rao_multi_import.yml

rao_import:
  sources:
    - name: "full_load"
      type: "aqwa"
      file: "data/vessel_full_load.lis"
      loading_condition: "Full Load"

    - name: "ballast"
      type: "aqwa"
      file: "data/vessel_ballast.lis"
      loading_condition: "Ballast"

  interpolation:
    method: "cubic"
    target_frequencies: "common_grid"
    target_headings: [0, 30, 60, 90, 120, 150, 180]

  output:
    combined_file: "output/vessel_raos_combined.yml"
    separate_files: true
```

## Python API

### Basic RAO Import

```python
from digitalmodel.modules.marine_analysis.rao_processor import RAOProcessor

# Initialize processor
processor = RAOProcessor()

# Import from AQWA
rao_data = processor.import_from_aqwa(
    file_path="data/vessel.lis",
    vessel_name="FPSO"
)

# Access data
print(f"Frequencies: {rao_data.frequencies}")
print(f"Headings: {rao_data.headings}")
print(f"DOFs: {rao_data.dofs}")

# Get specific RAO
heave_rao = rao_data.get_rao("heave", heading=90)
print(f"Heave RAO at 90 deg: Amplitudes = {heave_rao['amplitude']}")
```

### AQWA File Reading

```python
from digitalmodel.modules.marine_analysis.aqwa_reader import AQWAReader

# Initialize reader
reader = AQWAReader()

# Read AQWA .lis file
aqwa_data = reader.read_lis_file("data/vessel_aqwa.lis")

# Extract motion RAOs
raos = reader.extract_motion_raos(aqwa_data)

# Structure:
# raos = {
#     "frequencies": [...],
#     "headings": [...],
#     "surge": {"amplitude": [[...]], "phase": [[...]]},
#     "sway": {...},
#     "heave": {...},
#     "roll": {...},
#     "pitch": {...},
#     "yaw": {...}
# }
```

### OrcaFlex RAO Reading

```python
from digitalmodel.modules.marine_analysis.orcaflex_reader import OrcaFlexRAOReader

# Initialize reader
reader = OrcaFlexRAOReader()

# Read from OrcaFlex model
rao_data = reader.read_from_model("models/vessel_model.yml")

# Or read from vessel type definition
rao_data = reader.read_vessel_type("data/vessel_types/fpso_type.yml")
```

### RAO Validation

```python
from digitalmodel.modules.marine_analysis.rao_validators import RAOValidator

# Initialize validator
validator = RAOValidator()

# Define validation limits
limits = {
    "surge": 10.0,
    "sway": 10.0,
    "heave": 5.0,
    "roll": 50.0,
    "pitch": 20.0,
    "yaw": 30.0
}

# Validate RAO data
validation_result = validator.validate(
    rao_data,
    amplitude_limits=limits,
    check_phase_continuity=True,
    check_frequency_range=True
)

if validation_result.is_valid:
    print("RAO data passed validation")
else:
    for issue in validation_result.issues:
        print(f"Issue: {issue}")

# Get detailed report
report = validator.generate_validation_report(validation_result)
```

### RAO Interpolation

```python
from digitalmodel.modules.marine_analysis.rao_interpolator import RAOInterpolator

# Initialize interpolator
interpolator = RAOInterpolator()

# Define target grid
target_frequencies = np.linspace(0.02, 2.0, 100)
target_headings = np.arange(0, 181, 15)

# Interpolate
interpolated_raos = interpolator.interpolate_2d(
    rao_data,
    target_frequencies=target_frequencies,
    target_headings=target_headings,
    method="cubic"
)

# Quality assessment
quality = interpolator.assess_quality(rao_data, interpolated_raos)
print(f"Interpolation R²: {quality['r_squared']:.4f}")
```

### Export to OrcaFlex Format

```python
from digitalmodel.modules.marine_analysis.rao_processor import RAOProcessor

processor = RAOProcessor()

# Export to OrcaFlex YAML format
processor.export_to_orcaflex(
    rao_data,
    output_file="vessel_type.yml",
    vessel_name="FPSO_RAOs",
    include_metadata=True
)

# The output file can be directly loaded in OrcaFlex
# as a vessel type DisplacementRAOs section
```

### Complete Workflow

```python
from digitalmodel.modules.marine_analysis.rao_processor import RAOProcessor
from digitalmodel.modules.marine_analysis.rao_validators import RAOValidator
from digitalmodel.modules.marine_analysis.rao_interpolator import RAOInterpolator

# 1. Import RAOs
processor = RAOProcessor()
raw_raos = processor.import_from_aqwa("data/vessel.lis")

# 2. Validate
validator = RAOValidator()
validation = validator.validate(raw_raos)

if not validation.is_valid:
    print("Validation issues found:")
    for issue in validation.issues:
        print(f"  - {issue}")
    # Handle issues or continue with warnings

# 3. Interpolate to OrcaFlex-compatible grid
interpolator = RAOInterpolator()
interpolated = interpolator.interpolate_2d(
    raw_raos,
    target_frequencies=np.linspace(0.05, 1.5, 50),
    target_headings=[0, 45, 90, 135, 180]
)

# 4. Apply port/starboard symmetry
symmetric = processor.apply_symmetry(interpolated, "port_starboard")

# 5. Export for OrcaFlex
processor.export_to_orcaflex(
    symmetric,
    output_file="vessel_raos.yml",
    vessel_name="FPSO"
)

print("RAO import complete!")
```

## Output Formats

### OrcaFlex YAML Format

```yaml
VesselTypes:
  - Name: FPSO_RAOs
    DisplacementRAOs:
      RAOOrigin: [150.0, 0.0, 0.0]  # meters from vessel origin
      Directions: [0, 45, 90, 135, 180]  # degrees
      Periods: [5.0, 7.0, 10.0, 12.0, 15.0, 20.0]  # seconds

      # Amplitude and Phase for each DOF
      # Format: [heading][period]
      SurgeAmp:
        - [0.12, 0.25, 0.45, 0.52, 0.48, 0.35]  # 0 deg
        - [0.10, 0.22, 0.40, 0.48, 0.44, 0.32]  # 45 deg
        # ... more headings

      SurgePhase:
        - [0, 10, 25, 45, 60, 80]
        # ...

      # Similar for Sway, Heave, Roll, Pitch, Yaw
```

### DataFrame Export

```python
# Export to DataFrame for analysis
df = processor.to_dataframe(rao_data)

# Multi-level columns: (DOF, Heading)
# Index: Frequency
print(df.head())
#           Surge                    Sway
#           0      45     90        0      45     90
# 0.02      0.95   0.92   0.88     0.02   0.45   0.92
# 0.05      0.92   0.90   0.85     0.05   0.48   0.95
```

### Validation Report

```json
{
  "is_valid": false,
  "issues": [
    {
      "type": "amplitude_exceeded",
      "dof": "roll",
      "heading": 90,
      "frequency": 0.6,
      "value": 55.2,
      "limit": 50.0
    },
    {
      "type": "phase_discontinuity",
      "dof": "heave",
      "heading": 45,
      "location": "frequency 0.45 rad/s"
    }
  ],
  "warnings": [
    "Frequency range may not cover peak responses"
  ],
  "statistics": {
    "frequency_range": [0.02, 1.5],
    "heading_range": [0, 180],
    "max_amplitudes": {
      "surge": 0.95,
      "sway": 1.02,
      "heave": 1.85,
      "roll": 55.2,
      "pitch": 12.3,
      "yaw": 8.5
    }
  }
}
```

## Best Practices

### Data Quality

1. **Check source analysis** - Verify AQWA/WAMIT converged
2. **Review frequency range** - Cover wave spectrum
3. **Check peak responses** - Resonance captured
4. **Validate symmetry** - Port/starboard consistent

### Interpolation

1. **Don't extrapolate** - Stay within data range
2. **Preserve peaks** - Use adequate resolution
3. **Check quality metrics** - R² should be > 0.95
4. **Compare with source** - Spot-check values

### OrcaFlex Integration

1. **RAO origin** - Match vessel coordinate system
2. **Period vs frequency** - OrcaFlex uses periods
3. **Phase convention** - Check sign convention
4. **Test static equilibrium** - Verify RAO application

## Error Handling

```python
from digitalmodel.modules.marine_analysis.rao_processor import RAOImportError

try:
    rao_data = processor.import_from_aqwa("data/vessel.lis")
except RAOImportError as e:
    print(f"Import failed: {e}")
    print(f"Suggestions: {e.suggestions}")

except FileNotFoundError:
    print("AQWA file not found")

except ValueError as e:
    print(f"Data format error: {e}")
```

## Common Issues

### AQWA Import

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing DOFs | AQWA output incomplete | Check AQWA run settings |
| Wrong units | Unit conversion | Specify units in config |
| Truncated data | Large file | Use streaming reader |

### Interpolation

| Issue | Cause | Solution |
|-------|-------|----------|
| Oscillations | Sparse data | Use linear interpolation |
| NaN values | Out of range | Extend source data |
| Poor fit | Non-smooth data | Review source quality |

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Apply imported RAOs
- [orcawave-analysis](../orcawave-analysis/SKILL.md) - Generate RAOs from diffraction
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - AQWA-specific processing
- [hydrodynamics](../hydrodynamics/SKILL.md) - Hydrodynamic coefficient management

## References

- OrcaFlex: Vessel Type RAO Data
- ANSYS AQWA: Output File Formats
- Source: `src/digitalmodel/modules/marine_analysis/rao_processor.py`
- Source: `src/digitalmodel/modules/marine_analysis/aqwa_reader.py`
- Source: `src/digitalmodel/modules/marine_analysis/orcaflex_reader.py`
- User Story: `.ai/specs/modules/user-story-rao-data-import-processing-2025.md`
