---
name: orcaflex-line-wizard
description: Configure OrcaFlex line properties and use the Line Setup Wizard for
  automatic tension/length calculations. Use for mooring line configuration, riser
  setup, and achieving target line properties.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- line setup wizard
- line configuration
- target tension
- line length calculation
- mooring line setup
- riser configuration
- line properties
- segment configuration
---
# OrcaFlex Line Wizard Skill

Configure OrcaFlex lines and use the Line Setup Wizard for automated tension and length calculations.

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
- Initial release with Line Setup Wizard integration
- Target tension and length calculation modes
- Multi-line configuration support

## When to Use

- Setting up mooring lines with target pretensions
- Configuring riser lines with specified top tensions
- Calculating line lengths for given tension targets
- Calculating tensions for given line lengths
- Multi-line mooring system configuration
- Initial model setup before detailed analysis

## OrcaFlex Line Setup Wizard

The Line Setup Wizard is an OrcaFlex built-in tool that automatically calculates:
- **Line lengths** to achieve target tensions
- **Tensions** for specified line lengths

### Calculation Modes

| Mode | Input | Output |
|------|-------|--------|
| "Calculate line lengths" | Target tension | Required lengths |
| "Calculate tensions" | Line lengths | Resulting tensions |

## Python API

### Basic Line Setup

```python
import OrcFxAPI

# Load model
model = OrcFxAPI.Model("mooring_model.dat")

# Configure Line Setup Wizard
model.general.LineSetupCalculationMode = "Calculate line lengths"
model.general.LineSetupMaxDamping = 20  # For numerical stability

# Configure line 1 for target tension
line1 = model["Mooring_Line_1"]
line1.LineSetupTargetVariable = "Tension"
line1.LineSetupLineEnd = "End A"          # Measure tension at End A
line1.LineSetupTargetValue = 800.0        # Target 800 kN

# Configure line 2 similarly
line2 = model["Mooring_Line_2"]
line2.LineSetupTargetVariable = "Tension"
line2.LineSetupLineEnd = "End A"
line2.LineSetupTargetValue = 800.0

# Exclude line 3 from wizard (keep current configuration)
line3 = model["Mooring_Line_3"]
line3.LineSetupIncluded = "No"

# Run the wizard
model.InvokeLineSetupWizard()

# The model now has adjusted line lengths
# Save the result
model.SaveData("mooring_model_adjusted.dat")
```

### Comprehensive Line Configuration

```python
import OrcFxAPI
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LineSetupConfig:
    """Configuration for a line in the setup wizard."""
    name: str
    target_variable: str = "Tension"  # "Tension" or "Length"
    line_end: str = "End A"           # "End A" or "End B"
    target_value: float = 0.0         # kN for tension, m for length
    included: bool = True


def configure_line_setup(
    model: OrcFxAPI.Model,
    configs: List[LineSetupConfig],
    calculation_mode: str = "Calculate line lengths",
    max_damping: float = 20.0
) -> dict:
    """
    Configure and run the Line Setup Wizard.

    Args:
        model: OrcaFlex model
        configs: List of line configurations
        calculation_mode: "Calculate line lengths" or "Calculate tensions"
        max_damping: Maximum damping for solver

    Returns:
        Dictionary with results for each line
    """
    # Store original values
    original_lengths = {}
    original_tensions = {}

    # Configure wizard
    model.general.LineSetupCalculationMode = calculation_mode
    model.general.LineSetupMaxDamping = max_damping

    # Configure each line
    for config in configs:
        line = model[config.name]

        # Store original
        original_lengths[config.name] = list(line.Length)

        if config.included:
            line.LineSetupIncluded = "Yes"
            line.LineSetupTargetVariable = config.target_variable
            line.LineSetupLineEnd = config.line_end
            line.LineSetupTargetValue = config.target_value
        else:
            line.LineSetupIncluded = "No"

    # Run wizard
    model.InvokeLineSetupWizard()

    # Collect results
    results = {}
    for config in configs:
        line = model[config.name]

        # Get new lengths
        new_lengths = list(line.Length)

        # Calculate statics to get tensions
        model.CalculateStatics()

        results[config.name] = {
            "original_lengths": original_lengths[config.name],
            "new_lengths": new_lengths,
            "length_change": sum(new_lengths) - sum(original_lengths[config.name]),
            "target_value": config.target_value,
            "included": config.included
        }

    return results


# Example usage
configs = [
    LineSetupConfig(
        name="Mooring_Line_1",
        target_variable="Tension",
        line_end="End A",
        target_value=800.0,
        included=True
    ),
    LineSetupConfig(
        name="Mooring_Line_2",
        target_variable="Tension",
        line_end="End A",
        target_value=850.0,
        included=True
    ),
    LineSetupConfig(
        name="Riser_1",
        included=False  # Exclude from wizard
    )
]

model = OrcFxAPI.Model("model.dat")
results = configure_line_setup(model, configs)

for line_name, result in results.items():
    if result["included"]:
        print(f"{line_name}:")
        print(f"  Target: {result['target_value']} kN")
        print(f"  Length change: {result['length_change']:.2f} m")
```

### Line Section Configuration

```python
def configure_line_sections(
    model: OrcFxAPI.Model,
    line_name: str,
    sections: list
) -> None:
    """
    Configure line sections with multiple line types.

    Args:
        model: OrcaFlex model
        line_name: Name of the line
        sections: List of section configurations

    Example sections:
        [
            {"LineType": "Chain_84mm", "Length": 50.0, "TargetSegmentLength": 5.0},
            {"LineType": "Wire_76mm", "Length": 200.0, "TargetSegmentLength": 10.0},
            {"LineType": "Chain_84mm", "Length": 50.0, "TargetSegmentLength": 5.0}
        ]
    """
    line = model[line_name]

    # Set number of sections
    line.NumberOfSections = len(sections)

    # Configure each section
    for i, section in enumerate(sections):
        line.LineType[i] = section["LineType"]
        line.Length[i] = section["Length"]
        line.TargetSegmentLength[i] = section.get("TargetSegmentLength", 10.0)


# Example: Configure a typical mooring line
sections = [
    {"LineType": "Chain_R4_84mm", "Length": 50.0, "TargetSegmentLength": 5.0},
    {"LineType": "Polyester_Rope", "Length": 800.0, "TargetSegmentLength": 20.0},
    {"LineType": "Chain_R4_84mm", "Length": 50.0, "TargetSegmentLength": 5.0}
]

configure_line_sections(model, "Mooring_Line_1", sections)
```

## Configuration Examples

### YAML-Based Line Setup

```yaml
# configs/line_setup.yml

line_setup:
  calculation_mode: "Calculate line lengths"
  max_damping: 50

  lines:
    - name: "Mooring_Leg_1"
      target_variable: "Tension"
      line_end: "End A"
      target_value: 500.0      # kN
      included: true

    - name: "Mooring_Leg_2"
      target_variable: "Tension"
      line_end: "End A"
      target_value: 500.0
      included: true

    - name: "Mooring_Leg_3"
      target_variable: "Tension"
      line_end: "End A"
      target_value: 500.0
      included: true

    - name: "Mooring_Leg_4"
      target_variable: "Tension"
      line_end: "End A"
      target_value: 500.0
      included: true
```

### Multi-Segment Line Configuration

```yaml
# configs/line_sections.yml

lines:
  - name: "Catenary_Mooring_1"
    sections:
      - line_type: "Chain_R4_84mm"
        length: 80.0
        segment_length: 4.0

      - line_type: "Polyester_128mm"
        length: 1200.0
        segment_length: 25.0

      - line_type: "Chain_R4_84mm"
        length: 200.0
        segment_length: 5.0

    end_a:
      connection: "Vessel"
      object: "FPSO"
      position: [-150, 0, -20]

    end_b:
      connection: "Anchored"
      position: [-1800, 0, -1500]
```

## Line Properties Reference

### Common Line Setup Properties

| Property | Description | Values |
|----------|-------------|--------|
| `LineSetupIncluded` | Include in wizard | "Yes", "No" |
| `LineSetupTargetVariable` | What to target | "Tension", "Length" |
| `LineSetupLineEnd` | Where to measure | "End A", "End B" |
| `LineSetupTargetValue` | Target value | kN or m |

### Line Type Properties

| Property | Description | Units |
|----------|-------------|-------|
| `OD` | Outer diameter | m |
| `ID` | Inner diameter | m |
| `MassPerUnitLength` | Mass in air | kg/m |
| `EA` | Axial stiffness | N |
| `EI` | Bending stiffness | N.m² |
| `GJ` | Torsional stiffness | N.m² |
| `Cdx` | Drag coefficient (axial) | - |
| `Cdn` | Drag coefficient (normal) | - |
| `Cmx` | Added mass coeff (axial) | - |
| `Cmn` | Added mass coeff (normal) | - |

## Best Practices

### Before Using Line Setup Wizard

1. **Verify model loads correctly**
2. **Check all line connections**
3. **Ensure valid line types**
4. **Set reasonable initial lengths**

### Damping Settings

| Model Complexity | Recommended Damping |
|------------------|---------------------|
| Simple (1-4 lines) | 10-20 |
| Medium (5-10 lines) | 20-50 |
| Complex (10+ lines) | 50-100 |

### Target Values

1. **Use realistic tensions** based on design requirements
2. **Consider environmental loads** in final tension targets
3. **Account for line weight** in water
4. **Check against breaking loads**

## Error Handling

### Common Issues

```python
try:
    model.InvokeLineSetupWizard()
except OrcFxAPI.OrcaFlexError as e:
    error_msg = str(e)

    if "did not converge" in error_msg.lower():
        print("Wizard failed to converge")
        print("Try:")
        print("  - Increase MaxDamping")
        print("  - Check target values are achievable")
        print("  - Verify line lengths are reasonable")

    elif "line" in error_msg.lower() and "not found" in error_msg.lower():
        print("Line not found - check line names")

    else:
        print(f"Error: {e}")
```

### Validation After Wizard

```python
def validate_wizard_results(model, configs):
    """Validate that wizard achieved targets."""
    model.CalculateStatics()

    validation = {"passed": True, "results": []}

    for config in configs:
        if not config.included:
            continue

        line = model[config.name]

        # Get actual tension at specified end
        if config.line_end == "End A":
            actual = line.StaticResult("Effective Tension", OrcFxAPI.oeEndA)
        else:
            actual = line.StaticResult("Effective Tension", OrcFxAPI.oeEndB)

        target = config.target_value
        error_pct = abs(actual - target) / target * 100

        result = {
            "line": config.name,
            "target": target,
            "actual": actual,
            "error_pct": error_pct,
            "passed": error_pct < 1.0  # 1% tolerance
        }

        validation["results"].append(result)

        if not result["passed"]:
            validation["passed"] = False

    return validation
```

## Integration with Other Skills

### With Mooring Iteration

```python
# Use Line Setup Wizard for initial configuration
# Then use mooring-iteration skill for fine-tuning

# Step 1: Line Setup Wizard for rough adjustment
model.general.LineSetupCalculationMode = "Calculate line lengths"
model["Line1"].LineSetupTargetValue = 800.0
model.InvokeLineSetupWizard()

# Step 2: Fine-tune with iteration skill
from digitalmodel.modules.orcaflex.mooring_tension_iteration import MooringTensionIterator
iterator = MooringTensionIterator(config)
iterator.load_model("adjusted_model.dat")
result = iterator.iterate_to_targets()
```

### With Model Generator

```python
# Generate model from template
from digitalmodel.modules.orcaflex.model_generator import generate_model

model = generate_model(
    template="mooring/spread_mooring",
    config=mooring_config,
    output="initial_model.yml"
)

# Use Line Setup Wizard to achieve target pretensions
import OrcFxAPI
ofx_model = OrcFxAPI.Model("initial_model.yml")
# Configure and run wizard...
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-mooring-iteration](../orcaflex-mooring-iteration/SKILL.md) - Advanced tension iteration
- [mooring-design](../mooring-design/SKILL.md) - Design mooring systems
- [orcaflex-static-debug](../orcaflex-static-debug/SKILL.md) - Troubleshoot convergence

## References

- OrcaFlex Help: Line Setup Wizard
- OrcFxAPI Documentation: Model.InvokeLineSetupWizard()
- Source: `src/digitalmodel/modules/orcaflex/orcaflex_model_linesetup_wizard.py`
