---
name: hydrodynamics
description: "Manage hydrodynamic coefficients, wave spectra, and environmental loading\
  \ for vessel response analysis. Use for 6\xD76 matrix management, wave spectrum\
  \ modeling, OCIMF loading calculations, and RAO interpolation."
updated: '2026-01-07'
---
# Hydrodynamics Skill

Manage hydrodynamic coefficients, wave spectra, and environmental loading for vessel and floater response analysis.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
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

- 6×6 added mass and damping matrix management
- Wave spectrum modeling (JONSWAP, Bretschneider, PM)
- OCIMF wind and current loading calculations
- RAO interpolation and frequency-dependent coefficients
- Hydrodynamic coefficient database management
- Kramers-Kronig causality validation

## Prerequisites

- Python environment with `digitalmodel` package installed
- Hydrodynamic coefficient data (from AQWA, WAMIT, etc.)
- Environmental data for wave/wind/current loading

## Analysis Types

### 1. Coefficient Database Management

Store and retrieve hydrodynamic coefficients.

```yaml
hydrodynamics:
  coefficient_database:
    flag: true
    vessel_name: "FPSO"
    source_file: "data/hydro_coefficients.json"
    coefficients:
      - added_mass
      - damping
      - wave_excitation
    output:
      database_file: "results/coefficient_db.json"
```

### 2. Wave Spectra Modeling

Generate and analyze wave spectra.

```yaml
hydrodynamics:
  wave_spectra:
    flag: true
    spectrum_type: "jonswap"  # jonswap, bretschneider, pm, custom
    parameters:
      hs: 3.5  # Significant wave height (m)
      tp: 10.0  # Peak period (s)
      gamma: 3.3  # JONSWAP peakedness
    frequency_range:
      min: 0.02
      max: 0.5
      n_points: 100
    output:
      spectrum_file: "results/wave_spectrum.csv"
      plot_file: "results/spectrum_plot.html"
```

### 3. OCIMF Environmental Loading

Calculate wind and current loads per OCIMF guidelines.

```yaml
hydrodynamics:
  ocimf_loading:
    flag: true
    vessel:
      length: 300.0
      beam: 50.0
      draft: 20.0
      displacement: 200000
    environment:
      wind_speed: 25.0
      wind_direction: 45.0
      current_speed: 1.5
      current_direction: 90.0
    output:
      loads_file: "results/ocimf_loads.json"
```

### 4. RAO Interpolation

Interpolate RAOs across frequencies and directions.

```yaml
hydrodynamics:
  rao_interpolation:
    flag: true
    input_raos: "data/vessel_raos.csv"
    target_frequencies: [0.05, 0.1, 0.15, 0.2, 0.25]
    target_directions: [0, 30, 60, 90, 120, 150, 180]
    method: "cubic"  # linear, cubic, spline
    output:
      interpolated_file: "results/interpolated_raos.csv"
```

### 5. Displacement RAO Quality Checks

Validate displacement RAO data for physical correctness and consistency.

```yaml
hydrodynamics:
  rao_quality_check:
    flag: true
    input_file: "data/vessel_raos.yml"  # OrcaFlex format
    vessel_type: auto  # auto, ship, fpso, semi_submersible, spar, barge
    tolerances:
      amplitude: 0.05  # 5% tolerance
      phase: 10.0      # 10 degrees tolerance
    checks:
      - long_period_phase  # Phase angles at T → infinity
      - peak_detection     # Natural period validation
      - vessel_type_detection
    output:
      html_report: "reports/rao_qa/quality_report.html"
      csv_summary: "reports/rao_qa/quality_summary.csv"
```

**Quality Checks:**
- **Long Period Phase**: Validates phase angles approach expected values as period → infinity (Orcina convention)
- **Peak Detection**: Identifies resonance peaks and validates against vessel type natural period ranges
- **Vessel Type Detection**: Auto-detects vessel type from RAO characteristics with confidence score
- **Active DOF Validation**: Checks appropriate DOFs are active for each wave heading

## Python API

### Coefficient Database

```python
from digitalmodel.hydrodynamics.coefficient_database import CoefficientDatabase

# Initialize database
db = CoefficientDatabase()

# Store coefficients
db.store(
    vessel_name="FPSO",
    frequency=0.1,
    added_mass=added_mass_matrix,  # 6x6 numpy array
    damping=damping_matrix         # 6x6 numpy array
)

# Retrieve coefficients
A, B = db.get_matrices(vessel_name="FPSO", frequency=0.1)

# Get all frequencies
frequencies = db.get_frequencies("FPSO")
```

### Frequency-Dependent Matrices

```python
from digitalmodel.hydrodynamics.freq_dependent import FrequencyDependentMatrix

# Initialize with frequency-dependent data
fdm = FrequencyDependentMatrix()
fdm.load("hydro_data.json")

# Interpolate to specific frequency
A_interp = fdm.interpolate_added_mass(frequency=0.15)
B_interp = fdm.interpolate_damping(frequency=0.15)

# Get infinite frequency added mass
A_inf = fdm.get_infinite_frequency_added_mass()
```

### Wave Spectra

```python
from digitalmodel.hydrodynamics.wave_spectra import WaveSpectra

# Create JONSWAP spectrum
spectrum = WaveSpectra()
frequencies, S = spectrum.jonswap(
    hs=3.5,       # Significant wave height (m)
    tp=10.0,      # Peak period (s)
    gamma=3.3,    # Peakedness parameter
    freq_min=0.02,
    freq_max=0.5,
    n_points=100
)

# Alternative spectra
freq, S_pm = spectrum.pierson_moskowitz(hs=3.5, tp=10.0)
freq, S_bs = spectrum.bretschneider(hs=3.5, tp=10.0)

# Calculate spectral moments
m0 = spectrum.spectral_moment(frequencies, S, n=0)
m2 = spectrum.spectral_moment(frequencies, S, n=2)
Tz = np.sqrt(m0/m2)  # Zero-crossing period
```

### OCIMF Loading

```python
from digitalmodel.hydrodynamics.ocimf_loading import OCIMFLoading

# Initialize calculator
ocimf = OCIMFLoading()

# Define vessel
vessel = {
    "length": 300.0,
    "beam": 50.0,
    "draft": 20.0,
    "displacement": 200000
}

# Calculate wind load
wind_load = ocimf.wind_load(
    vessel=vessel,
    wind_speed=25.0,
    wind_direction=45.0  # degrees from bow
)
# Returns: {"Fx": ..., "Fy": ..., "Mz": ...}

# Calculate current load
current_load = ocimf.current_load(
    vessel=vessel,
    current_speed=1.5,
    current_direction=90.0
)
```

### Coefficient Interpolation

```python
from digitalmodel.hydrodynamics.interpolator import CoefficientsInterpolator

# Initialize interpolator
interp = CoefficientsInterpolator()

# Load RAO data
interp.load_raos("vessel_raos.csv")

# Interpolate to new frequencies
new_freqs = [0.05, 0.1, 0.15, 0.2]
interpolated = interp.interpolate_frequencies(new_freqs, method="cubic")

# Interpolate to new directions
new_dirs = [0, 45, 90, 135, 180]
interpolated = interp.interpolate_directions(new_dirs)
```

### Causality Validation

```python
from digitalmodel.hydrodynamics.validation import HydroValidator

# Initialize validator
validator = HydroValidator()

# Load frequency-dependent coefficients
validator.load_coefficients("hydro_data.json")

# Kramers-Kronig check
kk_result = validator.kramers_kronig_check()
if not kk_result["passed"]:
    print(f"Causality issues at: {kk_result['violations']}")

# Check matrix properties
sym_check = validator.check_symmetry()
pd_check = validator.check_positive_definite()
```

### Displacement RAO Quality Checks

```python
import yaml
from digitalmodel.marine_ops.marine_analysis import (
    RAODataValidators,
    VesselType,
    DisplacementRAOQualityReport
)
from digitalmodel.marine_ops.marine_analysis.rao_quality_report import RAOQualityReportGenerator

# Load OrcaFlex RAO data
with open("vessel_raos.yml", 'r') as f:
    rao_data = yaml.safe_load(f)

# Initialize validators
validators = RAODataValidators()

# Run quality check (auto-detects vessel type)
report = validators.validate_displacement_rao_quality(
    rao_data,
    source_file="vessel_raos.yml",
    vessel_type=None,  # Auto-detect, or specify VesselType.SHIP
    amplitude_tolerance=0.05,  # 5%
    phase_tolerance=10.0       # degrees
)

# Access results
print(f"Vessel Type: {report.vessel_type.value}")
print(f"Confidence: {report.vessel_type_confidence:.1%}")
print(f"Overall Status: {report.overall_status}")
print(f"Pass Rate: {report.pass_rate:.1f}%")
print(f"Total/Passed/Warnings/Failed: {report.total_checks}/{report.passed_checks}/{report.warning_checks}/{report.failed_checks}")

# Check phase results
for check in report.phase_checks:
    if check.status == 'FAIL':
        print(f"FAIL: {check.dof} @ {check.heading}° - {check.message}")

# Check peak detection results
for check in report.peak_checks:
    print(f"{check.dof}: Peak at {check.peak_period:.1f}s (expected {check.expected_range[0]:.1f}-{check.expected_range[1]:.1f}s)")

# Generate HTML report
generator = RAOQualityReportGenerator(output_dir="reports/rao_qa")
html_path = generator.generate_html_report(report, report_name="vessel_quality")
print(f"HTML report: {html_path}")

# Export CSV summary
csv_path = generator.export_csv_summary(report, report_name="vessel_summary")
print(f"CSV summary: {csv_path}")

# Get active DOFs for a heading
active_dofs = RAODataValidators.get_active_dofs_for_heading(180.0)
print(f"Active DOFs at head seas: {active_dofs}")
# Output: ['surge', 'heave', 'pitch']
```

**Wave Direction Convention:**
- 0° = Head seas (waves from bow, approaching vessel)
- 90° = Beam seas from starboard
- 180° = Following seas (waves from stern)
- 270° = Beam seas from port

**Expected Long Period Values (Orcina Convention):**

| DOF | Head Seas (0°) | Beam Seas (90°) | Following (180°) |
|-----|----------------|-----------------|------------------|
| Surge | Amp=1.0, Phase=-90° | Inactive | Amp=1.0, Phase=90° |
| Sway | Inactive | Amp=1.0, Phase=-90° | Inactive |
| Heave | Amp=1.0, Phase=0° | Amp=1.0, Phase=0° | Amp=1.0, Phase=0° |
| Roll | Inactive | Amp=1.0, Phase=-90° | Inactive |
| Pitch | Amp=1.0, Phase=90° | Inactive | Amp=1.0, Phase=-90° |
| Yaw | Inactive | Inactive | Inactive |

**Phase Convention Support:**
- `PhaseConvention.ORCINA` - Phase lag from wave crest (OrcaFlex, OrcaWave)
- `PhaseConvention.ISO_6954` - Phase lead over wave (AQWA, WAMIT)
- Auto-detection based on file extension (.yml → Orcina, .lis → ISO)

## Key Classes

| Class | Purpose |
|-------|---------|
| `CoefficientDatabase` | Coefficient storage and retrieval |
| `FrequencyDependentMatrix` | 6×6 matrix interpolation |
| `WaveSpectra` | Spectrum generation (JONSWAP, PM, etc.) |
| `OCIMFLoading` | OCIMF wind/current calculations |
| `CoefficientsInterpolator` | 2D interpolation (freq × direction) |
| `HydroValidator` | Kramers-Kronig and matrix validation |
| `RAODataValidators` | RAO quality checks (phase, peaks, vessel type) |
| `RAOQualityReportGenerator` | HTML/CSV quality report generation |

## Wave Spectrum Types

| Spectrum | Application |
|----------|-------------|
| JONSWAP | Fetch-limited seas (North Sea) |
| Pierson-Moskowitz | Fully developed seas |
| Bretschneider | General two-parameter spectrum |
| ISSC | Modified Pierson-Moskowitz |
| Ochi-Hubble | Bimodal sea states |

## Output Formats

### Coefficient Database JSON

```json
{
  "vessel_name": "FPSO",
  "frequencies_rad_s": [0.1, 0.2, 0.3],
  "added_mass": {
    "0.1": [[1.2e6, 0, 0, 0, 1.5e7, 0], ...],
    "0.2": [[1.1e6, 0, 0, 0, 1.4e7, 0], ...]
  },
  "damping": {
    "0.1": [[2.5e5, 0, 0, 0, 3.2e6, 0], ...],
    "0.2": [[2.8e5, 0, 0, 0, 3.5e6, 0], ...]
  }
}
```

### Wave Spectrum CSV

```csv
frequency_rad_s,frequency_hz,period_s,spectral_density
0.314,0.050,20.0,0.123
0.628,0.100,10.0,2.456
0.942,0.150,6.67,1.234
```

## Best Practices

1. **Frequency range** - Cover full wave spectrum of interest (typically 0.02-0.5 rad/s)
2. **Direction convention** - Use consistent direction convention (from/to, bow=0°)
3. **Unit consistency** - Verify units (rad/s vs Hz, degrees vs radians)
4. **Causality check** - Validate coefficients with Kramers-Kronig before use
5. **Matrix symmetry** - Verify added mass symmetry for physical consistency

## Related Skills

- [diffraction-analysis](../diffraction-analysis/SKILL.md) - **Master skill** for all diffraction workflows
- [aqwa-analysis](../aqwa-analysis/SKILL.md) - Extract coefficients from AQWA
- [bemrosetta](../bemrosetta/SKILL.md) - AQWA → OrcaFlex conversion with QTF and mesh support
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Apply in OrcaFlex models
- [viv-analysis](../viv-analysis/SKILL.md) - Hydrodynamic coefficient usage

## References

- DNV-RP-C205: Environmental Conditions and Environmental Loads
- OCIMF: Mooring Equipment Guidelines
- Newman, J.N.: Marine Hydrodynamics
