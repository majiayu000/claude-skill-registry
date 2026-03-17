---
name: orcaflex-operability
description: Perform operability analysis combining multiple sea states to assess
  system availability and weather downtime. Generate operability envelopes, critical
  heading analysis, and downtime calculations from wave scatter diagrams.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- operability analysis
- weather downtime
- operability envelope
- sea state analysis
- weather window
- operational limits
- critical headings
- wave scatter
- annual downtime
---
# OrcaFlex Operability Analysis Skill

Assess system operability across multiple sea states with envelope generation, critical heading analysis, and weather downtime calculations.

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
- Initial release with operability envelope generation
- Weather downtime calculations from wave scatter
- Critical heading analysis
- Interactive Plotly visualization

## When to Use

- Operability envelope generation for mooring systems
- Weather downtime calculations from scatter diagrams
- Critical heading identification for design loads
- Multi-sea-state analysis (1yr, 10yr, 100yr return periods)
- Tension limit assessment (intact vs damaged conditions)
- Annual operational availability studies
- Polar coordinate visualization of system limits

## Prerequisites

- OrcaFlex simulation results (.sim files) for multiple headings
- Wave scatter diagram (Hs-Tp probability matrix)
- Python environment with `digitalmodel` package installed
- Tension limits for intact and damaged conditions

## Operability Workflow

```
[Multiple .sim Files]    [Wave Scatter Diagram]
   (per heading)              (Hs-Tp matrix)
        ↓                          ↓
[Extract Max Tensions]    [Probability Distribution]
        ↓                          ↓
[Operability Envelope]  →  [Weather Downtime Calc]
        ↓                          ↓
[Critical Headings]      [Annual Availability %]
        ↓                          ↓
[Combined HTML Report with Interactive Plots]
```

## Configuration

### Basic Operability Configuration

```yaml
# configs/operability_config.yml

operability:
  # Input data
  simulation_directory: "results/.sim/"
  file_pattern: "mooring_heading_*.sim"

  # Tension extraction
  line_names:
    - "Mooring_Line_1"
    - "Mooring_Line_2"
    - "Mooring_Line_3"
    - "Mooring_Line_4"
  variable: "Effective Tension"
  statistic: "max"  # max, min, mean

  # Limits for envelope
  tension_limits:
    intact: 2500.0      # kN - intact condition limit
    damaged: 3000.0     # kN - damaged condition limit (typically higher)

  # Wave scatter for downtime
  wave_scatter:
    file: "data/wave_scatter_gom.csv"
    format: "hs_tp_matrix"  # or "hs_tp_list"

  # Output
  output:
    directory: "reports/operability/"
    report_name: "mooring_operability"
    format: "html"  # html, pdf
```

### Advanced Configuration

```yaml
# configs/operability_advanced.yml

operability:
  # Input data
  simulation_directory: "results/calm_operability/.sim/"
  file_pattern: "calm_hs*_tp*_dir*.sim"

  # Multi-line analysis
  line_groups:
    windward:
      lines: ["Leg_1", "Leg_2", "Leg_3"]
      critical_limit: 2000.0
    leeward:
      lines: ["Leg_4", "Leg_5", "Leg_6"]
      critical_limit: 2200.0

  # Heading analysis
  headings:
    start: 0
    end: 360
    step: 15
    critical_count: 5  # Top N critical headings to report

  # Envelope visualization
  envelope:
    polar_plot: true
    include_limits: true
    colorscale: "Viridis"
    show_critical_headings: true

  # Weather downtime
  downtime:
    operational_hours_per_year: 8760
    minimum_window_hours: 6  # Minimum weather window
    include_seasonal: true
    seasons:
      winter: [12, 1, 2]
      spring: [3, 4, 5]
      summer: [6, 7, 8]
      autumn: [9, 10, 11]

  # Output
  output:
    directory: "reports/operability/"
    report_name: "calm_operability_comprehensive"
    include_data_tables: true
    export_csv: true
```

## Python API

### Basic Operability Analysis

```python
from digitalmodel.orcaflex.operability_analysis import OperabilityAnalyzer

# Initialize analyzer
analyzer = OperabilityAnalyzer(
    simulation_directory="results/.sim/",
    output_directory="reports/operability/"
)

# Generate operability envelope
envelope = analyzer.generate_operability_envelope(
    line_names=["Mooring_Line_1", "Mooring_Line_2"],
    variable="Effective Tension",
    statistic="max",
    intact_limit=2500.0,
    damaged_limit=3000.0
)

# Save envelope plot
analyzer.save_envelope_plot(envelope, "operability_envelope.html")
```

### Weather Downtime Calculation

```python
from digitalmodel.orcaflex.operability_analysis import OperabilityAnalyzer
import pandas as pd

analyzer = OperabilityAnalyzer(
    simulation_directory="results/.sim/",
    output_directory="reports/"
)

# Load wave scatter diagram
wave_scatter = pd.read_csv("data/wave_scatter.csv", index_col=0)

# Calculate weather downtime
downtime_results = analyzer.calculate_weather_downtime(
    wave_scatter=wave_scatter,
    operational_limit_hs=4.0,  # Operational Hs limit
    operational_limit_tp=12.0  # Operational Tp limit
)

print(f"Annual downtime: {downtime_results['annual_downtime_percent']:.1f}%")
print(f"Operational hours: {downtime_results['operational_hours']:.0f} hrs/yr")
print(f"Downtime days: {downtime_results['downtime_days']:.1f} days/yr")
```

### Critical Headings Analysis

```python
from digitalmodel.orcaflex.operability_analysis import OperabilityAnalyzer

analyzer = OperabilityAnalyzer(
    simulation_directory="results/.sim/",
    output_directory="reports/"
)

# Identify critical headings
critical = analyzer.generate_critical_headings_report(
    line_names=["Leg_1", "Leg_2", "Leg_3", "Leg_4", "Leg_5", "Leg_6"],
    variable="Effective Tension",
    top_n=5,  # Top 5 most critical headings
    limit=2500.0
)

# Report format:
# critical = {
#     "headings": [45, 135, 225, 315, 0],
#     "max_tensions": [2450.2, 2380.5, 2350.1, 2290.8, 2250.3],
#     "utilization": [0.98, 0.95, 0.94, 0.92, 0.90],
#     "critical_lines": ["Leg_1", "Leg_3", "Leg_5", "Leg_2", "Leg_4"]
# }

for i, heading in enumerate(critical["headings"]):
    print(f"Heading {heading}°: {critical['max_tensions'][i]:.1f} kN "
          f"({critical['utilization'][i]*100:.1f}% utilization)")
```

### Comprehensive Report Generation

```python
from digitalmodel.orcaflex.operability_analysis import OperabilityAnalyzer

analyzer = OperabilityAnalyzer(
    simulation_directory="results/.sim/",
    output_directory="reports/"
)

# Generate comprehensive HTML report with all analyses
report_path = analyzer.generate_comprehensive_report(
    line_names=["Leg_1", "Leg_2", "Leg_3", "Leg_4", "Leg_5", "Leg_6"],
    variable="Effective Tension",
    intact_limit=2500.0,
    damaged_limit=3000.0,
    wave_scatter_file="data/wave_scatter.csv",
    report_title="CALM Buoy Mooring Operability Assessment",
    include_envelope=True,
    include_critical_headings=True,
    include_weather_downtime=True
)

print(f"Report saved to: {report_path}")
```

## Output Formats

### Operability Envelope Plot

Interactive Plotly polar plot showing:
- Maximum tension vs heading angle
- Intact and damaged limit circles
- Color-coded utilization zones
- Hover tooltips with exact values

### Critical Headings Table

| Rank | Heading (°) | Max Tension (kN) | Utilization (%) | Critical Line | Status |
|------|-------------|------------------|-----------------|---------------|--------|
| 1 | 45 | 2450.2 | 98.0 | Leg_1 | WARNING |
| 2 | 135 | 2380.5 | 95.2 | Leg_3 | OK |
| 3 | 225 | 2350.1 | 94.0 | Leg_5 | OK |

### Weather Downtime Summary

```json
{
  "annual_downtime_percent": 12.5,
  "operational_hours_per_year": 7665,
  "downtime_hours_per_year": 1095,
  "downtime_days_per_year": 45.6,
  "seasonal_breakdown": {
    "winter": {"downtime_percent": 25.3, "days": 23.1},
    "spring": {"downtime_percent": 10.2, "days": 9.3},
    "summer": {"downtime_percent": 5.1, "days": 4.7},
    "autumn": {"downtime_percent": 9.4, "days": 8.5}
  }
}
```

## Wave Scatter Diagram Format

### CSV Matrix Format

```csv
Tp\Hs,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0
4,0.001,0.002,0.001,0.000,0.000,0.000,0.000,0.000
6,0.005,0.015,0.020,0.010,0.003,0.001,0.000,0.000
8,0.010,0.050,0.080,0.060,0.030,0.010,0.003,0.001
10,0.008,0.040,0.070,0.080,0.050,0.025,0.010,0.003
12,0.005,0.025,0.040,0.050,0.040,0.020,0.010,0.005
14,0.002,0.010,0.020,0.025,0.020,0.015,0.008,0.003
```

Values represent probability of occurrence (sum = 1.0).

## Best Practices

### Simulation Setup

1. **Consistent headings** - Use regular intervals (15° or 30°)
2. **Sufficient sea states** - Cover full scatter diagram range
3. **Consistent naming** - Include heading in filename
4. **Complete simulations** - Ensure all finish successfully

### Limit Selection

1. **Intact limit** - Based on design code (e.g., 60% MBL)
2. **Damaged limit** - Account for redundancy (e.g., 80% MBL)
3. **Include safety factors** - Per API RP 2SK or DNV

### Weather Downtime

1. **Site-specific scatter** - Use project metocean data
2. **Operational limits** - Define based on system capabilities
3. **Weather windows** - Consider minimum window requirements

## Error Handling

```python
try:
    envelope = analyzer.generate_operability_envelope(...)
except FileNotFoundError as e:
    print(f"Simulation files not found: {e}")
    print("Check simulation_directory and file_pattern")

except ValueError as e:
    print(f"Configuration error: {e}")
    print("Check line names and variable specifications")
```

## Integration with Other Skills

### With OrcaFlex Modeling

```python
# 1. Run simulations for multiple headings
from digitalmodel.orcaflex.universal import UniversalOrcaFlexRunner

runner = UniversalOrcaFlexRunner()
for heading in range(0, 360, 15):
    runner.run_single(f"mooring_heading_{heading}.yml")

# 2. Run operability analysis
from digitalmodel.orcaflex.operability_analysis import OperabilityAnalyzer

analyzer = OperabilityAnalyzer(simulation_directory="results/.sim/")
analyzer.generate_comprehensive_report(...)
```

### With Post-Processing

```python
# Use OPP for detailed extraction, then operability for envelope
from digitalmodel.orcaflex.opp import OrcaFlexPostProcess
from digitalmodel.orcaflex.operability_analysis import OperabilityAnalyzer

# Extract detailed statistics
opp = OrcaFlexPostProcess()
stats = opp.extract_summary_statistics(...)

# Generate operability envelope
analyzer = OperabilityAnalyzer(...)
envelope = analyzer.generate_operability_envelope(...)
```

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Extract results
- [orcaflex-extreme-analysis](../orcaflex-extreme-analysis/SKILL.md) - Extreme value extraction
- [mooring-design](../mooring-design/SKILL.md) - Mooring system design

## References

- API RP 2SK: Design and Analysis of Stationkeeping Systems
- DNV-OS-E301: Position Mooring
- ISO 19901-7: Stationkeeping Systems
- Source: `src/digitalmodel/modules/orcaflex/operability_analysis.py`
