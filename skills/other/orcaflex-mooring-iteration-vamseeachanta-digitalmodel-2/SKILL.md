---
name: orcaflex-mooring-iteration
description: Iterate mooring line lengths to achieve target pretensions using scipy
  optimization, Newton-Raphson, or EA-based methods. Use for mooring system design,
  pretension optimization, and CALM/SALM buoy configuration.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- mooring tension iteration
- pretension optimization
- line length adjustment
- mooring design
- target tension
- tension matching
- mooring optimization
- CALM mooring
- SALM mooring
---
# OrcaFlex Mooring Tension Iteration Skill

Automatically iterate mooring line lengths to achieve target pretensions using advanced optimization methods.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
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
- Initial release with three iteration methods
- Scipy optimization (fsolve)
- Newton-Raphson with Jacobian caching
- EA-based iteration from catenary theory
- Comprehensive reporting and convergence tracking

## When to Use

- Achieving target mooring line pretensions
- Optimizing line lengths for design loads
- CALM/SALM buoy mooring configuration
- Spread mooring system design
- Turret mooring optimization
- Multi-line tension balancing
- Mooring system verification

## Prerequisites

- OrcaFlex license (for simulation)
- Python environment with `digitalmodel` package installed
- Initial mooring model (close to target configuration)
- Target pretensions for each line

## Iteration Methods

### 1. Scipy Optimization (Recommended)

Uses `scipy.optimize.fsolve` for robust multi-variable root finding.

**Best for:**
- Well-behaved systems
- Multiple lines with coupling
- Fast convergence

### 2. Newton-Raphson

Multi-dimensional Newton-Raphson with numerical Jacobian.

**Best for:**
- Systems needing fine control
- Cases with known sensitivity
- Debugging convergence issues

### 3. EA-Based (Catenary Theory)

Uses effective axial stiffness from catenary equations.

**Best for:**
- Simple catenary systems
- Initial estimates
- Lightweight iteration

## Configuration

### Basic Configuration

```yaml
# configs/mooring_iteration.yml

iteration:
  method: "scipy"  # scipy, newton_raphson, or ea_based

  convergence:
    tolerance: 1.0          # % error tolerance
    min_tolerance: 0.5      # Minimum acceptable
    max_iterations: 50
    damping_factor: 0.7     # Under-relaxation

  jacobian:
    perturbation_factor: 0.001
    min_perturbation: 0.1   # meters
    cache_enabled: true

  vessel_config:
    fix_vessels: true
    vessels_to_fix: ["FPSO"]
    fix_degrees_of_freedom: ["X", "Y", "Z", "Rotation 1", "Rotation 2", "Rotation 3"]

lines:
  - name: "Mooring_Line_1"
    target_tension: 800.0     # kN
    tolerance: 1.0            # % specific tolerance
    variable_section: 1       # Section index to adjust

  - name: "Mooring_Line_2"
    target_tension: 800.0
    tolerance: 1.0
    variable_section: 1

  - name: "Mooring_Line_3"
    target_tension: 800.0
    tolerance: 1.0
    variable_section: 1
```

### Advanced Configuration

```yaml
# configs/mooring_iteration_advanced.yml

iteration:
  method: "newton_raphson"

  convergence:
    tolerance: 0.5
    min_tolerance: 0.2
    max_iterations: 100
    damping_factor: 0.5       # More conservative

  jacobian:
    perturbation_factor: 0.002
    min_perturbation: 0.5
    cache_enabled: true
    recompute_interval: 5     # Recompute every N iterations

  vessel_config:
    fix_vessels: true
    vessels_to_fix: ["Buoy"]
    fix_degrees_of_freedom: ["X", "Y", "Rotation 3"]

  ea_config:                  # For EA-based method
    stiffness_factor: 1.0
    length_limit_factor: 0.1  # Max 10% length change per iteration

lines:
  - name: "Chain_Segment_1"
    target_tension: 500.0
    tolerance: 0.5
    variable_section: 0
    min_length: 50.0          # Minimum allowable length
    max_length: 200.0         # Maximum allowable length
    ea_value: 1.5e9           # Axial stiffness (N)

  - name: "Wire_Segment_1"
    target_tension: 1200.0
    tolerance: 0.5
    variable_section: 1
    min_length: 100.0
    max_length: 500.0
    ea_value: 2.8e9
```

## Python API

### Basic Usage

```python
from digitalmodel.orcaflex.mooring_tension_iteration import (
    MooringTensionIterator,
    IterationConfig,
    LineConfig,
    ConvergenceConfig
)

# Define configuration
config = IterationConfig(
    method="scipy",
    convergence=ConvergenceConfig(
        tolerance=1.0,
        max_iterations=50,
        damping_factor=0.7
    ),
    lines=[
        LineConfig(name="Line1", target_tension=800.0, variable_section=1),
        LineConfig(name="Line2", target_tension=800.0, variable_section=1),
        LineConfig(name="Line3", target_tension=800.0, variable_section=1),
    ]
)

# Initialize iterator
iterator = MooringTensionIterator(config, use_mock=False)

# Load model
iterator.load_model("mooring_model.sim")

# Run iteration
result = iterator.iterate_to_targets()

# Check result
print(result.summary())
# Output: "Iteration SUCCESS: 12 iterations, Max Error=0.45%, Time=34.2s"

# Get final tensions
for line_name, tension in result.final_tensions.items():
    print(f"{line_name}: {tension:.1f} kN")

# Get final lengths
for line_name, lengths in result.final_lengths.items():
    print(f"{line_name}: sections = {lengths}")
```

### With Vessel Fixing

```python
from digitalmodel.orcaflex.mooring_tension_iteration import (
    MooringTensionIterator,
    IterationConfig,
    VesselConfig
)

config = IterationConfig(
    method="scipy",
    vessel_config=VesselConfig(
        fix_vessels=True,
        vessels_to_fix=["FPSO", "Buoy"],
        fix_degrees_of_freedom=["X", "Y", "Z", "Rotation 1", "Rotation 2", "Rotation 3"]
    ),
    lines=[...]
)

iterator = MooringTensionIterator(config)
iterator.load_model("model.sim")

# Vessels will be fixed during iteration
result = iterator.iterate_to_targets(vessel_names=["FPSO"])
```

### Convergence Monitoring

```python
# After iteration
result = iterator.iterate_to_targets()

# Access convergence history
for i, error in enumerate(result.convergence_history):
    print(f"Iteration {i+1}: Max error = {error:.2f}%")

# Plot convergence
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(result.convergence_history) + 1),
         result.convergence_history, 'b-o')
plt.axhline(y=1.0, color='r', linestyle='--', label='Tolerance')
plt.xlabel('Iteration')
plt.ylabel('Max Error (%)')
plt.title('Mooring Tension Iteration Convergence')
plt.legend()
plt.grid(True)
plt.savefig('convergence.png')
```

### Generate Report

```python
# Generate comprehensive report
report = iterator.generate_report(output_path="iteration_report.txt")
print(report)

# Report includes:
# - Configuration summary
# - Target vs achieved tensions
# - Length modifications
# - Convergence history
```

## Algorithm Details

### Scipy Method

```
1. Define objective function: residual = current_tension - target_tension
2. Optimization variables: line lengths
3. scipy.optimize.fsolve minimizes residuals
4. Length changes distributed across sections proportionally
```

### Newton-Raphson Method

```
1. Calculate Jacobian: J[i,j] = ∂T_i/∂L_j
2. Calculate residuals: r_i = T_current_i - T_target_i
3. Solve: J × ΔL = -r
4. Update: L_new = L_old + damping × ΔL
5. Repeat until convergence
```

### EA-Based Method

```
1. From catenary theory: ΔL ≈ ΔT × L / EA
2. Calculate tension error: ΔT = T_current - T_target
3. Calculate length change: ΔL = ΔT × L / EA
4. Apply with damping
5. Repeat until convergence
```

## Output

### Iteration Result

```python
@dataclass
class IterationResult:
    converged: bool               # Did iteration succeed?
    iterations: int               # Number of iterations
    final_tensions: Dict[str, float]  # Final tensions per line
    final_lengths: Dict[str, List[float]]  # Final section lengths
    max_error: float              # Final maximum error %
    execution_time: float         # Total time in seconds
    convergence_history: List[float]  # Error at each iteration
```

### Report Format

```
================================================================================
MOORING TENSION ITERATION REPORT
================================================================================

Configuration:
  Method: scipy
  Max Iterations: 50
  Tolerance: 1.0%
  Damping Factor: 0.7

Tension Results:
--------------------------------------------------------------------------------
Line Name        Target (kN)    Achieved (kN)    Error (%)    Status
--------------------------------------------------------------------------------
Mooring_Line_1   800.0          803.2            0.40         PASS
Mooring_Line_2   800.0          796.8            -0.40        PASS
Mooring_Line_3   800.0          801.5            0.19         PASS
--------------------------------------------------------------------------------

Length Modifications:
--------------------------------------------------------------------------------
Line Name        Original (m)   Final (m)        Change (m)   Change (%)
--------------------------------------------------------------------------------
Mooring_Line_1   [50, 150, 30]  [50, 148.2, 30]  -1.8         -0.79
Mooring_Line_2   [50, 150, 30]  [50, 151.5, 30]  +1.5         +0.65
Mooring_Line_3   [50, 150, 30]  [50, 149.8, 30]  -0.2         -0.09
--------------------------------------------------------------------------------

Convergence History:
  Iteration 1: 15.23%
  Iteration 2: 8.45%
  Iteration 3: 4.12%
  ...
  Iteration 12: 0.40%

================================================================================
```

## Best Practices

### Initial Model

1. **Start close to target** - Begin with reasonable pretension estimate
2. **Verify static convergence** - Model must converge before iteration
3. **Check line connectivity** - Ensure proper vessel/anchor connections
4. **Reasonable initial lengths** - Avoid extreme configurations

### Configuration

1. **Start with default damping** (0.7) - Reduce if oscillating
2. **Use appropriate method** - Scipy for most cases
3. **Set realistic tolerances** - 1% is typical for design
4. **Limit iterations** - 50-100 usually sufficient

### Troubleshooting

1. **No convergence** - Reduce damping factor
2. **Oscillating** - Increase damping, check Jacobian
3. **Slow convergence** - Check EA values, initial guess
4. **Invalid lengths** - Set min/max length limits

## Error Handling

```python
try:
    result = iterator.iterate_to_targets()
except RuntimeError as e:
    print(f"Model validation failed: {e}")
    print("Check model connectivity and initial configuration")

if not result.converged:
    print(f"Failed to converge after {result.iterations} iterations")
    print(f"Final max error: {result.max_error:.2f}%")
    print("Suggestions:")
    print("  - Reduce damping factor")
    print("  - Increase max iterations")
    print("  - Check initial configuration")
    print("  - Verify target tensions are achievable")
```

## Integration with Other Skills

### With Mooring Design

```python
# 1. Design mooring using mooring-design skill
# 2. Generate initial OrcaFlex model
# 3. Run tension iteration to achieve pretensions
# 4. Verify with dynamic analysis

from digitalmodel.orcaflex.mooring_tension_iteration import MooringTensionIterator
from digitalmodel.orcaflex.universal import UniversalOrcaFlexRunner

# Step 1: Iterate to target tensions
iterator = MooringTensionIterator(config)
iterator.load_model("initial_mooring.sim")
result = iterator.iterate_to_targets()

# Step 2: Save optimized model
# (Model state is updated in-place)

# Step 3: Run dynamic analysis
runner = UniversalOrcaFlexRunner()
runner.run_single("optimized_mooring.yml")
```

### With CALM Buoy Analysis

```python
# For CALM buoy mooring systems
config = IterationConfig(
    method="scipy",
    vessel_config=VesselConfig(
        fix_vessels=True,
        vessels_to_fix=["CALM_Buoy"],
        fix_degrees_of_freedom=["X", "Y", "Rotation 3"]
    ),
    lines=[
        LineConfig(name="Leg_1", target_tension=500.0, variable_section=0),
        LineConfig(name="Leg_2", target_tension=500.0, variable_section=0),
        LineConfig(name="Leg_3", target_tension=500.0, variable_section=0),
        LineConfig(name="Leg_4", target_tension=500.0, variable_section=0),
        LineConfig(name="Leg_5", target_tension=500.0, variable_section=0),
        LineConfig(name="Leg_6", target_tension=500.0, variable_section=0),
    ]
)
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [mooring-design](../mooring-design/SKILL.md) - Design mooring systems
- [orcaflex-line-wizard](../orcaflex-line-wizard/SKILL.md) - Configure line properties
- [catenary-riser](../catenary-riser/SKILL.md) - Catenary analysis

## References

- OrcaFlex Line Setup Wizard: Orcina Documentation
- API RP 2SK: Design and Analysis of Stationkeeping Systems
- DNV-OS-E301: Position Mooring
- Source: `src/digitalmodel/modules/orcaflex/mooring_tension_iteration/`
- Tests: `tests/modules/orcaflex/mooring-tension-iteration/`
