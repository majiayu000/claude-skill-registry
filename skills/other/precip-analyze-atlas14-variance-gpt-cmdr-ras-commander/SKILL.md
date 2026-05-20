---
name: precip_analyze_atlas14-variance
type: skill
trigger_phrases:
  - atlas 14 variance
  - atlas14 variance
  - precipitation variance
  - spatial variance analysis
  - uniform rainfall
  - spatially variable rainfall
  - precipitation spatial variability
  - rain-on-grid variance
  - atlas 14 grid
  - atlas14 grid
  - noaa atlas 14 conus
  - precipitation frequency grid
  - assess uniform rainfall
  - extent-based precipitation
  - 2d flow area precipitation
description: |
  Analyze spatial variability of NOAA Atlas 14 precipitation frequency estimates
  within HEC-RAS model domains using intelligent extent-based downloading.

  Helps determine whether uniform rainfall assumptions are appropriate for
  rain-on-grid modeling by calculating min/max/mean/range statistics within
  2D flow areas or project extents.

  Uses NOAA CONUS NetCDF with HTTP byte-range requests for 99.9% data reduction
  compared to traditional state-level ZIP downloads.

  Primary sources:
  - ras_commander/precip/CLAUDE.md (lines 118-629) - Complete workflows
  - ras_commander/precip/Atlas14Grid.py - API reference
  - ras_commander/precip/Atlas14Variance.py - Variance analysis API
  - examples/725_atlas14_spatial_variance.ipynb - Working demonstration
---

# Atlas 14 Spatial Variance Analysis

**User-invocable skill for assessing precipitation spatial variability in HEC-RAS models**

## Primary Sources (Read These First)

**Complete Workflows** (lines 540-629):
- `ras_commander/precip/CLAUDE.md`
  - Lines 118-197: Module documentation (Atlas14Grid, Atlas14Variance)
  - Lines 540-629: Complete Atlas 14 Grid Workflow (4 steps)
  - Lines 522-538: Performance metrics

**API Reference**:
- `ras_commander/precip/Atlas14Grid.py` (404 lines)
  - `get_pfe_from_project()` - Main entry point for HEC-RAS integration
  - `get_pfe_for_bounds()` - Direct bounding box query
  - `get_point_pfe()` - Single point lookup

- `ras_commander/precip/Atlas14Variance.py` (322 lines)
  - `analyze()` - Full variance analysis
  - `analyze_quick()` - Rapid assessment (100-yr, 24-hr)
  - `is_uniform_rainfall_appropriate()` - Decision support
  - `generate_report()` - Export with plots

**Working Example**:
- `examples/725_atlas14_spatial_variance.ipynb`
  - Direct bounds queries
  - Point lookups
  - HEC-RAS project integration
  - Visualization

**Quick Reference**:
- `.claude/rules/hec-ras/precipitation.md` (lines 104-126)

---

## Quick Reference

### Typical Workflow (3 Steps)

```python
from ras_commander.precip import Atlas14Variance

# Step 1: Quick check for representative event
stats = Atlas14Variance.analyze_quick("MyProject.g01.hdf")

# Step 2: Interpret results
if stats['range_pct'] > 10:
    # High variance - run full analysis
    results = Atlas14Variance.analyze(
        geom_hdf="MyProject.g01.hdf",
        durations=[6, 12, 24],
        return_periods=[10, 25, 50, 100]
    )

    # Step 3: Generate report
    Atlas14Variance.generate_report(
        results,
        output_dir="Atlas14_Report",
        project_name="My Project"
    )
else:
    # Low variance - uniform rainfall OK
    print("✓ Uniform rainfall appropriate")
```

### Direct Grid Access

```python
from ras_commander.precip import Atlas14Grid

# Get PFE for project extent
pfe = Atlas14Grid.get_pfe_from_project(
    geom_hdf="MyProject.g01.hdf",
    extent_source="2d_flow_area",  # or "project_extent"
    durations=[6, 12, 24],
    return_periods=[10, 50, 100],
    buffer_percent=10.0
)

# Access data
print(f"Grid size: {pfe['lat'].shape[0]} x {pfe['lon'].shape[0]}")
print(f"100-yr 24-hr max: {pfe['pfe_24hr'][:,:,5].max():.2f} inches")
```

### Point Query (No Project)

```python
# Quick lookup for single location
df = Atlas14Grid.get_point_pfe(
    lat=29.76,
    lon=-95.37,
    durations=[6, 12, 24],
    return_periods=[10, 50, 100, 500]
)
print(df)
```

---

## When to Use This Skill

### Use Atlas14Variance When:

1. **Before rain-on-grid modeling** - Assess if uniform rainfall is valid
2. **Large model domains** (>100 sq mi) - Spatial variance more likely
3. **Multi-event analysis** - Compare variance across return periods
4. **Engineering review** - Generate reports for professional documentation

### Decision Criteria

| Range % | Interpretation | Recommendation |
|---------|----------------|----------------|
| < 5% | Very low variance | Uniform rainfall appropriate |
| 5-10% | Low variance | Uniform likely OK, monitor |
| 10-20% | Moderate variance | Consider spatially variable |
| > 20% | High variance | Use spatially variable rainfall |

**Representative Event**: 100-year, 24-hour is typical for quick assessment

---

## Common Workflows

### Workflow 1: Quick Assessment

**Purpose**: Rapid check if variance analysis is needed

**See**: `ras_commander/precip/CLAUDE.md` lines 544-564

```python
from ras_commander.precip import Atlas14Variance

stats = Atlas14Variance.analyze_quick("MyProject.g01.hdf")

if stats['range_pct'] > 10:
    print("⚠️ Run full analysis - high variance detected")
```

### Workflow 2: Full Analysis

**Purpose**: Comprehensive variance across multiple events

**See**: `ras_commander/precip/CLAUDE.md` lines 566-585

```python
results = Atlas14Variance.analyze(
    geom_hdf="MyProject.g01.hdf",
    durations=[6, 12, 24, 48],
    return_periods=[10, 25, 50, 100, 500],
    extent_source="2d_flow_area",
    variance_denominator='min',  # or 'max', 'mean'
    output_dir="Atlas14_Variance_Report"
)
```

### Workflow 3: Report Generation

**Purpose**: Engineering documentation

**See**: `ras_commander/precip/CLAUDE.md` lines 587-605

```python
report_dir = Atlas14Variance.generate_report(
    results_df=results,
    output_dir="reports/",
    project_name="My Project",
    include_plots=True
)

# Files created:
# - variance_statistics.csv
# - variance_summary.csv
# - variance_by_duration.png
# - variance_heatmap.png
```

### Workflow 4: Custom Grid Analysis

**Purpose**: Export for HEC-RAS import or custom processing

**See**: `ras_commander/precip/CLAUDE.md` lines 607-629

```python
from ras_commander.precip import Atlas14Grid

pfe = Atlas14Grid.get_pfe_from_project(
    geom_hdf="MyProject.g01.hdf",
    extent_source="2d_flow_area",
    durations=[24],
    return_periods=[100]
)

# Access raw arrays for custom analysis
lat = pfe['lat']
lon = pfe['lon']
data_100yr_24hr = pfe['pfe_24hr'][:, :, 5]
```

---

## Key Parameters

### extent_source

Controls which geometry is used for extent extraction:

- **`"2d_flow_area"`** (default, recommended)
  - Uses union of 2D flow area perimeters
  - Most relevant for rain-on-grid models
  - Can filter to specific areas via `mesh_area_names`

- **`"project_extent"`**
  - Uses full project bounding extent
  - Includes 1D and storage areas
  - Larger extent = more data downloaded

### use_huc12_boundary

Controls whether to use HUC12 watershed instead of 2D flow area:

- **`False`** (default)
  - Uses 2D flow area perimeters or project extent
  - Fastest analysis (smaller area)

- **`True`**
  - Finds HUC12 watershed containing center of 2D flow area
  - Downloads HUC12 boundary from NHDPlus
  - Analyzes full contributing watershed
  - Typically higher variance (larger extent)
  - Requires `pygeohydro` package

**Example**:
```python
# Analyze using HUC12 watershed
results = Atlas14Variance.analyze(
    geom_hdf="MyProject.g01.hdf",
    use_huc12_boundary=True
)
```

### variance_denominator

Controls how range percentage is calculated:

- **`'min'`** (default) - `range_pct = (max - min) / min × 100`
  - Shows variance relative to minimum value
  - Matches HEC-Commander approach
  - More sensitive to variance

- **`'max'`** - `range_pct = (max - min) / max × 100`
  - Shows variance relative to maximum value
  - More conservative metric

- **`'mean'`** - `range_pct = (max - min) / mean × 100`
  - Engineering standard
  - Balanced perspective

---

## Technical Details

### NOAA CONUS NetCDF Structure

**URL**: `https://hdsc.nws.noaa.gov/pub/hdsc/data/tx/NOAA_Atlas_14_CONUS.nc`

| Property | Value |
|----------|-------|
| Coverage | CONUS (24°N-50°N, -125°W to -66°W) |
| Resolution | ~0.0083° (~830m at 30°N) |
| Format | HDF5-based NetCDF-4 |
| Size | 320 MB (chunked for efficient access) |
| Chunking | (49, 111, 1) - optimized for spatial access |
| HTTP Support | Accept-Ranges: bytes ✓ |

**Available Data**:
- Durations: 1, 2, 3, 6, 12, 24, 48, 72, 96, 168 hours
- Return Periods: 2, 5, 10, 25, 50, 100, 200, 500, 1000 years
- Scale Factor: 0.01 (raw values × 0.01 = inches)

### Data Transfer Efficiency

| Project Size | Grid Cells | Data Transfer | Full Grid | Reduction |
|--------------|------------|---------------|-----------|-----------|
| Small (0.5° × 0.5°) | ~3,600 | ~60 KB | 379 MB | 99.98% |
| Medium (1° × 1°) | ~14,400 | ~250 KB | 379 MB | 99.93% |
| Large (2° × 2°) | ~57,600 | ~1 MB | 379 MB | 99.74% |

**Comparison**: Traditional approach downloads 50-100 MB per state as ZIP files.

---

## Critical Warnings

### CONUS Coverage Only

The NOAA CONUS NetCDF covers Continental US only:

**Covered**: Lower 48 states (24°N-50°N, -125°W to -66°W)

**Not Covered**:
- Hawaii (use StormGenerator point API instead)
- Alaska (use StormGenerator point API instead)
- Puerto Rico (use StormGenerator point API instead)
- Offshore areas (no data)

### Internet Required

Atlas14Grid requires internet access to NOAA servers:
- No offline mode currently implemented
- Cache coordinates in memory (cleared with `Atlas14Grid.clear_cache()`)
- Future: Local disk caching planned

### Return Period Mapping

The `ari` dimension uses return periods, not ARI indices:

```python
ari = [2, 5, 10, 25, 50, 100, 200, 500, 1000]

# 100-year event is index 5
pfe_100yr = pfe['pfe_24hr'][:, :, 5]  # Correct

# NOT index 100
pfe_100yr = pfe['pfe_24hr'][:, :, 100]  # Wrong!
```

---

## Dependencies

**Required** (already in ras-commander):
- `h5py>=3.0.0` - HDF5/NetCDF access
- `numpy` - Array operations
- `pandas` - DataFrames
- `geopandas>=0.12.0` - Spatial operations
- `fsspec>=2023.0.0` - Remote file systems (HTTP)

**Optional**:
- `matplotlib` - Plotting (for `generate_report()`)
- `rioxarray` - Enhanced raster operations (future)

**Installation**:
```bash
pip install ras-commander  # All required deps included
```

---

## Navigation Map

**For complete workflows**: Read `ras_commander/precip/CLAUDE.md` lines 540-629

**For API details**: Read docstrings in:
- `ras_commander/precip/Atlas14Grid.py`
- `ras_commander/precip/Atlas14Variance.py`

**For working code**: Run `examples/725_atlas14_spatial_variance.ipynb`

**For quick reference**: See `.claude/rules/hec-ras/precipitation.md` lines 104-126

**For research background**: See `.claude/outputs/atlas14-variance-research-summary.md`

---

## Common Questions

### Q: When should I use this instead of StormGenerator?

**Use Atlas14Grid/Variance when**:
- You need **spatial precipitation grids** (not just point values)
- You want to **assess uniform rainfall validity**
- You have a **large model domain** where variance matters

**Use StormGenerator when**:
- You need **point precipitation** for a single location
- You want **hyetograph generation** (temporal distribution)
- You're doing **design storm analysis** (not variance assessment)

### Q: How accurate is the spatial subsetting?

The HTTP range request approach downloads **exactly the grid cells within the specified extent**. Validation shows:
- ✓ Matches NOAA PFDS web interface values
- ✓ Houston, TX 100-yr 24-hr: 17.00 inches (correct)
- ✓ No data loss from subsetting
- ✓ Scale factor properly applied (0.01)

### Q: What if my project spans multiple states?

The CONUS NetCDF covers the entire Continental US in a single file, so:
- ✓ Multi-state projects work automatically
- ✓ No manual merging required
- ✓ No need to specify states

This is a **major advantage** over HEC-Commander's approach, which requires downloading separate state datasets and manually merging them.

### Q: Can I export the grid data to HEC-RAS?

**Current**: `Atlas14Grid` returns numpy arrays - export to GeoTIFF/NetCDF not yet implemented

**Workaround**: Use the data for variance analysis, then use `StormGenerator` or `Atlas14Storm` to create HEC-RAS precipitation input files

**Future**: Planned enhancement for direct GeoTIFF/NetCDF export

---

## Skill Invocation

When user asks to:
- "Analyze Atlas 14 spatial variance for my HEC-RAS project"
- "Check if uniform rainfall is appropriate"
- "Get precipitation frequency grids for my 2D flow areas"
- "Assess precipitation spatial variability"

**Respond with**:

1. **Quick Check First**:
   ```python
   from ras_commander.precip import Atlas14Variance

   stats = Atlas14Variance.analyze_quick("project.g01.hdf")
   print(f"Range: {stats['range_pct']:.1f}%")
   ```

2. **Interpret Results**:
   - Range < 10%: "✓ Uniform rainfall appropriate"
   - Range > 10%: "⚠️ Consider full analysis"

3. **Full Analysis if Needed**:
   ```python
   results = Atlas14Variance.analyze("project.g01.hdf")
   ok, msg = Atlas14Variance.is_uniform_rainfall_appropriate(results)
   print(msg)
   ```

4. **Generate Report**:
   ```python
   Atlas14Variance.generate_report(
       results,
       output_dir="Atlas14_Report",
       include_plots=True
   )
   ```

---

## Related Skills and Agents

**Related Skills**:
- `/precip_analyze_aorc` - Historic gridded precipitation
- (Future) `/atlas14-design-storms` - Hyetograph generation

**Relevant Agents**:
- `precipitation-specialist` - General precipitation workflows
- `hdf-analyst` - Extract HEC-RAS geometry for extent

**Complementary Classes**:
- `StormGenerator` - Point-based design storms (see `ras_commander/precip/CLAUDE.md` lines 44-77)
- `Atlas14Storm` - HMS-equivalent hyetographs (lines 79-116)
- `PrecipAorc` - Historic AORC data (lines 13-42)

---

## Examples by Use Case

### Use Case 1: Pre-Modeling Assessment

**Scenario**: Determine if uniform rainfall is valid before running rain-on-grid model

```python
from ras_commander.precip import Atlas14Variance

# Quick check
stats = Atlas14Variance.analyze_quick("MyProject.g01.hdf")

if stats['range_pct'] <= 10:
    print("Proceed with uniform rainfall")
    # Run HEC-RAS with single precipitation source
else:
    print("Consider spatially variable rainfall")
    # Run full analysis to quantify
```

### Use Case 2: Multi-Event Comparison

**Scenario**: Compare variance across multiple design storms

```python
results = Atlas14Variance.analyze(
    geom_hdf="MyProject.g01.hdf",
    durations=[6, 12, 24, 48],
    return_periods=[10, 25, 50, 100, 200, 500]
)

# Find highest variance event
worst = results.loc[results['range_pct'].idxmax()]
print(f"Highest variance: {worst['duration_hr']}-hr, {worst['return_period_yr']}-yr")
print(f"Range: {worst['range_pct']:.1f}%")
```

### Use Case 3: Engineering Report

**Scenario**: Generate documentation for design report

```python
# Full analysis
results = Atlas14Variance.analyze("MyProject.g01.hdf")

# Generate report with plots
report_dir = Atlas14Variance.generate_report(
    results,
    output_dir="Engineering_Report/Atlas14_Variance",
    project_name="Smith Creek Dam",
    include_plots=True
)

# Files suitable for inclusion in engineering documentation
```

### Use Case 4: Specific 2D Flow Areas

**Scenario**: Analyze variance for specific mesh areas only

```python
pfe = Atlas14Grid.get_pfe_from_project(
    geom_hdf="MyProject.g01.hdf",
    extent_source="2d_flow_area",
    mesh_area_names=["Floodplain_Upper", "Floodplain_Lower"],
    durations=[24],
    return_periods=[100]
)

# Only analyzes specified mesh areas
```

---

## Troubleshooting

### "ImportError: fsspec not installed"

**Cause**: Missing `fsspec` dependency

**Fix**:
```bash
pip install fsspec>=2023.0.0
# or
pip install --upgrade ras-commander
```

### "ValueError: No data within bounds"

**Cause**: Project extent outside CONUS coverage

**Check**:
```python
from ras_commander.hdf import HdfProject

bounds = HdfProject.get_project_bounds_latlon("project.g01.hdf")
print(f"Project bounds: {bounds}")

# Valid CONUS: lon=-125 to -66, lat=24 to 50
```

**Solution**: Project must be within Continental US

### "High variance but uniform rainfall expected"

**Possible Causes**:
1. Orographic effects (mountains causing local gradients)
2. Large model domain (>10° extent)
3. Edge of Atlas 14 data coverage

**Validation**:
- Compare with NOAA PFDS maps visually
- Check if variance concentrated at edges
- Consider physical geography (elevation changes)

### "IOError: Cannot access NOAA Atlas 14 CONUS NetCDF"

**Causes**:
1. Network connectivity issues
2. NOAA server temporarily down
3. Firewall blocking HTTPS

**Check**:
```python
# Test server availability
if Atlas14Grid.is_available():
    print("NOAA server reachable")
else:
    print("Cannot reach NOAA server - check network")
```

---

## Performance Tips

### 1. Use Quick Check First

Don't run full analysis unless needed:

```python
# Quick check is fast (~5 seconds)
stats = Atlas14Variance.analyze_quick("project.g01.hdf")

# Only run full analysis if variance is high
if stats['range_pct'] > 10:
    results = Atlas14Variance.analyze("project.g01.hdf")
```

### 2. Cache Coordinates

Coordinates are cached after first access:

```python
# First call downloads coordinates (~11 seconds)
pfe1 = Atlas14Grid.get_pfe_for_bounds(...)

# Subsequent calls use cache (much faster)
pfe2 = Atlas14Grid.get_pfe_for_bounds(...)

# Clear cache when done to free memory
Atlas14Grid.clear_cache()
```

### 3. Minimize Extent

Smaller extent = less data transfer:

```python
# Use 2D flow areas (smaller) instead of project extent (larger)
pfe = Atlas14Grid.get_pfe_from_project(
    geom_hdf="project.g01.hdf",
    extent_source="2d_flow_area",  # Smaller
    buffer_percent=5.0  # Minimal buffer
)
```

---

## See Also

**Primary Documentation**:
- `ras_commander/precip/CLAUDE.md` - Complete precipitation workflows
- `.claude/rules/hec-ras/precipitation.md` - Quick reference guide

**Related Features**:
- `StormGenerator` - Point-based Atlas 14 queries and hyetograph generation
- `Atlas14Storm` - HMS-equivalent temporal distributions
- `PrecipAorc` - Historic gridded precipitation data

**Example Notebooks**:
- `examples/725_atlas14_spatial_variance.ipynb` - This workflow
- `examples/720_atlas14_aep_events.ipynb` - Point-based design storms
- `examples/900_aorc_precipitation.ipynb` - Historic precipitation

**Research**:
- `.claude/outputs/atlas14-variance-research-summary.md` - Discovery of CONUS NetCDF approach
- `.claude/outputs/atlas14-variance-implementation-summary.md` - Implementation details
