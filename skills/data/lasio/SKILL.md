---
name: lasio
description: |
  Read, write, and manipulate LAS (Log ASCII Standard) well log files for borehole
  geophysical and petrophysical data. Use when Claude needs to: (1) Read/parse LAS
  1.2 or 2.0 files, (2) Extract well headers or curve data, (3) Convert LAS to
  DataFrame/CSV/Excel, (4) Create new LAS files from arrays, (5) Modify existing
  LAS files, (6) Handle problematic or malformed LAS files, (7) Batch process
  multiple well files.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Well Logs, LAS, Petrophysics, Data I/O, Lasio, CWLS, Wireline, Borehole]
dependencies: [lasio>=0.30]
complements: [welly, petropy, striplog]
workflow_role: data-loading
---

# lasio - LAS Well Log Files

## Quick Reference

```python
import lasio

# Read
las = lasio.read("well.las")

# Access data
df = las.df()                    # DataFrame (depth as index)
gr = las['GR']                   # Single curve as numpy array
depth = las['DEPT']

# Well info
well_name = las.well['WELL'].value
uwi = las.well['UWI'].value

# Write
las.write('output.las')
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `LASFile` | Main container - holds headers, curves, data |
| `CurveItem` | Single curve with mnemonic, unit, data array |
| `HeaderItem` | Header entry (mnemonic, unit, value, descr) |

## Essential Operations

### Read and Inspect
```python
las = lasio.read("well.las")
print(las.curves.keys())         # Available curves
print(las.well)                  # Well section headers
print(las.version)               # LAS version info
```

### Access Curve Data
```python
# As numpy arrays
gr = las['GR']
depth = las['DEPT']

# With metadata
curve = las.curves['GR']
print(curve.unit, curve.descr)   # 'GAPI', 'Gamma Ray'
```

### Create New LAS
```python
import numpy as np

las = lasio.LASFile()
las.well['WELL'] = lasio.HeaderItem('WELL', value='Test-1')
las.well['UWI'] = lasio.HeaderItem('UWI', value='12345678901234')

depth = np.arange(1000, 2000, 0.5)
las.append_curve('DEPT', depth, unit='M', descr='Depth')
las.append_curve('GR', gr_data, unit='GAPI', descr='Gamma Ray')
las.write('output.las')
```

### Modify Existing
```python
las = lasio.read("well.las")
las.append_curve('GR_NORM', las['GR'] / 150, unit='V/V')
del las.curves['BAD_CURVE']
las.well['WELL'].value = 'New Name'
las.write('modified.las')
```

### Handle Problematic Files
```python
# Ignore header errors
las = lasio.read("messy.las", ignore_header_errors=True)

# Check null value
null_val = las.well['NULL'].value  # Usually -999.25
```

## Null Value Handling

LAS files use a specific null value (typically -999.25). Always check and handle:
```python
import numpy as np
null_val = float(las.well['NULL'].value)
df = las.df().replace(null_val, np.nan)
```

## Batch Processing

```python
from pathlib import Path

for path in Path('wells/').glob('*.las'):
    las = lasio.read(path)
    df = las.df()
    # Process...
```

## When to Use vs Alternatives

| Tool | Best For |
|------|----------|
| **lasio** | Direct LAS file I/O, header manipulation, format conversion |
| **welly** | Higher-level well analysis, curve processing, multi-well projects |
| **dlisio** | DLIS/RP66 binary format files (not LAS) |

**Use lasio when** you need low-level control over LAS file reading/writing,
need to handle malformed files, or want to programmatically build LAS files.

**Use welly instead** when you need curve processing (despike, normalize),
multi-well project management, or formation tops. Welly uses lasio internally.

**Use dlisio instead** when your data is in DLIS format. DLIS files are binary,
support multi-frame data and array logs -- lasio cannot read them.

## Common Workflows

### Read, QC, and export well log data
```
- [ ] Read LAS file with `lasio.read()`, handle encoding if needed
- [ ] Inspect curves: `las.curves.keys()` and well headers
- [ ] Replace null values: `df.replace(null_val, np.nan)`
- [ ] Validate depth range and sample interval
- [ ] Check for missing curves or anomalous values
- [ ] Export to DataFrame with `las.df()` or write cleaned LAS
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Encoding errors | `lasio.read(f, encoding='latin-1')` |
| Missing curves | Check `las.curves.keys()` first |
| Header errors | Use `ignore_header_errors=True` |
| Wrong null value | Check `las.well['NULL'].value` |

## References

- **[Curve Mnemonics](references/curve_mnemonics.md)** - Standard curve names and units
- **[Troubleshooting](references/troubleshooting.md)** - Common problems and solutions
- **[LAS File Structure](references/file_structure.md)** - Detailed format specification

## Scripts

- **[scripts/validate_las.py](scripts/validate_las.py)** - Validate LAS file format
- **[scripts/las_to_csv.py](scripts/las_to_csv.py)** - Convert LAS to CSV
- **[scripts/merge_curves.py](scripts/merge_curves.py)** - Merge curves from multiple files
