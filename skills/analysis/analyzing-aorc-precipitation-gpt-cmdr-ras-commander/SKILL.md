---
name: analyzing-aorc-precipitation
description: |
  Retrieves and processes AORC precipitation data for HEC-RAS/HMS models.
  Handles spatial averaging over watersheds, temporal aggregation, DSS export,
  and Atlas 14 design storms. Use when working with historical precipitation,
  AORC data, calibration workflows, design storm generation, rainfall analysis,
  SCS Type II distributions, AEP events, 100-year storms, or generating
  precipitation boundary conditions for rain-on-grid models.
  Triggers: precipitation, AORC, Atlas 14, design storm, rainfall, SCS Type II, AEP, 100-year, rain-on-grid, hyetograph, temporal distribution, areal reduction, calibration, historical precipitation.
---

# Analyzing AORC Precipitation

**Purpose**: Navigate precipitation workflows for HEC-RAS/HMS models using AORC historical data and Atlas 14 design storms.

**This skill is a NAVIGATOR** - it points you to the primary sources containing complete workflows and API documentation. For implementation details, always refer to the primary sources below.

## Primary Sources (Read These First!)

### 1. Complete API Reference and Workflows
**`ras_commander/precip/CLAUDE.md`** (329 lines - AUTHORITATIVE SOURCE)

Contains:
- Complete module organization (PrecipAorc, StormGenerator)
- Full API reference with all methods
- Step-by-step AORC workflow (retrieval, spatial averaging, temporal aggregation, export)
- Step-by-step Atlas 14 workflow (query, generate, apply ARF, export)
- Multi-event workflows
- Performance characteristics
- Dependencies and installation

**THIS IS THE PRIMARY DOCUMENTATION** - use it for all detailed questions.

### 2. AORC Demonstration Notebook
**`examples/900_aorc_precipitation.ipynb`**

Live working example showing:
- AORC data retrieval from cloud storage
- Spatial averaging over watersheds
- Temporal aggregation to HEC-RAS intervals
- Export to DSS and CSV formats
- Integration with HEC-RAS unsteady flow files

### 3. Atlas 14 Single-Project Workflow
**`examples/720_atlas14_aep_events.ipynb`**

Complete design storm workflow:
- Query Atlas 14 precipitation frequency values
- Generate SCS Type II temporal distributions
- Apply areal reduction factors
- Create HEC-RAS plans for multiple AEP events
- Batch execution and results processing

### 4. Atlas 14 Multi-Project Batch Processing
**`examples/722_atlas14_multi_project.ipynb`**

Advanced batch processing:
- Process multiple HEC-RAS projects simultaneously
- Standardized AEP suite (10%, 2%, 1%, 0.2%)
- Automated plan creation across projects
- Parallel execution with result consolidation

## Quick Start

### AORC Historical Data (30 seconds)
```python
from ras_commander.precip import PrecipAorc

# Retrieve hourly AORC data for watershed
aorc_data = PrecipAorc.retrieve_aorc_data(
    watershed="02070010",  # HUC-8 code or shapefile path
    start_date="2015-05-01",
    end_date="2015-05-15"
)

# Spatial average over watershed
avg_precip = PrecipAorc.spatial_average(aorc_data, watershed)

# Aggregate to HEC-RAS interval
hourly = PrecipAorc.aggregate_to_interval(avg_precip, interval="1HR")

# Export to DSS for HEC-RAS
PrecipAorc.export_to_dss(
    hourly,
    dss_file="precipitation.dss",
    pathname="/PROJECT/PRECIP/AORC//1HOUR/OBS/"
)
```

### Atlas 14 Design Storm (30 seconds)
```python
from ras_commander.precip import StormGenerator

# Get 24-hr, 1% AEP (100-year) precipitation
precip = StormGenerator.get_precipitation_frequency(
    location=(38.9, -77.0),  # lat, lon
    duration_hours=24,
    aep_percent=1.0
)

# Generate SCS Type II distribution
hyetograph = StormGenerator.generate_design_storm(
    total_precip=precip,
    duration_hours=24,
    distribution="SCS_Type_II",
    interval_minutes=15
)

# Export to HEC-RAS DSS
StormGenerator.export_to_dss(
    hyetograph,
    dss_file="design_storm.dss",
    pathname="/PROJECT/PRECIP/DESIGN//15MIN/SYN/"
)
```

## When to Use This Skill

Use when you need to:

1. **Retrieve historical precipitation** - AORC data for calibration and validation
2. **Generate design storms** - Atlas 14 AEP events (10%, 2%, 1%, 0.2%, etc.)
3. **Process precipitation spatially** - Watershed averaging, areal reduction factors
4. **Aggregate precipitation temporally** - Match HEC-RAS/HMS timesteps
5. **Export to HEC-RAS/HMS** - DSS files, CSV time series, or direct HDF integration
6. **Identify storm events** - Extract individual storms from AORC record
7. **Apply temporal distributions** - SCS Type II, IA, III for design storms

## Core Concepts (Brief)

### AORC Dataset
- **Coverage**: CONUS (1979-present), ~800m hourly resolution
- **Format**: Cloud-optimized Zarr on AWS S3 (anonymous access)
- **Provider**: NOAA Office of Water Prediction
- **Use Case**: Historical calibration, storm event analysis

### NOAA Atlas 14
- **Coverage**: CONUS, Hawaii, Puerto Rico
- **Data**: Precipitation frequency estimates (depth-duration-frequency)
- **Access**: NOAA HDSC PFDS API (JSON)
- **Use Case**: Design storm generation for AEP events

### Temporal Distributions
- **SCS Type II**: Standard for most of US (peak at 12hr of 24hr storm)
- **SCS Type IA**: Pacific maritime climate (peak at 8hr)
- **SCS Type III**: Gulf Coast and Florida (peak at 13hr)

### Areal Reduction Factors (ARF)
- **< 10 sq mi**: ARF ≈ 1.0 (use point values)
- **10-100 sq mi**: ARF = 0.95-0.98
- **> 100 sq mi**: ARF < 0.95 (significant reduction)

## Common Workflows (High-Level)

### Calibration with AORC
1. Retrieve AORC for historical storm event
2. Apply spatial average over watershed
3. Aggregate to model timestep
4. Run HEC-RAS/HMS model
5. Compare modeled vs observed flow/stage

**Details**: See `ras_commander/precip/CLAUDE.md` "AORC Workflow" section

### Design Storm Analysis
1. Query Atlas 14 for design AEP
2. Generate temporal distribution (SCS Type II)
3. Apply areal reduction (if needed)
4. Export to HEC-RAS/HMS
5. Run model for design event

**Details**: See `ras_commander/precip/CLAUDE.md` "Atlas 14 Workflow" section

### Multi-Event Suite
1. Define AEP range (50% to 0.2%)
2. Loop through events and generate design storms
3. Batch run HEC-RAS models
4. Generate flood frequency curves

**Details**: See `examples/104_Atlas14_AEP_Multi_Project.ipynb`

## API Quick Reference (Navigate to CLAUDE.md for Details)

### PrecipAorc Methods
**Data Retrieval**:
- `retrieve_aorc_data()` - Download AORC time series for watershed
- `get_available_years()` - Query available data years (1979-present)
- `check_data_coverage()` - Verify spatial and temporal coverage

**Spatial Processing**:
- `spatial_average()` - Calculate areal average over watershed
- `extract_by_watershed()` - Extract data for HUC or custom polygon
- `resample_grid()` - Aggregate AORC grid cells to coarser resolution

**Temporal Processing**:
- `aggregate_to_interval()` - Aggregate to HEC-RAS/HMS intervals (1HR, 6HR, 1DAY)
- `extract_storm_events()` - Identify and extract individual storm events
- `calculate_rolling_totals()` - Compute N-hour rolling precipitation totals

**Output Formats**:
- `export_to_dss()` - DSS format for HEC-RAS/HMS
- `to_csv()` - CSV time series for HEC-HMS
- `to_netcdf()` - NetCDF for further analysis

### StormGenerator Methods
**Design Storm Creation**:
- `generate_design_storm()` - Create Atlas 14 design storm hyetograph
- `get_precipitation_frequency()` - Query Atlas 14 point precipitation values
- `apply_temporal_distribution()` - Apply standard temporal patterns (SCS Type II, etc.)

**Spatial Processing**:
- `apply_areal_reduction()` - Apply ARF for large watersheds
- `interpolate_point_values()` - Interpolate Atlas 14 values to grid
- `generate_multi_point_storms()` - Spatially distributed design storms

**Output Formats**:
- `export_to_dss()` - HEC-RAS DSS precipitation
- `export_to_hms_gage()` - HEC-HMS precipitation gage file
- `to_csv()` - Tabular hyetograph (CSV)

**Full method signatures and parameters**: See `ras_commander/precip/CLAUDE.md`

## Example Patterns

### AORC Storm Catalog Generation
```python
from ras_commander.precip import PrecipAorc
from ras_commander import init_ras_project
from ras_commander.hdf import HdfProject

# Initialize project
ras = init_ras_project("path/to/project", "6.6")

# Get project bounds from geometry HDF
geom_hdf = ras.project_folder / f"{ras.project_name}.g09.hdf"
bounds = HdfProject.get_project_bounds_latlon(
    geom_hdf,
    buffer_percent=50.0  # 50% buffer ensures full coverage
)

# Generate storm catalog
catalog = PrecipAorc.get_storm_catalog(
    bounds=bounds,
    year=2020,
    inter_event_hours=8.0,     # USGS standard for storm separation
    min_depth_inches=0.75,     # Minimum significant precipitation
    buffer_hours=48            # Simulation warmup buffer
)

# Returns DataFrame with:
# storm_id, start_time, end_time, sim_start, sim_end,
# total_depth_in, peak_intensity_in_hr, duration_hours, rank
```

**Complete workflow**: See `examples/900_aorc_precipitation.ipynb`

### Atlas 14 Multi-Event Suite
```python
from ras_commander.precip import StormGenerator

# Define AEP suite
aep_events = [10, 4, 2, 1, 0.5, 0.2]  # 10%, 4%, 2%, 1%, 0.5%, 0.2%

for aep in aep_events:
    # Query Atlas 14
    precip = StormGenerator.get_precipitation_frequency(
        location=(38.9, -77.0),
        duration_hours=24,
        aep_percent=aep
    )

    # Generate design storm
    hyetograph = StormGenerator.generate_design_storm(
        total_precip=precip,
        duration_hours=24,
        distribution="SCS_Type_II"
    )

    # Export to DSS
    dss_file = f"design_storm_{aep}pct.dss"
    StormGenerator.export_to_dss(hyetograph, dss_file)
```

**Complete multi-project workflow**: See `examples/722_atlas14_multi_project.ipynb`

## Dependencies

**Required**:
- pandas (time series handling)
- numpy (numerical operations)
- xarray (for AORC NetCDF data)
- requests (Atlas 14 API access)

**Optional**:
- geopandas (spatial operations on watersheds)
- rasterio (AORC grid processing)

**Installation**:
```bash
pip install ras-commander[precip]  # Includes all precipitation dependencies
# OR
pip install xarray rasterio geopandas
```

## Navigation Map

**When you need...**

### API Documentation
→ Read `ras_commander/precip/CLAUDE.md` (329 lines, complete API reference)

### AORC Workflow Example
→ Open `examples/900_aorc_precipitation.ipynb` (live working code)

### Atlas 14 Single Project
→ Open `examples/720_atlas14_aep_events.ipynb`

### Atlas 14 Multi-Project Batch
→ Open `examples/722_atlas14_multi_project.ipynb`

### Method Signatures and Parameters
→ Read `ras_commander/precip/CLAUDE.md` "Module Organization" section

### Use Cases and Performance
→ Read `ras_commander/precip/CLAUDE.md` "Common Use Cases" and "Performance" sections

### Data Source Details
→ Read `ras_commander/precip/CLAUDE.md` "Data Sources" section

## Key Design Principles

1. **Primary Sources First**: Always refer to `ras_commander/precip/CLAUDE.md` for authoritative API details
2. **Example Notebooks as References**: Use notebooks to understand workflows in practice
3. **No Duplication**: This skill does NOT duplicate workflows - it NAVIGATES to them
4. **Multi-Level Verifiability**: All outputs reviewable in HEC-RAS/HMS GUI
5. **Lazy Loading**: Optional dependencies only loaded when needed

## Performance Notes (Brief)

**AORC Data Retrieval**:
- Speed: ~1-5 minutes per year of hourly data
- Storage: ~10-50 MB per year (hourly, single watershed)
- Caching: Local cache recommended for repeated analyses

**Atlas 14 Queries**:
- Speed: < 5 seconds per query (API access)
- Rate Limiting: NOAA PFDS has request limits (respect usage guidelines)
- Caching: Automatic caching of API responses

**Details**: See `ras_commander/precip/CLAUDE.md` "Performance" section

## See Also

**Within Repository**:
- `ras_commander/precip/CLAUDE.md` - Complete precipitation API reference (PRIMARY SOURCE)
- `ras_commander/CLAUDE.md` - Parent library context
- `ras_commander/dss/AGENTS.md` - DSS file operations
- `examples/900_aorc_precipitation.ipynb` - AORC demonstration
- `examples/720_atlas14_aep_events.ipynb` - Atlas 14 single project
- `examples/722_atlas14_multi_project.ipynb` - Atlas 14 multi-project

**Related Components**:
- `ras_commander.RasUnsteady` - Unsteady flow file management
- `ras_commander.dss.RasDss` - DSS file operations
- `.claude/rules/python/path-handling.md` - Spatial data handling patterns

## Usage Pattern

1. **Understand the workflow**: Read `ras_commander/precip/CLAUDE.md` for complete details
2. **See it in action**: Open relevant example notebook (`examples/24_*.ipynb`, `examples/103_*.ipynb`, etc.)
3. **Implement**: Copy patterns from notebook, adapt to your project
4. **Verify**: Check outputs in HEC-RAS/HMS GUI

**This skill is a lightweight index - detailed content lives in primary sources.**
