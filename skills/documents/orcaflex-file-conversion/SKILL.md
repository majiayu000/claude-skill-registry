---
name: orcaflex-file-conversion
description: Convert OrcaFlex files between formats (.dat, .yml, .sim) for digital
  analysis and automation. Supports bidirectional conversion, batch processing, and
  format standardization.
version: 1.0.0
updated: 2026-01-02
category: offshore-engineering
triggers:
- convert OrcaFlex files
- .dat to .yml conversion
- .yml to .dat conversion
- .sim to .dat conversion
- .sim to .yml conversion
- OrcaFlex file format conversion
- batch OrcaFlex conversion
- digitally analyze OrcaFlex files
---
# OrcaFlex File Conversion Skill

Convert OrcaFlex model files between binary (.dat, .sim) and YAML (.yml) formats for digital analysis, automation, and version control.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
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

- Converting .dat files to .yml for human-readable inspection
- Converting .yml files back to .dat for OrcaFlex execution
- Converting .sim files to both .dat and .yml formats
- Batch processing multiple OrcaFlex files
- Preparing files for digital analysis and automation
- Creating version-control-friendly YAML representations
- Standardizing file formats across projects

## File Format Overview

### OrcaFlex File Types

| Format | Type | Description | Use Case |
|--------|------|-------------|----------|
| **.dat** | Binary | Compressed binary model data | OrcaFlex native format (fast loading) |
| **.yml** | ASCII | YAML text representation | Human-readable, version control, automation |
| **.sim** | Binary | Simulation results + model | Post-processing, result analysis |

### Conversion Capabilities

```
.dat  ⟷  .yml   (Bidirectional)
.sim  →  .dat   (Extract model from simulation)
.sim  →  .yml   (Extract model as YAML)
```

## Prerequisites

- OrcaFlex license (for OrcFxAPI)
- Python environment with `digitalmodel` package installed
- OrcFxAPI Python module configured

## Quick Start

### Single File Conversion

```bash
# Convert .dat to .yml
python -m digitalmodel.modules.orcaflex.orcaflex_yml_converter model.dat

# Convert .yml to .dat
python -m digitalmodel.modules.orcaflex.orcaflex_yml_converter model.yml
```

### Batch Conversion

```bash
# Convert all .dat files in directory
python -m digitalmodel.modules.orcaflex.examples_integration.batch_converter \
    --input-dir models/ \
    --output-dir models_yml/ \
    --pattern "*.dat"

# Convert with validation
python -m digitalmodel.modules.orcaflex.examples_integration.batch_converter \
    --input-dir models/ \
    --output-dir models_yml/ \
    --validate \
    --max-retries 3
```

## Python API

### Basic Conversion

```python
from digitalmodel.modules.orcaflex.orcaflex_yml_converter import convert_to_yml
from pathlib import Path

# Convert single file
success = convert_to_yml("model.dat")

# Check output
if success:
    yml_file = Path("model.yml")
    print(f"Converted to: {yml_file}")
```

### Batch Conversion with Progress Tracking

```python
from digitalmodel.modules.orcaflex.examples_integration.batch_converter import OrcaFlexBatchConverter
from pathlib import Path

# Initialize converter
converter = OrcaFlexBatchConverter(
    input_dir=Path("models/"),
    output_dir=Path("models_yml/"),
    use_mock=False,      # Use real OrcFxAPI
    validate=True,       # Validate converted files
    max_retries=2        # Retry failed conversions
)

# Run batch conversion
results = converter.convert_batch()

# Check statistics
print(f"Total: {results['statistics']['total_files']}")
print(f"Success: {results['statistics']['successful']}")
print(f"Failed: {results['statistics']['failed']}")
```

### Advanced: Bidirectional Conversion

```python
import OrcFxAPI
from pathlib import Path

def convert_yml_to_dat(yml_file: str, dat_file: str = None):
    """Convert YAML to binary .dat format."""
    yml_path = Path(yml_file)

    # Default output path
    if dat_file is None:
        dat_file = yml_path.with_suffix('.dat')

    # Load YAML and save as .dat
    model = OrcFxAPI.Model(str(yml_path))
    model.SaveData(str(dat_file))

    print(f"Converted: {yml_path.name} → {Path(dat_file).name}")
    return True

# Usage
convert_yml_to_dat("model.yml", "model.dat")
```

### Simulation File Conversion

```python
from digitalmodel.modules.orcaflex.examples_integration.orcfxapi_converter import OrcFxAPIConverter
from pathlib import Path

# Initialize converter for .sim files
converter = OrcFxAPIConverter(
    input_dir=Path("results/.sim/"),
    preserve_originals=True
)

# Convert all .sim files to .dat and .yml
stats = converter.convert_all()

print(f".dat files created: {stats['dat_files_created']}")
print(f".yml files created: {stats['yml_files_created']}")
```

## Batch Processing Patterns

### Pattern-Based Conversion

```python
from pathlib import Path
from digitalmodel.modules.orcaflex.examples_integration.batch_converter import OrcaFlexBatchConverter

converter = OrcaFlexBatchConverter(
    input_dir=Path("docs/modules/orcaflex/examples/raw"),
    output_dir=Path("docs/modules/orcaflex/examples/yaml"),
    validate=True
)

# Find and convert all files
converter.find_orcaflex_files()  # Searches for *.dat and *.sim
results = converter.convert_batch()

# Review conversion report
report_path = Path("docs/modules/orcaflex/examples/yaml/conversion_report.md")
```

### Parallel Processing

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def convert_file_wrapper(file_path):
    """Wrapper for parallel conversion."""
    from digitalmodel.modules.orcaflex.orcaflex_yml_converter import convert_to_yml
    return convert_to_yml(str(file_path))

# Get all .dat files
dat_files = list(Path("models/").glob("**/*.dat"))

# Convert in parallel
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(convert_file_wrapper, dat_files))

success_count = sum(results)
print(f"Successfully converted: {success_count}/{len(dat_files)}")
```

## Configuration

### Batch Converter Options

```python
OrcaFlexBatchConverter(
    input_dir=Path,              # Source directory
    output_dir=Path,             # Destination directory
    use_mock=False,              # Use mock mode if OrcFxAPI unavailable
    validate=True,               # Validate YAML structure
    max_retries=2                # Retry attempts for failed conversions
)
```

### Conversion Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Real** | Uses OrcFxAPI | Production conversions with license |
| **Mock** | Creates placeholder YAML | Testing without license |

## Output & Reports

### Conversion Report (Markdown)

Automatically generated at `{output_dir}/conversion_report.md`:

```markdown
# OrcaFlex Batch Conversion Report

Generated: 2026-01-02 10:30:45

## Summary

- **Total Files**: 180
- **Successful**: 178
- **Failed**: 2
- **Skipped**: 0
- **Processing Time**: 145.32 seconds
- **Conversion Mode**: Real (OrcFxAPI)

## Success Rate: 98.9%

## File Types

- **.dat files**: 150
- **.sim files**: 30
```

### Conversion Report (JSON)

Detailed JSON report at `{output_dir}/conversion_report.json`:

```json
{
  "statistics": {
    "total_files": 180,
    "successful": 178,
    "failed": 2,
    "processing_time": 145.32,
    "files_by_type": {
      "dat": 150,
      "sim": 30
    },
    "errors": [
      {
        "file": "corrupted_model.dat",
        "error": "Failed to load model",
        "attempts": 2
      }
    ]
  },
  "results": [...],
  "timestamp": "2026-01-02T10:30:45"
}
```

## YAML Format Structure

### Example OrcaFlex YAML Output

```yaml
General:
  UnitsSystem: SI
  g: 9.80665
  AirDensity: 1.225
  WaterDensity: 1025.0
  KinematicViscosity: 1.35e-06

Environment:
  WaterDepth: 100.0
  WaveType: JONSWAP
  WaveHs: 6.0
  WaveTp: 12.0
  WaveGamma: 3.3
  CurrentSpeed: 1.5
  CurrentDirection: 0.0

VesselTypes:
  - Name: FPSO_Alpha
    Length: 300.0
    Breadth: 60.0
    Draught: 20.0
    Displacement: 180000.0
    DisplacementRAOs:
      Directions: [0, 45, 90, 135, 180]
      Frequencies: [0.1, 0.2, 0.3, 0.4, 0.5]
      Surge: [[...]]
      Sway: [[...]]
      Heave: [[...]]
      Roll: [[...]]
      Pitch: [[...]]
      Yaw: [[...]]

Lines:
  - Name: Mooring_Line_1
    LineType: Chain_120mm
    Length: 1500.0
    TargetSegmentLength: 10.0
    EndAConnection: Anchored
    EndAX: -800.0
    EndAY: 0.0
    EndAZ: -100.0
    EndBConnection: Vessel
```

## Validation

### YAML Structure Validation

The converter validates:
- File is readable YAML
- Contains OrcaFlex-specific sections (General, Environment, etc.)
- File size is reasonable (> 100 bytes)
- No corruption during conversion

### Round-Trip Validation

```python
def validate_round_trip(original_dat: Path):
    """Validate .dat → .yml → .dat conversion."""
    import OrcFxAPI

    # Convert to YAML
    yml_file = original_dat.with_suffix('.yml')
    model1 = OrcFxAPI.Model(str(original_dat))
    model1.SaveData(str(yml_file))

    # Convert back to .dat
    dat_file_new = original_dat.with_stem(original_dat.stem + '_roundtrip')
    model2 = OrcFxAPI.Model(str(yml_file))
    model2.SaveData(str(dat_file_new))

    # Compare file sizes (should be similar)
    size_original = original_dat.stat().st_size
    size_new = dat_file_new.stat().st_size

    diff_percent = abs(size_new - size_original) / size_original * 100

    if diff_percent < 5:
        print(f"✓ Round-trip validated ({diff_percent:.2f}% size difference)")
        return True
    else:
        print(f"✗ Round-trip failed ({diff_percent:.2f}% size difference)")
        return False
```

## Integration with Universal CLI

### Adding Conversion to Universal CLI

The converter can be integrated into the universal CLI for seamless workflow:

```bash
# Future integration (planned)
orcaflex-universal convert --input models/ --output models_yml/ --format yml
orcaflex-universal convert --input models_yml/ --output models/ --format dat
```

## Use Cases

### 1. Version Control Preparation

Convert binary .dat files to YAML for Git tracking:

```bash
python -m digitalmodel.modules.orcaflex.examples_integration.batch_converter \
    --input-dir models/ \
    --output-dir models_version_control/ \
    --pattern "*.dat"

# Commit YAML files to Git
git add models_version_control/*.yml
git commit -m "Add OrcaFlex models in YAML format"
```

### 2. Automated Model Generation

Generate .dat files from YAML templates:

```python
import OrcFxAPI
from pathlib import Path
import yaml

# Load YAML template
with open("template.yml") as f:
    config = yaml.safe_load(f)

# Modify parameters
config['Environment']['WaveHs'] = 8.0
config['Environment']['WaveTp'] = 14.0

# Save as new YAML
with open("case_100yr.yml", "w") as f:
    yaml.dump(config, f)

# Convert to .dat for OrcaFlex
model = OrcFxAPI.Model("case_100yr.yml")
model.SaveData("case_100yr.dat")
```

### 3. Batch Analysis Preparation

Convert 180+ example files for analysis:

```python
from digitalmodel.modules.orcaflex.examples_integration.batch_converter import OrcaFlexBatchConverter
from pathlib import Path

# Convert all examples
converter = OrcaFlexBatchConverter(
    input_dir=Path("docs/modules/orcaflex/examples/raw"),
    output_dir=Path("docs/modules/orcaflex/examples/yaml"),
    validate=True
)

results = converter.convert_batch()

# Now ready for digital analysis
print(f"Converted {results['statistics']['successful']} files")
print("Ready for automated analysis and feature extraction")
```

### 4. Model Inspection and Debugging

Convert .dat to .yml for inspection:

```bash
# Convert problematic model to YAML
python -m digitalmodel.modules.orcaflex.orcaflex_yml_converter problem_model.dat

# Inspect YAML in text editor
code problem_model.yml

# Make corrections in YAML
# Convert back to .dat
python -m digitalmodel.modules.orcaflex.orcaflex_yml_converter problem_model.yml
```

## Error Handling

### Common Issues

**1. OrcFxAPI Not Available**
```python
try:
    import OrcFxAPI
except ImportError:
    print("ERROR: OrcFxAPI not available")
    print("Install: pip install <OrcaFlex_install_dir>/OrcFxAPI/Python")
    # Fall back to mock mode
    converter = OrcaFlexBatchConverter(use_mock=True)
```

**2. Corrupted File**
```python
# The batch converter automatically retries
converter = OrcaFlexBatchConverter(max_retries=3)
# Failed files are logged in conversion_report.json
```

**3. License Issues**
```python
# Check license before conversion
from digitalmodel.modules.orcaflex.orcaflex_utilities import OrcaflexUtilities

utils = OrcaflexUtilities()
if not utils.is_orcaflex_available():
    print("No OrcaFlex license - using mock mode")
    converter = OrcaFlexBatchConverter(use_mock=True)
```

## Best Practices

### File Organization

```
project/
├── models/
│   ├── original/          # Original .dat files (read-only)
│   ├── working/           # Working .yml files (editable)
│   └── generated/         # Generated .dat files for execution
├── results/
│   └── .sim/             # Simulation results
└── conversion_logs/      # Conversion reports and logs
```

### Workflow Recommendations

1. **Keep originals**: Always preserve original .dat files
2. **Version control YAML**: Commit .yml files, not .dat files
3. **Validate conversions**: Enable validation for production
4. **Batch processing**: Use parallel processing for large datasets
5. **Document changes**: Add comments in YAML files for modifications

## Performance

### Benchmarks

- **Single file conversion**: 0.5-2 seconds per file
- **Batch processing (180 files)**: ~145 seconds with validation
- **Parallel processing (4 workers)**: ~3x faster than sequential
- **Memory usage**: ~200-500 MB per file during conversion

### Optimization Tips

1. Use parallel processing for > 10 files
2. Disable validation for trusted files
3. Process smaller files first (auto-sorted by size)
4. Limit max_workers based on available licenses

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Process simulation results

## References

- Existing Converters:
  - `src/digitalmodel/modules/orcaflex/orcaflex_yml_converter.py`
  - `src/digitalmodel/modules/orcaflex/examples_integration/batch_converter.py`
  - `src/digitalmodel/modules/orcaflex/examples_integration/orcfxapi_converter.py`
- OrcFxAPI Documentation
- YAML Specification: https://yaml.org/

---

## Version History

- **1.0.0** (2026-01-02): Initial release with bidirectional conversion, batch processing, and comprehensive reporting
