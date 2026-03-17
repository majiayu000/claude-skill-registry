---
name: orcaflex-post-processing
description: Post-process OrcaFlex simulation results using OPP (OrcaFlex Post-Process).
  Use for extracting summary statistics, linked statistics, range graphs, time series,
  histograms, and generating interactive HTML reports from .sim files.
updated: '2026-01-07'
---
# OrcaFlex Post-Processing Skill

Extract and analyze results from OrcaFlex simulation files (.sim) using the OPP (OrcaFlex Post-Process) module.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  signal-analysis: '>=1.0.0,<2.0.0'
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

- Extracting summary statistics from simulation results
- Creating range graphs for motion/load envelopes
- Generating time series plots for specific variables
- Computing linked statistics (correlations between variables)
- Creating histogram distributions of results
- Building interactive HTML dashboards from simulation data
- Batch processing multiple .sim files in parallel

## Prerequisites

- OrcaFlex license (for reading .sim files)
- Completed simulations in `.sim/` directory
- Python environment with `digitalmodel` package installed

## Post-Processing Types

### 1. Summary Statistics

Extract min, max, mean, std dev for all monitored variables.

```yaml
orcaflex:
  postprocess:
    summary:
      flag: true
      variables:
        - object: "Line1"
          variable_name: "Effective Tension"
        - object: "Vessel1"
          variable_name: "X"
      output_format: csv  # csv, json, or xlsx
      output_path: "results/summary/"
```

### 2. Linked Statistics

Compute correlations and linked values between variables.

```yaml
orcaflex:
  postprocess:
    linked_statistics:
      flag: true
      primary_variable:
        object: "Line1"
        variable_name: "Effective Tension"
      linked_variables:
        - object: "Vessel1"
          variable_name: "Heave"
        - object: "Vessel1"
          variable_name: "Pitch"
      statistics: ["max_with_linked", "min_with_linked"]
      output_path: "results/linked_stats/"
```

### 3. Range Graphs

Generate envelope plots showing variable ranges.

```yaml
orcaflex:
  postprocess:
    RangeGraph:
      flag: true
      objects:
        - name: "Line1"
          variables:
            - "Effective Tension"
            - "Bend Moment"
            - "Curvature"
      arc_length_range: [0, 500]  # meters
      output_format: html  # Interactive Plotly
      output_path: "results/range_graphs/"
```

### 4. Time Series

Extract and plot time-domain data.

```yaml
orcaflex:
  postprocess:
    time_series:
      flag: true
      variables:
        - object: "Vessel1"
          variable_name: "X"
        - object: "Vessel1"
          variable_name: "Heave"
        - object: "Line1"
          variable_name: "End A X"
      time_range: [0, 3600]  # Start and end time (seconds)
      output_format: html
      output_path: "results/time_series/"
```

### 5. Histograms

Generate probability distributions.

```yaml
orcaflex:
  postprocess:
    visualization:
      flag: true
      histogram:
        enabled: true
        variables:
          - object: "Line1"
            variable_name: "Effective Tension"
        bins: 50
        normalize: true  # Show as probability density
      output_path: "results/histograms/"
```

## Python API

### Basic Post-Processing

```python
from digitalmodel.orcaflex.opp import OrcaFlexPostProcess

# Initialize post-processor
opp = OrcaFlexPostProcess()

# Load configuration
cfg = {
    "orcaflex": {
        "postprocess": {
            "summary": {
                "flag": True,
                "variables": [
                    {"object": "Line1", "variable_name": "Effective Tension"}
                ]
            }
        }
    }
}

# Run post-processing
results = opp.post_process_router(cfg)
```

### Batch Processing with Parallel Execution

```python
from digitalmodel.orcaflex.opp import OrcaFlexPostProcess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

opp = OrcaFlexPostProcess()

# Get all .sim files
sim_files = list(Path("results/.sim/").glob("*.sim"))

# Process in parallel
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = []
    for sim_file in sim_files:
        future = executor.submit(opp.process_single_file, sim_file)
        futures.append(future)

    # Collect results
    for future in futures:
        result = future.result()
        print(f"Processed: {result['file_name']}")
```

### Extract Specific Results

```python
from digitalmodel.orcaflex.orcaflex_utilities import OrcaflexUtilities

utils = OrcaflexUtilities()

# Load simulation
model, metadata = utils.get_model_and_metadata("simulation.sim")

# Get time history
line = model["Line1"]
tension = line.TimeHistory("Effective Tension", period=None)

# Get range graph data
range_data = line.RangeGraph("Effective Tension")

# Get statistics
stats = line.StaticResult("Effective Tension")
```

## Configuration Examples

### Complete Post-Processing Configuration

```yaml
basename: mooring_analysis

orcaflex:
  postprocess:
    # Summary statistics for all key variables
    summary:
      flag: true
      variables:
        - object: "Line1"
          variable_name: "Effective Tension"
        - object: "Line1"
          variable_name: "Bend Moment"
        - object: "Vessel1"
          variable_name: "X"
        - object: "Vessel1"
          variable_name: "Y"
        - object: "Vessel1"
          variable_name: "Z"
        - object: "Vessel1"
          variable_name: "Rotation 1"
        - object: "Vessel1"
          variable_name: "Rotation 2"
        - object: "Vessel1"
          variable_name: "Rotation 3"
      output_format: csv

    # Linked statistics for tension correlation
    linked_statistics:
      flag: true
      primary_variable:
        object: "Line1"
        variable_name: "Effective Tension"
      linked_variables:
        - object: "Vessel1"
          variable_name: "Heave"
        - object: "Vessel1"
          variable_name: "Surge"
      statistics: ["max_with_linked", "min_with_linked", "correlation"]

    # Range graphs for line profiles
    RangeGraph:
      flag: true
      objects:
        - name: "Line1"
          variables:
            - "Effective Tension"
            - "Curvature"
        - name: "Line2"
          variables:
            - "Effective Tension"
      arc_length_range: null  # Full length
      percentiles: [1, 5, 50, 95, 99]

    # Time series for key motions
    time_series:
      flag: true
      variables:
        - object: "Vessel1"
          variable_name: "X"
        - object: "Vessel1"
          variable_name: "Heave"
      time_range: null  # Full simulation
      sample_rate: 0.1  # Every 0.1 seconds

    # Visualization options
    visualization:
      flag: true
      histogram:
        enabled: true
        bins: 100
      interactive: true
      theme: "plotly_white"
```

### Minimal Quick Summary

```yaml
orcaflex:
  postprocess:
    summary:
      flag: true
      output_format: csv
      output_path: "results/quick_summary.csv"
```

## Output Formats

### CSV Output

```csv
Object,Variable,Min,Max,Mean,StdDev,Units
Line1,Effective Tension,450.2,1823.5,892.3,234.1,kN
Line1,Bend Moment,0.0,125.4,45.2,28.9,kN.m
Vessel1,X,-15.2,12.8,-1.2,5.4,m
```

### JSON Output

```json
{
  "simulation": "mooring_case_001.sim",
  "results": [
    {
      "object": "Line1",
      "variable": "Effective Tension",
      "statistics": {
        "min": 450.2,
        "max": 1823.5,
        "mean": 892.3,
        "std": 234.1
      },
      "units": "kN"
    }
  ]
}
```

### Interactive HTML

OPP generates interactive Plotly HTML reports with:
- Zoomable time series
- Hover tooltips with exact values
- Legend toggling
- Export to PNG/SVG
- Responsive design

## Parallel Processing Details

The OPP module uses `ProcessPoolExecutor` for efficient batch processing:

```python
# From opp.py - parallel processing pattern
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_sim_files_parallel(sim_files, cfg, max_workers=4):
    """Process multiple .sim files in parallel."""
    results = {}

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_single_sim, f, cfg): f
            for f in sim_files
        }

        for future in as_completed(future_to_file):
            file_name = future_to_file[future]
            try:
                result = future.result()
                results[file_name] = result
            except Exception as e:
                results[file_name] = {"error": str(e)}

    return results
```

## Variable Reference

### Common Vessel Variables

| Variable | Description | Units |
|----------|-------------|-------|
| X, Y, Z | Position | m |
| Rotation 1/2/3 | Roll/Pitch/Yaw | deg |
| Velocity | Resultant velocity | m/s |
| Acceleration | Resultant acceleration | m/s² |

### Common Line Variables

| Variable | Description | Units |
|----------|-------------|-------|
| Effective Tension | Tension including pressure effects | kN |
| Wall Tension | Tension at pipe wall | kN |
| Bend Moment | Bending moment | kN.m |
| Curvature | Line curvature | 1/m |
| Torsion Moment | Torsional moment | kN.m |
| X, Y, Z | Node position | m |

### Common Buoy Variables

| Variable | Description | Units |
|----------|-------------|-------|
| X, Y, Z | Position | m |
| Connection X Force | Force in X | kN |
| Connection Z Force | Force in Z | kN |

## Best Practices

### Efficient Processing

1. **Use parallel processing** for multiple .sim files
2. **Limit variables** to only those needed
3. **Specify time ranges** to reduce data volume
4. **Use CSV for data analysis**, HTML for reporting

### Data Organization

1. Store summaries in `results/summary/`
2. Store time series in `results/time_series/`
3. Store range graphs in `results/range_graphs/`
4. Use consistent naming: `{case_name}_{variable_type}.{format}`

### Interactive Reports

1. Always use **Plotly** for interactive HTML (mandatory per workspace standards)
2. Include hover tooltips with values
3. Add legend for multi-line plots
4. Use consistent color schemes

## Error Handling

### Common Issues

1. **Missing .sim file**
   ```python
   if not Path(sim_file).exists():
       logger.error(f"Simulation file not found: {sim_file}")
   ```

2. **Invalid variable name**
   ```python
   try:
       data = line.TimeHistory(variable_name)
   except OrcFxAPI.OrcaFlexError as e:
       logger.warning(f"Variable not found: {variable_name}")
   ```

3. **Memory issues with large simulations**
   - Process in chunks
   - Downsample time series
   - Release model after processing

## Related Skills

- [orcaflex-modeling](../orcaflex-modeling/SKILL.md) - Run OrcaFlex simulations
- [mooring-design](../mooring-design/SKILL.md) - Mooring system design
- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Fatigue assessment

## References

- OrcaFlex Results Documentation
- OrcFxAPI Python Guide
- Workspace HTML Reporting Standards: `docs/modules/standards/HTML_REPORTING_STANDARDS.md`
