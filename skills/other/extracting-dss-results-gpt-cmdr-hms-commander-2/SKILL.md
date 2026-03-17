---
name: extracting-dss-results
description: |
  Extracts and analyzes HEC-HMS simulation results from DSS files using HmsDss and
  HmsResults classes. Handles peak flows, hydrographs, volume summaries, and time series
  data. Leverages ras-commander's RasDss for DSS V6/V7 support. Use when processing
  HMS results, extracting peak flows, analyzing hydrographs, computing volumes, or
  exporting time series. Integrates with HEC-RAS for boundary condition workflows.
  Trigger keywords: DSS file, results, peak flow, hydrograph, time series, volume,
  extract results, HMS output, analyze results.
---

# Extracting DSS Results

## Quick Start

```python
from hms_commander import HmsResults, HmsDss

# Extract peak flows
peaks = HmsResults.get_peak_flows("results.dss")

# Extract hydrograph
flows = HmsResults.get_outflow_timeseries("results.dss", "Outlet")

# Get precipitation time series
precip = HmsResults.get_precipitation_timeseries("results.dss", "Subbasin1")
```

## Primary Sources

**Code**:
- `hms_commander/HmsDss.py` - DSS operations (wraps RasDss)
- `hms_commander/HmsResults.py` - Results extraction and analysis

**Integration**: Uses `ras_commander.RasDss` for DSS V6/V7 support

**Rules**: `.claude/rules/hec-hms/dss-operations.md` - DSS patterns

## When to Use This Skill

- Extracting simulation results after HmsCmdr.compute_run()
- Analyzing peak flows and timing
- Processing hydrographs for plotting or export
- Computing volume summaries (acre-feet)
- Linking HMS results to HEC-RAS (boundary conditions)
- Comparing multiple runs

## Core Capabilities

### 1. Peak Flow Extraction

Returns DataFrame with peak flows for all elements:
```python
peaks = HmsResults.get_peak_flows("results.dss")
# Columns: Element, Peak Flow (cfs), Time to Peak
```

### 2. Time Series Extraction

Get complete hydrographs:
```python
flows = HmsResults.get_outflow_timeseries("results.dss", "Outlet")
# Returns: pandas DataFrame with datetime index
```

### 3. Volume Analysis

```python
volumes = HmsResults.get_volume_summary("results.dss")
# Returns: DataFrame with volumes in acre-feet
```

### 4. Multi-Run Comparison

```python
comparison = HmsResults.compare_runs(
    ["baseline.dss", "alternative.dss"],
    element="Outlet"
)
```

## DSS Pathname Format

HMS uses standard DSS pathname: `/A/B/C/D/E/F/`

- **A**: Basin name
- **B**: Element name (subbasin/junction/reach)
- **C**: Parameter type (FLOW, PRECIP, etc.)
- **D**: Time interval (15MIN, 1HOUR, etc.)
- **E**: Run name
- **F**: Version (usually blank)

Example: `/BASIN/OUTLET/FLOW/15MIN/RUN1/`

**See**: `.claude/rules/hec-hms/dss-operations.md` for complete pathname details

## RasDss Integration

HmsDss wraps ras-commander's RasDss:

**Why?**
- No code duplication
- Consistent DSS operations across HMS and RAS
- Automatic V6/V7 support
- Shared Java bridge maintenance

**Check availability**:
```python
if HmsDss.is_available():
    catalog = HmsDss.get_catalog("results.dss")
else:
    print("RasDss not available - install ras-commander")
```

## Common Workflows

### Workflow 1: Post-Simulation Analysis

```python
from hms_commander import init_hms_project, hms, HmsCmdr, HmsResults

# Run simulation
init_hms_project("project")
HmsCmdr.compute_run("Run 1")

# Extract results
dss_file = hms.run_df.loc["Run 1", "dss_file"]
peaks = HmsResults.get_peak_flows(dss_file)
print(peaks)
```

### Workflow 2: Export for External Analysis

```python
# Export all results to CSV
HmsResults.export_results_to_csv("results.dss", "output_folder")
```

### Workflow 3: HMS to RAS Linking

```python
from hms_commander import HmsResults, HmsGeo

# Extract HMS hydrograph
hms_flows = HmsResults.get_outflow_timeseries("hms_results.dss", "Outlet")

# Get peak for validation
peaks = HmsResults.get_peak_flows("hms_results.dss")
hms_peak = peaks.loc["Outlet", "Peak Flow (cfs)"]

# Document spatial reference for RAS matching
lat, lon = HmsGeo.get_project_centroid_latlon("project.geo")

# Handoff to RAS:
# - DSS file: hms_results.dss
# - Pathname: /BASIN/OUTLET/FLOW/15MIN/RUN/
# - Outlet location: (lat, lon)
# - Peak: hms_peak cfs

# See: linking-hms-to-hecras skill for complete workflow
```

## Reference Files

- `reference/hmsdss_api.md` - Complete HmsDss API
- `reference/hmsresults_api.md` - Complete HmsResults API
- `reference/dss_pathnames.md` - Pathname structure details
- `examples/peak_flows.md` - Peak flow analysis
- `examples/hydrographs.md` - Time series plotting

## Related Skills

- **executing-hms-runs** - Generate results to extract
- **linking-hms-to-hecras** - Use HMS results in RAS (complete workflow)
