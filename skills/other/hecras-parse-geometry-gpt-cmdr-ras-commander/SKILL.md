---
name: hecras_parse_geometry
allowed-tools: [Read, Grep, Glob]
description: |
  Parses and modifies HEC-RAS plain text geometry files (.g##) using fixed-width
  FORTRAN format. Handles cross sections, storage areas, bridges, culverts,
  lateral structures, and Manning's n tables. Use when reading geometry files,
  modifying cross sections, updating roughness, extracting structure data,
  parsing .g## files, working with XS station-elevation data, or analyzing
  bridge/culvert geometry. Keywords: parse, geometry, .g##, cross section, XS,
  Manning's n, bridge, culvert, storage, fixed-width, lateral structure,
  inline weir, 2D land cover, bank stations.
---

# Parsing HEC-RAS Geometry Files

**Primary Sources (navigate to these for details)**:
- **Implementation guide**: `ras_commander/geom/AGENTS.md` (parsing algorithms, API reference)
- **Working examples**: `examples/201_1d_plaintext_geometry.ipynb` and `examples/202_2d_plaintext_geometry.ipynb` (comprehensive demonstrations)

This skill provides quick-reference patterns for common tasks. For implementation details, parsing algorithms, and complete API documentation, see the primary sources above.

## Quick Start Patterns

### List Cross Sections

```python
from ras_commander.geom.GeomCrossSection import GeomCrossSection

# List all cross sections in file
xs_df = GeomCrossSection.get_cross_sections("model.g01")
# Returns: DataFrame with River, Reach, RS, NodeName

# Filter by river/reach
xs_df = GeomCrossSection.get_cross_sections(
    "model.g01",
    river="Ohio River",
    reach="Reach 1"
)
```

### Read Cross Section Geometry

```python
# Get station-elevation profile
df = GeomCrossSection.get_station_elevation(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000"
)
# Returns: DataFrame with Station, Elevation columns

# Get bank stations
banks = GeomCrossSection.get_bank_stations(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000"
)
# Returns: dict with BankLeft, BankRight keys
```

### Modify Cross Section

```python
# Read current geometry
df = GeomCrossSection.get_station_elevation(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000"
)

# Modify elevations (e.g., lower channel 2 feet)
df.loc[df['Station'].between(100, 200), 'Elevation'] -= 2.0

# Get bank stations
banks = GeomCrossSection.get_bank_stations(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000"
)

# Write back (creates .bak backup, handles bank interpolation)
GeomCrossSection.set_station_elevation(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000",
    df,
    bank_left=banks['BankLeft'],
    bank_right=banks['BankRight']
)
```

### Update 2D Manning's n

```python
from ras_commander.geom.GeomLandCover import GeomLandCover

# Read land cover table
lc_df = GeomLandCover.get_base_mannings_n("model.g01")
# Returns: DataFrame with LandCoverID, ManningsN

# Modify roughness
lc_df.loc[lc_df['LandCoverID'] == 42, 'ManningsN'] = 0.15

# Write back (creates .bak backup)
GeomLandCover.set_base_mannings_n("model.g01", lc_df)
```

### Extract Storage Areas

```python
from ras_commander.geom.GeomStorage import GeomStorage

# List storage areas (exclude 2D flow areas)
storage_areas = GeomStorage.get_storage_areas("model.g01", exclude_2d=True)

# Get elevation-volume curve
df = GeomStorage.get_elevation_volume("model.g01", "Detention Basin 1")
# Returns: DataFrame with Elevation, Area, Volume columns
```

### Read Bridge Geometry

```python
from ras_commander.geom.GeomBridge import GeomBridge

# List all bridges
bridges = GeomBridge.get_bridges("model.g01")

# Get bridge deck geometry
deck_df = GeomBridge.get_deck(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000"
)
# Returns: DataFrame with Station, Elevation, Width, Distance

# Get pier data
piers_df = GeomBridge.get_piers(
    "model.g01",
    "Ohio River",
    "Reach 1",
    "1000"
)
# Returns: DataFrame with Station, Width, CD coefficients
```

### Read Culverts

```python
from ras_commander.geom.GeomCulvert import GeomCulvert

# Get all culverts in file
culverts_df = GeomCulvert.get_all("model.g01")
# Returns: DataFrame with River, Reach, RS, CulvertNum, Shape, etc.

# Filter by river/reach
culverts_df = GeomCulvert.get_all(
    "model.g01",
    river="Ohio River",
    reach="Reach 1"
)

# Culvert shape codes:
# 1=Circular, 2=Box, 3=Pipe Arch, 4=Ellipse, 5=Arch
# 6=Semi-Circle, 7=Low Profile Arch, 8=High Profile Arch, 9=Con Span
```

## Module Organization

| Module | Class | Purpose |
|--------|-------|---------|
| GeomParser | `GeomParser` | Fixed-width format parsing utilities |
| GeomCrossSection | `GeomCrossSection` | 1D cross section operations |
| GeomStorage | `GeomStorage` | Storage area elevation-volume curves |
| GeomLandCover | `GeomLandCover` | 2D Manning's n land cover tables |
| GeomLateral | `GeomLateral` | Lateral structures and SA/2D connections |
| GeomInlineWeir | `GeomInlineWeir` | Inline weir structures |
| GeomBridge | `GeomBridge` | Bridge/culvert structure geometry |
| GeomCulvert | `GeomCulvert` | Culvert data extraction |
| GeomPreprocessor | `GeomPreprocessor` | Geometry preprocessor file management |

See `ras_commander/geom/AGENTS.md` for complete API documentation.

## Critical Implementation Notes

### Bank Station Interpolation
**Handled automatically** - `set_station_elevation()` ensures bank stations appear as exact points:
- If bank station exists in data: uses it directly
- If bank station missing: interpolates elevation and inserts point
- You don't need to manually interpolate bank stations

### 450 Point Limit
HEC-RAS enforces maximum 450 points per cross section:
```python
# Validate before writing
if len(df) > 450:
    raise ValueError(f"Cross section has {len(df)} points (max 450)")
```

### Case-Sensitive Identifiers
River, Reach, and RS are **case-sensitive**:
```python
# These are DIFFERENT:
GeomCrossSection.get_station_elevation(geom_file, "Ohio River", ...)
GeomCrossSection.get_station_elevation(geom_file, "ohio river", ...)
```
Use exact casing from `get_cross_sections()` DataFrame.

### Automatic Backups
All write operations create `.bak` files:
```
Original: model.g01
Modified: model.g01
Backup:   model.g01.bak
```

### Fixed-Width Format
HEC-RAS uses FORTRAN-era formatting:
- **Column width**: 8 characters per value
- **Values per line**: 10 values (80 characters total)
- **Count interpretation**: `#Sta/Elev= 40` means 40 PAIRS (80 total values)

See `ras_commander/geom/AGENTS.md` for parsing algorithm details.

## Common Workflows

### Batch Modify All Cross Sections

```python
# Get list of all cross sections
xs_df = GeomCrossSection.get_cross_sections("model.g01")

# Iterate through each
for _, row in xs_df.iterrows():
    river = row['River']
    reach = row['Reach']
    rs = row['RS']

    # Read geometry
    df = GeomCrossSection.get_station_elevation("model.g01", river, reach, rs)

    # Apply modification (e.g., raise all elevations 1 foot)
    df['Elevation'] += 1.0

    # Get bank stations
    banks = GeomCrossSection.get_bank_stations("model.g01", river, reach, rs)

    # Write back
    GeomCrossSection.set_station_elevation(
        "model.g01",
        river,
        reach,
        rs,
        df,
        bank_left=banks['BankLeft'],
        bank_right=banks['BankRight']
    )
```

### Extract All Storage Curves

```python
from ras_commander.geom.GeomStorage import GeomStorage

# List storage areas (exclude 2D flow areas)
storage_areas = GeomStorage.get_storage_areas("model.g01", exclude_2d=True)

# Extract elevation-volume curves
for area_name in storage_areas:
    df = GeomStorage.get_elevation_volume("model.g01", area_name)
    print(f"{area_name}: {len(df)} elevation points")
    # df has columns: Elevation, Area, Volume
```

### Survey All Culverts

```python
from ras_commander.geom.GeomCulvert import GeomCulvert

# Get all culverts in file
culverts_df = GeomCulvert.get_all("model.g01")

# Interpret shape codes
shape_map = {
    1: "Circular", 2: "Box", 3: "Pipe Arch", 4: "Ellipse",
    5: "Arch", 6: "Semi-Circle", 7: "Low Profile Arch",
    8: "High Profile Arch", 9: "Con Span"
}

for _, row in culverts_df.iterrows():
    shape_name = shape_map[row['Shape']]
    print(f"{row['River']} - {row['RS']}: {shape_name} culvert")
```

## Error Handling

### File Not Found
```python
from pathlib import Path

# Verify file exists
if not Path(geom_file).exists():
    raise FileNotFoundError(f"Geometry file not found: {geom_file}")
```

### Invalid River/Reach/RS
```python
# List available features first
xs_df = GeomCrossSection.get_cross_sections(geom_file)
print(xs_df[['River', 'Reach', 'RS']])

# Use exact casing
df = GeomCrossSection.get_station_elevation(
    geom_file,
    "Ohio River",  # Exact case
    "Reach 1",     # Exact case
    "1000"         # Exact string
)
```

### Point Limit Exceeded
```python
# Validate before writing
if len(df) > 450:
    # Option 1: Simplify geometry
    from scipy.interpolate import interp1d
    f = interp1d(df['Station'], df['Elevation'])
    new_stations = np.linspace(df['Station'].min(), df['Station'].max(), 400)
    df = pd.DataFrame({
        'Station': new_stations,
        'Elevation': f(new_stations)
    })

    # Option 2: Raise error for user to handle
    raise ValueError(f"Cross section has {len(df)} points (max 450)")
```

## Primary Sources

**For complete details, navigate to**:

1. **`ras_commander/geom/AGENTS.md`**
   - Parsing algorithms (fixed-width format, count interpretation)
   - Complete API reference for all 9 modules
   - Technical patterns and implementation notes
   - Culvert shape codes table
   - Deprecated class mappings

2. **`examples/201_1d_plaintext_geometry.ipynb`** and **`examples/202_2d_plaintext_geometry.ipynb`**
   - Working code demonstrations for all modules
   - Real HEC-RAS project examples
   - Output visualizations
   - Error handling examples
   - Integration with other ras-commander features

## Import Pattern

All classes use static methods - no instantiation required:

```python
from ras_commander.geom.GeomCrossSection import GeomCrossSection
from ras_commander.geom.GeomStorage import GeomStorage
from ras_commander.geom.GeomBridge import GeomBridge
from ras_commander.geom.GeomCulvert import GeomCulvert
from ras_commander.geom.GeomLandCover import GeomLandCover

# Use directly (no instantiation)
xs_df = GeomCrossSection.get_cross_sections("model.g01")
```

## See Also

- **CLAUDE.md**: Architecture section on geometry parsing (lines 165-220)
- **Subagent**: `.claude/agents/geometry-parser/SUBAGENT.md` - For delegation
