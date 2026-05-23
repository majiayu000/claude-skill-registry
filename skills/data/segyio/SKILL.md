---
name: segyio
description: |
  Read, write, and manipulate SEG-Y seismic data files. Fast C library with Python
  bindings for trace, header, inline, and crossline access. Use when Claude needs to:
  (1) Read/inspect SEG-Y files, (2) Extract trace data or headers, (3) Access 3D survey
  data by inline/crossline, (4) Create new SEG-Y files from arrays, (5) Modify existing
  SEG-Y files, (6) Extract subsets of seismic data, (7) Read/write Seismic Unix format.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Seismic, SEG-Y, Data I/O, Traces, Headers, Segyio, Inlines, Crosslines]
dependencies: [segyio>=1.9.0, numpy]
complements: [obspy, bruges, pyvista]
workflow_role: data-loading
---

# segyio - SEG-Y Seismic Data

## Quick Reference

```python
import segyio

# Read
with segyio.open('seismic.sgy', 'r') as f:
    print(f.tracecount, len(f.samples))
    trace0 = f.trace[0]              # Single trace as numpy array
    data = segyio.tools.collect(f.trace[:])  # All traces

# 3D access (specify inline/xline byte locations)
with segyio.open('seismic.sgy', 'r', iline=189, xline=193) as f:
    inline_100 = f.iline[100]        # 2D array (xlines x samples)
    cube = segyio.tools.cube(f)      # Full 3D cube

# Write
spec = segyio.spec()
spec.samples = samples
spec.tracecount = n_traces
with segyio.create('output.sgy', spec) as f:
    f.trace[0] = data
```

## Key Access Modes

| Mode | Description |
|------|-------------|
| `f.trace[i]` | Sequential trace access by index |
| `f.header[i]` | Trace header access (dict-like) |
| `f.iline[n]` | Inline slice (3D surveys) |
| `f.xline[n]` | Crossline slice (3D surveys) |
| `f.depth_slice[n]` | Horizontal time/depth slice |
| `f.text[0]` | Text header (3200 bytes) |
| `f.bin` | Binary header |

## Essential Operations

### Open and Inspect
```python
with segyio.open('seismic.sgy', 'r') as f:
    print(f"Traces: {f.tracecount}")
    print(f"Samples: {len(f.samples)}")
    print(f"Sample interval: {f.samples[1] - f.samples[0]} ms")
    if f.ilines is not None:
        print(f"Inlines: {f.ilines}")
        print(f"Crosslines: {f.xlines}")
```

### Read Trace Headers
```python
with segyio.open('seismic.sgy', 'r') as f:
    header = f.header[0]
    print(header[segyio.TraceField.INLINE_3D])
    print(header[segyio.TraceField.CDP_X])

    # Get all values for one field
    inlines = f.attributes(segyio.TraceField.INLINE_3D)[:]
```

### Read 3D Data
```python
with segyio.open('seismic.sgy', 'r', iline=189, xline=193) as f:
    inline_data = f.iline[100]       # Shape: (n_xlines, n_samples)
    xline_data = f.xline[200]        # Shape: (n_ilines, n_samples)
    time_slice = f.depth_slice[250]  # Shape: (n_ilines, n_xlines)
    cube = segyio.tools.cube(f)      # Shape: (ilines, xlines, samples)
```

### Read Unstructured Data
```python
# For 2D lines or unsorted data
with segyio.open('seismic.sgy', 'r', ignore_geometry=True) as f:
    data = segyio.tools.collect(f.trace[:])
```

### Create New SEG-Y
```python
import numpy as np

spec = segyio.spec()
spec.samples = np.arange(500) * 4  # 4ms sample rate
spec.tracecount = 100
spec.format = 1  # IBM float

with segyio.create('output.sgy', spec) as f:
    for i in range(100):
        f.trace[i] = data[i]
        f.header[i] = {
            segyio.TraceField.TRACE_SEQUENCE_LINE: i + 1,
        }
```

### Modify Existing File
```python
with segyio.open('seismic.sgy', 'r+') as f:
    f.trace[0] = f.trace[0] * 2.0
    f.header[0][segyio.TraceField.CDP] = 999
```

## Data Formats

| Code | Format |
|------|--------|
| 1 | IBM 4-byte float |
| 2 | 4-byte signed integer |
| 3 | 2-byte signed integer |
| 5 | IEEE 4-byte float |
| 8 | 1-byte signed integer |

## When to Use vs Alternatives

| Tool | Best For |
|------|----------|
| **segyio** | Fast SEG-Y I/O, 3D inline/crossline access, header manipulation |
| **obspy** | Broader seismology: FDSN access, waveform processing, event analysis |
| **segysak** | xarray-based SEG-Y workflows, NetCDF conversion, labeled dimensions |

**Use segyio when** you need fast, low-level access to SEG-Y files -- reading
traces, headers, 3D slices, or creating new SEG-Y files programmatically.

**Use obspy instead** when you need seismological processing beyond file I/O:
instrument response removal, FDSN data fetching, or earthquake analysis.

**Use segysak instead** when you want xarray integration with labeled
dimensions (inline, crossline, time) and easy conversion to NetCDF/Zarr.

## Common Workflows

### Read, inspect, and extract 3D seismic data
```
- [ ] Open file with `segyio.open()`, specify `iline=` and `xline=` byte positions
- [ ] Inspect geometry: trace count, sample count, inline/crossline ranges
- [ ] Read headers to verify coordinate and survey metadata
- [ ] Extract target inline/crossline slices or full cube
- [ ] Apply amplitude scaling or subset extraction as needed
- [ ] Write results to new SEG-Y or export as numpy arrays
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Geometry not detected | Specify `iline=` and `xline=` byte positions |
| Can't read 3D slices | Use `ignore_geometry=True` for unstructured data |
| Wrong inline/xline bytes | Check headers with `f.header[0]` to find correct bytes |
| File not opening | Check file path, permissions, and SEG-Y format validity |

## References

- **[Trace Header Fields](references/header_fields.md)** - Complete header field reference (bytes, types)
- **[Troubleshooting](references/troubleshooting.md)** - Common problems and solutions

## Scripts

- **[scripts/inspect_segy.py](scripts/inspect_segy.py)** - Inspect SEG-Y file structure and geometry
- **[scripts/extract_subset.py](scripts/extract_subset.py)** - Extract subset of traces or inlines
