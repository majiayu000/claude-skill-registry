---
name: orcawave-qtf-analysis
description: Second-order wave force specialist for QTF (Quadratic Transfer Function)
  computation in OrcaWave. Handles mean drift, difference-frequency, sum-frequency
  forces, and slow-drift response analysis for offshore structures.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- QTF computation
- quadratic transfer function
- mean drift force
- second order wave forces
- difference frequency
- sum frequency
- slow drift
- Newman approximation
- full QTF
---

# OrcaWave QTF Analysis Skill

Specialized expertise for second-order wave force computation using Quadratic Transfer Functions in OrcaWave.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  numpy: '>=1.24.0'
  scipy: '>=1.11.0'
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

- Computing mean drift forces for mooring analysis
- Generating full QTF matrices for slow-drift response
- Difference-frequency force calculation
- Sum-frequency force calculation (springing)
- Newman approximation vs full QTF comparison
- Deep water vs shallow water second-order effects
- Moored vessel slow-drift motion prediction

## Second-Order Theory Overview

### Force Components

| Component | Frequency | Application |
|-----------|-----------|-------------|
| Mean Drift | Zero (DC) | Steady mooring loads |
| Difference-Frequency | Low frequency | Slow drift, resonance |
| Sum-Frequency | High frequency | Springing, ringing |

### Methods

| Method | Accuracy | Computation Time | Use Case |
|--------|----------|------------------|----------|
| Newman Approximation | Moderate | Fast | Initial design |
| Full QTF | High | Slow | Detailed analysis |
| Pressure Integration | High | Moderate | Validation |
| Momentum Conservation | High | Moderate | Deep water |

## Python API

### Basic QTF Computation

```python
from digitalmodel.modules.orcawave.qtf import OrcaWaveQTF

# Initialize QTF analysis
qtf = OrcaWaveQTF()

# Load OrcaWave model with first-order results
qtf.load_model("models/fpso.owr")

# Configure QTF computation
qtf.configure(
    compute_mean_drift=True,
    compute_difference_frequency=True,
    compute_sum_frequency=False,  # Optional
    headings=[0, 45, 90, 135, 180],
    frequency_pairs="diagonal"  # or "full"
)

# Run QTF analysis
results = qtf.compute()

# Extract mean drift forces
mean_drift = results.get_mean_drift()
print(f"Surge drift at 0 deg: {mean_drift['surge'][0]:.2f} kN/m²")

# Extract difference-frequency QTF
diff_qtf = results.get_difference_qtf()
```

### Full QTF Matrix Generation

```python
from digitalmodel.modules.orcawave.qtf import FullQTFComputation

# Initialize full QTF computation
full_qtf = FullQTFComputation()

# Configure frequency pairs
full_qtf.configure(
    frequencies=np.linspace(0.02, 0.5, 25),  # rad/s
    heading_pairs=[
        (0, 0),    # Co-linear
        (0, 45),   # Cross seas
        (45, 45),
        (90, 90),
    ],
    dofs=['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
)

# Run computation
qtf_matrix = full_qtf.compute("models/fpso.owr")

# Export to OrcaFlex format
full_qtf.export_to_orcaflex(
    qtf_matrix,
    output_file="orcaflex_models/fpso_qtf.yml"
)
```

### Newman Approximation

```python
from digitalmodel.modules.orcawave.qtf import NewmanApproximation

# Initialize Newman approximation
newman = NewmanApproximation()

# Load first-order results
newman.load_first_order_results("results/fpso_raos.csv")

# Compute approximate QTF
approx_qtf = newman.compute(
    frequencies=np.linspace(0.02, 0.5, 50),
    headings=[0, 45, 90, 135, 180]
)

# Compare with full QTF
comparison = newman.compare_with_full_qtf(
    full_qtf_results=full_qtf_matrix,
    approx_qtf_results=approx_qtf
)

print(f"Newman approximation error: {comparison['max_error']:.1%}")
```

### Mean Drift Analysis

```python
from digitalmodel.modules.orcawave.qtf import MeanDriftAnalyzer

# Initialize analyzer
drift = MeanDriftAnalyzer()

# Load OrcaWave results
drift.load_results("models/fpso.owr")

# Extract mean drift by method
drift_pressure = drift.get_mean_drift(method="pressure_integration")
drift_momentum = drift.get_mean_drift(method="momentum_conservation")
drift_control = drift.get_mean_drift(method="control_surface")

# Compare methods
comparison = drift.compare_methods()
print(f"Method agreement: {comparison['agreement']:.1%}")

# Export for mooring analysis
drift.export_for_mooring(
    output_file="mooring/mean_drift_forces.csv",
    wave_height=3.0,  # Hs
    format="OrcaFlex"
)
```

### Slow Drift Response

```python
from digitalmodel.modules.orcawave.qtf import SlowDriftResponse

# Initialize slow drift analysis
slow_drift = SlowDriftResponse()

# Load QTF data
slow_drift.load_qtf("results/fpso_qtf.yml")

# Configure sea state
slow_drift.configure_sea_state(
    spectrum="JONSWAP",
    hs=4.0,  # Significant wave height (m)
    tp=10.0,  # Peak period (s)
    gamma=3.3,
    spreading="cos2s",
    spreading_exponent=4
)

# Compute slow drift spectrum
response = slow_drift.compute_response(
    dofs=['Surge', 'Sway', 'Yaw'],
    include_viscous_damping=True
)

# Get statistics
print(f"Surge slow drift std dev: {response['surge']['std']:.2f} m")
print(f"Yaw slow drift std dev: {np.degrees(response['yaw']['std']):.2f} deg")

# Plot response spectrum
slow_drift.plot_response_spectrum(
    response,
    output_file="plots/slow_drift_spectrum.html"
)
```

## Configuration Examples

### QTF Analysis Configuration

```yaml
# configs/qtf_analysis.yml

qtf_analysis:
  model:
    file: "models/fpso.owr"

  computation:
    mean_drift: true
    difference_frequency: true
    sum_frequency: false

  methods:
    mean_drift: "momentum_conservation"  # or "pressure_integration"
    qtf: "full"  # or "newman"

  frequencies:
    min: 0.02  # rad/s
    max: 0.50
    count: 25

  headings:
    pairs:
      - [0, 0]
      - [0, 30]
      - [0, 60]
      - [30, 30]
      - [60, 60]
      - [90, 90]

  dofs:
    - Surge
    - Sway
    - Heave
    - Roll
    - Pitch
    - Yaw

  output:
    directory: "results/qtf/"
    formats: ["orcaflex", "csv", "json"]
```

### Slow Drift Configuration

```yaml
# configs/slow_drift.yml

slow_drift:
  qtf_source: "results/qtf/fpso_full_qtf.yml"

  sea_states:
    - name: "operational"
      hs: 2.5
      tp: 8.0
      spectrum: "JONSWAP"
      gamma: 3.3

    - name: "design"
      hs: 5.0
      tp: 12.0
      spectrum: "JONSWAP"
      gamma: 2.5

    - name: "survival"
      hs: 8.0
      tp: 14.0
      spectrum: "JONSWAP"
      gamma: 2.0

  mooring:
    stiffness:
      surge: 50000  # kN/m
      sway: 45000
      yaw: 1.5e8  # kN.m/rad
    damping:
      surge: 0.05  # fraction of critical
      sway: 0.05
      yaw: 0.05

  output:
    statistics: true
    time_series: true
    spectra: true
```

## OrcaWave API Properties for QTF

### Available Data

```python
# Mean drift loads (3 methods available)
mean_drift_pressure = model.meanDriftLoadPressureIntegration
mean_drift_momentum = model.meanDriftLoadMomentumConservation
mean_drift_control = model.meanDriftLoadControlSurface

# QTF data structure
qtf_freqs = model.QTFFrequencies
qtf_periods = model.QTFPeriods
qtf_heading_pairs = model.QTFHeadingPairs

# Quadratic loads
quad_pressure = model.quadraticLoadFromPressureIntegration
quad_control = model.quadraticLoadFromControlSurface
direct_potential = model.directPotentialLoad
indirect_potential = model.indirectPotentialLoad
```

### Heading Pair Management

```python
from digitalmodel.modules.orcawave.qtf import QTFHeadingManager

# Manage QTF heading pairs
manager = QTFHeadingManager()

# Define heading pairs for bi-directional seas
pairs = manager.generate_pairs(
    headings=[0, 30, 60, 90, 120, 150, 180],
    pair_type="symmetric"  # Reduce computation using symmetry
)

# Filter for specific conditions
crossing_pairs = manager.filter_pairs(
    pairs,
    min_difference=30,  # Minimum heading difference
    max_difference=90   # Maximum heading difference
)
```

## CLI Usage

```bash
# Compute full QTF
python -m digitalmodel.modules.orcawave.qtf compute \
    --model models/fpso.owr \
    --method full \
    --output results/qtf/

# Mean drift extraction
python -m digitalmodel.modules.orcawave.qtf mean-drift \
    --model models/fpso.owr \
    --method momentum \
    --output results/mean_drift.csv

# Newman approximation
python -m digitalmodel.modules.orcawave.qtf newman \
    --raos results/fpso_raos.csv \
    --output results/newman_qtf.yml

# Slow drift analysis
python -m digitalmodel.modules.orcawave.qtf slow-drift \
    --qtf results/qtf/fpso_full.yml \
    --hs 4.0 --tp 10.0 \
    --output results/slow_drift/

# Export to OrcaFlex
python -m digitalmodel.modules.orcawave.qtf export \
    --qtf results/qtf/fpso_full.yml \
    --format orcaflex \
    --output orcaflex_models/fpso_qtf.yml
```

## Best Practices

### When to Use Full QTF vs Newman

| Scenario | Recommendation |
|----------|----------------|
| Initial design | Newman approximation |
| Mooring design | Full QTF |
| Shallow water (d < 100m) | Full QTF required |
| Deep water (d > 300m) | Newman often sufficient |
| Bi-directional seas | Full QTF |
| Long-crested seas | Newman acceptable |
| SPM/turret systems | Full QTF |

### Computational Considerations

1. **Frequency Resolution**: Use 20-30 frequencies minimum for accurate QTF
2. **Heading Pairs**: Exploit symmetry to reduce computation
3. **Memory**: Full QTF matrices can be large; consider frequency range
4. **Validation**: Compare Newman vs Full for at least one condition
5. **Mesh Quality**: QTF more sensitive to mesh than first-order

### Integration with Mooring Analysis

```python
from digitalmodel.modules.orcawave.qtf import QTFMooringIntegration

# Prepare QTF for mooring analysis
integration = QTFMooringIntegration()

# Load QTF results
integration.load_qtf("results/qtf/fpso_full.yml")

# Convert to mooring analysis format
integration.export_for_mooring_analysis(
    output_file="mooring/qtf_loading.yml",
    format="OrcaFlex",
    include_mean_drift=True,
    include_slow_drift=True,
    sea_state={
        "hs": 4.0,
        "tp": 10.0,
        "gamma": 3.3
    }
)
```

## Error Handling

```python
# Handle QTF computation errors
try:
    results = qtf.compute()
except InsufficientFrequencyResolutionError as e:
    print(f"Need finer frequency resolution: {e}")
    # Increase frequency count
    qtf.configure(frequencies=np.linspace(0.02, 0.5, 50))
    results = qtf.compute()

except HeadingPairError as e:
    print(f"Invalid heading pair configuration: {e}")

except ConvergenceError as e:
    print(f"QTF computation did not converge: {e}")
    # Try different method
    results = qtf.compute(method="control_surface")
```

## Related Skills

- [orcawave-analysis](../orcawave-analysis/SKILL.md) - First-order diffraction analysis
- [mooring-design](../mooring-design/SKILL.md) - Mooring system design
- [hydrodynamics](../hydrodynamics/SKILL.md) - Wave loading management
- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Time-domain simulation

## References

- Pinkster, J.A.: Low Frequency Second Order Wave Exciting Forces
- Newman, J.N.: Second-Order Wave Forces on a Vertical Cylinder
- Standing, R.G.: Low Frequency Wave Drift Forces
- OrcaWave QTF Documentation

---

**Version History**

- **1.0.0** (2026-01-17): Initial release with full QTF, Newman approximation, and slow drift analysis
