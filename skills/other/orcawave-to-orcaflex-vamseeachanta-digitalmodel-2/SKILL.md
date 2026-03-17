---
name: orcawave-to-orcaflex
description: Integration specialist for converting OrcaWave diffraction results to
  OrcaFlex vessel types. Handles hydrodynamic database generation, RAO import, viscous
  damping addition, and coordinate system transformations.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- OrcaWave to OrcaFlex
- hydrodynamic database
- vessel type creation
- RAO import
- diffraction to time domain
- added mass damping export
- OrcaFlex vessel setup
---

# OrcaWave to OrcaFlex Integration Skill

Specialized expertise for converting OrcaWave diffraction analysis results to OrcaFlex vessel type format for time-domain simulations.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  numpy: '>=1.24.0'
  pandas: '>=2.0.0'
  pyyaml: '>=6.0'
orcaflex_version: '>=11.0'
orcawave_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
```

## When to Use

- Converting OrcaWave results (.owr) to OrcaFlex vessel type
- Creating hydrodynamic database for time-domain analysis
- Importing RAO data from diffraction analysis
- Adding viscous damping to radiation damping
- Transforming coordinate systems between tools
- Setting up vessel types with full hydrodynamic properties
- Batch conversion of multiple loading conditions

## Workflow Overview

```
OrcaWave Analysis              OrcaFlex Model
┌──────────────────┐          ┌──────────────────┐
│ Panel mesh       │          │ Vessel object    │
│ Diffraction/     │    →     │ Vessel type      │
│ Radiation        │          │ - RAOs           │
│ QTF (optional)   │          │ - Added mass     │
└──────────────────┘          │ - Damping        │
                              │ - QTF (optional) │
                              └──────────────────┘
```

## Python API

### Basic Conversion

```python
from digitalmodel.diffraction.orcawave_converter import OrcaWaveConverter
from digitalmodel.diffraction.orcaflex_exporter import OrcaFlexExporter

# Load OrcaWave results
import OrcFxAPI

# Option 1: From OrcaWave model directly
orcawave_model = OrcFxAPI.DiffractionModel("models/fpso.owr")
vessel = orcawave_model.Vessel

# Initialize converter
converter = OrcaWaveConverter(vessel)

# Convert to unified schema
unified_data = converter.convert()

# Export to OrcaFlex format
exporter = OrcaFlexExporter()
exporter.export_vessel_type(
    data=unified_data,
    output_file="orcaflex_models/fpso_vessel_type.yml",
    format="yaml"
)
```

### With Viscous Damping

```python
from digitalmodel.orcawave.orcaflex_export import OrcaWaveToOrcaFlex

# Initialize converter with damping options
converter = OrcaWaveToOrcaFlex()

# Load OrcaWave results
converter.load_orcawave("models/fpso.owr")

# Add viscous damping (percentage of critical)
converter.set_viscous_damping({
    'Roll': 0.05,   # 5% critical
    'Pitch': 0.03,  # 3% critical
    'Heave': 0.02,  # 2% critical
    'Surge': 0.01,
    'Sway': 0.01,
    'Yaw': 0.02
})

# Export with combined damping
converter.export(
    output_file="orcaflex_models/fpso_with_damping.yml",
    include_qtf=True,
    include_mean_drift=True
)
```

### Full Hydrodynamic Database

```python
from digitalmodel.orcawave.orcaflex_export import HydrodynamicDatabaseCreator

# Create complete hydrodynamic database
db_creator = HydrodynamicDatabaseCreator()

# Load all loading conditions
db_creator.add_condition(
    name="full_load",
    orcawave_file="models/fpso_full.owr",
    draft=22.0
)
db_creator.add_condition(
    name="ballast",
    orcawave_file="models/fpso_ballast.owr",
    draft=12.0
)
db_creator.add_condition(
    name="transit",
    orcawave_file="models/fpso_transit.owr",
    draft=8.0
)

# Create interpolated database
db = db_creator.create_database(
    interpolation_parameter="draft",
    output_directory="orcaflex_models/hydro_database/"
)

# Generate vessel type with draft-dependent properties
db_creator.export_vessel_type(
    db,
    output_file="orcaflex_models/fpso_vessel_type.yml"
)
```

### RAO Import with Validation

```python
from digitalmodel.orcawave.rao_import import RAOImporter
from digitalmodel.diffraction.output_validator import OutputValidator

# Import RAOs with validation
importer = RAOImporter()

# Load OrcaWave RAOs
raos = importer.load_from_orcawave("models/fpso.owr")

# Validate before export
validator = OutputValidator()
validation_result = validator.validate_raos(
    raos,
    checks=[
        "frequency_range",
        "heading_coverage",
        "value_ranges",
        "phase_continuity",
        "symmetry"
    ]
)

if validation_result.is_valid:
    # Export validated RAOs
    importer.export_to_orcaflex(
        raos,
        output_file="orcaflex_models/fpso_raos.yml"
    )
else:
    print(f"Validation issues: {validation_result.issues}")
```

### Coordinate Transformation

```python
from digitalmodel.orcawave.coordinate_transform import CoordinateTransformer

# Handle coordinate system differences
transformer = CoordinateTransformer()

# OrcaWave uses different conventions than OrcaFlex
# Transform origin location
transformer.set_orcawave_origin(
    x=150.0,  # Midship
    y=0.0,
    z=0.0     # At waterline
)

transformer.set_orcaflex_origin(
    x=0.0,    # Stern
    y=0.0,
    z=-10.0   # At keel
)

# Transform RAO phases for heading convention
# OrcaWave: Wave FROM direction
# OrcaFlex: Wave TO direction (configurable)
transformer.set_heading_convention(
    orcawave="from",
    orcaflex="from"  # Match conventions
)

# Apply transformation to data
transformed_data = transformer.transform(orcawave_data)
```

## Configuration Examples

### Standard Export Configuration

```yaml
# configs/orcawave_to_orcaflex.yml

conversion:
  input:
    orcawave_file: "models/fpso.owr"

  output:
    directory: "orcaflex_models/"
    vessel_type_file: "fpso_vessel_type.yml"

  contents:
    include_raos: true
    include_added_mass: true
    include_damping: true
    include_hydrostatics: true
    include_qtf: true
    include_mean_drift: true

  viscous_damping:
    roll: 0.05
    pitch: 0.03
    heave: 0.02
    surge: 0.01
    sway: 0.01
    yaw: 0.02

  coordinate_transform:
    origin_shift: [0.0, 0.0, 0.0]
    heading_convention: "from"  # Wave direction convention

  validation:
    check_frequency_range: true
    check_heading_coverage: true
    check_value_ranges: true
    min_frequency: 0.02
    max_frequency: 2.0
```

### Batch Conversion Configuration

```yaml
# configs/batch_conversion.yml

batch_conversion:
  conditions:
    - name: "draft_22m"
      input: "models/fpso_draft22.owr"
      draft: 22.0
      trim: 0.0

    - name: "draft_18m"
      input: "models/fpso_draft18.owr"
      draft: 18.0
      trim: 0.5

    - name: "draft_14m"
      input: "models/fpso_draft14.owr"
      draft: 14.0
      trim: 1.0

  common_settings:
    viscous_damping:
      roll: 0.05
    include_qtf: true

  output:
    directory: "orcaflex_models/conditions/"
    naming_pattern: "fpso_{name}.yml"
```

## Export Formats

### Supported Output Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| YAML | .yml | OrcaFlex vessel type |
| CSV | .csv | Spreadsheet analysis |
| Excel | .xlsx | Multi-sheet export |
| JSON | .json | API integration |
| OrcaFlex Data | .dat | Direct OrcaFlex import |
| HDF5 | .h5 | Large dataset storage |

### Multi-Format Export

```python
from digitalmodel.diffraction.orcawave_converter import OrcaWaveConverter

# Convert and export to multiple formats
converter = OrcaWaveConverter(vessel)
unified_data = converter.convert()

# Export all formats
converter.export_all_formats(
    unified_data,
    output_directory="exports/",
    base_name="fpso_hydro",
    formats=["yaml", "csv", "xlsx", "json"]
)
```

## CLI Usage

```bash
# Basic conversion
python -m digitalmodel.orcawave.convert \
    --input models/fpso.owr \
    --output orcaflex_models/fpso_vessel_type.yml

# With viscous damping
python -m digitalmodel.orcawave.convert \
    --input models/fpso.owr \
    --output orcaflex_models/fpso_vessel_type.yml \
    --roll-damping 0.05 \
    --pitch-damping 0.03

# Include QTF
python -m digitalmodel.orcawave.convert \
    --input models/fpso.owr \
    --output orcaflex_models/fpso_vessel_type.yml \
    --include-qtf \
    --include-mean-drift

# Batch conversion
python -m digitalmodel.orcawave.convert batch \
    --config configs/batch_conversion.yml

# Validate before export
python -m digitalmodel.orcawave.convert \
    --input models/fpso.owr \
    --output orcaflex_models/fpso_vessel_type.yml \
    --validate \
    --validation-report reports/validation.html
```

## Validation Checks

### Pre-Export Validation

```python
from digitalmodel.diffraction.output_validator import OrcaFlexExportValidator

# Validate export data
validator = OrcaFlexExportValidator()

# Run all checks
validation = validator.validate_for_orcaflex(
    data=unified_data,
    checks=[
        "frequency_range",      # 0.02-2.0 rad/s typical
        "heading_coverage",     # 0-360 degrees
        "rao_ranges",           # Physical limits
        "added_mass_positive",  # Diagonal > 0
        "damping_positive",     # Diagonal >= 0
        "phase_continuity",     # No 360-degree jumps
        "matrix_symmetry",      # A_ij = A_ji
        "units_consistency"     # SI units
    ]
)

# Report issues
if not validation.passed:
    for issue in validation.issues:
        print(f"[{issue.severity}] {issue.check}: {issue.message}")
```

## OrcaFlex Vessel Type Structure

### Generated YAML Structure

```yaml
# Generated vessel type file
VesselType:
  Name: "FPSO_HydroDB"

  DisplacementRAOs:
    # Surge RAO
    - Period: 5.0
      Direction: 0.0
      SurgeAmplitude: 0.95
      SurgePhase: 15.0
    # ... more entries

  LoadRAOs:
    # Force/moment RAOs
    - Period: 5.0
      Direction: 0.0
      SurgeLoadAmplitude: 150000.0
      SurgeLoadPhase: 20.0
    # ... more entries

  AddedMassAndDamping:
    - Period: 5.0
      AddedMassX: 25000000.0
      AddedMassY: 35000000.0
      AddedMassZ: 45000000.0
      # ... full 6x6 matrix
      DampingX: 1500000.0
      DampingY: 2000000.0
      # ... full 6x6 matrix

  WaveDrift:
    # Mean drift coefficients
    - Period: 5.0
      Direction: 0.0
      DriftForceX: -50000.0
      DriftForceY: 0.0
      DriftMomentZ: 0.0

  QTF:
    # Quadratic transfer functions (if included)
    Frequencies: [0.05, 0.1, 0.15, ...]
    HeadingPairs: [[0, 0], [0, 30], ...]
    Data:
      - FrequencyPair: [0.05, 0.05]
        HeadingPair: [0, 0]
        SurgeReal: -10000.0
        SurgeImag: 5000.0
        # ... other DOFs
```

## Best Practices

1. **Validate First**: Always validate OrcaWave results before conversion
2. **Consistent Units**: Verify SI units throughout
3. **Coordinate Systems**: Document origin locations clearly
4. **Heading Convention**: Match wave direction conventions
5. **Viscous Damping**: Add realistic viscous damping for roll
6. **Frequency Range**: Ensure coverage of wave spectrum
7. **QTF Data**: Include for moored vessel analysis
8. **Version Control**: Track both OrcaWave and OrcaFlex versions

## Error Handling

```python
# Handle conversion errors
try:
    converter = OrcaWaveConverter(vessel)
    data = converter.convert()

except MissingDataError as e:
    print(f"Required data missing: {e}")
    # Check OrcaWave analysis completeness

except FrequencyMismatchError as e:
    print(f"Frequency discretization issue: {e}")
    # Interpolate to common frequencies

except CoordinateTransformError as e:
    print(f"Coordinate transformation failed: {e}")
    # Verify origin definitions

except ExportError as e:
    print(f"Export failed: {e}")
    # Check output directory permissions
```

## Related Skills

- [orcawave-analysis](../orcawave-analysis/SKILL.md) - OrcaWave diffraction analysis
- [orcaflex-vessel-setup](../orcaflex-vessel-setup/SKILL.md) - OrcaFlex vessel configuration
- [orcaflex-rao-import](../orcaflex-rao-import/SKILL.md) - RAO data import
- [hydrodynamics](../hydrodynamics/SKILL.md) - Coefficient management

## References

- OrcaWave Data Format Specification
- OrcaFlex Vessel Type Documentation
- Converter Implementation: `src/digitalmodel/modules/diffraction/orcawave_converter.py`
- Exporter Implementation: `src/digitalmodel/modules/diffraction/orcaflex_exporter.py`

---

**Version History**

- **1.0.0** (2026-01-17): Initial release with conversion, validation, and multi-format export
