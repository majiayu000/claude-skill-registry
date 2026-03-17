---
name: aqwa-analysis
description: Integrate with AQWA hydrodynamic software for RAO computation, damping
  analysis, and coefficient extraction. Use for AQWA file processing, RAO calculation,
  hydrodynamic coefficient extraction, and pre/post processing workflows.
version: 3.0.0
updated: 2025-01-02
category: offshore-engineering
triggers:
- AQWA analysis
- RAO extraction
- added mass calculation
- damping coefficient
- wave diffraction
- radiation analysis
- AQWA-LINE
- AQWA-DRIFT
- AQWA-LIBRIUM
- AQWA-NAUT
- .LIS files
- .DAT files
- .MES files
---
# AQWA Analysis Skill

Integrate with ANSYS AQWA hydrodynamic software for RAO computation, added mass/damping extraction, and hydrodynamic coefficient management.

## Version Metadata

```yaml
version: 3.0.0
python_min_version: '3.10'
dependencies:
  hydrodynamics: '>=1.0.0,<2.0.0'
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

### [3.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- AQWA hydrodynamic analysis post-processing
- RAO (Response Amplitude Operator) computation
- Hydrodynamic coefficient extraction
- AQWA file processing (LIS, DAT, MES)
- Added mass and damping matrix extraction
- Viscous damping determination
- Pre/post processing workflows
- Diffraction/radiation analysis (AQWA-LINE)
- Time domain motions (AQWA-DRIFT)
- Stability analysis (AQWA-LIBRIUM)
- Cable dynamics (AQWA-NAUT)
- Coupled analysis (AQWA-WAVE)

## Agent Capabilities

This skill integrates agent capabilities from `/agents/aqwa/`:

### Domain Expertise
- **Software**: ANSYS AQWA
- **Analysis Modules**:
  - AQWA-LINE: Diffraction/Radiation analysis
  - AQWA-DRIFT: Time domain motions
  - AQWA-LIBRIUM: Stability analysis
  - AQWA-NAUT: Cable dynamics
  - AQWA-WAVE: Coupled analysis

### Core Capabilities
- First-order wave forces
- Second-order drift forces
- Multi-body interactions
- Mooring and riser systems
- Hydrodynamic coefficients
- RAO calculations

### Industry Standards
- DNV-RP-C205 (Environmental Conditions)
- API RP 2SK (Stationkeeping)
- ISO 19901-7 (Mooring Systems)
- IEC 61400-3 (Wind Turbines)

### Context Optimization
- Cross-references: OrcaFlex, ANSYS Mechanical
- Focused domain: AQWA hydrodynamics
- Max context size: 16000 tokens

## Prerequisites

- Python environment with `digitalmodel` package installed
- AQWA output files (LIS, DAT, or MES format)
- For running AQWA: ANSYS AQWA license

## Analysis Types

### 1. RAO Extraction

Extract RAOs from AQWA results.

```yaml
aqwa_analysis:
  rao_extraction:
    flag: true
    input_file: "aqwa_results/vessel.LIS"
    vessel_name: "FPSO"
    wave_directions: [0, 45, 90, 135, 180]
    output:
      rao_file: "results/vessel_raos.csv"
      plot_file: "results/rao_plots.html"
      format: "amplitude_phase"  # or real_imaginary
```

### 2. Hydrodynamic Coefficients

Extract added mass and damping matrices.

```yaml
aqwa_analysis:
  coefficients:
    flag: true
    input_file: "aqwa_results/vessel.LIS"
    frequencies: "all"  # or specific list [0.1, 0.2, 0.3]
    output:
      added_mass_file: "results/added_mass.csv"
      damping_file: "results/damping.csv"
      matrices_file: "results/hydro_matrices.json"
```

### 3. AQWA File Processing

Parse and process AQWA output files.

```yaml
aqwa_analysis:
  file_processing:
    flag: true
    files:
      - path: "aqwa_results/vessel.LIS"
        type: "lis"
      - path: "aqwa_results/vessel.DAT"
        type: "dat"
    extract:
      - "raos"
      - "added_mass"
      - "damping"
      - "wave_forces"
      - "drift_forces"
    output_directory: "results/aqwa_processed/"
```

### 4. Viscous Damping

Determine viscous damping from decay tests or empirical methods.

```yaml
aqwa_analysis:
  viscous_damping:
    flag: true
    method: "empirical"  # or decay_test
    vessel:
      length: 300.0
      beam: 50.0
      draft: 20.0
    motions: ["roll", "pitch", "heave"]
    empirical_factors:
      roll_percentage: 5.0   # % of critical
      pitch_percentage: 3.0
      heave_percentage: 2.0
    output:
      damping_file: "results/viscous_damping.json"
```

## Python API

### RAO Extraction

```python
from digitalmodel.aqwa.aqwa_raos import AqwaRAOs

# Initialize RAO extractor
raos = AqwaRAOs()

# Load AQWA results
raos.load("aqwa_results/vessel.LIS")

# Get RAO for specific motion and direction
surge_rao = raos.get_rao(
    motion="surge",
    wave_direction=180.0  # degrees (head seas)
)

# Get all RAOs as DataFrame
rao_df = raos.to_dataframe()
# Columns: frequency, direction, surge_amp, surge_phase, sway_amp, ...

# Plot RAOs
raos.plot_rao(
    motions=["heave", "pitch", "roll"],
    directions=[0, 90, 180],
    output_file="results/rao_comparison.html"
)

# Export to OrcaFlex format
raos.export_orcaflex("vessel_raos.yml")
```

### Hydrodynamic Coefficient Extraction

```python
from digitalmodel.aqwa.aqwa_reader import AqwaReader
from digitalmodel.aqwa.aqwa_analysis import AqwaAnalysis

# Initialize reader
reader = AqwaReader()

# Load AQWA output
data = reader.read("aqwa_results/vessel.LIS")

# Get added mass matrix at specific frequency
frequency = 0.1  # rad/s
added_mass = data.get_added_mass(frequency)
# Returns 6x6 numpy array

# Get damping matrix
damping = data.get_damping(frequency)
# Returns 6x6 numpy array

# Get frequency-dependent matrices
frequencies = data.get_frequencies()
for freq in frequencies:
    A = data.get_added_mass(freq)
    B = data.get_damping(freq)
    print(f"ω = {freq:.3f}: A33 = {A[2,2]:.1f}, B33 = {B[2,2]:.1f}")
```

### AQWA Analysis Router

```python
from digitalmodel.aqwa.aqwa_analysis import AqwaAnalysis

# Initialize analysis
aqwa = AqwaAnalysis()

# Configure analysis
cfg = {
    "aqwa": {
        "input_file": "aqwa_results/vessel.LIS",
        "extract": ["raos", "added_mass", "damping", "drift_forces"],
        "output_directory": "results/"
    }
}

# Run extraction
results = aqwa.run(cfg)

# Access results
raos = results["raos"]
added_mass = results["added_mass"]
damping = results["damping"]
drift = results["drift_forces"]
```

### Pre-Processing

```python
from digitalmodel.aqwa.aqwa_preprocess import AqwaPreProcess

# Initialize pre-processor
preprocess = AqwaPreProcess()

# Generate AQWA input from vessel geometry
preprocess.generate_input(
    vessel_geometry="geometry/hull.stl",
    water_depth=1000.0,
    wave_frequencies=[0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.8, 1.0],
    wave_directions=[0, 45, 90, 135, 180],
    output_file="aqwa_input/vessel.dat"
)
```

### Post-Processing

```python
from digitalmodel.aqwa.aqwa_postprocess import AqwaPostProcess

# Initialize post-processor
postprocess = AqwaPostProcess()

# Load results
postprocess.load("aqwa_results/vessel.LIS")

# Generate comprehensive report
postprocess.generate_report(
    output_file="results/aqwa_report.html",
    include=[
        "summary",
        "rao_plots",
        "coefficient_tables",
        "drift_force_plots"
    ]
)

# Validate results
validation = postprocess.validate()
if validation["warnings"]:
    for warning in validation["warnings"]:
        print(f"Warning: {warning}")
```

### Result Validation

```python
from digitalmodel.aqwa.aqwa_validator import AqwaValidator

# Initialize validator
validator = AqwaValidator()

# Load results
validator.load("aqwa_results/vessel.LIS")

# Run validation checks
results = validator.validate()

# Check for common issues
if not results["symmetry_check"]:
    print("Warning: RAOs not symmetric for symmetric vessel")
if not results["low_frequency_check"]:
    print("Warning: Low frequency added mass may be inaccurate")
if not results["radiation_check"]:
    print("Warning: Radiation damping check failed")

# Kramers-Kronig causality check
kk_result = validator.kramers_kronig_check()
if not kk_result["passed"]:
    print(f"Causality violation at frequencies: {kk_result['violations']}")
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `AqwaAnalysis` | Main analysis router |
| `AqwaRAOs` | RAO computation and export |
| `AqwaReader` | File parsing (LIS, DAT, MES) |
| `AqwaPreProcess` | Input file generation |
| `AqwaPostProcess` | Results post-processing |
| `AqwaValidator` | Result validation |

## File Format Support

### LIS Files (Listing Output)

Primary output file containing:
- RAOs (amplitude and phase)
- Added mass matrices
- Damping matrices
- Wave excitation forces
- Drift forces

### DAT Files (Data Input)

Input file containing:
- Hull geometry
- Mass properties
- Analysis settings
- Wave conditions

### MES Files (Mesh)

Mesh definition:
- Panel geometry
- Node coordinates
- Panel connectivity

## Configuration Examples

### Complete AQWA Workflow

```yaml
basename: aqwa_analysis

aqwa_analysis:
  # Step 1: Process AQWA output
  file_processing:
    flag: true
    input_file: "aqwa_results/fpso.LIS"
    output_directory: "results/"

  # Step 2: Extract RAOs
  rao_extraction:
    flag: true
    wave_directions: [0, 30, 60, 90, 120, 150, 180]
    output:
      rao_file: "results/fpso_raos.csv"
      orcaflex_file: "results/fpso_raos.yml"
      plots: "results/rao_plots.html"

  # Step 3: Extract coefficients
  coefficients:
    flag: true
    output:
      added_mass: "results/added_mass.csv"
      damping: "results/damping.csv"

  # Step 4: Add viscous damping
  viscous_damping:
    flag: true
    method: "percentage_critical"
    values:
      roll: 5.0
      pitch: 3.0
      heave: 2.0

  # Step 5: Validate results
  validation:
    flag: true
    checks:
      - symmetry
      - low_frequency
      - kramers_kronig
    output:
      report: "results/validation_report.json"
```

## Output Formats

### RAO CSV Format

```csv
frequency_rad_s,direction_deg,surge_amp,surge_phase,sway_amp,sway_phase,heave_amp,heave_phase,roll_amp,roll_phase,pitch_amp,pitch_phase,yaw_amp,yaw_phase
0.100,0.0,0.985,178.2,0.000,0.0,1.023,-2.5,0.000,0.0,0.156,175.8,0.000,0.0
0.100,90.0,0.000,0.0,0.978,175.4,1.015,-3.2,2.345,-8.5,0.000,0.0,0.012,92.1
```

### Coefficient Matrices JSON

```json
{
  "frequencies_rad_s": [0.1, 0.2, 0.3, 0.5, 0.8],
  "added_mass": {
    "0.1": [[1.2e6, 0, 0, 0, 1.5e7, 0],
            [0, 1.3e6, 0, -1.2e7, 0, 0],
            ...],
    "0.2": [...]
  },
  "damping": {
    "0.1": [[2.5e5, 0, 0, 0, 3.2e6, 0],
            ...],
    "0.2": [...]
  }
}
```

## Best Practices

1. **Frequency range** - Ensure frequencies cover wave spectrum of interest
2. **Direction resolution** - Use 30° or finer for asymmetric vessels
3. **Panel density** - Verify mesh convergence for accurate results
4. **Low frequency** - Check added mass at low frequencies for stability
5. **Viscous damping** - Always add viscous damping for roll motion

## Common Issues

### Mesh Quality

```python
# Check mesh quality before running
from digitalmodel.aqwa.mesh_check import AqwaMeshCheck

mesh = AqwaMeshCheck()
mesh.load("geometry/hull.mes")
quality = mesh.check_quality()

if quality["min_aspect_ratio"] < 0.1:
    print("Warning: Poor aspect ratio panels detected")
if quality["intersecting_panels"] > 0:
    print(f"Error: {quality['intersecting_panels']} intersecting panels")
```

### Standalone DAT File Format (Non-Workbench)

Critical conventions for generating AQWA standalone `.DAT` input files (non-Workbench mode):

```
Element type:     QPPL DIFF    (NOT just QPPL — without DIFF, elements are "NON-DIFFRACTING")
ILID card:        1ILID AUTO 21  (after ZLWL — required for irregular frequency removal)
SEAG card:        SEAG (nx, ny)  (2 params only in non-Workbench mode, NOT 6-param bounding box)
OPTIONS GOON:     Continue past non-fatal errors (separate line, before feature OPTIONS)
Line length:      Max 80 columns per line (AQWA enforces strict column limits)
```

**Mesh Quality Rules (FATAL — cannot override):**
- Panels must be roughly square (aspect ratio near 1:1)
- "Facet Radius" distance check at 90° corners of box geometries
- For a 100m x 20m x 8m barge: minimum nx=40, ny=8, nz=4 (704 panels)
- `OPTIONS GOON` does NOT bypass FATAL mesh quality errors

**LIS Parsing Conventions:**
- `ADDED  MASS` header has **double space** — use whitespace normalization for matching
- WAVE FREQUENCY line appears ~23 lines before DAMPING section — search backward 30 lines
- Matrix rows in added mass/damping sections are separated by blank lines
- First RAO section = displacement RAOs; subsequent sections = velocity/acceleration (skip these)

### Result Validation

```python
# Always validate extracted coefficients
validator = AqwaValidator()
validator.load("results/vessel.LIS")

# Check physical consistency
if not validator.check_positive_definite_damping():
    print("Warning: Damping matrix not positive definite")

if not validator.check_symmetric_added_mass():
    print("Warning: Added mass matrix not symmetric")
```

## MCP Tool Integration

### Swarm Coordination
```javascript
// Initialize hydrodynamic analysis swarm
mcp__claude-flow__swarm_init { topology: "mesh", maxAgents: 4 }

// Spawn specialized agents
mcp__claude-flow__agent_spawn { type: "analyst", name: "aqwa-processor" }
mcp__claude-flow__agent_spawn { type: "code-analyzer", name: "coefficient-extractor" }
```

### Memory Coordination
```javascript
// Store extracted RAOs
mcp__claude-flow__memory_usage {
  action: "store",
  key: "aqwa/raos/vessel",
  namespace: "hydrodynamics",
  value: JSON.stringify({
    vessel: "FPSO",
    directions: [0, 45, 90, 135, 180],
    frequencies: 50,
    timestamp: Date.now()
  })
}

// Store coefficient matrices
mcp__claude-flow__memory_usage {
  action: "store",
  key: "aqwa/coefficients/added_mass",
  namespace: "hydrodynamics",
  value: JSON.stringify({
    frequency_count: 25,
    matrix_size: "6x6",
    validated: true
  })
}
```

### Phased Processing Workflow
The agent uses a phased approach for AQWA processing:
1. **Discovery**: Identify AQWA output files
2. **Quality**: Validate file integrity
3. **Extraction**: Extract RAOs and coefficients
4. **Synthesis**: Combine multi-body results
5. **Validation**: Check physical consistency
6. **Integration**: Export to OrcaFlex format

### 5. Benchmark Comparison vs OrcaWave

Compare AQWA results with OrcaWave for validation focusing on peak/significant values.

```yaml
aqwa_analysis:
  benchmark_comparison:
    flag: true
    aqwa_results: "aqwa_results/vessel.LIS"
    orcawave_results: "orcawave_results/vessel.sim"  # Optional
    tolerance: 0.05  # 5% tolerance for peaks
    peak_threshold: 0.10  # 10% of peak magnitude
    output:
      comparison_report: "results/aqwa_orcawave_comparison.html"
      peak_analysis: "results/peak_values_comparison.html"
```

### Peak-Focused Validation

**Using the Standalone Comparison Script:**

```bash
# Run peak-focused comparison (AQWA vs OrcaWave)
cd docs/modules/orcawave/L01_aqwa_benchmark
python run_comparison_peaks.py

# Output:
# - comparison_results/peak_comparison_YYYYMMDD_HHMMSS.html
# - Peak RAO values for all 6 DOFs
# - Statistical analysis focused on significant values (≥10% of peak)
```

**Script Features:**
- Extracts AQWA RAOs from `.LIS` files
- Identifies peak values for each DOF (heave, pitch, roll, surge, sway, yaw)
- Compares peaks with OrcaWave results (when available)
- Applies 5% tolerance to significant values only
- Generates interactive HTML report with visualization

**For Custom Heading-by-Heading Analysis:**

```bash
# Run comprehensive heading-by-heading comparison
cd docs/modules/orcawave/L01_aqwa_benchmark
python run_proper_comparison.py

# Output:
# - comparison_results/final_comparison_YYYYMMDD_HHMMSS.html
# - Heading-by-heading RAO comparison for all 6 DOFs
# - Statistical analysis with mean/max differences
# - Interactive plots with period-based comparison
```

**For Module-Level Integration:**

```python
# Use the diffraction comparison framework module
from digitalmodel.diffraction.comparison_framework import DiffractionComparator
from digitalmodel.diffraction.aqwa_converter import AQWAConverter

# Extract AQWA data
converter = AQWAConverter(
    analysis_folder="docs/modules/orcawave/L01_aqwa_benchmark",
    vessel_name="SHIP_RAOS"
)
aqwa_results = converter.convert_to_unified_schema(water_depth=30.0)

# Create diffraction comparator (requires both AQWA and OrcaWave results)
# comparator = DiffractionComparator(
#     aqwa_results=aqwa_results,
#     orcawave_results=orcawave_results,  # Both required
#     tolerance=0.05  # 5% tolerance
# )
#
# # Compare RAOs
# rao_comparison = comparator.compare_raos()
#
# # Generate comprehensive report
# report = comparator.generate_report()
# print(f"RAO comparison complete")

# Note: For actual benchmark analysis, use the standalone scripts above
```

## Benchmark Validation Criteria

**Engineering Standard Practice:**
- 5% tolerance applies to **peak and significant values only**
- "Significant" = RAO magnitude ≥ 10% of peak value
- Pass requires 90% of significant points within 5% tolerance
- Low-amplitude responses (<10% of peak) excluded from validation
- Focus on resonance regions and operationally important periods

**Typical Peak Values by DOF:**
- **Heave**: 0.9-1.1 m/m (near natural period)
- **Pitch**: 0.4-0.6 deg/m (near natural period)
- **Roll**: 2-5 deg/m (beam seas, low frequency)
- **Surge**: 0.8-1.0 m/m (following seas)
- **Sway**: 0.8-1.0 m/m (beam seas)
- **Yaw**: Small (<0.1 deg/m for symmetric vessels)

## Related Skills

- [diffraction-analysis](../diffraction-analysis/SKILL.md) - **Master skill** for all diffraction workflows
- [bemrosetta](../bemrosetta/SKILL.md) - AQWA → OrcaFlex conversion with QTF and mesh support
- [hydrodynamics](../hydrodynamics/SKILL.md) - Coefficient management
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Apply RAOs in OrcaFlex
- [orcawave-analysis](../orcawave-analysis/SKILL.md) - Benchmark validation
- [mooring-design](../mooring-design/SKILL.md) - Vessel motion input

## References

- ANSYS AQWA User Manual
- DNV-RP-C205: Environmental Conditions and Environmental Loads
- Newman, J.N.: Marine Hydrodynamics
- Agent Configuration: `agents/aqwa/agent.yaml`

---

## Version History

- **3.2.0** (2026-02-05): Added standalone DAT file format conventions, mesh quality rules, LIS parsing gotchas from 3-way benchmark work
- **3.1.0** (2026-01-05): Added peak-focused benchmark comparison framework, 5% tolerance validation for significant values, automated AQWA vs OrcaWave comparison scripts
- **3.0.0** (2025-01-02): Merged agent capabilities from agents/aqwa/, added MCP integration, phased processing workflow, AQWA module descriptions
- **2.0.0** (2024-11-15): Added validation and preprocessing modules
- **1.0.0** (2024-10-01): Initial release with RAO extraction and coefficient management
