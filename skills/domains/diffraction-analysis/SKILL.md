---
name: diffraction-analysis
description: Master skill for hydrodynamic diffraction analysis - AQWA, OrcaWave, and BEMRosetta integration
version: 1.0.0
updated: 2026-01-27
category: offshore-engineering
triggers:
  - diffraction analysis
  - hydrodynamic analysis
  - RAO analysis
  - added mass
  - radiation damping
  - wave forces
  - BEM solver
  - panel method
  - frequency domain
---

# Diffraction Analysis Master Skill

## Overview

This skill provides guidance on hydrodynamic diffraction/radiation analysis using the available modules in digitalmodel. Three primary modules handle different aspects of the workflow:

| Module | Purpose | Primary Use Case |
|--------|---------|------------------|
| **aqwa** | Native AQWA analysis | Direct AQWA .LIS file processing |
| **orcawave** | OrcaWave diffraction | OrcaFlex-integrated analysis |
| **bemrosetta** | Format conversion | AQWA → OrcaFlex workflow, mesh conversion |
| **diffraction** | Unified schemas | Data structures and comparison framework |

## Version

- **Skill Version**: 1.0.0
- **Updated**: 2026-01-27
- **Category**: Offshore Engineering

## Module Comparison

### When to Use Each Module

| Scenario | Recommended Module | Reason |
|----------|-------------------|--------|
| Parse AQWA .LIS files | `aqwa` or `bemrosetta` | Native parsing, no external dependencies |
| Run OrcaWave analysis | `orcawave` | Direct OrcaFlex API integration |
| Convert AQWA → OrcaFlex | `bemrosetta` | Purpose-built converter with validation |
| Compare AQWA vs OrcaWave | `diffraction` | Unified schema comparison framework |
| Handle QTF data | `bemrosetta` | QTF parser and OrcaFlex export |
| Convert mesh formats | `bemrosetta` | GDF/DAT/STL conversion |
| Store/retrieve coefficients | `hydrodynamics` | Coefficient database |

### Feature Matrix

| Feature | aqwa | orcawave | bemrosetta | diffraction |
|---------|------|----------|------------|-------------|
| Parse AQWA .LIS | ✅ | ❌ | ✅ | ✅ (via converter) |
| Parse OrcaWave | ❌ | ✅ | ❌ | ✅ (via converter) |
| RAO extraction | ✅ | ✅ | ✅ | ✅ |
| Added mass/damping | ✅ | ✅ | ✅ | ✅ |
| QTF (2nd order) | ❌ | ✅ | ✅ | ❌ |
| Export to OrcaFlex | ❌ | Native | ✅ | ✅ |
| Mesh conversion | ❌ | ❌ | ✅ | ❌ |
| Coefficient validation | ❌ | ❌ | ✅ | ✅ |
| Comparison framework | ❌ | ❌ | ❌ | ✅ |

## Unified Data Schema

All modules use the unified schema from `diffraction.output_schemas`:

```python
from digitalmodel.modules.diffraction import (
    DiffractionResults,  # Complete analysis container
    RAOSet, RAOComponent, # RAO data structures
    AddedMassSet, DampingSet,  # Coefficient matrices
    HydrodynamicMatrix,  # 6×6 frequency-dependent matrix
    FrequencyData, HeadingData,  # Discretization
    DOF, Unit,  # Enumerations
)
```

### DiffractionResults Structure
```
DiffractionResults
├── vessel_name: str
├── frequencies: FrequencyData
├── headings: HeadingData
├── raos: RAOSet
│   ├── surge: RAOComponent (magnitude, phase)
│   ├── sway: RAOComponent
│   ├── heave: RAOComponent
│   ├── roll: RAOComponent
│   ├── pitch: RAOComponent
│   └── yaw: RAOComponent
├── added_mass: AddedMassSet
│   └── matrices: List[HydrodynamicMatrix]  # 6×6 per frequency
├── damping: DampingSet
│   └── matrices: List[HydrodynamicMatrix]
└── source_file: str
```

## Typical Workflows

### Workflow 1: AQWA Analysis Only

```python
from digitalmodel.modules.aqwa import AQWAAnalysis

# Direct AQWA analysis
analysis = AQWAAnalysis(folder="aqwa_results/")
analysis.run()
```

### Workflow 2: AQWA → OrcaFlex Conversion

```python
from digitalmodel.modules.bemrosetta import (
    AQWAParser, OrcaFlexConverter, validate_coefficients
)

# Parse AQWA
parser = AQWAParser()
results = parser.parse("analysis.LIS")

# Validate
report = validate_coefficients(results)
if report.is_valid:
    # Convert to OrcaFlex
    converter = OrcaFlexConverter(output_dir="./orcaflex")
    converter.convert(results)
```

### Workflow 3: OrcaWave Analysis

```python
from digitalmodel.modules.orcawave import OrcaWaveAnalysis

# Run OrcaWave (requires OrcFxAPI)
analysis = OrcaWaveAnalysis()
analysis.setup_model(vessel_file="vessel.yml")
analysis.run_diffraction()
results = analysis.get_results()
```

### Workflow 4: AQWA vs OrcaWave Comparison

```python
from digitalmodel.modules.diffraction import (
    DiffractionComparator,
    AQWAConverter,
    OrcaWaveConverter,
)

# Convert both sources to unified schema
aqwa_results = AQWAConverter("aqwa_folder/").convert_to_unified_schema()
orcawave_results = OrcaWaveConverter(model).convert_to_unified_schema()

# Compare
comparator = DiffractionComparator()
report = comparator.compare(aqwa_results, orcawave_results)
print(f"RAO match: {report.rao_match_percentage:.1f}%")
```

### Workflow 5: Complete Pipeline with QTF

```python
from digitalmodel.modules.bemrosetta import (
    AQWAParser, QTFParser, OrcaFlexConverter,
    CoefficientValidator, CausalityChecker,
)

# Parse main results
parser = AQWAParser()
results = parser.parse("analysis.LIS")

# Parse QTF
qtf_parser = QTFParser()
qtf_data = qtf_parser.parse("analysis.QTF")

# Validate
coef_validator = CoefficientValidator(check_symmetry=True)
coef_report = coef_validator.validate(results)

causality_checker = CausalityChecker()
kk_report = causality_checker.validate(results)

# Convert with QTF
converter = OrcaFlexConverter(output_dir="./output")
converter.set_qtf_data(qtf_data)
converter.convert(results)
```

## CLI Commands

### AQWA Module
```bash
# (Uses existing AQWA CLI if available)
```

### BEMRosetta Module
```bash
bemrosetta convert analysis.LIS -o ./output
bemrosetta convert analysis.LIS --qtf analysis.QTF -o ./output
bemrosetta info analysis.LIS
bemrosetta validate analysis.LIS --strict --causality
bemrosetta convert-mesh hull.gdf -o hull.stl
bemrosetta status
```

### Diffraction Module
```bash
# Batch processing
python -m digitalmodel.modules.diffraction.batch_processor config.yml
```

## Output Formats

### OrcaFlex Vessel Type YAML
```yaml
VesselType:
  Name: FPSO
  Category: Vessel
  PrimaryMotion: Calculated (6 DOF)
  RAOOrigin: [0, 0, 0]
  RAOPhaseConvention: AQWA
```

### Coefficient CSV
```csv
Frequency_rad/s,A11,A12,A13,A14,A15,A16,...
0.3,1.0e7,0.0,0.0,0.0,0.0,0.0,...
0.4,1.1e7,0.0,0.0,0.0,0.0,0.0,...
```

### QTF CSV
```csv
Freq1_rad/s,Freq2_rad/s,Heading_deg,Surge_Re,Surge_Im,...
0.3,0.3,0.0,1.2e5,0.0,...
```

## Validation Criteria

### Coefficient Validation
- **Symmetry**: Added mass and damping matrices should be symmetric
- **Positive definiteness**: Diagonal elements non-negative
- **Physical limits**: No NaN/Inf values, reasonable magnitudes

### Kramers-Kronig Causality
- Added mass A(ω) and damping B(ω) must satisfy K-K relations
- Tolerance: typically 10% relative error acceptable

### RAO Validation
- Magnitude non-negative
- Phase in reasonable range (-360° to 360°)
- Physical trends (heave RAO → 1.0 at low frequency)

## Best Practices

1. **Always validate coefficients** before using in OrcaFlex
2. **Check K-K causality** for added mass/damping consistency
3. **Compare results** when both AQWA and OrcaWave are available
4. **Use unified schema** for interoperability
5. **Document water depth** and frequency range assumptions

## Related Skills

| Skill | Description |
|-------|-------------|
| **aqwa-analysis** | AQWA .LIS processing and RAO extraction |
| **orcawave-analysis** | OrcaWave diffraction/radiation analysis |
| **bemrosetta** | AQWA → OrcaFlex converter with QTF support |
| **hydrodynamics** | 6×6 matrices, wave spectra, OCIMF loading |
| **orcaflex-rao-import** | Multi-format RAO import to OrcaFlex |
| **orcawave-to-orcaflex** | OrcaWave to OrcaFlex conversion |
| **orcawave-aqwa-benchmark** | Cross-validation comparison |

## Module Locations

```
src/digitalmodel/modules/
├── aqwa/                    # AQWA analysis tools
├── orcawave/                # OrcaWave analysis
├── bemrosetta/              # Format conversion
│   ├── parsers/             # AQWA, QTF parsers
│   ├── converters/          # OrcaFlex export
│   ├── mesh/                # GDF, DAT, STL handlers
│   └── validators/          # Coefficient, causality
├── diffraction/             # Unified schemas
│   ├── output_schemas.py    # DiffractionResults
│   ├── aqwa_converter.py    # AQWA to unified
│   ├── orcawave_converter.py # OrcaWave to unified
│   ├── orcaflex_exporter.py # Export to OrcaFlex
│   └── comparison_framework.py # Compare results
└── hydrodynamics/           # Coefficient database
```

## References

- OrcaFlex Documentation: https://www.orcina.com/webhelp/OrcaFlex/
- WAMIT Manual: https://www.wamit.com/manual.htm
- BEMRosetta: https://github.com/BEMRosetta/BEMRosetta
