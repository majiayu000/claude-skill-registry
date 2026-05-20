---
name: hecras_extract_results
allowed-tools: [Read, Grep, Glob]
description: |
  Extract HEC-RAS hydraulic results from HDF files including water surface elevations (WSE),
  depths, velocities, and flows for both steady and unsteady simulations. Handles cross section
  time series, 2D mesh results, maximum envelopes, and dam breach results. Use when you need to
  extract, analyze, or post-process HEC-RAS simulation outputs, retrieve water levels, query
  velocity fields, get depth grids, extract flow data, analyze breach hydrographs, or pull
  hydraulic variables from .hdf result files.
---

# Extracting HEC-RAS Results

**Purpose**: Lightweight skill index that navigates you to primary documentation sources. This skill does NOT duplicate content - it points you to where complete, authoritative information lives.

**Primary Sources**:
- **HDF Class Reference**: `C:\GH\ras-commander\ras_commander\hdf\AGENTS.md` (215 lines) - Complete class hierarchy, lazy loading patterns, decorators
- **Library Context**: `C:\GH\ras-commander\ras_commander\CLAUDE.md` - HDF architecture overview, subpackage organization
- **Example Notebooks**:
  - `C:\GH\ras-commander\examples\10_1d_hdf_data_extraction.ipynb` - 1D cross section results (unsteady)
  - `C:\GH\ras-commander\examples\11_2d_hdf_data_extraction.ipynb` - 2D mesh results (comprehensive)
  - `C:\GH\ras-commander\examples\19_steady_flow_analysis.ipynb` - Steady state results (complete workflow)
  - `C:\GH\ras-commander\examples\18_breach_results_extraction.ipynb` - Dam breach results
- **Code Docstrings**: All HDF classes have comprehensive docstrings with parameter details

---

## Quick Start

### Minimal Working Example

```python
from ras_commander import init_ras_project, HdfResultsPlan, HdfResultsMesh

# Initialize project
init_ras_project("C:/Projects/MyModel", "6.6")

# Check simulation type
is_steady = HdfResultsPlan.is_steady_plan("01")

# Extract results based on type
if is_steady:
    profiles = HdfResultsPlan.get_steady_profile_names("01")
    wse = HdfResultsPlan.get_steady_wse("01", profile_name="100 year")
else:
    max_wse = HdfResultsMesh.get_mesh_maximum("01", variable="Water Surface")
```

---

## Navigation Guide

### 1. Architecture & Organization

**Read First**: `C:\GH\ras-commander\ras_commander\hdf\AGENTS.md`

This is the **definitive reference** for:
- 18 HDF classes and their organization
- Module structure (Core, Geometry, Results, Infrastructure, Visualization)
- Class hierarchy and dependencies
- Lazy loading patterns for heavy dependencies
- Decorator usage (`@staticmethod`, `@log_call`, `@standardize_input`)
- File type expectations (plan_hdf vs geom_hdf)
- Common HDF paths in files

**Key Sections**:
- Lines 5-45: Module structure and organization
- Lines 47-114: Class hierarchy and dependencies
- Lines 116-138: Import patterns
- Lines 140-215: Adding new methods (decorator patterns, error handling)

---

### 2. Complete Workflows

**1D Unsteady Results**: `C:\GH\ras-commander\examples\10_1d_hdf_data_extraction.ipynb`

Navigate to this notebook for:
- Cross section time series extraction (`HdfResultsXsec`)
- Output time handling
- Computation message extraction
- 1D hydraulic variables

**2D Unsteady Results**: `C:\GH\ras-commander\examples\11_2d_hdf_data_extraction.ipynb`

Navigate to this notebook for:
- 2D mesh maximum envelopes (`HdfResultsMesh.get_mesh_maximum`)
- Time series at specific locations
- Spatial grids and polygons
- Complete working examples with real data

**Steady Flow Results**: `C:\GH\ras-commander\examples\19_steady_flow_analysis.ipynb`

Navigate to this notebook for:
- Profile detection (`get_steady_profile_names`)
- Water surface elevation extraction by profile
- Multiple profile comparison
- Steady state metadata extraction
- Variable discovery (`list_steady_variables`)

**Dam Breach Results**: `C:\GH\ras-commander\examples\18_breach_results_extraction.ipynb`

Navigate to this notebook for:
- Structure identification (`HdfStruc.list_sa2d_connections`)
- Breach time series (`HdfResultsBreach.get_breach_timeseries`)
- Summary statistics and peak values
- Breach geometry evolution
- Complete breach workflow from detection to visualization

---

### 3. Class Reference

**Core HDF Classes** (all in `ras_commander/hdf/`):

| Class | Purpose | Primary Use |
|-------|---------|-------------|
| **HdfResultsPlan** | Plan-level results | Steady profiles, metadata, plan info, output times, computation messages |
| **HdfResultsMesh** | 2D mesh results | Maximum envelopes, time series, spatial grids |
| **HdfResultsXsec** | Cross section results | 1D time series, longitudinal profiles |
| **HdfResultsBreach** | Breach results | Dam breach time series, summary statistics, geometry evolution |
| **HdfMesh** | Mesh geometry | Cell polygons, face points, perimeter extraction |
| **HdfXsec** | XS geometry | Cross section coordinates, attributes |
| **HdfStruc** | Structure geometry | SA/2D connections, breach capability info |
| **HdfHydraulicTables** | HTAB extraction | Rating curves, property tables |

**Read**: `C:\GH\ras-commander\ras_commander\hdf\AGENTS.md` lines 5-45 for complete class list and organization.

---

### 4. Method Signatures

**Instead of duplicating API documentation here**, use these strategies:

#### Strategy 1: Read Docstrings Directly
```python
from ras_commander import HdfResultsPlan
help(HdfResultsPlan.get_steady_wse)  # Complete parameter docs
```

#### Strategy 2: Check Source Files
Navigate to class files in `C:\GH\ras-commander\ras_commander\hdf\`:
- `HdfResultsPlan.py` - Lines 1-500 contain all steady/unsteady methods
- `HdfResultsMesh.py` - Lines 1-400 contain mesh extraction methods
- `HdfResultsXsec.py` - Lines 1-300 contain cross section methods
- `HdfResultsBreach.py` - Lines 1-400 contain breach methods

#### Strategy 3: Use Example Notebooks
Example notebooks show **actual usage** with real HEC-RAS projects:
- See notebook cells for working code patterns
- Notebook markdown explains each step
- Output cells show expected return structures

---

## Common Workflows (Quick Reference)

### Detect Plan Type

```python
is_steady = HdfResultsPlan.is_steady_plan("02")
plan_info = HdfResultsPlan.get_plan_info("02")
```

**Return**: Boolean for `is_steady_plan()`, DataFrame with program version, run type, etc. for `get_plan_info()`

---

### Steady Flow Extraction

```python
# List profiles
profiles = HdfResultsPlan.get_steady_profile_names("02")

# Extract specific profile
wse = HdfResultsPlan.get_steady_wse("02", profile_name="100 year")

# Extract all profiles
wse_all = HdfResultsPlan.get_steady_wse("02")

# Discover variables
vars_dict = HdfResultsPlan.list_steady_variables("02")
```

**Returns**: List of profile names, DataFrame with River/Reach/Station/WSE columns

**Full Details**: `C:\GH\ras-commander\examples\19_steady_flow_analysis.ipynb`

---

### Unsteady Cross Section Time Series

```python
# Get all variables as xarray Dataset
xsec_data = HdfResultsXsec.get_xsec_timeseries("01")

# Access specific variable
wse_ts = xsec_data["Water_Surface"]  # (time, cross_section)
velocity_ts = xsec_data["Velocity_Total"]

# Select specific cross section
target_xs = "River Reach 12345.6"
wse_at_xs = wse_ts.sel(cross_section=target_xs)
```

**Returns**: xarray Dataset with dimensions (time, cross_section), coordinates for River/Reach/Station

**Full Details**: `C:\GH\ras-commander\examples\10_1d_hdf_data_extraction.ipynb`

---

### 2D Mesh Maximum Envelopes

```python
# Get maximum water surface
max_wse = HdfResultsMesh.get_mesh_maximum("01", variable="Water Surface")

# Get maximum depth
max_depth = HdfResultsMesh.get_mesh_maximum("01", variable="Depth")

# Get maximum velocity
max_vel = HdfResultsMesh.get_mesh_maximum("01", variable="Velocity")
```

**Returns**: GeoDataFrame with columns: cell_id, max_value, max_time, geometry (Polygon)

**Full Details**: `C:\GH\ras-commander\examples\11_2d_hdf_data_extraction.ipynb`

---

### Dam Breach Results

```python
from ras_commander import HdfStruc, HdfResultsBreach

# List structures
structures = HdfStruc.list_sa2d_connections("02")

# Get breach info
breach_info = HdfStruc.get_sa2d_breach_info("02")

# Extract time series
breach_ts = HdfResultsBreach.get_breach_timeseries("02", "Dam")

# Get summary statistics
summary = HdfResultsBreach.get_breach_summary("02", "Dam")
```

**Returns**: DataFrames with structure names, breach timing, flows, geometry evolution

**Full Details**: `C:\GH\ras-commander\examples\18_breach_results_extraction.ipynb`

---

## Integration Patterns

### With hdf-analyst Skill

**Division of Responsibility**:
- **This skill (hecras_extract_results)**: Standard HEC-RAS result extraction using documented API
- **hdf-analyst skill**: Custom HDF path navigation, advanced xarray operations, performance optimization

**Example Handoff**:
```python
# You handle standard extraction
max_wse = HdfResultsMesh.get_mesh_maximum("01", variable="Water Surface")

# Delegate to hdf-analyst for:
# - Custom HDF group navigation
# - Non-standard path queries
# - Advanced xarray transformations
# - Memory optimization for large files
```

---

## Common Issues & Solutions

### Structure Name Mismatches

**Issue**: Structure names differ between plan files and HDF
**Solution**: Always use `HdfStruc.list_sa2d_connections()` to get HDF names
**Example**: Plan file "Dam" might be "BaldEagleCr Dam" in HDF

### Missing Timesteps

**Issue**: Fewer timesteps than expected in results
**Solution**: Check if simulation completed with `HdfResultsPlan.get_compute_messages()`
**Details**: Partial runs will have truncated output

### Large Memory Usage

**Issue**: Mesh time series extraction uses too much RAM
**Solution**: Extract specific timesteps, not all
**Example**: Use `timestep_indices=[0, 50, 100]` instead of `timestep_indices="all"`

### Variable Not Found

**Issue**: Cannot find expected variable in HDF
**Solution**: Use `HdfResultsPlan.list_steady_variables()` or inspect HDF structure directly
**Note**: Variable names differ between HEC-RAS versions

---

## Related Skills

- **hecras_compute_plans**: Run simulations to generate HDF results (prerequisite)
- **hdf-analyst**: Advanced HDF operations and custom analysis (advanced use cases)

---

## Navigation Checklist

When a user asks about HEC-RAS result extraction:

1. **Start Here**: Determine if they need steady or unsteady extraction
2. **Navigate to Example**: Point to relevant notebook (10, 11, 18, or 19)
3. **Check Class Reference**: If they need architectural details, point to `hdf/AGENTS.md`
4. **Read Docstrings**: For parameter details, use `help()` or read source files
5. **Avoid Duplication**: Never replicate content that exists in primary sources

**Primary Sources Are Always More Current**: This skill is a navigation aid. When in doubt, trust the example notebooks and code docstrings over this file.

---

## Summary

**Total Lines**: ~350 (lightweight index)
**Purpose**: Navigate to primary sources, not duplicate them
**When to Use**: User needs HEC-RAS result extraction guidance
**Primary Sources**:
- Architecture: `ras_commander/hdf/AGENTS.md`
- Workflows: `examples/400_1d_hdf_data_extraction.ipynb`, `examples/410_2d_hdf_data_extraction.ipynb`, `examples/401_steady_flow_analysis.ipynb`, `examples/420_breach_results_extraction.ipynb`
- API Details: Code docstrings in `ras_commander/hdf/*.py`

**Key Principle**: Point to authoritative sources, don't replicate them.
