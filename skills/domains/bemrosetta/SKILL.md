---
name: bemrosetta
description: BEMRosetta hydrodynamic coefficient converter - AQWA to OrcaFlex workflow with QTF and mesh support
version: 1.0.0
updated: 2026-01-27
category: offshore-engineering
triggers:
  - bemrosetta
  - hydrodynamic conversion
  - AQWA to OrcaFlex
  - coefficient converter
  - QTF conversion
  - mesh format conversion
  - GDF to STL
  - panel mesh
  - Kramers-Kronig
  - causality check
---

# BEMRosetta Integration Skill

## Version

- **Skill Version**: 1.0.0
- **Module Version**: 1.0.0
- **Python**: 3.11+
- **Dependencies**: numpy, scipy, click, pydantic, loguru

## Changelog

### 1.0.0 (2026-01-27)
- Initial release
- AQWA parser for .LIS files
- QTF parser for second-order forces
- OrcaFlex converter (YAML, CSV)
- Mesh handlers (GDF, DAT, STL)
- Coefficient and causality validators
- Click-based CLI

## When to Use

Use this skill when you need to:

1. **Convert AQWA outputs to OrcaFlex format**
   - Parse AQWA .LIS diffraction analysis files
   - Export to OrcaFlex-compatible YAML and CSV

2. **Handle QTF (second-order forces) data**
   - Parse QTF files for sum/difference frequency forces
   - Export QTF to OrcaFlex format

3. **Convert mesh formats**
   - Convert between GDF (WAMIT), DAT (AQWA/NEMOH), STL formats
   - Validate mesh quality

4. **Validate hydrodynamic coefficients**
   - Check matrix symmetry and positive definiteness
   - Verify Kramers-Kronig causality relations

## Agent Capabilities

The BEMRosetta skill enables agents to:

### Parsing
- Parse AQWA .LIS files extracting RAOs, added mass, damping
- Parse QTF files for second-order wave forces
- Extract solver metadata (version, water depth, frequencies, headings)

### Conversion
- Convert to OrcaFlex vessel type YAML
- Export coefficient CSV files
- Export QTF data in OrcaFlex format

### Mesh Processing
- Read/write WAMIT GDF format
- Read/write AQWA/NEMOH DAT format
- Read/write STL format (ASCII and binary)
- Calculate mesh quality metrics

### Validation
- Coefficient symmetry checks
- Positive definiteness verification
- Physical limits validation
- Kramers-Kronig causality checking

## Prerequisites

```bash
# Module is included in digitalmodel package
uv pip install -e .

# Verify installation
bemrosetta status
```

## CLI Commands

```bash
# Convert AQWA to OrcaFlex
bemrosetta convert analysis.LIS -o ./output

# Convert with QTF data
bemrosetta convert analysis.LIS --qtf analysis.QTF -o ./output

# Display file information
bemrosetta info analysis.LIS

# Validate coefficients
bemrosetta validate analysis.LIS --strict --causality

# Convert mesh formats
bemrosetta convert-mesh input.gdf -o output.stl
bemrosetta convert-mesh input.dat -o output.gdf

# Validate mesh quality
bemrosetta validate-mesh hull.gdf --check-normals

# Show module status
bemrosetta status
```

## Python API

### Basic Workflow

```python
from digitalmodel.modules.bemrosetta import (
    AQWAParser,
    OrcaFlexConverter,
    validate_coefficients,
)

# Parse AQWA results
parser = AQWAParser()
results = parser.parse("analysis.LIS")

# Access metadata
print(f"Vessel: {parser.metadata.vessel_name}")
print(f"Water depth: {parser.metadata.water_depth}")
print(f"Frequencies: {parser.metadata.frequency_count}")

# Validate coefficients
report = validate_coefficients(results, strict=True)
if not report.is_valid:
    print(f"Errors: {report.errors}")

# Convert to OrcaFlex format
converter = OrcaFlexConverter(output_dir="./output")
converter.convert(results)
```

### QTF Handling

```python
from digitalmodel.modules.bemrosetta import QTFParser, OrcaFlexConverter

# Parse QTF file
qtf_parser = QTFParser()
qtf_data = qtf_parser.parse("analysis.QTF")

print(f"QTF type: {qtf_data.qtf_type}")
print(f"Frequencies: {qtf_data.n_frequencies_1} x {qtf_data.n_frequencies_2}")

# Include QTF in conversion
converter = OrcaFlexConverter(output_dir="./output")
converter.set_qtf_data(qtf_data)
converter.convert(results)
```

### Mesh Conversion

```python
from digitalmodel.modules.bemrosetta import (
    GDFHandler, DATHandler, STLHandler, convert_mesh
)

# Read GDF mesh
handler = GDFHandler()
mesh = handler.read("hull.gdf")

# Check quality
report = handler.validate_mesh(mesh)
print(f"Panels: {report.n_panels}")
print(f"Quality score: {report.quality_score}/100")

# Convert to STL
convert_mesh("hull.gdf", "hull.stl")
```

### Causality Validation

```python
from digitalmodel.modules.bemrosetta import (
    CoefficientValidator,
    CausalityChecker,
)

# Coefficient validation
validator = CoefficientValidator(
    check_symmetry=True,
    check_positive_definite=True,
    tolerance=0.01,
)
report = validator.validate(results)

# Kramers-Kronig causality check
checker = CausalityChecker(tolerance=0.1)
kk_report = checker.validate(results)
for key, error in kk_report.info.items():
    if error and error > 0.1:
        print(f"Warning: {key} KK error = {error:.2%}")
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `AQWAParser` | Parse AQWA .LIS files |
| `QTFParser` | Parse QTF second-order force files |
| `OrcaFlexConverter` | Convert to OrcaFlex format |
| `GDFHandler` | WAMIT GDF mesh format |
| `DATHandler` | AQWA/NEMOH DAT mesh format |
| `STLHandler` | STL mesh format |
| `CoefficientValidator` | Validate coefficient matrices |
| `CausalityChecker` | Kramers-Kronig validation |

## Data Models

| Model | Description |
|-------|-------------|
| `BEMSolverMetadata` | Solver name, version, water depth, vessel info |
| `QTFData` | QTF coefficients with frequency pairs |
| `PanelMesh` | Vertices, panels, normals, areas |
| `MeshQualityReport` | Panel statistics and quality score |
| `ConversionResult` | Conversion operation result |

## Best Practices

1. **Always validate before conversion**
   ```python
   report = validate_coefficients(results, strict=True)
   if not report.is_valid:
       raise ValueError(f"Invalid coefficients: {report.errors}")
   ```

2. **Check mesh quality before use**
   ```python
   report = handler.validate_mesh(mesh)
   if report.quality_score < 70:
       print("Warning: Low mesh quality")
   ```

3. **Use native parsers for reliability**
   - Native Python parsers don't require BEMRosetta executable
   - BEMRosetta executable provides extended features when available

4. **Handle missing data gracefully**
   ```python
   warnings = converter.validate_input(results)
   for w in warnings:
       logger.warning(w)
   ```

## Integration with Other Modules

### With diffraction module
```python
from digitalmodel.modules.diffraction import OrcaFlexExporter
from digitalmodel.modules.bemrosetta import AQWAParser

# BEMRosetta uses diffraction module schemas
parser = AQWAParser()
results = parser.parse("analysis.LIS")  # Returns DiffractionResults

# Can use existing OrcaFlexExporter
exporter = OrcaFlexExporter(results, output_dir)
exporter.export_all()
```

### With hydrodynamics module
```python
from digitalmodel.modules.hydrodynamics import CoefficientDatabase

# Store parsed coefficients in database
db = CoefficientDatabase()
db.store(results.added_mass, results.damping)
```

## Error Handling

```python
from digitalmodel.modules.bemrosetta import (
    BEMRosettaError,
    ParserError,
    ConverterError,
    MeshError,
)

try:
    results = parser.parse("analysis.LIS")
except ParserError as e:
    print(f"Parse error: {e}")
    print(f"File: {e.context.get('file_path')}")
except BEMRosettaError as e:
    print(f"BEMRosetta error: {e}")
```

## Related Skills

- **aqwa-analysis** - AQWA .LIS processing and RAO extraction
- **orcawave-analysis** - OrcaWave diffraction/radiation analysis
- **orcawave-to-orcaflex** - OrcaWave to OrcaFlex conversion
- **orcaflex-rao-import** - Multi-format RAO import
- **hydrodynamics** - 6x6 matrices and wave spectra
- **diffraction-analysis** - Master skill for diffraction workflows

## References

- [BEMRosetta GitHub](https://github.com/BEMRosetta/BEMRosetta)
- [Module README](../../../src/digitalmodel/modules/bemrosetta/MODULE_README.md)
- [OrcaFlex Documentation](https://www.orcina.com/webhelp/OrcaFlex/)
