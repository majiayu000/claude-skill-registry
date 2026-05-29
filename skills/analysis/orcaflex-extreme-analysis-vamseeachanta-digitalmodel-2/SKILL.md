---
name: orcaflex-extreme-analysis
description: Extract extreme response values with linked statistics from OrcaFlex
  simulations. Use for design load identification, max/min extraction with associated
  values, and extreme event characterization.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- extreme analysis
- max tension
- linked statistics
- extreme values
- design loads
- maximum response
- associated values
- peak extraction
---
# OrcaFlex Extreme Analysis Skill

Extract extreme response values with linked statistics for design load identification and extreme event characterization.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  orcaflex-post-processing: '>=1.0.0,<2.0.0'
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
- Initial release with linked statistics extraction
- Max/min value extraction with timestamps
- Associated variable extraction at extremes
- Batch processing across multiple simulations

## When to Use

- Extracting maximum/minimum values from simulations
- Identifying design loads for structural analysis
- Finding associated values at extreme events
- Characterizing vessel motions at peak tensions
- Riser curvature at maximum tension conditions
- Wave conditions at extreme responses
- Multi-variable correlation at extremes

## Prerequisites

- OrcaFlex simulation results (.sim files)
- Python environment with `digitalmodel` package installed
- Knowledge of variables to extract (object names, variable names)

## Key Concepts

### Linked Statistics

Linked statistics capture what other variables were doing when a primary variable reached its extreme:

```
At time T_max when Line1.Tension = MAX:
  - Vessel.Heave = ?
  - Vessel.Pitch = ?
  - Line1.Curvature = ?
  - Wave.Elevation = ?
```

This enables understanding of the physical conditions that caused the extreme.

### Extreme Types

| Statistic | Description |
|-----------|-------------|
| `Max` | Maximum value during simulation |
| `Min` | Minimum value during simulation |
| `TimeOfMax` | Time when maximum occurred |
| `TimeOfMin` | Time when minimum occurred |
| `ValueAtMax` | Primary variable's max value |
| `ValueAtMin` | Primary variable's min value |
| `LinkedValueAtMax` | Secondary variable value at primary's max time |
| `LinkedValueAtMin` | Secondary variable value at primary's min time |

## Configuration

### Basic Extreme Extraction

```yaml
# configs/extreme_analysis.yml

orcaflex:
  postprocess:
    linked_statistics:
      flag: true

      # Primary variable (extremes will be found for this)
      primary:
        object: "Mooring_Line_1"
        variable: "Effective Tension"

      # Linked variables (values at primary's extremes)
      linked:
        - object: "Vessel"
          variable: "Heave"
        - object: "Vessel"
          variable: "Pitch"
        - object: "Vessel"
          variable: "Roll"
        - object: "Vessel"
          variable: "X"

      # Statistics to extract
      statistics:
        - "Max"
        - "Min"
        - "TimeOfMax"
        - "TimeOfMin"
        - "LinkedValueAtMax"
        - "LinkedValueAtMin"

      output:
        format: csv
        directory: "results/extremes/"
```

### Multi-Object Analysis

```yaml
# configs/extreme_multi_object.yml

orcaflex:
  postprocess:
    linked_statistics:
      flag: true

      # Analyze multiple primary objects
      groups:
        - name: "mooring_tensions"
          primaries:
            - object: "Leg_1"
              variable: "Effective Tension"
            - object: "Leg_2"
              variable: "Effective Tension"
            - object: "Leg_3"
              variable: "Effective Tension"
          linked:
            - object: "CALM_Buoy"
              variable: "X"
            - object: "CALM_Buoy"
              variable: "Y"

        - name: "vessel_motions"
          primaries:
            - object: "Tanker"
              variable: "Heave"
            - object: "Tanker"
              variable: "Pitch"
          linked:
            - object: "Hawser"
              variable: "Effective Tension"

      output:
        format: csv
        directory: "results/extremes/"
        separate_files: true
```

## Python API

### Basic Linked Statistics

```python
from digitalmodel.orcaflex.opp_linkedstatistics import OPPLinkedStatistics

# Initialize extractor
extractor = OPPLinkedStatistics()

# Configure extraction
config = {
    "primary": {
        "object": "Mooring_Line_1",
        "variable": "Effective Tension"
    },
    "linked": [
        {"object": "Vessel", "variable": "Heave"},
        {"object": "Vessel", "variable": "Pitch"},
        {"object": "Vessel", "variable": "Roll"}
    ]
}

# Extract from simulation
results = extractor.extract_linked_statistics(
    sim_file="results/mooring_analysis.sim",
    config=config
)

# Access results
print(f"Max Tension: {results['Max']:.1f} kN")
print(f"Time of Max: {results['TimeOfMax']:.2f} s")
print(f"Heave at Max Tension: {results['LinkedValueAtMax']['Heave']:.2f} m")
print(f"Pitch at Max Tension: {results['LinkedValueAtMax']['Pitch']:.2f} deg")
```

### Direct OrcFxAPI Usage

```python
import OrcFxAPI
from pathlib import Path

def extract_extremes_with_linked(sim_file: str, config: dict) -> dict:
    """
    Extract extreme values with linked statistics.

    Args:
        sim_file: Path to .sim file
        config: Configuration dictionary

    Returns:
        Dictionary with extreme values and linked values
    """
    model = OrcFxAPI.Model(sim_file)

    # Get primary object
    primary_obj = model[config["primary"]["object"]]
    primary_var = config["primary"]["variable"]

    # Get time history
    time_history = primary_obj.TimeHistory(primary_var, period=None)
    times = primary_obj.SampleTimes(period=None)

    # Find extremes
    max_idx = time_history.argmax()
    min_idx = time_history.argmin()

    results = {
        "Max": float(time_history[max_idx]),
        "Min": float(time_history[min_idx]),
        "TimeOfMax": float(times[max_idx]),
        "TimeOfMin": float(times[min_idx]),
        "LinkedValueAtMax": {},
        "LinkedValueAtMin": {}
    }

    # Extract linked values at extreme times
    for linked_config in config["linked"]:
        linked_obj = model[linked_config["object"]]
        linked_var = linked_config["variable"]

        linked_history = linked_obj.TimeHistory(linked_var, period=None)

        results["LinkedValueAtMax"][linked_var] = float(linked_history[max_idx])
        results["LinkedValueAtMin"][linked_var] = float(linked_history[min_idx])

    return results

# Example usage
config = {
    "primary": {"object": "Line1", "variable": "Effective Tension"},
    "linked": [
        {"object": "Vessel", "variable": "Heave"},
        {"object": "Vessel", "variable": "Pitch"}
    ]
}

results = extract_extremes_with_linked("simulation.sim", config)
```

### Batch Extreme Analysis

```python
from digitalmodel.orcaflex.opp_linkedstatistics import OPPLinkedStatistics
from pathlib import Path
import pandas as pd

def batch_extreme_analysis(sim_directory: str, config: dict) -> pd.DataFrame:
    """
    Extract extremes from multiple simulations.
    """
    extractor = OPPLinkedStatistics()

    sim_files = list(Path(sim_directory).glob("*.sim"))
    all_results = []

    for sim_file in sim_files:
        try:
            results = extractor.extract_linked_statistics(
                sim_file=str(sim_file),
                config=config
            )

            results["file"] = sim_file.stem
            all_results.append(results)

        except Exception as e:
            print(f"Error processing {sim_file}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(all_results)

    # Find overall extremes
    overall_max = df.loc[df["Max"].idxmax()]
    overall_min = df.loc[df["Min"].idxmin()]

    print(f"Overall Max: {overall_max['Max']:.1f} kN in {overall_max['file']}")
    print(f"Overall Min: {overall_min['Min']:.1f} kN in {overall_min['file']}")

    return df

# Run batch analysis
results_df = batch_extreme_analysis(
    sim_directory="results/.sim/",
    config=config
)
results_df.to_csv("extreme_summary.csv", index=False)
```

### Range Graph Extremes

```python
from digitalmodel.orcaflex.opp_range_graph import OPPRangeGraph

# Extract range graph (min/max/mean along arc length)
range_extractor = OPPRangeGraph()

config = {
    "object": "Riser",
    "variables": ["Effective Tension", "Curvature", "Bend Moment"],
    "arc_length_range": [0, 1500]  # meters
}

range_data = range_extractor.extract_range_graph(
    sim_file="riser_analysis.sim",
    config=config
)

# Find critical location
max_curvature_idx = range_data["Curvature"]["Max"].argmax()
critical_arc_length = range_data["arc_length"][max_curvature_idx]

print(f"Maximum curvature at arc length: {critical_arc_length:.1f} m")
print(f"Curvature value: {range_data['Curvature']['Max'][max_curvature_idx]:.6f} 1/m")
```

## Output Formats

### Linked Statistics CSV

```csv
File,Primary_Object,Primary_Variable,Max,Min,TimeOfMax,TimeOfMin,Heave_AtMax,Pitch_AtMax,Roll_AtMax,Heave_AtMin,Pitch_AtMin,Roll_AtMin
case_001,Mooring_Line_1,Effective Tension,2450.5,320.1,1823.4,2156.7,3.2,-1.5,0.8,-2.1,0.9,-0.3
case_002,Mooring_Line_1,Effective Tension,2380.2,345.6,1567.2,1890.3,2.8,-1.2,0.5,-1.8,0.7,-0.2
```

### Extreme Summary Report

```json
{
  "simulation": "mooring_100yr.sim",
  "primary": {
    "object": "Mooring_Line_1",
    "variable": "Effective Tension",
    "units": "kN"
  },
  "extremes": {
    "maximum": {
      "value": 2450.5,
      "time": 1823.4,
      "linked_values": {
        "Vessel.Heave": 3.2,
        "Vessel.Pitch": -1.5,
        "Vessel.Roll": 0.8
      }
    },
    "minimum": {
      "value": 320.1,
      "time": 2156.7,
      "linked_values": {
        "Vessel.Heave": -2.1,
        "Vessel.Pitch": 0.9,
        "Vessel.Roll": -0.3
      }
    }
  }
}
```

## Common Use Cases

### 1. Design Load Identification

```python
# Find maximum tension for structural design
config = {
    "primary": {"object": "Riser", "variable": "Wall Tension"},
    "linked": [
        {"object": "Riser", "variable": "Curvature"},
        {"object": "Riser", "variable": "Bend Moment"}
    ]
}

results = extractor.extract_linked_statistics(sim_file, config)
design_tension = results["Max"] * 1.1  # Add 10% margin
```

### 2. VIV Characterization

```python
# Characterize conditions at maximum amplitude
config = {
    "primary": {"object": "Riser", "variable": "Max Amplitude"},
    "linked": [
        {"object": "Environment", "variable": "Current Velocity"},
        {"object": "Riser", "variable": "Inline Frequency"}
    ]
}
```

### 3. Mooring Load Case

```python
# Extract design load case for mooring
config = {
    "primary": {"object": "Hawser", "variable": "Effective Tension"},
    "linked": [
        {"object": "Tanker", "variable": "X"},
        {"object": "Tanker", "variable": "Y"},
        {"object": "Tanker", "variable": "Heading"}
    ]
}

# Results define the design load case
```

## Best Practices

### Variable Selection

1. **Primary variable** - Choose the most critical response
2. **Linked variables** - Include relevant causative factors
3. **Physical correlation** - Select variables that explain the extreme

### Time Range

1. **Exclude ramp-up** - Skip initial transient period
2. **Statistical period** - Use 3-hour simulation for design
3. **Multiple seeds** - Consider seed variability

### Reporting

1. **Context** - Include simulation parameters
2. **Units** - Always specify units
3. **Uncertainty** - Note seed sensitivity if applicable

## Error Handling

```python
try:
    results = extractor.extract_linked_statistics(sim_file, config)
except OrcFxAPI.OrcaFlexError as e:
    print(f"OrcaFlex error: {e}")
    print("Check object names and variable specifications")

except FileNotFoundError:
    print("Simulation file not found")
```

## Related Skills

- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - General post-processing
- [orcaflex-operability](../orcaflex-operability/SKILL.md) - Multi-sea-state analysis
- [orcaflex-results-comparison](../orcaflex-results-comparison/SKILL.md) - Compare multiple results
- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Fatigue from time histories

## References

- OrcaFlex Results: Linked Statistics
- OrcFxAPI Documentation
- Source: `src/digitalmodel/modules/orcaflex/opp_linkedstatistics.py`
- Source: `src/digitalmodel/modules/orcaflex/opp_range_graph.py`
