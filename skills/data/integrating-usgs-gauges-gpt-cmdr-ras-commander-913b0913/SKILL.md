---
name: integrating-usgs-gauges
allowed-tools: [Read, Grep, Glob]
description: |
  Complete USGS gauge data integration workflow from spatial discovery to
  model validation. Handles gauge finding, data retrieval, matching to HEC-RAS
  features, boundary condition generation, initial conditions, real-time
  monitoring, and validation metrics (NSE, KGE). Use when working with USGS
  data, NWIS gauges, generating boundaries from observed flow, calibrating
  models, validating with observed data, or setting up operational forecasting.
---

# Integrating USGS Gauges

**Lightweight skill navigator** - Points you to authoritative sources instead of duplicating content.

## Primary Documentation Sources

**COMPLETE WORKFLOWS AND API REFERENCE**:
- `ras_commander/usgs/CLAUDE.md` (367 lines) - **Complete module documentation with workflows**
  - Module overview and API reference
  - 7-stage workflow (discovery → validation)
  - Real-time monitoring patterns
  - Catalog generation workflow

**WORKING EXAMPLES**:
- `examples/911_usgs_gauge_data_integration.ipynb` - Complete workflow (discovery → validation)
- `examples/912_usgs_real_time_monitoring.ipynb` - Real-time monitoring examples
- `examples/913_bc_generation_from_live_gauge.ipynb` - Boundary condition generation
- `examples/914_model_validation_with_usgs.ipynb` - Model validation workflow
- `examples/910_usgs_gauge_catalog.ipynb` - Catalog generation (v0.89.0+)

**CODE DOCSTRINGS**:
- All classes have comprehensive docstrings with examples
- Read docstrings for detailed parameter documentation

## Quick Navigation Guide

### What to Use When

| Task | Primary Source | Secondary Source |
|------|----------------|------------------|
| **API reference** | `ras_commander/usgs/CLAUDE.md` | Code docstrings |
| **Complete workflows** | `ras_commander/usgs/CLAUDE.md` | Example notebooks |
| **Spatial discovery** | `CLAUDE.md` → Spatial Queries section | `421_usgs_*.ipynb` |
| **Data retrieval** | `CLAUDE.md` → Data Retrieval section | `421_usgs_*.ipynb` |
| **Gauge matching** | `CLAUDE.md` → Gauge Matching section | `421_usgs_*.ipynb` |
| **Boundary generation** | `CLAUDE.md` → Boundary Conditions section | `423_bc_*.ipynb` |
| **Initial conditions** | `CLAUDE.md` → Initial Conditions section | `423_bc_*.ipynb` |
| **Real-time monitoring** | `CLAUDE.md` → Real-Time Monitoring section | `422_*.ipynb` |
| **Catalog generation** | `CLAUDE.md` → Catalog Generation section | `420_*.ipynb` |
| **Model validation** | `CLAUDE.md` → Validation Metrics section | `424_*.ipynb` |
| **Visualization** | `CLAUDE.md` → Visualization section | `424_*.ipynb` |
| **Troubleshooting** | Example notebooks (see errors/warnings) | Code comments |

## Module Quick Reference

From `ras_commander/usgs/CLAUDE.md`:

**Core Data Retrieval** (`core.py`):
- `RasUsgsCore.retrieve_flow_data()` - Get flow time series
- `RasUsgsCore.retrieve_stage_data()` - Get stage time series
- `RasUsgsCore.get_gauge_metadata()` - Get gauge info
- `RasUsgsCore.check_data_availability()` - Check data exists

**Spatial Discovery** (`spatial.py`):
- `UsgsGaugeSpatial.find_gauges_in_project()` - Find gauges in project bounds
- `UsgsGaugeSpatial.get_project_gauges_with_data()` - Find gauges with data for sim period

**Gauge Matching** (`gauge_matching.py`):
- `GaugeMatcher.auto_match_gauges()` - Automatic matching
- `GaugeMatcher.match_gauge_to_cross_section()` - Match to 1D XS
- `GaugeMatcher.match_gauge_to_2d_area()` - Match to 2D area

**Time Series** (`time_series.py`):
- `RasUsgsTimeSeries.resample_to_hecras_interval()` - Resample to HEC-RAS intervals
- `RasUsgsTimeSeries.check_data_gaps()` - Detect gaps
- `RasUsgsTimeSeries.align_timeseries()` - Align observed/modeled

**Boundary Generation** (`boundary_generation.py`):
- `RasUsgsBoundaryGeneration.generate_flow_hydrograph_table()` - Create BC table
- `RasUsgsBoundaryGeneration.update_boundary_hydrograph()` - Update .u## file

**Initial Conditions** (`initial_conditions.py`):
- `InitialConditions.create_ic_line()` - Generate IC line
- `InitialConditions.get_ic_value_from_usgs()` - Extract IC from USGS data

**Real-Time** (`real_time.py`) - v0.87.0+:
- `RasUsgsRealTime.get_latest_value()` - Get most recent reading
- `RasUsgsRealTime.monitor_gauge()` - Continuous monitoring with callbacks
- `RasUsgsRealTime.detect_threshold_crossing()` - Flood detection

**Catalog** (`catalog.py`) - v0.89.0+:
- `catalog.generate_gauge_catalog()` - Create standardized gauge catalog
- `catalog.load_gauge_catalog()` - Load catalog
- `catalog.load_gauge_data()` - Load historical data

**Validation** (`metrics.py`):
- `metrics.nash_sutcliffe_efficiency()` - NSE metric
- `metrics.kling_gupta_efficiency()` - KGE metric
- `metrics.calculate_all_metrics()` - Complete validation suite

**Visualization** (`visualization.py`):
- `visualization.plot_timeseries_comparison()` - Observed vs modeled plots
- `visualization.plot_scatter_comparison()` - Scatter with 1:1 line
- `visualization.plot_residuals()` - 4-panel diagnostics

**File I/O** (`file_io.py`):
- `RasUsgsFileIo.cache_gauge_data()` - Save to CSV
- `RasUsgsFileIo.load_cached_gauge_data()` - Load from CSV

## Minimal Quick Start

For complete quick start, see `ras_commander/usgs/CLAUDE.md`.

**Basic pattern** (copy-paste starting point):

```python
from ras_commander import init_ras_project
from ras_commander.usgs import UsgsGaugeSpatial, RasUsgsCore, GaugeMatcher

# Initialize
init_ras_project(r"C:\Projects\MyModel", "6.5")

# 1. Find gauges
gauges = UsgsGaugeSpatial.find_gauges_in_project(
    project_folder=r"C:\Projects\MyModel",
    buffer_miles=5.0
)

# 2. Get data
flow_data = RasUsgsCore.retrieve_flow_data(
    site_no="01646500",
    start_date="2023-09-01",
    end_date="2023-09-15",
    service='iv'  # Instantaneous values
)

# 3. Match to model
matches = GaugeMatcher.auto_match_gauges(
    gauges_gdf=gauges,
    project_folder=r"C:\Projects\MyModel"
)

# For complete workflow, see ras_commander/usgs/CLAUDE.md
```

## Common Workflow Patterns

### Pattern 1: Boundary Condition Generation
**See**: `ras_commander/usgs/CLAUDE.md` → "Complete Workflow" section → Stage 5
**Example**: `examples/913_bc_generation_from_live_gauge.ipynb`

### Pattern 2: Model Validation
**See**: `ras_commander/usgs/CLAUDE.md` → "Complete Workflow" section → Stage 6
**Example**: `examples/914_model_validation_with_usgs.ipynb`

### Pattern 3: Real-Time Monitoring
**See**: `ras_commander/usgs/CLAUDE.md` → "Real-Time Workflows" section
**Example**: `examples/912_usgs_real_time_monitoring.ipynb`

### Pattern 4: Gauge Catalog Generation
**See**: `ras_commander/usgs/CLAUDE.md` → "Complete Workflow" section → Stage 7
**Example**: `examples/910_usgs_gauge_catalog.ipynb`

## Troubleshooting Guide

### Missing dataretrieval Module
```
ModuleNotFoundError: No module named 'dataretrieval'
```
**Solution**: `pip install dataretrieval`

### No Gauges Found
**Check**:
1. Increase `buffer_miles` parameter
2. Verify project coordinate system
3. Check if project bounds are correct

**See**: `examples/911_usgs_*.ipynb` for spatial discovery debugging

### Data Gaps
**Tools**:
- `RasUsgsTimeSeries.check_data_gaps()` - Detect gaps
- `RasUsgsTimeSeries.fill_data_gaps()` - Interpolate gaps

**See**: `ras_commander/usgs/CLAUDE.md` → Time Series Processing

### Invalid Boundary Format
**Check**:
1. Verify HEC-RAS interval code (`15MIN`, `1HOUR`, etc.)
2. Use `validate_boundary_format()` to check format
3. Review fixed-width format requirements

**See**: `examples/913_bc_*.ipynb` for boundary generation debugging

### Poor Validation Metrics (NSE < 0.5)
**Investigate**:
1. Model calibration parameters
2. Boundary condition accuracy
3. Gauge location vs model feature match
4. Timing alignment

**See**: `examples/914_*.ipynb` for validation workflow

## Dependencies

**Required** (always available):
- pandas, geopandas, requests

**Optional** (lazy-loaded):
- `dataretrieval` - USGS NWIS client (recommended)
  - Install: `pip install dataretrieval`
  - Methods check availability on first use

**Check dependencies**:
```python
from ras_commander.usgs import check_dependencies
deps = check_dependencies()
print(deps)  # {'pandas': True, 'geopandas': True, 'dataretrieval': True/False}
```

## Validation Metric Interpretation

**See**: `ras_commander/usgs/CLAUDE.md` → Validation Metrics section for complete details.

**Quick reference**:
- **NSE** (Nash-Sutcliffe): −∞ to 1 (perfect = 1)
  - > 0.75: Very good
  - 0.65-0.75: Good
  - 0.50-0.65: Satisfactory
  - < 0.50: Unsatisfactory
- **KGE** (Kling-Gupta): −∞ to 1 (perfect = 1)
  - Similar interpretation to NSE
  - Components: correlation, bias ratio, variability ratio

**For detailed interpretation**: See `examples/914_model_validation_with_usgs.ipynb`

## Key Features

### Multi-Level Verifiability
- Boundary conditions in .u## files reviewable in HEC-RAS GUI
- Visual outputs for domain expert review
- Code audit trails with @log_call decorators

### USGS Service Compliance
- Rate limiting (1 req/sec default)
- Proper parameter codes (00060 = flow, 00065 = stage)
- Timeout handling and retry logic

### Data Quality
- Automatic gap detection
- Data availability checks
- Resampling validation

**See**: `ras_commander/usgs/CLAUDE.md` → Key Features for details

## See Also

- **HEC-RAS execution**: `.claude/skills/executing-hecras-plans/`
- **HDF results extraction**: `.claude/skills/extracting-hecras-results/`
- **Precipitation data**: `ras_commander.precipitation` module
- **Boundary utilities**: `ras_commander.RasUnsteady`

## Skill Development Philosophy

This skill is intentionally lightweight (~300 lines) and serves as a **navigator to authoritative sources** rather than duplicating content. This approach:

1. **Eliminates duplication** - Workflows exist in `ras_commander/usgs/CLAUDE.md` (367 lines)
2. **Reduces maintenance burden** - Update workflows in one place
3. **Improves accuracy** - Single source of truth for API details
4. **Provides quick navigation** - Table guides you to right source for your task
5. **Keeps skills focused** - Skills point to docs, docs contain complete details

**When to use this skill**:
- You need quick navigation to USGS integration resources
- You want to know which module handles which task
- You need a starting point for USGS workflows

**When to read full docs**:
- You need complete workflow details → Read `ras_commander/usgs/CLAUDE.md`
- You need working code examples → Open example notebooks
- You need parameter documentation → Read code docstrings
