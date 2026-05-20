---
name: dss_read_boundary-data
allowed-tools: [Read, Grep, Glob]
description: |
  Reads HEC-DSS files (V6 and V7) for boundary condition extraction using
  RasDss class. Handles JVM configuration, HEC Monolith download, catalog
  reading, and time series extraction. Use when working with DSS files,
  extracting boundary data, reading HEC-HMS output, or integrating DSS workflows.
  Triggers: DSS, HEC-DSS, boundary condition, time series, JVM, Java, catalog, pathname, HEC-HMS, Monolith, pyjnius, read DSS, extract DSS, DSS boundary.
version: 1.0.0
---

# Reading DSS Boundary Data

**Primary Source Navigator**: This skill provides a concise entry point to DSS file operations. Complete documentation exists in authoritative sources.

## Quick Reference

```python
from ras_commander import init_ras_project, RasDss

# Initialize project
ras = init_ras_project("path/to/project", "6.6")

# Read DSS catalog
catalog = RasDss.get_catalog("file.dss")

# Extract single time series
df = RasDss.read_timeseries("file.dss", pathname)

# Extract ALL boundary DSS data (recommended)
enhanced = RasDss.extract_boundary_timeseries(
    ras.boundaries_df,
    ras_object=ras
)
```

## Primary Sources (Read These First)

### 1. Module Architecture & Developer Guidance
**Location**: `C:\GH\ras-commander\ras_commander\dss\AGENTS.md`

Read this for:
- Lazy loading architecture (no overhead until first use)
- Three-level lazy loading (package → subpackage → method)
- Public API reference table
- DataFrame metadata structure (`df.attrs`)
- Dependencies (pyjnius, Java, HEC Monolith)
- Adding new DSS methods
- Testing DSS operations
- Common issues and troubleshooting

**Why this is authoritative**: Written by maintainers, updated with code changes, read by developers working on the module.

### 2. Complete Workflow Example
**Location**: `C:\GH\ras-commander\examples\310_dss_boundary_extraction.ipynb`

Read this for:
- Step-by-step extraction workflow
- Real project (BaldEagleCrkMulti2D)
- Catalog reading examples
- Single time series extraction
- Batch extraction with `extract_boundary_timeseries()`
- Plotting DSS boundary data
- Exporting results to CSV
- Accessing extracted DataFrames

**Why this is authoritative**: Tested with real HEC-RAS projects, serves as functional test, maintained alongside library.

### 3. Source Code & Docstrings
**Location**: `C:\GH\ras-commander\ras_commander\dss\RasDss.py`

Read this for:
- Complete method signatures
- Parameter types and defaults
- Return value structures
- Error handling patterns
- Implementation details

**Why this is authoritative**: Source code is always correct, docstrings updated with each release.

## When to Use This Skill

Use when:
- Working with HEC-DSS files (V6 or V7)
- Extracting boundary conditions from DSS
- Reading HEC-HMS model output
- Integrating DSS workflows with HEC-RAS
- Need to catalog DSS file contents
- Converting DSS data to pandas DataFrames

## Technology Overview

### HEC-DSS Format
- **DSS** = Data Storage System (binary format)
- Used by HEC-HMS, HEC-ResSim, HEC-FIA
- Versions: V6 (older) and V7 (current)
- Data identified by **pathname** (7-part string)

### DSS Pathname Format
```
/A/B/C/D/E/F/
```
- **A**: Project or basin name
- **B**: Location (e.g., gauge, river station)
- **C**: Parameter (FLOW, STAGE, PRECIP, etc.)
- **D**: Start date (e.g., 01JAN2000)
- **E**: Time interval (15MIN, 1HOUR, 1DAY, etc.)
- **F**: Version or scenario (RUN:SCENARIO, GAGE, OBS, etc.)

Example:
```
//BALD EAGLE 40/FLOW/01JAN1999/15MIN/RUN:PMF-EVENT/
```

## Lazy Loading Architecture

### No Overhead Until First Use

See `ras_commander/dss/AGENTS.md` for complete details.

**Three-level lazy loading**:

1. **Package Import**: Lightweight, no Java loaded
   ```python
   from ras_commander import RasDss  # Fast, no JVM
   ```

2. **First Method Call**: Configures JVM, downloads Monolith (~20 MB, one-time)
   ```python
   catalog = RasDss.get_catalog("file.dss")  # Triggers setup
   ```

3. **Subsequent Calls**: Uses cached JVM and libraries
   ```python
   df = RasDss.read_timeseries(...)  # Fast, reuses JVM
   ```

### Dependencies
**Required** (must install manually):
```bash
pip install pyjnius
```

**Required** (system):
- Java JRE or JDK 8+ (set JAVA_HOME)

**Auto-downloaded**:
- HEC Monolith libraries (~20 MB) to `~/.ras-commander/dss/`

## Core Methods

See `ras_commander/dss/AGENTS.md` for complete API reference table.

### Essential Methods

1. **`get_catalog(dss_file)`** - List all paths in DSS file
   - Returns: `List[str]` of DSS pathnames
   - Use: Explore DSS file contents

2. **`read_timeseries(dss_file, pathname)`** - Extract single time series
   - Returns: `DataFrame` with DatetimeIndex and 'value' column
   - Metadata in `df.attrs` (pathname, units, type, interval, dss_file)
   - Use: Extract specific boundary data

3. **`extract_boundary_timeseries(boundaries_df, ras_object)`** - Extract ALL DSS boundaries
   - Returns: Enhanced DataFrame with 'dss_timeseries' column
   - Automatically processes all DSS-defined boundaries
   - Use: **Recommended** for complete boundary extraction

4. **`get_info(dss_file)`** - Quick file summary
   - Returns: `Dict` with filename, size, total_paths, sample_paths
   - Use: Validate DSS file before full extraction

5. **`read_multiple_timeseries(dss_file, pathnames)`** - Batch extract
   - Returns: `Dict[str, DataFrame]` mapping pathname to data
   - Use: Extract specific set of paths efficiently

## Common Workflows

### Workflow 1: Read Catalog and Extract Single Path

```python
# List available data
catalog = RasDss.get_catalog("file.dss")
flow_paths = [p for p in catalog if '/FLOW/' in p]

# Extract specific path
df = RasDss.read_timeseries("file.dss", flow_paths[0])
print(f"Units: {df.attrs['units']}")
print(f"Points: {len(df)}")
```

### Workflow 2: Extract ALL Boundary Data (Recommended)

```python
from ras_commander import init_ras_project, RasDss

# Initialize project
ras = init_ras_project("project_path", "6.6")

# Extract all DSS boundary data
enhanced = RasDss.extract_boundary_timeseries(
    ras.boundaries_df,
    ras_object=ras
)

# Access extracted data
for idx, row in enhanced.iterrows():
    if row['Use DSS'] and row['dss_timeseries'] is not None:
        df = row['dss_timeseries']
        print(f"{row['bc_type']}: {len(df)} points")
```

### Workflow 3: Plot DSS Boundary

```python
import matplotlib.pyplot as plt

# Get DSS boundary
dss_boundaries = enhanced[enhanced['Use DSS'] == True]
first_dss = dss_boundaries.iloc[0]

# Plot
df = first_dss['dss_timeseries']
df['value'].plot(figsize=(12, 4))
plt.title(f"{first_dss['bc_type']} - {first_dss['river_reach_name']}")
plt.ylabel(f"Flow ({df.attrs['units']})")
plt.grid(True)
plt.show()
```

## Error Handling

See `ras_commander/dss/AGENTS.md` for complete troubleshooting guide.

### Common Errors

**1. pyjnius Not Installed**
```
ImportError: pyjnius is required for DSS file operations.
```
**Fix**: `pip install pyjnius`

**2. Java Not Found**
```
RuntimeError: JAVA_HOME not set and Java not found automatically.
```
**Fix**: Install Java JRE/JDK 8+ and set JAVA_HOME

**3. JVM Already Started**
```
RuntimeError: JVM configuration already done.
```
**Fix**: Restart Python process or notebook kernel

**4. DSS File Not Found**
```
FileNotFoundError: DSS file not found: ...
```
**Fix**: Use absolute paths or resolve relative to project directory

### Robust Pattern

```python
from pathlib import Path

try:
    dss_file = Path("file.dss").resolve()
    if not dss_file.exists():
        raise FileNotFoundError(f"DSS file not found: {dss_file}")

    catalog = RasDss.get_catalog(dss_file)
    print(f"Success: {len(catalog)} paths")

except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install: pip install pyjnius")

except RuntimeError as e:
    print(f"Java/JVM error: {e}")
    print("Check JAVA_HOME and Java installation")
```

## Complete Documentation

**DO NOT read the reference/ or examples/ folders in this skill directory** - they contain outdated duplicated content.

**Always prefer primary sources**:

1. **Module architecture**: `ras_commander/dss/AGENTS.md`
2. **Complete workflow**: `examples/310_dss_boundary_extraction.ipynb`
3. **API details**: `ras_commander/dss/RasDss.py` docstrings

## Key Takeaways

1. **Lazy Loading**: No overhead until first DSS method call
2. **Auto-Download**: HEC Monolith installed automatically (~20 MB, one-time)
3. **Unified API**: DSS and manual boundaries in same DataFrame
4. **One-Call Extraction**: `extract_boundary_timeseries()` handles all DSS data
5. **Metadata Preserved**: Units, pathname, interval in `df.attrs`
6. **V6 and V7**: Both DSS versions supported
7. **Primary Sources**: Always read AGENTS.md and notebook 310 for authoritative guidance

## Version History

- **v1.0.0**: Refactored to lightweight navigator (points to primary sources)
- **v0.82.0**: Initial RasDss implementation
- **v0.86.0**: Moved to `dss/` subpackage with lazy loading
