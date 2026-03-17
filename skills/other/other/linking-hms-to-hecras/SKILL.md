---
name: linking-hms-to-hecras
description: |
  Links HEC-HMS watershed models to HEC-RAS river models by extracting HMS DSS results
  and preparing them for RAS boundary condition import. Handles flow hydrograph export,
  spatial referencing (HMS outlets to RAS cross sections), DSS pathname formatting,
  quality validation, and time series alignment. Use when setting up HMS→RAS workflows,
  exporting HMS results for RAS, preparing upstream boundary conditions, or coordinating
  watershed-to-river integrated modeling. Leverages shared RasDss infrastructure for
  consistent DSS operations across both tools.
  Trigger keywords: HMS to RAS, link HMS RAS, boundary condition, upstream BC, watershed
  to river, integrated model, export HMS, DSS pathname, spatial matching, hydrograph.
---

# Linking HMS to HEC-RAS

## Quick Start

```python
from hms_commander import init_hms_project, HmsCmdr, HmsResults, HmsGeo

# 1. Execute HMS simulation
init_hms_project("watershed")
HmsCmdr.compute_run("Design_Storm")

# 2. Extract flow hydrograph for RAS
dss_file = hms.run_df.loc["Design_Storm", "dss_file"]
flows = HmsResults.get_outflow_timeseries(dss_file, "Watershed_Outlet")

# 3. Document outlet location for spatial matching
lat, lon = HmsGeo.get_project_centroid_latlon("project.geo")
print(f"Outlet location: {lat:.4f}°N, {lon:.4f}°W")

# 4. Handoff to RAS engineer
print(f"DSS file: {dss_file}")
print(f"Pathname: /BASIN/WATERSHED_OUTLET/FLOW/15MIN/DESIGN_STORM/")
print(f"Peak flow: {flows['Flow'].max()} cfs")
```

## Primary Sources

**Code**:
- `hms_commander/HmsResults.py` - Flow extraction
- `hms_commander/HmsDss.py` - DSS operations (wraps RasDss)
- `hms_commander/HmsGeo.py` - Spatial reference

**Integration**: Uses `ras_commander.RasDss` for shared DSS infrastructure

**Rules**: `.claude/rules/integration/hms-ras-linking.md` - Complete workflow

**Cross-Reference**: `ras-commander/.claude/skills/importing-hms-boundaries/` - RAS side

## When to Use This Skill

- Setting up integrated HMS→RAS modeling workflows
- Exporting HMS hydrographs for RAS boundary conditions
- Preparing upstream boundary conditions from watershed analysis
- Coordinating watershed-to-river models
- Validating HMS results before handoff to RAS
- Documenting spatial reference for outlet matching

## Workflow Overview

```
HEC-HMS (Watershed)          HEC-RAS (River)
    ↓                            ↓
1. Precipitation             Geometry
    ↓                            ↓
2. Runoff Generation     ←── 5. Import HMS Flows
    ↓                            ↓
3. DSS Output           6. Hydraulic Analysis
    ↓                            ↓
4. Extract & Validate    Flood Inundation
```

**HMS Responsibilities** (this skill):
1. Execute watershed simulation
2. Generate runoff hydrographs
3. Export to DSS format
4. Extract flows for validation
5. Document spatial reference
6. Validate quality before handoff

**RAS Responsibilities** (see ras-commander):
- Import DSS as boundary condition
- Spatial matching (HMS outlet → RAS cross section)
- Time series alignment
- Hydraulic analysis

## Core Capabilities

### 1. Flow Hydrograph Extraction

```python
from hms_commander import HmsResults

# Extract single outlet
flows = HmsResults.get_outflow_timeseries(dss_file, "Outlet")
# Returns: DataFrame with datetime index, flow in cfs

# Extract multiple tributaries
tributaries = ["Trib_A", "Trib_B", "Trib_C"]
for trib in tributaries:
    flows = HmsResults.get_outflow_timeseries(dss_file, trib)
    print(f"{trib}: Peak = {flows['Flow'].max()} cfs")
```

**See**: `extracting-dss-results` skill for complete extraction capabilities

### 2. Spatial Reference Documentation

```python
from hms_commander import HmsGeo

# Get project centroid (general reference)
lat, lon = HmsGeo.get_project_centroid_latlon("project.geo", crs_epsg="EPSG:2278")

# Export subbasin boundaries to GeoJSON
HmsGeo.export_all_geojson(
    basin_path="project.basin",
    output_dir="geojson",
    geo_path="project.geo"
)
# Creates: geojson/subbasins.geojson
# RAS engineer can view in GIS to match outlets → cross sections
```

**Critical**: RAS engineer needs outlet locations to spatially match HMS→RAS

### 3. DSS Pathname Format

HMS uses standard DSS pathname: `/A/B/C/D/E/F/`

**Parts**:
- **A**: Basin name
- **B**: Element name (outlet, junction, reach)
- **C**: Parameter (FLOW)
- **D**: Time interval (15MIN, 1HOUR)
- **E**: Run name
- **F**: Version (blank)

**Example**: `/WATERSHED/OUTLET/FLOW/15MIN/100YR/`

```python
from hms_commander import HmsDss

# Parse pathname
parts = HmsDss.parse_dss_pathname("/WATERSHED/OUTLET/FLOW/15MIN/100YR/")
# Returns: {'basin': 'WATERSHED', 'element': 'OUTLET', ...}

# Create pathname
pathname = HmsDss.create_dss_pathname(
    basin="WATERSHED",
    element="Outlet",
    param_type="FLOW",
    interval="15MIN"
)
```

**See**: `.claude/rules/integration/hms-ras-linking.md` for pathname details

### 4. Quality Validation

Before handing off to RAS:

```python
from hms_commander import HmsResults

# Check peak flows
peaks = HmsResults.get_peak_flows(dss_file)
assert all(peaks["Peak Flow (cfs)"] > 0), "Negative peaks!"

# Check volume conservation
volumes = HmsResults.get_volume_summary(dss_file)
precip_vol = volumes["Precipitation Volume (ac-ft)"].sum()
runoff_vol = volumes["Runoff Volume (ac-ft)"].sum()
loss_ratio = 1 - (runoff_vol / precip_vol)
print(f"Loss ratio: {loss_ratio:.1%}")  # Should be 20-70%

# Check time series completeness
flows = HmsResults.get_outflow_timeseries(dss_file, "Outlet")
assert flows.notna().all().all(), "Missing data!"
```

## Common Workflows

### Workflow 1: Single Watershed Outlet → RAS Upstream BC

**Complete Example**:

```python
from hms_commander import init_hms_project, HmsCmdr, HmsResults, HmsGeo, hms

# === HMS SIDE ===

# 1. Execute watershed simulation
init_hms_project(r"C:\Projects\Watershed")
HmsCmdr.compute_run("100yr_Storm")

# 2. Extract results
dss_file = hms.run_df.loc["100yr_Storm", "dss_file"]
outlet_flows = HmsResults.get_outflow_timeseries(dss_file, "Watershed_Outlet")

# 3. Validate quality
peaks = HmsResults.get_peak_flows(dss_file)
peak_flow = peaks.loc["Watershed_Outlet", "Peak Flow (cfs)"]
peak_time = peaks.loc["Watershed_Outlet", "Time to Peak"]
print(f"Peak: {peak_flow} cfs at {peak_time}")

# 4. Document spatial reference
lat, lon = HmsGeo.get_project_centroid_latlon("Watershed.geo", crs_epsg="EPSG:2278")
HmsGeo.export_all_geojson("Watershed.basin", "geojson", "Watershed.geo")

# 5. Prepare handoff documentation
print(f"""
HMS Results Ready for RAS Import
=================================
DSS File: {dss_file}
Pathname: /WATERSHED/WATERSHED_OUTLET/FLOW/15MIN/100YR_STORM/
Outlet Location: {lat:.4f}°N, {lon:.4f}°W
Peak Flow: {peak_flow} cfs
Time to Peak: {peak_time}
GeoJSON: geojson/subbasins.geojson (view in GIS for spatial matching)

Next Step: RAS engineer imports as upstream boundary condition
""")

# === RAS SIDE (informational, see ras-commander) ===
# 1. Open RAS project
# 2. Import DSS file as upstream boundary condition
# 3. Spatially match outlet location to RAS cross section
# 4. Validate time series alignment
# 5. Run hydraulic analysis
```

**See**: `examples/single-outlet-to-ras.md` for complete walkthrough

### Workflow 2: Multiple Tributaries → Multiple RAS BCs

```python
# Extract flows for multiple tributaries
tributaries = ["North_Fork", "South_Fork", "West_Branch"]

for trib in tributaries:
    flows = HmsResults.get_outflow_timeseries(dss_file, trib)
    peak = flows['Flow'].max()
    print(f"{trib}: Peak = {peak} cfs")
    # Each becomes separate RAS upstream BC
```

**See**: `examples/multiple-tributaries.md` for complete example

### Workflow 3: Internal Junctions → RAS Lateral Inflows

```python
from hms_commander import HmsBasin

# Get all junctions in basin model
junctions = HmsBasin.get_junctions("project.basin")

# Extract flows at each junction
for junction in junctions.index:
    flows = HmsResults.get_outflow_timeseries(dss_file, junction)
    # Each junction becomes lateral inflow in RAS
```

**See**: `examples/lateral-inflows.md` for complete example

## Cross-Tool Integration

### Shared DSS Infrastructure

**Both HMS and RAS use RasDss**:

```python
from hms_commander import HmsDss

# HmsDss wraps ras_commander.RasDss
if HmsDss.is_available():
    catalog = HmsDss.get_catalog(dss_file)
    flows = HmsDss.read_timeseries(dss_file, pathname)
```

**Why This Matters**:
- RAS can directly read HMS DSS files (same Java bridge)
- No format conversion needed
- Consistent operations across tools

**See**: `.claude/rules/hec-hms/dss-operations.md` for DSS integration details

### Time Step Compatibility

**HMS**: Typically 15-minute or 1-hour intervals
**RAS**: Computation interval set in unsteady flow plan

**Recommendations**:
- Urban watersheds: 15-minute HMS interval
- Large rural watersheds: 1-hour HMS interval
- RAS can interpolate, but matching intervals preferred

### Units Consistency

**HMS**: CFS (cubic feet per second) - standard
**RAS**: CFS (cubic feet per second) - standard

✅ **Units match** - no conversion needed

### Coordinate Systems

**Critical**: Both must use same coordinate system

```python
# Ensure HMS uses same CRS as RAS project
lat, lon = HmsGeo.get_project_centroid_latlon(
    "project.geo",
    crs_epsg="EPSG:2278"  # Match RAS project CRS
)
```

## Quality Checks

### Pre-Handoff Validation

```python
def validate_hms_results_for_ras(dss_file, outlet_name):
    """Validate HMS results before RAS import."""
    from hms_commander import HmsResults

    # 1. Check peak flows are positive
    peaks = HmsResults.get_peak_flows(dss_file)
    assert peaks.loc[outlet_name, "Peak Flow (cfs)"] > 0, "Zero or negative peak!"

    # 2. Check volume conservation
    volumes = HmsResults.get_volume_summary(dss_file)
    precip_vol = volumes["Precipitation Volume (ac-ft)"].sum()
    runoff_vol = volumes["Runoff Volume (ac-ft)"].sum()
    loss_ratio = 1 - (runoff_vol / precip_vol)
    assert 0.2 <= loss_ratio <= 0.7, f"Unrealistic loss ratio: {loss_ratio:.1%}"

    # 3. Check time series has no gaps
    flows = HmsResults.get_outflow_timeseries(dss_file, outlet_name)
    assert flows.notna().all().all(), "Missing data in time series!"

    # 4. Check reasonable flow values
    assert flows["Flow"].min() >= 0, "Negative flows detected!"

    print("✅ HMS results validated for RAS import")
    return True
```

**See**: `reference/quality-checks.md` for complete validation procedures

## Troubleshooting

### Issue 1: RAS Can't Find DSS File

**Symptom**: RAS reports "DSS file not found"

**Solution**: Provide absolute path or copy DSS to RAS project folder
```python
import shutil
shutil.copy(hms_dss_file, ras_project_folder)
```

### Issue 2: Spatial Mismatch

**Symptom**: Uncertain which RAS cross section matches HMS outlet

**Solution**: Export HMS boundaries to GeoJSON, view in GIS alongside RAS geometry
```python
HmsGeo.export_all_geojson("basin.basin", "geojson", "project.geo")
# Open geojson/subbasins.geojson in QGIS/ArcGIS with RAS geometry
```

### Issue 3: Time Series Gaps

**Symptom**: HMS results have missing timesteps

**Solution**: Check HMS log file, re-run with shorter time interval
```python
# Check for computation errors in HMS log
log_file = hms.project_folder / "RUN_Design_Storm.log"
print(log_file.read_text())
```

## Reference Files

**Detailed Documentation** (load on-demand):
- `reference/dss-pathname-format.md` - Complete pathname structure
- `reference/spatial-matching.md` - GIS-based outlet matching
- `reference/quality-checks.md` - Validation procedures
- `reference/time-alignment.md` - Time step compatibility

**Complete Examples**:
- `examples/single-outlet-to-ras.md` - Basic workflow
- `examples/multiple-tributaries.md` - Multiple upstream BCs
- `examples/lateral-inflows.md` - Internal junction flows
- `examples/qaqc-checklist.md` - Pre-handoff validation

## Integration Points

**Before This Skill**:
- Execute HMS simulation (see `executing-hms-runs` skill)
- Validate basin model (see `parsing-basin-models` skill)
- Update precipitation if needed (see `updating-met-models` skill)

**After This Skill**:
- RAS imports boundary conditions (see `ras-commander/.claude/skills/importing-hms-boundaries/`)
- RAS runs hydraulic analysis
- Compare HMS peaks vs RAS peaks (QAQC)

## Related Skills

- **executing-hms-runs** - Generate HMS results
- **extracting-dss-results** - Extract and validate flows
- **parsing-basin-models** - Understand watershed structure

**Cross-Repository**:
- **ras-commander/importing-hms-boundaries** - RAS side of workflow
- **hms-ras-workflow-coordinator** (subagent) - Coordinates both sides

## Future Automation

**Potential**: Production task agent for end-to-end linking

**Would Automate**:
1. Extract HMS hydrographs from DSS
2. Spatial matching (HMS outlets → RAS cross sections)
3. Import to RAS boundary conditions
4. Validate alignment (peak, volume, timing)
5. Generate QAQC report

**Status**: Documented in planning, not yet implemented

**See**: `hms_agents/HMS_to_RAS_Linker/` (placeholder for future)

---

**Navigation**: This skill covers the HMS side of HMS→RAS integration. For the RAS side, see `ras-commander/.claude/skills/importing-hms-boundaries/`. For coordinated workflows, use the `hms-ras-workflow-coordinator` subagent.
