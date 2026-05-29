---
name: viv-analysis
description: Assess vortex-induced vibration (VIV) for risers and tubular members
  with natural frequency and safety factor calculations. Use for VIV susceptibility
  analysis, natural frequency calculation, vortex shedding assessment, and tubular
  member fatigue from VIV.
updated: '2026-01-07'
---
# VIV Analysis Skill

Assess vortex-induced vibration (VIV) susceptibility for risers and tubular members with natural frequency calculations and safety factor evaluation.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  structural-analysis: '>=1.0.0,<2.0.0'
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

- VIV analysis for risers and pipelines
- Natural frequency calculation for tubular members
- Vortex shedding frequency analysis
- VIV fatigue damage assessment
- Tubular member VIV screening
- Safety factor evaluation against VIV criteria

## Prerequisites

- Python environment with `digitalmodel` package installed
- Member geometry and material properties
- Current velocity profiles
- For risers: tension distribution along length

## Analysis Types

### 1. Natural Frequency Analysis

Calculate natural frequencies for tubular members.

```yaml
viv_analysis:
  natural_frequency:
    flag: true
    member:
      length: 50.0
      outer_diameter: 0.5
      wall_thickness: 0.025
      material:
        youngs_modulus: 207e9
        density: 7850
      boundary_conditions: "pinned-pinned"  # or fixed-fixed, fixed-pinned
    added_mass:
      coefficient: 1.0
      fluid_density: 1025
    output:
      frequencies_file: "results/natural_frequencies.json"
      mode_shapes_file: "results/mode_shapes.csv"
```

### 2. Vortex Shedding Assessment

Evaluate vortex shedding frequencies against natural frequencies.

```yaml
viv_analysis:
  vortex_shedding:
    flag: true
    member:
      outer_diameter: 0.5
      length: 50.0
    current_profile:
      type: "power_law"  # or uniform, linear, custom
      surface_velocity: 1.5
      power_exponent: 0.143
    strouhal_number: 0.2
    output:
      shedding_frequencies: "results/vortex_shedding.csv"
      lock_in_check: "results/lock_in_analysis.json"
```

### 3. VIV Susceptibility Screening

Quick screening for VIV susceptibility.

```yaml
viv_analysis:
  screening:
    flag: true
    members:
      - name: "Riser1"
        outer_diameter: 0.273
        length: 1500.0
        natural_frequency: 0.15
      - name: "Jumper1"
        outer_diameter: 0.2032
        length: 30.0
        natural_frequency: 2.5
    current_velocity: 1.2
    criteria:
      reduced_velocity_min: 4.0
      reduced_velocity_max: 8.0
    output:
      screening_report: "results/viv_screening.json"
```

### 4. Tubular Member VIV Analysis

Complete VIV analysis for tubular members per design codes.

```yaml
viv_analysis:
  tubular_members:
    flag: true
    members:
      - name: "Brace1"
        geometry:
          outer_diameter: 0.324
          wall_thickness: 0.0127
          length: 12.0
        end_conditions: "fixed-fixed"
        effective_length_factor: 0.7
    environment:
      current_velocity: 1.0
      water_depth: 100.0
    design_code: "DNV-RP-C205"
    output:
      analysis_report: "results/tubular_viv_analysis.json"
      safety_factors: "results/viv_safety_factors.csv"
```

## Python API

### Natural Frequency Calculation

```python
from digitalmodel.modules.viv_analysis.viv_analysis import VIVAnalysis
from digitalmodel.modules.viv_analysis.viv_tubular_members import VIVTubularMembers

# Initialize analysis
viv = VIVAnalysis()

# Define member properties
member = {
    "length": 50.0,
    "outer_diameter": 0.5,
    "wall_thickness": 0.025,
    "youngs_modulus": 207e9,
    "density": 7850,
    "boundary_conditions": "pinned-pinned"
}

# Calculate natural frequencies
frequencies = viv.calculate_natural_frequencies(
    member,
    n_modes=5,
    added_mass_coefficient=1.0,
    fluid_density=1025
)

for i, freq in enumerate(frequencies):
    print(f"Mode {i+1}: {freq:.3f} Hz, Period: {1/freq:.3f} s")
```

### Vortex Shedding Analysis

```python
# Vortex shedding frequency
diameter = 0.5  # meters
current_velocity = 1.5  # m/s
strouhal = 0.2

shedding_freq = viv.vortex_shedding_frequency(
    diameter=diameter,
    velocity=current_velocity,
    strouhal_number=strouhal
)
print(f"Shedding frequency: {shedding_freq:.3f} Hz")

# Reduced velocity
natural_freq = 0.15  # Hz
reduced_velocity = viv.reduced_velocity(
    velocity=current_velocity,
    frequency=natural_freq,
    diameter=diameter
)
print(f"Reduced velocity: {reduced_velocity:.2f}")

# Lock-in check
is_lock_in = viv.check_lock_in(
    reduced_velocity=reduced_velocity,
    vr_min=4.0,
    vr_max=8.0
)
print(f"Lock-in condition: {is_lock_in}")
```

### Tubular Member Analysis

```python
from digitalmodel.modules.viv_analysis.viv_tubular_members import VIVTubularMembers

# Initialize tubular member analysis
tubular = VIVTubularMembers()

# Define member
member_props = {
    "name": "Brace1",
    "outer_diameter": 0.324,
    "wall_thickness": 0.0127,
    "length": 12.0,
    "end_conditions": "fixed-fixed",
    "effective_length_factor": 0.7,
    "youngs_modulus": 207e9,
    "steel_density": 7850
}

# Run analysis
results = tubular.analyze(
    member=member_props,
    current_velocity=1.0,
    water_depth=100.0,
    design_code="DNV-RP-C205"
)

print(f"Natural frequency: {results['natural_frequency']:.3f} Hz")
print(f"Shedding frequency: {results['shedding_frequency']:.3f} Hz")
print(f"Reduced velocity: {results['reduced_velocity']:.2f}")
print(f"VIV susceptible: {results['is_susceptible']}")
print(f"Safety factor: {results['safety_factor']:.2f}")
```

### VIV Fatigue Assessment

```python
from digitalmodel.modules.viv_analysis.viv_fatigue import VIVFatigue

# Initialize VIV fatigue analysis
viv_fatigue = VIVFatigue()

# Calculate VIV-induced stress range
stress_range = viv_fatigue.calculate_stress_range(
    amplitude=0.5,  # VIV amplitude in diameters
    diameter=0.324,
    wall_thickness=0.0127,
    mode_shape="first_mode"
)

# Calculate fatigue damage from VIV
damage = viv_fatigue.calculate_damage(
    stress_range=stress_range,
    frequency=0.5,  # Hz
    duration=3600,  # seconds
    sn_curve="DNV-D"
)
print(f"VIV fatigue damage: {damage:.6f}")
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `VIVAnalysis` | Main VIV analysis router |
| `VIVTubularMembers` | Tubular member assessment |
| `VIVAnalysisComponents` | Component-level analysis |
| `VIVFatigue` | VIV-induced fatigue damage |

## VIV Parameters

### Strouhal Number

| Geometry | Strouhal Number |
|----------|-----------------|
| Smooth cylinder | 0.2 |
| Rough cylinder | 0.21 |
| Straked cylinder | 0.14-0.18 |

### Reduced Velocity Ranges

| Condition | Reduced Velocity Range |
|-----------|----------------------|
| Cross-flow VIV onset | 4 - 8 |
| In-line VIV onset | 1 - 3.5 |
| Lock-in region | 5 - 7 |

### Added Mass Coefficients

| Configuration | Ca |
|---------------|-----|
| Circular cylinder in infinite fluid | 1.0 |
| Near seabed (gap/D = 0.5) | 1.2 |
| Near seabed (gap/D = 0.1) | 2.0 |

## Configuration Examples

### Complete VIV Screening Workflow

```yaml
basename: viv_screening

viv_analysis:
  # Step 1: Natural frequencies for all members
  natural_frequencies:
    flag: true
    members:
      - name: "Riser"
        length: 1500.0
        outer_diameter: 0.273
        wall_thickness: 0.0159
        boundary: "tension_controlled"
        top_tension: 500e3
      - name: "Jumper"
        length: 25.0
        outer_diameter: 0.2032
        wall_thickness: 0.0127
        boundary: "fixed-fixed"

  # Step 2: Current profile analysis
  current_analysis:
    flag: true
    profiles:
      - name: "1-year"
        surface_velocity: 0.8
      - name: "100-year"
        surface_velocity: 1.5

  # Step 3: VIV susceptibility
  susceptibility:
    flag: true
    criteria: "DNV-RP-C205"
    output:
      report: "results/viv_susceptibility.html"
      summary: "results/viv_summary.json"
```

## Output Formats

### Natural Frequencies JSON

```json
{
  "member_name": "Riser1",
  "n_modes": 5,
  "frequencies": [0.15, 0.42, 0.78, 1.21, 1.72],
  "periods": [6.67, 2.38, 1.28, 0.83, 0.58],
  "boundary_conditions": "tension_controlled",
  "effective_tension": 500000.0
}
```

### VIV Screening Report

```json
{
  "member": "Brace1",
  "natural_frequency_hz": 2.5,
  "shedding_frequency_hz": 0.62,
  "reduced_velocity": 4.94,
  "is_susceptible": true,
  "lock_in_margin": 0.94,
  "safety_factor": 1.02,
  "recommendation": "VIV suppression required"
}
```

## Best Practices

1. **Include added mass** - Always account for added mass in frequency calculations
2. **Conservative Strouhal** - Use appropriate Strouhal for surface roughness
3. **Multiple modes** - Check several natural frequency modes
4. **Current profiles** - Use depth-varying current profiles
5. **Safety margins** - Apply appropriate safety factors per design code

## Design Code References

| Code | Application |
|------|-------------|
| DNV-RP-C205 | Environmental conditions and loads |
| DNV-RP-F105 | Free spanning pipelines |
| API RP 2A-WSD | Fixed offshore platforms |
| ISO 13819-2 | Fixed steel structures |

## Related Skills

- [catenary-riser](../catenary-riser/SKILL.md) - Riser configuration
- [fatigue-analysis](../fatigue-analysis/SKILL.md) - VIV fatigue damage
- [structural-analysis](../structural-analysis/SKILL.md) - Stress verification

## References

- DNV-RP-C205: Environmental Conditions and Environmental Loads
- DNV-RP-F105: Free Spanning Pipelines
- Blevins, R.D.: Flow-Induced Vibration
