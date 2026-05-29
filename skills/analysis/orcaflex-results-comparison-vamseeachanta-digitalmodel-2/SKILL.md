---
name: orcaflex-results-comparison
description: Compare results across multiple OrcaFlex simulations for design verification,
  sensitivity studies, and configuration comparison. Includes pretension, stiffness,
  and force distribution analysis.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- compare simulations
- results comparison
- sensitivity study
- design comparison
- configuration comparison
- pretension comparison
- stiffness comparison
- mooring comparison
---
# OrcaFlex Results Comparison Skill

Compare results across multiple OrcaFlex simulations for design verification, sensitivity studies, and configuration analysis.

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
- Initial release with multi-simulation comparison
- Pretension and stiffness comparison
- Force distribution analysis
- Visualization and reporting

## When to Use

- Comparing design alternatives
- Sensitivity analysis (depth, heading, sea state)
- Baseline vs modified configuration
- Design verification against target values
- Multi-configuration optimization
- Mooring system comparison
- Installation sequence comparison

## Prerequisites

- Multiple OrcaFlex simulation results (.sim files or extracted CSV)
- Python environment with `digitalmodel` package installed
- Consistent variable naming across simulations

## Comparison Types

### 1. Pretension Comparison

Compare mooring line pretensions across configurations.

### 2. Stiffness Comparison

Compare system stiffness (directional and coupled).

### 3. Force Distribution

Compare force distribution among lines.

### 4. Response Comparison

Compare dynamic responses (tensions, motions).

## Configuration

### Basic Comparison

```yaml
# configs/comparison_config.yml

comparison:
  # Simulations to compare
  simulations:
    - name: "Baseline"
      path: "results/baseline/.sim/mooring_analysis.sim"
    - name: "Modified_Chain"
      path: "results/modified/.sim/mooring_analysis.sim"
    - name: "Increased_Pretension"
      path: "results/high_pretension/.sim/mooring_analysis.sim"

  # Variables to compare
  variables:
    - object_pattern: "Mooring_Line_*"
      variable: "Effective Tension"
      statistic: "max"
    - object: "Vessel"
      variable: "X"
      statistic: "std"  # Standard deviation (offset)

  output:
    directory: "reports/comparison/"
    format: "html"
    include_plots: true
```

### Mooring System Comparison

```yaml
# configs/mooring_comparison.yml

comparison:
  type: "mooring_system"

  configurations:
    - name: "6-Leg Catenary"
      directory: "results/6leg_catenary/"
    - name: "8-Leg Catenary"
      directory: "results/8leg_catenary/"
    - name: "6-Leg Taut"
      directory: "results/6leg_taut/"

  analyses:
    pretension:
      enabled: true
      target_values:
        bow: 800.0     # kN
        stern: 800.0
        spring: 600.0

    stiffness:
      enabled: true
      compare_terms:
        - "K_xx"  # Surge stiffness
        - "K_yy"  # Sway stiffness
        - "K_xy"  # Coupling

    line_forces:
      enabled: true
      group_by:
        bow: ["Leg_1", "Leg_2"]
        stern: ["Leg_3", "Leg_4"]
        spring: ["Leg_5", "Leg_6"]

  output:
    report_name: "mooring_comparison"
    include_plots: true
```

## Python API

### Basic Comparison

```python
from digitalmodel.orcaflex.analysis.comparative import MooringComparativeAnalysis
from pathlib import Path

# Initialize analyzer
analyzer = MooringComparativeAnalysis(
    results_directory=Path("results/")
)

# Compare pretensions
pretension_comparison = analyzer.compare_pretensions(
    configurations=["baseline", "modified"],
    target_tensions={
        "Leg_1": 800.0,
        "Leg_2": 800.0,
        "Leg_3": 800.0,
        "Leg_4": 800.0
    }
)

# Display results
for config, results in pretension_comparison.items():
    print(f"\n{config}:")
    for line, data in results.items():
        print(f"  {line}: {data['actual']:.1f} kN "
              f"(target: {data['target']:.1f}, error: {data['error_pct']:.1f}%)")
```

### Stiffness Comparison

```python
from digitalmodel.orcaflex.analysis.comparative import MooringComparativeAnalysis

analyzer = MooringComparativeAnalysis(results_directory=Path("results/"))

# Compare stiffness matrices
stiffness_comparison = analyzer.compare_stiffness(
    configurations=["6_leg", "8_leg", "taut_leg"]
)

# Results structure:
# {
#     "6_leg": {
#         "K_xx": 1250.5,  # kN/m
#         "K_yy": 1180.2,
#         "K_zz": 850.0,
#         "K_xy": -45.2,
#         "T_surge": 120.5,  # Natural period (s)
#         "T_sway": 125.3,
#         "T_heave": 145.2
#     },
#     "8_leg": {...},
#     "taut_leg": {...}
# }

# Find configuration with highest surge stiffness
best_surge = max(stiffness_comparison.items(),
                 key=lambda x: x[1]["K_xx"])
print(f"Best surge stiffness: {best_surge[0]} ({best_surge[1]['K_xx']:.1f} kN/m)")
```

### Line Force Distribution

```python
from digitalmodel.orcaflex.analysis.comparative import MooringComparativeAnalysis

analyzer = MooringComparativeAnalysis(results_directory=Path("results/"))

# Compare force distribution by line groups
force_comparison = analyzer.compare_line_stiffness_distribution(
    configurations=["baseline", "optimized"],
    line_groups={
        "bow": ["Leg_1", "Leg_2"],
        "stern": ["Leg_3", "Leg_4"],
        "spring": ["Leg_5", "Leg_6"]
    }
)

# Results show force contribution per group
for config, groups in force_comparison.items():
    print(f"\n{config}:")
    total_force = sum(g["total_force"] for g in groups.values())
    for group_name, data in groups.items():
        pct = data["total_force"] / total_force * 100
        print(f"  {group_name}: {data['total_force']:.1f} kN ({pct:.1f}%)")
```

### Multi-Simulation Response Comparison

```python
import OrcFxAPI
from pathlib import Path
import pandas as pd
import numpy as np

def compare_simulation_responses(
    sim_files: list,
    config: dict
) -> pd.DataFrame:
    """
    Compare responses across multiple simulations.

    Args:
        sim_files: List of .sim file paths
        config: Configuration with objects and variables

    Returns:
        DataFrame with comparison results
    """
    results = []

    for sim_file in sim_files:
        model = OrcFxAPI.Model(str(sim_file))

        row = {"simulation": Path(sim_file).stem}

        for var_config in config["variables"]:
            obj = model[var_config["object"]]
            var = var_config["variable"]

            time_history = obj.TimeHistory(var, period=None)

            # Calculate statistics
            row[f"{var_config['object']}_{var}_max"] = float(time_history.max())
            row[f"{var_config['object']}_{var}_min"] = float(time_history.min())
            row[f"{var_config['object']}_{var}_mean"] = float(time_history.mean())
            row[f"{var_config['object']}_{var}_std"] = float(time_history.std())

        results.append(row)

    return pd.DataFrame(results)

# Example usage
sim_files = list(Path("results/.sim/").glob("*.sim"))

config = {
    "variables": [
        {"object": "Mooring_Line_1", "variable": "Effective Tension"},
        {"object": "Vessel", "variable": "X"},
        {"object": "Vessel", "variable": "Heave"}
    ]
}

comparison_df = compare_simulation_responses(sim_files, config)

# Find simulation with maximum tension
max_tension_sim = comparison_df.loc[
    comparison_df["Mooring_Line_1_Effective Tension_max"].idxmax()
]
print(f"Maximum tension in: {max_tension_sim['simulation']}")
```

### Sensitivity Analysis

```python
def sensitivity_analysis(
    parameter_name: str,
    parameter_values: list,
    result_variable: str,
    results: pd.DataFrame
) -> dict:
    """
    Analyze sensitivity of result to parameter.
    """
    sensitivity = {
        "parameter": parameter_name,
        "values": parameter_values,
        "results": results[result_variable].tolist()
    }

    # Calculate sensitivity gradient
    if len(parameter_values) > 1:
        gradients = np.gradient(
            sensitivity["results"],
            parameter_values
        )
        sensitivity["gradient"] = gradients.tolist()
        sensitivity["max_sensitivity"] = float(np.max(np.abs(gradients)))

    return sensitivity

# Example: Water depth sensitivity
depths = [800, 1000, 1200, 1400, 1600]
results_df = compare_simulation_responses(
    [f"results/depth_{d}m.sim" for d in depths],
    config
)

sensitivity = sensitivity_analysis(
    parameter_name="Water Depth (m)",
    parameter_values=depths,
    result_variable="Mooring_Line_1_Effective Tension_max",
    results=results_df
)

print(f"Maximum sensitivity: {sensitivity['max_sensitivity']:.2f} kN/m")
```

## Visualization

### Comparison Bar Chart

```python
import plotly.graph_objects as go

def create_comparison_bar_chart(
    comparison_df: pd.DataFrame,
    variable: str,
    title: str
) -> go.Figure:
    """Create interactive bar chart comparing simulations."""

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=comparison_df["simulation"],
        y=comparison_df[f"{variable}_max"],
        name="Maximum",
        marker_color="indianred"
    ))

    fig.add_trace(go.Bar(
        x=comparison_df["simulation"],
        y=comparison_df[f"{variable}_mean"],
        name="Mean",
        marker_color="lightsalmon"
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Simulation",
        yaxis_title=variable,
        barmode="group"
    )

    return fig

# Create and save chart
fig = create_comparison_bar_chart(
    comparison_df,
    "Mooring_Line_1_Effective Tension",
    "Tension Comparison Across Configurations"
)
fig.write_html("comparison_chart.html")
```

### Radar Chart for Multi-Variable Comparison

```python
import plotly.graph_objects as go

def create_radar_comparison(
    stiffness_comparison: dict
) -> go.Figure:
    """Create radar chart for stiffness comparison."""

    categories = ["K_xx", "K_yy", "K_zz", "K_xy", "K_xz", "K_yz"]

    fig = go.Figure()

    for config_name, data in stiffness_comparison.items():
        values = [data.get(cat, 0) for cat in categories]
        values.append(values[0])  # Close the polygon

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            name=config_name,
            fill='toself'
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="Stiffness Comparison"
    )

    return fig
```

## Output Formats

### Comparison Summary Table

| Metric | Baseline | Modified | Optimized | Units |
|--------|----------|----------|-----------|-------|
| Max Tension (Leg_1) | 2450.5 | 2380.2 | 2320.1 | kN |
| Max Tension (Leg_2) | 2380.2 | 2350.8 | 2290.5 | kN |
| Surge Stiffness | 1250.5 | 1320.8 | 1450.2 | kN/m |
| Surge Period | 120.5 | 115.2 | 105.8 | s |

### Difference Report

```json
{
  "comparison": "Modified vs Baseline",
  "differences": {
    "Leg_1_Max_Tension": {
      "baseline": 2450.5,
      "modified": 2380.2,
      "difference": -70.3,
      "percent_change": -2.87
    },
    "K_xx": {
      "baseline": 1250.5,
      "modified": 1320.8,
      "difference": 70.3,
      "percent_change": 5.62
    }
  }
}
```

## Best Practices

### Simulation Setup

1. **Consistent naming** - Use same object names across configurations
2. **Same analysis period** - Compare equivalent simulation lengths
3. **Same environmental conditions** - Unless comparing sensitivity
4. **Documented changes** - Track what differs between configurations

### Comparison Approach

1. **Baseline first** - Establish reference configuration
2. **One change at a time** - For sensitivity studies
3. **Statistical significance** - Consider variability
4. **Normalization** - Compare percentage changes when scales differ

### Reporting

1. **Clear labels** - Identify each configuration
2. **Key metrics** - Focus on design-critical values
3. **Visualization** - Use charts for patterns
4. **Conclusions** - State design implications

## Error Handling

```python
try:
    comparison = analyzer.compare_pretensions(configurations, targets)
except FileNotFoundError as e:
    print(f"Results file not found: {e}")
    print("Check configuration paths")

except KeyError as e:
    print(f"Variable not found: {e}")
    print("Check object and variable names match simulations")
```

## Related Skills

- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Extract results
- [orcaflex-extreme-analysis](../orcaflex-extreme-analysis/SKILL.md) - Extreme values
- [orcaflex-operability](../orcaflex-operability/SKILL.md) - Multi-sea-state analysis
- [mooring-design](../mooring-design/SKILL.md) - Mooring system design

## References

- API RP 2SK: Design and Analysis of Stationkeeping Systems
- DNV-OS-E301: Position Mooring
- Source: `src/digitalmodel/modules/orcaflex/analysis/comparative.py`
