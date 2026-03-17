---
name: orcawave-damping-sweep
description: Viscous damping analysis specialist for OrcaWave. Handles parametric
  damping studies, roll damping optimization, critical damping calculations, and
  comparison with model test data for vessel motion tuning.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- damping sweep
- roll damping
- viscous damping study
- critical damping
- damping optimization
- bilge keel effect
- damping coefficient tuning
- model test comparison
---

# OrcaWave Damping Sweep Skill

Specialized expertise for parametric viscous damping studies and roll damping optimization in OrcaWave diffraction analysis.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  numpy: '>=1.24.0'
  scipy: '>=1.11.0'
  plotly: '>=5.15.0'
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

- Parametric studies of viscous damping effects
- Roll damping coefficient optimization
- Comparing radiation damping with viscous damping
- Tuning damping to match model test data
- Estimating bilge keel damping contribution
- Critical damping ratio calculations
- Sensitivity analysis for motion predictions
- Roll resonance mitigation studies

## Damping Components

### Total Damping Composition

```
Total Damping = Radiation Damping + Viscous Damping + Appendage Damping
                (from OrcaWave)    (user input)      (bilge keels, etc.)
```

### Damping Sources

| Source | Type | Typical Contribution |
|--------|------|---------------------|
| Radiation | Linear | 10-30% of total roll damping |
| Skin friction | Nonlinear | 5-15% |
| Eddy making | Nonlinear | 20-40% |
| Bilge keels | Nonlinear | 40-60% |
| Appendages | Mixed | 5-10% |

## Python API

### Basic Damping Sweep

```python
from digitalmodel.orcawave.damping import DampingSweep

# Initialize sweep
sweep = DampingSweep()

# Load base model
sweep.load_model("models/fpso.owr")

# Define damping values to sweep
roll_damping_values = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15]  # Fraction of critical

# Run sweep
results = sweep.run(
    parameter="roll_damping",
    values=roll_damping_values,
    output_directory="results/damping_sweep/"
)

# Analyze results
analysis = sweep.analyze_sensitivity(results)
print(f"Roll RAO sensitivity to damping: {analysis['roll_rao_sensitivity']:.2f}")

# Plot results
sweep.plot_sweep_results(
    results,
    dof="roll",
    output_file="plots/roll_damping_sweep.html"
)
```

### Multi-Parameter Sweep

```python
from digitalmodel.orcawave.damping import MultiParameterDampingSweep

# Initialize multi-parameter sweep
sweep = MultiParameterDampingSweep()

# Load model
sweep.load_model("models/fpso.owr")

# Define parameter space
sweep.configure(
    parameters={
        "roll_damping": [0.03, 0.05, 0.07, 0.10],
        "pitch_damping": [0.02, 0.03, 0.04, 0.05],
        "heave_damping": [0.01, 0.02, 0.03]
    }
)

# Run full factorial sweep
results = sweep.run_factorial(
    output_directory="results/multi_param_sweep/"
)

# Find optimal combination
optimal = sweep.find_optimal(
    results,
    objective="minimize_peak_roll",
    constraints={
        "pitch_rao_limit": 2.0,  # deg/m
        "heave_rao_limit": 1.0   # m/m
    }
)

print(f"Optimal roll damping: {optimal['roll_damping']:.2%}")
print(f"Optimal pitch damping: {optimal['pitch_damping']:.2%}")
```

### Critical Damping Calculation

```python
from digitalmodel.orcawave.damping import CriticalDampingCalculator

# Initialize calculator
calc = CriticalDampingCalculator()

# Load model with mass and stiffness
calc.load_model("models/fpso.owr")

# Calculate critical damping for each DOF
critical = calc.compute_critical_damping()

for dof, value in critical.items():
    print(f"{dof} critical damping: {value:.2e} N.s/m or N.m.s/rad")

# Get damping as percentage of critical
percent_critical = calc.damping_percent_critical(
    actual_damping={
        "roll": 5.0e8,   # N.m.s/rad
        "pitch": 8.0e9,
        "heave": 2.0e7
    }
)

for dof, pct in percent_critical.items():
    print(f"{dof}: {pct:.1%} of critical")
```

### Model Test Comparison

```python
from digitalmodel.orcawave.damping import ModelTestComparison

# Initialize comparison
comparison = ModelTestComparison()

# Load OrcaWave results
comparison.load_orcawave_results("results/fpso.owr")

# Load model test data
comparison.load_model_test_data(
    "data/model_tests/roll_decay.csv",
    format="decay_curve"
)

# Extract damping from decay tests
test_damping = comparison.extract_decay_damping(
    method="logarithmic_decrement"
)
print(f"Model test roll damping: {test_damping['roll']:.1%} critical")

# Find matching OrcaWave damping
optimal_damping = comparison.match_damping(
    dof="roll",
    target_rao=test_damping['roll_rao'],
    frequency=test_damping['roll_natural_freq']
)

print(f"Required viscous damping: {optimal_damping:.1%} critical")

# Generate comparison plot
comparison.plot_comparison(
    output_file="plots/model_test_comparison.html"
)
```

### Bilge Keel Estimation

```python
from digitalmodel.orcawave.damping import BilgeKeelDamping

# Initialize bilge keel damping estimator
bk = BilgeKeelDamping()

# Configure vessel parameters
bk.configure_vessel(
    beam=50.0,          # m
    draft=22.0,         # m
    bilge_radius=3.0,   # m
    lpp=280.0           # m
)

# Configure bilge keels
bk.add_bilge_keel(
    length=100.0,       # m
    height=1.5,         # m
    position_from_ap=90.0  # m from aft perpendicular
)

# Estimate damping contribution
bk_damping = bk.estimate_damping(
    roll_amplitude=5.0,  # degrees (nonlinear)
    roll_period=12.0     # seconds
)

print(f"Bilge keel damping: {bk_damping['percent_critical']:.1%} critical")
print(f"Equivalent linear: {bk_damping['equivalent_linear']:.2e} N.m.s/rad")

# Sensitivity to roll amplitude
amplitude_study = bk.amplitude_sensitivity(
    amplitudes=[2, 5, 10, 15, 20],  # degrees
    roll_period=12.0
)
```

### Damping-Period Relationship

```python
from digitalmodel.orcawave.damping import DampingPeriodAnalyzer

# Analyze damping vs period relationship
analyzer = DampingPeriodAnalyzer()

# Load OrcaWave radiation damping results
analyzer.load_results("models/fpso.owr")

# Extract frequency-dependent radiation damping
rad_damping = analyzer.get_radiation_damping()

# Plot damping vs frequency
analyzer.plot_damping_spectrum(
    rad_damping,
    dofs=["roll", "pitch", "heave"],
    output_file="plots/radiation_damping_spectrum.html"
)

# Identify peak damping frequencies
peaks = analyzer.find_damping_peaks()
for dof, freq in peaks.items():
    print(f"{dof} peak radiation damping at {freq:.3f} rad/s")

# Compute integrated damping metrics
metrics = analyzer.compute_metrics(
    frequency_range=(0.1, 0.8),
    dofs=["roll"]
)
print(f"Roll average radiation damping: {metrics['roll']['average']:.2e}")
```

## Configuration Examples

### Damping Sweep Configuration

```yaml
# configs/damping_sweep.yml

damping_sweep:
  model: "models/fpso.owr"

  parameters:
    roll_damping:
      type: "percent_critical"
      values: [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15]

    pitch_damping:
      type: "percent_critical"
      values: [0.02, 0.03, 0.04, 0.05]

  sweep_type: "factorial"  # or "one_at_a_time"

  analysis:
    frequencies: "from_model"  # Use frequencies from OrcaWave model
    headings: [0, 45, 90, 135, 180]

  metrics:
    - "peak_rao"
    - "rao_at_resonance"
    - "significant_response"

  output:
    directory: "results/damping_sweep/"
    plots: true
    format: "html"
```

### Model Test Comparison Configuration

```yaml
# configs/model_test_comparison.yml

model_test_comparison:
  orcawave_results: "results/fpso.owr"

  model_test_data:
    roll_decay: "data/roll_decay.csv"
    pitch_decay: "data/pitch_decay.csv"
    regular_wave_tests: "data/regular_waves.csv"

  analysis:
    decay_method: "logarithmic_decrement"
    rao_comparison: true

  damping_optimization:
    dofs: ["roll", "pitch"]
    objective: "minimize_rao_error"
    bounds:
      roll: [0.02, 0.20]
      pitch: [0.01, 0.10]

  output:
    report: "reports/damping_calibration.html"
    optimal_damping: "configs/calibrated_damping.yml"
```

## CLI Usage

```bash
# Run damping sweep
python -m digitalmodel.orcawave.damping sweep \
    --model models/fpso.owr \
    --parameter roll_damping \
    --values 0.02,0.04,0.06,0.08,0.10 \
    --output results/roll_sweep/

# Multi-parameter sweep
python -m digitalmodel.orcawave.damping multi-sweep \
    --config configs/damping_sweep.yml \
    --output results/multi_sweep/

# Calculate critical damping
python -m digitalmodel.orcawave.damping critical \
    --model models/fpso.owr \
    --output critical_damping.csv

# Compare with model tests
python -m digitalmodel.orcawave.damping compare \
    --orcawave results/fpso.owr \
    --model-test data/roll_decay.csv \
    --output reports/comparison.html

# Estimate bilge keel damping
python -m digitalmodel.orcawave.damping bilge-keel \
    --beam 50.0 --draft 22.0 \
    --bk-length 100.0 --bk-height 1.5 \
    --roll-amplitude 5.0 --roll-period 12.0

# Extract radiation damping spectrum
python -m digitalmodel.orcawave.damping spectrum \
    --model models/fpso.owr \
    --dofs roll,pitch,heave \
    --output plots/damping_spectrum.html
```

## Damping Recommendations

### Typical Values by Vessel Type

| Vessel Type | Roll Damping (% critical) | Notes |
|-------------|---------------------------|-------|
| FPSO | 5-10% | With bilge keels |
| Tanker | 3-8% | Varies with loading |
| Semi-submersible | 8-15% | Large radiation damping |
| Spar | 3-6% | Strake-dependent |
| Barge | 2-5% | Low damping |

### By Loading Condition

| Condition | Typical Adjustment |
|-----------|-------------------|
| Full load | Base value |
| Ballast | -20% to -30% |
| Partial load | -10% to -20% |
| Transit | +10% to +20% (hull exposure) |

## OrcaWave API Properties

### Damping-Related Properties

```python
# Access damping data from OrcaWave model
import OrcFxAPI

model = OrcFxAPI.DiffractionModel("fpso.owr")

# Radiation damping (frequency-dependent)
rad_damping = model.damping  # 6x6xNfreq array

# Extra roll damping (user-specified viscous)
extra_roll = model.extraRollDamping

# Roll damping as percent critical
roll_pct = model.rollDampingPercentCritical

# Hydrostatic stiffness (for critical damping calc)
stiffness = model.hydrostaticResults
```

## Best Practices

1. **Start with Radiation**: Analyze radiation damping before adding viscous
2. **Calibrate to Tests**: Match damping to model test data when available
3. **Amplitude Effects**: Remember bilge keel damping is amplitude-dependent
4. **Sensitivity Study**: Always perform sensitivity analysis
5. **Document Assumptions**: Record damping values and justification
6. **Conservative Design**: Use lower damping for conservative motion estimates
7. **Frequency Range**: Check damping at resonance frequencies

## Error Handling

```python
# Handle damping analysis errors
try:
    sweep = DampingSweep()
    sweep.load_model("models/fpso.owr")
    results = sweep.run(parameter="roll_damping", values=[0.05, 0.10])

except DampingOutOfRangeError as e:
    print(f"Damping value unrealistic: {e}")
    # Typical range 1-20% critical

except NegativeDampingError as e:
    print(f"Negative damping detected: {e}")
    # Check model setup

except ConvergenceError as e:
    print(f"Analysis did not converge: {e}")
    # Reduce damping or check mesh
```

## Related Skills

- [orcawave-analysis](../orcawave-analysis/SKILL.md) - OrcaWave diffraction analysis
- [orcawave-to-orcaflex](../orcawave-to-orcaflex/SKILL.md) - Export with damping
- [hydrodynamics](../hydrodynamics/SKILL.md) - Coefficient management
- [viv-analysis](../viv-analysis/SKILL.md) - Vibration damping

## References

- Himeno, Y.: Prediction of Ship Roll Damping - State of the Art
- Ikeda, Y.: Prediction Methods of Roll Damping of Ships
- OrcaWave Roll Damping Documentation
- Script: `scripts/python/digitalmodel/modules/run_orcawave_damping_sweep.py`

---

**Version History**

- **1.0.0** (2026-01-17): Initial release with damping sweep, model test comparison, and bilge keel estimation
